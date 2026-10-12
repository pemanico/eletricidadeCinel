import json, copy
from eletro.schema.project import Project, load, polygon_area
from eletro.schema.dynamic import resolve, diff
from eletro.cad.planta import desenhar
from eletro.cad.dxf import parse_entities

EX = "examples/moradia_t3/projeto.json"

def _raw(): return json.load(open(EX, encoding="utf-8"))

def test_area_do_poligono():
    assert polygon_area([(0,0),(6,0),(6,4),(0,4)]) == 24
    p = load(EX)
    assert p.rooms[0].area_m2 == 24 and round(p.total_area(), 1) == 64.0

def test_area_incoerente_rejeitada():
    raw = _raw(); raw["rooms"][0]["area_m2"] = 30
    try: Project.model_validate(raw)
    except ValueError: return
    raise AssertionError("devia rejeitar area incoerente")

def test_referencia_inexistente_rejeitada():
    raw = _raw(); raw["equipment"][0]["room_id"] = "xx"
    try: Project.model_validate(raw)
    except ValueError: return
    raise AssertionError("devia rejeitar divisao inexistente")

def test_override_aplicado_e_sobrevive():
    raw = _raw()
    raw["overrides"] = [{"target": "panel", "field": "pos", "value": [0.3, 1.2], "base": [0.3, 0.5], "reason": "armario"}]
    p = Project.model_validate(raw)
    q, c = resolve(p)
    assert c == [] and tuple(q.panel.pos) == (0.3, 1.2)
    assert tuple(p.panel.pos) == (0.3, 0.5)  # original intacto

def test_override_conflito_quando_modelo_muda():
    raw = _raw()
    raw["overrides"] = [{"target": "panel", "field": "pos", "value": [0.3, 1.2], "base": [0.3, 0.5]}]
    raw["panel"]["pos"] = [5.0, 0.5]  # modelo mudou
    q, c = resolve(Project.model_validate(raw))
    assert len(c) == 1 and "NAO aplicado" in c[0] and tuple(q.panel.pos) == (5.0, 0.5)

def test_diff_revisoes():
    a = load(EX); raw = _raw()
    raw["rooms"][4]["use"] = "lavandaria"
    raw["equipment"][0]["power_w"] = 3000
    raw["equipment"].append({"id": "e2", "kind": "forno", "room_id": "r2", "power_w": 3500})
    ch = diff(a, Project.model_validate(raw))
    assert any("divisao r5.use" in x for x in ch)
    assert any("equipamento e1.power_w" in x for x in ch)
    assert "+ equipamento e2" in ch
    assert diff(a, a) == []

def test_dxf_estrutura():
    d, c = desenhar(load(EX))
    txt = d.dumps()
    lines = txt.split("\n")
    assert lines[-2] == "EOF" and len(lines) % 2 == 1  # pares codigo/valor + linha final vazia
    ents = parse_entities(txt)
    assert sum(1 for t, l in ents if t == "POLYLINE" and l == "PAREDES") == 5
    assert any(l == "QUADRO" for t, l in ents)
    assert "por confirmar" in txt and "RASCUNHO" in txt  # avisos de seguranca presentes
    assert txt.isascii()
