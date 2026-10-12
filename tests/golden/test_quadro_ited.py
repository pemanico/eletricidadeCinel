"""Quadro e ITED: valores calculados a mao. Convencao de simultaneidade v1 (ilum 1,0; tomadas 0,25 de 3680 W; equip. 1,0)."""
import json
from eletro.schema.project import load, Project
from eletro.engine import calcular
from eletro.rules.dotacao import carregar_perfil
from eletro.rules import ited as ited_mod
from eletro.rules.quadro import potencia_a_contratar, calibre_geral_a, calibre_ddr, pe_mm2, modulos

EX, PERFIL, ITED = "examples/moradia_t3/projeto.json", "data/convencoes/convencao_projeto_v1.json", "data/convencoes/ited_dotacao_v1.json"
def _res(raw=None):
    p = load(EX) if raw is None else Project.model_validate(raw)
    return calcular(p, carregar_perfil(PERFIL), ited_mod.carregar(ITED))
def _raw(): return json.load(open(EX, encoding="utf-8"))

def test_potencia_de_calculo_a_mao():
    q = _res().quadro
    assert q.p_inst_w == 360 + 4 * 3680 + 4600 == 19680
    assert q.p_calc_w == 360 + 4 * 920 + 4600 == 8640
    assert q.s_calc_kva == 8.64 and q.potencia_a_contratar_kva == 10.35   # 6,90 < 8,64 <= 10,35

def test_geral_e_ddr():
    q = _res().quadro
    assert q.geral_in_a == 45 and q.poder_corte_ka == 6 and q.n_mcb == 6
    assert [d["in_a"] for d in q.ddr] == [63, 63] and all(d["idn_ma"] == 30 for d in q.ddr)
    ddr = {d["id"]: d for d in q.ddr}
    assert ddr["DDR-1"]["circuitos"] == ["ILUM-1", "TOM-1", "TOM-3"]          # secos
    assert ddr["DDR-2"]["circuitos"] == ["TOM-2", "TOM-4", "EQ-e1"]           # cozinha, wc, equipamento
    assert ddr["DDR-1"]["corrente_calculo_a"] == 9.6 and ddr["DDR-2"]["corrente_calculo_a"] == 28.0   # 2200/230; 6440/230

def test_modulos_a_mao():
    # 1 geral(2) + 2 DDR(4) + 6 MCB(12) = 18; x1,2 = 21,6 -> 22; 2 fileiras de 12 = 24
    m = _res().quadro.modulos
    assert (m["base"], m["com_reserva"], m["fileiras"], m["total_modulos"]) == (18, 22, 2, 24)

def test_tabelas_do_quadro():
    assert [calibre_geral_a(k, 1) for k in (6.9, 10.35, 13.8, 17.25)] == [30, 45, 60, 75]
    assert [calibre_geral_a(k, 3) for k in (10.35, 17.25, 41.4)] == [15, 25, 60]
    assert [calibre_ddr(i, [25, 40, 63, 80, 100]) for i in (30, 45, 60, 75)] == [40, 63, 63, 80]
    assert [pe_mm2(s) for s in (1.5, 2.5, 16, 25, 50)] == [1.5, 2.5, 16, 16, 25.0]       # Quadro 54F
    esc = {"1": [1.15, 2.3, 3.45, 4.6, 5.75, 6.9, 10.35, 13.8]}
    assert potencia_a_contratar(5.0, 6.9, 1, esc) == 6.9 and potencia_a_contratar(11, 6.9, 1, esc) == 13.8

def test_pe_igual_a_seccao_de_fase_ate_16():
    c = {c.id: c for c in _res().circuitos}
    assert c["ILUM-1"].pe_mm2 == 1.5 and c["TOM-1"].pe_mm2 == 2.5 and c["EQ-e1"].pe_mm2 == 4.0

def test_ited_por_divisao_e_estado():
    r = _res()
    assert [(r.ited[k]["rj45"], r.ited[k]["tv"]) for k in ("r1", "r2", "r3", "r4", "r5")] == [(2, 1), (2, 1), (1, 1), (1, 1), (0, 0)]
    assert r.ited["r1"]["estado"] == "POR_CONFIRMAR" and r.ited["r3"]["estado"] == "CONVENCAO"
    assert any(v.ref == "Manual ITED" and "NAO dimensionados" in v.texto and "6 RJ45 e 4 TV" in v.texto for v in r.verificacoes)

def test_icc_e_terra_verificadas_quando_fornecidas():
    raw = _raw(); raw["supply"]["icc_ka"] = 10.0; raw["supply"]["r_terra_ohm"] = 30
    v = _res(raw).verificacoes
    assert any(x.ref == "RTIEBT 434" and x.estado == "NAO_CUMPRE" for x in v)           # 6 kA < 10 kA
    assert any("801.5.6.1" in x.ref and x.estado == "CUMPRE" for x in v)                # 30 ohm < 100; 30*0,03 = 0,9 V
    raw["supply"]["r_terra_ohm"] = 150
    assert any("801.5.6.1" in x.ref and x.estado == "NAO_CUMPRE" for x in _res(raw).verificacoes)

def test_icc_e_terra_em_falta_ficam_por_confirmar():
    v = _res().verificacoes
    assert any(x.ref == "RTIEBT 434" and x.estado == "POR_CONFIRMAR" for x in v)
    assert any("801.5.6.1" in x.ref and x.estado == "POR_CONFIRMAR" for x in v)
    assert any("magnetico" in x.texto and x.estado == "AVISO" for x in v)               # disparo magnetico NAO verificado

def test_potencia_contratada_abaixo_do_calculo_avisa():
    raw = _raw(); raw["supply"]["contracted_kva"] = 6.9
    assert any(x.estado == "AVISO" and "inferior a potencia de calculo" in x.texto for x in _res(raw).verificacoes)

def test_trifasico_nao_suportado_avisa_sem_quadro():
    raw = _raw(); raw["supply"]["phases"] = 3
    r = _res(raw)
    assert r.quadro is None and any("Trifasico ainda nao suportado" in x.texto for x in r.verificacoes)
