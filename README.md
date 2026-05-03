# Student Grade System

[![CI Pipeline](https://github.com/cariven/Student-Grade-System/actions/workflows/ci.yml/badge.svg)](https://github.com/cariven/Student-Grade-System/actions)
[![Coverage](https://codecov.io/gh/cariven/Student-Grade-System/branch/main/graph/badge.svg)](https://codecov.io/gh/cariven/Student-Grade-System)
![Python](https://img.shields.io/badge/python-3.11-blue)
![React](https://img.shields.io/badge/react-18-61dafb)
![License](https://img.shields.io/badge/license-MIT-green)

Aplikasi web full-stack untuk mengelola nilai siswa (CRUD) — monorepo dengan backend Flask dan frontend React.

## Deskripsi Sistem

Student Grade System memungkinkan guru/admin mendaftarkan siswa, memasukkan nilai (tugas, UTS, UAS), dan otomatis menghitung nilai akhir serta grade. Setiap pengguna (guru) hanya bisa melihat dan mengelola siswa & nilai miliknya sendiri.

Akses dilindungi autentikasi JWT — setiap request ke endpoint siswa dan nilai memerlukan token yang valid.

## Arsitektur Aplikasi

```
student-grade-system/
├── src/
│   ├── backend/app/          # Flask REST API
│   │   ├── __init__.py       # Inisialisasi Flask, CORS, error handler global
│   │   ├── models.py         # StudentRepository — query SQLite (users, students, grades)
│   │   ├── routes.py         # StudentController — endpoint siswa, nilai + JWT middleware
│   │   ├── services.py       # StudentService — logika bisnis, kalkulasi grade
│   │   ├── validators.py     # Validasi input (name, grades, email, password)
│   │   ├── auth_routes.py    # Endpoint /auth/register dan /auth/login
│   │   └── auth_service.py   # Logika autentikasi, JWT HS256, bcrypt
│   └── frontend/             # React + Vite
│       ├── api/apiClient.js  # Semua HTTP request ke backend
│       ├── components/       # StudentList, StudentCard, GradeForm, GradeBadge
│       │                     # LoginForm, RegisterForm
│       ├── App.jsx           # Root component, auth state, view toggle
│       └── main.jsx
├── tests/
│   ├── backend/
│   │   ├── conftest.py       # Fixtures: test client, SQLite in-memory
│   │   ├── unit/             # Unit test: validators, auth_service, services, models
│   │   └── integration/      # Integration test: auth routes, student/grade routes
│   └── frontend/             # Vitest: semua komponen + ApiClient
├── .github/workflows/ci.yml  # GitHub Actions CI/CD
├── requirements.txt
├── package.json
└── pytest.ini
```

## Alur Request Backend

```
Browser / ApiClient (HTTP)
         │
         ▼
StudentController (routes.py)    ← Routing, parsing, format JSON
         │
         ▼
StudentService   (services.py)   ← Aturan bisnis, orkestrasi, kalkulasi grade
         │         ↘
         │     Validator (validators.py)
         ▼
StudentRepository (models.py)    ← Query SQL ke SQLite
         │
         ▼
    SQLite DB (database.db)
```

## Stack Teknologi

| Bagian | Teknologi |
|--------|-----------|
| Backend | Python 3.11, Flask, SQLite |
| Frontend | React 18, Vite |
| Autentikasi | JWT HS256 (PyJWT), bcrypt |
| Backend Tests | pytest, pytest-cov, pytest-mock, Hypothesis |
| Frontend Tests | Vitest, fast-check, Testing Library |
| CI/CD | GitHub Actions |

## Menjalankan Aplikasi

### Prasyarat

- Python 3.11+
- Node.js 16+

### Environment Variables

Buat file `.env` di root dan `src/frontend/.env`:

| Variabel | Deskripsi | Contoh |
|----------|-----------|--------|
| `JWT_SECRET_KEY` | Secret key untuk JWT — wajib diganti di production | `your-secret-key-min-32-chars` |
| `VITE_API_BASE_URL` | Base URL backend API | `http://localhost:5000` |

> Jangan pernah commit nilai `JWT_SECRET_KEY` yang sebenarnya ke repository.

### Backend

```bash
pip install -r requirements.txt
PYTHONPATH=src/backend python run.py
```

Backend berjalan di `http://localhost:5000`.

### Frontend

```bash
npm install
npm run dev
```

Frontend berjalan di `http://localhost:5173`.

## Menjalankan Tests

### Backend

```bash
# Semua test backend dengan coverage
PYTHONPATH=src/backend pytest --cov=app --cov-report=term-missing
```

### Frontend

```bash
# Single run (tanpa watch mode)
npm run test
```

## Strategi Pengujian

### Unit Tests (Backend)

Menguji logika bisnis secara terisolasi — tanpa database atau HTTP call. Menggunakan pytest-mock.

- **Target:** StudentService, AuthService, Validator, StudentRepository
- **Cakupan:** perilaku normal, edge case, dan error handling

### Integration Tests (Backend)

Menguji seluruh alur HTTP → Service → Database menggunakan SQLite in-memory.

- **Target:** semua endpoint REST API (`/students`, `/grades`, `/auth/register`, `/auth/login`)
- **Cakupan:** semua operasi CRUD, autentikasi, ownership check, dan respons error

### Property-Based Tests

Menggunakan Hypothesis (backend) dan fast-check (frontend) untuk memverifikasi properti kebenaran sistem dengan ratusan input yang di-generate otomatis.

Contoh properti yang diuji:

- Nama siswa valid selalu menghasilkan siswa dengan created_at valid
- String whitespace-only atau kosong selalu ditolak validator
- Grade yang dihitung selalu sesuai rumus: (tugas×20% + uts×30% + uas×50%)
- Siswa yang dihapus tidak bisa diakses lagi (HTTP 404)
- N siswa di database → GET /students selalu mengembalikan tepat N elemen
- Grade letter selalu sesuai range nilai (A: 80-100, B: 70-79, C: 60-69, D: 50-59, E: <50)

### Frontend Tests

Menggunakan Vitest + Testing Library dengan mock ApiClient.

- **Cakupan:** semua komponen React (StudentList, StudentCard, GradeForm, GradeBadge, LoginForm, RegisterForm, App)
- **Property test dengan fast-check untuk validasi perilaku komponen**

## Test Coverage

Target coverage: **100%** pada seluruh kode backend (`src/backend/app/`).

```bash
PYTHONPATH=src/backend pytest --cov=app --cov-report=term-missing --cov-report=html
```

Konfigurasi di `pytest.ini`:

```ini
[pytest]
testpaths = tests/backend
addopts = --cov=app --cov-report=term-missing
```

## CI Pipeline

Pipeline otomatis berjalan di GitHub Actions pada setiap push dan pull request.

```
Push / Pull Request
        │
        ├── test-backend ──── Install deps → Validate import → pytest + coverage
        │
        └── test-frontend ─── Install deps → Build → Vitest
                │
                └── (kedua job lulus)
                        │
                        └── release (tag release*) ── Buat GitHub Release + tarball
```

| Job | Trigger | Aksi |
|-----|---------|------|
| `test-backend` | Semua push & PR | Install Python deps, validasi import, jalankan pytest + coverage |
| `test-frontend` | Semua push & PR | Install Node deps, build frontend, jalankan Vitest |
| `release` | Tag `release*` (setelah test lulus) | Buat GitHub Release dengan tarball |

## Dokumentasi API

**Base URL:** `http://localhost:5000`

Semua respons menggunakan `Content-Type: application/json`.

Endpoint siswa dan nilai memerlukan header `Authorization: Bearer <token>`.

### Model Student

```json
{
  "id": 1,
  "name": "Budi Santoso",
  "user_id": 1,
  "created_at": "2026-05-03T10:00:00"
}
```

### Model Grade

```json
{
  "id": 1,
  "student_id": 1,
  "user_id": 1,
  "tugas": 85,
  "uts": 80,
  "uas": 78,
  "final": 81.0,
  "grade": "A",
  "created_at": "2026-05-03T10:00:00"
}
```

Nilai `grade` yang valid: A, B, C, D, E (berdasarkan range nilai final).

### Auth Endpoints

| Method | Path | Deskripsi | Status Sukses |
|--------|------|-----------|---------------|
| `POST` | `/auth/register` | Daftar akun baru | 201 |
| `POST` | `/auth/login` | Login, dapatkan JWT | 200 |

### Student Endpoints (Protected)

| Method | Path | Deskripsi | Status Sukses |
|--------|------|-----------|---------------|
| `POST` | `/students` | Buat siswa baru | 201 |
| `GET` | `/students` | Ambil semua siswa milik guru | 200 |
| `GET` | `/students/{id}` | Ambil siswa by ID | 200 |
| `DELETE` | `/students/{id}` | Hapus siswa | 200 |

### Grade Endpoints (Protected)

| Method | Path | Deskripsi | Status Sukses |
|--------|------|-----------|---------------|
| `POST` | `/grades` | Buat/input grade siswa | 201 |
| `GET` | `/students/{id}/grades` | Ambil semua grade siswa | 200 |
| `DELETE` | `/grades/{id}` | Hapus grade | 200 |

## Penanganan Error

| Exception | HTTP Status | Keterangan |
|-----------|-------------|-----------|
| `ValueError` | 400 | Input tidak valid |
| `StudentNotFoundError` | 404 | Siswa tidak ditemukan |
| `PermissionError` | 403 | Siswa/grade milik guru lain |
| JWT tidak valid / kedaluwarsa | 401 | Autentikasi gagal |

