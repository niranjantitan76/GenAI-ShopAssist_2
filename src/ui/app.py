import gradio as gr
import asyncio
import httpx
import traceback
from fastapi import FastAPI
import uvicorn
import requests
# IMPORTANT: The FastAPI base URL is now derived from the container name defined in docker-compose.yml
FASTAPI_BASE_URL = "http://api:8000/api/v1/dialogue"


# Use httpx for asynchronous requests
def call_backend(user_input, state):
    try:
        # The backend expects a dictionary for the state
        payload = {
            "user_input": user_input,
            "state": state
        }


        response = requests.post(FASTAPI_BASE_URL, json=payload, timeout=60.0)
        response.raise_for_status()
        data = response.json()
        return data.get("reply"), data.get("state")

    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        traceback.print_exc()
        return "An unexpected error occurred. Please try again.", state or {}


with gr.Blocks(css=".chatbox {height: 400px;}") as demo:
    gr.Markdown("## 💻 Laptop Recommender Chatbot")

    chatbot = gr.Chatbot(elem_classes="chatbox", label="Laptop Assistant")
    msg = gr.Textbox(placeholder="Type here...", label="Your Message")
    status_text = gr.Textbox(label="Status", interactive=False)
    state = gr.State()


    async def respond(message, chat_history, state):
        if not chat_history:
            chat_history = []

            # 1. Immediately display the user's message
            chat_history.append([message, None])
            # YIELD 1: Display user message, show "Thinking..." and disable input
            yield chat_history, state, gr.update(value="Thinking..."), gr.update(value="", interactive=False)

            # 2. Call the backend with the user's message and current state
            reply, updated_state = await call_backend(message, state)

            # 3. Append the agent's response to the chat history
            chat_history[-1][1] = reply

            # 4. Check for reset state and reset the UI if necessary
            if updated_state and updated_state.get("step") == -1:
                # YIELD 2: Display reset message
                yield chat_history, updated_state, gr.update(
                    value="Conversation reset. Type to begin again."), gr.update(interactive=False)
                await asyncio.sleep(2)  # Wait for 2 seconds before clearing the history
                # YIELD 3: Clear all UI components to restart
                yield [], {"step": 0}, gr.update(value=""), gr.update(value="", interactive=True)
            else:
                # YIELD 4: Display new message and re-enable input
                yield chat_history, updated_state, gr.update(value=""), gr.update(interactive=True)

    def init_chat():
        reply, updated_state = call_backend(user_input="", state=None)
        return [[None, reply]], updated_state, gr.update(value=""), gr.update(interactive=True)


    demo.load(init_chat, inputs=None, outputs=[chatbot, state, status_text, msg])
    msg.submit(
        respond,
        [msg, chatbot, state],
        [chatbot, state, status_text, msg],
        api_name="respond"
    )

app = FastAPI()
app = gr.mount_gradio_app(app, demo, path="/gradio")
