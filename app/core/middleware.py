import asyncio
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.shared.audit import AuditEvent
from app.core.database import AsyncSessionLocal

async def _write_audit(actor, action, resource, extra=None):
    async with AsyncSessionLocal() as session:
        evt = AuditEvent(actor=actor, action=action, resource=resource, meta=extra)
        session.add(evt)
        await session.commit()

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        actor = getattr(request.state, 'user_username', 'anonymous')
        action = f"{request.method} {request.url.path}"
        resource = request.url.path
        extra = {"status_code": response.status_code}
        asyncio.create_task(_write_audit(actor, action, resource, extra))
        return response
