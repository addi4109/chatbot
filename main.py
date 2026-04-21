from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
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

# API KEY (Render environment variable)
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise Exception("GOOGLE_API_KEY is not set in environment variables")

# Gemini client
client = genai.Client(api_key=api_key)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Chatbot API is running"}

# CHAT ENDPOINT
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        response = client.models.generate_content(
            model="models/gemini-2.0-flash",   # ✅ SAFE + AVAILABLE from your list
            contents=req.message
        )
        return {"reply": response.text}

    except Exception as e:
        print("CHAT ERROR:", e)
        return {"reply": str(e)}

# MODEL LIST (debug)
@app.get("/models")
def list_models():
    try:
        models = client.models.list()
        return {"models": [m.name for m in models]}
    except Exception as e:
        print("MODEL ERROR:", e)
        return {"error": str(e)}
