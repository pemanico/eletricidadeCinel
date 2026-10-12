"""Tomadas de telecomunicacoes (ITED) por divisao. Fonte normativa: Manual ITED (ANACOM), NAO incluido nas fontes:
valores marcados POR_CONFIRMAR/CONVENCAO no ficheiro de dotacao. Nao dimensiona ATI/tubagem."""
import json

def carregar(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def dotacao_ited(room, cfg: dict) -> dict:
    d = cfg["dotacao"][room.use]
    return {"rj45": d["rj45"], "tv": d["tv"], "estado": d["estado"], "fonte": d["fonte"]}
