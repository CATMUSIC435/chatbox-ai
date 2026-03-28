# ConectAI - Hộ Tệp Khách Hàng Đa Tên Miền (Multi-Tenant RAG)

ConectAI là một hệ thống Chatbot AI thông minh tiên tiến được thiết kế để hỗ trợ nhiều website (tên miền) cùng một lúc từ duy nhất một server chung. Hệ thống có khả năng học hỏi tự động từ các file tài liệu được tải lên (`.pdf`, `.docx`, `.xlsx`, `.csv`, `.json`, `.txt`) và phân chia kiến thức hoàn toàn cách ly theo từng tên miền để đảm bảo an toàn.

Kết hợp cùng với một Widget nhaúng siêu mượt mà, cực kỳ đẹp mắt, có hoạt ảnh 3D và hỗ trợ chia sẻ (CORS) toàn diện, ConectAI vô cùng thích hợp cho những Agency triển khai hệ thống AI giá rẻ/chính xác cho từng khách hàng.

## 🌟 Tính Năng Nội Bật
1. **Kiến Trúc Multi-Tenant (Đa người dùng)**: Mọi dữ liệu Text đều được gắn thẻ `domain`. Khách hàng bên tư vấn Bất động sản sẽ không bao giờ sợ bị rò rỉ dữ liệu từ khách hàng Spa thẩm mỹ.
2. **Đọc Dữ Liệu Đa Định Dạng**: Khối `parsers.py` hỗ trợ rút trích chữ thô từ tất cả các tệp phổ biến (Excel, PDF, Word) mà người dùng có thể sử dụng UI để tự động đưa vào trí nhớ.
3. **Javascript Widget Nhiều Màn Hình**: Một đoạn Script nhỏ duy nhất (`/static/widget.js`) đã kèm theo hiệu ứng Glassmorphism, nút chat nổi bằng ảnh động (GIF/Vector) chuyên nghiệp. Bot cũng có thể xuất "Gợi Ý" (`---SUGGESTIONS---`) ngay ra bên ngoài dưới dạng nút bấm tương tác.
4. **Bảo Tuổi CORS Giao Diện**: Người Quản trị (Admin) có thể gán/xóa các đường dẫn `/api/domains` mà không cần khởi động lại Database.
5. **Vận Hành Toàn Phần Offline**: Tất cả LLM và Text-Embedding đều có thể được tự host ngay tại nhà với Ollama + Langchain để miễn phí 100% token chi phí.

## 🚀 Cài Đặt Và Sử Dụng

### 1. Yêu cầu hệ thống thiết yếu:
*   Python 3.10 trở lên.
*   Ollama (Đã kéo sẵn model như `llama3.2` hoặc `qwen2.5:0.5b`).

### 2. Tự Động Cài (Trên phía Linux/Ubuntu)
Nếu bạn chạy dự án trên VPS Ubuntu, hãy cấp quyền rồi khởi chạy file Bash cũng đã lắp sẵn một vòng cài đặt:
```bash
chmod +x setup.sh
./setup.sh
```

### 3. Cài Đặt Bằng Tay hoặc Tự Động (Cho Windows)
Dự án đã được trang bị sẵn file chạy tự động trên nền tảng Windows. Bạn chỉ cần click đúp vào file hoặc chạy lệnh:
```bat
.\setup.bat
```
Script sẽ tự sinh môi trường ảo (venv), cài tất cả thư viện và kiểm tra cài đặt Ollama tự động.

Nếu muốn cài bằng tay:
```bash
python -m venv venv
.\venv\Scripts\activate

pip install -r requirements.txt
```

### 4. Thiết Lập Và Khởi Chạy Server
Nếu bạn muốn tùy chỉnh bảo mật, model hay tên miền gốc, bạn hãy mở file `core/config.py` ra.  
Sau đó, khởi động FastAPI:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Bạn hãy mở trình duyệt ở cổng `http://127.0.0.1:8000` (Giao diện Admin) hoặc nhúng đoạn mã sau để sử dụng Chatbot lên bất cứ website nào!

### 5. Cách Nhúng Widget (HTML)
Chép thẻ `script` vào chân trang (footer) của web bạn cần lắp đặt, và thay tham số `data-domain` bằng tên miền bạn đã ném file dữ liệu từ trang Admin.
```html
<!-- Bắt buộc nạp Widget từ Server bạn, ví dụ localhost -->
<script src="http://127.0.0.1:8000/static/widget.js" data-domain="tên-miền-website-của-bạn.com"></script>
```

> **Lưu ý Cực Kỳ Quan Trọng:** 
> Nếu Bot của bạn bảo: "Tôi không có thông tin" trên web Bất động sản, nhưng nó trả lời được bên màn hình Admin, CHẮC CHẮN tham số ngầm `data-domain` và thẻ `domain` truyền về Stream đã sai lệch. Bạn không cần làm gì, nhưng hãy thật tỉnh táo đối chiếu điều đó!

---

*Chúc các bạn thành công với ConectAI – Làm chủ AI Hub Của Riêng Bạn!*
