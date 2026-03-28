from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from models.schemas import ChatRequest
from services.rag import get_context_async, build_prompt, stream_ollama_response, send_ollama_query

router = APIRouter(prefix="/chat", tags=["Chat & Inference"])

@router.post("")
async def chat(req: ChatRequest):
    context = await get_context_async(req.question, req.domain)
    prompt = build_prompt(context, req.question)
    answer = await send_ollama_query(prompt)
    return {"answer": answer}

@router.post("-stream")
async def chat_stream(req: ChatRequest):
    context = await get_context_async(req.question, req.domain)
    prompt = build_prompt(context, req.question)
    return StreamingResponse(stream_ollama_response(prompt), media_type="text/plain")
