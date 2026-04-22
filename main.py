from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# CORS (frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenRouter API Key (set in Render env)
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise Exception("OPENROUTER_API_KEY is not set in environment variables")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Chatbot API is running with OpenRouter"}

# CHAT ENDPOINT
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",   # optional
                "X-Title": "My Chatbot"               # optional
            },
            json={
                "model": "mistralai/mistral-7b-instruct",  # free model
                "messages": [
                    {"role": "user", "content": req.message}
                ]
            }
        )

        data = response.json()

        # handle errors safely
        if "choices" not in data:
            return {"reply": "Error: " + str(data)}

        return {
            "reply": data["choices"][0]["message"]["content"]
        }

    except Exception as e:
        print("CHAT ERROR:", e)
        return {"reply": "Server Error: " + str(e)}

# DEBUG ENDPOINT
@app.get("/test")
def test():
    return {"status": "OpenRouter working"}
