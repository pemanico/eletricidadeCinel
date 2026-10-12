"""Gera um DXF ASCII sintetico ao estilo de um arquiteto (mm, R2000-like) para testes. NAO e um ficheiro real."""
def _g(c, v): return f"{c}\n{v}\n"

def lwpoly(layer, pts, fechada=True):
    s = _g(0, "LWPOLYLINE") + _g(5, "A1") + _g(100, "AcDbEntity") + _g(8, layer) + _g(100, "AcDbPolyline") + _g(90, len(pts)) + _g(70, 1 if fechada else 0)
    for x, y in pts: s += _g(10, x) + _g(20, y)
    return s

def arquiteto_dxf(unid=4, com_envolvente=True, com_textos=True):
    # mesma planta de examples/moradia_t3, em mm
    rooms = {"SALA": [(0, 0), (6000, 0), (6000, 4000), (0, 4000)],
             "COZINHA": [(6000, 0), (9500, 0), (9500, 3000), (6000, 3000)],
             "QUARTO 1": [(0, 4000), (4000, 4000), (4000, 7500), (0, 7500)],
             "QUARTO 2": [(4000, 4000), (7000, 4000), (7000, 7500), (4000, 7500)],
             "I.S.": [(7000, 4000), (9500, 4000), (9500, 6000), (7000, 6000)]}
    h = _g(0, "SECTION") + _g(2, "HEADER") + _g(9, "$ACADVER") + _g(1, "AC1015") + _g(9, "$INSUNITS") + _g(70, unid) + _g(0, "ENDSEC")
    b = _g(0, "SECTION") + _g(2, "BLOCKS") + _g(0, "BLOCK") + _g(8, "0") + _g(2, "PORTA_90") + _g(0, "LINE") + _g(8, "0") + _g(10, 0) + _g(20, 0) + _g(11, 900) + _g(21, 0) + _g(0, "ENDBLK") + _g(0, "ENDSEC")
    e = _g(0, "SECTION") + _g(2, "ENTITIES")
    for nome, pts in rooms.items():
        e += lwpoly("AREAS", pts)
        if com_textos:
            cx = sum(p[0] for p in pts) / 4; cy = sum(p[1] for p in pts) / 4
            e += _g(0, "TEXT") + _g(8, "TEXTOS") + _g(10, cx) + _g(20, cy) + _g(40, 200) + _g(1, nome)
            e += _g(0, "MTEXT") + _g(8, "TEXTOS") + _g(10, cx) + _g(20, cy - 400) + _g(40, 150) + _g(1, "{\\fArial;12.5 m2}")
    if com_envolvente:
        e += lwpoly("AREAS", [(0, 0), (9500, 0), (9500, 7500), (0, 7500)])
    for (x1, y1, x2, y2) in [(0, 0, 9500, 0), (9500, 0, 9500, 7500), (9500, 7500, 0, 7500), (0, 7500, 0, 0)]:
        e += _g(0, "LINE") + _g(8, "PAREDES") + _g(10, x1) + _g(20, y1) + _g(11, x2) + _g(21, y2)
    e += _g(0, "INSERT") + _g(8, "PORTAS") + _g(2, "PORTA_90") + _g(10, 2550) + _g(20, 0) + _g(41, 1) + _g(42, 1) + _g(50, 0)
    e += _g(0, "INSERT") + _g(8, "JANELAS") + _g(2, "JANELA_120") + _g(10, 900) + _g(20, 4000) + _g(41, 1) + _g(42, 1) + _g(50, 0)
    e += _g(0, "INSERT") + _g(8, "MOBILIARIO") + _g(2, "SOFA") + _g(10, 2000) + _g(20, 2000)
    e += _g(0, "ENDSEC") + _g(0, "EOF")
    return h + b + e
