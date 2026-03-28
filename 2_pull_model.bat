@echo off
chcp 65001 >nul
echo ====================================================
echo 🧠 Đang tải Model Trí Tuệ Nhân Tạo (qwen2.5:0.5b)
echo ====================================================
echo.

echo 🔄 Đang đánh thức Ollama Server...
start /b ollama serve >nul 2>&1
timeout /t 3 >nul

echo 📥 Đang tải Model về máy (Quá trình này nhanh hay chậm phụ thuộc vào tốc độ mạng của bạn)...
ollama pull qwen2.5:0.5b

echo.
echo ====================================================
echo ✅ HOÀN TẤT TẢI MODEL AI!
echo Mọi hệ thống trí tuệ nhân tạo gốc đã sẵn sàng.
echo Bạn có thể quay lại chạy Server "uvicorn" được rồi!
echo ====================================================
pause
