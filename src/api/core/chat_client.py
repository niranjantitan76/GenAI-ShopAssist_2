import httpx

class ChatClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000/api"):
        self.base_url = base_url
        self.client = httpx.Client(timeout=10)

    def chat_completion(self, messages, json_format=False):
        payload = {"messages": messages, "json_format": json_format}
        response = self.client.post(f"{self.base_url}/chat/completions", json=payload)
        response.raise_for_status()
        return response.json()

    def moderation(self, text: str):
        payload = {"text": text}
        response = self.client.post(f"{self.base_url}/chat/moderation", json=payload)
        response.raise_for_status()
        return response.json()

    def close(self):
        self.client.close()
