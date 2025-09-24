

from functools import wraps
from typing import Callable, Any
from pydantic import BaseModel, Field, ValidationError
from typing import Literal, Optional
def intent1_confirmation_layer(response_assistant):
    delimiter = "####"

    allowed_values = {'low', 'medium', 'high'}
    confirm_values = {'Yes', 'No'}
    prompt = f"""
    You are a senior evaluator who has an eye for detail.The input text will contain a user requirement captured through 6 keys.
    You are provided an input. You need to evaluate if the input text has the following keys:
    {{
    'GPU intensity': 'values',
    'Display quality':'values',
    'Portability':'values',
    'Multitasking':'values',
    'Processing speed':'values',
    'Budget':number
    }}
    Rules:
    - Keys must match exactly.
    - Values must be only from {allowed_values}.
    - 'Budget' must be a number.
    
    Once the user requirement above is fully captured in python dictionary form, take consent or confirmation from user in yes or no as string and return it in JSON format at the key 'result' - "Yes" or "No".
    Thought 1 - Output a string "Yes" if the values are correctly filled for "result" key, otherwise output "No".
    Thought 2 - If the answer is "No", mention the reason in the key "reason".
    Thought 3 - Think carefully before the answering.
    
    {{
    "result": "Yes" or "No",
    "reason": "reason if No"
    }}
      Rules:
    - Keys must match exactly.
    - Values must be only from {confirm_values} in 'result' key.
    """
    # The values for the keys should only be from the allowed values: {allowed_values}.
    # The 'Budget' key can take only a numerical value.
    # Next you need to evaluate if the keys have the the values filled correctly.
    # Only output a one-word string in JSON format at the key 'result' - Yes/No.
    # Thought 1 - Output a string 'Yes' if the values are correctly filled for all keys, otherwise output 'No'.
    # Thought 2 - If the answer is No, mention the reason in the key 'reason'.
    # THought 3 - Think carefully before the answering.

    messages = [{"role": "system", "content": prompt},
                {"role": "user", "content": f"""Here is the input: {response_assistant}"""}]
    #confirmation = get_chat_completions(messages, True)

    return messages

def confirmation_evaluator(func: Callable) -> Callable:
    """A decorator to wrap the intent confirmation logic."""

    @wraps(func)
    def wrapper(response_assistant: Any, *args, **kwargs) -> dict:
        delimiter = "####"
        allowed_values = {'low', 'medium', 'high'}

        # The Pydantic model for the expected JSON output
        class ConfirmationResponse(BaseModel):
            result: Literal['Yes', 'No']
            reason: Optional[str] = None

        prompt = f"""
        You are a senior evaluator with an eye for detail. The input text will contain a user requirement captured through 6 keys.
        You need to evaluate if the input text has the following keys:
        {{
        'GPU intensity': 'values',
        'Display quality':'values',
        'Portability':'values',
        'Multitasking':'values',
        'Processing speed':'values',
        'Budget':'number'
        }}

        Rules:
        - Keys must match exactly.
        - Values must be from the set: {allowed_values} except for 'Budget' key.
        - 'Budget' must be a number.
        
        - The final output must be in JSON format with two keys: "result" and "reason".
        - The "result" key must have a value of True or False.
        - If "result" is False, provide a "reason" string explaining the failure.

        Example:
        {{
            "result": True or False,
            "reason": "The 'Budget' value is not a number."
        }}
        """

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Here is the input: {response_assistant}"}
        ]

        # This part assumes a function 'get_chat_completions' exists
        # confirmation = get_chat_completions(messages, True)

        return func(messages, *args, **kwargs)

    return wrapper


@confirmation_evaluator
def intent_confirmation_layer(messages: dict) -> dict:
    """The original function, now simplified to just return messages."""
    return messages


