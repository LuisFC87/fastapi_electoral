from sqlalchemy import Column, Integer, String, DateTime, JSON, func
from app.shared.base import Base

class AuditEvent(Base):
    __tablename__ = "audit_events"
    id = Column(Integer, primary_key=True)
    actor = Column(String(255), nullable=True)
    action = Column(String(255), nullable=False)
    resource = Column(String(255), nullable=True)
    meta = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
