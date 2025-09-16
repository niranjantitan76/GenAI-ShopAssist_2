

BASE_URL = "http://127.0.0.1:8000"

def intent_confirmation_layer(response_assistant):
    delimiter = "####"

    allowed_values = {'low', 'medium', 'high'}

    prompt = f"""
    You are a senior evaluator who has an eye for detail.The input text will contain a user requirement captured through 6 keys.
    You are provided an input. You need to evaluate if the input text has the following keys:
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
    - Values must be only from {allowed_values}.
    - 'Budget' must be a number.

    Only output a one-word string in JSON format at the key 'result' - Yes/No.
    Thought 1 - Output a string 'Yes' if the values are correctly filled for all keys, otherwise output 'No'.
    Thought 2 - If the answer is No, mention the reason in the key 'reason'.
    THought 3 - Think carefully before the answering.
    Return ONLY JSON:
    {{
    "result": "Yes" or "No",
    "reason": "reason if No"
    }}
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