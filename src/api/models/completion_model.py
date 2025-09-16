from pydantic import BaseModel
from typing import List, Dict, Any

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    user_input: str
    json_format: bool = False

class ChatResponse(BaseModel):
    reply: str
    new_state: Dict[str, Any]

