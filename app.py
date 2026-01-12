# app.py
from fastapi import FastAPI , Request
from fastapi.responses import HTMLResponse
from ai_connect import chatgpt_connection
from zalo_auth import zalo_oa_connection

from drive_connect import get_vectorstore

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
async def zalo_webhook(request: Request):
    # Lấy toàn bộ dữ liệu Zalo gửi sang
    body = await request.json()

    # In ra log để bạn nhìn thấy trên Render
    print("--- NHẬN ĐƯỢC WEBHOOK ---")
    print(body)
    print("--------------------------")

    # Trả về 200 OK ngay lập tức cho Zalo
    return {"status": "success"}


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
