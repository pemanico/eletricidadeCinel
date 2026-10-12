"""Quadro electrico de habitacao monofasica: potencia a contratar, geral, DDR, modulos.
FONTES: RTIEBT 801.5.2.2 (potencias minimas), 801.5.9 (diferenciais), 412.5/531.2.6/701 (30 mA), 543.1/Q.54F (PE).
O resto (simultaneidade, curvas, agrupamento de DDR, modulos) e CONVENCAO (ver perfil)."""
import math

def potencia_a_contratar(s_calc_kva: float, minima_kva: float, fases: int, escaloes: dict) -> float:
    lista = escaloes[str(fases)]
    return max(minima_kva, next((x for x in lista if x >= s_calc_kva - 1e-9), lista[-1]))

def calibre_geral_a(kva: float, fases: int) -> int:
    return round(kva * 1000 / (230.0 if fases == 1 else math.sqrt(3) * 400.0))

def calibre_ddr(in_geral: int, calibres: list[int]) -> int:
    return next((c for c in calibres if c >= in_geral), calibres[-1])

def pe_mm2(s_fase: float) -> float:
    """RTIEBT Quadro 54F (ed. 2000, por confirmar): SF<=16 -> SPE=SF; 16<SF<=35 -> 16; SF>35 -> SF/2. Minimo 2,5 (543.1.3a)."""
    if s_fase <= 16: pe = s_fase
    elif s_fase <= 35: pe = 16
    else: pe = s_fase / 2
    return pe   # PE no mesmo cabo que as fases; a regra 543.1.3 (2,5/4 mm2) aplica-se a PE fora da canalizacao

def modulos(n_mcb: int, n_ddr: int, cfg: dict) -> dict:
    base = n_mcb * cfg["por_mcb"] + n_ddr * cfg["por_ddr"] + cfg["por_geral"]
    com_reserva = math.ceil(base * (1 + cfg["reserva"]))
    fileiras = math.ceil(com_reserva / cfg["por_fileira"])
    return {"base": base, "com_reserva": com_reserva, "fileiras": fileiras, "total_modulos": fileiras * cfg["por_fileira"]}
