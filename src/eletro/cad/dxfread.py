"""Leitor minimo de DXF ASCII (sem dependencias) para ler a planta do arquiteto.
Suporta: LINE, LWPOLYLINE, POLYLINE/VERTEX, TEXT, MTEXT, INSERT (so da seccao ENTITIES). Ignora arcos/bulges (aproxima
por segmentos retos e avisa). NAO suporta DWG nem DXF binario: converter para DXF ASCII."""
from __future__ import annotations
import math, re, unicodedata
from dataclasses import dataclass, field

INSUNITS = {1: 0.0254, 2: 0.3048, 4: 0.001, 5: 0.01, 6: 1.0}   # polegada, pe, mm, cm, m

class DxfError(ValueError):
    pass

@dataclass
class Ent:
    tipo: str
    layer: str
    pts: list = field(default_factory=list)      # [(x, y)]
    fechada: bool = False
    texto: str = ""
    nome: str = ""                                # bloco (INSERT)
    escala: tuple = (1.0, 1.0)
    rot: float = 0.0
    bulge: bool = False

def _pares(text: str):
    if text.startswith("AutoCAD Binary DXF"):
        raise DxfError("DXF binario nao suportado: gravar como DXF ASCII")
    linhas = text.splitlines()
    out = []
    for i in range(0, len(linhas) - 1, 2):
        try:
            out.append((int(linhas[i].strip()), linhas[i + 1].strip()))
        except ValueError:
            raise DxfError(f"Ficheiro nao e DXF ASCII valido (linha {i + 1})")
    return out

def _limpar_mtext(t: str) -> str:
    t = re.sub(r"\\[Pp]", " ", t)
    t = re.sub(r"\\[A-Za-z][^;]*;", "", t)
    return t.replace("{", "").replace("}", "").replace("\\~", " ").strip()

def ler(text: str) -> dict:
    """Devolve {'unidades_codigo', 'entidades': [Ent], 'avisos': [..]}."""
    pares = _pares(text)
    seccoes, i = {}, 0
    while i < len(pares):
        if pares[i] == (0, "SECTION") and i + 1 < len(pares) and pares[i + 1][0] == 2:
            nome, j = pares[i + 1][1], i + 2
            while j < len(pares) and pares[j] != (0, "ENDSEC"):
                j += 1
            seccoes[nome] = pares[i + 2:j]
            i = j
        i += 1
    if "ENTITIES" not in seccoes:
        raise DxfError("Seccao ENTITIES nao encontrada")
    unid = 0
    h = seccoes.get("HEADER", [])
    for k, (c, v) in enumerate(h):
        if (c, v) == (9, "$INSUNITS") and k + 1 < len(h) and h[k + 1][0] == 70:
            unid = int(h[k + 1][1])
    # dividir em entidades
    brutas, atual = [], None
    for c, v in seccoes["ENTITIES"]:
        if c == 0:
            atual = [v, []]; brutas.append(atual)
        elif atual is not None:
            atual[1].append((c, v))
    ents, avisos, k = [], [], 0
    while k < len(brutas):
        tipo, dados = brutas[k]
        layer = next((v for c, v in dados if c == 8), "0")
        g = lambda code, d=None: next((v for c, v in dados if c == code), d)
        if tipo == "LINE":
            ents.append(Ent("LINE", layer, [(float(g(10, 0)), float(g(20, 0))), (float(g(11, 0)), float(g(21, 0)))]))
        elif tipo == "LWPOLYLINE":
            xs = [float(v) for c, v in dados if c == 10]; ys = [float(v) for c, v in dados if c == 20]
            bulge = any(c == 42 and abs(float(v)) > 1e-9 for c, v in dados)
            ents.append(Ent("POLY", layer, list(zip(xs, ys)), fechada=bool(int(g(70, 0)) & 1), bulge=bulge))
        elif tipo == "POLYLINE":
            fechada, pts, bulge = bool(int(g(70, 0)) & 1), [], False
            k += 1
            while k < len(brutas) and brutas[k][0] == "VERTEX":
                d = brutas[k][1]
                x = next((float(v) for c, v in d if c == 10), None); y = next((float(v) for c, v in d if c == 20), None)
                if x is not None and y is not None:
                    pts.append((x, y))
                bulge |= any(c == 42 and abs(float(v)) > 1e-9 for c, v in d)
                k += 1
            ents.append(Ent("POLY", layer, pts, fechada=fechada, bulge=bulge))
            # brutas[k] e SEQEND (ou fim): o ciclo seguinte avanca
        elif tipo == "TEXT":
            ents.append(Ent("TEXT", layer, [(float(g(10, 0)), float(g(20, 0)))], texto=g(1, "")))
        elif tipo == "MTEXT":
            t = "".join(v for c, v in dados if c == 3) + (g(1, "") or "")
            ents.append(Ent("TEXT", layer, [(float(g(10, 0)), float(g(20, 0)))], texto=_limpar_mtext(t)))
        elif tipo == "INSERT":
            ents.append(Ent("INSERT", layer, [(float(g(10, 0)), float(g(20, 0)))], nome=g(2, ""),
                            escala=(float(g(41, 1)), float(g(42, 1))), rot=float(g(50, 0))))
        k += 1
    if any(e.bulge for e in ents):
        avisos.append("Polilinhas com arcos (bulge) aproximadas por segmentos retos: areas podem diferir ligeiramente")
    return {"unidades_codigo": unid, "entidades": ents, "avisos": avisos, "texto": text}

def analisar(d: dict) -> dict:
    camadas = {}
    for e in d["entidades"]:
        c = camadas.setdefault(e.layer, {"poli_fechadas": 0, "poli_abertas": 0, "linhas": 0, "textos": 0, "blocos": 0})
        if e.tipo == "POLY": c["poli_fechadas" if e.fechada else "poli_abertas"] += 1
        elif e.tipo == "LINE": c["linhas"] += 1
        elif e.tipo == "TEXT": c["textos"] += 1
        elif e.tipo == "INSERT": c["blocos"] += 1
    u = INSUNITS.get(d["unidades_codigo"])
    return {"camadas": camadas, "unidade_m": u, "unidades_codigo": d["unidades_codigo"], "avisos": d["avisos"],
            "sugestao_camada_divisoes": max(camadas, key=lambda c: camadas[c]["poli_fechadas"]) if any(
                v["poli_fechadas"] for v in camadas.values()) else None}

def _area(poly):
    n = len(poly)
    return abs(sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))) / 2

def _dentro(pt, poly):
    x, y, c, n = pt[0], pt[1], False, len(poly)
    for i in range(n):
        x1, y1, x2, y2 = *poly[i], *poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c

def _dist_aresta(pt, poly):
    best = 1e18
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
        dx, dy = x2 - x1, y2 - y1
        t = 0 if dx == dy == 0 else max(0, min(1, ((pt[0] - x1) * dx + (pt[1] - y1) * dy) / (dx * dx + dy * dy)))
        best = min(best, math.hypot(pt[0] - (x1 + t * dx), pt[1] - (y1 + t * dy)))
    return best

def _norm(t: str) -> str:
    return unicodedata.normalize("NFKD", t.lower()).encode("ascii", "ignore").decode()

USOS = [("sala", r"sala|living|estar|jantar"), ("cozinha", r"cozinha|kitchen|copa"), ("quarto", r"quarto|suite|dormit|bedroom|qt\b"),
        ("wc", r"\bwc\b|\bi\.?s\.?\b|sanit|banho|bath|lavabo"), ("hall", r"hall|entrada"), ("corredor", r"corredor|circula"),
        ("arrumos", r"arrumo|despensa|dispensa|storage|arrecad"), ("garagem", r"garag"), ("varanda", r"varanda|terraco|balcon"),
        ("escritorio", r"escrit|gabinete|office"), ("lavandaria", r"lavand|laundry")]

def uso_por_nome(nome: str) -> str:
    n = _norm(nome)
    return next((u for u, rx in USOS if re.search(rx, n)), "outro")

def extrair_divisoes(d: dict, camada_divisoes: str, unit_m: float, area_min_m2: float = 1.0) -> dict:
    """Divisoes = polilinhas FECHADAS na camada indicada; nomes dos TEXT/MTEXT dentro de cada uma; portas/janelas por blocos."""
    avisos = list(d["avisos"])
    polis = [[(x * unit_m, y * unit_m) for x, y in e.pts] for e in d["entidades"]
             if e.tipo == "POLY" and e.fechada and e.layer == camada_divisoes and len(e.pts) >= 3]
    polis = [p for p in polis if _area(p) >= area_min_m2]
    # envolvente do edificio: contem >= 2 outras divisoes
    def centro(p): return (sum(x for x, _ in p) / len(p), sum(y for _, y in p) / len(p))
    finais = []
    for i, p in enumerate(polis):
        if sum(1 for j, q in enumerate(polis) if j != i and _dentro(centro(q), p)) >= 2:
            avisos.append(f"Polilinha de {_area(p):.1f} m2 ignorada (parece o contorno do edificio)")
            continue
        finais.append(p)
    textos = [(e.pts[0][0] * unit_m, e.pts[0][1] * unit_m, e.texto) for e in d["entidades"] if e.tipo == "TEXT" and e.texto.strip()]
    divisoes = []
    for i, p in enumerate(finais, 1):
        dentro = [t for x, y, t in textos if _dentro((x, y), p)]
        nomes = [t for t in dentro if not re.fullmatch(r"[\d.,\s]*(m2|m²)?", _norm(t).strip())]
        nome = " ".join(nomes[:2]) if nomes else f"Divisao {i}"
        if not nomes:
            avisos.append(f"r{i}: sem texto com o nome da divisao: usado '{nome}' (corrigir na app)")
        divisoes.append({"id": f"r{i}", "name": nome, "use": uso_por_nome(nome), "polygon": [[round(x, 4), round(y, 4)] for x, y in p],
                         "source": "dxf", "confirmed": False})
    aberturas, n = [], 0
    for e in d["entidades"]:
        if e.tipo != "INSERT":
            continue
        nb = _norm(e.nome + " " + e.layer)
        kind = "porta" if re.search(r"porta|door|\bpt\b", nb) else "janela" if re.search(r"janela|window|\bjan\b|vao", nb) else None
        if not kind:
            continue
        pos = (e.pts[0][0] * unit_m, e.pts[0][1] * unit_m)
        alvo = min(divisoes, key=lambda r: _dist_aresta(pos, r["polygon"]), default=None)
        if alvo and _dist_aresta(pos, alvo["polygon"]) < 0.5:
            n += 1
            aberturas.append({"id": f"{'p' if kind == 'porta' else 'j'}{n}", "kind": kind, "room_id": alvo["id"],
                              "pos": [round(pos[0], 4), round(pos[1], 4)], "width_m": 0.9 if kind == "porta" else 1.2})
    if not divisoes:
        avisos.append("Nenhuma divisao encontrada: a camada indicada nao tem polilinhas fechadas. "
                      "Se a planta so tem paredes (linhas), pedir ao arquiteto uma camada de areas ou desenhar polilinhas fechadas.")
    return {"divisoes": divisoes, "aberturas": aberturas, "avisos": avisos}
