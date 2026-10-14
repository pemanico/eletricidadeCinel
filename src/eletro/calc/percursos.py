"""Comprimentos de cabo a partir da aparelhagem COLOCADA na planta (ESTIMATIVA, sempre sinalizada).

Modelo (convencao, editavel em perfil['comprimentos']):
  modo "teto" (iluminacao): quadro -> sobe ao teto (pe-direito - altura do quadro) -> percorre o teto em L (Manhattan)
    ate cada ponto, pela ordem da cadeia -> desce a cada ponto (pe-direito - altura; luz no teto = 0) e volta a subir.
  modo "parede" (tomadas e dedicados): o cabo corre nas paredes/pavimento a altura dos pontos; vertical = diferenca de
    alturas entre pontos consecutivos (e entre o quadro e o 1.o ponto).
  Horizontal x fator_trajeto (curvas, folgas). Pontos noutro piso: + entre_pisos_m (o referencial de cada piso e o
  do respetivo PDF, por isso a horizontal entre pisos NAO e fiavel -> AVISO; corrigir em circuit_length_m)."""
from __future__ import annotations

def manhattan(a, b) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def percurso(quadro: dict, pontos: list[dict], fator: float, entre_pisos_m: float, modo: str = "teto") -> dict:
    if modo == "parede":
        return _parede(quadro, pontos, fator, entre_pisos_m)
    return _teto(quadro, pontos, fator, entre_pisos_m)

def _parede(quadro, pontos, fator, entre_pisos_m):
    cur, piso, h = tuple(quadro["pos"]), quadro["piso"], quadro["altura"]
    horiz = vert = acum = 0.0
    por_ponto, entre = {}, 0
    for q in pontos:
        hq = q["altura"] if q["altura"] is not None else q["pe_direito"]
        if q["piso"] != piso:
            entre += 1; acum += entre_pisos_m; piso = q["piso"]
        d = manhattan(cur, q["pos"]) * fator
        dv = abs(hq - h)
        horiz += d; vert += dv; acum += d + dv
        por_ponto[q["id"]] = round(acum, 2)
        cur, h = tuple(q["pos"]), hq
    return {"total_m": round(acum, 2), "por_ponto": por_ponto, "horizontal_m": round(horiz, 2),
            "vertical_m": round(vert, 2), "entre_pisos": entre}

def _teto(quadro: dict, pontos: list[dict], fator: float, entre_pisos_m: float) -> dict:
    """quadro = {pos, piso, pe_direito, altura}; pontos (ja pela ordem da cadeia) = [{id, pos, piso, pe_direito, altura}]
    (altura None = teto). Devolve {total_m, por_ponto: {id: distancia acumulada m}, horizontal_m, vertical_m, entre_pisos}."""
    cur, piso = tuple(quadro["pos"]), quadro["piso"]
    horiz = 0.0
    vert = max(0.0, quadro["pe_direito"] - quadro["altura"])      # subida do quadro ao teto
    acum, por_ponto, entre, subir = vert, {}, 0, 0.0
    for q in pontos:
        acum += subir; vert += subir                               # volta a subir do ponto anterior ao teto
        if q["piso"] != piso:
            entre += 1; acum += entre_pisos_m; piso = q["piso"]
        d = manhattan(cur, q["pos"]) * fator
        desc = 0.0 if q["altura"] is None else max(0.0, q["pe_direito"] - q["altura"])
        horiz += d; vert += desc; acum += d + desc
        por_ponto[q["id"]] = round(acum, 2)
        subir, cur = desc, tuple(q["pos"])
    total = horiz + vert + entre * entre_pisos_m
    return {"total_m": round(total, 2), "por_ponto": por_ponto, "horizontal_m": round(horiz, 2),
            "vertical_m": round(vert, 2), "entre_pisos": entre}
