from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict
from services.ai_services import ask_question, analyze_sentiment
from middlewares.authentication import authenticate

router = APIRouter()

class RequestPayload(BaseModel):
    service: str
    input: str
    envs: Dict[str, str]

class ApiResponse(BaseModel):
    result: str
    error: str
    stdout: str

@router.post("/ask", response_model=ApiResponse)
async def ask(payload: RequestPayload, token: str = Depends(authenticate)):
    try:
        service = payload.service.lower()
        input_text = payload.input
        envs = payload.envs

        if service == "q&a":
            result, stdout = await ask_question(input_text, envs)
        elif service == "sentiment_analysis":
            result, stdout = await analyze_sentiment(input_text, envs)
        else:
            raise ValueError("Invalid service requested")

        return ApiResponse(result=result, error="", stdout=stdout)

    except Exception as e:
        return ApiResponse(result="", error=str(e), stdout="")

@router.post("/sentiment_analysis", response_model=ApiResponse)
async def sentiment_analysis(payload: RequestPayload, token: str = Depends(authenticate)):
    try:
        input_text = payload.input
        envs = payload.envs
        result, stdout = await analyze_sentiment(input_text, envs)
        return ApiResponse(result=result, error="", stdout=stdout)

    except Exception as e:
        return ApiResponse(result="", error=str(e), stdout="")