from app.modules.seguridad.repository import SeguridadRepository
from app.core.errors import BusinessException
from app.core.security import create_access_token, verify_password
from datetime import timedelta

class SeguridadService:
    def __init__(self, repo: SeguridadRepository, db):
        self.repo = repo
        self.db = db

    # ----- auth / normal -----
    async def register_user(self, payload):
        existing = await self.repo.get_user_by_username(payload.username)
        if existing:
            raise BusinessException("Usuario ya existe", code=400)
        user = await self.repo.create_user(payload)
        return user

    async def authenticate_user(self, username: str, password: str):
        user = await self.repo.get_user_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    async def create_token_for_user(self, user, expires_minutes: int = 60):
        token = create_access_token(subject=str(user.id), expires_minutes=expires_minutes)
        return token

    # ----- admin / management -----
    async def list_users(self):
        return await self.repo.list_users()

    async def get_user(self, user_id: int):
        user = await self.repo.get_user_by_id(user_id)
        if not user:
            raise BusinessException("Usuario no encontrado", code=404)
        return user

    async def update_user(self, user_id: int, payload):
        user = await self.get_user(user_id)
        return await self.repo.update_user(user, payload)

    async def delete_user(self, user_id: int):
        user = await self.get_user(user_id)
        await self.repo.delete_user(user)
        return None

    async def list_roles(self):
        return await self.repo.list_roles()

    async def create_role(self, payload):
        existing = await self.repo.get_role_by_name(payload.name)
        if existing:
            raise BusinessException("Rol ya existe", code=400)
        return await self.repo.create_role(payload)

    async def get_role(self, role_id: int):
        role = await self.repo.get_role_by_id(role_id)
        if not role:
            raise BusinessException("Rol no encontrado", code=404)
        return role

    async def update_role(self, role_id: int, payload):
        role = await self.get_role(role_id)
        return await self.repo.update_role(role, payload)

    async def delete_role(self, role_id: int):
        role = await self.get_role(role_id)
        await self.repo.delete_role(role)
        return None

    async def assign_role(self, user_id: int, role_id: int):
        user = await self.get_user(user_id)
        role = await self.get_role(role_id)
        return await self.repo.assign_role_to_user(user, role)

    async def remove_role(self, user_id: int, role_id: int):
        user = await self.get_user(user_id)
        role = await self.get_role(role_id)
        return await self.repo.remove_role_from_user(user, role)
