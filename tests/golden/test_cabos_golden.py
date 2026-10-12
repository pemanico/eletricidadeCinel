"""Golden tests. Fonte das tabelas: RTIEBT Quadro 52-C1 (edicao 2000, a confirmar no DR original)."""
from eletro.calc.cabos import size_mono, ib_mono, IZ_PVC_CU_2, IZ_IEC2009_B1_PVC_CU_2, K1_PVC, K2_EMBEBIDOS

def test_tabela_rtiebt_52C1_metodo_B():
    assert IZ_PVC_CU_2["B"][4] == 32 and IZ_PVC_CU_2["B"][2.5] == 24 and IZ_PVC_CU_2["B"][6] == 41

def test_termoacumulador_rtiebt():
    # 4,6 kW, 25 m, metodo B (tubo embebido em alvenaria, ref.5), 35 C (52-D1), 3 circuitos (52-E1 ref.1)
    k1, k2 = K1_PVC[35], K2_EMBEBIDOS[3]
    assert (k1, k2) == (0.94, 0.70)
    r = size_mono(4600, 25, k1=k1, k2=k2, min_s_mm2=2.5)
    assert round(r["ib"]) == 20 and r["in"] == 20 and r["s_mm2"] == 4
    assert round(r["iz"], 2) == 21.06  # 32 * 0.94 * 0.70

def test_mesma_situacao_com_tabela_IEC2009_daria_6mm2():
    # Diferenca de tabela, nao de logica: 28*0.658 = 18.4 < 20 -> 6 mm2. NAO e o RTIEBT.
    assert round(IZ_IEC2009_B1_PVC_CU_2[4] * 0.94 * 0.70, 1) == 18.4

def test_circuito_tomadas_16A_secao_minima_habitacao():
    assert ib_mono(3680) == 16
    r = size_mono(3680, 10, min_s_mm2=2.5)   # 801.5.8: tomadas >= 2,5 mm2
    assert r["s_mm2"] == 2.5 and r["in"] == 16
