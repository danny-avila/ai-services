# routes\ai_utilities.py
import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict
from services.ai_services import AI_SERVICES
from middlewares.authentication import authenticate

ai_utilities_router = APIRouter()

class RequestPayload(BaseModel):
    service: str
    input: str
    envs: Dict[str, str]

class ApiResponse(BaseModel):
    result: str
    error: str
    stdout: str

@ai_utilities_router.post("/ask", response_model=ApiResponse)
async def ask(payload: RequestPayload, token: str = Depends(authenticate)):
    service = payload.service.lower()
    input_text = payload.input
    envs = payload.envs

    if service not in AI_SERVICES:
        raise HTTPException(status_code=400, detail="Invalid service requested")

    try:
        result = await AI_SERVICES[service](input_text, envs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if 'error' in result:
        raise HTTPException(status_code=400, detail=result['error'])

    return ApiResponse(result=result, error="", stdout="")

