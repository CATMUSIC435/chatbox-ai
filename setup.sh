#!/bin/bash

# Dừng file ngay lập tức nếu có bất kỳ lệnh nào bị lỗi
set -e

echo "🚀 Bắt đầu cài đặt hệ thống ConectAI trên Ubuntu..."
echo "----------------------------------------------------"

# Cập nhật package list và cài Python3 vái môi trường ảo (venv)
echo "🔄 Cập nhật hệ thống Ubuntu và cài đặt thư viện cần thiết..."
sudo apt update
sudo apt install -y python3 python3-venv python3-pip curl

# Tạo môi trường ảo (giống như trên Windows)
echo "📦 Đang tạo môi trường ảo (Virtual Environment)..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Kích hoạt môi trường ảo
source venv/bin/activate

# Cài đặt các thư viện AI & Web Server
echo "📥 Đang tải và cài đặt Python dependencies (sẽ tốn khoảng vài phút)..."
pip install --upgrade pip
pip install -r requirements.txt

# Kiểm tra xem máy chủ Ubuntu đã có AI Ollama chưa
echo "🦙 Đang kiểm tra hệ thống Ollama AI..."
if ! command -v ollama &> /dev/null
then
    echo "⚠️ Ollama chưa có. Hệ thống sẽ tự động cài Ollama cho bạn..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "✅ Ollama đã được cài đặt."
fi

# Tự động tải model Qwen siêu nhẹ về trước để test (nếu bạn dùng model khác, hãy sửa ở đây)
echo "📥 Đang tải Model ngôn ngữ AI (qwen2.5:0.5b)..."
# Chạy ngầm server ollama trước khi kéo model
sudo systemctl enable ollama || true
sudo systemctl start ollama || true
sleep 5 # Đợi ollama khởi động
ollama pull qwen2.5:0.5b

echo "----------------------------------------------------"
echo "🎉 CÀI ĐẶT HOÀN TẤT THÀNH CÔNG 🎉"
echo "Để khởi động Server trên Ubuntu, bạn hãy chạy 2 lệnh sau:"
echo " 1. Kích hoạt môi trường ảo:"
echo "    source venv/bin/activate"
echo ""
echo " 2. Chạy ứng dụng web (mở cổng 8000 cho mọi IP truy cập):"
echo "    uvicorn main:app --host 0.0.0.0 --port 8000"
echo "----------------------------------------------------"
