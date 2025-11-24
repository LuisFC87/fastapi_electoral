from pydantic import BaseModel
from typing import Optional
from datetime import date

class PartidoCreate(BaseModel):
    nombre: str
    sigla: str

class PartidoRead(BaseModel):
    id: int
    uuid: str
    nombre: str
    sigla: str
    class Config:
        orm_mode = True


class CargoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CargoRead(BaseModel):
    id: int
    uuid: str
    nombre: str
    descripcion: Optional[str]
    class Config:
        orm_mode = True


class CandidatoCreate(BaseModel):
    nombres: str
    apellidos: str
    partido_id: Optional[int] = None
    cargo_id: Optional[int] = None

class CandidatoRead(BaseModel):
    id: int
    uuid: str
    nombres: str
    apellidos: str
    partido_id: Optional[int]
    cargo_id: Optional[int]
    class Config:
        orm_mode = True


class ProcesoCreate(BaseModel):
    nombre: str
    fecha_inicio: date
    fecha_fin: date
    tipo: str
    estado: str

class ProcesoRead(BaseModel):
    id: int
    uuid: str
    nombre: str
    fecha_inicio: date
    fecha_fin: date
    tipo: str
    estado: str
    class Config:
        orm_mode = True


class EleccionCreate(BaseModel):
    proceso_id: int
    cargo_id: int
    descripcion: Optional[str] = None
    fecha: Optional[date] = None

class EleccionRead(BaseModel):
    id: int
    uuid: str
    proceso_id: int
    cargo_id: int
    descripcion: Optional[str]
    fecha: Optional[date]
    class Config:
        orm_mode = True
