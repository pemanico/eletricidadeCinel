"""Escritor DXF minimo (ASCII, formato R12), sem dependencias. Abre em QCAD/LibreCAD/AutoCAD.
Texto sem acentos (R12 ASCII). Pode ser substituido por ezdxf mais tarde."""
import unicodedata

def _ascii(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()

class Dxf:
    def __init__(self, layers: dict[str, int]):
        self.layers = layers
        self.ents: list[str] = []

    @staticmethod
    def _g(code: int, val) -> str:
        return f"{code}\n{val}\n"

    def line(self, layer, a, b):
        g = self._g
        self.ents.append(g(0, "LINE") + g(8, layer) + g(10, a[0]) + g(20, a[1]) + g(30, 0) + g(11, b[0]) + g(21, b[1]) + g(31, 0))

    def polyline(self, layer, pts, closed=True):
        g = self._g
        s = g(0, "POLYLINE") + g(8, layer) + g(66, 1) + g(70, 1 if closed else 0)
        for x, y in pts:
            s += g(0, "VERTEX") + g(8, layer) + g(10, x) + g(20, y) + g(30, 0)
        self.ents.append(s + g(0, "SEQEND") + g(8, layer))

    def circle(self, layer, c, r):
        g = self._g
        self.ents.append(g(0, "CIRCLE") + g(8, layer) + g(10, c[0]) + g(20, c[1]) + g(30, 0) + g(40, r))

    def text(self, layer, pos, height, txt):
        g = self._g
        self.ents.append(g(0, "TEXT") + g(8, layer) + g(10, pos[0]) + g(20, pos[1]) + g(30, 0) + g(40, height) + g(1, _ascii(txt)))

    def dumps(self) -> str:
        g = self._g
        s = g(0, "SECTION") + g(2, "TABLES")
        s += g(0, "TABLE") + g(2, "LTYPE") + g(70, 1)
        s += g(0, "LTYPE") + g(2, "CONTINUOUS") + g(70, 0) + g(3, "Solid line") + g(72, 65) + g(73, 0) + g(40, 0.0) + g(0, "ENDTAB")
        s += g(0, "TABLE") + g(2, "STYLE") + g(70, 1)
        s += g(0, "STYLE") + g(2, "STANDARD") + g(70, 0) + g(40, 0.0) + g(41, 1.0) + g(50, 0.0) + g(71, 0) + g(42, 0.2) + g(3, "txt") + g(4, "") + g(0, "ENDTAB")
        s += g(0, "TABLE") + g(2, "LAYER") + g(70, len(self.layers))
        for name, color in self.layers.items():
            s += g(0, "LAYER") + g(2, name) + g(70, 0) + g(62, color) + g(6, "CONTINUOUS")
        s += g(0, "ENDTAB") + g(0, "ENDSEC")
        s += g(0, "SECTION") + g(2, "ENTITIES") + "".join(self.ents) + g(0, "ENDSEC") + g(0, "EOF")
        return s

    def save(self, path):
        with open(path, "w", encoding="ascii", newline="\n") as f:
            f.write(self.dumps())

def parse_entities(text: str) -> list[tuple[str, str]]:
    """Leitor simples (para testes): devolve [(tipo, layer)] das entidades."""
    lines = text.split("\n")
    pairs = [(lines[i].strip(), lines[i + 1].strip()) for i in range(0, len(lines) - 1, 2)]
    out, in_ent, cur = [], False, None
    for c, v in pairs:
        if c == "2" and v == "ENTITIES": in_ent = True
        if c == "0" and v == "ENDSEC": in_ent = False
        if in_ent and c == "0":
            cur = [v, None]; out.append(cur)
        elif in_ent and c == "8" and cur and cur[1] is None:
            cur[1] = v
    return [(t, l) for t, l in out if t not in ("ENDSEC",)]
