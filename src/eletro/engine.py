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
from .rules.circuitos import agrupar_sequencial, agrupar_proximidade, ordenar_cadeia
from .calc.percursos import percurso
from .rules.potencia import compartimentos, potencia_minima_kva
from .rules.quadro import potencia_a_contratar, calibre_geral_a, calibre_ddr, pe_mm2, modulos
from .rules.ited import dotacao_ited
from .rules import alturas

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
    pontos_ids: list[str] = []          # aparelhagem colocada ligada a este circuito (pela ordem do cabo)
    origem_pontos: str = "CONVENCAO"    # PLANTA (pontos colocados) | CONVENCAO (contagem por area)
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
    pontos_circuito: dict[str, dict] = {}   # ponto -> {circuito, cabo_ate_m}

def s_min_de(c, cfg) -> float:
    return cfg["s_min_mm2"].get("iluminacao" if c.tipo == "iluminacao" else "tomadas" if c.tipo == "tomadas"
                                 else "avac" if c.tipo == "climatizacao" else c.tipo, 2.5)

def contar_pontos(pts, catalogo: dict) -> dict:
    """Contagens a partir da aparelhagem colocada na planta."""
    n = {"luz": 0, "tomadas": 0, "interruptores": 0, "rj45": 0, "tv": 0, "dedicado": 0}
    for q in pts:
        c = alturas.categoria(q.kind, catalogo)
        if c == "luz": n["luz"] += 1
        elif c == "tomada": n["tomadas"] += 1
        elif c == "interruptor": n["interruptores"] += 1
        elif c == "dedicado": n["dedicado"] += 1
        elif c == "ited": n["tv" if q.kind == "tv" else "rj45"] += 1
    return n

def calcular(p0: Project, perfil: dict, ited_cfg: Optional[dict] = None, simbolos: Optional[dict] = None) -> Resultado:
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

    pontos = {r.id: {**pontos_divisao(r, perfil), "origem": "CONVENCAO"} for r in p.rooms}
    v.append(Verificacao(ref=perfil["id"], estado=CONVENCAO,
                         texto="Numero de pontos por divisao e convencao de projeto (RTIEBT nao o fixa)"))
    # Aparelhagem colocada na planta: substitui a convencao NAS DIVISOES que tem pontos
    cat = simbolos or (alturas.carregar(str(alturas.CATALOGO_DEFAULT)) if p.points else None)
    contagens: dict[str, dict] = {}
    if p.points:
        por_div: dict[str, list] = {}
        for q in p.points:
            por_div.setdefault(q.room_id, []).append(q)
        nomes = {r.id: r.name for r in p.rooms}
        for rid, qs in por_div.items():
            n = contar_pontos(qs, cat); contagens[rid] = n
            conv = pontos[rid]
            if n["luz"] + n["tomadas"] + n["interruptores"]:
                pontos[rid] = {"luz": n["luz"], "tomadas": n["tomadas"], "interruptores": n["interruptores"], "origem": "PLANTA"}
                falta = [f"{k} {n[k]} < {conv[k]}" for k in ("luz", "tomadas") if n[k] < conv[k]]
                if falta:
                    v.append(Verificacao(ref=perfil["id"], estado=CONVENCAO,
                                         texto=f"{nomes[rid]}: abaixo da convencao ({', '.join(falta)}); decisao do projetista"))
            if n["dedicado"] and not any(e.room_id == rid for e in p.equipment):
                v.append(Verificacao(ref="projeto", estado=AVISO,
                                     texto=f"{nomes[rid]}: {n['dedicado']} ponto(s) dedicado(s) na planta sem equipamento definido (sem circuito nem potencia)"))
        rooms_id = {r.id: r for r in p.rooms}
        for ref, est, txt in alturas.verificar(p.points, rooms_id, cat):
            v.append(Verificacao(ref=ref, estado=est, texto=txt))
        velhos = alturas.desatualizados(p.points, rooms_id, cat)
        if velhos:
            v.append(Verificacao(ref=f"{cat['id']} v{cat['versao']}", estado=AVISO,
                                 texto=f"{len(velhos)} ponto(s) com altura da tabela antiga ({', '.join(q.id for q in velhos[:8])}"
                                       f"{'...' if len(velhos) > 8 else ''}): reaplicar a tabela no editor"))
        v.append(Verificacao(ref=f"{cat['id']} v{cat['versao']}", estado=CONVENCAO,
                             texto="Alturas de montagem: tabela editavel com fonte por valor (o RTIEBT nao fixa alturas gerais em habitacao)"))
    circuitos: list[Circuito] = []

    sim, qd = perfil["simultaneidade"], perfil["quadro"]

    comp = perfil["comprimentos"]
    altura_quadro, entre_pisos = comp.get("altura_quadro_m", 1.5), comp.get("entre_pisos_m", 3.0)
    rooms_id = {r.id: r for r in p.rooms}
    pontos_circuito: dict[str, dict] = {}
    if p.points and not p.panel:
        raise ValueError("Projeto sem quadro (panel): impossivel estimar comprimentos")
    quadro_info = None
    if p.panel:
        rq = rooms_id[p.panel.room_id]
        quadro_info = {"pos": tuple(p.panel.pos), "piso": rq.floor, "pe_direito": rq.height_m, "altura": altura_quadro}

    def info(q):
        r = rooms_id[q.room_id]
        return {"id": q.id, "pos": tuple(q.pos), "piso": r.floor, "pe_direito": r.height_m, "altura": q.height_m,
                "room_id": q.room_id, "kind": q.kind, "circuit": q.circuit}

    def juntar(cid, tipo, grupo, ib, inn, s_min, q_lim, p_inst, fsim, cadeia=None):
        """grupo = [(room_id, n)] (convencao) ou cadeia = [info(ponto)] (aparelhagem colocada, pela ordem do cabo)."""
        if cadeia:
            rids = list(dict.fromkeys(q["room_id"] for q in cadeia)); npts = len(cadeia)
        else:
            rids = [g[0] for g in grupo]; npts = sum(g[1] for g in grupo)
        manual = p.circuit_length_m.get(cid)
        if cadeia:
            pc = percurso(quadro_info, cadeia, fator, entre_pisos, "teto" if tipo == "iluminacao" else "parede")
            L = manual if manual is not None else pc["total_m"]
            for q in cadeia:
                pontos_circuito[q["id"]] = {"circuito": cid, "cabo_ate_m": pc["por_ponto"][q["id"]]}
            if pc["entre_pisos"] and manual is None:
                v.append(Verificacao(ref="projeto", estado=AVISO, texto=f"{cid}: liga pontos noutro piso; comprimento entre pisos "
                                     f"convencionado ({entre_pisos} m) e horizontal nao fiavel: medir e corrigir"))
        else:
            L = manual if manual is not None else comprimento_circuito(p, rids, fator, vert)
        c = dict(id=cid, tipo=tipo, divisoes=rids, pontos=npts, ib_a=round(ib, 3), in_a=inn,
                 comprimento_m=round(L, 2), comprimento_origem="MANUAL" if manual is not None else "ESTIMADO",
                 queda_max_pct=q_lim, p_inst_w=round(p_inst, 1), p_calc_w=round(p_inst * fsim, 1),
                 curva=qd["curvas"].get(tipo, qd["curvas"]["outros"]),
                 pontos_ids=[q["id"] for q in cadeia] if cadeia else [], origem_pontos="PLANTA" if cadeia else "CONVENCAO")
        try:
            s = size_for(ib, inn, L, k1=k1, k2=k2, max_drop_pct=q_lim, metodo=cond["metodo"], min_s_mm2=s_min)
            c.update(s_mm2=s["s_mm2"], iz_a=round(s["iz"], 2), queda_pct=round(s["drop_pct"], 3), pe_mm2=pe_mm2(s["s_mm2"]))
        except ValueError as e:
            c["erro"] = str(e)
        circuitos.append(Circuito(**c))

    # Iluminacao e tomadas, max. 8 pontos por circuito (801.5.3).
    #  - divisoes com aparelhagem colocada: circuitos a partir dos pontos (escolhidos a mao ou por proximidade ao quadro)
    #  - restantes divisoes: contagem da convencao, agrupamento sequencial por divisao
    mx = cfg["max_pontos_por_circuito"]
    plan = {rid for rid, d in pontos.items() if d["origem"] == "PLANTA"}
    usados_ids = {q.circuit for q in p.points if q.circuit}

    def numerar(prefixo):
        i = 0
        while True:
            i += 1
            if f"{prefixo}-{i}" not in usados_ids:
                usados_ids.add(f"{prefixo}-{i}"); yield f"{prefixo}-{i}"

    def cadeias(categoria):
        pts = [info(q) for q in p.points if q.room_id in plan and alturas.categoria(q.kind, cat) == categoria]
        manuais: dict[str, list] = {}
        for q in pts:
            if q["circuit"]: manuais.setdefault(q["circuit"], []).append(q)
        auto = [q for q in pts if not q["circuit"]]
        out = [(lab, ordenar_cadeia(g, quadro_info["pos"], quadro_info["piso"])) for lab, g in sorted(manuais.items())]
        out += [(None, g) for g in agrupar_proximidade(auto, quadro_info["pos"], quadro_info["piso"], mx)] if auto else []
        return out

    if plan:
        cats_lab = {}
        for q in p.points:
            if q.circuit and q.room_id in plan:
                cats_lab.setdefault(q.circuit, set()).add(alturas.categoria(q.kind, cat))
        for lab, cs in cats_lab.items():
            if {"luz", "tomada"} <= cs:
                v.append(Verificacao(ref="projeto", estado=AVISO, texto=f"circuito {lab}: mistura iluminacao e tomadas (separar)"))
            if cs - {"luz", "tomada"}:
                v.append(Verificacao(ref="projeto", estado=AVISO, texto=f"circuito {lab}: so iluminacao e tomadas sao agrupadas em circuitos; "
                                     f"interruptores, ITED e pontos dedicados ignoram a escolha"))
    nl, nt = numerar("ILUM"), numerar("TOM")
    w_luz = cfg["iluminacao"]["w_por_ponto"]
    if plan:
        for lab, g in cadeias("luz"):
            pw = len(g) * w_luz
            juntar(lab or next(nl), "iluminacao", None, pw / 230.0, cfg["iluminacao"]["in_a"], cfg["s_min_mm2"]["iluminacao"],
                   q_max["iluminacao"], pw, sim["iluminacao"], cadeia=g)
    for g in agrupar_sequencial([(r.id, pontos[r.id]["luz"]) for r in p.rooms if r.id not in plan], mx):
        n = sum(x[1] for x in g)
        if not n: continue
        pw = n * w_luz
        juntar(next(nl), "iluminacao", g, pw / 230.0, cfg["iluminacao"]["in_a"],
               cfg["s_min_mm2"]["iluminacao"], q_max["iluminacao"], pw, sim["iluminacao"])
    inn_t = cfg["tomadas"]["in_a"]
    if plan:
        for lab, g in cadeias("tomada"):
            juntar(lab or next(nt), "tomadas", None, float(inn_t), inn_t, cfg["s_min_mm2"]["tomadas"], q_max["outros"],
                   sim["tomada_circuito_w"], sim["tomadas"], cadeia=g)
    for g in agrupar_sequencial([(r.id, pontos[r.id]["tomadas"]) for r in p.rooms if r.id not in plan], mx):
        if not sum(x[1] for x in g): continue
        juntar(next(nt), "tomadas", g, float(inn_t), inn_t, cfg["s_min_mm2"]["tomadas"], q_max["outros"],
               sim["tomada_circuito_w"], sim["tomadas"])

    # Equipamentos dedicados; climatizacao (avac) agrupada ate 5 aparelhos por circuito (801.5.3).
    # Se houver ponto dedicado colocado na divisao do equipamento, o cabo vai ate esse ponto.
    livres_ded = [info(q) for q in p.points if alturas.categoria(q.kind, cat) == "dedicado"] if p.points else []
    mapa = (cat or {}).get("preenchimento", {}).get("equipamento", {})
    def ponto_de(e):
        cand = [q for q in livres_ded if q["room_id"] == e.room_id and q["kind"] == mapa.get(e.kind)] or \
               [q for q in livres_ded if q["room_id"] == e.room_id]
        if not cand: return None
        livres_ded.remove(cand[0]); return cand[0]
    avac = [e for e in p.equipment if e.kind == "avac"]
    mxa = cfg["max_aparelhos_climatizacao_por_circuito"]
    for k in range(0, len(avac), mxa):
        bloco = avac[k:k + mxa]
        ib = ib_mono(sum(e.power_w for e in bloco)); inn = next_in(ib)
        cad = [x for x in (ponto_de(e) for e in bloco) if x]
        cad = ordenar_cadeia(cad, quadro_info["pos"], quadro_info["piso"]) if cad and len(cad) == len(bloco) else None
        juntar(f"AVAC-{k // mxa + 1}", "climatizacao", [(e.room_id, 1) for e in bloco], ib, inn, cfg["s_min_mm2"]["avac"],
               q_max["outros"], sum(e.power_w for e in bloco), sim["climatizacao"], cadeia=cad)
    for e in p.equipment:
        if e.kind == "avac":
            continue
        ib = ib_mono(e.power_w); inn = next_in(ib)
        q = ponto_de(e)
        juntar(f"EQ-{e.id}", e.kind, [(e.room_id, 1)], ib, inn, cfg["s_min_mm2"].get(e.kind, 2.5), q_max["outros"],
               e.power_w, sim["equipamento"], cadeia=[q] if q else None)

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
            n = contagens.get(r.id)
            if n and (n["rj45"] or n["tv"]):
                minimo = (ited[r.id]["rj45"], ited[r.id]["tv"])
                ited[r.id] = {**ited[r.id], "rj45": n["rj45"], "tv": n["tv"], "origem": "PLANTA"}
                if n["rj45"] < minimo[0] or n["tv"] < minimo[1]:
                    v.append(Verificacao(ref="Manual ITED", estado=AVISO,
                                         texto=f"{r.name}: {n['rj45']} RJ45 / {n['tv']} TV na planta, abaixo da dotacao ({minimo[0]} / {minimo[1]})"))
        tot_rj, tot_tv = sum(x["rj45"] for x in ited.values()), sum(x["tv"] for x in ited.values())
        for uso_, est in sorted({(r.use, ited[r.id]["estado"]) for r in p.rooms}):
            if est != CUMPRE:
                v.append(Verificacao(ref="Manual ITED", estado=est, texto=f"tomadas ITED em '{uso_}': {est} (ver fonte no ficheiro de dotacao)"))
        v.append(Verificacao(ref="Manual ITED", estado=AVISO,
                             texto=f"Total {tot_rj} RJ45 e {tot_tv} TV. ATI, tubagem e cabos ITED NAO dimensionados"))

    return Resultado(
        projeto=p.name, revisao=p.revision, pontos=pontos, circuitos=circuitos,
        potencia_minima_kva=pmin, n_compartimentos=ncomp, verificacoes=v, quadro=quadro, ited=ited,
        pontos_circuito=pontos_circuito,
        pressupostos=[f"Metodo {cond['metodo']}, ambiente {cond['temperatura_ambiente_c']} C (k1={k1}), "
                      f"{cond['n_circuitos_agrupados']} circuitos agrupados (k2={k2})",
                      f"Comprimentos ESTIMADOS (fator {fator}, descidas {vert} m) salvo correcao manual",
                      f"Aparelhagem colocada: iluminacao pelo teto (sobe do quadro a {altura_quadro} m, desce a cada ponto); tomadas e "
                      f"dedicados pelas paredes a altura dos pontos; horizontais em L x {fator}; entre pisos {entre_pisos} m (convencao)",
                      "Queda de tensao com a corrente total do circuito em todo o comprimento (conservador)",
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
