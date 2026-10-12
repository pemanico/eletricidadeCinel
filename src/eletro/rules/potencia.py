"""Potencia minima e alimentacao em habitacao. FONTE: RTIEBT 801.5.2.2 e 801.1.1.3.3 (Portaria 949-A/2006, vers. 19-8-2015)."""
import math

def compartimentos(project, nao_contam: list[str]) -> int:
    return sum(1 for r in project.rooms if r.use not in nao_contam)

def potencia_minima_kva(n_comp: int, fases: int) -> float:
    """801.5.2.2. Mono: 3,45 (1 comp.), 6,90 (2 a 6), 10,35 (>6). Tri: 6,90 (<=6), 10,35 (>6)."""
    if fases == 1:
        return 3.45 if n_comp <= 1 else (6.90 if n_comp <= 6 else 10.35)
    return 6.90 if n_comp <= 6 else 10.35
