"""Golden tests: exemplos verificados nos study_notes. Se falharem, o codigo ou a nota esta errada."""
from eletro.calc.cabos import size_mono, ib_mono, drop_mono_pct

def test_termoacumulador_corrigido():
    # 4,6 kW, 25 m, B1, 35 C (k1=0.94), 3 circuitos (k2=0.70) -> 6 mm2, C20
    r = size_mono(4600, 25, k1=0.94, k2=0.70)
    assert round(r["ib"]) == 20 and r["in"] == 20 and r["s_mm2"] == 6
    assert round(r["iz"], 1) == 23.7

def test_4mm2_falha_no_exemplo():
    assert round(28 * 0.94 * 0.70, 1) == 18.4  # < 20 A

def test_exercicio_16A():
    assert ib_mono(3680) == 16
    r = size_mono(3680, 10)
    assert r["s_mm2"] == 2.5 and r["in"] == 16
