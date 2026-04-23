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

# ✅ Request Model
class ChatRequest(BaseModel):
    message: str
    history: list = []

@app.get("/")
def home():
    return {"message": "Chatbot API is running with OpenRouter"}

# ✅ Working Models (auto fallback)
MODELS = [
    "meta-llama/llama-3-8b-instruct",
    "openchat/openchat-7b",
    "nousresearch/nous-capybara-7b"
]

# ✅ CHAT ENDPOINT
@app.post("/chat")
def chat(req: ChatRequest):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-site.com",  # change after deploy
        "X-Title": "AI Chatbot"
    }

    # ✅ System Prompt
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful AI assistant.\n"
                "- Keep answers short (2-3 lines).\n"
                "- If user asks for code, give FULL working code.\n"
                "- Always format code inside triple backticks ```.\n"
                "- Be clear and structured."
            )
        }
    ]

    # ✅ Validate & append history
    if isinstance(req.history, list):
        for msg in req.history:
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

    # ✅ Add current message
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
                    "max_tokens": 800,
                    "temperature": 0.7
                },
                timeout=20
            )

            # ❗ Handle non-JSON safely
            try:
                data = response.json()
            except:
                continue

            # ✅ Success
            if "choices" in data and len(data["choices"]) > 0:
                reply = data["choices"][0]["message"]["content"]

                return {
                    "reply": reply.strip(),
                    "model_used": model
                }

            # ❌ Log API error
            if "error" in data:
                print(f"[{model}] API ERROR:", data["error"])

        except requests.exceptions.Timeout:
            print(f"[{model}] Timeout")
        except Exception as e:
            print(f"[{model}] Error:", e)

    # ❌ All models failed
    return {
        "reply": "⚠️ All AI models are busy right now. Please try again."
    }

# ✅ TEST ROUTE
@app.get("/test")
def test():
    return {"status": "OpenRouter working"}
