from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ API KEY
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise Exception("OPENROUTER_API_KEY is not set in environment variables")

# ✅ Request Model (with history)
class ChatRequest(BaseModel):
    message: str
    history: list = []   # 🔥 important for memory

@app.get("/")
def home():
    return {"message": "Chatbot API is running with OpenRouter"}

# ✅ Models (fallback)
MODELS = [
    "openchat/openchat-7b",
    "meta-llama/llama-3-8b-instruct",
    "nousresearch/nous-capybara-7b"
]

# ✅ CHAT ENDPOINT
@app.post("/chat")
def chat(req: ChatRequest):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "My Chatbot"
    }

    # 🔥 Build conversation history
    messages = [
        {
            "role": "system",
            "content": "Reply in short, clear answers (max 3 lines). Remember user's name if provided."
        }
    ]

    # Add previous messages
    for msg in req.history:
        messages.append(msg)

    # Add current message
    messages.append({
        "role": "user",
        "content": req.message
    })

    # 🔁 Try models one by one
    for model in MODELS:
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json={
                    "model": model,
                    "messages": messages,
                    "max_tokens": 100
                },
                timeout=10
            )

            data = response.json()

            # ✅ Success
            if "choices" in data:
                reply = data["choices"][0]["message"]["content"]

                return {
                    "reply": reply,
                    "model_used": model
                }

        except Exception as e:
            print(f"Error with model {model}:", e)

    # ❌ All failed
    return {"reply": "All AI models are busy. Try again later."}

# ✅ TEST
@app.get("/test")
def test():
    return {"status": "OpenRouter working"}
