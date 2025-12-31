# ai_service.py
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chatgpt_connection():
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a test bot."},
                {"role": "user", "content": "Ping"}
            ],
            max_tokens=10
        )
        return {
            "status": "success",
            "reply": response.choices[0].message.content
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
