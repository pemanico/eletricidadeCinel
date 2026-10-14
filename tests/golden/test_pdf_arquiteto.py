"""Golden tests: PDF vetorial do arquiteto -> divisoes + validacao.
Sinteticos (arq_pdf.py): medidas verificadas a mao (Sala 4.00x3.00 = 12.00 m2; Quarto 1 3.00x3.00 = 9.00 m2).
Real (fixtures/planta_real_piso0.json): extrato anonimizado da planta do Ordep; serve de REGRESSAO (o resultado
foi conferido contra o quadro de areas uteis do arquiteto, nao e verdade absoluta)."""
import json, tempfile
from pathlib import Path
import arq_pdf
from eletro.cad import pdfread, divisoes
from eletro.web.service import Servico
from eletro.schema.project import Project

FIX = Path(__file__).parent / "fixtures" / "planta_real_piso0.json"

def _detetar(dados, escala=50, vaos=("VISTA",)):
    e = pdfread.extrair(dados, 1, ["PAREDES"], escala, list(vaos))
    return divisoes.detetar(e["segmentos"], e["palavras"], e["quadro_areas"], e["piso"], escala, aux=e["aux"])

def _linha(r, nome):
    return next(v for v in r["validacao"] if v["nome"] == nome)

def test_pdf_analisar_paginas_camadas_escala_piso():
    a = pdfread.analisar(arq_pdf.pdf())
    p = a["paginas"][0]
    assert a["avisos"] == [] and a["sugestao_pagina"] == 1
    assert p["designacao"] == "PLANTA DO PISO 0" and p["escala"] == 50 and p["piso"] == 0
    assert set(p["camadas"]) == {"PAREDES", "VISTA"}
    assert p["sugestao_camada_paredes"] == "PAREDES" and p["sugestao_camada_vaos"] == "VISTA" and p["n_areas_quadro"] == 2

def test_pdf_quadro_de_areas():
    e = pdfread.extrair(arq_pdf.pdf(), 1, ["PAREDES"], 50)
    assert e["quadro_areas"] == {"Sala": 12.0, "Quarto 1": 9.0}

def test_pdf_divisoes_batem_com_medidas_a_mao():
    r = _detetar(arq_pdf.pdf())
    assert r["resumo"]["divisoes"] == 2 and r["resumo"]["erros"] == 0
    for nome, area in (("Sala", 12.0), ("Quarto 1", 9.0)):
        v = _linha(r, nome)
        assert v["estado"] == "ok" and abs(v["area_calc"] - area) <= 0.02 * area, v
        assert abs(v["area_poligono"] - area) <= 0.02 * area, v      # o poligono gravado no projeto tambem bate
    assert r["escala"]["validada"]
    assert all(d["confirmed"] is False and d["source"] == "pdf" and d["floor"] == 0 for d in r["divisoes"])

def test_pdf_frente_de_roupeiro_e_loica_nao_roubam_area():
    v = divisoes.filtrar_vaos(*[pdfread.extrair(arq_pdf.pdf(), 1, ["PAREDES"], 50, ["VISTA"])[k] for k in ("segmentos", "aux")])
    ys = sorted({round(a[1], 2) for a, b in v if abs(a[1] - b[1]) < 1e-6})
    assert 2.7 not in ys            # frente de roupeiro (a 0.60 m da parede) excluida
    assert 0.1 in ys and 0.2 in ys  # caixilho da janela (dentro da parede) incluido

def test_pdf_portas_e_janelas_detetadas():
    ab = _detetar(arq_pdf.pdf())["aberturas"]
    larg = sorted((a["kind"], a["width_m"]) for a in ab)
    assert ("porta", 0.9) in larg and ("janela", 1.2) in larg

def test_pdf_escala_errada_da_erro_e_sugere_a_certa():
    for errada in (100, 25):                         # desenho a 1:50 lido a 1:100 (areas x4) ou a 1:25 (areas /4)
        r = _detetar(arq_pdf.pdf(), escala=errada)
        assert not r["escala"]["validada"] and r["escala"]["escala_sugerida"] == 50, (errada, r["escala"])
        assert any(a["nivel"] == "erro" and "escala" in a["msg"] for a in r["avisos"])

def test_pdf_area_diferente_do_quadro_da_erro():
    r = _detetar(arq_pdf.pdf(quadro=(("Sala", "15.00"), ("Quarto 1", "9.00"))))
    v = _linha(r, "Sala")
    assert v["estado"] == "erro" and v["dif_pct"] == -20.0
    assert any("Sala" in a["msg"] and a["nivel"] == "erro" for a in r["avisos"])

def test_pdf_sem_parede_interior_funde_e_avisa():
    r = _detetar(arq_pdf.pdf(com_interior=False))
    assert _linha(r, "Sala")["estado"] == "fundida"
    assert any("mesma divisao" in a["msg"] and "21.00" in a["msg"] for a in r["avisos"])   # soma do quadro = 12+9

def test_pdf_sem_camadas_avisa():
    a = pdfread.analisar(arq_pdf.pdf(com_camadas=False))
    assert any("sem camadas" in x for x in a["avisos"])

def test_pdf_nao_pdf_recusado():
    try:
        pdfread.analisar(b"isto nao e um pdf"); assert False
    except pdfread.PdfError as e:
        assert "nao e um PDF" in str(e)

def test_pdf_planta_real_regressao():
    fx = json.loads(FIX.read_text(encoding="utf-8"))
    t = lambda ss: [tuple(map(tuple, s)) for s in ss]
    r = divisoes.detetar(t(fx["segmentos"]), fx["palavras"], fx["quadro_areas"], 0, 100, aux=t(fx["aux"]))
    est = {v["nome"]: v for v in r["validacao"]}
    assert r["escala"]["validada"]
    for nome in ("Garagem", "Escritório", "Lavandaria", "Quarto 1", "Quarto 2", "IS.1"):
        assert est[nome]["estado"] == "ok", (nome, est[nome])
    assert abs(est["Garagem"]["dif_pct"]) < 1
    # o espaco aberto e marcado como fundido (nao inventa paredes); alpendres = nao fechados; nada passa calado
    assert all(est[n]["estado"] == "fundida" for n in ("Hall 1", "Sala de estar/jantar", "Cozinha"))
    assert est["Alpendre 1"]["estado"] == "nao_fechado"
    assert r["resumo"]["erros"] >= 4

def test_servico_pdf_importar_so_substitui_o_piso():
    with tempfile.TemporaryDirectory() as tmp:
        sv = Servico(tmp)
        sv.criar("casa")
        a = sv.pdf_analisar("casa", arq_pdf.pdf())
        assert a["sugestao_pagina"] == 1 and (Path(tmp) / "casa" / "base.pdf").exists()
        det = sv.pdf_detetar("casa", 1, ["PAREDES"], ["VISTA"], 50)
        assert det["resumo"]["divisoes"] == 2 and det["svg"].startswith("<svg")
        cave = {"id": "cave1", "name": "Arrumos", "use": "arrumos", "floor": -1, "polygon": [[0, 0], [5, 0], [5, 4], [0, 4]]}
        x = sv.pdf_importar("casa", 1, ["PAREDES"], ["VISTA"], 50)
        # o cliente faz: divisoes de outros pisos + novas
        d0 = x["divisoes"][0]
        p = Project.model_validate({"name": "casa", "rooms": [cave] + x["divisoes"], "openings": x["aberturas"], "base": x["base"],
                                    "panel": {"room_id": d0["id"], "pos": d0["polygon"][0]}})
        assert {r.floor for r in p.rooms} == {-1, 0} and len(p.rooms) == 3
        assert (Path(tmp) / "casa" / "base.dxf").read_text(encoding="utf-8").count("ARQ-PAREDES") > 10
        res = sv.calcular("casa", json.loads(p.model_dump_json()))
        assert "<svg" in res["planta_svg"]

def test_projeto_vazio_da_mensagem_clara_e_nao_erro_interno():
    from eletro.web.service import Erro
    with tempfile.TemporaryDirectory() as tmp:
        sv = Servico(tmp); sv.criar("vazio")
        try:
            sv.calcular("vazio", sv.abrir("vazio")["project"]); assert False
        except Erro as e:
            assert "sem divisoes" in str(e)

def test_app_js_importadores_aceitam_projeto_sem_equipamentos():
    js = (Path(__file__).parents[2] / "src/eletro/web/static/app.js").read_text(encoding="utf-8")
    assert "S.P.equipment.filter" not in js and js.count("(S.P.equipment || []).filter") >= 2

def test_projeto_novo_grava_todos_os_campos():
    with tempfile.TemporaryDirectory() as tmp:
        sv = Servico(tmp); p = sv.criar("novo")["project"]
        assert p["equipment"] == [] and p["openings"] == [] and p["rooms"] == []

def test_servico_pdf_importar_recusa_escala_errada():
    """Teste manual 14-10, passo 2.5: com a escala errada a detecao da erro, mas o Importar deixava passar areas x4."""
    from eletro.web.service import Erro
    with tempfile.TemporaryDirectory() as tmp:
        sv = Servico(tmp); sv.criar("casa"); sv.pdf_analisar("casa", arq_pdf.pdf())
        try:
            sv.pdf_importar("casa", 1, ["PAREDES"], ["VISTA"], 100); assert False, "devia recusar"
        except Erro as e:
            assert "1:50" in str(e), e
        assert sv.pdf_importar("casa", 1, ["PAREDES"], ["VISTA"], 50)["divisoes"]

def test_pdf_leitores_ficam_fechados():
    """Teste manual 14-10, passo 0: aviso 'PdfDocument still open' -> a app acumulava PDFs abertos."""
    fechados = []
    orig = pdfread._fechar
    pdfread._fechar = lambda *a: (fechados.append(1), orig(*a))
    try:
        pdfread.analisar(arq_pdf.pdf()); pdfread.extrair(arq_pdf.pdf(), 1, ["PAREDES"], 50, ["VISTA"])
    finally:
        pdfread._fechar = orig
    assert len(fechados) == 2
