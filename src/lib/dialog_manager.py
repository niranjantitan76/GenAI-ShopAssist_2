#from IPython.display import display
import json
from lib.initialize_conversation import init_conversation
from lib.dictionary_req import dictionary_present
from lib.intent_confirmation import intent_confirmation_layer
from lib.recommendation import recommend
# from lib.chat_client import ChatClient
import traceback
from lib.chat_manager import chat_completions,moderation_check


# def __init__(self,client: ChatClient):
#     # Get the initial greeting and populate the LLM conversation history
#       self.client=client

async def dialogue(user_input, state):
    """
    Manages the dialogue flow for a laptop recommendation chatbot, processing one user input per call.
    It internally manages the LLM conversation history within the state object.

    Args:
        user_input (str): The current input from the user.
        state (dict): A dictionary to maintain the state of the conversation, including:
                      - 'step': Current step in the dialogue.
                      - 'llm_conversation_history': The conversation history in LLM format.
                      - 'top_3_laptops': List of recommended laptops, once identified.
                      - 'conversation_reco': Separate history for post-recommendation chat.

    Returns:
        tuple: A tuple containing the assistant's response (str) and the updated state (dict).
    """
    # client = ChatClient()
    # response = initial_conv_history_llm[-1]['content'] # Get the actual greeting text
    #state['step'] = 1  # Move to step 1 after initial greeting
    # Initialize state for a new session if needed
    # This block executes for the very first turn of a new session
    response = ""

    # Initialize state for a new session if needed
    # This block executes for the very first turn of a new session
    if state is None or state.get('step') == 0:
        # Initialize the state dictionary with default values
        state = {
            "step": 0,
            "llm_conversation_history": [],  # This will hold LLM-formatted chat history
            "top_3_laptops": None,
            "conversation_reco": None  # History for post-recommendation chat
        }
        # Get the initial greeting and populate the LLM conversation history
        initial_conv_history_llm = init_conversation()  # Should return something like [{"role": "assistant", "content": "Hello..."}]
        state['llm_conversation_history'] = initial_conv_history_llm
        # response = initial_conv_history_llm[-1]['content'] # Get the actual greeting text
        state['step'] = 1  # Move to step 1 after initial greeting
        # return response, state

    # --- Extract state variables for the current turn ---
    llm_conversation_history = state.get('llm_conversation_history')
    top_3_laptops = state.get('top_3_laptops')
    conversation_reco = state.get('conversation_reco')  # History for follow-up questions

    try:
        # --- Handle "exit" command ---
        if user_input.lower() == "exit":
            response = "Thank you for using the laptop recommender! Goodbye."
            state['step'] = -1
            # Reset state to allow a new conversation to start cleanly next time
            return response, {"step": 0, "llm_conversation_history": [], "top_3_laptops": None,
                              "conversation_reco": None}

        # --- Moderation Check for User Input ---
        moderation_status = moderation_check(user_input)
        if moderation_status == 'Flagged':
            response = "Sorry, this message has been flagged. Please restart your conversation."
            print(response)
            print(state)
            return {"reply":response, "state":state}  # Keep current state, user needs to restart by typing "exit" or refreshing

        # --- Main Dialogue Logic: Before Recommendations are Made (Gathering Info) ---
        if top_3_laptops is None:
            llm_conversation_history.append({"role": "user", "content": user_input})  # Add user input to LLM history
            response_assistant = chat_completions(llm_conversation_history)

            # --- Moderation Check for Assistant's Response ---
            moderation_status = moderation_check(response_assistant)
            if moderation_status == 'Flagged':
                response = "Sorry, this message has been flagged. Please restart your conversation."
                print(response)
                print(state)
                return {"reply":response, "state":state}
            print(f'response assistant: {response_assistant}')
            confirmation = chat_completions(intent_confirmation_layer(response_assistant),True)
            print("Intent Confirmation Yes/No:", confirmation)  # For debugging, print to console

            if "No" in confirmation.get('result'):
                # If intent not confirmed, continue gathering info from user
                llm_conversation_history.append({"role": "assistant", "content": response_assistant})
                response = response_assistant
            else:
                # Intent confirmed: extract variables and fetch laptops
                print('\n' + "Variables extracted!" + '\n')  # For debugging
                extracted_user_prefs = chat_completions(dictionary_present(response_assistant))
                print(
                    "Thank you for providing all the information. Kindly wait, while I fetch the products: \n")  # For debugging

                # Fetch and validate recommendations
                fetched_laptops = recommend(extracted_user_prefs)
                validated_reco = recommendation_validation(fetched_laptops)

                # Store top_3_laptops and initialize conversation_reco in state
                state['top_3_laptops'] = validated_reco
                state['conversation_reco'] = initialize_conv_reco(validated_reco)  # Initialize history for reco chat

                # Generate initial recommendation response using the recommendation specific history
                state['conversation_reco'].append(
                    {"role": "user", "content": "This is my user profile" + str(extracted_user_prefs)})
                recommendation_response = chat_completions(state['conversation_reco'])

                # --- Moderation Check for Recommendation Response ---
                moderation_status = moderation_check(recommendation_response)
                if moderation_status == 'Flagged':
                    response = "Sorry, this message has been flagged. Please restart your conversation."
                    return response, state

                # Append assistant's recommendation to both histories for full context
                llm_conversation_history.append({"role": "assistant", "content": recommendation_response})
                state['conversation_reco'].append({"role": "assistant", "content": recommendation_response})
                response = recommendation_response

        # --- Main Dialogue Logic: After Recommendations are Made (Handling Follow-up) ---
        else:
            # Continue the follow-up conversation using the dedicated recommendation history
            conversation_reco.append({"role": "user", "content": user_input})
            follow_up_response = chat_completions(conversation_reco)

            # --- Moderation Check for Follow-up Response ---
            moderation_status = moderation_check(follow_up_response)
            if moderation_status == 'Flagged':
                response = "Sorry, this message has been flagged. Please restart your conversation."
                return {"reply":response, "state":state}

            response = follow_up_response
            # Append assistant's response to the main LLM history as well (optional, but good for holistic view)
            llm_conversation_history.append({"role": "assistant", "content": response})
            # state['conversation_reco'] is already updated above
        print(response)
        state=state
        return {"reply":response, "state":state}  # Return the response and the updated state

    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")  # Print to console for server-side debugging
        # On error, provide a graceful message to the user and reset state for a fresh start
        print("Error type:", type(ex).__name__)
        print("Error message:", str(ex))
        print("Full traceback:")
        traceback.print_exc()
        return "An unexpected error occurred. Please try again or type 'exit' to restart.", \
            {"step": 0, "llm_conversation_history": [], "top_3_laptops": None, "conversation_reco": None}

def recommendation_validation(laptop_recommendation):
    data = json.loads(laptop_recommendation)
    data1 = []
    for i in range(len(data)):
        if data[i]['Score'] > 2:
            data1.append(data[i])

    return data1

def initialize_conv_reco(products):
    system_message = f"""
    You are an intelligent laptop gadget expert and you are tasked with the objective to \
    solve the user queries about any product from the catalogue in the user message \
    You should keep the user profile in mind while answering the questions.\

    Start with a brief summary of each laptop in the following format, in decreasing order of price of laptops:
    1. <Laptop Name> : <Major specifications of the laptop>, <Price in Rs>
    2. <Laptop Name> : <Major specifications of the laptop>, <Price in Rs>

    """
    user_message = f""" These are the user's products: {products}"""
    conversation = [{"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}]
    # conversation_final = conversation[0]['content']
    return conversation


