from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class PaisCreate(BaseModel):
    nombre: str

class PaisRead(BaseModel):
    id: int
    uuid: UUID
    nombre: str
    class Config:
        from_attributes = True


class DepartamentoCreate(BaseModel):
    nombre: str
    pais_id: int

class DepartamentoRead(BaseModel):
    id: int
    uuid: UUID
    nombre: str
    pais_id: int
    class Config:
        from_attributes = True


class ProvinciaCreate(BaseModel):
    nombre: str
    departamento_id: int

class ProvinciaRead(BaseModel):
    id: int
    uuid: UUID
    nombre: str
    departamento_id: int
    class Config:
        from_attributes = True


class MunicipioCreate(BaseModel):
    nombre: str
    provincia_id: int

class MunicipioRead(BaseModel):
    id: int
    uuid: UUID
    nombre: str
    provincia_id: int
    class Config:
        from_attributes = True


class LocalidadCreate(BaseModel):
    nombre: str
    municipio_id: int

class LocalidadRead(BaseModel):
    id: int
    uuid: UUID
    nombre: str
    municipio_id: int
    class Config:
        from_attributes = True


class RecintoCreate(BaseModel):
    nombre: str
    localidad_id: int

class RecintoRead(BaseModel):
    id: int
    uuid: UUID
    nombre: str
    localidad_id: int
    class Config:
        from_attributes = True


class MesaCreate(BaseModel):
    numero: int
    recinto_id: int
    habilitada: Optional[bool] = True

class MesaRead(BaseModel):
    id: int
    uuid: UUID
    numero: int
    recinto_id: int
    habilitada: bool
    class Config:
        from_attributes = True
