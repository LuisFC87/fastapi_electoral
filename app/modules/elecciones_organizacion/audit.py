from sqlalchemy import Column, Integer, String, DateTime, func
from app.shared.base import Base

class AuditEvent(Base):
    __tablename__ = 'audit_events'
    id = Column(Integer, primary_key=True)
    actor = Column(String(255))
    action = Column(String(255))
    resource = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
