# routes\ai_utilities.py
import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict
from services.ai_services import ask_question, sentiment_analysis
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

    if service == "q&a":
        result = ask_question(input_text, envs)
    elif service == "sentiment_analysis":
        result = sentiment_analysis(input_text, envs)
    else:
        raise HTTPException(status_code=400, detail="Invalid service requested")

    if 'error' in result:
        raise HTTPException(status_code=400, detail=result['error'])

    return ApiResponse(result=result, error="", stdout="")

@ai_utilities_router.post("/sentiment_analysis", response_model=ApiResponse)
async def sentiment_analysis_route(payload: RequestPayload, token: str = Depends(authenticate)):
    input_text = payload.input
    envs = payload.envs
    result = sentiment_analysis(input_text, envs)

    result_dict = json.loads(result)
    if 'error' in result_dict:
        raise HTTPException(status_code=400, detail=result_dict['error'])

    return ApiResponse(result=result, error="", stdout="")