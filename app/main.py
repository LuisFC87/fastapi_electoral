from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging import setup_logging
from app.core.config import settings
from app.core.errors import http_exception_handler, business_exception_handler, BusinessException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.middleware import AuditMiddleware
import importlib, pkgutil


def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(title=settings.APP_NAME)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(o) for o in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # register audit middleware
    # app.add_middleware(AuditMiddleware)  # Commented out until DB is available

    # dynamic router discovery
    try:
        package = importlib.import_module('app.modules')
        for finder, name, ispkg in pkgutil.iter_modules(package.__path__):
            full_mod = f"app.modules.{name}"
            try:
                mod = importlib.import_module(full_mod + '.endpoints')
                router = getattr(mod, 'router', None)
                if router is not None:
                    prefix = getattr(mod, 'ROUTE_PREFIX', None) or f"/api/v1/{name}"
                    app.include_router(router, prefix=prefix, tags=[name])
            except Exception:
                continue
    except Exception:
        pass

    from fastapi import HTTPException
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(BusinessException, business_exception_handler)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return JSONResponse(status_code=422, content={"detail": exc.errors()})

    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    return app

app = create_app()
