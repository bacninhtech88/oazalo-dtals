# analytic_python.py
from google_sheet import get_sheet_data  # Giả sử hàm này trả về list các hàng

def analyze_warranty_logic(user_query):
    """
    Hàm phân tích dữ liệu dựa trên câu hỏi.
    Ở giai đoạn này, ta sẽ chuẩn bị 'Context' tốt nhất để sau này đưa vào AI.
    """
    # 1. Lấy dữ liệu từ Google Sheet
    raw_rows = get_sheet_data()
    
    # 2. Xử lý logic tìm kiếm sơ bộ (không cần AI) để kiểm tra độ chính xác
    # Tìm xem trong query của khách có chứa mã nào trong Sheet không
    found_info = []
    query_lower = user_query.lower()
    
    for row in raw_rows:
        # Chuyển hàng thành chuỗi để tìm kiếm nhanh
        row_str = " ".join([str(cell) for cell in row]).lower()
        
        # Nếu bất kỳ ô nào trong hàng xuất hiện trong câu hỏi (ví dụ mã máy)
        # Hoặc ngược lại (mã máy trong hàng xuất hiện trong câu hỏi)
        for cell in row:
            cell_str = str(cell).strip().lower()
            if cell_str and cell_str in query_lower:
                found_info.append(row)
                break

    # 3. Giả lập cấu trúc mà ta sẽ gửi cho AI API sau này
    analysis_result = {
        "user_query": user_query,
        "matching_rows_found": len(found_info),
        "data_sent_to_ai": found_info,
        "prompt_preview": f"Dữ liệu tìm thấy: {found_info}. Hãy trả lời câu hỏi: {user_query}"
    }
    
    return analysis_result