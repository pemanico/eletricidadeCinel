"""Divisoes a partir de PAREDES (linhas), independente do formato (PDF, DXF/DWG so com paredes).

Metodo (determinista):
1. Aberturas: as pontas das paredes sao segmentos curtos (espessura da parede). Duas pontas paralelas, alinhadas,
   com a mesma espessura e frente a frente (0.4 a 5 m) sao os dois lados de uma porta/janela -> fecham-se com
   duas linhas ("pontes").
2. Rasterizacao das paredes+pontes (res. 2 cm) e preenchimento do espaco livre (conectividade 4).
   Regioes que tocam o bordo = exterior.
3. Cada etiqueta (nome da divisao) cai numa regiao -> divisao. Area = pixeis + meia linha no contorno.
4. Validacao contra o quadro de areas do arquiteto (se existir): areas, escala, etiquetas em falta,
   regioes fundidas (duas etiquetas na mesma regiao) e etiquetas em espaco aberto/exterior.

Nada disto e norma: e geometria. Tudo sai com confirmed=False (CLAUDE.md)."""
from __future__ import annotations
import math, re, statistics, unicodedata
from .dxfread import uso_por_nome

RES = 0.02          # m por pixel
TOL_OK, TOL_AVISO = 0.03, 0.08   # diferenca relativa de area: <=3% ok, <=8% aviso, >8% erro
# Divisoes fundidas: usar o uso mais exigente (mais tomadas/circuitos), para errar por excesso e nunca por defeito.
# Ordem pela densidade de tomadas da convencao de projeto v1 (data/convencoes/convencao_projeto_v1.json; e
# CONVENCAO do projeto, nao regra do RTIEBT). Teste manual 14-10: Hall 1+Sala+Cozinha+... ficava "hall" (1 tomada/100 m2).
USO_PRIORIDADE = ["cozinha", "sala", "escritorio", "lavandaria", "quarto", "outro", "garagem", "wc", "hall", "corredor", "arrumos", "varanda"]

def uso_fundida(nomes: list[str]) -> str:
    usos = [uso_por_nome(nm) for nm in nomes]
    return min(usos, key=lambda u: USO_PRIORIDADE.index(u) if u in USO_PRIORIDADE else len(USO_PRIORIDADE))

ESCALAS_NORMAIS = (20, 25, 50, 75, 100, 125, 150, 200, 250, 500, 1000)   # escalas usuais de desenho de arquitetura

def sugerir_escala(razoes: list[float], escala: float) -> float:
    """Escala sugerida quando as areas nao batem com o quadro. razoes = area_calculada / area_quadro a 1:escala.
    A area escala com o quadrado da escala: a 1:s, razao_s = razao * (s/escala)^2. Primeiro tenta as escalas
    usuais e escolhe a que poe mais divisoes a +-3% (>=2); so se nenhuma servir devolve a estimativa pela mediana.
    (Teste manual 14-10: divisoes fundidas puxavam a mediana e a app sugeria 1:116 em vez de 1:100.)"""
    melhor, n_melhor = None, 1
    for s_ in ESCALAS_NORMAIS:
        if s_ == escala: continue
        k = (s_ / escala) ** 2
        n = sum(1 for r in razoes if abs(r * k - 1) <= TOL_OK)
        if n > n_melhor: melhor, n_melhor = s_, n
    return melhor if melhor else escala / math.sqrt(statistics.median(razoes))

def _norm(t: str) -> str:
    return unicodedata.normalize("NFKD", t.lower()).encode("ascii", "ignore").decode().replace(" ", "")

# ---------- 1. aberturas (pontes entre pontas de parede) ----------

def _pontas(segs):
    ends = {}
    for s_ in segs:
        for p_ in s_:
            ends.setdefault((round(p_[0], 2), round(p_[1], 2)), []).append(s_)
    return ends

def _corpo(a, b, u, ends):
    """Direcao (unitaria) em que se estende o corpo da parede a partir da ponta (a,b), ou None."""
    for p_ in (a, b):
        k = (round(p_[0], 2), round(p_[1], 2))
        for s2 in ends.get(k, []):
            if s2 == (a, b) or s2 == (b, a): continue
            q = s2[1] if (round(s2[0][0], 2), round(s2[0][1], 2)) == k else s2[0]
            L2 = math.hypot(q[0] - p_[0], q[1] - p_[1])
            if L2 < 0.1: continue
            v = ((q[0] - p_[0]) / L2, (q[1] - p_[1]) / L2)
            if abs(v[0] * u[0] + v[1] * u[1]) < 0.2:
                return v
    return None

def pontes(segs, cap_min=0.05, cap_max=0.50, gap_min=0.40, gap_max=5.0):
    ends = _pontas(segs)
    caps = []
    for (a, b) in segs:
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if cap_min <= L <= cap_max:
            u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
            caps.append({"a": a, "b": b, "L": L, "u": u, "m": ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), "corpo": _corpo(a, b, u, ends)})
    cand = []
    for i, c in enumerate(caps):
        for j in range(i + 1, len(caps)):
            d = caps[j]
            if abs(c["L"] - d["L"]) > 0.04 or abs(c["u"][0] * d["u"][0] + c["u"][1] * d["u"][1]) < 0.996:
                continue
            vx, vy = d["m"][0] - c["m"][0], d["m"][1] - c["m"][1]
            dist = math.hypot(vx, vy)
            if not gap_min <= dist <= gap_max:
                continue
            if abs(vx * c["u"][0] + vy * c["u"][1]) > 0.03:      # desalinhadas (nao estao na mesma parede)
                continue
            # cada ponta tem de olhar para a outra (para fora do corpo da sua parede), senao e o proprio troco de parede
            if c["corpo"] and (vx * c["corpo"][0] + vy * c["corpo"][1]) / dist > -0.9: continue
            if d["corpo"] and (-vx * d["corpo"][0] - vy * d["corpo"][1]) / dist > -0.9: continue
            cand.append((dist, i, j))
    cand.sort()
    usados, out = set(), []
    for dist, i, j in cand:
        if i in usados or j in usados:
            continue
        c, d = caps[i], caps[j]
        if _cruza((c["m"], d["m"]), segs, ignorar=((c["a"], c["b"]), (d["a"], d["b"]))):
            continue
        usados |= {i, j}
        # ligar extremo a extremo do mesmo lado
        pc = sorted([c["a"], c["b"]], key=lambda p: p[0] * c["u"][0] + p[1] * c["u"][1])
        pd = sorted([d["a"], d["b"]], key=lambda p: p[0] * c["u"][0] + p[1] * c["u"][1])
        out.append({"segs": [(pc[0], pd[0]), (pc[1], pd[1])], "largura": round(dist, 2), "espessura": round(c["L"], 2),
                    "meio": ((c["m"][0] + d["m"][0]) / 2, (c["m"][1] + d["m"][1]) / 2), "atraves": c["u"]})
    return out

def _raio(p, d, segs, max_d):
    """Distancia ao primeiro segmento atingido por um raio a partir de p na direcao d (unitaria), ou None."""
    best = None
    for (a, b) in segs:
        ex, ey = b[0] - a[0], b[1] - a[1]
        den = d[0] * ey - d[1] * ex
        if abs(den) < 1e-12:
            continue
        wx, wy = a[0] - p[0], a[1] - p[1]
        t = (wx * ey - wy * ex) / den          # distancia ao longo do raio
        u = (wx * d[1] - wy * d[0]) / den      # posicao no segmento
        if 0.005 < t <= max_d and -1e-9 <= u <= 1 + 1e-9 and (best is None or t < best):
            best = t
    return best

def portas_face(segs, cap_min=0.05, cap_max=0.30, gap_min=0.60, gap_max=1.30):
    """Porta entre a PONTA de uma parede e a FACE de outra (caso tipico das portas interiores): da ponta,
    dois raios para fora (sentido oposto ao corpo da parede); se ambos batem numa parede a 0.6-1.3 m e a
    distancias iguais (+-5 cm), fecha-se com duas linhas."""
    ends = _pontas(segs)
    out = []
    for (a, b) in segs:
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if not cap_min <= L <= cap_max:
            continue
        u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        corpo = _corpo(a, b, u, ends)
        if not corpo:
            continue
        fora = (-corpo[0], -corpo[1])
        ta, tb = _raio(a, fora, segs, gap_max), _raio(b, fora, segs, gap_max)
        if ta and tb and gap_min <= min(ta, tb) and abs(ta - tb) <= 0.05:
            pa = (a[0] + fora[0] * ta, a[1] + fora[1] * ta); pb = (b[0] + fora[0] * tb, b[1] + fora[1] * tb)
            m = ((a[0] + b[0]) / 2 + fora[0] * ta / 2, (a[1] + b[1]) / 2 + fora[1] * ta / 2)
            out.append({"segs": [(a, pa), (b, pb)], "largura": round((ta + tb) / 2, 2), "espessura": round(L, 2),
                        "meio": m, "atraves": u})
    return out

def _sem_duplicados(pt):
    out = []
    for p_ in pt:
        if not any(math.hypot(p_["meio"][0] - q["meio"][0], p_["meio"][1] - q["meio"][1]) < 0.05 for q in out):
            out.append(p_)
    return out

def _cruza(seg, segs, ignorar=()):
    (x1, y1), (x2, y2) = seg
    for s in segs:
        if s in ignorar:
            continue
        (x3, y3), (x4, y4) = s
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(den) < 1e-12:
            continue
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
        if 0.02 < t < 0.98 and 0 <= u <= 1:
            return True
    return False

# ---------- 2. raster ----------

def _raster(segs, res=RES, margem=0.5):
    import numpy as np
    xs = [p[0] for s in segs for p in s]; ys = [p[1] for s in segs for p in s]
    ox, oy = min(xs) - margem, min(ys) - margem
    w = int((max(xs) - ox + margem) / res) + 1; h = int((max(ys) - oy + margem) / res) + 1
    if w * h > 40_000_000:
        raise ValueError("desenho demasiado grande para rasterizar (escala errada?)")
    g = np.zeros((h, w), dtype=bool)
    for (a, b) in segs:
        n = max(2, int(math.hypot(b[0] - a[0], b[1] - a[1]) / (res / 3)) + 2)
        t = np.linspace(0, 1, n)
        cx = ((a[0] + (b[0] - a[0]) * t - ox) / res).astype(int)
        cy = ((a[1] + (b[1] - a[1]) * t - oy) / res).astype(int)
        g[cy.clip(0, h - 1), cx.clip(0, w - 1)] = True
    return g, (ox, oy)

def _px(p, o, res=RES):
    return int((p[1] - o[1]) / res), int((p[0] - o[0]) / res)

# ---------- 3. contorno ----------

def _contorno(mask):
    """Contorno exterior (Moore-neighbour tracing, criterio de paragem de Jacob) de uma mascara com uma regiao.
    Devolve pixeis (linha, coluna) por ordem, sentido horario."""
    import numpy as np
    H, W = mask.shape
    ys, xs = np.nonzero(mask)
    k = int(np.argmin(ys * W + xs))
    start = (int(ys[k]), int(xs[k]))
    viz = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]   # N, NE, E, SE, S, SW, W, NW
    on = lambda r, c: 0 <= r < H and 0 <= c < W and bool(mask[r, c])
    pts, cur, back = [start], start, 6          # o pixel a oeste do inicio e fundo
    primeiro_passo = None
    for _ in range(8 * int(mask.sum()) + 16):
        achou = False
        for t in range(1, 9):
            d = (back + t) % 8
            r, c = cur[0] + viz[d][0], cur[1] + viz[d][1]
            if on(r, c):
                back = (d + 4 + 1) % 8 if d % 2 == 0 else (d + 4 + 2) % 8   # vizinho anterior (fundo) visto do novo pixel
                back = (back - 1) % 8
                nxt = (r, c)
                achou = True
                break
        if not achou:
            return pts                          # pixel isolado
        if primeiro_passo is None:
            primeiro_passo = nxt
        elif cur == start and nxt == primeiro_passo:
            return pts[:-1]
        cur = nxt
        pts.append(cur)
    return pts

def _dp(pts, eps):
    """Douglas-Peucker (pontos em metros)."""
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    L = math.hypot(x2 - x1, y2 - y1) or 1e-12
    dmax, idx = 0, 0
    for i in range(1, len(pts) - 1):
        d = abs((x2 - x1) * (y1 - pts[i][1]) - (x1 - pts[i][0]) * (y2 - y1)) / L
        if d > dmax:
            dmax, idx = d, i
    if dmax > eps:
        return _dp(pts[:idx + 1], eps)[:-1] + _dp(pts[idx:], eps)
    return [pts[0], pts[-1]]

def _simplificar_fechado(pts, eps):
    """Douglas-Peucker num contorno FECHADO: parte no ponto mais afastado do inicio e simplifica as duas metades."""
    if len(pts) < 4:
        return pts
    k = max(range(len(pts)), key=lambda i: (pts[i][0] - pts[0][0]) ** 2 + (pts[i][1] - pts[0][1]) ** 2)
    a = _dp(pts[:k + 1], eps); b = _dp(pts[k:] + [pts[0]], eps)
    return a[:-1] + b[:-1]

def _desviar(poly, d):
    """Desloca cada aresta de um poligono simples d metros para FORA (intersecao das arestas deslocadas)."""
    n = len(poly)
    sa = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
    sg = 1 if sa > 0 else -1                    # anti-horario: a normal exterior e (dy, -dx)
    linhas = []
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        L = math.hypot(x2 - x1, y2 - y1) or 1e-12
        nx, ny = sg * (y2 - y1) / L, -sg * (x2 - x1) / L
        linhas.append(((x1 + nx * d, y1 + ny * d), (x2 + nx * d, y2 + ny * d)))
    out = []
    for i in range(n):
        (a1, a2), (b1, b2) = linhas[i - 1], linhas[i]
        dx1, dy1, dx2, dy2 = a2[0] - a1[0], a2[1] - a1[1], b2[0] - b1[0], b2[1] - b1[1]
        den = dx1 * dy2 - dy1 * dx2
        if abs(den) < 1e-12:
            out.append(b1)
        else:
            t = ((b1[0] - a1[0]) * dy2 - (b1[1] - a1[1]) * dx2) / den
            out.append((a1[0] + t * dx1, a1[1] + t * dy1))
    return out

def _area(p):
    n = len(p)
    return abs(sum(p[i][0] * p[(i + 1) % n][1] - p[(i + 1) % n][0] * p[i][1] for i in range(n))) / 2

# ---------- etiquetas ----------

def etiquetas(palavras, nomes: list[str] | None):
    """Encontra no desenho cada nome (pode ter varias palavras). Sem quadro de areas: palavras com uso conhecido.
    palavras: [{'t', 'pos': (x,y) metros, 'x0','x1','y0','y1' (pt)}]."""
    ws = sorted(palavras, key=lambda w: (-round(w["y0"]), w["x0"]))
    out = []
    if nomes:
        for nome in nomes:
            alvo = _norm(nome)
            for i, w in enumerate(ws):
                if not alvo.startswith(_norm(w["t"])) or not _norm(w["t"]):
                    continue
                seq, txt = [w], _norm(w["t"])
                while txt != alvo and len(seq) < 6:
                    ult = seq[-1]
                    nxt = [v for v in ws if v is not ult and abs(v["y0"] - ult["y0"]) < 2 and 0 <= v["x0"] - ult["x1"] < 8
                           and alvo.startswith(txt + _norm(v["t"]))]
                    if not nxt: break
                    seq.append(nxt[0]); txt += _norm(nxt[0]["t"])
                if txt == alvo:
                    xs = [v["pos"][0] for v in seq]; ys = [v["pos"][1] for v in seq]
                    out.append({"nome": nome, "pos": (sum(xs) / len(xs), sum(ys) / len(ys))})
    else:
        for i, w in enumerate(ws):
            if len(w["t"]) >= 3 and uso_por_nome(w["t"]) != "outro":
                nxt = [v for v in ws if abs(v["y0"] - w["y0"]) < 2 and 0 <= v["x0"] - w["x1"] < 8 and re.fullmatch(r"\d{1,2}", v["t"])]
                nome = w["t"] + (" " + nxt[0]["t"] if nxt else "")
                out.append({"nome": nome, "pos": w["pos"]})
    return out

# ---------- principal ----------

FAIXA = 0.25       # m: linhas auxiliares (caixilharia/aros) so contam se ficarem dentro da faixa das paredes

def filtrar_vaos(segs, aux):
    """Das linhas auxiliares (camada de vistas: caixilharia e aros, mas tambem loicas, bancadas, roupeiros) guarda so
    as que estao no PROLONGAMENTO de uma parede: paralelas (<3 graus) a um segmento de parede, com os dois extremos a
    menos de FAIXA da linha dessa parede e a menos de FAIXA de alguma parede (ficam dentro da faixa da parede).
    Assim fecham-se os vaos sem as frentes de bancadas/roupeiros (paralelas mas a ~0.6 m) roubarem area."""
    import numpy as np
    from scipy import ndimage
    if not aux:
        return []
    g, o = _raster(list(segs) + list(aux))
    gp, _ = _raster_em(segs, o, g.shape)
    dist = ndimage.distance_transform_edt(~gp) * RES
    def perto(p):
        r, c = _px(p, o)
        return dist[min(max(r, 0), dist.shape[0] - 1), min(max(c, 0), dist.shape[1] - 1)] <= FAIXA
    dirs = []
    for (a, b) in segs:
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L >= 0.3:
            dirs.append((a, ((b[0] - a[0]) / L, (b[1] - a[1]) / L)))
    out = []
    for s in aux:
        (a, b) = s
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L < 0.05 or not (perto(a) and perto(b)):
            continue
        u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        for (q, v) in dirs:
            if abs(u[0] * v[0] + u[1] * v[1]) < 0.9986:          # ~3 graus
                continue
            da = abs((a[0] - q[0]) * v[1] - (a[1] - q[1]) * v[0]); db = abs((b[0] - q[0]) * v[1] - (b[1] - q[1]) * v[0])
            if da <= FAIXA and db <= FAIXA:
                out.append(s)
                break
    return out

def _raster_em(segs, o, shape, res=RES):
    import numpy as np
    g = np.zeros(shape, dtype=bool)
    h, w = shape
    for (a, b) in segs:
        n = max(2, int(math.hypot(b[0] - a[0], b[1] - a[1]) / (res / 3)) + 2)
        t = np.linspace(0, 1, n)
        cx = ((a[0] + (b[0] - a[0]) * t - o[0]) / res).astype(int)
        cy = ((a[1] + (b[1] - a[1]) * t - o[1]) / res).astype(int)
        g[cy.clip(0, h - 1), cx.clip(0, w - 1)] = True
    return g, o

def detetar(segs, palavras, quadro: dict[str, float] | None = None, piso: int = 0, escala: float | None = None, aux=None) -> dict:
    """segs: paredes [((x,y),(x,y))] em metros; aux: linhas de caixilharia/aros (filtradas por filtrar_vaos);
    palavras: ver etiquetas(); quadro: {nome: area_m2} do arquiteto."""
    import numpy as np
    from scipy import ndimage
    avisos = []                         # [{'nivel': 'erro'|'aviso'|'info', 'msg': str}]
    A = lambda nivel, msg: avisos.append({"nivel": nivel, "msg": msg})
    if not segs:
        return {"divisoes": [], "aberturas": [], "avisos": [{"nivel": "erro", "msg": "sem linhas de parede"}], "validacao": []}
    vaos = filtrar_vaos(segs, aux or [])
    pt = pontes(segs)
    pt = _sem_duplicados(pt + portas_face(list(segs) + vaos + [x for p in pt for x in p["segs"]]))
    todas = list(segs) + vaos + [s for p in pt for s in p["segs"]]
    g, o = _raster(todas)
    lab, n = ndimage.label(~g)          # conectividade 4: diagonais das paredes nao deixam passar
    bordo = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    ets = etiquetas(palavras, list(quadro) if quadro else None)
    if quadro:
        for nome in quadro:
            if not any(e["nome"] == nome for e in ets):
                A("aviso", f"'{nome}' esta no quadro de areas mas nao foi encontrado no desenho")
    if not ets:
        A("erro", "nenhum nome de divisao encontrado no desenho")
    por_regiao: dict[int, list] = {}
    for e in ets:
        r, c = _px(e["pos"], o)
        if not (0 <= r < lab.shape[0] and 0 <= c < lab.shape[1]):
            continue
        reg = int(lab[r, c])
        if reg == 0:                    # etiqueta em cima de uma linha: procurar pixel livre vizinho
            jan = lab[max(0, r - 3):r + 4, max(0, c - 3):c + 4]
            livres = jan[jan > 0]
            reg = int(livres[0]) if livres.size else 0
        por_regiao.setdefault(reg, []).append(e)
    divisoes, validacao, razoes, div_de = [], [], [], {}
    piso_id = f"p{piso}".replace("-", "m")
    i = 0
    for reg, es in sorted(por_regiao.items(), key=lambda kv: kv[1][0]["nome"]):
        nomes = [e["nome"] for e in es]
        if reg == 0 or reg in bordo:
            for nm in nomes:
                A("aviso", f"'{nm}': espaco nao fechado por paredes (exterior, alpendre ou aberto): nao importado, desenhar a mao se for preciso")
                validacao.append({"nome": nm, "estado": "nao_fechado", "area_calc": None, "area_quadro": (quadro or {}).get(nm)})
            continue
        mask = lab == reg
        mask_d = ndimage.binary_dilation(mask)          # incluir meia linha de parede
        area = float(mask.sum() + (mask_d.sum() - mask.sum()) / 2) * RES * RES
        ys, xs = np.nonzero(mask_d)
        sub = mask_d[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        cont = [((c + xs.min() + 0.5) * RES + o[0], (r + ys.min() + 0.5) * RES + o[1]) for r, c in _contorno(sub)]
        poly = _simplificar_fechado(cont, 0.03)
        if len(poly) >= 3:
            poly = _desviar(poly, RES / 2)      # o contorno passa pelo centro dos pixeis da orla: +meio pixel
        if len(poly) < 3:
            continue
        uso = uso_fundida(nomes)
        if len(nomes) > 1:
            soma = sum((quadro or {}).get(nm) or 0 for nm in nomes)
            extra = f"; soma no quadro {soma:.2f} m2 ({(area - soma) / soma * 100:+.1f}%)" if soma else ""
            usos = sorted({uso_por_nome(nm) for nm in nomes}, key=USO_PRIORIDADE.index)
            A("erro", f"{' + '.join(nomes)} ficaram na mesma divisao ({area:.2f} m2{extra}): espaco aberto ou porta nao detetada, dividir a mao. "
                      f"Uso atribuido: '{uso}' (o mais exigente de {', '.join(usos)}: erra por excesso ate a divisao ser dividida)")
        i += 1
        nome = nomes[0] if len(nomes) == 1 else " + ".join(nomes)
        divisoes.append({"id": f"{piso_id}r{i}", "name": nome, "use": uso, "floor": piso,
                         "polygon": [[round(x, 3), round(y, 3)] for x, y in poly], "source": "pdf", "confirmed": False})
        div_de[reg] = divisoes[-1]
        for nm in nomes:
            aq = (quadro or {}).get(nm)
            linha = {"nome": nm, "id": f"{piso_id}r{i}", "area_calc": round(area, 2), "area_poligono": round(float(_area(poly)), 2), "area_quadro": aq}
            if len(nomes) > 1:
                linha["estado"] = "fundida"
            elif aq:
                dif = (area - aq) / aq
                linha["dif_pct"] = round(dif * 100, 1)
                razoes.append(area / aq)
                linha["estado"] = "ok" if abs(dif) <= TOL_OK else "aviso" if abs(dif) <= TOL_AVISO else "erro"
                if linha["estado"] != "ok":
                    A(linha["estado"], f"'{nm}': area calculada {area:.2f} m2 vs quadro {aq:.2f} m2 ({dif * 100:+.1f}%)")
            else:
                linha["estado"] = "sem_referencia"
            validacao.append(linha)
    # regioes fechadas sem nome
    tam = ndimage.sum_labels(np.ones_like(lab), lab, index=np.arange(n + 1)) * RES * RES
    sem = [r for r in range(1, n + 1) if r not in bordo and r not in por_regiao and tam[r] >= 1.5]
    for r in sem:
        A("aviso", f"espaco fechado de {tam[r]:.1f} m2 sem nome (courette, arrumo, ou parede com folga): rever")
    # escala: se as areas falham todas pelo mesmo fator, a escala esta errada
    esc_info = None
    if len(razoes) >= 2:
        med = statistics.median(razoes)
        boas = sum(1 for r_ in razoes if abs(r_ - 1) <= TOL_OK)
        esc_info = {"razao_mediana_area": round(med, 3), "n": len(razoes), "dentro_3pct": boas, "validada": boas >= 2}
        if boas >= 2:
            pass                         # >=2 divisoes batem com o quadro a 3%: escala confirmada
        elif abs(med - 1) > TOL_OK and escala:
            sug = sugerir_escala(razoes, escala)
            esc_info["escala_sugerida"] = round(sug)
            A("erro", f"as areas diferem todas ~{(med - 1) * 100:+.0f}% do quadro: a escala 1:{escala:g} parece errada (1:{sug:.0f}?)")
    elif len(razoes) == 1 and escala and not 0.67 < razoes[0] < 1.5:
        sug = escala / math.sqrt(razoes[0])
        esc_info = {"razao_mediana_area": round(razoes[0], 3), "n": 1, "dentro_3pct": 0, "validada": False, "escala_sugerida": round(sug)}
        A("erro", f"a unica divisao comparavel difere {(razoes[0] - 1) * 100:+.0f}% do quadro: a escala 1:{escala:g} parece errada (1:{sug:.0f}?)")
    elif quadro:
        A("aviso", "poucas divisoes comparaveis com o quadro de areas: escala nao validada")
    else:
        A("aviso", "sem quadro de areas no desenho: areas e escala NAO validadas (confirmar com uma cota)")
    # aberturas -> portas/janelas na divisao mais proxima de cada lado
    aberturas = []
    for k, p in enumerate(pt, 1):
        lados = []
        for sgn in (1, -1):
            q = (p["meio"][0] + sgn * p["atraves"][0] * (p["espessura"] / 2 + 0.15), p["meio"][1] + sgn * p["atraves"][1] * (p["espessura"] / 2 + 0.15))
            r, c = _px(q, o)
            if 0 <= r < lab.shape[0] and 0 <= c < lab.shape[1]:
                lados.append(int(lab[r, c]))
        div = next((div_de[l] for l in lados if l in div_de), None)
        exterior = any(l in bordo for l in lados)
        if div:
            aberturas.append({"id": f"{piso_id}a{k}", "kind": "janela" if exterior and p["espessura"] >= 0.25 else "porta",
                              "room_id": div["id"], "pos": [round(p["meio"][0], 3), round(p["meio"][1], 3)], "width_m": p["largura"]})
    ok = sum(1 for v in validacao if v["estado"] == "ok")
    resumo = {"divisoes": len(divisoes), "pontes": len(pt), "vaos": len(vaos), "comparadas": len(razoes), "ok": ok,
              "erros": sum(1 for a in avisos if a["nivel"] == "erro"), "avisos": sum(1 for a in avisos if a["nivel"] == "aviso")}
    return {"divisoes": divisoes, "aberturas": aberturas, "avisos": avisos, "validacao": validacao, "escala": esc_info, "resumo": resumo}


_COR = {"ok": "#2e9d5b", "aviso": "#e0a020", "erro": "#d0453a", "fundida": "#d0453a", "sem_referencia": "#4a7fd0"}

def svg_previsao(segs, resultado, aux=()) -> str:
    """Pre-visualizacao: paredes (cinzento), divisoes coloridas pelo estado da validacao, nome e area."""
    from xml.sax.saxutils import escape
    pts = [p for s_ in segs for p in s_]
    if not pts:
        return "<svg xmlns='http://www.w3.org/2000/svg'/>"
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts); y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    W, H = x1 - x0 + 1, y1 - y0 + 1
    Y = lambda y: round(y1 + 0.5 - y, 3); X = lambda x: round(x - x0 + 0.5, 3)
    est = {}
    for v in resultado.get("validacao", []):
        if v.get("id"): est.setdefault(v["id"], v["estado"])
    out = [f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W:.2f} {H:.2f}' style='width:100%;max-height:70vh;background:#fff'>"]
    for d in resultado.get("divisoes", []):
        c = _COR.get(est.get(d["id"]), "#999")
        pp = " ".join(f"{X(x)},{Y(y)}" for x, y in d["polygon"])
        out.append(f"<polygon points='{pp}' fill='{c}' fill-opacity='0.35' stroke='{c}' stroke-width='0.04'/>")
    for (a, b) in list(segs) + list(aux):
        out.append(f"<line x1='{X(a[0])}' y1='{Y(a[1])}' x2='{X(b[0])}' y2='{Y(b[1])}' stroke='#333' stroke-width='0.025'/>")
    for d in resultado.get("divisoes", []):
        cx = sum(x for x, _ in d["polygon"]) / len(d["polygon"]); cy = sum(y for _, y in d["polygon"]) / len(d["polygon"])
        out.append(f"<text x='{X(cx)}' y='{Y(cy)}' font-size='0.35' text-anchor='middle' font-family='sans-serif'>{escape(d['name'])}</text>")
    return "".join(out) + "</svg>"
