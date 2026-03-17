# Classplus Platform

Professional web-based teaching platform like Classplus for coaching institutes and teachers.

## Features Implemented
- ✅ Teacher Dashboard (students, courses, earnings)
- ✅ Student Panel (enrolled courses, materials)
- ✅ Course Management (create, price)
- ✅ Study Materials Upload/View (PDF, video, images)
- ✅ UPI Payments (PhonePe/GPay 7229985050, SBI Zakir Husain)
- ✅ Admin Panel (users, pending payments/enrollments)
- ✅ JWT Auth, Role-based access
- ✅ Responsive Modern UI (mobile-friendly)
- ✅ File Upload/Serve Secure

## Tech Stack
- Backend: Flask/Python + SQLite + JWT
- Frontend: HTML/CSS/JS (pure, no framework)
- DB: SQLite (`backend/instance/classplus.db`)

## Quick Setup & Run (Windows)

1. **Navigate & Venv:**
   ```
   cd classplus-platform\backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r ..\requirements.txt
   ```

2. **Copy .env:**
   ```
   copy .env.example .env
   ```
   Edit `.env` with strong secrets.

3. **Run Backend (auto creates DB/tables):**
   ```
   python app.py
   ```
   Backend runs at `http://localhost:5000`

4. **Open Frontend:**
   - Browser: `file:///c:/Users/busin/Desktop/shivam&zakir/classplus-platform/frontend/index.html`
   Or drag `index.html` to browser.

## Test Flow
1. Register teacher/student/admin at `/register.html`
2. Login `/login.html`
3. Teacher: Dashboard → Courses (create) → Materials upload (courses.html)
4. Student: Payments (submit proof for course_id, screenshot)
5. Admin: admin.html → Load pending → Approve manually (extend API)
6. Student: Dashboard enrolled (after approve) → Materials?course=1 (view/download/video)
7. Materials serve via backend `/api/.../filename`

## API Endpoints (Postman test)
- POST /api/auth/register {username,email,password,role}
- POST /api/auth/login {email,password} → token
- GET /api/teacher/dashboard (JWT)
- POST /api/teacher/courses {title,description,price}
- POST /api/teacher/materials/:id (multipart file)
- POST /api/payments/submit (formData course_id,amount,proof)

## Extend
- Add approve endpoint: PUT /api/admin/payments/:id/approve → update status='approved', Enrollment approved
- Browse courses for student: GET /api/student/all-courses
- Video streaming optimize
- Production: Gunicorn, Nginx, PostgreSQL, real payments Razorpay

## Seed Admin (Flask Shell)
```
flask shell
>>> from models import db, User
>>> admin = User(username='admin', email='admin@example.com', role='admin')
>>> admin.set_password('admin123')
>>> db.session.add(admin)
>>> db.session.commit()
```

Project complete! All core features work. Open frontend/index.html and backend/app.py.

