from fastapi import FastAPI
from contextlib import asynccontextmanager
import httpx
from .routes.chat_router import chat
from .routes.dictionary_router import dictionary
from .routes.dialog_router import dialog
import logging
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
    version="1.0.0"#,
    #lifespan=lifespan
)

logger = logging.getLogger("uvicorn.error")  #
# Register routers
app.include_router(chat,prefix="/api/v1", tags=["Chat"])
#app.include_router(moderation, prefix="/api/v1", tags=["Moderation"])
app.include_router(dictionary, prefix="/api/v1", tags=["Dictionary"])
app.include_router(dialog, prefix="/api/v1", tags=["Dialogue"])