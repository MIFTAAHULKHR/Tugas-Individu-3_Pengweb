# 📊 Product Review Analyzer - Tugas Individu 3

## 🎯 Deskripsi Proyek
**Product Review Analyzer** adalah aplikasi web *full-stack* yang dapat menganalisis ulasan produk teks. Aplikasi ini menggunakan kecerdasan buatan (AI) untuk melakukan analisis sentimen secara otomatis dan mengekstrak poin-poin kunci dari ulasan pengguna. Aplikasi ini dibangun untuk memenuhi Tugas Individu 3 mata kuliah Praktikum Pemrograman Web dan menggabungkan beberapa teknologi modern dalam satu sistem yang fungsional.

**Tampilan Aplikasi:**
![Tampilan Aplikasi Product Review Analyzer](tampilan.png)

### ✨ Fitur Utama
1. **📝 Input Ulasan Produk** - Pengguna dapat memasukkan teks ulasan produk melalui form di antarmuka React.
2. **🧠 Analisis Sentimen Otomatis** - Menggunakan model Hugging Face untuk mengklasifikasikan sentimen menjadi **Positif**, **Negatif**, atau **Netral**.
3. **🔑 Ekstraksi Poin Kunci** - Memanfaatkan Google Gemini API untuk mengekstrak poin-poin penting dari ulasan.
4. **📊 Tampilan Hasil Interaktif** - Menampilkan hasil analisis dengan visualisasi yang jelas di frontend React.
5. **💾 Penyimpanan Data** - Menyimpan semua hasil analisis ke database PostgreSQL dengan integrasi SQLAlchemy.

## 🏗️ Teknologi yang Digunakan

### **Backend** (`/backend`)
- **Python 3.13** - Bahasa pemrograman utama
- **Flask** - Web framework (menggantikan Pyramid karena kompatibilitas)
- **SQLAlchemy** - ORM untuk database
- **PostgreSQL** - Database relasional
- **Transformers (Hugging Face)** - Untuk analisis sentimen
- **Google Generative AI** - Untuk ekstraksi poin kunci
- **python-dotenv** - Management environment variables

### **Frontend** (`/frontend`)
- **React 18** - Library untuk membangun antarmuka pengguna
- **Axios** - Untuk komunikasi dengan API backend
- **CSS3** - Styling dengan custom CSS

### **Lainnya**
- **Git** - Version control
- **npm** - Package manager untuk JavaScript
- **pip** - Package manager untuk Python

## 📁 Struktur Proyek

```
product-review-analyzer/
│
├── backend/                         
│   ├── flask_app.py                
│   ├── requirements.txt            
│   ├── .env                         
│   ├── database.py                  
│   ├── models.py                   
│   ├── sentiment_analyzer.py       
│   ├── keypoints_extractor.py       
│   ├── create_tables.py            
│   └── test_api.py                 
│
├── frontend/                      
│   │   ├── index.html             
│   │   └── favicon.ico            
│   │
│   ├── src/
│   │   ├── App.js                  
│   │   ├── App.css                 
│   │   ├── index.js               
│   │   ├── index.css             
│   │   │
│   │   ├── components/             
│   │   │   ├── ReviewForm.js     
│   │   │   ├── ReviewList.js     
│   │   │   └── SentimentDisplay.js 
│   │   │
│   │   └── services/              
│   │       └── api.js              
│   │
│   ├── package.json               
│   └── package-lock.json         
├── README.md                     
├── run_all.bat                     
├── setup_frontend.bat              
├── setup_backend.bat              
└── tampilan.png                   
```

**Catatan Struktur:** Struktur frontend mengikuti prinsip modularitas dan pemisahan concern yang memudahkan pemeliharaan dan pengembangan.

## ⚙️ Instalasi dan Konfigurasi

### **Prerequisites**
1. **Python 3.13** (atau versi 3.11/3.10 untuk kompatibilitas lebih baik)
2. **Node.js 16+** dan **npm**
3. **PostgreSQL** (atau SQLite untuk kemudahan)
4. **API Keys**:
   - [Google Gemini API Key](https://makersuite.google.com/app/apikey)
   - (Opsional) Hugging Face Token

### **Langkah 1: Clone Repository**
```bash
git clone <repository-url>
cd product-review-analyzer
```

### **Langkah 2: Setup Backend**
```bash
cd backend

# Install dependencies Python
pip install -r requirements.txt

# Atau install manual jika requirements.txt tidak ada
pip install flask flask-cors sqlalchemy psycopg2-binary python-dotenv transformers torch google-generativeai requests

# Buat file .env
echo "DATABASE_URL=postgresql://username:password@localhost:5432/review_db
GEMINI_API_KEY=your_gemini_api_key_here
PYRAMID_SECRET=mysecretkey123" > .env

# Buat tabel database
python create_tables.py
```

### **Langkah 3: Setup Frontend**
```bash
cd ../frontend

# Install dependencies JavaScript
npm install

# Atau jika ada error, clean install
rmdir /s /q node_modules 2>nul
del package-lock.json 2>nul
npm install
```

### **Langkah 4: Konfigurasi Database**
**Opsi A: PostgreSQL** (direkomendasikan)
```sql
CREATE DATABASE review_db;
CREATE USER review_user WITH PASSWORD 'review_password';
GRANT ALL PRIVILEGES ON DATABASE review_db TO review_user;
```

**Opsi B: SQLite** (lebih mudah)
Ubah `DATABASE_URL` di `.env` menjadi:
```
DATABASE_URL=sqlite:///./reviews.db
```

## 🚀 Menjalankan Aplikasi

### **Metode 1: Manual (2 Terminal)**
**Terminal 1 - Backend:**
```bash
cd backend
python flask_app.py
# Server berjalan di http://localhost:5000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
# Aplikasi terbuka di http://localhost:3000
```

### **Metode 2: Menggunakan Script Batch (Windows)**
```bash
# Jalankan script run_all.bat
run_all.bat
```

### **Metode 3: Menggunakan Docker** (opsional)
```bash
docker-compose up --build
```

## 📡 API Endpoints

### **1. `POST /api/analyze-review`**
Menganalisis ulasan produk baru.

**Request:**
```json
{
  "review_text": "This product is amazing! Great quality and fast delivery."
}
```

**Response:**
```json
{
  "id": 1,
  "review_text": "This product is amazing! Great quality and fast delivery.",
  "sentiment": "positive",
  "key_points": [
    "Excellent product quality",
    "Fast delivery service",
    "Positive customer experience"
  ],
  "created_at": "2025-12-14T16:17:15.123456",
  "message": "Review analyzed successfully"
}
```

### **2. `GET /api/reviews`**
Mendapatkan semua ulasan yang telah dianalisis.

**Response:**
```json
{
  "reviews": [
    {
      "id": 1,
      "review_text": "This product is amazing! Great quality and fast delivery.",
      "sentiment": "positive",
      "key_points": ["Excellent quality", "Fast delivery"],
      "created_at": "2025-12-14T16:17:15.123456"
    }
  ],
  "count": 1
}
```

### **3. `GET /api/health`**
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Product Review Analyzer",
  "database": "connected",
  "sentiment_analyzer": "loaded",
  "gemini_api": "loaded"
}
```

## 🔧 Troubleshooting Umum

### **1. Error: "Proxy error: ECONNREFUSED"**
**Penyebab:** Backend Flask tidak berjalan.
**Solusi:** Pastikan `python flask_app.py` berjalan di terminal terpisah sebelum menjalankan `npm start`.

### **2. Error: "No module named 'transformers'"**
**Solusi:**
```bash
cd backend
pip install transformers torch
```

### **3. Error: "Could not find a required file. Name: index.html"**
**Solusi:** Pastikan folder `public/` dan file `index.html` ada di `frontend/`.

### **4. Error Database Connection**
**Solusi:** Periksa `DATABASE_URL` di `.env` dan pastikan PostgreSQL service berjalan.

### **5. Error Gemini API**
**Solusi:** Periksa API key di `.env` dan kunjungi [Google AI Studio](https://makersuite.google.com/app/apikey) untuk membuat key baru.

## 🧪 Testing Aplikasi

### **Test API dengan curl:**
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test analyze endpoint
curl -X POST http://localhost:5000/api/analyze-review \
  -H "Content-Type: application/json" \
  -d '{"review_text": "This is the worst product I have ever bought!"}'

# Test get reviews endpoint
curl http://localhost:5000/api/reviews
```

### **Contoh Input untuk Testing:**
1. **Positif:** "Sony WH-1000XM5 headphones are fantastic! The noise cancellation is incredible."
2. **Negatif:** "Terrible product! Broke after 2 weeks and customer service was unhelpful."
3. **Netral:** "The product has good features but the price is quite high for what it offers."

## 📚 Dokumentasi Teknis Tambahan

### **Analisis Sentimen**
Menggunakan model `distilbert-base-uncased-finetuned-sst-2-english` dari Hugging Face untuk klasifikasi sentimen. Model ini memberikan akurasi yang baik dengan ukuran model yang relatif kecil.

### **Ekstraksi Poin Kunci** 
Menggunakan Google Gemini Pro model dengan prompt engineering untuk mengekstrak 3-5 poin kunci dari ulasan dalam format JSON.

### **Struktur Database**
Tabel `reviews` memiliki struktur:
- `id` (SERIAL, PRIMARY KEY)
- `review_text` (TEXT, NOT NULL)
- `sentiment` (VARCHAR(20), NOT NULL)
- `key_points` (TEXT) - Disimpan sebagai JSON string
- `created_at` (TIMESTAMP WITH TIME ZONE, DEFAULT now())

## 👥 Kontributor
- **Nama:** Miftahul Khoiriyah
- **NIM:** [123140064]
- **Mata Kuliah:** Praktikum Pemrograman Web
- **Semester:** 5

## 📄 Lisensi
Proyek ini dibuat untuk tujuan akademik. Semua hak cipta pada kode sumber dimiliki oleh pembuat.

## 🔗 Link Penting
- **GitHub Repository:** [https://github.com/MIFTAAHULKHR/Tugas-Individu-3_Pengweb](https://github.com/MIFTAAHULKHR/Tugas-Individu-3_Pengweb)
- **Demo Aplikasi:** [http://localhost:3000](http://localhost:3000) (setelah dijalankan lokal)


