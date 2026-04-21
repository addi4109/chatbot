import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
import os

# 🔐 API key from environment (IMPORTANT for deployment)
genai.configure(api_key="AIzaSyCqcuMPwt0JtFnzCp2OQJLolY6nqR9etDM")

model = genai.GenerativeModel("gemini-1.5-pro")

app = FastAPI()

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

        return {"reply": response.text}

    except Exception as e:
        return {"error": str(e)}
