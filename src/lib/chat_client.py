import httpx
import logging
import asyncio
from api.models.completion_model import ChatRequest
class ChatClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000/api/v1"):
        self.base_url = base_url
        self.client = httpx.Client(timeout=10)
        logging.info("Connecting to OpenAI chat client")

    def chat_completion(self, user_input, json_format=False):
        payload = {"user_input": user_input, "json_format": json_format}

        response = self.client.post(f"{self.base_url}/chat_completions", json=payload)
        response.raise_for_status()
        return response.json()

    def moderation(self, user_input: str):
        payload = {"user_input": user_input}
        response = self.client.post(f"{self.base_url}/moderation", json=payload)
        response.raise_for_status()
        return response.json()

    def close(self):
        self.client.close()
