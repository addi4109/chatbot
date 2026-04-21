from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        api_key = os.getenv("GEMINI_API_KEY")

        # 🔥 IMPORTANT: check at runtime, not startup
        if not api_key:
            return {"reply": "Missing GOOGLE_API_KEY in environment"}

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=req.message
        )

        return {"reply": response.text}

    except Exception as e:
        return {"reply": "Backend error", "error": str(e)}
