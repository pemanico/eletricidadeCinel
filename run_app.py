"""Arranca a app web local (funciona em Windows/macOS/Linux sem configurar PYTHONPATH).
Uso: python run_app.py [porta]   ->  http://127.0.0.1:8765"""
import deps_check  # noqa: F401  (mensagem clara se faltar o venv/dependencias)
import sys, webbrowser, threading
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))
from eletro.web.server import servir

if __name__ == "__main__":
    porta = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    srv = servir(porta)
    threading.Timer(0.8, lambda: webbrowser.open(f"http://127.0.0.1:{porta}")).start()
    try: srv.serve_forever()
    except KeyboardInterrupt: print("\nterminado")
