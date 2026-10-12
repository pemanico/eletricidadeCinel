"""Dimensionamento de condutores. CALCULO DETERMINISTICO: o LLM chama, nao calcula.
ATENCAO: tabelas simplificadas para ESTUDO. Validar contra IEC 60364-5-52 / RTIEBT antes de uso real."""
import math

# Cu/PVC, metodo B1, 2 condutores carregados, 30 C (A). Fonte: ver study_notes/B2_UC01781*
IZ_B1_PVC_2 = {1.5: 15.5, 2.5: 21, 4: 28, 6: 36, 10: 50, 16: 68}
# Disjuntores normalizados (A)
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

def size_mono(p_w: float, length_m: float, k1: float = 1.0, k2: float = 1.0,
              cosphi: float = 1.0, max_drop_pct: float = 3.0) -> dict:
    """Escolhe a menor secao com Ib<=In<=Iz (Iz = I'z*k1*k2) e queda de tensao <= max."""
    ib = ib_mono(p_w, cosphi=cosphi)
    inn = next_in(ib)
    for s, iz0 in IZ_B1_PVC_2.items():
        iz = iz0 * k1 * k2
        d = drop_mono_pct(ib, length_m, s)
        # I2 = 1.45*In para disjuntores => 1.45*In <= 1.45*Iz  <=>  In <= Iz (coberto)
        if inn <= iz and d <= max_drop_pct:
            return {"ib": ib, "in": inn, "s_mm2": s, "iz": iz, "drop_pct": d}
    raise ValueError("Nenhuma secao <=16 mm2 cumpre: rever metodo/comprimento")
