from pydantic import BaseModel
from typing import Optional

class PaisCreate(BaseModel):
    nombre: str

class PaisRead(BaseModel):
    id: int
    uuid: str
    nombre: str
    class Config:
        orm_mode = True


class DepartamentoCreate(BaseModel):
    nombre: str
    pais_id: int

class DepartamentoRead(BaseModel):
    id: int
    uuid: str
    nombre: str
    pais_id: int
    class Config:
        orm_mode = True


class ProvinciaCreate(BaseModel):
    nombre: str
    departamento_id: int

class ProvinciaRead(BaseModel):
    id: int
    uuid: str
    nombre: str
    departamento_id: int
    class Config:
        orm_mode = True


class MunicipioCreate(BaseModel):
    nombre: str
    provincia_id: int

class MunicipioRead(BaseModel):
    id: int
    uuid: str
    nombre: str
    provincia_id: int
    class Config:
        orm_mode = True


class LocalidadCreate(BaseModel):
    nombre: str
    municipio_id: int

class LocalidadRead(BaseModel):
    id: int
    uuid: str
    nombre: str
    municipio_id: int
    class Config:
        orm_mode = True


class RecintoCreate(BaseModel):
    nombre: str
    localidad_id: int

class RecintoRead(BaseModel):
    id: int
    uuid: str
    nombre: str
    localidad_id: int
    class Config:
        orm_mode = True


class MesaCreate(BaseModel):
    numero: int
    recinto_id: int
    habilitada: Optional[bool] = True

class MesaRead(BaseModel):
    id: int
    uuid: str
    numero: int
    recinto_id: int
    habilitada: bool
    class Config:
        orm_mode = True
