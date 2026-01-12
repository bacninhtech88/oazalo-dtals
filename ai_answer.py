import os
from openai import OpenAI
from drive_connect import get_vectorstore # Kết nối với 95 đoạn văn bản đã nạp
from dotenv import load_dotenv

load_dotenv()

# Khởi tạo OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def get_rag_answer(user_query: str):
    try:
        # 1. Lấy dữ liệu từ Vectorstore (ChromaDB)
        vectorstore = get_vectorstore()
        
        # 2. Tìm kiếm các đoạn văn bản liên quan nhất (ví dụ lấy 3 đoạn)
        # Hệ thống sẽ tìm trong 95 chunks bạn đã load thành công
        docs = vectorstore.similarity_search(user_query, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # 3. Xây dựng Prompt cho ChatGPT
        system_prompt = f"""
        Bạn là trợ lý AI của Công ty CP Nền tảng số DTALS.
        Hãy trả lời câu hỏi của khách hàng một cách lịch sự dựa trên thông tin được cung cấp dưới đây.
        Nếu thông tin không có trong tài liệu, hãy trả lời rằng bạn chưa có thông tin về vấn đề này và mời khách hàng liên hệ hotline.

        THÔNG TIN TÀI LIỆU:
        {context}
        """

        # 4. Gọi ChatGPT xử lý
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Hoặc gpt-4o
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            temperature=0.3 # Thấp để trả lời chính xác theo tài liệu
        )
        
        return response.choices[0].message.content

    except Exception as e:
        print(f"Lỗi tại ai_answer.py: {e}")
        return "Xin lỗi, hệ thống AI đang bận. Vui lòng thử lại sau ít phút."