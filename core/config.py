import os

# Cấu hình đường dẫn
DB_PATH = "./db"
DATA_PATH = "data.txt"

# Cấu hình Ollama
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
MODEL = os.getenv("MODEL", "llama3.2")  # Bạn có thể đổi lại thành qwen2.5:0.5b

# Cấu hình Tên miền và Bảo mật
DEFAULT_DOMAIN = os.getenv("DEFAULT_DOMAIN", "http://127.0.0.1")
API_KEY_SECRET = os.getenv("API_KEY_SECRET", "conectai-secret-2026")
