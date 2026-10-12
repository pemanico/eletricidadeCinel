"""Runner sem dependencias (pytest nao disponivel em todos os ambientes). Uso: python run_tests.py"""
import sys, glob, importlib.util, os
sys.path.insert(0, "src"); sys.path.insert(0, "tests/golden")
fails = 0
for f in sorted(glob.glob("tests/golden/test_*.py")):
    spec = importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    for n in sorted(dir(m)):
        if n.startswith("test_"):
            try: getattr(m, n)(); print("OK  ", f.split("/")[-1], n)
            except Exception as e: fails += 1; print("FALHA", f.split("/")[-1], n, "->", repr(e))
sys.exit(1 if fails else 0)
