# google_sheet.py
import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()

def get_sheet_data():
    """Kết nối và lấy dữ liệu từ Google Sheet"""
    try:
        # 1. Cấu hình phạm vi truy cập
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # 2. Xác thực từ biến môi trường đã có
        creds_json = json.loads(os.getenv("GCP_CREDENTIALS_JSON"))
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
        client = gspread.authorize(creds)

        # 3. Mở file theo tên bạn đã đặt trên Drive
        # Thay "Ví dụ Bảo hành" bằng tên file thực tế của bạn
        sheet = client.open("Ví dụ Bảo hành").sheet1 
        
        return sheet.get_all_records()
    except Exception as e:
        print(f"Lỗi kết nối Google Sheet: {e}")
        return []

def search_warranty(machine_id):
    """Tìm kiếm thông tin bảo hành theo mã máy"""
    data = get_sheet_data()
    machine_id_str = str(machine_id).strip().lower()
    
    for row in data:
        # Giả sử cột trong Sheet của bạn tên là "Mã Máy"
        if str(row.get('Mã Máy', '')).strip().lower() == machine_id_str:
            return row
    return None