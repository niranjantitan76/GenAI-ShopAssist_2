from openai import OpenAI
from fastapi import APIRouter
from api.core.config import settings
from dotenv import load_dotenv
load_dotenv()
def process(user_input):
    client=OpenAI(api_key=settings.OPENAI_API_KEY)
    response = client.moderations.create(input=user_input)
    if response.results[0].flagged:
        return "Flagged"
    return "Not Flagged"
