from typing import List, Dict, Any

class LLMInterface:
    async def get_chat_completions(self, messages: List[Dict[str, str]]) -> str:
        raise NotImplementedError
