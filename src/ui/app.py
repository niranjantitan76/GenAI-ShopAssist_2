# import gradio as gr
# import asyncio
# import requests
# import traceback
# from fastapi import FastAPI, Request, Form, File, UploadFile
# from fastapi.responses import JSONResponse
# FASTAPI_BASE_URL = "http://api:8000/api/v1/dialogue"
# from fastapi.middleware.cors import CORSMiddleware
# import httpx
# import httpx
# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],            # <-- Change to list of allowed domains in prod
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# @app.get("/manifest.json")
# def manifest():
#     return JSONResponse({
#         "name": "Laptop Chatbot",
#         "short_name": "Chatbot",
#         "start_url": "/",
#         "display": "standalone",
#         "background_color": "#ffffff",
#         "description": "Demo chatbot app"
#     })
#
# def call_backend(user_input, state):
#     try:
#         if not state:
#             state = {"step": 0}
#         payload = {
#             "user_input": user_input,
#             "state": {"step": 0}
#         }
#
#         response = requests.post(FASTAPI_BASE_URL, json=payload)
#         response.raise_for_status()
#         data = response.json()
#         print(f'after response{data}')
#         reply = data.get("reply", "No response")
#         state = data.get("state", {})
#         print('before reply')
#         return reply, state
#     except Exception as e:
#         print(f"❌ Error calling backend: {e}")
#         print(f"An unexpected error occurred: {e}")  # Print to console for server-side debugging
#         # On error, provide a graceful message to the user and reset state for a fresh start
#         print("Error type:", type(e).__name__)
#         print("Error message:", str(e))
#         print("Full traceback:")
#         traceback.print_exc()
#         return "Backend error, check logs.", state or {}
# def greet(name):
#     return f"Hello, {name}!"
# with gr.Blocks(css=".chatbox {height: 400px;}") as demo:
#     gr.Markdown("## 💻 Laptop Recommender Chatbot")
#
#     chatbot = gr.Chatbot(elem_classes="chatbox", label="Laptop Assistant")
#     msg = gr.Textbox(placeholder="Type here...", label="Your Message")
#     state = gr.State()
#
#     async def respond(message, chat_history, state):
#         if chat_history is None:
#             chat_history = []
#         reply, state = call_backend(message, state)
#
#         # ✅ must append as dicts, not tuples
#         # chat_history.append({"role": "user", "content": message})
#         # chat_history.append({"role": "assistant", "content": reply})
#         chat_history = chat_history + [[message, reply]]
#         # detect exit
#         if state and state.get("step") == -1:
#             import threading
#             threading.Thread(target=lambda: demo.close(), daemon=True).start()
#
#         return "", chat_history, state
#
#     async def init_chat():
#         first_msg, state = call_backend(user_input="", state=None)
#         print(f'First:{first_msg},state:{state}')
#         return [[None, first_msg]], state
#
#     demo.load(init_chat, inputs=None, outputs=[chatbot, state])  # auto-start
#     msg.submit(respond, [msg, chatbot, state], [msg, chatbot, state])
#     app = gr.mount_gradio_app(app, demo, path="/gradio")
#
# if __name__ == "__main__":
#     demo.launch(server_name="127.0.0.1", server_port=7860)
#
# #def start_ui():
#     # with gr.Blocks(css=".chatbox {height: 400px;}") as demo:
#     #     gr.Markdown("## 💻 Laptop Recommender Chatbot")
#     #
#     #     chatbot = gr.Chatbot(elem_classes="chatbox", label="Laptop Assistant")
#     #     msg = gr.Textbox(placeholder="Type here...", label="Your Message")
#     #     state = gr.State()
#     #     def respond(message, chat_history, state):
#     #         reply, state = post_to_api(endpoint="dialog", data={})
#     #         chat_history = chat_history + [[message, reply]]
#     #         # detect exit
#     #         if state.get("step") == -1:
#     #             import threading
#     #             threading.Thread(target=lambda: demo.close(), daemon=True).start()
#     #         return "", chat_history, state
#     #     # inject first bot message
#     #     def init_chat():
#     #         #first_msg, state = post_to_api(endpoint="dialog", data={})
#     #         return "Hello" # None means no user message, only bot
#     #
#     #     demo.load(init_chat, inputs=None, outputs=[chatbot, state])  # auto-start
#     #
#     #     msg.submit(respond, [msg, chatbot, state], [msg, chatbot, state])
#     # app = gr.mount_gradio_app(app, demo, path="/gradio")
#     # demo.launch()
#
# # def chatbot(message, history):
# #     return "Hello 👋, you said: " + message
# #
# # # Create gradio UI
# # demo = gr.Interface(fn=chatbot, inputs="text", outputs="text")
# #
# # # Mount Gradio to FastAPI at /gradio
# # app = gr.mount_gradio_app(app, demo, path="/gradio")
# # #
# #
# # if __name__ == "__main__":
# #     start_ui()
