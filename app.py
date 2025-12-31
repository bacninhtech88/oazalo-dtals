# app.py
from fastapi import FastAPI
from ai_connect import test_chatgpt_connection

app = FastAPI()

@app.get("/")
def health_check():
    return {
        "status": "Server is running"
    }

@app.get("/test-chatgpt")
def test_chatgpt():
    return test_chatgpt_connection()
