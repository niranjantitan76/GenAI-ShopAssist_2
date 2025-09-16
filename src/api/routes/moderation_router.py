from fastapi import APIRouter, Depends
from  ..services.moderation import process
from pydantic import BaseModel
import asyncio
moderation = APIRouter()

class ModerationRequest(BaseModel):
    user_input: str
@moderation.post("/moderation")
def check(req: ModerationRequest):
    return process(req.user_input)
