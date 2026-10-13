"""Logica da aplicacao (sem HTTP): armazenamento por projeto, calculo, revisoes, DXF do arquiteto.
projetos/<slug>/: current.json, rev_<N>.json, base.dxf, perfil.json (opcional)."""
from __future__ import annotations
import json, re, datetime
from pathlib import Path
from ..schema.project import Project, Revision
from ..schema.dynamic import resolve, diff
from ..engine import calcular, pendencias
from ..rules.dotacao import carregar_perfil
from ..rules.ited import carregar as carregar_ited
from ..calc.material import lista_material
from ..cad import dxfread
from ..cad.desenho import planta, unifilar, para_svg, para_dxf, base_do_arquiteto
from .relatorio import relatorio_html

RAIZ = Path(__file__).resolve().parents[3]
PERFIL_DEFAULT = RAIZ / "data/convencoes/convencao_projeto_v1.json"
ITED_DEFAULT = RAIZ / "data/convencoes/ited_dotacao_v1.json"
EXEMPLO = RAIZ / "examples/moradia_t3/projeto.json"
SLUG = re.compile(r"^[a-z0-9][a-z0-9_-]{0,40}$")

class Erro(ValueError):
    pass

class Servico:
    def __init__(self, pasta: Path | None = None):
        self.pasta = Path(pasta) if pasta else RAIZ / "projetos"
        self.pasta.mkdir(parents=True, exist_ok=True)

    def _dir(self, slug: str) -> Path:
        if not SLUG.match(slug or ""): raise Erro("identificador invalido (a-z, 0-9, - _)")
        return self.pasta / slug

    def listar(self):
        out = []
        for d in sorted(self.pasta.iterdir()):
            if (d / "current.json").exists():
                p = json.loads((d / "current.json").read_text(encoding="utf-8"))
                out.append({"slug": d.name, "name": p.get("name"), "revision": p.get("revision")})
        return out

    def criar(self, slug: str, exemplo: bool = False):
        d = self._dir(slug)
        if d.exists(): raise Erro("ja existe")
        d.mkdir(parents=True)
        base = json.loads(EXEMPLO.read_text(encoding="utf-8")) if exemplo else {
            "name": slug, "rooms": [], "revision": 1, "supply": {"phases": 1},
            "revisions": [{"number": 1, "date": str(datetime.date.today()), "author": "", "reason": "versao inicial"}]}
        Project.model_validate(base)
        (d / "current.json").write_text(json.dumps(base, ensure_ascii=False, indent=1), encoding="utf-8")
        (d / "rev_1.json").write_text(json.dumps(base, ensure_ascii=False, indent=1), encoding="utf-8")
        return self.abrir(slug)

    def perfil(self, slug):
        f = self._dir(slug) / "perfil.json"
        return json.loads(f.read_text(encoding="utf-8")) if f.exists() else carregar_perfil(str(PERFIL_DEFAULT))

    def abrir(self, slug):
        d = self._dir(slug)
        if not (d / "current.json").exists(): raise Erro("projeto inexistente")
        return {"slug": slug, "project": json.loads((d / "current.json").read_text(encoding="utf-8")),
                "perfil": self.perfil(slug), "tem_base_dxf": (d / "base.dxf").exists()}

    def guardar_perfil(self, slug, perfil: dict):
        for k in ("dotacao", "circuitos", "condicoes_instalacao", "comprimentos", "quadro"):
            if k not in perfil: raise Erro(f"convencao sem '{k}'")
        (self._dir(slug) / "perfil.json").write_text(json.dumps(perfil, ensure_ascii=False, indent=1), encoding="utf-8")

    def _fundo(self, slug, p: Project):
        f = self._dir(slug) / "base.dxf"
        if p.base and f.exists():
            return base_do_arquiteto(dxfread.ler(f.read_text(encoding="utf-8", errors="replace")), p.base.unit_m)
        return None

    def calcular(self, slug, proj: dict, perfil: dict | None = None):
        p0 = Project.model_validate(proj)
        perfil = perfil or self.perfil(slug)
        res = calcular(p0, perfil, carregar_ited(str(ITED_DEFAULT)))
        p, conflitos = resolve(p0)
        fundo = self._fundo(slug, p0)
        return {"resultado": {**json.loads(res.model_dump_json()), "pendencias": pendencias(res)}, "material": lista_material(res), "conflitos": conflitos,
                "planta_svg": para_svg(planta(p, res), fundo), "unifilar_svg": para_svg(unifilar(res), esp=1.5)}

    def guardar(self, slug, proj: dict, motivo: str, autor: str = ""):
        """Nova revisao: N+1 em rev_N+1.json e current.json. Nunca altera revisoes antigas."""
        d = self._dir(slug)
        p = Project.model_validate(proj)
        n = max(int(f.stem.split("_")[1]) for f in d.glob("rev_*.json")) + 1
        p.revision = n
        p.revisions.append(Revision(number=n, date=str(datetime.date.today()), author=autor, reason=motivo or "sem motivo"))
        txt = p.model_dump_json(indent=1)
        (d / f"rev_{n}.json").write_text(txt, encoding="utf-8")
        (d / "current.json").write_text(txt, encoding="utf-8")
        return {"revision": n}

    def revisoes(self, slug):
        d = self._dir(slug)
        return sorted(int(f.stem.split("_")[1]) for f in d.glob("rev_*.json"))

    def diferencas(self, slug, a: int, b: int):
        d = self._dir(slug)
        try:
            pa, pb = (Project.model_validate(json.loads((d / f"rev_{x}.json").read_text(encoding="utf-8"))) for x in (a, b))
        except FileNotFoundError: raise Erro("revisao inexistente")
        return diff(pa, pb)

    def restaurar(self, slug, n: int):
        d = self._dir(slug); f = d / f"rev_{n}.json"
        if not f.exists(): raise Erro("revisao inexistente")
        return json.loads(f.read_text(encoding="utf-8"))   # devolve para edicao; so passa a revisao nova ao guardar

    # ---- DXF do arquiteto ----
    def dxf_analisar(self, slug, texto: str, unit_m: float | None = None):
        d = dxfread.ler(texto)
        a = dxfread.analisar(d)
        (self._dir(slug) / "base.dxf").write_text(texto, encoding="utf-8")
        return a

    def dxf_importar(self, slug, camada: str, unit_m: float):
        f = self._dir(slug) / "base.dxf"
        if not f.exists(): raise Erro("carregar primeiro o DXF")
        if not (unit_m > 0): raise Erro("unidade invalida")
        r = dxfread.extrair_divisoes(dxfread.ler(f.read_text(encoding="utf-8", errors="replace")), camada, unit_m)
        return {**r, "base": {"file": "base.dxf", "unit_m": unit_m}}

    def exportar_dxf(self, slug, proj: dict, que: str = "planta"):
        p0 = Project.model_validate(proj)
        res = calcular(p0, self.perfil(slug), carregar_ited(str(ITED_DEFAULT)))
        p, _ = resolve(p0)
        u = p0.base.unit_m if p0.base else 1.0
        if que == "unifilar":
            return para_dxf(unifilar(res), 0.001).dumps()
        prim = planta(p, res, incluir_divisoes=not p0.base)
        fundo = self._fundo(slug, p0) or []
        return para_dxf(fundo + prim, u).dumps()

    def relatorio(self, slug, proj: dict):
        p0 = Project.model_validate(proj)
        res = calcular(p0, self.perfil(slug), carregar_ited(str(ITED_DEFAULT)))
        p, _ = resolve(p0)
        return relatorio_html(p, res)
