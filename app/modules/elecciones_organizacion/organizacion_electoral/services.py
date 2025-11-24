from typing import List, Optional
from app.modules.elecciones_organizacion.organizacion_electoral.repository import OrgRepository
from app.modules.elecciones_organizacion.organizacion_electoral import models, schemas
from app.core.errors import BusinessException


class OrgService:
    def __init__(self, repo: OrgRepository, db):
        self.repo = repo
        self.db = db

    # Partidos
    async def create_partido(self, payload: schemas.PartidoCreate) -> models.Partido:
        existing = await self.repo.list_partidos()
        if any(p.nombre.lower() == payload.nombre.lower() for p in existing):
            raise BusinessException(code=400, message=f"Partido ya existe: {payload.nombre}")
        if any(p.sigla.lower() == payload.sigla.lower() for p in existing):
            raise BusinessException(code=400, message=f"Sigla ya registrada: {payload.sigla}")
        return await self.repo.create_partido(payload)

    async def list_partidos(self) -> List[models.Partido]:
        return await self.repo.list_partidos()

    async def get_partido(self, partido_id: int) -> Optional[models.Partido]:
        return await self.repo.get_partido_by_id(partido_id)

    # Cargos
    async def create_cargo(self, payload: schemas.CargoCreate) -> models.Cargo:
        # simple duplicate check by name
        existing = await self.repo.list_cargos()
        if any(c.nombre.lower() == payload.nombre.lower() for c in existing):
            raise BusinessException(code=400, message="Cargo ya existe")
        return await self.repo.create_cargo(payload)

    async def list_cargos(self) -> List[models.Cargo]:
        return await self.repo.list_cargos()

    async def get_cargo(self, cargo_id: int) -> Optional[models.Cargo]:
        return await self.repo.get_cargo_by_id(cargo_id)

    # Candidatos
    async def create_candidato(self, payload: schemas.CandidatoCreate) -> models.Candidato:
        # validate FK partido and cargo if provided
        if payload.partido_id:
            partido = await self.repo.get_partido_by_id(payload.partido_id)
            if not partido:
                raise BusinessException(code=400, message="Partido referenciado no existe")
        if payload.cargo_id:
            cargo = await self.repo.get_cargo_by_id(payload.cargo_id)
            if not cargo:
                raise BusinessException(code=400, message="Cargo referenciado no existe")
        return await self.repo.create_candidato(payload)

    async def list_candidatos(self) -> List[models.Candidato]:
        return await self.repo.list_candidatos()

    async def get_candidato(self, candidato_id: int) -> Optional[models.Candidato]:
        return await self.repo.get_candidato_by_id(candidato_id)

    # Procesos
    async def create_proceso(self, payload: schemas.ProcesoCreate) -> models.Proceso:
        return await self.repo.create_proceso(payload)

    async def list_procesos(self) -> List[models.Proceso]:
        return await self.repo.list_procesos()

    async def get_proceso(self, proceso_id: int) -> Optional[models.Proceso]:
        return await self.repo.get_proceso_by_id(proceso_id)

    # Elecciones
    async def create_eleccion(self, payload: schemas.EleccionCreate) -> models.Eleccion:
        # validate FK proceso and cargo
        proceso = await self.repo.get_proceso_by_id(payload.proceso_id)
        if not proceso:
            raise BusinessException(code=400, message="Proceso referenciado no existe")
        cargo = await self.repo.get_cargo_by_id(payload.cargo_id)
        if not cargo:
            raise BusinessException(code=400, message="Cargo referenciado no existe")
        return await self.repo.create_eleccion(payload)

    async def list_elecciones(self) -> List[models.Eleccion]:
        return await self.repo.list_elecciones()

    async def get_eleccion(self, eleccion_id: int) -> Optional[models.Eleccion]:
        return await self.repo.get_eleccion_by_id(eleccion_id)
