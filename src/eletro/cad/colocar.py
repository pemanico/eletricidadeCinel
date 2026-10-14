"""Posicoes INICIAIS da aparelhagem ao preencher pela convencao (o tecnico ajusta depois no editor).
Funciona em divisoes com qualquer orientacao (paredes obliquas): segue o poligono real, nao o retangulo envolvente."""
from __future__ import annotations
import math
from .dxfread import _dentro

def _area_assinada(poly):
    n = len(poly)
    return sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n)) / 2

def centroide(poly):
    a = _area_assinada(poly)
    if abs(a) < 1e-12:
        return (sum(p[0] for p in poly) / len(poly), sum(p[1] for p in poly) / len(poly))
    cx = cy = 0.0
    n = len(poly)
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        f = x1 * y2 - x2 * y1
        cx += (x1 + x2) * f; cy += (y1 + y2) * f
    c = (cx / (6 * a), cy / (6 * a))
    return c if _dentro(c, poly) else ponto_interior(poly)

def ponto_interior(poly):
    """Um ponto garantidamente dentro (divisoes em L/U onde o centroide cai fora)."""
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    y = (min(ys) + max(ys)) / 2
    cortes = []
    n = len(poly)
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            cortes.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
    cortes.sort()
    if len(cortes) >= 2:
        return ((cortes[0] + cortes[1]) / 2, y)
    return ((min(xs) + max(xs)) / 2, y)

def para_dentro(pt, poly, passo=0.05):
    """Se pt esta fora, aproxima-o do centroide ate entrar."""
    if _dentro(pt, poly):
        return pt
    c = centroide(poly)
    d = math.hypot(c[0] - pt[0], c[1] - pt[1])
    n = max(1, int(d / passo))
    for i in range(1, n + 1):
        q = (pt[0] + (c[0] - pt[0]) * i / n, pt[1] + (c[1] - pt[1]) * i / n)
        if _dentro(q, poly):
            return q
    return c

def no_perimetro(poly, n, recuo=0.15, evitar=()):
    """n pontos igualmente espacados ao longo do perimetro REAL, recuados 'recuo' m para dentro.
    'evitar' = posicoes (portas) a manter a >=0.5 m."""
    if n <= 0:
        return []
    m = len(poly)
    sg = 1 if _area_assinada(poly) > 0 else -1          # anti-horario: interior a esquerda
    arestas, total = [], 0.0
    for i in range(m):
        a, b = poly[i], poly[(i + 1) % m]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L > 1e-9:
            arestas.append((a, b, L, total)); total += L
    out = []
    for k in range(n):
        d = (k + 0.5) * total / n
        for _ in range(8):                                 # afastar das portas deslizando no perimetro
            a, b, L, ini = next(x for x in arestas if x[3] <= d % total < x[3] + x[2])
            t = (d % total - ini) / L
            ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
            nx, ny = -uy * sg, ux * sg
            q = (a[0] + ux * t * L + nx * recuo, a[1] + uy * t * L + ny * recuo)
            if all(math.hypot(q[0] - e[0], q[1] - e[1]) >= 0.5 for e in evitar):
                break
            d += 0.6
        out.append(para_dentro(q, poly))
    return out

def eixo_principal(poly):
    """Direcao (unitaria) da aresta mais comprida."""
    m = len(poly)
    a, b = max(((poly[i], poly[(i + 1) % m]) for i in range(m)), key=lambda e: math.hypot(e[1][0] - e[0][0], e[1][1] - e[0][1]))
    L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1
    return ((b[0] - a[0]) / L, (b[1] - a[1]) / L)

def luzes(poly, n):
    """n pontos de luz ao longo do eixo principal, pelo centro da divisao."""
    c = centroide(poly)
    if n <= 1:
        return [c]
    u = eixo_principal(poly)
    proj = [(p[0] - c[0]) * u[0] + (p[1] - c[1]) * u[1] for p in poly]
    lo, hi = min(proj), max(proj)
    return [para_dentro((c[0] + u[0] * (lo + (i + 1) * (hi - lo) / (n + 1)), c[1] + u[1] * (lo + (i + 1) * (hi - lo) / (n + 1))), poly)
            for i in range(n)]

def junto_porta(poly, portas, n, recuo=0.25):
    """Interruptores: junto a porta (se houver), recuados para dentro e espacados 0.2 m; senao no 1.o vertice."""
    base = portas[0] if portas else poly[0]
    c = centroide(poly)
    d = math.hypot(c[0] - base[0], c[1] - base[1]) or 1
    v = ((c[0] - base[0]) / d, (c[1] - base[1]) / d)
    p0 = para_dentro((base[0] + v[0] * (recuo + 0.3), base[1] + v[1] * (recuo + 0.3)), poly)
    return [para_dentro((p0[0] - v[1] * 0.2 * i, p0[1] + v[0] * 0.2 * i), poly) for i in range(n)]
