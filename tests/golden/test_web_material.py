import json, tempfile, threading, urllib.request, urllib.error
from arq_dxf import arquiteto_dxf
from eletro.web.service import Servico, Erro
from eletro.web.server import servir
from eletro.schema.project import load
from eletro.engine import calcular
from eletro.rules.dotacao import carregar_perfil
from eletro.rules.ited import carregar
from eletro.calc.material import lista_material
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
def _res():
    p = load(str(RAIZ / "examples/moradia_t3/projeto.json"))
    return calcular(p, carregar_perfil(str(RAIZ / "data/convencoes/convencao_projeto_v1.json")), carregar(str(RAIZ / "data/convencoes/ited_dotacao_v1.json")))

def test_material_cabos_e_aparelhagem_batem_com_circuitos():
    r = _res(); m = lista_material(r)
    cab = {x["descricao"].split("3G")[1].split()[0]: x["qtd"] for x in m if x["categoria"] == "Cabos"}
    assert cab == {"1.5": 38.2, "2.5": 60.1, "4": 19.7}                      # (34.74, 54.66, 17.94) m x 1.10
    q = {x["descricao"]: x["qtd"] for x in m}
    assert q["Disjuntor C16 1P+N"] == 4 and q["Disjuntor B10 1P+N"] == 1 and q["Disjuntor C20 1P+N"] == 1
    assert q["Tomada 2P+T 16 A"] == 21 and q["Tomada RJ45"] == 6 and q["Tomada TV"] == 4

def test_servico_revisoes_nunca_alteram_as_antigas():
    s = Servico(tempfile.mkdtemp()); a = s.criar("t3", True)
    pr = a["project"]; pr["equipment"][0]["power_w"] = 3000
    assert s.guardar("t3", pr, "menos potencia", "x") == {"revision": 2}
    assert s.revisoes("t3") == [1, 2]
    assert s.diferencas("t3", 1, 2) == ["~ equipamento e1.power_w: 4600.0 -> 3000.0"]
    assert s.restaurar("t3", 1)["equipment"][0]["power_w"] == 4600

def test_slug_invalido_rejeitado():
    s = Servico(tempfile.mkdtemp())
    for x in ("../x", "A b", "", "x/y"):
        try: s.criar(x); assert False, x
        except Erro: pass

def test_dxf_do_arquiteto_ate_ao_dxf_exportado():
    s = Servico(tempfile.mkdtemp()); a = s.criar("t3", True)
    assert s.dxf_analisar("t3", arquiteto_dxf())["sugestao_camada_divisoes"] == "AREAS"
    im = s.dxf_importar("t3", "AREAS", 0.001)
    pr = dict(a["project"]); pr.update(rooms=im["divisoes"], openings=im["aberturas"], base=im["base"], equipment=[])
    c = s.calcular("t3", pr)
    assert c["resultado"]["quadro"] and any(v["ref"] == "dados" for v in c["resultado"]["verificacoes"])   # divisoes importadas por confirmar
    dxf = s.exportar_dxf("t3", pr)
    assert "ARQ-AREAS" in dxf and "ENDSEC" in dxf
    assert "<h1>" in s.relatorio("t3", pr) and "RASCUNHO" in s.relatorio("t3", pr)

def test_http_smoke_e_erros():
    srv = servir(0, tempfile.mkdtemp()); porta = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    def req(path, body=None):
        r = urllib.request.Request(f"http://127.0.0.1:{porta}{path}", data=None if body is None else json.dumps(body).encode())
        try:
            with urllib.request.urlopen(r) as f: return f.status, f.read().decode()
        except urllib.error.HTTPError as e: return e.code, e.read().decode()
    assert req("/")[0] == 200
    assert req("/api/projetos", {"slug": "t3", "exemplo": True})[0] == 200
    c, t = req("/api/p/t3/calc", {"project": json.loads(req("/api/p/t3")[1])["project"]})
    assert c == 200 and json.loads(t)["resultado"]["quadro"]["geral_in_a"] == 45
    assert req("/api/projetos", {"slug": "../etc"})[0] == 400
    assert req("/static/../server.py")[0] in (404, 400)
    assert req("/api/p/t3/calc", {"project": {"name": "x", "rooms": [{"id": "a"}]}})[0] == 400
    srv.shutdown()

def test_pendencias_bloqueiam_enquanto_ha_por_confirmar():
    from eletro.engine import pendencias, relatorio_texto
    r = _res(); pd = pendencias(r)
    assert pd["bloqueado"] and pd["POR_CONFIRMAR"] > 0                       # tabelas da edicao 2000
    assert "NAO UTILIZAVEL" in relatorio_texto(r)
    from eletro.web.relatorio import relatorio_html
    p = load(str(RAIZ / "examples/moradia_t3/projeto.json"))
    assert "NÃO UTILIZÁVEL COMO PROJETO" in relatorio_html(p, r)
