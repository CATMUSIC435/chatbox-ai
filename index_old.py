import os
import httpx
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json
from pydantic import BaseModel
from langchain_core.documents import Document

from langchain_community.document_loaders import TextLoader
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
DB_PATH = "./db"
DATA_PATH = "data.txt"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "llama3.2"

app = FastAPI()
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

if os.path.exists(DB_PATH):
    db = Chroma(persist_directory=DB_PATH, embedding_function=embedding)
else:
    loader = TextLoader(DATA_PATH, encoding="utf-8")
    docs = loader.load()
    splits = text_splitter.split_documents(docs)
    
    db = Chroma.from_documents(splits, embedding, persist_directory=DB_PATH)
class ChatRequest(BaseModel):
    question: str

class LearnRequest(BaseModel):
    text: str
async def get_context_async(query):
    results = await db.asimilarity_search(query, k=3)
    return "\n".join([doc.page_content for doc in results])
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
    except httpx.ConnectError:
        return {"answer": "❌ Lỗi: Không thể kết nối đến Ollama. Vui lòng đảm bảo phần mềm Ollama đang chạy (11434)."}
    except httpx.TimeoutException:
        return {"answer": "❌ Lỗi: Ollama phản hồi quá lâu (Timeout)."}
    except Exception as e:
        return {"answer": f"❌ Lỗi AI: {str(e)}"}
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
    return StreamingResponse(generate(), media_type="text/plain")
@app.post("/learn")
async def learn_data(req: LearnRequest):
    try:
        new_docs = [Document(page_content=req.text, metadata={"source": "api_upload"})]
        splits = text_splitter.split_documents(new_docs)
        await db.aadd_documents(splits)
        
        return {
            "status": "success", 
            "message": f"🤖 Tớ đã nhét ngay {len(splits)} đoạn kiến thức nóng hổi vào não! Hỏi tớ thử xem."
        }
    except Exception as e:
        return {"status": "error", "message": f"❌ Lỗi: Không thể học được vì {str(e)}"}