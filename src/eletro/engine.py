"""Motor de calculo v1 para moradia: Project + perfil -> Resultado (pontos, circuitos, verificacoes).
Cada linha traz estado e fonte. NADA aqui e documento assinavel: e rascunho."""
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from .schema.project import Project
from .schema.dynamic import resolve
from .calc.cabos import ib_mono, next_in, size_for, K1_PVC, K2_EMBEBIDOS
from .calc.comprimentos import comprimento_circuito
from .rules.dotacao import pontos_divisao
from .rules.circuitos import agrupar_sequencial
from .rules.potencia import compartimentos, potencia_minima_kva
from .rules.quadro import potencia_a_contratar, calibre_geral_a, calibre_ddr, pe_mm2, modulos
from .rules.ited import dotacao_ited

CUMPRE, NAO_CUMPRE, CONVENCAO, POR_CONFIRMAR, AVISO = "CUMPRE", "NAO_CUMPRE", "CONVENCAO", "POR_CONFIRMAR", "AVISO"

class Verificacao(BaseModel):
    ref: str
    estado: str
    texto: str

class Circuito(BaseModel):
    id: str
    tipo: str
    divisoes: list[str]
    pontos: int
    ib_a: float
    in_a: int
    s_mm2: Optional[float] = None
    iz_a: Optional[float] = None
    comprimento_m: float
    comprimento_origem: str   # "ESTIMADO" ou "MANUAL"
    queda_pct: Optional[float] = None
    queda_max_pct: float
    erro: Optional[str] = None
    p_inst_w: float = 0
    p_calc_w: float = 0
    curva: str = ""
    ddr: str = ""
    pe_mm2: Optional[float] = None

class Quadro(BaseModel):
    p_inst_w: float
    p_calc_w: float
    s_calc_kva: float
    potencia_a_contratar_kva: float
    geral_in_a: int
    poder_corte_ka: float
    ddr: list[dict]
    n_mcb: int
    modulos: dict

class Resultado(BaseModel):
    projeto: str
    revisao: int
    pontos: dict[str, dict]
    circuitos: list[Circuito]
    potencia_minima_kva: float
    n_compartimentos: int
    verificacoes: list[Verificacao]
    pressupostos: list[str]
    quadro: Optional[Quadro] = None
    ited: dict = {}

def s_min_de(c, cfg) -> float:
    return cfg["s_min_mm2"].get("iluminacao" if c.tipo == "iluminacao" else "tomadas" if c.tipo == "tomadas"
                                 else "avac" if c.tipo == "climatizacao" else c.tipo, 2.5)

def calcular(p0: Project, perfil: dict, ited_cfg: Optional[dict] = None) -> Resultado:
    p, conflitos = resolve(p0)
    v: list[Verificacao] = []
    for c in conflitos:
        v.append(Verificacao(ref="overrides", estado=AVISO, texto=c))
    for r in p.unconfirmed():
        v.append(Verificacao(ref="dados", estado=AVISO, texto=f"Divisao {r.id} ({r.name}) por confirmar"))

    cond, cfg = perfil["condicoes_instalacao"], perfil["circuitos"]
    k1, k2 = K1_PVC[cond["temperatura_ambiente_c"]], K2_EMBEBIDOS[cond["n_circuitos_agrupados"]]
    fator, vert = perfil["comprimentos"]["fator_trajeto"], perfil["comprimentos"]["vertical_m"]
    q_max = perfil["queda_max_pct"]

    pontos = {r.id: pontos_divisao(r, perfil) for r in p.rooms}
    v.append(Verificacao(ref=perfil["id"], estado=CONVENCAO,
                         texto="Numero de pontos por divisao e convencao de projeto (RTIEBT nao o fixa)"))
    circuitos: list[Circuito] = []

    sim, qd = perfil["simultaneidade"], perfil["quadro"]

    def juntar(cid, tipo, grupo, ib, inn, s_min, q_lim, p_inst, fsim):
        rids = [g[0] for g in grupo]
        npts = sum(g[1] for g in grupo)
        manual = p.circuit_length_m.get(cid)
        L = manual if manual is not None else comprimento_circuito(p, rids, fator, vert)
        c = dict(id=cid, tipo=tipo, divisoes=rids, pontos=npts, ib_a=round(ib, 3), in_a=inn,
                 comprimento_m=round(L, 2), comprimento_origem="MANUAL" if manual is not None else "ESTIMADO",
                 queda_max_pct=q_lim, p_inst_w=round(p_inst, 1), p_calc_w=round(p_inst * fsim, 1),
                 curva=qd["curvas"].get(tipo, qd["curvas"]["outros"]))
        try:
            s = size_for(ib, inn, L, k1=k1, k2=k2, max_drop_pct=q_lim, metodo=cond["metodo"], min_s_mm2=s_min)
            c.update(s_mm2=s["s_mm2"], iz_a=round(s["iz"], 2), queda_pct=round(s["drop_pct"], 3), pe_mm2=pe_mm2(s["s_mm2"]))
        except ValueError as e:
            c["erro"] = str(e)
        circuitos.append(Circuito(**c))

    # Iluminacao e tomadas: agrupamento sequencial, max. 8 pontos (801.5.3)
    mx = cfg["max_pontos_por_circuito"]
    luz = agrupar_sequencial([(r.id, pontos[r.id]["luz"]) for r in p.rooms], mx)
    for i, g in enumerate(luz, 1):
        n = sum(x[1] for x in g)
        pw = n * cfg["iluminacao"]["w_por_ponto"]
        juntar(f"ILUM-{i}", "iluminacao", g, pw / 230.0, cfg["iluminacao"]["in_a"],
               cfg["s_min_mm2"]["iluminacao"], q_max["iluminacao"], pw, sim["iluminacao"])
    tom = agrupar_sequencial([(r.id, pontos[r.id]["tomadas"]) for r in p.rooms], mx)
    for i, g in enumerate(tom, 1):
        inn = cfg["tomadas"]["in_a"]
        juntar(f"TOM-{i}", "tomadas", g, float(inn), inn, cfg["s_min_mm2"]["tomadas"], q_max["outros"],
               sim["tomada_circuito_w"], sim["tomadas"])

    # Equipamentos dedicados; climatizacao (avac) agrupada ate 5 aparelhos por circuito (801.5.3)
    avac = [e for e in p.equipment if e.kind == "avac"]
    for k in range(0, len(avac), cfg["max_aparelhos_climatizacao_por_circuito"]):
        bloco = avac[k:k + cfg["max_aparelhos_climatizacao_por_circuito"]]
        ib = ib_mono(sum(e.power_w for e in bloco)); inn = next_in(ib)
        juntar(f"AVAC-{k // cfg['max_aparelhos_climatizacao_por_circuito'] + 1}", "climatizacao",
               [(e.room_id, 1) for e in bloco], ib, inn, cfg["s_min_mm2"]["avac"], q_max["outros"],
               sum(e.power_w for e in bloco), sim["climatizacao"])
    for e in p.equipment:
        if e.kind == "avac":
            continue
        ib = ib_mono(e.power_w); inn = next_in(ib)
        juntar(f"EQ-{e.id}", e.kind, [(e.room_id, 1)], ib, inn, cfg["s_min_mm2"].get(e.kind, 2.5), q_max["outros"],
               e.power_w, sim["equipamento"])

    # Verificacoes regulamentares
    for c in circuitos:
        if c.tipo in ("iluminacao", "tomadas"):
            ok = c.pontos <= mx
            v.append(Verificacao(ref="RTIEBT 801.5.3", estado=CUMPRE if ok else NAO_CUMPRE,
                                 texto=f"{c.id}: {c.pontos} pontos (max. {mx})"))
        if c.erro:
            v.append(Verificacao(ref="RTIEBT 523/525", estado=NAO_CUMPRE, texto=f"{c.id}: {c.erro}"))
        else:
            v.append(Verificacao(ref="RTIEBT 433/523", estado=POR_CONFIRMAR,
                                 texto=f"{c.id}: Ib {c.ib_a} A <= In {c.in_a} A <= Iz {c.iz_a} A, {c.s_mm2} mm2 "
                                       f"(tabelas da edicao 2000)"))
            if c.s_mm2 > s_min_de(c, cfg):
                v.append(Verificacao(ref="projeto", estado=AVISO,
                                     texto=f"{c.id}: seccao aumentada para {c.s_mm2} mm2 (minimo {s_min_de(c, cfg)} mm2) por queda de tensao/aquecimento"))
            v.append(Verificacao(ref="RTIEBT 525 Q.52O", estado=POR_CONFIRMAR if c.queda_pct <= c.queda_max_pct else NAO_CUMPRE,
                                 texto=f"{c.id}: queda {c.queda_pct:.2f}% (max. {c.queda_max_pct}%), comprimento {c.comprimento_origem}"))
    ncomp = compartimentos(p, perfil["compartimentos_nao_contam"])
    pmin = potencia_minima_kva(ncomp, p.supply.phases)
    v.append(Verificacao(ref="RTIEBT 801.5.2.2", estado=CONVENCAO,
                         texto=f"{ncomp} compartimentos (criterio de contagem e convencao) -> potencia minima {pmin:.2f} kVA"))
    cont = p.supply.contracted_kva
    if cont is not None:
        v.append(Verificacao(ref="RTIEBT 801.5.2.2", estado=CUMPRE if cont >= pmin else NAO_CUMPRE,
                             texto=f"potencia contratada {cont} kVA vs minima {pmin:.2f} kVA"))
        if p.supply.phases == 1 and cont > 10.35:
            v.append(Verificacao(ref="RTIEBT 801.1.1.3.3", estado=AVISO,
                                 texto="monofasico acima de 10,35 kVA so com acordo previo do distribuidor"))
    # ---- Quadro electrico (monofasico) ----
    quadro = None
    if p.supply.phases != 1:
        v.append(Verificacao(ref="projeto", estado=AVISO, texto="Trifasico ainda nao suportado no motor v1: quadro nao calculado"))
    else:
        validos = [c for c in circuitos if not c.erro]
        p_inst = sum(c.p_inst_w for c in validos); p_calc = sum(c.p_calc_w for c in validos)
        s_calc = p_calc / sim["cos_phi"] / 1000.0
        rec = potencia_a_contratar(s_calc, pmin, 1, qd["potencias_normalizadas_kva"])
        v.append(Verificacao(ref=perfil["id"], estado=CONVENCAO,
                             texto=f"Potencia de calculo {p_calc:.0f} W ({s_calc:.2f} kVA) com simultaneidade convencionada; potencia a contratar recomendada {rec:.2f} kVA"))
        ref_kva = cont if cont is not None else rec
        if cont is not None and cont < s_calc:
            v.append(Verificacao(ref=perfil["id"], estado=AVISO,
                                 texto=f"potencia contratada {cont} kVA inferior a potencia de calculo {s_calc:.2f} kVA (convencao de simultaneidade)"))
        in_geral = calibre_geral_a(ref_kva, 1)
        pdc = qd["poder_corte_assumido_ka"]
        if p.supply.icc_ka is None:
            v.append(Verificacao(ref="RTIEBT 434", estado=POR_CONFIRMAR,
                                 texto=f"Poder de corte {pdc} kA assumido: pedir a Icc no ponto de ligacao a e-Redes"))
        else:
            v.append(Verificacao(ref="RTIEBT 434", estado=CUMPRE if pdc >= p.supply.icc_ka else NAO_CUMPRE,
                                 texto=f"poder de corte {pdc} kA vs Icc {p.supply.icc_ka} kA"))
        v.append(Verificacao(ref="RTIEBT 433/434", estado=AVISO,
                             texto="Disparo magnetico (Icc minima, Zs) e I2t NAO verificados: faltam impedancias e Icc; curvas B/C sao convencao"))
        # DDR 30 mA: zonas humidas separadas (convenção); In >= geral (protecao contra sobrecarga a montante)
        hum = set(qd["ddr"]["zonas_humidas"]); uso = {r.id: r.use for r in p.rooms}
        for c in circuitos:
            if c.erro: continue
            humido = c.tipo not in ("iluminacao", "tomadas") or all(uso[r] in hum for r in c.divisoes)
            c.ddr = "DDR-2" if humido else "DDR-1"
        in_ddr = calibre_ddr(in_geral, qd["ddr"]["calibres_a"])
        ddr = []
        for nome in ("DDR-1", "DDR-2"):
            cs = [c for c in validos if c.ddr == nome]
            if cs:
                ddr.append({"id": nome, "in_a": in_ddr, "idn_ma": qd["ddr"]["ina_mA"], "tipo": qd["ddr"]["tipo"],
                            "circuitos": [c.id for c in cs], "corrente_calculo_a": round(sum(c.p_calc_w for c in cs) / 230.0, 1)})
        v.append(Verificacao(ref="RTIEBT 801.5.9", estado=CUMPRE if all(c.ddr for c in validos) else NAO_CUMPRE,
                             texto="todos os circuitos protegidos por diferencial"))
        v.append(Verificacao(ref="RTIEBT 412.5/531.2.6/701", estado=CONVENCAO,
                             texto=f"DDR {qd['ddr']['ina_mA']} mA tipo {qd['ddr']['tipo']} em todos os circuitos (30 mA exigido em casas de banho e exterior; no resto e convencao)"))
        if p.supply.r_terra_ohm is None:
            v.append(Verificacao(ref="RTIEBT 801.5.6.1", estado=POR_CONFIRMAR, texto="Resistencia de terra por medir (exigido < 100 ohm com disjuntor de entrada diferencial)"))
        else:
            ra, idn = p.supply.r_terra_ohm, qd["ddr"]["ina_mA"] / 1000.0
            v.append(Verificacao(ref="RTIEBT 801.5.6.1 / 413.1.4", estado=CUMPRE if ra < 100 and ra * idn <= 50 else NAO_CUMPRE,
                                 texto=f"RA={ra} ohm: <100 ohm e RA*IDn={ra * idn:.2f} V <= 50 V"))
        v.append(Verificacao(ref="RTIEBT 543.1/Q.54F", estado=POR_CONFIRMAR, texto="Condutor de protecao: SPE = SF para SF <= 16 mm2 (tabela da edicao 2000)"))
        mod = modulos(len(validos), len(ddr), qd["modulos"])
        quadro = Quadro(p_inst_w=round(p_inst, 1), p_calc_w=round(p_calc, 1), s_calc_kva=round(s_calc, 3),
                        potencia_a_contratar_kva=rec, geral_in_a=in_geral, poder_corte_ka=pdc, ddr=ddr,
                        n_mcb=len(validos), modulos=mod)

    # ---- ITED (tomadas de telecomunicacoes) ----
    ited = {}
    if ited_cfg:
        for r in p.rooms:
            ited[r.id] = dotacao_ited(r, ited_cfg)
        tot_rj, tot_tv = sum(x["rj45"] for x in ited.values()), sum(x["tv"] for x in ited.values())
        for uso_, est in sorted({(r.use, ited[r.id]["estado"]) for r in p.rooms}):
            if est != CUMPRE:
                v.append(Verificacao(ref="Manual ITED", estado=est, texto=f"tomadas ITED em '{uso_}': {est} (ver fonte no ficheiro de dotacao)"))
        v.append(Verificacao(ref="Manual ITED", estado=AVISO,
                             texto=f"Total {tot_rj} RJ45 e {tot_tv} TV. ATI, tubagem e cabos ITED NAO dimensionados"))

    return Resultado(
        projeto=p.name, revisao=p.revision, pontos=pontos, circuitos=circuitos,
        potencia_minima_kva=pmin, n_compartimentos=ncomp, verificacoes=v, quadro=quadro, ited=ited,
        pressupostos=[f"Metodo {cond['metodo']}, ambiente {cond['temperatura_ambiente_c']} C (k1={k1}), "
                      f"{cond['n_circuitos_agrupados']} circuitos agrupados (k2={k2})",
                      f"Comprimentos ESTIMADOS (fator {fator}, descidas {vert} m) salvo correcao manual",
                      "Tomadas: Ib de calculo = In (conservador); iluminacao: "
                      f"{cfg['iluminacao']['w_por_ponto']} W/ponto",
                      "Tabelas de correntes admissiveis e de secoes minimas: edicao 2000, POR CONFIRMAR",
                      "Saida e RASCUNHO nao assinado"])

def pendencias(r: Resultado) -> dict:
    """Contagem de linhas que impedem tratar a saida como utilizavel. Rascunho SEMPRE; 'bloqueado' = ha pontos por confirmar/violacoes."""
    n = {e: sum(1 for v in r.verificacoes if v.estado == e) for e in (NAO_CUMPRE, POR_CONFIRMAR, CONVENCAO, AVISO)}
    n["erros_circuito"] = sum(1 for c in r.circuitos if c.erro)
    n["bloqueado"] = bool(n[NAO_CUMPRE] or n[POR_CONFIRMAR] or n[AVISO] or n["erros_circuito"])
    return n

def relatorio_texto(r: Resultado) -> str:
    pd = pendencias(r)
    out = [f"PROJETO: {r.projeto} (rev {r.revisao}) - RASCUNHO" + (f" - NAO UTILIZAVEL: {pd[NAO_CUMPRE]} nao cumpre, {pd[POR_CONFIRMAR]} por confirmar, {pd[AVISO]} avisos, {pd['erros_circuito']} circuitos com erro" if pd["bloqueado"] else ""), "", "PONTOS POR DIVISAO (convencao)"]
    for rid, d in r.pontos.items():
        out.append(f"  {rid}: luz {d['luz']}, tomadas {d['tomadas']}, interruptores {d['interruptores']}")
    out += ["", "CIRCUITOS"]
    for c in r.circuitos:
        s = f"{c.s_mm2} mm2, Iz {c.iz_a} A, queda {c.queda_pct}%" if not c.erro else f"ERRO: {c.erro}"
        out.append(f"  {c.id:<10} {c.tipo:<15} {c.pontos} pts  Ib {c.ib_a} A  In {c.in_a} A  L {c.comprimento_m} m ({c.comprimento_origem})  {s}")
    if r.quadro:
        q = r.quadro
        out += ["", "QUADRO DE CARGAS (potencias em W)", "  circ       tipo             Pinst   Pcalc   In  curva  PE    DDR"]
        for c in r.circuitos:
            if not c.erro:
                out.append(f"  {c.id:<10} {c.tipo:<15} {c.p_inst_w:>7.0f} {c.p_calc_w:>7.0f}  {c.in_a:>3}  {c.curva:<4}  {c.pe_mm2}  {c.ddr}")
        out.append(f"  TOTAL: instalada {q.p_inst_w:.0f} W, calculo {q.p_calc_w:.0f} W ({q.s_calc_kva:.2f} kVA) -> contratar {q.potencia_a_contratar_kva} kVA")
        out += ["", "QUADRO", f"  Geral {q.geral_in_a} A (2P); poder de corte assumido {q.poder_corte_ka} kA; {q.n_mcb} disjuntores 1P+N"]
        for d in q.ddr:
            out.append(f"  {d['id']}: {d['in_a']} A {d['idn_ma']} mA tipo {d['tipo']}; circuitos {', '.join(d['circuitos'])} (corrente de calculo {d['corrente_calculo_a']} A)")
        m = q.modulos
        out.append(f"  Modulos: {m['base']} + reserva = {m['com_reserva']} -> {m['fileiras']} fileira(s), {m['total_modulos']} modulos")
    if r.ited:
        out += ["", "ITED (tomadas por divisao: RJ45 / TV)"]
        for rid, d in r.ited.items():
            out.append(f"  {rid}: {d['rj45']} RJ45, {d['tv']} TV [{d['estado']}]")
    out += ["", "VERIFICACOES"]
    out += [f"  [{x.estado}] {x.ref}: {x.texto}" for x in r.verificacoes]
    out += ["", "PRESSUPOSTOS"] + [f"  - {x}" for x in r.pressupostos]
    return "\n".join(out)
