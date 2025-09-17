from fastapi import FastAPI
from contextlib import asynccontextmanager
import httpx
from api.routes.chat_router import chat
from api.routes.dictionary_router import dictionary
from api.routes.dialog_router import dialog
import logging
from fastapi.middleware.cors import CORSMiddleware
# Dependency injection for HTTP client
# @asynccontextmanager
# async def lifespan(api: FastAPI):
#     api.state.http_client = httpx.AsyncClient()
#     yield
#     await api.state.http_client.aclose()


# Create FastAPI api with lifespan (dependency injection)
app = FastAPI(
    title="Chat Completion API",
    description="Service for OpenAI chat completions and moderation",
    version="1.0.0",
    #lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # <-- Change to list of allowed domains in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("uvicorn.error")  #
# Register routers
app.include_router(chat,prefix="/api/v1", tags=["Chat"])
#app.include_router(moderation, prefix="/api/v1", tags=["Moderation"])
app.include_router(dictionary, prefix="/api/v1", tags=["Dictionary"])
app.include_router(dialog, prefix="/api/v1", tags=["Dialogue"])