from fastapi import APIRouter, Depends
from ..services.chat.chat_services import process
from ..models.completion_model import ChatRequest
from pydantic import BaseModel
from typing import Dict, Optional, Any

chat = APIRouter()
@chat.post("/chat_completions")
def completion(req: ChatRequest):
    return  process(req.user_input, req.json_format)
