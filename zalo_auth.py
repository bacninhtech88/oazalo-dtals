import os
import requests

# URL để lấy thông tin OA (đã có của bạn)
ZALO_OA_INFO_URL = "https://openapi.zalo.me/v2.0/oa/getoa"
# URL để gửi tin nhắn phản hồi cho người dùng (API v3.0)
ZALO_SEND_MSG_URL = "https://openapi.zalo.me/v3.0/oa/message/cs"

def zalo_oa_connection():
    access_token = os.getenv("ZALO_OA_ACCESS_TOKEN")
    if not access_token:
        return {"status": "error", "error": "ZALO_OA_ACCESS_TOKEN not found"}

    headers = {"access_token": access_token}
    try:
        response = requests.get(ZALO_OA_INFO_URL, headers=headers, timeout=10)
        data = response.json()
        if data.get("error") == 0:
            return {
                "status": "success",
                "oa_name": data["data"].get("name"),
                "oa_id": data["data"].get("oa_id")
            }
        else:
            return {"status": "error", "zalo_error": data}
    except Exception as e:
        return {"status": "error", "exception": str(e)}

def send_zalo_message(user_id, text_message):
    """
    Gửi tin nhắn văn bản từ OA đến người dùng dựa trên user_id.
    """
    access_token = os.getenv("ZALO_OA_ACCESS_TOKEN")
    if not access_token:
        print("LỖI: Không tìm thấy ZALO_OA_ACCESS_TOKEN")
        return

    headers = {
        "Content-Type": "application/json",
        "access_token": access_token
    }

    payload = {
        "recipient": {"user_id": user_id},
        "message": {"text": text_message}
    }

    try:
        response = requests.post(ZALO_SEND_MSG_URL, headers=headers, json=payload, timeout=10)
        result = response.json()
        if result.get("error") == 0:
            print(f"Gửi tin nhắn thành công đến {user_id}")
        else:
            print(f"Lỗi khi gửi tin nhắn Zalo: {result}")
    except Exception as e:
        print(f"Exception khi gọi API Zalo: {str(e)}")