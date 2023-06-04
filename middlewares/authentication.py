from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "your-secret-key"

http_auth = HTTPBearer()

async def authenticate(request: Request, credentials: HTTPAuthorizationCredentials = None):
    if credentials:
        token = credentials.credentials
        if token == SECRET_KEY:
            return True
    raise HTTPException(status_code=401, detail="Invalid credentials")

async def auth_middleware(request: Request, call_next):
    credentials = None
    if "Authorization" in request.headers:
        try:
            credentials = http_auth(request)
        except HTTPException:
            pass

    if not await authenticate(request, credentials):
        raise HTTPException(status_code=401, detail="Unauthorized")

    response = await call_next(request)
    return response