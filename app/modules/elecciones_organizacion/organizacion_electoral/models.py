from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.shared.base import Base, BaseMixin

class Partido(Base, BaseMixin):
    __tablename__ = 'partidos'
    nombre = Column(String(255), unique=True, nullable=False)
    sigla = Column(String(100), unique=True, nullable=False)

class Cargo(Base, BaseMixin):
    __tablename__ = 'cargos'
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text)

class Candidato(Base, BaseMixin):
    __tablename__ = 'candidatos'
    nombres = Column(String(255), nullable=False)
    apellidos = Column(String(255), nullable=False)
    partido_id = Column(Integer, ForeignKey('partidos.id'))
    partido = relationship('Partido', backref='candidatos')
    cargo_id = Column(Integer, ForeignKey('cargos.id'))
    cargo = relationship('Cargo', backref='candidatos')

class Proceso(Base, BaseMixin):
    __tablename__ = 'procesos'
    nombre = Column(String(255), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    tipo = Column(String(50), nullable=False)
    estado = Column(String(50), nullable=False)

class Eleccion(Base, BaseMixin):
    __tablename__ = 'elecciones'
    proceso_id = Column(Integer, ForeignKey('procesos.id'), nullable=False)
    proceso = relationship('Proceso', backref='elecciones')
    cargo_id = Column(Integer, ForeignKey('cargos.id'), nullable=False)
    cargo = relationship('Cargo')
    descripcion = Column(Text)
    fecha = Column(Date)

#  No todos los candidatos del cargo participan en todas las elecciones
class CandidatoEleccion(Base):
    __tablename__ = 'candidatos_eleccion'
    id = Column(Integer, primary_key=True)
    candidato_id = Column(Integer, ForeignKey('candidatos.id'))
    eleccion_id = Column(Integer, ForeignKey('elecciones.id'))
