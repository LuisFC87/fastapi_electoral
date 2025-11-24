from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.shared.base import Base, BaseMixin

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)

class User(Base, BaseMixin):
    __tablename__ = "users"
    username = Column(String(150), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    roles = relationship("Role", secondary=user_roles, back_populates="users")

class Role(Base, BaseMixin):
    __tablename__ = "roles"
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    users = relationship("User", secondary=user_roles, back_populates="roles")
