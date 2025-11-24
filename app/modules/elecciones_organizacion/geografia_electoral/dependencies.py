from fastapi import Depends
from app.shared.dependencies import get_db
from app.modules.elecciones_organizacion.geografia_electoral.repository import GeoRepository
from app.modules.elecciones_organizacion.geografia_electoral.services import GeoService

async def get_geo_repository(db=Depends(get_db)):
    return GeoRepository(db)

async def get_geo_service(repo=Depends(get_geo_repository), db=Depends(get_db)):
    return GeoService(repo, db)
