"""Dotacao de pontos por divisao. CONVENCAO DE PROJETO (nao normativa): ver data/convencoes/."""
import math, json

def carregar_perfil(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def pontos_divisao(room, perfil: dict) -> dict:
    d = perfil["dotacao"][room.use]
    luz = max(d["luz_min"], math.ceil(room.area_m2 / d["luz_divisor_m2"]))
    tom = max(d["tom_min"], math.ceil(room.area_m2 / d["tom_divisor_m2"]))
    interr = max(1, math.ceil(luz / perfil["interruptores_por_pontos_de_luz"]))
    return {"luz": luz, "tomadas": tom, "interruptores": interr}
