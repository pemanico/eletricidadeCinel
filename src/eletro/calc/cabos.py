"""Dimensionamento de condutores. CALCULO DETERMINISTICO: o LLM chama, nao calcula.

FONTE DAS TABELAS: RTIEBT (Portaria 949-A/2006), Parte 5, Anexo, Quadro 52-C1 (Cu, PVC, 2 condutores
carregados, 70 C, ambiente 30 C), colunas dos metodos de referencia A, B e C (Quadro 52H).
Valores lidos da edicao anotada de 2000 (sources/normativas/RTIEBT_anotada_...pdf, ~linha 20595).
!! O PDF consolidado (versao 19-8-2015) NAO traz o texto das tabelas ("ver documento original").
!! POR CONFIRMAR contra o original do Diario da Republica / DGEG antes de uso real.
Factores: Quadro 52-D1 (temperatura, PVC) e 52-E1 (agrupamento, ref. 1 encastrados)."""
import math

# RTIEBT Quadro 52-C1, Cu/PVC, 2 condutores carregados, 30 C: {metodo: {secao_mm2: A}}
IZ_PVC_CU_2 = {
    "A": {1.5: 14.5, 2.5: 19.5, 4: 26, 6: 34, 10: 46, 16: 61, 25: 80, 35: 99, 50: 119},
    "B": {1.5: 17.5, 2.5: 24, 4: 32, 6: 41, 10: 57, 16: 76, 25: 101, 35: 125, 50: 151},
    "C": {1.5: 19.5, 2.5: 27, 4: 36, 6: 46, 10: 63, 16: 85, 25: 112, 35: 138, 50: 168},
}
# IEC 60364-5-52:2009 metodo B1 (NAO e o RTIEBT). Guardado so para comparacao; nao usar em projeto PT.
IZ_IEC2009_B1_PVC_CU_2 = {1.5: 15.5, 2.5: 21, 4: 28, 6: 36, 10: 50, 16: 68}

K1_PVC = {10: 1.22, 15: 1.17, 20: 1.12, 25: 1.06, 30: 1.00, 35: 0.94, 40: 0.87, 45: 0.79, 50: 0.71, 55: 0.61, 60: 0.50}  # 52-D1
K2_EMBEBIDOS = {1: 1.00, 2: 0.80, 3: 0.70, 4: 0.65, 5: 0.60, 6: 0.57, 7: 0.54, 8: 0.52, 9: 0.50}  # 52-E1 ref. 1

IN_STD = [6, 10, 13, 16, 20, 25, 32, 40, 50, 63]
RHO_CU = 0.0225  # ohm.mm2/m a ~70 C (valor de projeto usado nos exemplos)

def ib_mono(p_w: float, u: float = 230.0, cosphi: float = 1.0) -> float:
    return p_w / (u * cosphi)

def ib_tri(p_w: float, u: float = 400.0, cosphi: float = 1.0) -> float:
    return p_w / (math.sqrt(3) * u * cosphi)

def next_in(ib: float) -> int:
    return next(i for i in IN_STD if i >= ib)

def drop_mono_pct(ib: float, length_m: float, s_mm2: float, u: float = 230.0) -> float:
    return 2 * RHO_CU * length_m * ib / s_mm2 / u * 100

def size_mono(p_w: float, length_m: float, k1: float = 1.0, k2: float = 1.0, cosphi: float = 1.0,
              max_drop_pct: float = 3.0, metodo: str = "B", min_s_mm2: float = 1.5) -> dict:
    """Menor secao com Ib<=In<=Iz (Iz = I'z*k1*k2), queda de tensao <= max e secao >= minima regulamentar
    (801.5.8 em habitacao: iluminacao 1,5; tomadas/termoacumuladores/maquinas/climatizacao 2,5; fogoes 4)."""
    ib = ib_mono(p_w, cosphi=cosphi)
    inn = next_in(ib)
    for s, iz0 in IZ_PVC_CU_2[metodo].items():
        if s < min_s_mm2:
            continue
        iz = iz0 * k1 * k2
        d = drop_mono_pct(ib, length_m, s)
        # I2 = 1,45*In (disjuntores) => I2 <= 1,45*Iz equivale a In <= Iz (coberto)
        if inn <= iz and d <= max_drop_pct:
            return {"ib": ib, "in": inn, "s_mm2": s, "iz": iz, "drop_pct": d, "metodo": metodo}
    raise ValueError("Nenhuma secao <=50 mm2 cumpre: rever metodo/comprimento")
