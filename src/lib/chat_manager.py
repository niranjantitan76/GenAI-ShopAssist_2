import json

from kubernetes.stream import stream
from openai import OpenAI
from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt
from api.core.config import settings
import logging
from lib.models.intent_model import ConfirmationResponse

load_dotenv()
client = OpenAI(api_key=settings.OPENAI_API_KEY)
MODEL = settings.MODEL
@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def moderation_check(user_input):
    response = client.moderations.create(input=user_input)
    if response.results[0].flagged:
        return "Flagged"
    return "Not Flagged"


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def chat_completions(input, json_format=False):
    logging.info(f"Chat input: {input}")

    system_instruction = """<<. Return output in JSON format to the key output.>>"""
    system_message_json_output= " You are a helpful assistant. Return output in JSON under the key 'output'."
    # Ensure messages is a list
    if not isinstance(input, list):
        raise TypeError(f"Expected messages to be a list of dicts, got {type(input)}: {input!r}")

    # Ensure each item is a dict with keys "role" and "content"
    for i, m in enumerate(input):
        if not isinstance(m, dict):
            raise TypeError(f"Expected message at index {i} to be dict, got {type(m)}: {m!r}")
        if "role" not in m or "content" not in m:
            raise KeyError(f"Message at index {i} missing 'role' or 'content'. Message: {m!r}")

    if json_format:
        if not input or input[0]["role"] != "system":
            input.insert(0, {
                "role": "system",
                "content": "You are a helpful assistant. Return output in JSON under the key 'output'."
            })
        else:
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
@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def intent_completions(input, json_format=False):
    logging.info(f"Chat input: {input}")
    response = client.responses.parse(
        model=MODEL,
        input=input,
        text_format=ConfirmationResponse
    )

    output = response.output_parsed
    return output