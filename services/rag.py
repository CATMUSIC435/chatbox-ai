import os
import json
import httpx
from langchain_community.document_loaders import TextLoader
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from core.config import DB_PATH, DATA_PATH, OLLAMA_URL, MODEL, DEFAULT_DOMAIN

embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

db_exists = os.path.exists(DB_PATH)
db = Chroma(persist_directory=DB_PATH, embedding_function=embedding)

if not db_exists and os.path.exists(DATA_PATH):
    loader = TextLoader(DATA_PATH, encoding="utf-8")
    docs = loader.load()
    for doc in docs:
        doc.metadata["domain"] = DEFAULT_DOMAIN
    db.add_documents(text_splitter.split_documents(docs))

async def get_context_async(query: str, domain: str = "default") -> str:
    results = await db.asimilarity_search(query, k=3, filter={"domain": domain})
    return "\n".join([doc.page_content for doc in results])

def build_prompt(context: str, question: str) -> str:
    return f"""Bạn là một chuyên gia tư vấn thông minh của hệ thống.
Dưới đây là các thông tin bạn được cấp phép sử dụng để trả lời:
<thông_tin>
{context}
</thông_tin>

YÊU CẦU TỐI THƯỢNG:
1. NẾU THÔNG TIN KHÔNG CÓ TRONG THẺ <thông_tin>, BẠN PHẢI TRẢ LỜI: "Xin lỗi, hiện tại tôi chưa được cung cấp thông tin về vấn đề này."
2. TUYỆT ĐỐI KHÔNG SỬ DỤNG KIẾN THỨC CÁ NHÂN ĐỂ BỊA ĐẶT CÂU TRẢ LỜI. CHỈ ĐƯỢC PHÉP TRẢ LỜI DỰA TRÊN <thông_tin> Ở TRÊN.
3. Không lải nhải "Dựa vào thông tin được cấp", hãy đi thẳng vào vấn đề.

Câu hỏi của khách: {question}

BẮT BUỘC: Ở cuối câu trả lời, bạn phải tạo ra 3 câu hỏi gợi ý để dẫn dắt khách hàng. Cấu trúc PHẢI như sau (không được sai lệch):
---SUGGESTIONS---
- Gợi ý 1
- Gợi ý 2
- Gợi ý 3

Trả lời:
"""

async def stream_ollama_response(prompt: str):
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            async with client.stream(
                "POST", OLLAMA_URL,
                json={"model": MODEL, "prompt": prompt, "stream": True}
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        data = json.loads(line)
                        yield data.get("response", "")
    except Exception as e:
        yield f"\n❌ Lỗi kết nối AI: {str(e)}"

async def send_ollama_query(prompt: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            res = await client.post(
                OLLAMA_URL,
                json={"model": MODEL, "prompt": prompt, "stream": False}
            )
            res.raise_for_status()
        data = res.json()
        return data.get("response", "❌ Error")
    except Exception as e:
        return f"❌ Error: {str(e)}"

async def learn_new_text(text: str, domain: str = "default") -> int:
    new_docs = [Document(page_content=text, metadata={"source": "api_upload", "domain": domain})]
    splits = text_splitter.split_documents(new_docs)
    await db.aadd_documents(splits)
    return len(splits)

async def delete_domain_knowledge(domain: str) -> int:
    try:
        result = db.get(where={"domain": domain})
        ids = result.get("ids", [])
        if ids:
            db.delete(ids=ids)
            return len(ids)
        return 0
    except Exception as e:
        raise e
