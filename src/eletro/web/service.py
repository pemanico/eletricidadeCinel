"""Logica da aplicacao (sem HTTP): armazenamento por projeto, calculo, revisoes, DXF do arquiteto.
projetos/<slug>/: current.json, rev_<N>.json, base.dxf, base.pdf (opcional), perfil.json (opcional)."""
from __future__ import annotations
import json, re, datetime
from pathlib import Path
from ..schema.project import Project, Revision, Panel
from ..schema.dynamic import resolve, diff
from ..engine import calcular, pendencias
from ..rules.dotacao import carregar_perfil
from ..rules.ited import carregar as carregar_ited
from ..rules import alturas
from ..cad import colocar
from ..calc.material import lista_material
from ..cad import dxfread
from ..cad.dxf import Dxf
from ..cad.desenho import planta, unifilar, para_svg, para_dxf, base_do_arquiteto
from .relatorio import relatorio_html

RAIZ = Path(__file__).resolve().parents[3]
PERFIL_DEFAULT = RAIZ / "data/convencoes/convencao_projeto_v1.json"
ITED_DEFAULT = RAIZ / "data/convencoes/ited_dotacao_v1.json"
EXEMPLO = RAIZ / "examples/moradia_t3/projeto.json"
SIMBOLOS_DEFAULT = alturas.CATALOGO_DEFAULT
SLUG = re.compile(r"^[a-z0-9][a-z0-9_-]{0,40}$")

class Erro(ValueError):
    pass

class Servico:
    def __init__(self, pasta: Path | None = None, simbolos: Path | None = None):
        self.pasta = Path(pasta) if pasta else RAIZ / "projetos"
        self.simbolos_path = Path(simbolos) if simbolos else SIMBOLOS_DEFAULT   # tabela de alturas (partilhada por todos os projetos)
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
        txt = Project.model_validate(base).model_dump_json(indent=1)   # modelo completo: todas as listas presentes
        (d / "current.json").write_text(txt, encoding="utf-8")
        (d / "rev_1.json").write_text(txt, encoding="utf-8")
        return self.abrir(slug)

    def perfil(self, slug):
        f = self._dir(slug) / "perfil.json"
        return json.loads(f.read_text(encoding="utf-8")) if f.exists() else carregar_perfil(str(PERFIL_DEFAULT))

    def abrir(self, slug):
        d = self._dir(slug)
        if not (d / "current.json").exists(): raise Erro("projeto inexistente")
        return {"slug": slug, "project": json.loads((d / "current.json").read_text(encoding="utf-8")),
                "perfil": self.perfil(slug), "tem_base_dxf": (d / "base.dxf").exists(), "tem_base_pdf": (d / "base.pdf").exists()}

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
        if not p0.rooms:
            raise Erro("projeto sem divisoes: importar a planta (DXF/PDF do arquiteto) ou acrescentar divisoes")
        perfil = perfil or self.perfil(slug)
        cat = self.simbolos()
        res = calcular(p0, perfil, carregar_ited(str(ITED_DEFAULT)), cat)
        p, conflitos = resolve(p0)
        fundo = self._fundo(slug, p0)
        return {"resultado": {**json.loads(res.model_dump_json()), "pendencias": pendencias(res)},
                "material": lista_material(res, pontos=p0.points, catalogo=cat), "conflitos": conflitos,
                "planta_svg": para_svg(planta(p, res, catalogo=cat), fundo), "unifilar_svg": para_svg(unifilar(res), esp=1.5)}

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

    # ---- Aparelhagem na planta: simbolos, alturas, preenchimento ----
    def simbolos(self):
        return alturas.carregar(str(self.simbolos_path))

    def simbolos_alterar(self, alteracoes: list, autor: str = ""):
        """Grava a tabela de alturas (nova versao + historico). O ficheiro esta no repositorio: fazer commit para o guardar."""
        if not isinstance(alteracoes, list) or not alteracoes: raise Erro("sem alteracoes")
        try:
            novo, entradas = alturas.alterar(self.simbolos(), alteracoes, autor, str(datetime.date.today()))
        except ValueError as e:
            raise Erro(str(e))
        alturas.guardar(novo, str(self.simbolos_path))
        return {"tabela": novo, "alteracoes": entradas}

    def reaplicar(self, slug, proj: dict, piso: int | None = None):
        """Atualiza para a tabela atual as alturas dos pontos com origem CONVENCAO (os MANUAL nao mudam).
        Devolve a lista completa de pontos e quantos mudaram; o cliente guarda a revisao."""
        cat = self.simbolos()
        p0 = Project.model_validate(proj)
        rooms = {r.id: r for r in p0.rooms}
        n = 0
        for q in p0.points:
            r = rooms[q.room_id]
            if q.height_origem != "CONVENCAO" or (piso is not None and r.floor != piso) or q.kind not in cat["simbolos"]:
                continue
            h = alturas.altura_por_defeito(q.kind, r.use, cat, None)
            if h != q.height_m: n += 1
            q.height_m, q.height_ver = h, cat["versao"]
        return {"points": [json.loads(q.model_dump_json()) for q in p0.points], "alterados": n, "versao": cat["versao"]}

    def fundo_piso(self, slug, piso: int):
        """Paredes do arquiteto (metros) para o editor: base_p<piso>.dxf (PDF importado) ou base.dxf."""
        d = self._dir(slug)
        f = d / f"base_p{piso}.dxf"
        unit = 1.0
        if not f.exists():
            f = d / "base.dxf"
            p = json.loads((d / "current.json").read_text(encoding="utf-8")) if (d / "current.json").exists() else {}
            unit = (p.get("base") or {}).get("unit_m", 1.0)
        if not f.exists():
            return {"segmentos": []}
        segs = []
        for e in base_do_arquiteto(dxfread.ler(f.read_text(encoding="utf-8", errors="replace")), unit):
            if e["t"] == "line": segs.append([list(e["a"]), list(e["b"])])
            elif e["t"] == "poly":
                pts = e["pts"] + ([e["pts"][0]] if e["closed"] else [])
                segs += [[list(a), list(b)] for a, b in zip(pts, pts[1:])]
        return {"segmentos": segs}

    def preencher(self, slug, proj: dict, piso: int, so_vazias: bool = True):
        """Gera aparelhagem pela convencao (contagens) nas divisoes do piso, com alturas do catalogo.
        so_vazias=True: so divisoes sem pontos; False: substitui os pontos das divisoes do piso.
        Devolve a lista COMPLETA de pontos do projeto (o cliente substitui e guarda quando quiser)."""
        cat = self.simbolos(); pr = cat["preenchimento"]
        p0 = Project.model_validate(proj)
        alvo = [r for r in p0.rooms if r.floor == piso and r.polygon
                and (not so_vazias or not any(q.room_id == r.id for q in p0.points))]
        ids_alvo = {r.id for r in alvo}
        manter = [q for q in p0.points if q.room_id not in ids_alvo]
        tmp = p0.model_copy(deep=True); tmp.points = manter
        if tmp.panel is None and tmp.rooms:
            tmp.panel = Panel(room_id=tmp.rooms[0].id, pos=tuple(tmp.rooms[0].polygon[0]) if tmp.rooms[0].polygon else (0.0, 0.0))
        res = calcular(tmp, self.perfil(slug), carregar_ited(str(ITED_DEFAULT)), cat)
        usados = {q.id for q in manter}
        def novo_id():
            i = 1
            while f"q{i}" in usados: i += 1
            usados.add(f"q{i}"); return f"q{i}"
        novos = []
        def add(kind, r, xy):
            novos.append({"id": novo_id(), "kind": kind, "room_id": r.id, "pos": [round(xy[0], 3), round(xy[1], 3)],
                          "height_m": alturas.altura_por_defeito(kind, r.use, cat, None), "height_origem": "CONVENCAO",
                          "height_ver": cat["versao"]})
        for r in alvo:
            poly = [tuple(v) for v in r.polygon]
            n = res.pontos[r.id]; it = res.ited.get(r.id, {"rj45": 0, "tv": 0})
            portas = [tuple(o.pos) for o in p0.openings if o.room_id == r.id and o.kind == "porta"]
            n_banc = int(n["tomadas"] * pr["cozinha_bancada_fracao"] + 0.5) if r.use == "cozinha" else 0
            for xy in colocar.luzes(poly, n["luz"]): add(pr["luz"], r, xy)
            for xy in colocar.junto_porta(poly, portas, n["interruptores"]): add(pr["interruptor"], r, xy)
            for i, xy in enumerate(colocar.no_perimetro(poly, n["tomadas"], 0.15, portas)):
                add("tomada_bancada" if i < n_banc else pr["tomada"], r, xy)
            ext = colocar.no_perimetro(poly, it["rj45"] + it["tv"], 0.35, portas)
            for xy in ext[:it["rj45"]]: add(pr["ited"]["rj45"], r, xy)
            for xy in ext[it["rj45"]:]: add(pr["ited"]["tv"], r, xy)
            c = colocar.centroide(poly)
            for k, e in enumerate(x for x in p0.equipment if x.room_id == r.id):
                add(pr["equipamento"].get(e.kind, "caixa_ligacao"), r, colocar.para_dentro((c[0] + 0.35 * (k + 1), c[1] - 0.35), poly))
        return {"points": [json.loads(q.model_dump_json()) for q in manter] + novos, "gerados": len(novos),
                "divisoes": len(alvo)}

    # ---- PDF do arquiteto (vetorial, com camadas) ----
    def pdf_analisar(self, slug, dados: bytes):
        from ..cad import pdfread
        a = pdfread.analisar(dados)
        (self._dir(slug) / "base.pdf").write_bytes(dados)
        return a

    def _pdf_detetar(self, slug, pagina, camadas_paredes, camadas_vaos, escala, piso):
        from ..cad import pdfread, divisoes
        f = self._dir(slug) / "base.pdf"
        if not f.exists(): raise Erro("carregar primeiro o PDF")
        if not camadas_paredes: raise Erro("escolher a camada das paredes")
        e = pdfread.extrair(f.read_bytes(), int(pagina), list(camadas_paredes), float(escala), list(camadas_vaos or []))
        piso = int(piso if piso is not None else (e["piso"] if e["piso"] is not None else 0))
        r = divisoes.detetar(e["segmentos"], e["palavras"], e["quadro_areas"], piso, float(escala), aux=e["aux"])
        return e, r, piso

    def pdf_detetar(self, slug, pagina, camadas_paredes, camadas_vaos, escala, piso=None):
        """So pre-visualiza: nao altera o projeto."""
        from ..cad import divisoes
        e, r, piso = self._pdf_detetar(slug, pagina, camadas_paredes, camadas_vaos, escala, piso)
        vaos = divisoes.filtrar_vaos(e["segmentos"], e["aux"])
        return {**r, "piso": piso, "pagina": int(pagina), "designacao": e["designacao"], "quadro_areas": e["quadro_areas"],
                "svg": divisoes.svg_previsao(e["segmentos"], r, vaos)}

    def pdf_importar(self, slug, pagina, camadas_paredes, camadas_vaos, escala, piso=None):
        """Devolve as divisoes do piso (confirmed=False) e grava as paredes como base.dxf (metros) para o fundo da planta
        e para a exportacao DXF. O cliente substitui SO as divisoes desse piso."""
        from ..cad import divisoes
        e, r, piso = self._pdf_detetar(slug, pagina, camadas_paredes, camadas_vaos, escala, piso)
        if not r["divisoes"]: raise Erro("nenhuma divisao fechada detetada: nada para importar (ver avisos)")
        d = Dxf({"ARQ-PAREDES": 8, "ARQ-VAOS": 9})
        for a, b in e["segmentos"]: d.line("ARQ-PAREDES", a, b)
        for a, b in divisoes.filtrar_vaos(e["segmentos"], e["aux"]): d.line("ARQ-VAOS", a, b)
        (self._dir(slug) / "base.dxf").write_text(d.dumps(), encoding="utf-8")
        (self._dir(slug) / f"base_p{piso}.dxf").write_text(d.dumps(), encoding="utf-8")   # paredes por piso (editor)
        return {"divisoes": r["divisoes"], "aberturas": r["aberturas"], "avisos": r["avisos"], "piso": piso,
                "base": {"file": "base.dxf", "unit_m": 1.0}}

    def exportar_dxf(self, slug, proj: dict, que: str = "planta"):
        p0 = Project.model_validate(proj)
        cat = self.simbolos()
        res = calcular(p0, self.perfil(slug), carregar_ited(str(ITED_DEFAULT)), cat)
        p, _ = resolve(p0)
        u = p0.base.unit_m if p0.base else 1.0
        if que == "unifilar":
            return para_dxf(unifilar(res), 0.001).dumps()
        prim = planta(p, res, incluir_divisoes=not p0.base, catalogo=cat)
        fundo = self._fundo(slug, p0) or []
        return para_dxf(fundo + prim, u).dumps()

    def relatorio(self, slug, proj: dict):
        p0 = Project.model_validate(proj)
        cat = self.simbolos()
        res = calcular(p0, self.perfil(slug), carregar_ited(str(ITED_DEFAULT)), cat)
        p, _ = resolve(p0)
        return relatorio_html(p, res, cat)
