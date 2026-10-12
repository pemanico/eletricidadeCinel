"""Desenho como PRIMITIVAS geometricas (linha, polilinha, circulo, texto) -> SVG (app) e DXF (exportacao).
Planta: coordenadas em METROS (as do Project). Unifilar: folha propria, 1 unidade = 1 mm de papel.
Posicoes dos pontos sao INDICATIVAS (geradas automaticamente a partir das divisoes): o tecnico ajusta no CAD."""
from __future__ import annotations
import math
from ..schema.project import Project
from ..schema.dynamic import resolve
from ..engine import Resultado
from .dxfread import _dentro

COR = {"iluminacao": "#d4a017", "tomadas": "#1f77b4", "termoacumulador": "#d62728", "climatizacao": "#2ca02c",
       "forno": "#ff7f0e", "placa": "#ff7f0e", "maq_lavar": "#17becf", "outro": "#9467bd"}
ACI = {"#d4a017": 2, "#1f77b4": 5, "#d62728": 1, "#2ca02c": 3, "#ff7f0e": 30, "#17becf": 4, "#9467bd": 6, "#888888": 8, "#000000": 7, "#555555": 9}

def L(a, b, layer, cor="#000000"): return {"t": "line", "a": tuple(a), "b": tuple(b), "layer": layer, "cor": cor}
def P(pts, layer, cor="#000000", fechada=True): return {"t": "poly", "pts": [tuple(p) for p in pts], "closed": fechada, "layer": layer, "cor": cor}
def C(c, r, layer, cor="#000000"): return {"t": "circle", "c": tuple(c), "r": r, "layer": layer, "cor": cor}
def T(pos, h, txt, layer, cor="#000000"): return {"t": "text", "pos": tuple(pos), "h": h, "txt": txt, "layer": layer, "cor": cor}

def _bbox(poly):
    xs, ys = [p[0] for p in poly], [p[1] for p in poly]
    return min(xs), min(ys), max(xs), max(ys)

def _centro(poly):
    x0, y0, x1, y1 = _bbox(poly); return ((x0 + x1) / 2, (y0 + y1) / 2)

def _percurso_perimetro(poly, n, margem=0.2):
    """n pontos igualmente espacados no perimetro do retangulo envolvente recolhido por 'margem'."""
    x0, y0, x1, y1 = _bbox(poly)
    x0 += margem; y0 += margem; x1 -= margem; y1 -= margem
    per = 2 * ((x1 - x0) + (y1 - y0))
    out = []
    for i in range(n):
        d = (i + 0.5) * per / n
        if d < x1 - x0: pt = (x0 + d, y0)
        elif d < (x1 - x0) + (y1 - y0): pt = (x1, y0 + d - (x1 - x0))
        elif d < 2 * (x1 - x0) + (y1 - y0): pt = (x1 - (d - (x1 - x0) - (y1 - y0)), y1)
        else: pt = (x0, y1 - (d - 2 * (x1 - x0) - (y1 - y0)))
        out.append(pt if _dentro(pt, poly) else _centro(poly))
    return out

def _pontos_luz(poly, n):
    x0, y0, x1, y1 = _bbox(poly); cx, cy = _centro(poly)
    if n == 1: return [(cx, cy)]
    horiz = (x1 - x0) >= (y1 - y0)
    return [((x0 + (i + 1) * (x1 - x0) / (n + 1), cy) if horiz else (cx, y0 + (i + 1) * (y1 - y0) / (n + 1))) for i in range(n)]

def posicoes_pontos(p: Project, res: Resultado) -> dict:
    """{room_id: {'luz': [...], 'tomadas': [...], 'interruptores': [...], 'rj45': [...], 'tv': [...]}} (indicativo)."""
    out = {}
    for r in p.rooms:
        if not r.polygon: continue
        pts = res.pontos[r.id]
        tom = _percurso_perimetro(r.polygon, pts["tomadas"], 0.2)
        ited = res.ited.get(r.id, {"rj45": 0, "tv": 0})
        ext = _percurso_perimetro(r.polygon, ited["rj45"] + ited["tv"], 0.45) if ited["rj45"] + ited["tv"] else []
        porta = next((o for o in p.openings if o.room_id == r.id and o.kind == "porta"), None)
        x0, y0, x1, y1 = _bbox(r.polygon)
        base = (porta.pos[0] + 0.3, porta.pos[1] + 0.15) if porta else (x0 + 0.2, y0 + 0.2)
        if not _dentro(base, r.polygon): base = (x0 + 0.2, y0 + 0.2)
        out[r.id] = {"luz": _pontos_luz(r.polygon, pts["luz"]), "tomadas": tom,
                     "interruptores": [(base[0] + 0.25 * i, base[1]) for i in range(pts["interruptores"])],
                     "rj45": ext[:ited["rj45"]], "tv": ext[ited["rj45"]:]}
    return out

def planta(p0: Project, res: Resultado, incluir_divisoes: bool = True) -> list[dict]:
    """Planta eletrica: pontos, percursos dos circuitos (cor por tipo), quadro, ITED, legenda."""
    p, _ = resolve(p0)
    prim, rooms = [], {r.id: r for r in p.rooms}
    pos = posicoes_pontos(p, res)
    if incluir_divisoes:
        for r in p.rooms:
            if r.polygon:
                prim.append(P(r.polygon, "BASE-DIVISOES", "#888888"))
                cx, cy = _centro(r.polygon)
                prim.append(T((cx - 0.8, cy + 0.15), 0.18, r.name, "BASE-TEXTO", "#555555"))
                prim.append(T((cx - 0.8, cy - 0.15), 0.13, f"{r.area_m2:.1f} m2", "BASE-TEXTO", "#555555"))
        for o in p.openings:
            prim.append(L((o.pos[0] - o.width_m / 2, o.pos[1]), (o.pos[0] + o.width_m / 2, o.pos[1]), "BASE-ABERTURAS",
                          "#2ca02c" if o.kind == "porta" else "#17becf"))
    qpos = tuple(p.panel.pos) if p.panel else None
    # percursos dos circuitos
    for c in res.circuitos:
        cor, lay = COR.get(c.tipo, COR["outro"]), f"ELE-{c.id}"
        pts, cur = [], qpos
        for rid in c.divisoes:
            if rid not in rooms or not rooms[rid].polygon: continue
            ctr = _centro(rooms[rid].polygon)
            if cur: prim.append(L(cur, (cur[0], ctr[1]), lay, cor)); prim.append(L((cur[0], ctr[1]), ctr, lay, cor))
            cur = ctr
            if c.tipo in ("iluminacao", "tomadas"):
                for q in pos[rid]["luz" if c.tipo == "iluminacao" else "tomadas"]:
                    prim.append(L(ctr, q, lay, cor))
            else:
                prim.append(P([(ctr[0] - .15, ctr[1] - .15), (ctr[0] + .15, ctr[1] - .15), (ctr[0] + .15, ctr[1] + .15), (ctr[0] - .15, ctr[1] + .15)], "ELE-SIMBOLOS", cor))
                prim.append(T((ctr[0] + .2, ctr[1] - .05), 0.12, c.tipo, "ELE-TEXTO", cor))
        if qpos and c.divisoes and rooms.get(c.divisoes[0]) and rooms[c.divisoes[0]].polygon:
            ctr0 = _centro(rooms[c.divisoes[0]].polygon)
            prim.append(T((qpos[0] + 0.1, (qpos[1] + ctr0[1]) / 2), 0.11, c.id, "ELE-TEXTO", cor))
    # simbolos
    for rid, d in pos.items():
        for q in d["luz"]:
            prim += [C(q, 0.12, "ELE-SIMBOLOS", COR["iluminacao"]), L((q[0] - .09, q[1] - .09), (q[0] + .09, q[1] + .09), "ELE-SIMBOLOS", COR["iluminacao"]), L((q[0] - .09, q[1] + .09), (q[0] + .09, q[1] - .09), "ELE-SIMBOLOS", COR["iluminacao"])]
        for q in d["tomadas"]:
            prim += [C(q, 0.09, "ELE-SIMBOLOS", COR["tomadas"]), L((q[0] - .09, q[1]), (q[0] + .09, q[1]), "ELE-SIMBOLOS", COR["tomadas"])]
        for q in d["interruptores"]:
            prim += [C(q, 0.06, "ELE-SIMBOLOS", "#000000"), L(q, (q[0] + .12, q[1] + .12), "ELE-SIMBOLOS", "#000000")]
        for q in d["rj45"]:
            prim += [P([(q[0] - .08, q[1] - .08), (q[0] + .08, q[1] - .08), (q[0] + .08, q[1] + .08), (q[0] - .08, q[1] + .08)], "ITED", "#9467bd"), T((q[0] - .06, q[1] - .04), 0.08, "D", "ITED", "#9467bd")]
        for q in d["tv"]:
            prim += [P([(q[0] - .08, q[1] - .08), (q[0] + .08, q[1] - .08), (q[0] + .08, q[1] + .08), (q[0] - .08, q[1] + .08)], "ITED", "#9467bd"), T((q[0] - .07, q[1] - .04), 0.07, "TV", "ITED", "#9467bd")]
    if qpos:
        x, y = qpos
        prim += [P([(x - .2, y - .1), (x + .2, y - .1), (x + .2, y + .1), (x - .2, y + .1)], "ELE-QUADRO", "#d62728"), T((x - .15, y - .05), 0.13, "QE", "ELE-QUADRO", "#d62728")]
    # legenda
    allpts = [pt for r in p.rooms for pt in r.polygon] or [(0, 0)]
    x0, y0 = min(a for a, _ in allpts), min(b for _, b in allpts) - 0.8
    prim.append(T((x0, y0), 0.16, "LEGENDA (posicoes indicativas; RASCUNHO nao assinado)", "ELE-TEXTO"))
    for i, c in enumerate(res.circuitos):
        prim.append(T((x0, y0 - 0.3 * (i + 1)), 0.13, f"{c.id}: {c.pontos} pt, {c.in_a} A {c.curva}, {c.s_mm2} mm2" + (" [ERRO]" if c.erro else ""),
                      "ELE-TEXTO", COR.get(c.tipo, COR["outro"])))
    return prim

def unifilar(res: Resultado) -> list[dict]:
    """Esquema unifilar (1 unidade = 1 mm de folha). Rede -> geral -> DDR -> disjuntores -> cabos/destinos."""
    q = res.quadro
    prim = []
    if not q: return [T((0, 0), 5, "Unifilar nao disponivel (quadro nao calculado)", "UNI-TEXTO")]
    W = 62.0
    por_ddr = {d["id"]: [c for c in res.circuitos if c.id in d["circuitos"]] for d in q.ddr}
    total = sum(len(v) for v in por_ddr.values())
    larg = max(total * W, 160)
    cx = larg / 2
    prim += [T((cx - 30, 0), 5, "REDE DE DISTRIBUICAO BT 230 V TT", "UNI-TEXTO"), L((cx, -3), (cx, -18), "UNI-LINHAS")]
    prim += [P([(cx - 25, -18), (cx + 25, -18), (cx + 25, -34), (cx - 25, -34)], "UNI-APARELHOS"),
             T((cx - 23, -24), 4, f"GERAL {q.geral_in_a} A 2P", "UNI-TEXTO"), T((cx - 23, -30), 3, f"PdC {q.poder_corte_ka:g} kA (assumido)", "UNI-TEXTO"),
             L((cx, -34), (cx, -44), "UNI-LINHAS")]
    xcol, centros = 0.0, []
    for d in q.ddr:
        cs = por_ddr[d["id"]]
        x_ini = xcol
        xcol += max(len(cs), 1) * W
        centros.append(((x_ini + xcol) / 2 - W / 2 + W / 2, x_ini, xcol, d, cs))
    prim.append(L((centros[0][0], -44), (centros[-1][0], -44), "UNI-LINHAS"))
    for xm, xa, xb, d, cs in centros:
        prim += [L((xm, -44), (xm, -52), "UNI-LINHAS"),
                 P([(xm - 28, -52), (xm + 28, -52), (xm + 28, -72), (xm - 28, -72)], "UNI-APARELHOS"),
                 T((xm - 26, -58), 3.6, f"{d['id']} {d['in_a']} A {d['idn_ma']} mA", "UNI-TEXTO"), T((xm - 26, -64), 3.2, f"tipo {d['tipo']} 2P", "UNI-TEXTO"),
                 L((xm, -72), (xm, -80), "UNI-LINHAS")]
        if cs:
            prim.append(L((xa + W / 2, -80), (xb - W / 2, -80), "UNI-LINHAS"))
        for i, c in enumerate(cs):
            x = xa + W / 2 + i * W
            cor = COR.get(c.tipo, COR["outro"])
            prim += [L((x, -80), (x, -88), "UNI-LINHAS", cor), P([(x - 8, -88), (x + 8, -88), (x + 8, -104), (x - 8, -104)], "UNI-APARELHOS", cor),
                     T((x - 7, -95), 3.4, f"{c.curva}{c.in_a}", "UNI-TEXTO", cor), T((x - 7, -100), 2.6, "1P+N", "UNI-TEXTO", cor),
                     L((x, -104), (x, -112), "UNI-LINHAS", cor)]
            lin = [c.id, f"{c.tipo[:14]}", f"{c.pontos} pt" if c.tipo in ("iluminacao", "tomadas") else f"{c.p_inst_w:.0f} W",
                   f"H07V-U 3G{c.s_mm2:g}" if c.s_mm2 else "SEM SECCAO", f"PE {c.pe_mm2:g} mm2" if c.pe_mm2 else "",
                   f"L {c.comprimento_m:.0f} m ({c.comprimento_origem[:3].lower()})", f"dU {c.queda_pct:.1f}%" if c.queda_pct is not None else ""]
            for k, t in enumerate(l for l in lin if l):
                prim.append(T((x - 14, -118 - 4.6 * k), 3.0, t, "UNI-TEXTO", cor))
    prim.append(T((0, -165), 3.2, f"Quadro: {q.modulos['total_modulos']} modulos ({q.modulos['fileiras']} fileira(s)). RASCUNHO nao assinado: simultaneidade, curvas e PdC sao convencao; tabelas da edicao 2000 por confirmar.", "UNI-TEXTO"))
    return prim

# ---------- renderizacao ----------
def _limites(prim):
    xs, ys = [], []
    for e in prim:
        if e["t"] == "line": xs += [e["a"][0], e["b"][0]]; ys += [e["a"][1], e["b"][1]]
        elif e["t"] == "poly":
            xs += [q[0] for q in e["pts"]]; ys += [q[1] for q in e["pts"]]
        elif e["t"] == "circle": xs += [e["c"][0] - e["r"], e["c"][0] + e["r"]]; ys += [e["c"][1] - e["r"], e["c"][1] + e["r"]]
        else: xs += [e["pos"][0], e["pos"][0] + len(e["txt"]) * e["h"] * 0.6]; ys += [e["pos"][1], e["pos"][1] + e["h"]]
    return (min(xs), min(ys), max(xs), max(ys)) if xs else (0, 0, 1, 1)

def _esc(t): return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def para_svg(prim: list[dict], fundo: list[dict] | None = None, margem: float = 0.5, esp: float = 0.03) -> str:
    """SVG com eixo Y para cima (como o CAD). 'fundo' = geometria do arquiteto (cinzento)."""
    tudo = (fundo or []) + prim
    x0, y0, x1, y1 = _limites(tudo)
    x0 -= margem; y0 -= margem; x1 += margem; y1 += margem
    w, h = x1 - x0, y1 - y0
    f = lambda y: y0 + y1 - y
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.3f} {y0:.3f} {w:.3f} {h:.3f}" preserveAspectRatio="xMidYMid meet" style="background:#fff">']
    for grupo, op in ((fundo or [], 0.55), (prim, 1.0)):
        out.append(f'<g opacity="{op}">')
        for e in grupo:
            cor, lay = e["cor"], e["layer"]
            if e["t"] == "line":
                out.append(f'<line data-layer="{lay}" x1="{e["a"][0]:.3f}" y1="{f(e["a"][1]):.3f}" x2="{e["b"][0]:.3f}" y2="{f(e["b"][1]):.3f}" stroke="{cor}" stroke-width="{esp}"/>')
            elif e["t"] == "poly":
                pts = " ".join(f"{a:.3f},{f(b):.3f}" for a, b in e["pts"])
                tag = "polygon" if e["closed"] else "polyline"
                out.append(f'<{tag} data-layer="{lay}" points="{pts}" fill="none" stroke="{cor}" stroke-width="{esp}"/>')
            elif e["t"] == "circle":
                out.append(f'<circle data-layer="{lay}" cx="{e["c"][0]:.3f}" cy="{f(e["c"][1]):.3f}" r="{e["r"]:.3f}" fill="none" stroke="{cor}" stroke-width="{esp}"/>')
            else:
                out.append(f'<text data-layer="{lay}" x="{e["pos"][0]:.3f}" y="{f(e["pos"][1]):.3f}" font-size="{e["h"]:.3f}" fill="{cor}" font-family="sans-serif">{_esc(e["txt"])}</text>')
        out.append("</g>")
    out.append("</svg>")
    return "".join(out)

def para_dxf(prim: list[dict], unit_m: float = 1.0):
    """Primitivas -> Dxf (camadas com cor). Coordenadas divididas por unit_m (metros por unidade do desenho)."""
    from .dxf import Dxf
    layers = {}
    for e in prim: layers.setdefault(e["layer"], ACI.get(e["cor"], 7))
    d = Dxf(layers)
    s = 1.0 / unit_m
    for e in prim:
        if e["t"] == "line": d.line(e["layer"], (e["a"][0] * s, e["a"][1] * s), (e["b"][0] * s, e["b"][1] * s))
        elif e["t"] == "poly": d.polyline(e["layer"], [(a * s, b * s) for a, b in e["pts"]], e["closed"])
        elif e["t"] == "circle": d.circle(e["layer"], (e["c"][0] * s, e["c"][1] * s), e["r"] * s)
        else: d.text(e["layer"], (e["pos"][0] * s, e["pos"][1] * s), e["h"] * s, e["txt"])
    return d

def base_do_arquiteto(dxf_lido: dict, unit_m: float, camadas_excluir=()) -> list[dict]:
    """Geometria do DXF do arquiteto como fundo (cinzento) em metros: linhas e polilinhas (sem textos/blocos)."""
    out = []
    for e in dxf_lido["entidades"]:
        if e.layer in camadas_excluir: continue
        if e.tipo == "LINE": out.append(L([c * unit_m for c in e.pts[0]], [c * unit_m for c in e.pts[1]], "ARQ-" + e.layer, "#888888"))
        elif e.tipo == "POLY" and len(e.pts) >= 2: out.append(P([(x * unit_m, y * unit_m) for x, y in e.pts], "ARQ-" + e.layer, "#888888", e.fechada))
    return out
