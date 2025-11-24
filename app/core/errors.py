from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException

class BusinessException(Exception):
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

async def business_exception_handler(request: Request, exc: BusinessException):
    return JSONResponse(status_code=exc.code, content={"detail": exc.message})
