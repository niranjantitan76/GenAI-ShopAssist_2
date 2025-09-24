import json
import asyncio
from lib.initialize_conversation import init_conversation
from lib.dictionary_req import dictionary_present,dictionary_present_validated
from lib.intent_confirmation import intent_confirmation_layer
from lib.recommendation import compare_product_user_req
import traceback
from lib.chat_manager import chat_completions,moderation_check,intent_completions

# def recommendation_validation(laptop_recommendation):
#     data = json.loads(laptop_recommendation)
#     data1 = []
#     for i in range(len(data)):
#         if data[i]['Score'] > 2:
#             data1.append(data[i])
#
#     return data1

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


def format_laptops_for_display(laptops):
    """Formats the list of laptops into a readable string for the user."""
    if not laptops:
        return "Sorry, I couldn't find any laptops that match your preferences."

    formatted_list = "Here are my top 3 recommendations:\n\n"
    for i, laptop in enumerate(laptops[:3]):
        try:
            formatted_list += f"{i + 1}. **{laptop['name']}** - {laptop['display']} display, {laptop['cpu']} CPU, {laptop['ram']} RAM, and {laptop['storage']} storage. Priced at Rs. {laptop['price']}.\n"
        except KeyError as e:
            print(f"Missing key in laptop data: {e}")
            continue
    formatted_list += "\nDo you have any questions about these options, or would you like to restart?"
    return formatted_list

#
# def recommendation_validation(laptop_recommendation):
#     """Validates and filters laptop recommendations based on a score."""
#     try:
#         data = json.loads(laptop_recommendation)
#         valid_laptops = [laptop for laptop in data if laptop.get('Score', 0) > 2]
#         return valid_laptops
#     except json.JSONDecodeError as e:
#         print(f"Error decoding JSON from recommendation: {e}")
#         return []
def recommendation_validation(laptop_recommendation):
    print('recommendation_validation Layer')
    data = json.loads(laptop_recommendation)
    data1 = []
    for i in range(len(data)):
        if data[i]['Score'] > 2:
            data1.append(data[i])

    return data1

def dialogue_more_advance(user_input, state):

    # """
    # Improved dialogue manager for laptop recommender
    # """
    #
    response = ""

    # --- Initialize state ---
    if state is None or state.get('step') == 0:
        state = {
            "step": 0,
            "llm_conversation_history": [],
            "top_3_laptops": None,
            "conversation_reco": None
        }
        initial_conv_history_llm =init_conversation()
        state['llm_conversation_history'] = initial_conv_history_llm
        state['step'] = 1
        #return {"reply": initial_conv_history_llm, "state": state}

    llm_conversation_history = state.get('llm_conversation_history')
    top_3_laptops = state.get('top_3_laptops')
    conversation_reco = state.get('conversation_reco')

    try:
        # --- Exit command ---
        if user_input.lower() == "exit":
            return {
                "reply": "Thank you for using the laptop recommender! Goodbye.",
                "state": {"step": 0, "llm_conversation_history": [], "top_3_laptops": None, "conversation_reco": None}
            }

        # --- Moderation Check ---
        moderation_status = moderation_check(user_input)
        if moderation_status == 'Flagged':
            return {"reply": "⚠️ Your message was flagged. Please restart.", "state": state}

        # --- Before recommendation step ---
        if top_3_laptops is None and int(state['step'])<=4:
            llm_conversation_history.append({"role": "user", "content": user_input})
            response_assistant = chat_completions(llm_conversation_history)

            # Confirm intent
            confirmation = intent_completions(intent_confirmation_layer(response_assistant))
            print("Intent Confirmation Yes/No:", confirmation)  # For debugging, print to console

            if not confirmation.result:
                llm_conversation_history.append({"role": "assistant", "content": response_assistant})
                response = response_assistant
            else:
                # Intent confirmed: extract variables and fetch laptops
                print('\n' + "Variables extracted!" + '\n')  # For debugging
               # Intent confirmed – start fetching laptops
                state['step'] = 2
                extracted_user_prefs = chat_completions(dictionary_present(response_assistant), True)

                # Interim response ("please wait")
                interim_msg = "⏳ Thank you for the details. Please wait while I fetch the best laptops..."
                # Gradio will show this first
                print("Interim Message:", interim_msg)
                #yield {"reply": interim_msg, "state": state}

                fetched_laptops = compare_product_user_req(extracted_user_prefs)
                top_3_laptops = recommendation_validation(fetched_laptops)
                print("top_3_laptops:", top_3_laptops)

                state['top_3_laptops'] = top_3_laptops
                conversation_reco=initialize_conv_reco(top_3_laptops)
                state['conversation_reco']= conversation_reco
                print("Conversation Reco:", conversation_reco)
                conversation_reco.append({"role": "user", "content": "This is my user profile" + str(extracted_user_prefs)})

                recommendation = chat_completions(conversation_reco)
                print("Conversation Reco:", recommendation)
                moderation = moderation_check(recommendation)
                if moderation == 'Flagged':
                    return {"reply": "⚠️ Your message was flagged. Please restart.", "state": state}

                conversation_reco.append({"role": "assistant", "content": str(recommendation)})

                print(str(recommendation) + '\n')
                response = recommendation
            return {"reply": response, "state": state}

        # --- After recommendation available ---
        else:
            if "recommend" in user_input.lower():
                state['conversation_reco'].append({"role": "user", "content": user_input})
                recommendation_response = chat_completions(state['conversation_reco'])

                # Reset after showing recommendations
                reply_final = "📊 Top 3 Laptop Recommendations:\n\n" + recommendation_response
                reset_state = {"step": 0, "llm_conversation_history": [], "top_3_laptops": None, "conversation_reco": None}
                return {"reply": reply_final, "state": reset_state}

            else:
                # Normal follow-up conversation
                conversation_reco.append({"role": "user", "content": user_input})
                follow_up_response = chat_completions(conversation_reco)
                return {"reply": f"👤 You: {user_input}\n🤖 {follow_up_response}", "state": state}

    except Exception as ex:
        traceback.print_exc()
        return {
            "reply": "❌ An unexpected error occurred. Please type 'exit' to restart.",
            "state": {"step": 0, "llm_conversation_history": [], "top_3_laptops": None, "conversation_reco": None}
        }
