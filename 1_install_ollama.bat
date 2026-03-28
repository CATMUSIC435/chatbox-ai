@echo off
chcp 65001 >nul
echo ====================================================
echo 🦙 Tự động tải và cài đặt Ollama AI Engine (Cho Windows)
echo ====================================================
echo.
echo ⏳ Đang tải file cài đặt Ollama... Vui lòng đợi trong giây lát.
powershell -Command "Invoke-WebRequest -Uri 'https://ollama.com/download/OllamaSetup.exe' -OutFile 'OllamaSetup.exe'"

if exist OllamaSetup.exe (
    echo ✅ Đã tải xong file OllamaSetup.exe!
    echo 🚀 Đang tự động mở trình cài đặt...
    echo 👉 (Vui lòng bấm nút INSTALL trên cửa sổ màu trắng hiện ra nhé)
    start /wait OllamaSetup.exe
    
    echo.
    echo 🧹 Đang dọn dẹp file rác...
    del OllamaSetup.exe
    
    echo.
    echo ====================================================
    echo ✅ ĐÃ CÀI ĐẶT OLLAMA THÀNH CÔNG!
    echo 👉 Bước tiếp theo: Bạn hãy chạy file "2_pull_model.bat" để tải bộ não AI nhé.
    echo ====================================================
) else (
    echo ❌ [Lỗi] Không thể tải được file. Vui lòng tự tải qua trình duyệt ở link: https://ollama.com/download
)
pause
