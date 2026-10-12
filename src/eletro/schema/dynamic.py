"""Dinamismo: overrides com deteção de conflito, e diff entre revisões."""
from __future__ import annotations
from .project import Project

def _get(p: Project, target: str, field: str):
    if target == "panel":
        return getattr(p.panel, field, None) if p.panel else None
    if target.startswith("room:"):
        rid = target[5:]
        r = next((r for r in p.rooms if r.id == rid), None)
        return getattr(r, field, None) if r else None
    return None

def _set(p: Project, target: str, field: str, value):
    if target == "panel" and p.panel:
        setattr(p.panel, field, tuple(value) if field == "pos" else value)
    elif target.startswith("room:"):
        r = next(r for r in p.rooms if r.id == target[5:])
        setattr(r, field, value)

def resolve(p: Project) -> tuple[Project, list[str]]:
    """Aplica overrides sobre uma COPIA. Se o valor-base do modelo mudou desde que o ajuste foi
    feito, NAO aplica e devolve conflito (o humano decide)."""
    q = p.model_copy(deep=True)
    conflicts: list[str] = []
    for o in p.overrides:
        cur = _get(q, o.target, o.field)
        if cur is None:
            conflicts.append(f"{o.target}.{o.field}: alvo inexistente (override orfao)")
            continue
        base = tuple(o.base) if isinstance(o.base, list) else o.base
        cur_cmp = tuple(cur) if isinstance(cur, list) else cur
        if o.base is not None and cur_cmp != base:
            conflicts.append(f"{o.target}.{o.field}: modelo mudou ({base} -> {cur_cmp}); override {o.value} NAO aplicado")
            continue
        _set(q, o.target, o.field, o.value)
    return q, conflicts

def diff(a: Project, b: Project) -> list[str]:
    """Alterações entre duas revisões (a -> b)."""
    out: list[str] = []
    def by_id(items): return {i.id: i for i in items}
    for label, la, lb in (("divisao", a.rooms, b.rooms), ("abertura", a.openings, b.openings),
                          ("equipamento", a.equipment, b.equipment)):
        da, db = by_id(la), by_id(lb)
        for k in db.keys() - da.keys(): out.append(f"+ {label} {k}")
        for k in da.keys() - db.keys(): out.append(f"- {label} {k}")
        for k in da.keys() & db.keys():
            xa, xb = da[k].model_dump(), db[k].model_dump()
            for f in xa:
                if xa[f] != xb[f]:
                    out.append(f"~ {label} {k}.{f}: {xa[f]} -> {xb[f]}")
    if a.supply != b.supply:
        out.append(f"~ alimentacao: {a.supply.model_dump()} -> {b.supply.model_dump()}")
    if a.panel != b.panel:
        out.append(f"~ quadro: {a.panel} -> {b.panel}")
    return out
