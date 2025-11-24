from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.elecciones_organizacion.geografia_electoral import models
from app.modules.elecciones_organizacion.geografia_electoral import schemas

class GeoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_pais(self, payload: schemas.PaisCreate) -> models.Pais:
        obj = models.Pais(nombre=payload.nombre)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def list_paises(self) -> List[models.Pais]:
        q = select(models.Pais)
        r = await self.session.execute(q)
        return r.scalars().all()

    async def get_pais_by_id(self, pais_id: int) -> Optional[models.Pais]:
        q = select(models.Pais).where(models.Pais.id == pais_id)
        r = await self.session.execute(q)
        return r.scalar_one_or_none()

    # Departamento
    async def create_departamento(self, payload: schemas.DepartamentoCreate) -> models.Departamento:
        obj = models.Departamento(nombre=payload.nombre, pais_id=payload.pais_id)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def list_departamentos(self) -> List[models.Departamento]:
        q = select(models.Departamento)
        r = await self.session.execute(q)
        return r.scalars().all()

    async def get_departamento_by_id(self, departamento_id: int) -> Optional[models.Departamento]:
        q = select(models.Departamento).where(models.Departamento.id == departamento_id)
        r = await self.session.execute(q)
        return r.scalar_one_or_none()

    # Provincia
    async def create_provincia(self, payload: schemas.ProvinciaCreate) -> models.Provincia:
        obj = models.Provincia(nombre=payload.nombre, departamento_id=payload.departamento_id)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def list_provincias(self) -> List[models.Provincia]:
        q = select(models.Provincia)
        r = await self.session.execute(q)
        return r.scalars().all()

    async def get_provincia_by_id(self, provincia_id: int) -> Optional[models.Provincia]:
        q = select(models.Provincia).where(models.Provincia.id == provincia_id)
        r = await self.session.execute(q)
        return r.scalar_one_or_none()

    # Municipio
    async def create_municipio(self, payload: schemas.MunicipioCreate) -> models.Municipio:
        obj = models.Municipio(nombre=payload.nombre, provincia_id=payload.provincia_id)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def list_municipios(self) -> List[models.Municipio]:
        q = select(models.Municipio)
        r = await self.session.execute(q)
        return r.scalars().all()

    async def get_municipio_by_id(self, municipio_id: int) -> Optional[models.Municipio]:
        q = select(models.Municipio).where(models.Municipio.id == municipio_id)
        r = await self.session.execute(q)
        return r.scalar_one_or_none()

    # Localidad
    async def create_localidad(self, payload: schemas.LocalidadCreate) -> models.Localidad:
        obj = models.Localidad(nombre=payload.nombre, municipio_id=payload.municipio_id)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def list_localidades(self) -> List[models.Localidad]:
        q = select(models.Localidad)
        r = await self.session.execute(q)
        return r.scalars().all()

    async def get_localidad_by_id(self, localidad_id: int) -> Optional[models.Localidad]:
        q = select(models.Localidad).where(models.Localidad.id == localidad_id)
        r = await self.session.execute(q)
        return r.scalar_one_or_none()

    # Recinto
    async def create_recinto(self, payload: schemas.RecintoCreate) -> models.Recinto:
        obj = models.Recinto(nombre=payload.nombre, localidad_id=payload.localidad_id)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def list_recintos(self) -> List[models.Recinto]:
        q = select(models.Recinto)
        r = await self.session.execute(q)
        return r.scalars().all()

    async def get_recinto_by_id(self, recinto_id: int) -> Optional[models.Recinto]:
        q = select(models.Recinto).where(models.Recinto.id == recinto_id)
        r = await self.session.execute(q)
        return r.scalar_one_or_none()

    # Mesa
    async def create_mesa(self, payload: schemas.MesaCreate) -> models.Mesa:
        obj = models.Mesa(numero=payload.numero, recinto_id=payload.recinto_id, habilitada=payload.habilitada)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def list_mesas(self) -> List[models.Mesa]:
        q = select(models.Mesa)
        r = await self.session.execute(q)
        return r.scalars().all()

    async def get_mesa_by_id(self, mesa_id: int) -> Optional[models.Mesa]:
        q = select(models.Mesa).where(models.Mesa.id == mesa_id)
        r = await self.session.execute(q)
        return r.scalar_one_or_none()
