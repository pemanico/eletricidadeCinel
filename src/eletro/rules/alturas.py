"""Alturas de montagem da aparelhagem: preenchimento (CONVENCAO) e verificacoes com fonte.

Fonte normativa consultada: Portaria 949-A/2006 (RTIEBT), texto consolidado em sources/normativas/.
O RTIEBT NAO fixa alturas gerais para tomadas/interruptores em habitacao (pesquisa de "altura" no texto,
2026-10-13). Os valores por defeito sao CONVENCAO (data/convencoes/simbolos_alturas.json, editavel na app).

Regras com fonte que limitam alturas e se aplicam (ou podem aplicar-se) a moradias:
- RTIEBT 701.71.2 (Portaria 949-A/2006): "Nas casas de banho com chuveiros, os aparelhos de iluminacao nao podem
  ser localizados no volume 1 e devem ser instalados a uma altura superior as dos chuveiros."
  -> a altura do chuveiro nao esta no modelo: usa-se o limiar CONVENCIONADO de 2,25 m e o resultado e AVISO.
- RTIEBT 801.3.5.5 (Portaria 949-A/2006): "Os equipamentos intercalados nas canalizacoes devem ser colocados a uma
  altura acima do pavimento superior a 1 m [...]" -- seccao 801.3 (locais com veiculos/risco de explosao).
  Aplicacao a garagem de moradia: POR CONFIRMAR (formador/projetista).
Nao aplicavel a habitacao: 801.2.3.3 (tomadas a >= 1,60 m em escolas para criancas, nota da edicao anotada)."""
from __future__ import annotations
import json
from pathlib import Path

CATALOGO_DEFAULT = Path(__file__).resolve().parents[3] / "data/convencoes/simbolos_alturas.json"
USOS = ("sala", "quarto", "cozinha", "wc", "hall", "corredor", "arrumos", "garagem", "varanda", "escritorio", "lavandaria", "outro")
ALTURA_MAX_M = 6.0
LIMIAR_CHUVEIRO_M = 2.25          # CONVENCAO (altura tipica do chuveiro + folga); ver 701.71.2
GARAGEM_MIN_M = 1.0               # RTIEBT 801.3.5.5 (aplicacao a moradia POR CONFIRMAR)

def carregar(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def altura_por_defeito(kind: str, uso: str, catalogo: dict, pe_direito: float | None = None) -> float | None:
    """Altura CONVENCIONADA do eixo ao pavimento. 'teto' -> pe-direito da divisao (None se desconhecido)."""
    s = catalogo["simbolos"].get(kind)
    if s is None:
        raise ValueError(f"simbolo desconhecido: {kind}")
    h = s.get("por_uso", {}).get(uso, s["altura"])
    if h == "teto":
        return pe_direito
    return float(h)

def fonte_de(kind: str, uso: str, catalogo: dict) -> str:
    s = catalogo["simbolos"][kind]
    if uso in s.get("por_uso", {}):
        return s.get("fontes_por_uso", {}).get(uso, "")
    return s.get("fonte", "")

def guardar(catalogo: dict, path: str) -> None:
    """Escrita atomica (ficheiro temporario + replace): um erro a meio nao corrompe a tabela."""
    import os, tempfile
    validar(catalogo)
    d = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
        json.dump(catalogo, f, ensure_ascii=False, indent=1); f.write("\n")
    os.replace(tmp, path)

def _altura_valida(kind: str, v, catalogo: dict):
    if v == "teto":
        if catalogo["simbolos"][kind]["categoria"] != "luz":
            raise ValueError(f"{kind}: 'teto' so e valido para iluminacao")
        return v
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not (0 < v <= ALTURA_MAX_M):
        raise ValueError(f"{kind}: altura invalida {v!r} (0 < h <= {ALTURA_MAX_M} m, ou 'teto' na iluminacao)")
    return round(float(v), 2)

def validar(catalogo: dict) -> None:
    for k, s in catalogo["simbolos"].items():
        _altura_valida(k, s["altura"], catalogo)
        for u, v in s.get("por_uso", {}).items():
            if u not in USOS: raise ValueError(f"{k}: uso desconhecido '{u}'")
            _altura_valida(k, v, catalogo)
    if not isinstance(catalogo.get("versao"), int) or catalogo["versao"] < 1:
        raise ValueError("tabela sem 'versao' inteira")

def alterar(catalogo: dict, alteracoes: list[dict], autor: str, data: str) -> tuple[dict, list[dict]]:
    """Aplica alteracoes [{kind, uso ('*' = altura por defeito), altura (numero | 'teto' | None = remover excecao),
    fonte}] numa COPIA. Fonte obrigatoria. Devolve (tabela nova com versao+1, entradas de historico)."""
    import copy
    novo = copy.deepcopy(catalogo)
    autor = (autor or "").strip() or "?"
    entradas = []
    for a in alteracoes:
        kind, uso, fonte = a.get("kind"), a.get("uso", "*"), (a.get("fonte") or "").strip()
        if kind not in novo["simbolos"]:
            raise ValueError(f"simbolo desconhecido: {kind}")
        if uso != "*" and uso not in USOS:
            raise ValueError(f"uso desconhecido: {uso}")
        if len(fonte) < 3:
            raise ValueError(f"{kind}/{uso}: indicar a fonte da altura (ex. 'UC 6006, formador, 2026-11-03')")
        s = novo["simbolos"][kind]
        if uso == "*":
            de = s["altura"]
            if a.get("altura") is None: raise ValueError(f"{kind}: a altura por defeito nao pode ser removida")
            para = _altura_valida(kind, a["altura"], novo)
            if para == de and fonte == s.get("fonte"): continue
            s["altura"], s["fonte"] = para, fonte
        else:
            pu, fu = s.setdefault("por_uso", {}), s.setdefault("fontes_por_uso", {})
            de = pu.get(uso)
            if a.get("altura") is None:
                if uso not in pu: continue
                pu.pop(uso); fu.pop(uso, None); para = None
            else:
                para = _altura_valida(kind, a["altura"], novo)
                if para == de and fonte == fu.get(uso): continue
                pu[uso], fu[uso] = para, fonte
            if not pu: s.pop("por_uso"); s.pop("fontes_por_uso", None)
        entradas.append({"kind": kind, "uso": uso, "de": de, "para": para, "fonte": fonte})
    if not entradas:
        raise ValueError("nada mudou")
    novo["versao"] = catalogo["versao"] + 1
    novo.setdefault("historico", []).extend(
        {"versao": novo["versao"], "data": data, "autor": autor, "alteracao": f"{e['kind']} [{e['uso']}]: {e['de']} -> {e['para']}",
         "fonte": e["fonte"]} for e in entradas)
    validar(novo)
    return novo, entradas

def desatualizados(pontos, rooms_por_id: dict, catalogo: dict) -> list:
    """Pontos com altura da CONVENCAO que ja nao coincide com a tabela atual (a tabela mudou depois de os colocar)."""
    out = []
    for q in pontos:
        r = rooms_por_id.get(q.room_id)
        if r is None or q.height_origem != "CONVENCAO" or q.kind not in catalogo["simbolos"]:
            continue
        if altura_por_defeito(q.kind, r.use, catalogo, None) != q.height_m:
            out.append(q)
    return out

def categoria(kind: str, catalogo: dict) -> str:
    s = catalogo["simbolos"].get(kind)
    return s["categoria"] if s else "desconhecido"

def verificar(pontos, rooms_por_id: dict, catalogo: dict) -> list[tuple[str, str, str]]:
    """Devolve [(ref, estado, texto)] para os pontos colocados."""
    out = []
    for q in pontos:
        r = rooms_por_id.get(q.room_id)
        if r is None:
            continue
        cat = categoria(q.kind, catalogo)
        h = q.height_m if q.height_m is not None else r.height_m
        if cat == "desconhecido":
            out.append(("projeto", "AVISO", f"ponto {q.id}: simbolo '{q.kind}' nao existe no catalogo"))
            continue
        # 701.71.2: iluminacao em casa de banho acima do chuveiro
        if r.use == "wc" and cat == "luz" and h is not None and h < LIMIAR_CHUVEIRO_M:
            out.append(("RTIEBT 701.71.2", "AVISO",
                        f"ponto {q.id} ({r.name}): iluminacao a {h:.2f} m; tem de ficar acima do chuveiro e fora do volume 1 "
                        f"(limiar convencionado {LIMIAR_CHUVEIRO_M} m)"))
        # 801.3.5.5: garagem, aparelhagem acima de 1 m (aplicacao POR CONFIRMAR)
        if r.use == "garagem" and cat in ("tomada", "interruptor", "dedicado") and h is not None and h <= GARAGEM_MIN_M:
            out.append(("RTIEBT 801.3.5.5", "POR_CONFIRMAR",
                        f"ponto {q.id} ({r.name}): {h:.2f} m; em locais com veiculos a aparelhagem deve ficar acima de 1 m "
                        f"(aplicacao a garagem de moradia por confirmar)"))
        if h is not None and r.height_m and h > r.height_m + 1e-9:
            out.append(("projeto", "AVISO", f"ponto {q.id} ({r.name}): altura {h:.2f} m acima do pe-direito {r.height_m} m"))
    return out
