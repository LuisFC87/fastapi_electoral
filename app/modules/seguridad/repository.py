from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.hash import bcrypt
from app.modules.seguridad import models, schemas

class SeguridadRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # ---------- Users ----------
    async def get_user_by_username(self, username: str) -> Optional[models.User]:
        q = select(models.User).where(models.User.username == username)
        r = await self.session.execute(q)
        return r.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> Optional[models.User]:
        q = select(models.User).where(models.User.id == user_id)
        r = await self.session.execute(q)
        return r.scalar_one_or_none()

    async def list_users(self) -> List[models.User]:
        q = select(models.User)
        r = await self.session.execute(q)
        return r.scalars().all()

    async def create_user(self, payload: schemas.UserCreate) -> models.User:
        hashed = bcrypt.hash(payload.password)
        obj = models.User(username=payload.username, email=payload.email, hashed_password=hashed)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        await self.session.commit()
        return obj

    async def update_user(self, user: models.User, payload: schemas.UserUpdate) -> models.User:
        if payload.email is not None:
            user.email = payload.email
        if payload.is_active is not None:
            user.is_active = payload.is_active
        if payload.password:
            user.hashed_password = bcrypt.hash(payload.password)
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        await self.session.commit()
        return user

    async def delete_user(self, user: models.User) -> None:
        await self.session.delete(user)
        await self.session.flush()
        await self.session.commit()
        return None

    # ---------- Roles ----------
    async def create_role(self, payload: schemas.RoleCreate) -> models.Role:
        obj = models.Role(name=payload.name, description=payload.description)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        await self.session.commit()
        return obj

    async def get_role_by_id(self, role_id: int) -> Optional[models.Role]:
        q = select(models.Role).where(models.Role.id == role_id)
        r = await self.session.execute(q)
        return r.scalar_one_or_none()

    async def get_role_by_name(self, name: str) -> Optional[models.Role]:
        q = select(models.Role).where(models.Role.name == name)
        r = await self.session.execute(q)
        return r.scalar_one_or_none()

    async def list_roles(self) -> List[models.Role]:
        q = select(models.Role)
        r = await self.session.execute(q)
        return r.scalars().all()

    async def update_role(self, role: models.Role, payload: schemas.RoleUpdate) -> models.Role:
        if payload.name is not None:
            role.name = payload.name
        if payload.description is not None:
            role.description = payload.description
        self.session.add(role)
        await self.session.flush()
        await self.session.refresh(role)
        await self.session.commit()
        return role

    async def delete_role(self, role: models.Role) -> None:
        await self.session.delete(role)
        await self.session.flush()
        await self.session.commit()
        return None

    # ---------- Role assignment ----------
    async def assign_role_to_user(self, user: models.User, role: models.Role) -> models.User:
        if role not in user.roles:
            user.roles.append(role)
            self.session.add(user)
            await self.session.flush()
            await self.session.refresh(user)
            await self.session.commit()
        return user

    async def remove_role_from_user(self, user: models.User, role: models.Role) -> models.User:
        if role in user.roles:
            user.roles.remove(role)
            self.session.add(user)
            await self.session.flush()
            await self.session.refresh(user)
            await self.session.commit()
        return user
