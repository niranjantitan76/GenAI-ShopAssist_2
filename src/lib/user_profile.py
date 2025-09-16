import openai
import json
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_laptop_preferences(
        gpu_intensity: str,
        display_quality: str,
        portability: str,
        multitasking: str,
        processing_speed: str,
        budget: str
):
    """
    Extracts the user's preferences for a laptop from a given message.
    This function is not actually called, but its parameters are used to
    define the schema for the OpenAI function tool.

    Args:
        gpu_intensity (str): The user's preference for GPU intensity (low, medium, or high).
        display_quality (str): The user's preference for display quality (low, medium, or high).
        portability (str): The user's preference for portability (low, medium, or high).
        multitasking (str): The user's preference for multitasking ability (low, medium, or high).
        processing_speed (str): The user's preference for processing speed (low, medium, or high).
        budget (str): The user's budget, in a numerical string format (e.g., '50000').
    """
    # This function body is just a placeholder to show the expected arguments.
    # In a real application, you would pass these arguments to another function.
    pass


# The JSON schema for our function tool
tools = [
    {
        "type": "function",
        "function": {
            "name": "extract_laptop_preferences",
            "description": "Extracts the user's preferences for a laptop from their message.",
            "parameters": {
                "type": "object",
                "properties": {
                    "gpu_intensity": {
                        "type": "string",
                        "description": "The user's preference for GPU intensity.",
                        "enum": ["low", "medium", "high"],
                    },
                    "display_quality": {
                        "type": "string",
                        "description": "The user's preference for display quality.",
                        "enum": ["low", "medium", "high"],
                    },
                    "portability": {
                        "type": "string",
                        "description": "The user's preference for portability.",
                        "enum": ["low", "medium", "high"],
                    },
                    "multitasking": {
                        "type": "string",
                        "description": "The user's preference for multitasking ability.",
                        "enum": ["low", "medium", "high"],
                    },
                    "processing_speed": {
                        "type": "string",
                        "description": "The user's preference for processing speed.",
                        "enum": ["low", "medium", "high"],
                    },
                    "budget": {
                        "type": "string",
                        "description": "The user's budget in a numerical format. E.g., '100000'.",
                    },
                },
                "required": ["budget", "gpu_intensity", "display_quality", "portability", "multitasking",
                             "processing_speed"],
            },
        },
    }
]


# A function that uses the tool to get a response from the model
def get_user_preferences(user_input: str):
    """
    Sends the user's input to the OpenAI model with the function tool enabled.
    """
    messages = [{"role": "user", "content": user_input}]

    response = openai.chat.completions.create(
        model="gpt-4o-mini",  # Using a smaller model for efficiency
        messages=messages,
        tools=tools,
        tool_choice="auto",  # Allows the model to decide whether to use the tool
    )

    # Check if the model has decided to use the tool
    tool_calls = response.choices[0].message.tool_calls

    if tool_calls:
        tool_call = tool_calls[0]
        function_name = tool_call.function.name
        arguments_json = json.loads(tool_call.function.arguments)

        print(f"Model decided to call the function: '{function_name}'")
        print("Extracted Parameters:")
        return arguments_json
    else:
        # If the model didn't call the function, it means it didn't find the necessary info
        print("The model did not find enough information to extract all preferences.")
        return None


# --- Example Usage ---
if __name__ == "__main__":
    # Example 1: Clear user input that matches the schema
    input1 = "I need a new laptop with high GPU intensity, high display quality, low portability, high multitasking, medium processing speed, and a budget of 150000."
    print("User Input 1:")
    print(input1)
    extracted_data_1 = get_user_preferences(input1)
    if extracted_data_1:
        print(json.dumps(extracted_data_1, indent=4))
        print("-" * 30)

    # Example 2: Input that doesn't provide all the required info
    input2 = "I need a gaming laptop for around 200000 rupees."
    print("\nUser Input 2:")
    print(input2)
    extracted_data_2 = get_user_preferences(input2)
    if extracted_data_2:
        print(json.dumps(extracted_data_2, indent=4))
        print("-" * 30)
