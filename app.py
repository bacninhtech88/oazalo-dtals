# app.py
from fastapi import FastAPI
from ai_connect import chatgpt_connection

app = FastAPI()

@app.get("/")
def health_check():
    return {
        "status": "Server is running"
    }

@app.get("/test-chatgpt")
def test_chatgpt():
    return chatgpt_connection()
