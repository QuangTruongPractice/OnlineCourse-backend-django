# Courses Online - Backend API (Django)

Hệ thống API backend cho dự án Online Course, được xây dựng trên nền tảng Django REST Framework, cung cấp khả năng quản lý khóa học, người dùng và tích hợp thanh toán.

## 🛠️ Công nghệ sử dụng

- **Framework:** Django 4.2 & Django REST Framework (DRF)
- **Cơ sở dữ liệu:** PostgreSQL
- **Xác thực:** OAuth2 (django-oauth-toolkit)
- **Lưu trữ media:** Cloudinary (lưu trực tiếp ảnh, video bài học)
- **Caching:** Redis & Django Redis
- **Tài liệu API:** Swagger/Redoc (drf-yasg)
- **Triển khai:** Render (Free Tier)

## 🔗 Demo & Tài liệu
- **API Base URL:** [https://onlinecourse-backend-django.onrender.com/](https://onlinecourse-backend-django.onrender.com/)
- **Swagger UI:** `[API_URL]/swagger/`
- **Admin Interface:** `[API_URL]/admin/`

## ⚙️ Hướng dẫn cài đặt (Local)

1.  **Clone source code:**
    ```bash
    git clone [repository-url]
    cd OnlineCourse-backend-django
    ```

2.  **Khởi tạo môi trường ảo:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    source venv/bin/activate  # Linux/macOS
    ```

3.  **Cài đặt các gói phụ thuộc:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Cấu hình biến môi trường (`.env`):**
    Tạo file `.env` và cấu hình các thông số sau:
    ```env
    DEBUG=True
    SECRET_KEY=your_secret_key
    DB_NAME=postgres
    DB_USER=postgres
    DB_PASSWORD=your_password
    DB_HOST=localhost
    DB_PORT=5432
    ```

5.  **Chạy Migrations & Khởi động server:**
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

## 🧪 Chạy Tests
Để đảm bảo chất lượng mã nguồn, chạy lệnh sau:
```bash
python manage.py test
```

## 📝 Ghi chú quan trọng
- Bản deploy trên **Render** có cơ chế tự ngủ đông. Nếu truy cập lần đầu thấy lâu, hãy đợi 5-10 phút để server khởi động lại.
- Dữ liệu media (ảnh đại diện, video bài học) được đồng bộ trực tiếp lên Cloudinary.

