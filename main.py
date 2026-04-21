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
        prompt = f"""
You are a helpful chatbot for a student website.
Answer clearly and simply.

User: {req.message}
"""

        response = model.generate_content(prompt)

        return {
            "reply": response.text
        }

    except Exception as e:
        # ✅ FULL ERROR OUTPUT (VERY IMPORTANT FOR DEBUGGING)
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }
