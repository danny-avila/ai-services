from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from middlewares.authentication import authenticate

router = APIRouter()

class AuthRequest(BaseModel):
    secret_key: str

@router.post("/authenticate")
async def auth_endpoint(auth_request: AuthRequest) -> dict:
    secret_key = auth_request.secret_key
    is_authenticated = authenticate(secret_key)

    if is_authenticated:
        return {"status": "success", "message": "Authenticated successfully"}
    else:
        raise HTTPException(status_code=401, detail="Invalid secret key")