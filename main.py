from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import os

# ✅ Initialize Gemini client (NEW SDK)
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

# ✅ CORS FIX (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body
class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Chatbot backend is running 🚀"}

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        prompt = f"""
You are a helpful AI assistant for students.
Explain everything in a simple and clear way.

User: {req.message}
"""

        # ✅ New Gemini API call
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        return {
            "reply": response.text
        }

    except Exception as e:
        return {
            "reply": "Error occurred in backend",
            "error": str(e)
        }
