# import gradio as gr
# import requests
#
# API_URL = "http://127.0.0.1:8000/api/v1/chat"
# from lib.dialog_manager import Dialogue_mgmt_system
# """""
# def chat_with_api(user_input):
#     response = requests.post(API_URL, json={"user_input": user_input})
#     if response.status_code == 200:
#         return response.json()
#     return {"error": "API call failed"}
#
#
# def start_ui():
#     with gr.Blocks() as demo:
#         chatbot = gr.Chatbot()
#         msg = gr.Textbox(placeholder="Type here...")
#
#         def respond(message, chat_history):
#             reply = chat_with_api(message)
#             chat_history.append((message, str(reply)))
#             return "", chat_history
#
#         msg.submit(respond, [msg, chatbot], [msg, chatbot])
#     demo.launch()
# """""
# def start_ui():
#     with gr.Blocks(css=".chatbox {height: 400px;}") as demo:
#         gr.Markdown("## 💻 Laptop Recommender Chatbot")
#
#         chatbot = gr.Chatbot(elem_classes="chatbox", label="Laptop Assistant")
#         msg = gr.Textbox(placeholder="Type here...", label="Your Message")
#         state = gr.State()
#         app=Dialogue_mgmt_system()
#         def respond(message, chat_history, state):
#             reply, state = app.dialogue(message, state)
#             chat_history = chat_history + [[message, reply]]
#             # detect exit
#             if state.get("step") == -1:
#                 import threading
#                 threading.Thread(target=lambda: demo.close(), daemon=True).start()
#             return "", chat_history, state
#         # inject first bot message
#         def init_chat():
#             first_msg, state = app.dialogue("",None)
#             return [[None, first_msg]], state  # None means no user message, only bot
#
#         demo.load(init_chat, inputs=None, outputs=[chatbot, state])  # auto-start
#
#         msg.submit(respond, [msg, chatbot, state], [msg, chatbot, state])
#
#     demo.launch()
#
# if __name__ == "__main__":
#     start_ui()
