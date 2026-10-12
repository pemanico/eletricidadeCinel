"""Modelo de dados do projeto: FONTE UNICA DE VERDADE. Desenhos, quadros e orçamento são vistas geradas."""
from __future__ import annotations
from typing import Literal, Optional
from pydantic import BaseModel, Field, model_validator

Point = tuple[float, float]  # metros, referencial do piso

Use = Literal["sala", "quarto", "cozinha", "wc", "hall", "corredor", "arrumos",
              "garagem", "varanda", "escritorio", "lavandaria", "outro"]

def polygon_area(poly: list[Point]) -> float:
    """Formula de Gauss (shoelace)."""
    n = len(poly)
    s = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
    return abs(s) / 2

class Room(BaseModel):
    id: str
    name: str
    use: Use
    floor: int = 0
    polygon: list[Point] = []
    area_m2: Optional[float] = Field(default=None, gt=0)
    height_m: float = 2.6
    source: Literal["manual", "dxf", "pdf", "foto"] = "manual"
    confirmed: bool = False  # dados de pdf/foto ficam False ate validacao humana

    @model_validator(mode="after")
    def _area(self):
        if self.polygon:
            if len(self.polygon) < 3:
                raise ValueError(f"{self.id}: poligono precisa de >=3 pontos")
            a = polygon_area(self.polygon)
            if self.area_m2 is None:
                self.area_m2 = round(a, 2)
            elif abs(self.area_m2 - a) / a > 0.02:
                raise ValueError(f"{self.id}: area {self.area_m2} m2 difere do poligono ({a:.2f} m2) >2%")
        elif self.area_m2 is None:
            raise ValueError(f"{self.id}: indicar poligono ou area_m2")
        return self

class Opening(BaseModel):
    id: str
    kind: Literal["porta", "janela"]
    room_id: str
    pos: Point
    width_m: float = 0.9

class Equipment(BaseModel):
    id: str
    kind: Literal["termoacumulador", "forno", "placa", "avac", "maq_lavar", "outro"]
    room_id: str
    power_w: float = Field(gt=0)

class Panel(BaseModel):
    room_id: str
    pos: Point

class Supply(BaseModel):
    phases: Literal[1, 3] = 1
    contracted_kva: Optional[float] = None
    icc_ka: Optional[float] = None        # corrente de curto-circuito no ponto de ligacao (pedir a e-Redes)
    r_terra_ohm: Optional[float] = None   # resistencia de terra medida

class Revision(BaseModel):
    number: int
    date: str
    author: str = ""
    reason: str = ""

class Override(BaseModel):
    """Ajuste manual que sobrevive a regeneracao. `base` = valor do modelo quando o ajuste foi feito."""
    target: str          # "panel" ou "room:<id>"
    field: str           # "pos" | "name" | "height_m"
    value: object
    base: object = None
    reason: str = ""

class BaseDxf(BaseModel):
    """DXF do arquiteto usado como base. Coordenadas do Project = coordenadas DXF x unit_m (metros por unidade)."""
    file: str
    unit_m: float = Field(gt=0)

class Project(BaseModel):
    name: str
    location: str = ""
    supply: Supply = Supply()
    rooms: list[Room]
    openings: list[Opening] = []
    equipment: list[Equipment] = []
    panel: Optional[Panel] = None
    revision: int = 0
    revisions: list[Revision] = []
    overrides: list[Override] = []
    base: Optional[BaseDxf] = None
    circuit_length_m: dict[str, float] = {}   # correcao manual do comprimento por circuito (ex.: "TOM-1": 18.5)

    @model_validator(mode="after")
    def _refs(self):
        ids = {r.id for r in self.rooms}
        if len(ids) != len(self.rooms):
            raise ValueError("ids de divisao repetidos")
        for o in self.openings:
            if o.room_id not in ids: raise ValueError(f"abertura {o.id}: divisao {o.room_id} inexistente")
        for e in self.equipment:
            if e.room_id not in ids: raise ValueError(f"equipamento {e.id}: divisao {e.room_id} inexistente")
        if self.panel and self.panel.room_id not in ids:
            raise ValueError("quadro: divisao inexistente")
        return self

    def unconfirmed(self) -> list[Room]:
        return [r for r in self.rooms if not r.confirmed]

    def total_area(self) -> float:
        return sum(r.area_m2 for r in self.rooms)

def load(path: str) -> Project:
    import json
    with open(path, encoding="utf-8") as f:
        return Project.model_validate(json.load(f))
