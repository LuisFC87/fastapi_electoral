from fastapi import APIRouter, Depends, HTTPException
from app.modules.elecciones_organizacion.geografia_electoral import schemas
from app.modules.elecciones_organizacion.geografia_electoral.dependencies import get_geo_service
from app.core.errors import BusinessException

router = APIRouter()

@router.post("/paises", response_model=schemas.PaisRead, summary="Crear país", description="Crea un nuevo país con nombre único")
async def create_pais(payload: schemas.PaisCreate, service=Depends(get_geo_service)):
    try:
        return await service.create_pais(payload)
    except BusinessException as e:
        raise HTTPException(status_code=e.code, detail=e.message)

@router.get("/paises", response_model=list[schemas.PaisRead], summary="Listar países")
async def list_paises(service=Depends(get_geo_service)):
    return await service.list_paises()


@router.get("/paises/{pais_id}", response_model=schemas.PaisRead, summary="Obtener país")
async def get_pais(pais_id: int, service=Depends(get_geo_service)):
    pais = await service.get_pais(pais_id)
    if not pais:
        raise HTTPException(status_code=404, detail="País no encontrado")
    return pais

# Departamentos
@router.post("/departamentos", response_model=schemas.DepartamentoRead, summary="Crear departamento", description="Crea un departamento asociado a un país")
async def create_departamento(payload: schemas.DepartamentoCreate, service=Depends(get_geo_service)):
    try:
        return await service.create_departamento(payload)
    except BusinessException as e:
        raise HTTPException(status_code=e.code, detail=e.message)

@router.get("/departamentos", response_model=list[schemas.DepartamentoRead], summary="Listar departamentos")
async def list_departamentos(service=Depends(get_geo_service)):
    return await service.list_departamentos()

@router.get("/departamentos/{departamento_id}", response_model=schemas.DepartamentoRead, summary="Obtener departamento")
async def get_departamento(departamento_id: int, service=Depends(get_geo_service)):
    obj = await service.get_departamento(departamento_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")
    return obj

# Provincias
@router.post("/provincias", response_model=schemas.ProvinciaRead, summary="Crear provincia")
async def create_provincia(payload: schemas.ProvinciaCreate, service=Depends(get_geo_service)):
    try:
        return await service.create_provincia(payload)
    except BusinessException as e:
        raise HTTPException(status_code=e.code, detail=e.message)

@router.get("/provincias", response_model=list[schemas.ProvinciaRead], summary="Listar provincias")
async def list_provincias(service=Depends(get_geo_service)):
    return await service.list_provincias()

@router.get("/provincias/{provincia_id}", response_model=schemas.ProvinciaRead, summary="Obtener provincia")
async def get_provincia(provincia_id: int, service=Depends(get_geo_service)):
    obj = await service.get_provincia(provincia_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")
    return obj

# Municipios
@router.post("/municipios", response_model=schemas.MunicipioRead, summary="Crear municipio")
async def create_municipio(payload: schemas.MunicipioCreate, service=Depends(get_geo_service)):
    try:
        return await service.create_municipio(payload)
    except BusinessException as e:
        raise HTTPException(status_code=e.code, detail=e.message)

@router.get("/municipios", response_model=list[schemas.MunicipioRead], summary="Listar municipios")
async def list_municipios(service=Depends(get_geo_service)):
    return await service.list_municipios()

@router.get("/municipios/{municipio_id}", response_model=schemas.MunicipioRead, summary="Obtener municipio")
async def get_municipio(municipio_id: int, service=Depends(get_geo_service)):
    obj = await service.get_municipio(municipio_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Municipio no encontrado")
    return obj

# Localidades
@router.post("/localidades", response_model=schemas.LocalidadRead, summary="Crear localidad")
async def create_localidad(payload: schemas.LocalidadCreate, service=Depends(get_geo_service)):
    try:
        return await service.create_localidad(payload)
    except BusinessException as e:
        raise HTTPException(status_code=e.code, detail=e.message)

@router.get("/localidades", response_model=list[schemas.LocalidadRead], summary="Listar localidades")
async def list_localidades(service=Depends(get_geo_service)):
    return await service.list_localidades()

@router.get("/localidades/{localidad_id}", response_model=schemas.LocalidadRead, summary="Obtener localidad")
async def get_localidad(localidad_id: int, service=Depends(get_geo_service)):
    obj = await service.get_localidad(localidad_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Localidad no encontrada")
    return obj

# Recintos
@router.post("/recintos", response_model=schemas.RecintoRead, summary="Crear recinto")
async def create_recinto(payload: schemas.RecintoCreate, service=Depends(get_geo_service)):
    try:
        return await service.create_recinto(payload)
    except BusinessException as e:
        raise HTTPException(status_code=e.code, detail=e.message)

@router.get("/recintos", response_model=list[schemas.RecintoRead], summary="Listar recintos")
async def list_recintos(service=Depends(get_geo_service)):
    return await service.list_recintos()

@router.get("/recintos/{recinto_id}", response_model=schemas.RecintoRead, summary="Obtener recinto")
async def get_recinto(recinto_id: int, service=Depends(get_geo_service)):
    obj = await service.get_recinto(recinto_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Recinto no encontrado")
    return obj

# Mesas
@router.post("/mesas", response_model=schemas.MesaRead, summary="Crear mesa")
async def create_mesa(payload: schemas.MesaCreate, service=Depends(get_geo_service)):
    try:
        return await service.create_mesa(payload)
    except BusinessException as e:
        raise HTTPException(status_code=e.code, detail=e.message)

@router.get("/mesas", response_model=list[schemas.MesaRead], summary="Listar mesas")
async def list_mesas(service=Depends(get_geo_service)):
    return await service.list_mesas()

@router.get("/mesas/{mesa_id}", response_model=schemas.MesaRead, summary="Obtener mesa")
async def get_mesa(mesa_id: int, service=Depends(get_geo_service)):
    obj = await service.get_mesa(mesa_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return obj
