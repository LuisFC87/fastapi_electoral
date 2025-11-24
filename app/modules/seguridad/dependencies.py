from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
from app.modules.seguridad.repository import SeguridadRepository
from app.modules.seguridad.services import SeguridadService
from app.shared.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/seguridad/token")

async def get_seg_repository(db=Depends(get_db)):
    return SeguridadRepository(db)

async def get_seg_service(repo: SeguridadRepository = Depends(get_seg_repository), db: AsyncSession = Depends(get_db)):
    return SeguridadService(repo, db)

async def get_current_user(request: Request, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    """Decodifica token, obtiene usuario y setea request.state.user_username para auditoría."""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")
    user_id = payload.get("sub")
    repo = SeguridadRepository(db)
    user = await repo.get_user_by_id(int(user_id))
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autorizado")
    try:
        request.state.user_username = user.username
        request.state.user_id = str(user.id)
    except Exception:
        pass
    return user

def require_roles(*allowed_roles: str):
    async def role_checker(user=Depends(get_current_user)):
        user_role_names = {r.name for r in user.roles}
        if not set(allowed_roles).intersection(user_role_names):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
        return user
    return Depends(role_checker)
