from pydantic import BaseModel
from typing import List, Dict, Any

class ModerationRequest(BaseModel):
    text: str

class ModerationResponse(BaseModel):
    result: str

