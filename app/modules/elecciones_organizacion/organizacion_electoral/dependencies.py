from fastapi import Depends
from app.shared.dependencies import get_db
from app.modules.elecciones_organizacion.organizacion_electoral.repository import OrgRepository
from app.modules.elecciones_organizacion.organizacion_electoral.services import OrgService

async def get_org_repository(db=Depends(get_db)):
    return OrgRepository(db)

async def get_org_service(repo=Depends(get_org_repository), db=Depends(get_db)):
    return OrgService(repo, db)
