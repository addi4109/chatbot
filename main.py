import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

# 🔐 Correct API key usage (IMPORTANT)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ Use stable model
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

# ✅ FIX: CORS (this fixes Failed to fetch)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict later if needed
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

        # ✅ Safe response handling
        return {
            "reply": response.text if response.text else "No response from AI"
        }

    except Exception as e:
        # 🔥 FULL ERROR (for debugging)
        return {
            "reply": "Error occurred in backend",
            "error": str(e)
        }
