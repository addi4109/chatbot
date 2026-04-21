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

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Chatbot API is running"}

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash-001",
            contents=req.message
        )

        return {"reply": response.text}

    except Exception as e:
    print("REAL ERROR:", e)
    return {"reply": str(e)}
