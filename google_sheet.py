# google_sheet.py
import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()

# def get_sheet_data():
#     """Kết nối và lấy dữ liệu từ Google Sheet"""
#     try:
#         # 1. Cấu hình phạm vi truy cập
#         scope = [
#             "https://spreadsheets.google.com/feeds",
#             "https://www.googleapis.com/auth/drive"
#         ]
        
#         # 2. Xác thực từ biến môi trường đã có
#         creds_json = json.loads(os.getenv("GCP_CREDENTIALS_JSON"))
#         creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
#         client = gspread.authorize(creds)
#         SHEET_ID = "1MPL86dM26ypGQHCDDwN-eCL3kENvg8821dwRS7pYxgI"
#         # 3. Mở file theo tên bạn đã đặt trên Drive
#         # Thay "Ví dụ Bảo hành" bằng tên file thực tế của bạn
#         sheet = client.open_by_key(SHEET_ID).sheet1
#         # sheet = client.open("Ví dụ Bảo hành").sheet1 
        
#         return sheet.get_all_values()
#     except Exception as e:
#         print(f"Lỗi kết nối Google Sheet: {e}")
#         return []


def get_sheet_data():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_raw = os.getenv("GCP_CREDENTIALS_JSON")
        
        if not creds_raw:
            return "LOI: Bien moi truong GCP_CREDENTIALS_JSON dang trong"

        creds_json = json.loads(creds_raw)
        
        # DÒNG QUAN TRỌNG: In email thực tế đang chạy trên Render ra Log
        current_email = creds_json.get('client_email')
        print(f"--- KIEM TRA EMAIL: {current_email} ---")
        
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
        client = gspread.authorize(creds)

        # ID Sheet của bạn
        SHEET_ID = "1MPL86dM26ypGQHCDDwN-eCL3kENvg8821dwRS7pYxgI"
        
        # Thử mở Sheet
        sheet = client.open_by_key(SHEET_ID).sheet1
        return sheet.get_all_values()

    except Exception as e:
        # Ép kiểu string để Log Render bắt buộc phải hiện nội dung lỗi
        error_msg = str(e)
        print(f"--- LOI CHI TIET: {error_msg} ---")
        return f"Error: {error_msg}"

def search_warranty(machine_id):
    """Tìm kiếm thông tin bảo hành theo mã máy"""
    data = get_sheet_data()
    machine_id_str = str(machine_id).strip().lower()
    
    for row in data:
        # Giả sử cột trong Sheet của bạn tên là "Mã Máy"
        if str(row.get('Mã Máy', '')).strip().lower() == machine_id_str:
            return row
    return None