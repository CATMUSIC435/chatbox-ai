import os
import httpx
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json
from pydantic import BaseModel
from langchain_core.documents import Document

from langchain_community.document_loaders import TextLoader
import warnings
# Bỏ qua warning không quan trọng của Langchain bản cũ nếu chưa update
warnings.filterwarnings("ignore", category=DeprecationWarning)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ===== CONFIG =====
DB_PATH = "./db"
DATA_PATH = "data.txt"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "llama3.2"

app = FastAPI()

# ===== LOAD DB (chỉ load 1 lần) =====
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Khởi tạo công cụ cắt chữ để dùng chung toàn hệ thống
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

if os.path.exists(DB_PATH):
    db = Chroma(persist_directory=DB_PATH, embedding_function=embedding)
else:
    loader = TextLoader(DATA_PATH, encoding="utf-8")
    docs = loader.load()
    
    # Sửa lỗi 1: Cắt nhỏ file text (chunking) để tránh quá giới hạn model & tìm từ khóa chính xác hơn
    splits = text_splitter.split_documents(docs)
    
    db = Chroma.from_documents(splits, embedding, persist_directory=DB_PATH)
    # db.persist()  # Lỗi 2: Không cần gọi hàm này nữa ở Chroma phiên bản mới (bị deprecate/báo lỗi)

# ===== REQUEST MODEL =====
class ChatRequest(BaseModel):
    question: str

class LearnRequest(BaseModel):
    text: str

# ===== GET CONTEXT =====
async def get_context_async(query):
    # Dùng hàm async (asimilarity_search) để TỐI ƯU CÙNG LÚC NHIỀU NGƯỜI DÙNG. 
    # Hàm này không đóng băng toàn bộ hệ thống API trong khi đi lục tìm DB
    results = await db.asimilarity_search(query, k=3)
    return "\n".join([doc.page_content for doc in results])

# ===== PROMPT =====
def build_prompt(context, question):
    return f"""
Bạn là chuyên viên tư vấn bất động sản.

- Không bịa
- Trả lời ngắn gọn
- Thân thiện

Thông tin:
{context}

Câu hỏi: {question}

Trả lời:
"""

# ===== API =====
@app.post("/chat")
async def chat(req: ChatRequest):
    context = await get_context_async(req.question)
    prompt = build_prompt(context, req.question)

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            res = await client.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": False
                }
            )
            res.raise_for_status() # Kiểm tra và ném lỗi HTTP (ví dụ đường dẫn sai, server sập)
            
        data = res.json()
        return {
            "answer": data.get("response", "❌ Không tìm thấy trường 'response' từ AI")
        }
        
    # Sửa lỗi 3: Xử lý các ngoại lệ (Exception) hay gặp khi gọi API Ollama
    except httpx.ConnectError:
        return {"answer": "❌ Lỗi: Không thể kết nối đến Ollama. Vui lòng đảm bảo phần mềm Ollama đang chạy (11434)."}
    except httpx.TimeoutException:
        return {"answer": "❌ Lỗi: Ollama phản hồi quá lâu (Timeout)."}
    except Exception as e:
        return {"answer": f"❌ Lỗi AI: {str(e)}"}

# ===== API STREAMING (CHẠY SIÊU NHANH) =====
@app.post("/chat-stream")
async def chat_stream(req: ChatRequest):
    context = await get_context_async(req.question)
    prompt = build_prompt(context, req.question)

    async def generate():
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                async with client.stream(
                    "POST",
                    OLLAMA_URL,
                    json={
                        "model": MODEL,
                        "prompt": prompt,
                        "stream": True  # Bật chế độ stream của Ollama
                    }
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line:
                            data = json.loads(line)
                            yield data.get("response", "")
        except Exception as e:
            yield f"❌ Lỗi: {str(e)}"

    # Trả về từng chữ một ngay lập tức (giống hệt ChatGPT gõ chữ)
    return StreamingResponse(generate(), media_type="text/plain")

# ===== API HỌC KIẾN THỨC MỚI (TỰ ĐỘNG CẬP NHẬT LIÊN TỤC) =====
@app.post("/learn")
async def learn_data(req: LearnRequest):
    try:
        # Bọc chữ của người dùng truyền lên vào Document trắng
        new_docs = [Document(page_content=req.text, metadata={"source": "api_upload"})]
        
        # Cắt nhỏ văn bản bằng công cụ text_splitter
        splits = text_splitter.split_documents(new_docs)
        
        # Thêm kiến thức trực tiếp vào Database. 
        # aadd_documents chạy ngầm (async) giúp không bị lag ngay cả khi có rất nhiều user
        await db.aadd_documents(splits)
        
        return {
            "status": "success", 
            "message": f"🤖 Tớ đã nhét ngay {len(splits)} đoạn kiến thức nóng hổi vào não! Hỏi tớ thử xem."
        }
    except Exception as e:
        return {"status": "error", "message": f"❌ Lỗi: Không thể học được vì {str(e)}"}