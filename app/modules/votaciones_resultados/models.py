from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, JSON, DateTime, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.shared.base import Base, BaseMixin

class ActaRaw(Base, BaseMixin):
    __tablename__ = "actas_raw"
    numero = Column(String(100), nullable=True)
    codigo_unico = Column(String(255), nullable=True)
    imagen_url = Column(Text, nullable=False)
    checksum = Column(String(128), nullable=False, index=True)
    mesa_id = Column(Integer, ForeignKey("mesas.id"), nullable=False)
    proceso_id = Column(Integer, ForeignKey("procesos.id"), nullable=False)
    uploaded_by = Column(Integer, nullable=True)
    status = Column(String(30), nullable=False, default='CARGADA')
    idempotency_key = Column(String(255), nullable=True)
    origen = Column(String(50), default="UPLOAD")
    __table_args__ = (UniqueConstraint('proceso_id', 'mesa_id', 'idempotency_key', name='uq_acta_idempotency'), )
    processed_versions = relationship("ActaProcessed", back_populates="raw_acta")

class ActaProcessed(Base, BaseMixin):
    __tablename__ = "actas_processed"
    acta_raw_id = Column(Integer, ForeignKey("actas_raw.id"), nullable=False)
    processed_at = Column(DateTime(timezone=True), server_default=func.now())
    processor = Column(String(100), nullable=True)
    ocr_json = Column(JSONB, nullable=True)
    validated = Column(Boolean, default=False)
    version = Column(Integer, default=1)
    raw_acta = relationship("ActaRaw", back_populates="processed_versions")
    resultados = relationship("Resultado", back_populates="processed")

class Resultado(Base, BaseMixin):
    __tablename__ = "resultados"
    acta_processed_id = Column(Integer, ForeignKey("actas_processed.id"), nullable=False)
    candidato_id = Column(Integer, ForeignKey("candidatos.id"), nullable=True)
    partido_id = Column(Integer, ForeignKey("partidos.id"), nullable=True)
    votos = Column(Integer, nullable=False, default=0)
    processed = relationship("ActaProcessed", back_populates="resultados", uselist=False)

class ResultadosPorCargo(Base, BaseMixin):
    __tablename__ = "resultados_por_cargo"
    acta_processed_id = Column(Integer, ForeignKey("actas_processed.id"), nullable=False)
    cargo_id = Column(Integer, ForeignKey("cargos.id"), nullable=False)
    partido_id = Column(Integer, ForeignKey("partidos.id"), nullable=True)
    votos_validos = Column(Integer, default=0)
    votos_blancos = Column(Integer, default=0)
    votos_nulos = Column(Integer, default=0)
    votos_observados = Column(Integer, default=0)
    proceso_id = Column(Integer, ForeignKey("procesos.id"), nullable=False)
    verificado = Column(Boolean, default=False)
    version = Column(Integer, default=1)
    __table_args__ = (UniqueConstraint('acta_processed_id', 'cargo_id', 'partido_id', 'version', name='uq_res_cargo_version'), )

class ValidacionActa(Base, BaseMixin):
    __tablename__ = "validaciones_actas"
    acta_id = Column(Integer, ForeignKey("actas_raw.id"), nullable=False)
    regla = Column(String(100), nullable=False)
    resultado = Column(Boolean, nullable=False)
    mensaje = Column(Text, nullable=True)
    nivel = Column(String(20), default="ERROR")
    usuario_id = Column(Integer, nullable=True)

class ErrorProcesamiento(Base, BaseMixin):
    __tablename__ = "errores_procesamiento"
    acta_id = Column(Integer, ForeignKey("actas_raw.id"), nullable=True)
    tipo = Column(String(50))
    mensaje = Column(Text)
    detalles = Column(JSONB)
