# main.py
import openai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.ai_utilities import ai_utilities_router
from middlewares.authentication import AuthenticationMiddleware

app = FastAPI()

app.include_router(ai_utilities_router, prefix="/ai")

app.add_middleware(AuthenticationMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_event():
    await openai.aiosession.get().close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info")