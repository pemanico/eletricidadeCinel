"""Servidor HTTP local (stdlib). Escuta so em 127.0.0.1. python -m eletro.web.server [porta]"""
from __future__ import annotations
import json, sys, re, mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from pydantic import ValidationError
from .service import Servico, Erro
from ..cad.dxfread import DxfError

STATIC = Path(__file__).parent / "static"
MAX_BODY = 20 * 1024 * 1024

def fazer_handler(sv: Servico):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a): pass
        def _send(self, code, body, ctype="application/json; charset=utf-8", extra=None):
            b = body if isinstance(body, bytes) else body.encode("utf-8")
            self.send_response(code); self.send_header("Content-Type", ctype); self.send_header("Content-Length", str(len(b)))
            for k, v in (extra or {}).items(): self.send_header(k, v)
            self.end_headers(); self.wfile.write(b)
        def _json(self, obj, code=200): self._send(code, json.dumps(obj, ensure_ascii=False))
        def _body(self):
            n = int(self.headers.get("Content-Length") or 0)
            if n > MAX_BODY: raise Erro("pedido demasiado grande")
            return self.rfile.read(n).decode("utf-8", errors="replace")
        def _tratar(self, fn):
            try: fn()
            except (Erro, DxfError, ValueError) as e:
                msg = "dados invalidos: " + "; ".join(f"{'.'.join(map(str, x['loc']))}: {x['msg']}" for x in e.errors()[:5]) if isinstance(e, ValidationError) else str(e)
                self._json({"erro": msg}, 400)
            except Exception as e:
                self._json({"erro": f"erro interno: {type(e).__name__}"}, 500)
        def do_GET(self): self._tratar(self._get)
        def do_POST(self): self._tratar(self._post)
        def do_PUT(self): self._tratar(self._post)

        def _get(self):
            u = urlparse(self.path); q = parse_qs(u.query)
            if u.path in ("/", "/index.html"): return self._send(200, (STATIC / "index.html").read_bytes(), "text/html; charset=utf-8")
            if u.path.startswith("/static/"):
                f = (STATIC / u.path[8:]).resolve()
                if STATIC.resolve() not in f.parents or not f.is_file(): return self._json({"erro": "nao encontrado"}, 404)
                return self._send(200, f.read_bytes(), mimetypes.guess_type(f.name)[0] or "application/octet-stream")
            if u.path == "/api/projetos": return self._json(sv.listar())
            m = re.fullmatch(r"/api/p/([^/]+)(?:/(\w+))?", u.path)
            if not m: return self._json({"erro": "nao encontrado"}, 404)
            slug, ac = m.groups()
            if ac is None: return self._json(sv.abrir(slug))
            if ac == "revisoes": return self._json(sv.revisoes(slug))
            if ac == "diff": return self._json(sv.diferencas(slug, int(q["a"][0]), int(q["b"][0])))
            if ac == "revisao": return self._json(sv.restaurar(slug, int(q["n"][0])))
            return self._json({"erro": "nao encontrado"}, 404)

        def _post(self):
            u = urlparse(self.path)
            d = json.loads(self._body() or "{}") if not u.path.endswith("/dxf") else None
            if u.path == "/api/projetos": return self._json(sv.criar(d.get("slug", ""), bool(d.get("exemplo"))))
            m = re.fullmatch(r"/api/p/([^/]+)/(\w+)", u.path)
            if not m: return self._json({"erro": "nao encontrado"}, 404)
            slug, ac = m.groups()
            if ac == "calc": return self._json(sv.calcular(slug, d["project"], d.get("perfil")))
            if ac == "guardar": return self._json(sv.guardar(slug, d["project"], d.get("motivo", ""), d.get("autor", "")))
            if ac == "perfil": sv.guardar_perfil(slug, d["perfil"]); return self._json({"ok": True})
            if ac == "dxf": return self._json(sv.dxf_analisar(slug, self._body()))
            if ac == "importar": return self._json(sv.dxf_importar(slug, d["camada"], float(d["unit_m"])))
            if ac == "export_dxf":
                return self._send(200, sv.exportar_dxf(slug, d["project"], d.get("que", "planta")), "application/dxf",
                                  {"Content-Disposition": f'attachment; filename="{slug}_{d.get("que", "planta")}.dxf"'})
            if ac == "relatorio": return self._send(200, sv.relatorio(slug, d["project"]), "text/html; charset=utf-8")
            return self._json({"erro": "nao encontrado"}, 404)
    return H

def servir(porta=8765, pasta=None):
    srv = ThreadingHTTPServer(("127.0.0.1", porta), fazer_handler(Servico(pasta)))
    print(f"http://127.0.0.1:{porta}"); return srv

if __name__ == "__main__":
    servir(int(sys.argv[1]) if len(sys.argv) > 1 else 8765).serve_forever()
