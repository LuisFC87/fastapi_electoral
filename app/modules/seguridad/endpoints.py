from fastapi import APIRouter, Depends, HTTPException, status, Form
from app.modules.seguridad import schemas
from app.modules.seguridad.dependencies import oauth2_scheme, get_seg_service, get_seg_repository, get_current_user, require_roles
from app.modules.seguridad.repository import SeguridadRepository
from app.modules.seguridad.services import SeguridadService
from app.shared.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession

ROUTE_PREFIX = "/api/v1/seguridad"
router = APIRouter()


@router.post("/token", response_model=schemas.Token, summary="Obtener token de acceso", description="Intercambia credenciales por un token JWT (grant_type=password)")
async def login_for_access_token(username: str = Form(...), password: str = Form(...), svc: SeguridadService = Depends(get_seg_service)):
    """Autentica usuario y devuelve access_token"""
    user = await svc.authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
    token = await svc.create_token_for_user(user)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register", response_model=schemas.UserRead, summary="Registrar usuario", description="Crea un nuevo usuario (retorna data sin password)")
async def register_user(payload: schemas.UserCreate, svc: SeguridadService = Depends(get_seg_service)):
    user = await svc.register_user(payload)
    return user

@router.get("/me", response_model=schemas.UserRead, summary="Perfil del usuario autenticado")
async def read_me(current_user = Depends(get_current_user)):
    return current_user

# Admin RBAC routes (admin only)
@router.post("/roles", response_model=schemas.RoleRead, dependencies=[require_roles("admin")])
async def create_role(payload: schemas.RoleCreate, svc: SeguridadService = Depends(get_seg_service)):
    try:
        return await svc.create_role(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/roles", response_model=list[schemas.RoleRead], dependencies=[require_roles("admin")])
async def list_roles(svc: SeguridadService = Depends(get_seg_service)):
    return await svc.list_roles()

@router.get("/roles/{role_id}", response_model=schemas.RoleRead, dependencies=[require_roles("admin")])
async def get_role(role_id: int, svc: SeguridadService = Depends(get_seg_service)):
    return await svc.get_role(role_id)

@router.put("/roles/{role_id}", response_model=schemas.RoleRead, dependencies=[require_roles("admin")])
async def update_role(role_id: int, payload: schemas.RoleUpdate, svc: SeguridadService = Depends(get_seg_service)):
    return await svc.update_role(role_id, payload)

@router.delete("/roles/{role_id}", status_code=204, dependencies=[require_roles("admin")])
async def delete_role(role_id: int, svc: SeguridadService = Depends(get_seg_service)):
    await svc.delete_role(role_id)
    return {}

@router.get("/users", response_model=list[schemas.UserRead], dependencies=[require_roles("admin")])
async def list_users(svc: SeguridadService = Depends(get_seg_service)):
    return await svc.list_users()

@router.get("/users/{user_id}", response_model=schemas.UserRead, dependencies=[require_roles("admin")])
async def get_user(user_id: int, svc: SeguridadService = Depends(get_seg_service)):
    return await svc.get_user(user_id)

@router.put("/users/{user_id}", response_model=schemas.UserRead, dependencies=[require_roles("admin")])
async def update_user(user_id: int, payload: schemas.UserUpdate, svc: SeguridadService = Depends(get_seg_service)):
    return await svc.update_user(user_id, payload)

@router.delete("/users/{user_id}", status_code=204, dependencies=[require_roles("admin")])
async def delete_user(user_id: int, svc: SeguridadService = Depends(get_seg_service)):
    await svc.delete_user(user_id)
    return {}

@router.post("/users/{user_id}/roles/{role_id}", response_model=schemas.UserRead, dependencies=[require_roles("admin")])
async def assign_role(user_id: int, role_id: int, svc: SeguridadService = Depends(get_seg_service)):
    return await svc.assign_role(user_id, role_id)

@router.delete("/users/{user_id}/roles/{role_id}", response_model=schemas.UserRead, dependencies=[require_roles("admin")])
async def remove_role(user_id: int, role_id: int, svc: SeguridadService = Depends(get_seg_service)):
    return await svc.remove_role(user_id, role_id)
