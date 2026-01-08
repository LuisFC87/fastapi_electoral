from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ActaUploadResponse(BaseModel):
    id: int
    status: str
    idempotency_key: Optional[str]
    checksum: str
    imagen_url: str
    created_at: datetime

class ActaRawRead(BaseModel):
    id: int
    numero: Optional[str]
    codigo_unico: Optional[str]
    imagen_url: str
    checksum: str
    mesa_id: int
    proceso_id: int
    status: str
    idempotency_key: Optional[str]
    created_at: datetime
    class Config:
        orm_mode = True

class ActaProcessedRead(BaseModel):
    id: int
    acta_raw_id: int
    processed_at: datetime
    processor: Optional[str]
    validated: bool
    version: int
    class Config:
        orm_mode = True

class ResultadoItem(BaseModel):
    candidato_id: Optional[int]
    partido_id: Optional[int]
    votos: int

class ResultadosCreate(BaseModel):
    acta_processed_id: int
    resultados: List[ResultadoItem]

class ValidatePayload(BaseModel):
    validated: bool
    corrections: Optional[List[ResultadoItem]] = None
    comment: Optional[str] = None

class AggregateResponse(BaseModel):
    totals: dict
    by_party: List[dict]
