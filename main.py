from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import os

# 🔐 Load API key from environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise Exception("GOOGLE_API_KEY is not set in environment variables")

# 🤖 Initialize Gemini client (NEW SDK)
client = genai.Client(api_key=API_KEY)

app = FastAPI()

# 🌐 CORS (allow frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change later to your domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📩 Request model
class ChatRequest(BaseModel):
    message: str

# 🏠 Health check route
@app.get("/")
def home():
    return {"status": "ok", "message": "Chatbot backend is running 🚀"}

# 💬 Chat endpoint
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        if not req.message:
            return {"reply": "Please send a message"}

        # 🧠 Prompt (you can customize personality here)
        prompt = f"""
You are a helpful AI assistant for students.
Explain clearly and simply.

User: {req.message}
"""

        # 🤖 Gemini response
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        return {
            "reply": response.text
        }

    except Exception as e:
        # ❌ Full debug response (important for Render logs)
        return {
            "reply": "Something went wrong in backend",
            "error": str(e)
        }
