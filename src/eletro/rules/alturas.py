"""Alturas de montagem da aparelhagem: preenchimento (CONVENCAO) e verificacoes com fonte.

Fonte normativa consultada: Portaria 949-A/2006 (RTIEBT), texto consolidado em sources/normativas/.
O RTIEBT NAO fixa alturas gerais para tomadas/interruptores em habitacao (pesquisa de "altura" no texto,
2026-10-13). Os valores por defeito sao CONVENCAO (data/convencoes/simbolos_alturas_v1.json).

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

CATALOGO_DEFAULT = Path(__file__).resolve().parents[3] / "data/convencoes/simbolos_alturas_v1.json"
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
