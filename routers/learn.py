from fastapi import APIRouter, File, UploadFile, HTTPException, Header
from models.schemas import LearnRequest
from services.rag import learn_new_text, delete_domain_knowledge
from services.parsers import extract_text_from_file
from core import config

router = APIRouter(prefix="/learn", tags=["Continuous Learning"])

@router.post("")
async def learn_data(req: LearnRequest, x_api_key: str = Header("None")):
    if x_api_key != config.API_KEY_SECRET:
        raise HTTPException(status_code=403, detail="Từ chối truy cập: API Key không đúng!")
        
    """API học kiến thức mới từ một đoạn text (dạng JSON)"""
    try:
        count = await learn_new_text(req.text, req.domain)
        return {"status": "success", "message": f"🤖 Đã nhét {count} đoạn kiến thức cho tên miền {req.domain}!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def learn_from_file(domain: str = "default", file: UploadFile = File(...), x_api_key: str = Header("None")):
    if x_api_key != config.API_KEY_SECRET:
        raise HTTPException(status_code=403, detail="Từ chối truy cập: API Key không đúng!")
        
    """AIP nhận trực tiếp các file tài liệu và học nội dung của nó"""
    allowed_exts = (".txt", ".pdf", ".docx", ".csv", ".xlsx", ".json")
    if not file.filename.lower().endswith(allowed_exts):
        raise HTTPException(status_code=400, detail=f"Chỉ hỗ trợ file {', '.join(allowed_exts)}")
    
    try:
        # Sử dụng parser để đọc đa định dạng
        text = await extract_text_from_file(file)
        
        # Đẩy vào AI để học
        count = await learn_new_text(text, domain)
        
        return {
            "status": "success", 
            "message": f"🤖 Học thành công {count} đoạn từ file '{file.filename}' cho tên miền {domain}!"
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Lỗi đọc file: {str(e)}")

@router.delete("/domain")
async def clear_domain_data(domain: str, x_api_key: str = Header("None")):
    """Xóa bỏ hoàn toàn trí nhớ của AI về một trang web cụ thể"""
    if x_api_key != config.API_KEY_SECRET:
        raise HTTPException(status_code=403, detail="Từ chối truy cập: API Key không đúng!")
        
    try:
        count = await delete_domain_knowledge(domain)
        if count == 0:
            return {"status": "success", "message": f"Tên miền '{domain}' hiện đang trống, không có dữ liệu để xóa."}
        return {"status": "success", "message": f"🗑 Đã xóa sạch {count} đoạn bộ nhớ của AI về tên miền '{domain}'!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xóa dữ liệu: {str(e)}")
