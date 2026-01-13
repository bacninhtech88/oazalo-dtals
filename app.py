# app.py
from fastapi import FastAPI , Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from ai_connect import chatgpt_connection
from zalo_auth import zalo_oa_connection

from drive_connect import get_vectorstore

from ai_answer import get_rag_answer
from zalo_auth import send_zalo_message

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

@app.post("/webhook")
# kiểm tra kết nối webhook
# async def zalo_webhook(request: Request):
#     body = await request.json()
#     print("--- NHẬN ĐƯỢC WEBHOOK ---")
#     print(body)
#     print("--------------------------")
#     return {"status": "success"}
#kết thúc kiểm tra kết nối webhook
async def zalo_webhook(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    
    # Kiểm tra nếu là tin nhắn văn bản từ người dùng
    if body.get("event_name") == "user_send_text":
        sender_id = body.get("sender", {}).get("id")
        user_text = body.get("message", {}).get("text")
        
        # Đưa vào hàng đợi xử lý ngầm
        background_tasks.add_task(process_and_reply, sender_id, user_text)
        
    return {"status": "ok"}




@app.get("/check-drive")
async def check_drive():
    try:
        # Gọi vectorstore đã được khởi tạo trong drive_connect.py
        vectorstore = get_vectorstore()
        
        # Đếm số lượng mẩu dữ liệu đã học được từ các file PDF/Docx
        count = vectorstore._collection.count()
        
        return {
            "status": "success",
            "folder_id": "Đã kết nối", # Có thể lấy từ os.getenv("DRIVE_FOLDER_ID")
            "total_documents_chunks": count,
            "message": "Kết nối Google Drive và ChromaDB hoạt động tốt!"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Lỗi kết nối Drive: {str(e)}"
        }

async def process_and_reply(sender_id: str, user_text: str):
    # 1. Gọi AI xử lý dựa trên dữ liệu Google Drive
    bot_reply = await get_rag_answer(user_text)
    
    # 2. Gửi tin nhắn trả lời lại cho người dùng qua Zalo
    # Bạn cần hoàn thiện hàm này trong zalo_auth.py
    send_zalo_message(sender_id, bot_reply)

