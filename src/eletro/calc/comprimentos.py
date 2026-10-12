"""Comprimentos de cabo ESTIMADOS a partir da planta (nao medidos). Sempre sinalizados como estimativa."""
from ..schema.project import Project

def centro(room) -> tuple[float, float]:
    xs, ys = [p[0] for p in room.polygon], [p[1] for p in room.polygon]
    return ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)

def manhattan(a, b) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def comprimento_circuito(p: Project, room_ids: list[str], fator: float, vertical_m: float) -> float:
    """Percurso quadro -> divisoes na ordem dada (distancia Manhattan entre centros) x fator + descidas."""
    if not p.panel:
        raise ValueError("Projeto sem quadro (panel): impossivel estimar comprimentos")
    rooms = {r.id: r for r in p.rooms}
    pos, total = tuple(p.panel.pos), 0.0
    for rid in room_ids:
        r = rooms[rid]
        if not r.polygon:
            raise ValueError(f"Divisao {rid} sem poligono: impossivel estimar comprimentos")
        c = centro(r)
        total += manhattan(pos, c)
        pos = c
    return total * fator + vertical_m
