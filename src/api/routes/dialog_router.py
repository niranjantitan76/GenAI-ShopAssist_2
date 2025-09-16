
from fastapi import APIRouter, Depends
from ..services.dialog.dialog_service import dialogue
from lib.chat_client import ChatClient
# from lib.dialog_manager import Dialogue_mgmt_system
dialog = APIRouter()
from pydantic import BaseModel
from typing import Dict, Any
import logging
class DialogueRequest(BaseModel):
    user_input: str
    state: Dict[str, Any] = {}

class DialogueResponse(BaseModel):
    reply: str
    new_state: Dict[str, Any]
@dialog.post("/dialogue")
async def run_dialogue(req: DialogueRequest):
    #response, new_state = service.dialogue(req.user_input, req.state)
    logging.info(f"Received dialogue request: {req.user_input}")

    return await dialogue(req.user_input, req.state) # DialogueResponse(reply=response, new_state=new_state)