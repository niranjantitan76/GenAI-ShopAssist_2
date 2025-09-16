from lib.chat_manager import chat_completions

def process(user_input: str,json_format: bool = False):
    return chat_completions(user_input, json_format)

