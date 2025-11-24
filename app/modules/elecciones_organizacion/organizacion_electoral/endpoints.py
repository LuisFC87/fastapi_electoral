from fastapi import APIRouter, Depends, HTTPException
from app.modules.elecciones_organizacion.organizacion_electoral import schemas
from app.modules.elecciones_organizacion.organizacion_electoral.dependencies import get_org_service
from app.core.errors import BusinessException

router = APIRouter()

@router.post("/partidos", response_model=schemas.PartidoRead, summary="Crear partido")
async def create_partido(payload: schemas.PartidoCreate, service=Depends(get_org_service)):
    try:
        return await service.create_partido(payload)
    except BusinessException as e:
        raise HTTPException(status_code=e.code, detail=e.message)

@router.get("/partidos", response_model=list[schemas.PartidoRead], summary="Listar partidos")
async def list_partidos(service=Depends(get_org_service)):
    return await service.list_partidos()


@router.get("/partidos/{partido_id}", response_model=schemas.PartidoRead, summary="Obtener partido")
async def get_partido(partido_id: int, service=Depends(get_org_service)):
    obj = await service.get_partido(partido_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return obj

# Cargos
@router.post("/cargos", response_model=schemas.CargoRead, summary="Crear cargo")
async def create_cargo(payload: schemas.CargoCreate, service=Depends(get_org_service)):
    try:
        return await service.create_cargo(payload)
    except BusinessException as e:
        raise HTTPException(status_code=e.code, detail=e.message)

@router.get("/cargos", response_model=list[schemas.CargoRead], summary="Listar cargos")
async def list_cargos(service=Depends(get_org_service)):
    return await service.list_cargos()

@router.get("/cargos/{cargo_id}", response_model=schemas.CargoRead, summary="Obtener cargo")
async def get_cargo(cargo_id: int, service=Depends(get_org_service)):
    obj = await service.get_cargo(cargo_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Cargo no encontrado")
    return obj

# Candidatos
@router.post("/candidatos", response_model=schemas.CandidatoRead, summary="Crear candidato")
async def create_candidato(payload: schemas.CandidatoCreate, service=Depends(get_org_service)):
    try:
        return await service.create_candidato(payload)
    except BusinessException as e:
        raise HTTPException(status_code=e.code, detail=e.message)

@router.get("/candidatos", response_model=list[schemas.CandidatoRead], summary="Listar candidatos")
async def list_candidatos(service=Depends(get_org_service)):
    return await service.list_candidatos()

@router.get("/candidatos/{candidato_id}", response_model=schemas.CandidatoRead, summary="Obtener candidato")
async def get_candidato(candidato_id: int, service=Depends(get_org_service)):
    obj = await service.get_candidato(candidato_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    return obj

# Procesos
@router.post("/procesos", response_model=schemas.ProcesoRead, summary="Crear proceso")
async def create_proceso(payload: schemas.ProcesoCreate, service=Depends(get_org_service)):
    try:
        return await service.create_proceso(payload)
    except BusinessException as e:
        raise HTTPException(status_code=e.code, detail=e.message)

@router.get("/procesos", response_model=list[schemas.ProcesoRead], summary="Listar procesos")
async def list_procesos(service=Depends(get_org_service)):
    return await service.list_procesos()

@router.get("/procesos/{proceso_id}", response_model=schemas.ProcesoRead, summary="Obtener proceso")
async def get_proceso(proceso_id: int, service=Depends(get_org_service)):
    obj = await service.get_proceso(proceso_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    return obj

# Elecciones
@router.post("/elecciones", response_model=schemas.EleccionRead, summary="Crear elección")
async def create_eleccion(payload: schemas.EleccionCreate, service=Depends(get_org_service)):
    try:
        return await service.create_eleccion(payload)
    except BusinessException as e:
        raise HTTPException(status_code=e.code, detail=e.message)

@router.get("/elecciones", response_model=list[schemas.EleccionRead], summary="Listar elecciones")
async def list_elecciones(service=Depends(get_org_service)):
    return await service.list_elecciones()

@router.get("/elecciones/{eleccion_id}", response_model=schemas.EleccionRead, summary="Obtener elección")
async def get_eleccion(eleccion_id: int, service=Depends(get_org_service)):
    obj = await service.get_eleccion(eleccion_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Elección no encontrada")
    return obj
