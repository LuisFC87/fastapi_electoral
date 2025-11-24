from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, DateTime, func
import uuid
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class BaseMixin:
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
