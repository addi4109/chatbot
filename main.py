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

# ✅ Working Models
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
        "HTTP-Referer": "http://localhost",
        "X-Title": "My Chatbot"
    }

    # 🔥 Smart system prompt
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful AI assistant.\n"
                "- Give short answers (2-3 lines) for normal questions.\n"
                "- If user asks for code/program, give full working code.\n"
                "- Format code properly using code blocks.\n"
                "- Remember user's name if provided."
            )
        }
    ]

    # ✅ Add previous history
    for msg in req.history:
        messages.append(msg)

    # ✅ Add current message
    messages.append({
        "role": "user",
        "content": req.message
    })

    # 🔁 Try models
    for model in MODELS:
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json={
                    "model": model,
                    "messages": messages,
                    "max_tokens": 500,   # 🔥 increased for code
                    "temperature": 0.7
                },
                timeout=15
            )

            data = response.json()

            # ✅ Debug print (optional)
            print("API Response:", data)

            if "choices" in data:
                reply = data["choices"][0]["message"]["content"]

                return {
                    "reply": reply,
                    "model_used": model
                }

            # ❌ If API returns error
            if "error" in data:
                print("API ERROR:", data["error"])

        except Exception as e:
            print(f"Error with model {model}:", e)

    return {"reply": "All AI models are busy. Try again later."}


# ✅ TEST
@app.get("/test")
def test():
    return {"status": "OpenRouter working"}
