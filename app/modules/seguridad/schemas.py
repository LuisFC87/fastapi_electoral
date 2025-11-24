from pydantic import BaseModel, EmailStr
from typing import Optional, List

class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class RoleRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    email: Optional[EmailStr]
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None  # if provided, will be hashed

class UserRead(BaseModel):
    id: int
    uuid: str
    username: str
    email: Optional[EmailStr]
    is_active: bool
    roles: Optional[List[RoleRead]] = []
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: Optional[str] = None
