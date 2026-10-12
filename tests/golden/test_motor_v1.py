"""Valores calculados a mao (independentes do codigo) para a moradia-tipo de examples/moradia_t3.
Convencao v1; tabelas RTIEBT 52-C1 (ed. 2000, por confirmar)."""
import json
from eletro.schema.project import load, Project
from eletro.engine import calcular
from eletro.rules.dotacao import carregar_perfil
from eletro.rules.circuitos import agrupar_sequencial
from eletro.rules.potencia import potencia_minima_kva

EX, PERFIL = "examples/moradia_t3/projeto.json", "data/convencoes/convencao_projeto_v1.json"
def _res(raw=None):
    p = load(EX) if raw is None else Project.model_validate(raw)
    return calcular(p, carregar_perfil(PERFIL))
def _c(r, cid): return next(c for c in r.circuitos if c.id == cid)

def test_pontos_por_divisao():
    r = _res()
    assert [r.pontos[k]["luz"] for k in ("r1", "r2", "r3", "r4", "r5")] == [2, 1, 1, 1, 1]
    assert [r.pontos[k]["tomadas"] for k in ("r1", "r2", "r3", "r4", "r5")] == [6, 6, 4, 4, 1]

def test_circuitos_agrupados_max_8_pontos():
    r = _res()
    assert [c.id for c in r.circuitos] == ["ILUM-1", "TOM-1", "TOM-2", "TOM-3", "TOM-4", "EQ-e1"]
    assert _c(r, "TOM-3").divisoes == ["r3", "r4"] and _c(r, "TOM-3").pontos == 8
    assert agrupar_sequencial([("a", 10)], 8) == [[("a", 8)], [("a", 2)]]

def test_comprimentos_estimados_a_mao():
    r = _res()   # (Manhattan * 1,2) + 3,0
    for cid, L in [("ILUM-1", 34.74), ("TOM-1", 8.04), ("TOM-2", 13.14), ("TOM-3", 15.54), ("TOM-4", 17.94)]:
        assert abs(_c(r, cid).comprimento_m - L) < 0.01, cid

def test_seccoes_iz_e_quedas():
    r = _res()
    assert (_c(r, "ILUM-1").s_mm2, _c(r, "ILUM-1").iz_a) == (1.5, 12.25)      # 17,5*0,70
    assert (_c(r, "TOM-4").s_mm2, _c(r, "TOM-4").iz_a) == (2.5, 16.8)         # 24*0,70
    eq = _c(r, "EQ-e1")
    assert (eq.s_mm2, eq.in_a, eq.iz_a) == (4.0, 20, 22.4)                    # 32*0,70
    assert abs(_c(r, "TOM-4").queda_pct - 2.246) < 0.005
    assert abs(_c(r, "ILUM-1").queda_pct - 0.709) < 0.005

def test_potencia_minima_801_5_2_2():
    assert [potencia_minima_kva(n, 1) for n in (1, 2, 6, 7)] == [3.45, 6.90, 6.90, 10.35]
    assert [potencia_minima_kva(n, 3) for n in (5, 6, 7)] == [6.90, 6.90, 10.35]
    assert _res().potencia_minima_kva == 6.90 and _res().n_compartimentos == 5

def test_potencia_contratada_insuficiente_e_detetada():
    raw = json.load(open(EX, encoding="utf-8")); raw["supply"]["contracted_kva"] = 3.45
    assert any(v.estado == "NAO_CUMPRE" and "801.5.2.2" in v.ref for v in _res(raw).verificacoes)

def test_comprimento_manual_substitui_estimativa():
    raw = json.load(open(EX, encoding="utf-8")); raw["circuit_length_m"] = {"TOM-4": 40.0}
    c = _c(_res(raw), "TOM-4")
    assert c.comprimento_origem == "MANUAL" and c.comprimento_m == 40.0
    assert c.queda_pct > 2.246  # a queda sobe com o comprimento (ou a secao aumenta)

def test_dados_por_confirmar_sao_assinalados_e_convencao_identificada():
    r = _res()
    assert any(v.estado == "AVISO" and "r5" in v.texto for v in r.verificacoes)
    assert any(v.estado == "CONVENCAO" for v in r.verificacoes)
    assert any(v.estado == "POR_CONFIRMAR" for v in r.verificacoes)

def test_circuito_inviavel_fica_com_erro_e_NAO_CUMPRE():
    raw = json.load(open(EX, encoding="utf-8")); raw["circuit_length_m"] = {"TOM-4": 3000.0}
    r = _res(raw)
    assert _c(r, "TOM-4").erro and any(v.estado == "NAO_CUMPRE" and "TOM-4" in v.texto for v in r.verificacoes)

def test_aviso_quando_seccao_sobe_acima_do_minimo():
    raw = json.load(open(EX, encoding="utf-8")); raw["circuit_length_m"] = {"TOM-4": 60.0}
    r = _res(raw); c = _c(r, "TOM-4")
    assert c.s_mm2 > 2.5   # 2,5 mm2 daria queda > 5% a 60 m com 16 A
    assert any(v.estado == "AVISO" and "TOM-4" in v.texto and "aumentada" in v.texto for v in r.verificacoes)
