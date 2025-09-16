from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from config import settings
# Load env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class EmbeddingRequest(BaseModel):
    text: str

@app.post("/embedding")
async def generate_embedding(req: EmbeddingRequest):
    response = client.embeddings.create(
        model=settings.MODEL,
        input=req.text
    )
    return {
        "embedding": response.data[0].embedding,
        "dimension": len(response.data[0].embedding)
    }
