from pydantic import BaseModel
from typing import Optional
from datetime import date
from uuid import UUID

class PartidoCreate(BaseModel):
    nombre: str
    sigla: str

class PartidoRead(BaseModel):
    id: int
    uuid: UUID
    nombre: str
    sigla: str
    class Config:
        from_attributes = True


class CargoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CargoRead(BaseModel):
    id: int
    uuid: UUID
    nombre: str
    descripcion: Optional[str]
    class Config:
        from_attributes = True


class CandidatoCreate(BaseModel):
    nombres: str
    apellidos: str
    partido_id: Optional[int] = None
    cargo_id: Optional[int] = None

class CandidatoRead(BaseModel):
    id: int
    uuid: UUID
    nombres: str
    apellidos: str
    partido_id: Optional[int]
    cargo_id: Optional[int]
    class Config:
        from_attributes = True


class ProcesoCreate(BaseModel):
    nombre: str
    fecha_inicio: date
    fecha_fin: date
    tipo: str
    estado: str

class ProcesoRead(BaseModel):
    id: int
    uuid: UUID
    nombre: str
    fecha_inicio: date
    fecha_fin: date
    tipo: str
    estado: str
    class Config:
        from_attributes = True


class EleccionCreate(BaseModel):
    proceso_id: int
    cargo_id: int
    descripcion: Optional[str] = None
    fecha: Optional[date] = None

class EleccionRead(BaseModel):
    id: int
    uuid: UUID
    proceso_id: int
    cargo_id: int
    descripcion: Optional[str]
    fecha: Optional[date]
    class Config:
        from_attributes = True
