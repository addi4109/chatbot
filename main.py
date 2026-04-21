import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import traceback

# 🔐 API KEY (Render ENV recommended)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

# ✅ FIX: CORS (THIS FIXES "Failed to fetch")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for testing (you can restrict later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Chatbot backend is running"}

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        prompt = f"You are a helpful chatbot. User: {req.message}"

        response = model.generate_content(prompt)

        text = getattr(response, "text", None)

        return {
            "reply": text or "No response from AI"
        }

    except Exception as e:
        return {"reply": "Error", "error": str(e)}
