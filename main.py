from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import os

app = FastAPI()

# CORS setup (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Request model
class ChatRequest(BaseModel):
    message: str

# Health check route
@app.get("/")
def home():
    return {"message": "Chatbot API is running"}

# Chat route
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash-001",
            contents=req.message
        )

        return {"reply": response.text}

    except Exception as e:
        # IMPORTANT: proper indentation fixed
        print("REAL ERROR:", e)
        return {"reply": str(e)}
