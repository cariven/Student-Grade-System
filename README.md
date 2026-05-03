# Student Grade System

Sistem manajemen nilai siswa berbasis web yang memungkinkan guru atau admin untuk mengelola data siswa dan melacak nilai mereka dengan mudah. Aplikasi ini dibangun dengan teknologi modern dan arsitektur full-stack.

## 🎯 Fitur Utama

- **Autentikasi Pengguna**: Sistem login aman menggunakan JWT dan bcrypt password hashing
- **Manajemen Data Siswa**: Tambah, hapus, dan lihat data siswa dengan mudah
- **Tracking Nilai**: Catat nilai dari berbagai komponen (Tugas, UTS, UAS)
- **Kalkulasi Otomatis**: Nilai akhir dihitung secara otomatis dari komponen nilai
- **Grading System**: Konversi nilai menjadi huruf grade (A, B, C, D, E)
- **Kontrol Akses**: Setiap pengguna hanya bisa melihat data siswa mereka sendiri
- **API REST**: Endpoint API yang lengkap untuk integrasi

## 🛠️ Teknologi yang Digunakan

### Backend
- **Python 3.x** - Bahasa pemrograman
- **Flask 3.0.0** - Web framework
- **Flask-JWT-Extended** - Autentikasi JWT
- **bcrypt** - Password hashing
- **Flask-CORS** - Cross-Origin Resource Sharing
- **SQLite** - Database

### Frontend
- **React 18.0** - UI library
- **Vite 5.0** - Build tool
- **React Router 7.14** - Navigation
- **Node.js** - Runtime environment

### Testing
- **pytest** - Unit testing untuk backend
- **pytest-cov** - Code coverage
- **vitest** - Testing untuk frontend
- **hypothesis** - Property-based testing

## 📋 Prasyarat Instalasi

Sebelum memulai, pastikan Anda memiliki:

- **Python 3.8+** (untuk backend)
- **Node.js 16+** dan **npm** (untuk frontend)
- **Git** (untuk cloning repository)
- **pip** (Python package manager, biasanya sudah tersedia dengan Python)

## 📁 Struktur Project

```
Student-Grade-System/
├── src/
│   ├── backend/
│   │   └── app/
│   │       ├── __init__.py           # Flask app initialization
│   │       ├── models.py             # Database models & queries
│   │       ├── routes.py             # Main API endpoints
│   │       ├── auth_routes.py        # Authentication endpoints
│   │       ├── auth_service.py       # Auth business logic
│   │       ├── services.py           # Helper services
│   │       └── validators.py         # Input validation
│   └── frontend/
│       ├── src/                      # React components
│       ├── public/                   # Static assets
│       └── package.json              # Frontend dependencies
├── tests/                            # Test files
├── requirements.txt                  # Python dependencies
├── package.json                      # Root dependencies
├── pytest.ini                        # Pytest configuration
├── .coveragerc                       # Coverage configuration
├── run.py                            # Entry point untuk backend
└── README.md                         # Documentation
```

## 🚀 Instalasi dan Setup

### 1. Clone Repository

```bash
git clone https://github.com/cariven/Student-Grade-System.git
cd Student-Grade-System
```

### 2. Setup Backend

#### Buat Virtual Environment

```bash
# Di Windows
python -m venv venv
venv\Scripts\activate

# Di macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Setup Environment Variables

Buat file `.env` di root directory (atau set langsung):

```bash
# Windows
set JWT_SECRET_KEY=kunci-rahasia-yang-panjang-dan-aman-minimal-32-karakter
set DATABASE=database.db

# macOS/Linux
export JWT_SECRET_KEY=kunci-rahasia-yang-panjang-dan-aman-minimal-32-karakter
export DATABASE=database.db
```

### 3. Setup Frontend

```bash
cd src/frontend
npm install
```

## 💻 Cara Menggunakan

### Menjalankan Backend

```bash
# Dari root directory (virtual environment sudah aktif)
python run.py
```

Backend akan berjalan di `http://localhost:5000`

### Menjalankan Frontend

```bash
# Dari directory src/frontend
npm run dev
```

Frontend akan berjalan di `http://localhost:5173`

### Menjalankan Tests

#### Backend Tests

```bash
# Dari root directory
pytest
```

Dengan coverage report:

```bash
pytest --cov=src --cov-report=html
```

#### Frontend Tests

```bash
# Dari src/frontend directory
npm test
```

## 📖 Contoh Penggunaan

### 1. Registrasi Pengguna

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "guru@example.com",
    "password": "password123"
  }'
```

Response:
```json
{
  "message": "User registered successfully",
  "user_id": 1
}
```

### 2. Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "guru@example.com",
    "password": "password123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": 1
}
```

### 3. Tambah Siswa

```bash
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {access_token}" \
  -d '{
    "name": "Budi Santoso"
  }'
```

Response:
```json
{
  "id": 1,
  "name": "Budi Santoso",
  "user_id": 1,
  "created_at": "2026-05-03T10:00:00"
}
```

### 4. Input Nilai Siswa

```bash
curl -X POST http://localhost:5000/api/grades \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {access_token}" \
  -d '{
    "student_id": 1,
    "tugas": 85,
    "uts": 80,
    "uas": 78
  }'
```

Response:
```json
{
  "id": 1,
  "student_id": 1,
  "tugas": 85,
  "uts": 80,
  "uas": 78,
  "final": 81.0,
  "grade": "A",
  "created_at": "2026-05-03T10:00:00"
}
```

### 5. Lihat Daftar Siswa

```bash
curl -X GET http://localhost:5000/api/students \
  -H "Authorization: Bearer {access_token}"
```

### 6. Lihat Nilai Siswa

```bash
curl -X GET http://localhost:5000/api/students/1/grades \
  -H "Authorization: Bearer {access_token}"
```

## 🤝 Kontribusi

Kami menerima kontribusi dari siapa saja! Berikut cara berkontribusi:

### Langkah-Langkah Kontribusi

1. **Fork Repository**
   ```bash
   Klik tombol "Fork" di halaman repository
   ```

2. **Clone Repository Forked Anda**
   ```bash
   git clone https://github.com/username-anda/Student-Grade-System.git
   cd Student-Grade-System
   ```

3. **Buat Branch Baru**
   ```bash
   git checkout -b feature/nama-fitur-anda
   ```

4. **Buat Perubahan**
   - Pastikan kode Anda mengikuti style guide yang ada
   - Tambahkan test untuk fitur baru
   - Update dokumentasi jika diperlukan

5. **Commit Perubahan**
   ```bash
   git add .
   git commit -m "Deskripsi perubahan yang jelas dan ringkas"
   ```

6. **Push ke Branch**
   ```bash
   git push origin feature/nama-fitur-anda
   ```

7. **Buat Pull Request**
   - Buka repository di GitHub
   - Klik "New Pull Request"
   - Pilih branch Anda dan tulis deskripsi yang detail

### Guidelines Pengembangan

- **Naming Convention**: Gunakan snake_case untuk Python, camelCase untuk JavaScript
- **Code Style**: Ikuti PEP 8 untuk Python
- **Testing**: Pastikan semua test lolos sebelum submit PR
- **Dokumentasi**: Update README dan docstrings jika menambah fitur baru
- **Commit Message**: Gunakan pesan yang deskriptif dan jelas

## 📄 Lisensi

Proyek ini dilisensikan di bawah **MIT License** - lihat file [LICENSE](LICENSE) untuk detail lengkapnya.

### MIT License Summary

Anda bebas untuk:
- ✅ Menggunakan, mempelajari, dan mengubah kode
- ✅ Mendistribusikan dan menggunakan kode secara komersial
- ✅ Menggunakan secara pribadi

Dengan syarat:
- ℹ️ Sertakan pemberitahuan lisensi dan copyright
- ℹ️ Lampirkan file LICENSE dengan distribusi

Tanpa tanggung jawab atau garansi apapun.

---

**Dibuat oleh**: [cariven](https://github.com/cariven)

**Dibuat pada**: 2026-05-03

Jika ada pertanyaan atau butuh bantuan, silakan buka [Issue](https://github.com/cariven/Student-Grade-System/issues) baru!
