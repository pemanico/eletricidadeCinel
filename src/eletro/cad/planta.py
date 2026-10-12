"""Vista: planta da moradia em DXF, gerada do Project (apos aplicar overrides)."""
from ..schema.project import Project
from ..schema.dynamic import resolve
from .dxf import Dxf

LAYERS = {"PAREDES": 7, "PORTAS": 3, "JANELAS": 5, "TEXTO": 2, "QUADRO": 1, "LEGENDA": 8, "CARIMBO": 8}

def _center(poly):
    xs, ys = [p[0] for p in poly], [p[1] for p in poly]
    return ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)

def desenhar(p: Project, floor: int = 0) -> tuple[Dxf, list[str]]:
    q, conflicts = resolve(p)
    d = Dxf(LAYERS)
    rooms = {r.id: r for r in q.rooms}
    for r in q.rooms:
        if r.floor != floor or not r.polygon:
            continue
        d.polyline("PAREDES", r.polygon, closed=True)
        cx, cy = _center(r.polygon)
        d.text("TEXTO", (cx - 0.8, cy + 0.1), 0.18, r.name)
        d.text("TEXTO", (cx - 0.8, cy - 0.2), 0.14, f"{r.area_m2:.1f} m2")
    for o in q.openings:
        r = rooms[o.room_id]
        if r.floor != floor: continue
        x, y = o.pos
        layer = "PORTAS" if o.kind == "porta" else "JANELAS"
        d.line(layer, (x - o.width_m / 2, y), (x + o.width_m / 2, y))
    if q.panel and rooms[q.panel.room_id].floor == floor:
        x, y = q.panel.pos
        d.polyline("QUADRO", [(x - .2, y - .1), (x + .2, y - .1), (x + .2, y + .1), (x - .2, y + .1)])
        d.text("QUADRO", (x + .3, y - .05), 0.15, "QE")
    allpts = [pt for r in q.rooms if r.floor == floor for pt in r.polygon]
    x0 = min((p_[0] for p_ in allpts), default=0)
    y0 = min((p_[1] for p_ in allpts), default=0) - 1.5
    d.text("LEGENDA", (x0, y0), 0.15, "Legenda: parede (branco) | porta (verde) | janela (ciano) | QE quadro")
    last = q.revisions[-1] if q.revisions else None
    rev = f"Rev {p.revision}" + (f" {last.date} {last.reason}" if last else "")
    d.text("CARIMBO", (x0, y0 - 0.4), 0.15, f"{q.name} | piso {floor} | {rev} | RASCUNHO - nao assinado")
    if q.unconfirmed():
        d.text("CARIMBO", (x0, y0 - 0.8), 0.15, "ATENCAO: divisoes por confirmar: " + ", ".join(r.id for r in q.unconfirmed()))
    for c in conflicts:
        d.text("CARIMBO", (x0, y0 - 1.2), 0.12, "CONFLITO: " + c)
    return d, conflicts
