# analytic_python.py
from google_sheet import get_sheet_data

def analyze_warranty_logic(user_query: str):
    if not user_query:
        return {"error": "Thiếu câu hỏi"}

    # Lấy dữ liệu thô (mảng 2 chiều)
    raw_data = get_sheet_data()
    query_clean = user_query.strip().lower()
    
    # BƯỚC 1: Xây dựng bản đồ dữ liệu có địa chỉ
    structured_map = []
    for r_idx, row in enumerate(raw_data):
        for c_idx, cell in enumerate(row):
            val = str(cell).strip()
            if val:
                # Lưu giá trị kèm tọa độ: R (Row), C (Column)
                # Ví dụ: {"pos": "R2C5", "val": "NX510"}
                structured_map.append({
                    "pos": f"R{r_idx + 1}C{c_idx + 1}", 
                    "val": val
                })

    # BƯỚC 2: Tìm kiếm thông minh dựa trên tọa độ
    # Tìm tất cả các ô có chứa từ khóa
    matches = [item for item in structured_map if query_clean in item['val'].lower()]

    # BƯỚC 3: Phân tích vùng lân cận (Contextual Analysis)
    # Nếu tìm thấy một ô, ta sẽ lấy toàn bộ các ô cùng hàng và cùng cột để AI hiểu ngữ cảnh
    detailed_context = []
    for m in matches:
        row_num = m['pos'].split('C')[0] # Lấy "R2" chẳng hạn
        # Lấy tất cả các ô nằm cùng hàng với ô vừa tìm thấy
        related_cells = [i['val'] for i in structured_map if i['pos'].startswith(row_num)]
        detailed_context.append(f"Tại địa chỉ {row_num}: {' | '.join(related_cells)}")

    return {
        "user_query": user_query,
        "matching_results": len(matches),
        "data_sent_to_ai": "\n".join(detailed_context)
    }