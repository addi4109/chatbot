from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import os

app = FastAPI()

# 🌐 CORS (frontend access fix)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📩 Request format
class ChatRequest(BaseModel):
    message: str

# 🏠 Health check
@app.get("/")
def home():
    return {"status": "ok", "message": "Chatbot backend running"}

# 💬 Chat endpoint
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        # 🔑 MUST MATCH Render env variable name
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            return {"reply": "API key missing. Set GOOGLE_API_KEY in Render."}

        # 🤖 Gemini client
        client = genai.Client(api_key=api_key)

        # 🧠 AI response
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=req.message
        )

        return {
            "reply": response.text
        }

    except Exception as e:
        return {
            "reply": "Backend error occurred",
            "error": str(e)
        }
