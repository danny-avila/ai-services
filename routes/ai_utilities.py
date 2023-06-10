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

def process_result(result):
    if isinstance(result, dict):
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        stdout_dict = result.copy()
        stdout_dict.pop('output', None)
        stdout = json.dumps(stdout_dict)
        result = result.get("output", "")
    else:
        stdout = result
    return result, stdout

@ai_utilities_router.post("/ask", response_model=ApiResponse)
async def ask(payload: RequestPayload, token: str = Depends(authenticate)):
    service = payload.service.lower()
    input_text = payload.input
    envs = payload.envs

    if service not in AI_SERVICES:
        raise HTTPException(status_code=400, detail="Invalid service requested")

    try:
        result = await AI_SERVICES[service](input_text, envs)
        result, stdout = process_result(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return ApiResponse(result=result, error="", stdout=stdout)

# @ai_utilities_router.get("/plugins", response_model=ApiResponse)
# async def plugins(token: str = Depends(authenticate)):
#     try:
#         result = await load_plugins()
#         result, stdout = process_result(result)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

#     return ApiResponse(result=result, error="", stdout=stdout)

