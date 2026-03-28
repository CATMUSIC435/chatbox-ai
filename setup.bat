@echo off
chcp 65001 >nul
echo.
echo ====================================================
echo 🚀 Bắt đầu cài đặt hệ thống ConectAI trên Windows...
echo ====================================================

echo.
echo 1️⃣  Kiểm tra Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ [LỖI] Không tìm thấy Python. Vui lòng cài đặt Python (phiên bản > 3.10) và tích chọn ô "Add Python to PATH" lúc cài đặt nha!
    pause
    exit /b
)
echo ✅ Đã tìm thấy Python!

echo.
echo 2️⃣  Tạo môi trường ảo (Virtual Environment)...
if not exist "venv\" (
    python -m venv venv
    echo ✅ Tạo venv thành công!
) else (
    echo ℹ️  Thư mục venv đã tồn tại, tự động bỏ qua bước này.
)

echo.
echo 3️⃣  Tải và cài đặt các thư viện AI (Python Dependencies)...
call .\venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo 4️⃣  Kiểm tra Hệ thống AI Ollama...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ [CẢNH BÁO] Hệ thống phát hiện bạn chưa cài đặt phần mềm Ollama.
    echo 👉 Bạn vui lòng tải bản cài đặt '.exe' tại link sau: https://ollama.com/download 
    echo (Nhớ cài xong rồi hãy chạy máy chủ nhé!)
) else (
    echo ✅ Ollama đã sẵn sàng.
    echo 📥 Đang tự động kéo model nội bộ (qwen2.5:0.5b) về máy... (Cần có Mạng Internet)
    start /b ollama serve >nul 2>&1
    timeout /t 3 >nul
    ollama pull qwen2.5:0.5b
)

echo.
echo ====================================================
echo 🎉 CÀI ĐẶT HOÀN TẤT THÀNH CÔNG THƯA SẾP! 🎉
echo ====================================================
echo 👉 Bây giờ, để chạy ứng dụng bạn hãy làm 2 bước sau:
echo  1. Kích hoạt venv bằng lệnh:  .\venv\Scripts\activate
echo  2. Khởi động Web Server:      uvicorn main:app --reload --host 0.0.0.0 --port 8000
echo.
pause
