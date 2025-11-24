from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.elecciones_organizacion.organizacion_electoral import models
from app.modules.elecciones_organizacion.organizacion_electoral import schemas

class OrgRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_partido(self, payload: schemas.PartidoCreate) -> models.Partido:
        obj = models.Partido(nombre=payload.nombre, sigla=payload.sigla)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def list_partidos(self) -> List[models.Partido]:
        q = select(models.Partido)
        r = await self.session.execute(q)
        return r.scalars().all()

    async def get_partido_by_id(self, partido_id: int) -> models.Partido:
        q = select(models.Partido).where(models.Partido.id == partido_id)
        r = await self.session.execute(q)
        return r.scalar_one_or_none()

    # Cargos
    async def create_cargo(self, payload: schemas.CargoCreate) -> models.Cargo:
        obj = models.Cargo(nombre=payload.nombre, descripcion=payload.descripcion)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def list_cargos(self) -> List[models.Cargo]:
        q = select(models.Cargo)
        r = await self.session.execute(q)
        return r.scalars().all()

    async def get_cargo_by_id(self, cargo_id: int) -> models.Cargo:
        q = select(models.Cargo).where(models.Cargo.id == cargo_id)
        r = await self.session.execute(q)
        return r.scalar_one_or_none()

    # Candidatos
    async def create_candidato(self, payload: schemas.CandidatoCreate) -> models.Candidato:
        obj = models.Candidato(nombres=payload.nombres, apellidos=payload.apellidos,
                               partido_id=payload.partido_id, cargo_id=payload.cargo_id)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def list_candidatos(self) -> List[models.Candidato]:
        q = select(models.Candidato)
        r = await self.session.execute(q)
        return r.scalars().all()

    async def get_candidato_by_id(self, candidato_id: int) -> models.Candidato:
        q = select(models.Candidato).where(models.Candidato.id == candidato_id)
        r = await self.session.execute(q)
        return r.scalar_one_or_none()

    # Procesos
    async def create_proceso(self, payload: schemas.ProcesoCreate) -> models.Proceso:
        obj = models.Proceso(nombre=payload.nombre, fecha_inicio=payload.fecha_inicio,
                             fecha_fin=payload.fecha_fin, tipo=payload.tipo, estado=payload.estado)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def list_procesos(self) -> List[models.Proceso]:
        q = select(models.Proceso)
        r = await self.session.execute(q)
        return r.scalars().all()

    async def get_proceso_by_id(self, proceso_id: int) -> models.Proceso:
        q = select(models.Proceso).where(models.Proceso.id == proceso_id)
        r = await self.session.execute(q)
        return r.scalar_one_or_none()

    # Elecciones
    async def create_eleccion(self, payload: schemas.EleccionCreate) -> models.Eleccion:
        obj = models.Eleccion(proceso_id=payload.proceso_id, cargo_id=payload.cargo_id,
                              descripcion=payload.descripcion, fecha=payload.fecha)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def list_elecciones(self) -> List[models.Eleccion]:
        q = select(models.Eleccion)
        r = await self.session.execute(q)
        return r.scalars().all()

    async def get_eleccion_by_id(self, eleccion_id: int) -> models.Eleccion:
        q = select(models.Eleccion).where(models.Eleccion.id == eleccion_id)
        r = await self.session.execute(q)
        return r.scalar_one_or_none()
