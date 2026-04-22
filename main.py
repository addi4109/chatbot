from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# ✅ CORS (frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Correct Environment Variable
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise Exception("OPENROUTER_API_KEY is not set in environment variables")

# ✅ Request Model
class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Chatbot API is running with OpenRouter"}

# ✅ List of working models (auto fallback)
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
        "HTTP-Referer": "http://localhost",  # optional
        "X-Title": "My Chatbot"
    }

    for model in MODELS:
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
json={
    "model": model,
    "messages": [
        {
            "role": "system",
            "content": "Reply in short, clear answers. Max 3-4 lines. No long paragraphs."
        },
        {
            "role": "user",
            "content": req.message
        }
    ],
    "max_tokens": 100
}
            )

            data = response.json()

            # ✅ Success
            if "choices" in data:
                return {
                    "reply": data["choices"][0]["message"]["content"],
                    "model_used": model
                }

        except Exception as e:
            print(f"Error with model {model}:", e)

    # ❌ If all models fail
    return {"reply": "All AI models are currently busy. Try again later."}

# ✅ TEST ENDPOINT
@app.get("/test")
def test():
    return {"status": "OpenRouter working"}
