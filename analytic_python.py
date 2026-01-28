# analytic_python.py
from google_sheet import get_sheet_data

def analyze_warranty_logic(user_query: str):
    raw_data = get_sheet_data()
    
    # TRƯỜNG HỢP 1: Lỗi kết nối (trả về chuỗi lỗi thay vì list)
    if isinstance(raw_data, str):
        return {"status": "Lỗi kết nối", "detail": raw_data}

    # TRƯỜNG HỢP 2: Sheet trống rỗng
    if not raw_data:
        return {"status": "Sheet trống", "detail": "Đã vào được sheet nhưng không có dữ liệu"}

    query_clean = user_query.strip().lower()
    found_info = []
    
    # NỘI SOI: Kiểm tra 5 dòng đầu tiên để xem cấu trúc thực tế
    preview = raw_data[:5] 

    for r_idx, row in enumerate(raw_data):
        row_str = " ".join([str(c).lower() for c in row])
        if query_clean in row_str:
            found_info.append({"hàng": r_idx + 1, "nội_dung": row})

    return {
        "user_query": user_query,
        "tong_so_hang_thay": len(raw_data),
        "so_cot_dong_1": len(raw_data[0]) if raw_data else 0,
        "ket_qua_tim_kiem": found_info,
        "noi_soi_5_dong_dau": preview,
        "loi_khuyen": "Nếu 'noi_soi' hiện toàn ô trống, hãy kiểm tra lại tab 'Bảo hành' có đúng dữ liệu không."
    }