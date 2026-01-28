# analytic_python.py
from google_sheet import get_sheet_data

def analyze_warranty_logic(user_query: str):
    if not user_query:
        return {"status": "error", "message": "Thiếu từ khóa tìm kiếm"}

    raw_data = get_sheet_data()
    if isinstance(raw_data, str): # Trả về lỗi nếu không kết nối được
        return {"status": "error", "message": raw_data}

    query_clean = user_query.strip().lower()
    found_rows = []

    # Duyệt qua từng hàng trong Sheet
    for r_idx, row in enumerate(raw_data):
        # Chuyển toàn bộ hàng thành một chuỗi văn bản để tìm kiếm linh hoạt
        # row_str sẽ bao gồm cả: "Nguyễn văn B | KH2456 | 6785 | NX510"
        row_str = " ".join([str(cell).strip().lower() for cell in row if cell])
        
        if query_clean in row_str:
            found_rows.append({
                "hang": r_idx + 1,
                "chi_tiet": row
            })

    return {
        "user_query": user_query,
        "matching_results": len(found_rows),
        "data_for_ai": found_rows if found_rows else "Không tìm thấy thông tin phù hợp"
    }