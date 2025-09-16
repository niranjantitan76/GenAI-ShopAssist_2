import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt
from api.core.config import settings
import logging
# Load API key
load_dotenv()
@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def moderation_check(user_input):
    client=OpenAI(api_key=settings.OPENAI_API_KEY)
    response = client.moderations.create(input=user_input)
    if response.results[0].flagged:
        return "Flagged"
    return "Not Flagged"
@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def chat_completions(input, json_format=False):
    logging.info(f"Chat input: {input}")
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    #input=[{"role": "system", "content": 'Hi'}]
    MODEL = settings.MODEL
    system_message_json_output = """<<. Return output in JSON format to the key output.>>"""
    if json_format:
        input[0]['content'] += system_message_json_output

        chat_completion_json = client.chat.completions.create(
            model=MODEL,
            messages=input,
            response_format={"type": "json_object"},
            seed=1234
        )
        output = json.loads(chat_completion_json.choices[0].message.content)
    else:
        chat_completion = client.chat.completions.create(
            model=MODEL,
            messages=input,
            seed=2345
        )
        output = chat_completion.choices[0].message.content

    return output
