"""CLI usada por humanos e por agentes. python -m eletro.cli <cmd>"""
import argparse, sys
from .schema.project import load
from .schema.dynamic import resolve, diff
from .cad.planta import desenhar

def main(argv=None):
    ap = argparse.ArgumentParser(prog="eletro")
    sp = ap.add_subparsers(dest="cmd", required=True)
    v = sp.add_parser("validate"); v.add_argument("projeto")
    d = sp.add_parser("draw"); d.add_argument("projeto"); d.add_argument("-o", "--out", required=True); d.add_argument("--piso", type=int, default=0)
    f = sp.add_parser("diff"); f.add_argument("antes"); f.add_argument("depois")
    a = ap.parse_args(argv)
    if a.cmd == "validate":
        p = load(a.projeto)
        print(f"OK: {len(p.rooms)} divisoes, {p.total_area():.1f} m2, revisao {p.revision}")
        un = p.unconfirmed()
        if un: print("Por confirmar:", ", ".join(r.id for r in un))
        _, c = resolve(p)
        for x in c: print("CONFLITO:", x)
        return 1 if c else 0
    if a.cmd == "draw":
        dx, c = desenhar(load(a.projeto), a.piso)
        dx.save(a.out); print(f"DXF escrito em {a.out}")
        for x in c: print("CONFLITO:", x)
        return 1 if c else 0
    if a.cmd == "diff":
        ch = diff(load(a.antes), load(a.depois))
        print("\n".join(ch) if ch else "Sem alteracoes")
    return 0

if __name__ == "__main__":
    sys.exit(main())
