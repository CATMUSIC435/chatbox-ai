import io
import json
import PyPDF2
from docx import Document
import pandas as pd
from fastapi import UploadFile

async def extract_text_from_file(file: UploadFile) -> str:
    """
    Nhận một file UploadFile từ FastAPI và trích xuất toàn bộ nội dung text 
    dựa trên định dạng file (txt, pdf, docx, csv, xlsx, json).
    """
    content = await file.read()
    filename = file.filename.lower()
    
    if filename.endswith(".txt"):
        return content.decode("utf-8", errors="ignore")
        
    elif filename.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        text = ""
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text
        
    elif filename.endswith(".docx"):
        doc = Document(io.BytesIO(content))
        return "\n".join([p.text for p in doc.paragraphs])
        
    elif filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(content))
        return df.to_string()
        
    elif filename.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(content))
        return df.to_string()
        
    elif filename.endswith(".json"):
        try:
            data = json.loads(content.decode("utf-8", errors="ignore"))
            return json.dumps(data, ensure_ascii=False, indent=2)
        except Exception:
            return content.decode("utf-8", errors="ignore")
            
    else:
        raise ValueError(f"Định dạng file không được hỗ trợ: {filename}")
