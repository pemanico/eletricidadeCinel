"""Lista de material (quantidades derivadas do Resultado; nada aqui e preco nem orcamento).
Comprimentos de cabo: ESTIMADOS (ver circuito.comprimento_origem) + margem configuravel.
Fora de ambito (nao dimensionado): tubagem, caixas, ATI/ITED, bornes, ligacoes equipotenciais."""
from __future__ import annotations
from collections import defaultdict
from ..engine import Resultado

def lista_material(r: Resultado, margem_cabo: float = 0.10) -> list[dict]:
    it: list[dict] = []
    def add(cat, desc, qtd, un, nota=""):
        it.append({"categoria": cat, "descricao": desc, "qtd": qtd, "un": un, "nota": nota})
    ok = [c for c in r.circuitos if not c.erro]
    cab = defaultdict(float)
    for c in ok:
        cab[c.s_mm2] += c.comprimento_m
    for s in sorted(cab):
        # 3 condutores (fase, neutro, PE) por circuito monofasico
        add("Cabos", f"Cabo H07V-U 3G{s:g} mm2 (fase+neutro+PE)", round(cab[s] * (1 + margem_cabo), 1), "m",
            f"{cab[s]:.1f} m estimados + {margem_cabo:.0%} de margem")
    if r.quadro:
        q = r.quadro
        add("Quadro", f"Interruptor geral {q.geral_in_a} A 2P (PdC {q.poder_corte_ka:g} kA assumido)", 1, "un")
        for d in q.ddr:
            add("Quadro", f"Diferencial {d['in_a']} A {d['idn_ma']} mA tipo {d['tipo']} 2P", 1, "un", d["id"])
        mc = defaultdict(int)
        for c in ok:
            mc[(c.curva, c.in_a)] += 1
        for (cv, ina), n in sorted(mc.items(), key=lambda k: (k[0][1], k[0][0])):
            add("Quadro", f"Disjuntor {cv}{ina} 1P+N", n, "un")
        add("Quadro", f"Quadro/caixa {q.modulos['total_modulos']} modulos ({q.modulos['fileiras']} fileira(s))", 1, "un",
            "inclui 20% de reserva (convencao)")
    luz = sum(d["luz"] for d in r.pontos.values()); tom = sum(d["tomadas"] for d in r.pontos.values())
    inter = sum(d["interruptores"] for d in r.pontos.values())
    if luz: add("Aparelhagem", "Ponto de luz (caixa + casquilho/armadura)", luz, "un")
    if inter: add("Aparelhagem", "Interruptor", inter, "un")
    if tom: add("Aparelhagem", "Tomada 2P+T 16 A", tom, "un")
    rj = sum(d["rj45"] for d in r.ited.values()); tv = sum(d["tv"] for d in r.ited.values())
    if rj: add("ITED", "Tomada RJ45", rj, "un", "cabos/ATI/tubagem ITED nao dimensionados")
    if tv: add("ITED", "Tomada TV", tv, "un", "idem")
    for c in ok:
        if c.tipo not in ("iluminacao", "tomadas"):
            add("Equipamento", f"Ligacao dedicada {c.id} ({c.p_inst_w:.0f} W)", 1, "un", c.tipo)
    return it
