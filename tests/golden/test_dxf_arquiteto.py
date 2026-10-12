from arq_dxf import arquiteto_dxf
from eletro.cad import dxfread
from eletro.schema.project import Project

def test_analise_camadas_e_unidades():
    d = dxfread.ler(arquiteto_dxf())
    a = dxfread.analisar(d)
    assert a["unidade_m"] == 0.001 and a["unidades_codigo"] == 4
    assert a["camadas"]["AREAS"]["poli_fechadas"] == 6          # 5 divisoes + envolvente
    assert a["camadas"]["PAREDES"]["linhas"] == 4 and a["camadas"]["TEXTOS"]["textos"] == 10
    assert a["sugestao_camada_divisoes"] == "AREAS"
    assert not any(e.nome == "SOFA" and e.layer == "PORTAS" for e in d["entidades"])   # bloco BLOCKS nao e lido como entidade
    assert sum(1 for e in d["entidades"] if e.tipo == "LINE" and e.layer == "0") == 0   # linha dentro de BLOCK ignorada

def test_extrai_divisoes_areas_usos_e_ignora_envolvente():
    d = dxfread.ler(arquiteto_dxf())
    r = dxfread.extrair_divisoes(d, "AREAS", 0.001)
    assert [x["name"] for x in r["divisoes"]] == ["SALA", "COZINHA", "QUARTO 1", "QUARTO 2", "I.S."]
    assert [x["use"] for x in r["divisoes"]] == ["sala", "cozinha", "quarto", "quarto", "wc"]
    assert any("contorno do edificio" in a for a in r["avisos"])
    assert all(x["confirmed"] is False and x["source"] == "dxf" for x in r["divisoes"])
    p = Project.model_validate({"name": "t", "rooms": r["divisoes"], "openings": r["aberturas"]})
    assert [r_.area_m2 for r_ in p.rooms] == [24.0, 10.5, 14.0, 10.5, 5.0]        # m2, convertidos de mm

def test_portas_e_janelas_por_blocos_ligadas_a_divisao():
    r = dxfread.extrair_divisoes(dxfread.ler(arquiteto_dxf()), "AREAS", 0.001)
    ab = {a["kind"]: a for a in r["aberturas"]}
    assert ab["porta"]["room_id"] == "r1" and ab["porta"]["pos"] == [2.55, 0.0]
    assert ab["janela"]["pos"] == [0.9, 4.0] and ab["janela"]["room_id"] in ("r1", "r3")   # parede partilhada
    assert len(r["aberturas"]) == 2                                                          # SOFA ignorado

def test_sem_textos_usa_nome_generico_e_avisa():
    r = dxfread.extrair_divisoes(dxfread.ler(arquiteto_dxf(com_textos=False)), "AREAS", 0.001)
    assert r["divisoes"][0]["name"] == "Divisao 1" and any("sem texto" in a for a in r["avisos"])

def test_camada_errada_avisa():
    r = dxfread.extrair_divisoes(dxfread.ler(arquiteto_dxf()), "PAREDES", 0.001)
    assert r["divisoes"] == [] and any("Nenhuma divisao" in a for a in r["avisos"])

def test_dxf_binario_e_lixo_rejeitados():
    for txt in ("AutoCAD Binary DXF\r\n\x1a\x00", "isto nao e um dxf\ncom linhas\nsoltas"):
        try: dxfread.ler(txt)
        except dxfread.DxfError: continue
        raise AssertionError("devia rejeitar")
