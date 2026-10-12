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

class Resultado(BaseModel):
    projeto: str
    revisao: int
    pontos: dict[str, dict]
    circuitos: list[Circuito]
    potencia_minima_kva: float
    n_compartimentos: int
    verificacoes: list[Verificacao]
    pressupostos: list[str]

def s_min_de(c, cfg) -> float:
    return cfg["s_min_mm2"].get("iluminacao" if c.tipo == "iluminacao" else "tomadas" if c.tipo == "tomadas"
                                 else "avac" if c.tipo == "climatizacao" else c.tipo, 2.5)

def calcular(p0: Project, perfil: dict) -> Resultado:
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

    def juntar(cid, tipo, grupo, ib, inn, s_min, q_lim):
        rids = [g[0] for g in grupo]
        npts = sum(g[1] for g in grupo)
        manual = p.circuit_length_m.get(cid)
        L = manual if manual is not None else comprimento_circuito(p, rids, fator, vert)
        c = dict(id=cid, tipo=tipo, divisoes=rids, pontos=npts, ib_a=round(ib, 3), in_a=inn,
                 comprimento_m=round(L, 2), comprimento_origem="MANUAL" if manual is not None else "ESTIMADO",
                 queda_max_pct=q_lim)
        try:
            s = size_for(ib, inn, L, k1=k1, k2=k2, max_drop_pct=q_lim, metodo=cond["metodo"], min_s_mm2=s_min)
            c.update(s_mm2=s["s_mm2"], iz_a=round(s["iz"], 2), queda_pct=round(s["drop_pct"], 3))
        except ValueError as e:
            c["erro"] = str(e)
        circuitos.append(Circuito(**c))

    # Iluminacao e tomadas: agrupamento sequencial, max. 8 pontos (801.5.3)
    mx = cfg["max_pontos_por_circuito"]
    luz = agrupar_sequencial([(r.id, pontos[r.id]["luz"]) for r in p.rooms], mx)
    for i, g in enumerate(luz, 1):
        n = sum(x[1] for x in g)
        juntar(f"ILUM-{i}", "iluminacao", g, n * cfg["iluminacao"]["w_por_ponto"] / 230.0,
               cfg["iluminacao"]["in_a"], cfg["s_min_mm2"]["iluminacao"], q_max["iluminacao"])
    tom = agrupar_sequencial([(r.id, pontos[r.id]["tomadas"]) for r in p.rooms], mx)
    for i, g in enumerate(tom, 1):
        inn = cfg["tomadas"]["in_a"]
        juntar(f"TOM-{i}", "tomadas", g, float(inn), inn, cfg["s_min_mm2"]["tomadas"], q_max["outros"])

    # Equipamentos dedicados; climatizacao (avac) agrupada ate 5 aparelhos por circuito (801.5.3)
    avac = [e for e in p.equipment if e.kind == "avac"]
    for k in range(0, len(avac), cfg["max_aparelhos_climatizacao_por_circuito"]):
        bloco = avac[k:k + cfg["max_aparelhos_climatizacao_por_circuito"]]
        ib = ib_mono(sum(e.power_w for e in bloco)); inn = next_in(ib)
        juntar(f"AVAC-{k // cfg['max_aparelhos_climatizacao_por_circuito'] + 1}", "climatizacao",
               [(e.room_id, 1) for e in bloco], ib, inn, cfg["s_min_mm2"]["avac"], q_max["outros"])
    for e in p.equipment:
        if e.kind == "avac":
            continue
        ib = ib_mono(e.power_w); inn = next_in(ib)
        juntar(f"EQ-{e.id}", e.kind, [(e.room_id, 1)], ib, inn, cfg["s_min_mm2"].get(e.kind, 2.5), q_max["outros"])

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
    return Resultado(
        projeto=p.name, revisao=p.revision, pontos=pontos, circuitos=circuitos,
        potencia_minima_kva=pmin, n_compartimentos=ncomp, verificacoes=v,
        pressupostos=[f"Metodo {cond['metodo']}, ambiente {cond['temperatura_ambiente_c']} C (k1={k1}), "
                      f"{cond['n_circuitos_agrupados']} circuitos agrupados (k2={k2})",
                      f"Comprimentos ESTIMADOS (fator {fator}, descidas {vert} m) salvo correcao manual",
                      "Tomadas: Ib de calculo = In (conservador); iluminacao: "
                      f"{cfg['iluminacao']['w_por_ponto']} W/ponto",
                      "Tabelas de correntes admissiveis e de secoes minimas: edicao 2000, POR CONFIRMAR",
                      "Saida e RASCUNHO nao assinado"])

def relatorio_texto(r: Resultado) -> str:
    out = [f"PROJETO: {r.projeto} (rev {r.revisao}) - RASCUNHO", "", "PONTOS POR DIVISAO (convencao)"]
    for rid, d in r.pontos.items():
        out.append(f"  {rid}: luz {d['luz']}, tomadas {d['tomadas']}, interruptores {d['interruptores']}")
    out += ["", "CIRCUITOS"]
    for c in r.circuitos:
        s = f"{c.s_mm2} mm2, Iz {c.iz_a} A, queda {c.queda_pct}%" if not c.erro else f"ERRO: {c.erro}"
        out.append(f"  {c.id:<10} {c.tipo:<15} {c.pontos} pts  Ib {c.ib_a} A  In {c.in_a} A  L {c.comprimento_m} m ({c.comprimento_origem})  {s}")
    out += ["", "VERIFICACOES"]
    out += [f"  [{x.estado}] {x.ref}: {x.texto}" for x in r.verificacoes]
    out += ["", "PRESSUPOSTOS"] + [f"  - {x}" for x in r.pressupostos]
    return "\n".join(out)
