# middlewares\authentication.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

SECRET_KEY = "your-secret-key"

async def authenticate(request: Request):
    if "x-api-key" in request.headers and request.headers["x-api-key"] == SECRET_KEY:
        return True
    else:
        raise HTTPException(status_code=401, detail="Invalid API key")

class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not await authenticate(request):
            raise HTTPException(status_code=401, detail="Unauthorized")

        response = await call_next(request)
        return response