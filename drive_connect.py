# ====================================================================
# FILE: drive_connect.py - Xử lý Google Drive và Vectorstore (Dùng Env JSON)
# ====================================================================

import os
import io
import json
from dotenv import load_dotenv

# LangChain và Google Drive Imports
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Tải biến môi trường
load_dotenv()

# ==== Cấu hình API ====
# Lấy nội dung JSON trực tiếp từ biến môi trường trên Render
GCP_JSON_STR = os.getenv("GCP_CREDENTIALS_JSON")
DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")
TEMP_DATA_DIR = "/tmp/data"
CHROMA_DB_DIR = "/tmp/chroma_db"

def setup_vectorstore():
    """
    Xác thực Google Drive từ biến môi trường, tải tài liệu, 
    xử lý và trả về Vectorstore (ChromaDB).
    """
    
    # 1. Xác thực Google Drive sử dụng JSON từ biến môi trường
    print("Bắt đầu: Xác thực Google Drive...")
    try:
        if not GCP_JSON_STR:
            raise Exception("Không tìm thấy biến môi trường GCP_CREDENTIALS_JSON")
        
        # Chuyển đổi chuỗi JSON từ env thành dict
        info = json.loads(GCP_JSON_STR)
        creds = service_account.Credentials.from_service_account_info(info)
        drive_service = build("drive", "v3", credentials=creds)
        print("Hoàn tất: Xác thực Google Drive thành công.")
    except Exception as e:
        print(f"LỖI FATAL khi xác thực: {e}")
        raise e

    # 2. Tải tài liệu từ Drive
    os.makedirs(TEMP_DATA_DIR, exist_ok=True)
    print(f"Bắt đầu: Tải tài liệu từ Folder ID {DRIVE_FOLDER_ID}...")
    
    try:
        results = drive_service.files().list(
            q=f"'{DRIVE_FOLDER_ID}' in parents and trashed=false",
            fields="files(id, name)"
        ).execute()
        files = results.get("files", [])
        
        for file in files:
            file_path = os.path.join(TEMP_DATA_DIR, file["name"])
            # Tải file nếu chưa tồn tại trong thư mục tạm
            if not os.path.exists(file_path):
                request = drive_service.files().get_media(fileId=file["id"])
                with io.FileIO(file_path, "wb") as fh:
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while not done:
                        _, done = downloader.next_chunk()
                print(f"   -> Đã tải: {file['name']}")
    except Exception as e:
        print(f"Lỗi khi tải file từ Drive: {e}")

    print("Hoàn tất: Tải tài liệu Drive.")

    # 3. Xử lý tài liệu (Load & Split)
    print("Bắt đầu: Xử lý và chia nhỏ tài liệu...")
    docs = []
    if os.path.exists(TEMP_DATA_DIR):
        for filename in os.listdir(TEMP_DATA_DIR):
            filepath = os.path.join(TEMP_DATA_DIR, filename)
            if os.path.getsize(filepath) == 0: continue
            
            if filename.endswith(".pdf"):
                docs.extend(PyPDFLoader(filepath).load())
            elif filename.endswith(".txt"):
                docs.extend(TextLoader(filepath).load())
            elif filename.endswith(".docx"):
                docs.extend(Docx2txtLoader(filepath).load())
            
    if not docs:
        print("CẢNH BÁO: Không có tài liệu nào để xử lý.")
        # Trả về vectorstore trống hoặc xử lý tùy ý
        
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)
    print(f"Hoàn tất: Đã chia thành {len(splits)} đoạn văn.")

    # 4. Tạo Vectorstore (Chroma)
    print("Bắt đầu: Tạo Vectorstore (Embedding)...")
    embedding = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        persist_directory=CHROMA_DB_DIR
    )
    print("✅ Hoàn tất: Vectorstore đã sẵn sàng.")
    
    return vectorstore

# Khởi tạo duy nhất một lần khi ứng dụng bắt đầu
VECTORSTORE = setup_vectorstore()

def get_vectorstore():
    return VECTORSTORE