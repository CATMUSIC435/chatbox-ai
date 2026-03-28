import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from routers import chat, learn
from core import config

app = FastAPI(title="ConectAI Server", description="Hệ thống RAG Đa Người Dùng & Học Liên Tục")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

DOMAINS_FILE = "allowed_domains.txt"

def load_domains():
    if not os.path.exists(DOMAINS_FILE):
        with open(DOMAINS_FILE, "w", encoding="utf-8") as f:
            f.write("http://localhost\nhttp://127.0.0.1\n")
    with open(DOMAINS_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def save_domains(domains):
    with open(DOMAINS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(domains))

@app.middleware("http")
async def dynamic_cors_validator(request: Request, call_next):
    if request.url.path.startswith("/chat-stream") or request.url.path.startswith("/learn"):
        origin = request.headers.get("origin")
        if origin:
            allowed = load_domains()
            if origin not in allowed and "*" not in allowed:
                return JSONResponse(status_code=403, content={"detail": f"CORS Blocked: Domain '{origin}' not in whitelist"})
    return await call_next(request)

class DomainReq(BaseModel):
    domain: str

@app.get("/api/domains")
def get_domains():
    return {"domains": load_domains()}

@app.post("/api/domains")
def add_domain(req: DomainReq):
    domains = load_domains()
    if req.domain not in domains:
        domains.append(req.domain)
        save_domains(domains)
    return {"domains": domains}

@app.delete("/api/domains")
def remove_domain(domain: str):
    domains = load_domains()
    if domain in domains:
        domains.remove(domain)
        save_domains(domains)
    return {"domains": domains}
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(chat.router)
app.include_router(learn.router)

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Phục vụ file giao diện người dùng chính"""
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Không tìm thấy file index.html trong thư mục!</h1>")
