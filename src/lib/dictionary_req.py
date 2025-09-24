import asyncio
import json

from pydantic import ValidationError

from .models.intent_model import UserRequirementModel
def dictionary_present(response):
    delimiter = "####"

    user_req = {'GPU intensity': 'high',
                'Display quality': 'high',
                'Portability': 'medium',
                'Multitasking': 'high',
                'Processing speed': 'high',
                'Budget': '200000'}

    prompt = f"""You are a python expert. You are provided an input.
            You have to check if there is a python dictionary present in the string.
            It will have the following format {user_req}.
            Your task is to just extract the relevant values from the input and return only the python dictionary in JSON format.
            The output should match the format as {user_req}.

            {delimiter}
            Make sure that the value of budget is also present in the user input. ###
            The output should contain the exact keys and values as present in the input.
            Ensure the keys and values are in the given format:
            {{
            'GPU intensity': 'low/medium/high ',
            'Display quality':'low/medium/high',
            'Portability':'low/medium/high',
            'Multitasking':'low/medium/high',
            'Processing speed':'low/medium/high',
            'Budget':'numerical value'
            }}
            Here are some sample input output pairs for better understanding:
            {delimiter}
            input 1: - GPU intensity: low - Display quality: high - Portability: low - Multitasking: high - Processing speed: medium - Budget: 50,000 INR
            output 1: {{'GPU intensity': 'low', 'Display quality': 'high', 'Portability': 'low', 'Multitasking': 'high', 'Processing speed': 'medium', 'Budget': '50000'}}

            input 2: {{'GPU intensity':     'low', 'Display quality':     'low', 'Portability':    'medium', 'Multitasking': 'medium', 'Processing speed': 'low', 'Budget': '90,000'}}
            output 2: {{'GPU intensity': 'low', 'Display quality': 'low', 'Portability': 'medium', 'Multitasking': 'medium', 'Processing speed': 'low', 'Budget': '90000'}}

            input 3: Here is your user profile 'GPU intensity': 'high','Display quality': 'high','Portability': 'medium','Multitasking': 'high','Processing speed': 'high','Budget': '200000 INR'
            output 3: {{'GPU intensity': 'high','Display quality': 'high','Portability': 'medium','Multitasking': 'high','Processing speed': 'high','Budget': '200000'}}
            {delimiter}
            """
    messages = [{"role": "system", "content":prompt },
                {"role": "user", "content":response }]

    return messages


def dictionary_present_validated(response: str):
    """
    Prepares a prompt for an LLM to extract a user requirement dictionary
    and then validates the LLM's output using a Pydantic model.
    """
    delimiter = "####"

    # Define the structure in a clean, maintainable way
    user_req_schema = {
        'GPU intensity': 'low/medium/high',
        'Display quality': 'low/medium/high',
        'Portability': 'low/medium/high',
        'Multitasking': 'low/medium/high',
        'Processing speed': 'low/medium/high',
        'Budget': 'numerical value'
    }

    # The prompt still needs to be descriptive for the LLM
    prompt = f"""
    You are a python expert. You are provided an input.
    Your task is to extract a Python dictionary with the following exact keys and value formats: {user_req_schema}.
    The dictionary must be returned in JSON format ONLY.

    {delimiter}
    Rules:
    - The keys must match exactly.
    - The 'Budget' value must be a number (remove any currency symbols like INR, $, commas, etc.).
    - Your output should be a JSON object and nothing else.

    Here are some sample input output pairs for better understanding:
    input 1: - GPU intensity: low - Display quality: high - Portability: low - Multitasking: high - Processing speed: medium - Budget: 50,000 INR
    output 1: {{'GPU intensity': 'low', 'Display quality': 'high', 'Portability': 'low', 'Multitasking': 'high', 'Processing speed': 'medium', 'Budget': '50000'}}

    input 2: {{'GPU intensity':     'low', 'Display quality':     'low', 'Portability':    'medium', 'Multitasking': 'medium', 'Processing speed': 'low', 'Budget': '90,000'}}
    output 2: {{'GPU intensity': 'low', 'Display quality': 'low', 'Portability': 'medium', 'Multitasking': 'medium', 'Processing speed': 'low', 'Budget': '90000'}}

    input 3: Here is your user profile 'GPU intensity': 'high','Display quality': 'high','Portability': 'medium','Multitasking': 'high','Processing speed': 'high','Budget': '200000 INR'
    output 3: {{'GPU intensity': 'high','Display quality': 'high','Portability': 'medium','Multitasking': 'high','Processing speed': 'high','Budget': '200000'}}
    {delimiter}
    """
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Here is the user input: {response}"}
    ]

    # In a real application, you would call your LLM here:
    # llm_response_string = await get_chat_completions(messages, True)

    # For demonstration, let's assume a dummy response from the LLM:
    llm_response_string = "{'GPU intensity': 'high','Display quality': 'high','Portability': 'medium','Multitasking': 'high','Processing speed': 'high','Budget': '200000'}"

    try:
        # Use json.loads to parse the string into a Python dict
        response_dict = json.loads(llm_response_string.replace("'", '"'))

        # Use the Pydantic model to validate the parsed dictionary
        validated_data = UserRequirementModel(**response_dict)
        print("Validation successful!")
        return messages

    except (json.JSONDecodeError, ValidationError) as e:
        print(f"Validation failed: {e}")
        return None