# main.py
import openai
from logger import logger
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from routes.ai_utilities import ai_utilities_router
from middlewares.authentication import AuthenticationMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    logger.info("Shutting down...")
    logger.info("Closing OpenAI AIO session...")
    await openai.aiosession.get().close()

app = FastAPI(lifespan=lifespan)

app.include_router(ai_utilities_router, prefix="/ai")

app.add_middleware(AuthenticationMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info")