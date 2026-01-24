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


import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

def get_sheet_data():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        # 1. Kiểm tra xác thực
        creds_raw = os.getenv("GCP_CREDENTIALS_JSON")
        if not creds_raw:
            return [{"error": "Thieu biến môi trường GCP_CREDENTIALS_JSON"}]
            
        creds_json = json.loads(creds_raw)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
        client = gspread.authorize(creds)

        # 2. Sử dụng ID chính xác từ ảnh của bạn
        SHEET_ID = "1MPL86dM26ypGQHCDDwN-eCL3kENvg8821dwRS7pYxgI"
        
        # 3. Mở và lấy giá trị thô (Dùng get_all_values để tránh lỗi tiêu đề)
        sheet = client.open_by_key(SHEET_ID).sheet1
        data = sheet.get_all_values() 
        
        return data
    except Exception as e:
        # In lỗi cực kỳ chi tiết ra Log
        print(f"--- LOI DOC SHEET: {str(e)} ---")
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