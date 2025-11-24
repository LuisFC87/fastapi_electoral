from fastapi import APIRouter
import importlib

ROUTE_PREFIX = "/api/v1/elecciones"

router = APIRouter()

# include submodule routers under the desired subpaths
try:
    mod_geo = importlib.import_module("app.modules.elecciones_organizacion.geografia_electoral.endpoints")
    geo_router = getattr(mod_geo, "router", None)
    if geo_router is not None:
        router.include_router(geo_router, prefix="/geografia", tags=["geografia_electoral"])
except Exception:
    pass

try:
    mod_org = importlib.import_module("app.modules.elecciones_organizacion.organizacion_electoral.endpoints")
    org_router = getattr(mod_org, "router", None)
    if org_router is not None:
        router.include_router(org_router, prefix="/organizacion", tags=["organizacion_electoral"])
except Exception:
    pass
