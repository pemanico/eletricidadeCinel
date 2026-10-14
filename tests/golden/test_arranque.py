"""Arranque: run_tests.py/run_app.py avisam em portugues se faltar o venv/dependencias (em vez de traceback).
Garante que a lista verificada acompanha o requirements.txt."""
import re
from pathlib import Path

RAIZ = Path(__file__).parents[2]
MODULO = {"pydantic": "pydantic", "pikepdf": "pikepdf", "pdfplumber": "pdfplumber", "pypdfium2": "pypdfium2", "numpy": "numpy", "scipy": "scipy"}

def test_deps_check_cobre_o_requirements():
    req = [re.split(r"[<>=\[ ]", l.strip())[0].lower() for l in (RAIZ / "requirements.txt").read_text(encoding="utf-8").splitlines()
           if l.strip() and not l.startswith("#")]
    chk = (RAIZ / "deps_check.py").read_text(encoding="utf-8")
    for pkg in req:
        assert f'"{MODULO.get(pkg, pkg)}"' in chk, pkg

def test_runners_verificam_dependencias_antes_de_importar():
    for f in ("run_tests.py", "run_app.py"):
        linhas = [l for l in (RAIZ / f).read_text(encoding="utf-8").splitlines() if l.startswith(("import", "from"))]
        assert linhas[0].startswith("import deps_check"), f
