# app.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from ai_connect import chatgpt_connection
from zalo_auth import zalo_oa_connection

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta property="zalo-platform-site-verification"
      content="S_-JSvNAFNjqlAmjgiy44dYviGYKpsLLDJ8s" />
</head>
<body>
There Is No Limit To What You Can Accomplish Using Zalo!
</body>
</html>"""

@app.get("/test-chatgpt")
def test_chatgpt():
    return chatgpt_connection()

@app.get("/test-zalo")
def test_zalo():
    return zalo_oa_connection()




