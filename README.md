<div align="center">

# 🪖 ER MEYDANI

### Askerlik anılarının paylaşıldığı modern sosyal platform.

<p>
Kullanıcıların askerlik anılarını paylaşabildiği, yorum yapabildiği ve kendi profillerini oluşturabildiği
mobil odaklı sosyal medya uygulaması.
</p>

<br>

<img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white">
<img src="https://img.shields.io/badge/Kotlin-Android-7F52FF?style=for-the-badge&logo=kotlin&logoColor=white">
<img src="https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white">
<img src="https://img.shields.io/badge/Supabase-Cloud_DB-3FCF8E?style=for-the-badge&logo=supabase&logoColor=white">
<img src="https://img.shields.io/badge/JWT-Authentication-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white">

<br><br>

<img src="https://img.shields.io/badge/Status-Development-orange?style=flat-square">
<img src="https://img.shields.io/badge/API-REST-blue?style=flat-square">
<img src="https://img.shields.io/badge/Python-3.x-yellow?style=flat-square&logo=python">

</div>

---

## 📖 Proje Hakkında

**Er Meydanı**, askerlik yapmış veya askerlik deneyimlerini paylaşmak isteyen kullanıcıların anılarını yayınlayabileceği sosyal bir platformdur.

Projenin backend tarafı **FastAPI**, mobil uygulama tarafı ise **Kotlin + Jetpack Compose** kullanılarak geliştirilmektedir.

Backend sistemi kullanıcı yönetimi, JWT tabanlı authentication, e-posta doğrulaması, anı paylaşımı ve yorum sistemi gibi temel sosyal medya özelliklerini sağlamaktadır.

---

## ✨ Özellikler

<table>
<tr>
<td width="50%">

### 👤 Kullanıcı Sistemi

* Kullanıcı kaydı
* Kullanıcı girişi
* JWT authentication
* Profil bilgileri
* Profil fotoğrafı desteği
* Kullanıcı doğrulama sistemi
* E-posta verification kodu

</td>

<td width="50%">

### 📝 Anı Sistemi

* Anı oluşturma
* Anıları listeleme
* Kullanıcıya ait anıları görüntüleme
* Anı güncelleme
* Anı silme
* Yetkilendirme kontrolü

</td>
</tr>

<tr>
<td>

### 💬 Yorum Sistemi

* Anılara yorum yapma
* Yorum güncelleme
* Yorum silme
* Kullanıcı bazlı yetkilendirme

</td>

<td>

### 🔐 Güvenlik

* OAuth2
* JWT Access Token
* Password Hashing
* Protected API Routes
* Owner-based authorization
* Environment variables

</td>
</tr>
</table>

---

<div align="center">

## 🛠️ Tech Stack

</div>

### Backend

<p>
<img src="https://skillicons.dev/icons?i=python,fastapi,postgresql" />
</p>

* **Python**
* **FastAPI**
* **SQLAlchemy**
* **Pydantic**
* **PostgreSQL**
* **Supabase**

### Authentication & Security

* **OAuth2PasswordBearer**
* **JWT**
* **bcrypt**
* **Passlib**
* **python-jose**

### Mobile

<p>
<img src="https://skillicons.dev/icons?i=kotlin,androidstudio" />
</p>

* **Kotlin**
* **Android Studio**
* **Jetpack Compose**
* **Retrofit**
* **Coroutines**

### Infrastructure

<p>
<img src="https://skillicons.dev/icons?i=git,github" />
</p>

* **Git**
* **GitHub**
* **Cloudflare Tunnel**
* **Supabase PostgreSQL**

---

## 🧠 Sistem Mimarisi

```text
┌──────────────────────┐
│   Android Client     │
│ Kotlin + Compose     │
└──────────┬───────────┘
           │
           │ HTTPS / REST
           ▼
┌──────────────────────┐
│    FastAPI Backend   │
│                      │
│  Authentication      │
│  Users               │
│  Memories            │
│  Comments            │
└──────────┬───────────┘
           │
           │ SQLAlchemy
           ▼
┌──────────────────────┐
│     PostgreSQL       │
│      Supabase        │
└──────────────────────┘
```

---

## 📂 Proje Yapısı

```text
er_meydani/
│
├── backend/
│   │
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── memories.py
│   │   └── comments.py
│   │
│   ├── utils/
│   │   ├── authentication.py
│   │   └── email.py
│   │
│   ├── .env
│   └── requirements.txt
│
├── android/
│   └── ErMeydani/
│
├── .gitignore
└── README.md
```

> Proje yapısı geliştirme sürecine göre değişebilir.

---

<div align="center">

## 🔌 API

</div>

FastAPI sayesinde backend'in interaktif API dokümantasyonu otomatik olarak oluşturulur.

Backend çalışırken:

```text
http://127.0.0.1:8000/docs
```

adresinden Swagger UI'a ulaşılabilir.

---

## 🔐 Authentication

Er Meydanı API'si **JWT Access Token** kullanmaktadır.

Authentication akışı:

```text
Register
   ↓
E-mail Verification
   ↓
Login
   ↓
JWT Access Token
   ↓
Protected API Endpoints
```

Login sonrasında elde edilen token:

```http
Authorization: Bearer <access_token>
```

formatında protected endpoint'lere gönderilir.

---

## 📡 API Endpoints

### Authentication

| Method | Endpoint         | Açıklama                         |
| ------ | ---------------- | -------------------------------- |
| `POST` | `/auth/register` | Yeni kullanıcı oluşturur         |
| `POST` | `/auth/verify`   | E-posta doğrulaması yapar        |
| `POST` | `/auth/login`    | Kullanıcı girişi                 |
| `GET`  | `/auth/me`       | Giriş yapan kullanıcıyı döndürür |

---

### Memories

| Method   | Endpoint                | Açıklama                       |
| -------- | ----------------------- | ------------------------------ |
| `GET`    | `/memories`             | Tüm anıları listeler           |
| `POST`   | `/memories/create`      | Yeni anı oluşturur             |
| `GET`    | `/memories/{user_id}`   | Kullanıcının anılarını getirir |
| `PATCH`  | `/memories/{memory_id}` | Anıyı günceller                |
| `DELETE` | `/memories/{memory_id}` | Anıyı siler                    |

---

### Comments

| Method   | Endpoint                 | Açıklama          |
| -------- | ------------------------ | ----------------- |
| `POST`   | `/comments/{memory_id}`  | Anıya yorum yapar |
| `PATCH`  | `/comments/{comment_id}` | Yorumu günceller  |
| `DELETE` | `/comments/{comment_id}` | Yorumu siler      |

---

### Users

| Method   | Endpoint                  | Açıklama                      |
| -------- | ------------------------- | ----------------------------- |
| `GET`    | `/users`                  | Kullanıcıları listeler        |
| `GET`    | `/users/{user_id}`        | Kullanıcı bilgilerini getirir |
| `PATCH`  | `/users/update/{user_id}` | Kullanıcıyı günceller         |
| `DELETE` | `/users/delete/{user_id}` | Kullanıcıyı siler             |

---

## 🚀 Kurulum

Repository'yi klonla:

```bash
git clone https://github.com/YOUR_USERNAME/er_meydani.git
```

Proje dizinine gir:

```bash
cd er_meydani/backend
```

Virtual environment oluştur:

```bash
python -m venv .venv
```

Linux / macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

Dependency'leri yükle:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Backend klasöründe bir `.env` dosyası oluştur:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key

EMAIL_ADDRESS=your_email
EMAIL_PASSWORD=your_app_password
```

> ⚠️ `.env` dosyası kesinlikle GitHub repository'sine gönderilmemelidir.

`.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

---

## ▶️ Backend'i Çalıştırma

```bash
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## 📱 Android Client

Mobil uygulama:

```text
Kotlin
   ↓
Jetpack Compose
   ↓
Retrofit
   ↓
FastAPI REST API
```

Retrofit ile backend endpoint'lerine HTTP istekleri gönderilmektedir.

---

## 🗄️ Database

Ana tablolar:

```text
users
 │
 ├── memories
 │      │
 │      └── comments
 │
 └── comments
```

Temel ilişkiler:

```text
User
 ├── has many → Memories
 └── has many → Comments

Memory
 ├── belongs to → User
 └── has many → Comments

Comment
 ├── belongs to → User
 └── belongs to → Memory
```

---

## 🗺️ Roadmap

* [x] FastAPI backend
* [x] PostgreSQL database
* [x] User registration
* [x] JWT authentication
* [x] E-mail verification
* [x] Memory CRUD
* [x] Comment CRUD
* [x] User CRUD
* [x] Android client başlangıcı
* [x] Retrofit API bağlantısı
* [ ] Ana sayfa tasarımı
* [ ] Kullanıcı profilleri
* [ ] Profil fotoğrafı yükleme
* [ ] Like sistemi
* [ ] Moderasyon sistemi
* [ ] AI destekli içerik kontrolü
* [ ] Bildirim sistemi
* [ ] Production deployment
* [ ] Google Play release

---

## 🤖 Planlanan AI Moderasyon Sistemi

İlerleyen sürümlerde paylaşılan içeriklerin otomatik olarak kontrol edilmesi planlanmaktadır.

```text
Yeni Memory
     │
     ▼
AI Moderation
     │
     ├──── Safe ────► Publish
     │
     └──── Review ──► Moderation Queue
```

Bu yapı sayesinde uygunsuz, hassas veya platform kurallarına aykırı içeriklerin kullanıcıya gösterilmeden önce değerlendirilmesi hedeflenmektedir.

---

## 🎯 Projenin Amacı

Er Meydanı sadece bir sosyal medya uygulaması değil, aynı zamanda modern backend mimarileri üzerine geliştirilmiş gerçek dünya odaklı bir yazılım projesidir.

Projede özellikle:

* REST API tasarımı
* Authentication
* Authorization
* Relational database tasarımı
* ORM kullanımı
* Android ↔ Backend iletişimi
* E-posta doğrulaması
* Güvenli kullanıcı yönetimi
* Asenkron API iletişimi
* Mobil uygulama geliştirme

konularına odaklanılmaktadır.

---

<div align="center">

## 👨‍💻 Developer

### Deniz Sarp Yazıcıoğlu

**Software Engineer • Backend Developer • Systems Programming**

<br>

<a href="https://github.com/YOUR_USERNAME">
<img src="https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge&logo=github">
</a>

<br><br>

Developed with ☕, Python and questionable amounts of debugging.

<br>

⭐ **Projeyi beğendiysen repository'ye star bırakabilirsin.**

</div>
