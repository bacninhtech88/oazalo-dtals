# google_sheet.py
import gspread
import json
import os
import traceback
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


# def get_sheet_data():
#     try:
#         scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#         creds_raw = os.getenv("GCP_CREDENTIALS_JSON")
        
#         if not creds_raw:
#             return "LOI: Bien moi truong GCP_CREDENTIALS_JSON dang trong"

#         creds_json = json.loads(creds_raw)
        
#         # DÒNG QUAN TRỌNG: In email thực tế đang chạy trên Render ra Log
#         current_email = creds_json.get('client_email')
#         print(f"--- KIEM TRA EMAIL: {current_email} ---")
        
#         creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
#         client = gspread.authorize(creds)

#         # ID Sheet của bạn
#         SHEET_ID = "1MPL86dM26ypGQHCDDwN-eCL3kENvg8821dwRS7pYxgI"
        
#         # Thử mở Sheet
#         sheet = client.open_by_key(SHEET_ID).worksheet("Bảo hành")
#         return sheet.get_all_values()

#     except Exception as e:
#         # Ép kiểu string để Log Render bắt buộc phải hiện nội dung lỗi
#         error_msg = str(e)
#         print(f"--- LOI CHI TIET: {error_msg} ---")
#         return f"Error: {error_msg}"


def get_sheet_data():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        # 1. Kiểm tra biến môi trường
        creds_raw = os.getenv("GCP_CREDENTIALS_JSON")
        if not creds_raw:
            return "Lỗi: Biến GCP_CREDENTIALS_JSON đang trống hoặc chưa được cài trên Render."
            
        # 2. Thử giải mã JSON
        try:
            creds_json = json.loads(creds_raw)
        except Exception as json_err:
            return f"Lỗi định dạng JSON: {str(json_err)}. Hãy kiểm tra xem bạn có dán thiếu dấu ngoặc nào không."
        
        # 3. Xác thực
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
        client = gspread.authorize(creds)

        # 4. Mở Spreadsheet
        SHEET_ID = "1MPL86dM26ypGQHCDDwN-eCL3kENvg8821dwRS7pYxgI"
        try:
            spreadsheet = client.open_by_key(SHEET_ID)
        except Exception as open_err:
            return f"Lỗi không mở được file Sheet (ID sai hoặc chưa share quyền): {str(open_err)}"

        # 5. Mở tab 'Bảo hành'
        try:
            sheet = spreadsheet.worksheet("Bảo hành")
            return sheet.get_all_values()
        except gspread.exceptions.WorksheetNotFound:
            # Nếu không tìm thấy, lấy danh sách tab để báo lỗi cho chuẩn
            all_tabs = [ws.title for ws in spreadsheet.worksheets()]
            return f"Không thấy tab 'Bảo hành'. Các tab hiện có là: {all_tabs}"

    except Exception as e:
        # In chi tiết lỗi ra màn hình Console của Render
        print("--- LỖI HỆ THỐNG CHI TIẾT ---")
        traceback.print_exc()
        return f"Lỗi chưa xác định: {type(e).__name__} - {str(e)}"

def search_warranty(machine_id):
    """Tìm kiếm thông tin bảo hành theo mã máy"""
    data = get_sheet_data()
    machine_id_str = str(machine_id).strip().lower()
    
    for row in data:
        # Giả sử cột trong Sheet của bạn tên là "Mã Máy"
        if str(row.get('Mã Máy', '')).strip().lower() == machine_id_str:
            return row
    return None