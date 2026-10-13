"""Leitor de PDF vetorial de arquitetura (plot direto do CAD, com camadas/OCG).

O que faz (determinista, sem LLM):
- analisar(): lista as paginas com designacao, escala do carimbo, camadas (nr. de segmentos) e quadro de areas.
- extrair(): segmentos da(s) camada(s) escolhida(s) em METROS reais, textos com posicao, quadro de areas,
  (a escala e validada depois, pelas areas, em cad/divisoes.py).

Limites: PDF de imagem (digitalizado) nao tem vetores -> recusado com mensagem; PDF sem camadas (OCG)
-> todas as linhas ficam na camada "(sem camada)" e a deteccao de paredes fica pouco fiavel (aviso).
Unidades: PDF em pontos (1/72 pol). Metros reais = pt * 25.4/72 / 1000 * escala.
Dependencias: pikepdf (geometria + camadas), pypdfium2 (texto rapido de todas as paginas),
pdfplumber (palavras com posicao, so na pagina escolhida)."""
from __future__ import annotations
import io, math, re, statistics
from collections import Counter

SEM_CAMADA = "(sem camada)"

class PdfError(ValueError):
    pass

def _libs():
    try:
        import pikepdf, pdfplumber, pypdfium2
    except ImportError as e:
        raise PdfError("faltam dependencias para ler PDF: correr 'pip install -r requirements.txt'") from e
    return pikepdf, pdfplumber, pypdfium2

def _abrir(dados: bytes):
    pikepdf, pdfplumber, pdfium = _libs()
    if not dados.startswith(b"%PDF"):
        raise PdfError("o ficheiro nao e um PDF")
    try:
        return pikepdf.open(io.BytesIO(dados)), pdfplumber.open(io.BytesIO(dados)), pdfium.PdfDocument(dados)
    except Exception as e:
        raise PdfError(f"PDF ilegivel: {type(e).__name__}") from e

def _texto(doc, i: int) -> str:
    return doc[i].get_textpage().get_text_range().replace("\r\n", "\n").replace("\r", "\n")

def m_por_pt(escala: float) -> float:
    return 25.4 / 72 / 1000 * escala

def _mul(a, b):
    """Matrizes PDF [a b c d e f]: resultado = a x b (aplica a, depois b)."""
    return [a[0] * b[0] + a[1] * b[2], a[0] * b[1] + a[1] * b[3],
            a[2] * b[0] + a[3] * b[2], a[2] * b[1] + a[3] * b[3],
            a[4] * b[0] + a[5] * b[2] + b[4], a[4] * b[1] + a[5] * b[3] + b[5]]

def _ap(m, x, y):
    return (m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5])

def segmentos_por_camada(pg) -> dict[str, list]:
    """Percorre o content stream da pagina e devolve {camada: [((x1,y1),(x2,y2)), ...]} em pontos PDF
    (espaco da pagina, y para cima). Curvas de Bezier sao aproximadas pela corda (portas/arcos nao interessam
    para paredes). Ignora caminhos usados so como recorte (W n)."""
    import pikepdf
    props = pg.Resources.get("/Properties", {}) if "/Resources" in pg.obj else {}
    nome = {str(k): str(v.get("/Name", k)) for k, v in props.items()} if props else {}
    out: dict[str, list] = {}
    ctm, pilha, oc = [1, 0, 0, 1, 0, 0], [], []
    caminho, atual, inicio, clip = [], None, None, False
    def camada():
        return next((c for c in reversed(oc) if c), SEM_CAMADA)
    for ops, op in pikepdf.parse_content_stream(pg):
        o = str(op)
        if o == "q": pilha.append(ctm[:])
        elif o == "Q": ctm = pilha.pop() if pilha else ctm
        elif o == "cm": ctm = _mul([float(v) for v in ops], ctm)
        elif o == "BDC": oc.append(nome.get(str(ops[1]), str(ops[1])) if str(ops[0]) == "/OC" else None)
        elif o == "BMC": oc.append(None)
        elif o == "EMC": oc and oc.pop()
        elif o == "m":
            atual = inicio = _ap(ctm, float(ops[0]), float(ops[1]))
        elif o == "l" and atual is not None:
            p = _ap(ctm, float(ops[0]), float(ops[1])); caminho.append((atual, p)); atual = p
        elif o in ("c", "v", "y") and atual is not None:
            p = _ap(ctm, float(ops[-2]), float(ops[-1])); caminho.append((atual, p)); atual = p
        elif o == "re":
            x, y, w, h = (float(v) for v in ops)
            pts = [_ap(ctm, x, y), _ap(ctm, x + w, y), _ap(ctm, x + w, y + h), _ap(ctm, x, y + h)]
            caminho += [(pts[i], pts[(i + 1) % 4]) for i in range(4)]; atual = inicio = pts[0]
        elif o == "h" and atual is not None and inicio is not None:
            if atual != inicio: caminho.append((atual, inicio))
            atual = inicio
        elif o == "W" or o == "W*":
            clip = True
        elif o in ("S", "s", "f", "F", "f*", "B", "B*", "b", "b*", "n"):
            if o in ("s", "b", "b*") and atual is not None and inicio is not None and atual != inicio:
                caminho.append((atual, inicio))
            if o != "n" and not clip:
                out.setdefault(camada(), []).extend(s for s in caminho if s[0] != s[1])
            caminho, atual, inicio, clip = [], None, None, False
    return out

_RX_ESCALA = re.compile(r"\b1\s*:\s*(\d{2,4})\b")
_RX_AREA = re.compile(r"([^\s:][^:\n]{0,60}?)\s*:\s*(\d+[.,]\d+)\s*m[2²]")

def _escala_carimbo(texto: str) -> float | None:
    """Escala mais frequente do tipo 1:N com N comum em arquitetura (ignora '1: 16' de rotulos de vaos)."""
    c = Counter(int(n) for n in _RX_ESCALA.findall(texto) if int(n) in (20, 25, 50, 100, 200, 500, 1000))
    return float(c.most_common(1)[0][0]) if c else None

_RX_DES = re.compile(r"\b(PLANTA (?:D[OAE]S? )?[A-ZÀ-Ý0-9 \-]{2,40}?|ALÇADOS?[A-ZÀ-Ý \-]{0,40}?|CORTES?[A-ZÀ-Ý0-9 \-]{0,30}?|PERFIS[A-Z0-9 ]{0,20}?)(?=\s*(?:\n|P\.|FASE|$))")

def _designacao(texto: str) -> str:
    m = _RX_DES.search(texto) or re.search(r"(PLANTA DO PISO\s*-?\d+|PLANTA D[AO] [A-ZÀ-Ý]+)", texto)
    d = m.group(1).strip() if m else ""
    for f in ("PROPOSTO", "VERMELHOS/AMARELOS", "EXISTENTE"):
        if d and f not in d and re.search(rf"\b{f}\b", texto): return f"{d} ({f.lower()})"
    return d

def quadro_areas(texto: str) -> dict[str, float]:
    """Linhas 'Nome: 12.34m²' (quadro de areas uteis do arquiteto). Ordem preservada."""
    out = {}
    for nome, v in _RX_AREA.findall(texto):
        nome = re.sub(r"^.*\b(?:piso|pisos)\s+-?\d+\s+", "", nome.strip(), flags=re.I)   # "Areas uteis do piso 0 Hall 1"
        nome = re.sub(r"^.*\b(?:uteis|úteis)\b\s*", "", nome)
        if nome: out.setdefault(nome, float(v.replace(",", ".")))
    return out

def _piso(designacao: str) -> int | None:
    m = re.search(r"PISO\s*(-?\d)", designacao.upper())
    if m: return int(m.group(1))
    if re.search(r"R[ÉE]S[- ]DO[- ]CH", designacao.upper()): return 0
    if re.search(r"CAVE", designacao.upper()): return -1
    return None

_RX_PAREDE = re.compile(r"corte|parede|wall|muro|alvenar", re.I)
_RX_VAOS = re.compile(r"vista|caixil|vao|vão|janela|porta|window|door", re.I)

def analisar(dados: bytes) -> dict:
    pk, pl, doc = _abrir(dados)
    paginas, avisos = [], []
    for i, pg in enumerate(pk.pages):
        texto = _texto(doc, i)
        mb = [float(v) for v in pg.MediaBox]
        n_img = sum(1 for v in pg.Resources.get("/XObject", {}).values() if str(v.get("/Subtype")) == "/Image") if "/Resources" in pg.obj else 0
        segs = segmentos_por_camada(pg)
        camadas = {k: len(v) for k, v in sorted(segs.items(), key=lambda kv: -len(kv[1]))}
        des = _designacao(texto)
        areas = quadro_areas(texto)
        sug = next((c for c in camadas if _RX_PAREDE.search(c)), None)
        sug_v = next((c for c in camadas if _RX_VAOS.search(c) and not re.search(r"tracej|hidden", c, re.I)), None)
        paginas.append({"pagina": i + 1, "designacao": des, "escala": _escala_carimbo(texto), "piso": _piso(des),
                        "largura_mm": round((mb[2] - mb[0]) * 25.4 / 72), "altura_mm": round((mb[3] - mb[1]) * 25.4 / 72),
                        "camadas": camadas, "sugestao_camada_paredes": sug, "sugestao_camada_vaos": sug_v, "n_areas_quadro": len(areas),
                        "vetorial": sum(camadas.values()) >= 20, "imagens": n_img})
    if not any(p["vetorial"] for p in paginas):
        avisos.append("Nenhuma pagina com desenho vetorial: parece um PDF digitalizado (imagem). Nao e possivel extrair paredes.")
    elif not any(len(p["camadas"]) > 1 for p in paginas if p["vetorial"]):
        avisos.append("PDF sem camadas (foi regravado/impresso, nao plotado do CAD): paredes misturadas com tudo o resto. Pedir ao arquiteto o PDF plotado do CAD ou o DWG.")
    cand = [p for p in paginas if p["vetorial"] and p["designacao"].upper().startswith("PLANTA") and p["sugestao_camada_paredes"]]
    cand.sort(key=lambda p: ("vermelhos" in p["designacao"] or "existente" in p["designacao"], -p["n_areas_quadro"], p["pagina"]))
    return {"paginas": paginas, "sugestao_pagina": cand[0]["pagina"] if cand else None, "avisos": avisos}

def _palavras(pp):
    """Palavras com posicao em pontos PDF (y para cima, como a geometria)."""
    h = float(pp.height)
    return [{"t": w["text"], "x": (w["x0"] + w["x1"]) / 2, "y": h - (w["top"] + w["bottom"]) / 2,
             "x0": w["x0"], "x1": w["x1"], "y0": h - w["bottom"], "y1": h - w["top"], "upright": w.get("upright", True)}
            for w in pp.extract_words(keep_blank_chars=False, use_text_flow=False)]

def extrair(dados: bytes, pagina: int, camadas_paredes: list[str], escala: float, camadas_vaos: list[str] = ()) -> dict:
    """Geometria da pagina em metros (origem no canto inferior esquerdo das paredes).
    camadas_vaos: camada(s) com caixilharia/aros (ex. vistas), usadas so para fechar vaos."""
    pk, pl, doc = _abrir(dados)
    if not (1 <= pagina <= len(pk.pages)):
        raise PdfError(f"pagina {pagina} nao existe (o PDF tem {len(pk.pages)})")
    if not (escala and escala > 0):
        raise PdfError("escala invalida")
    pg, pp = pk.pages[pagina - 1], pl.pages[pagina - 1]
    segs = segmentos_por_camada(pg)
    paredes = [s for c in camadas_paredes for s in segs.get(c, [])]
    if not paredes:
        raise PdfError(f"a camada {camadas_paredes} nao tem linhas nesta pagina")
    texto = _texto(doc, pagina - 1)
    palavras = _palavras(pp)
    k = m_por_pt(escala)
    x0 = min(min(a[0], b[0]) for a, b in paredes); y0 = min(min(a[1], b[1]) for a, b in paredes)
    x1 = max(max(a[0], b[0]) for a, b in paredes); y1 = max(max(a[1], b[1]) for a, b in paredes)
    M = lambda p: (round((p[0] - x0) * k, 4), round((p[1] - y0) * k, 4))
    dentro = lambda w: x0 - 5 <= w["x"] <= x1 + 5 and y0 - 5 <= w["y"] <= y1 + 5
    return {"pagina": pagina, "escala": escala, "designacao": _designacao(texto), "piso": _piso(_designacao(texto)),
            "segmentos": [(M(a), M(b)) for a, b in paredes],
            "aux": [(M(a), M(b)) for c in camadas_vaos if c not in camadas_paredes for a, b in segs.get(c, [])
                    if x0 - 5 <= a[0] <= x1 + 5 and y0 - 5 <= a[1] <= y1 + 5],
            "palavras": [{**w, "pos": M((w["x"], w["y"]))} for w in palavras if dentro(w)],
            "quadro_areas": quadro_areas(texto)}
