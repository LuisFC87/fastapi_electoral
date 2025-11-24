from typing import List, Optional
from app.modules.elecciones_organizacion.geografia_electoral.repository import GeoRepository
from app.modules.elecciones_organizacion.geografia_electoral import models, schemas
from app.core.errors import BusinessException


class GeoService:
    def __init__(self, repo: GeoRepository, db):
        self.repo = repo
        self.db = db

    # Paises
    async def create_pais(self, payload: schemas.PaisCreate) -> models.Pais:
        existing = await self.repo.list_paises()
        if any(p.nombre.lower() == payload.nombre.lower() for p in existing):
            raise BusinessException(code=400, message=f"País ya existe: {payload.nombre}")
        return await self.repo.create_pais(payload)

    async def list_paises(self) -> List[models.Pais]:
        return await self.repo.list_paises()

    async def get_pais(self, pais_id: int) -> Optional[models.Pais]:
        return await self.repo.get_pais_by_id(pais_id)

    # Departamentos
    async def create_departamento(self, payload: schemas.DepartamentoCreate) -> models.Departamento:
        pais = await self.repo.get_pais_by_id(payload.pais_id)
        if not pais:
            raise BusinessException(code=400, message="País referenciado no existe")
        # avoid duplicate name in same country
        existing = await self.repo.list_departamentos()
        if any(d.nombre.lower() == payload.nombre.lower() and d.pais_id == payload.pais_id for d in existing):
            raise BusinessException(code=400, message="Departamento ya existe en ese país")
        return await self.repo.create_departamento(payload)

    async def list_departamentos(self) -> List[models.Departamento]:
        return await self.repo.list_departamentos()

    async def get_departamento(self, departamento_id: int) -> Optional[models.Departamento]:
        return await self.repo.get_departamento_by_id(departamento_id)

    # Provincias
    async def create_provincia(self, payload: schemas.ProvinciaCreate) -> models.Provincia:
        dept = await self.repo.get_departamento_by_id(payload.departamento_id)
        if not dept:
            raise BusinessException(code=400, message="Departamento referenciado no existe")
        existing = await self.repo.list_provincias()
        if any(p.nombre.lower() == payload.nombre.lower() and p.departamento_id == payload.departamento_id for p in existing):
            raise BusinessException(code=400, message="Provincia ya existe en ese departamento")
        return await self.repo.create_provincia(payload)

    async def list_provincias(self) -> List[models.Provincia]:
        return await self.repo.list_provincias()

    async def get_provincia(self, provincia_id: int) -> Optional[models.Provincia]:
        return await self.repo.get_provincia_by_id(provincia_id)

    # Municipios
    async def create_municipio(self, payload: schemas.MunicipioCreate) -> models.Municipio:
        prov = await self.repo.get_provincia_by_id(payload.provincia_id)
        if not prov:
            raise BusinessException(code=400, message="Provincia referenciada no existe")
        existing = await self.repo.list_municipios()
        if any(m.nombre.lower() == payload.nombre.lower() and m.provincia_id == payload.provincia_id for m in existing):
            raise BusinessException(code=400, message="Municipio ya existe en esa provincia")
        return await self.repo.create_municipio(payload)

    async def list_municipios(self) -> List[models.Municipio]:
        return await self.repo.list_municipios()

    async def get_municipio(self, municipio_id: int) -> Optional[models.Municipio]:
        return await self.repo.get_municipio_by_id(municipio_id)

    # Localidades
    async def create_localidad(self, payload: schemas.LocalidadCreate) -> models.Localidad:
        mun = await self.repo.get_municipio_by_id(payload.municipio_id)
        if not mun:
            raise BusinessException(code=400, message="Municipio referenciado no existe")
        existing = await self.repo.list_localidades()
        if any(l.nombre.lower() == payload.nombre.lower() and l.municipio_id == payload.municipio_id for l in existing):
            raise BusinessException(code=400, message="Localidad ya existe en ese municipio")
        return await self.repo.create_localidad(payload)

    async def list_localidades(self) -> List[models.Localidad]:
        return await self.repo.list_localidades()

    async def get_localidad(self, localidad_id: int) -> Optional[models.Localidad]:
        return await self.repo.get_localidad_by_id(localidad_id)

    # Recintos
    async def create_recinto(self, payload: schemas.RecintoCreate) -> models.Recinto:
        loc = await self.repo.get_localidad_by_id(payload.localidad_id)
        if not loc:
            raise BusinessException(code=400, message="Localidad referenciada no existe")
        return await self.repo.create_recinto(payload)

    async def list_recintos(self) -> List[models.Recinto]:
        return await self.repo.list_recintos()

    async def get_recinto(self, recinto_id: int) -> Optional[models.Recinto]:
        return await self.repo.get_recinto_by_id(recinto_id)

    # Mesas
    async def create_mesa(self, payload: schemas.MesaCreate) -> models.Mesa:
        rec = await self.repo.get_recinto_by_id(payload.recinto_id)
        if not rec:
            raise BusinessException(code=400, message="Recinto referenciado no existe")
        # enforce unique number per recinto via DB constraint; service does not duplicate-check here
        return await self.repo.create_mesa(payload)

    async def list_mesas(self) -> List[models.Mesa]:
        return await self.repo.list_mesas()

    async def get_mesa(self, mesa_id: int) -> Optional[models.Mesa]:
        return await self.repo.get_mesa_by_id(mesa_id)
