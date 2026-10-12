"""Modelo de dados do projeto. Toda a entrada (JSON manual, DXF, PDF) converge aqui."""
from __future__ import annotations
from typing import Literal, Optional
from pydantic import BaseModel, Field

Use = Literal["sala", "quarto", "cozinha", "wc", "hall", "corredor", "arrumos",
              "garagem", "varanda", "escritorio", "lavandaria", "outro"]

class Room(BaseModel):
    id: str
    name: str
    use: Use
    area_m2: float = Field(gt=0)
    height_m: float = 2.6
    source: Literal["manual", "dxf", "pdf", "foto"] = "manual"
    confirmed: bool = False  # humano validou? dados vindos de pdf/foto ficam False

class Supply(BaseModel):
    phases: Literal[1, 3] = 1
    contracted_kva: Optional[float] = None

class Project(BaseModel):
    name: str
    location: str = ""
    supply: Supply = Supply()
    rooms: list[Room]

    def unconfirmed(self) -> list[Room]:
        return [r for r in self.rooms if not r.confirmed]

    def total_area(self) -> float:
        return sum(r.area_m2 for r in self.rooms)
