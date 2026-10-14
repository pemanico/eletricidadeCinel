"""Uso: import deps_check (no inicio de run_tests.py e run_app.py)."""
# Verificacao de dependencias ANTES de importar o projeto: mensagem clara em vez de traceback.
import importlib.util as _iu, sys as _sys
_falta = [m for m in ("pydantic", "pikepdf", "pdfplumber", "pypdfium2", "numpy", "scipy") if _iu.find_spec(m) is None]
if _falta:
    print("Faltam dependencias: " + ", ".join(_falta))
    print("Ative o ambiente virtual e instale:  .\\.venv\\Scripts\\Activate.ps1   (Windows)  |  source .venv/bin/activate   (Linux/macOS)")
    print("                                     pip install -r requirements.txt")
    print("Python em uso: " + _sys.executable)
    raise SystemExit(2)
