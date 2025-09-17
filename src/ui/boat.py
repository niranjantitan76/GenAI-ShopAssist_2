import gradio as gr
import requests
import traceback
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

FASTAPI_BASE_URL = "http://api:8000/api/v1/dialogue"

app = FastAPI()

# CORS (⚠️ tighten in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/manifest.json")
def manifest():
    return JSONResponse({
        "name": "Laptop Chatbot",
        "short_name": "Chatbot",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "description": "Demo chatbot app"
    })

# ---------------------
# Backend call helper
# ---------------------
def call_backend(user_input, state):
    try:
        if not state:
            state = {"step": 0}

        payload = {"user_input": user_input, "state": state}

        response = requests.post(FASTAPI_BASE_URL, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        reply = data.get("reply", "No response")
        state = data.get("state", {})

        return reply, state
    except Exception as e:
        print("❌ Backend call failed:", e)
        traceback.print_exc()
        return "Backend error, please try again later.", state or {}

# ---------------------
# Gradio UI
# ---------------------
with gr.Blocks(css=".chatbox {height: 400px;}") as demo:
    gr.Markdown("## 💻 Laptop Recommender Chatbot")

    chatbot = gr.Chatbot(elem_classes="chatbox", label="Laptop Assistant")
    msg = gr.Textbox(placeholder="Type here...", label="Your Message")
    state = gr.State()

    def respond(message, chat_history, state):
        if chat_history is None:
            chat_history = []
        reply, state = call_backend(message, state)
        chat_history = chat_history + [[message, reply]]

        if state and state.get("step") == -1:
            import threading
            threading.Thread(target=lambda: demo.close(), daemon=True).start()

        return "", chat_history, state

    def init_chat():
        first_msg, state = call_backend(user_input="", state=None)
        return [[None, first_msg]], state

    def init_chat_dummy():
        return [["System", "Welcome!"]], {}
    demo.load(init_chat_dummy, None, [chatbot, state])  # auto-start
    msg.submit(respond, [msg, chatbot, state], [msg, chatbot, state])

# Mount Gradio at /gradio
app = gr.mount_gradio_app(app, demo, path="/gradio")

# ⚠️ Don't use demo.launch() here!
# Run with: uvicorn app:app --host 0.0.0.0 --port 8000
