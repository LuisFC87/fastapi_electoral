from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from app.shared.base import Base, BaseMixin

class Pais(Base, BaseMixin):
    __tablename__ = 'pais'
    nombre = Column(String(255), unique=True, nullable=False)

class Departamento(Base, BaseMixin):
    __tablename__ = 'departamento'
    nombre = Column(String(255), nullable=False)
    pais_id = Column(Integer, ForeignKey('pais.id'), nullable=False)
    pais = relationship('Pais', backref='departamentos')

class Provincia(Base, BaseMixin):
    __tablename__ = 'provincia'
    nombre = Column(String(255), nullable=False)
    departamento_id = Column(Integer, ForeignKey('departamento.id'), nullable=False)
    departamento = relationship('Departamento', backref='provincias')

class Municipio(Base, BaseMixin):
    __tablename__ = 'municipio'
    nombre = Column(String(255), nullable=False)
    provincia_id = Column(Integer, ForeignKey('provincia.id'), nullable=False)
    provincia = relationship('Provincia', backref='municipios')

class Localidad(Base, BaseMixin):
    __tablename__ = 'localidad'
    nombre = Column(String(255), nullable=False)
    municipio_id = Column(Integer, ForeignKey('municipio.id'), nullable=False)
    municipio = relationship('Municipio', backref='localidades')

class Recinto(Base, BaseMixin):
    __tablename__ = 'recintos'
    nombre = Column(String(255), nullable=False)
    localidad_id = Column(Integer, ForeignKey('localidad.id'), nullable=False)
    localidad = relationship('Localidad', backref='recintos')

class Mesa(Base, BaseMixin):
    __tablename__ = 'mesas'
    numero = Column(Integer, nullable=False)
    habilitada = Column(Boolean, default=True)
    recinto_id = Column(Integer, ForeignKey('recintos.id'), nullable=False)
    recinto = relationship('Recinto', backref='mesas')
    __table_args__ = (UniqueConstraint('recinto_id', 'numero', name='uq_recinto_numero'),)
