# Analisis Persepsi Publik Terhadap Isu Kenegaraan (NLP)

Repositori ini memuat implementasi *Natural Language Processing* (NLP) *End-to-End* untuk melakukan Klasifikasi Sentimen dan *Zero-Shot Stance Detection* (Dukungan vs Kritikan) pada komentar YouTube terkait isu kenegaraan.

Proyek ini dibangun menggunakan arsitektur *Decoupled* yang siap produksi (Production-Ready) menggunakan perpaduan **FastAPI**, **Gradio**, dan **Vite (Vanilla JS)**.

## 📖 Laporan Lengkap (Untuk UAS)
Jika Anda mencari laporan akademik yang berisi Latar Belakang, Penjelasan Model (LSTM vs Transformer), Evaluasi, dan Kesimpulan, silakan buka file berikut:
👉 [**docs/LAPORAN_FINAL_UAS.md**](./docs/LAPORAN_FINAL_UAS.md)

---

## 📂 Struktur Direktori
```text
nlp-uas/
├── docs/                      # Dokumentasi Proyek (Laporan Akademik Lengkap)
├── frontend/                  # Source code Web App Dasbor (Vite, JS, CSS)
├── app.py                     # Mesin Utama (FastAPI Backend + Gradio Mount)
├── Dockerfile                 # Konfigurasi deployment untuk Hugging Face Docker
├── requirements.txt           # Daftar pustaka Python (Dependencies)
├── public_perception_analysis.ipynb # Workspace eksperimen Data Science (Training LSTM dll)
└── youtube_dataset.csv        # Dataset komentar YouTube (>6.000 baris)
```

---

## 🚀 Panduan Menjalankan Sistem Secara Lokal

### 1. Menjalankan Backend API & UI Gradio (Python)
Pastikan Anda sudah menginstal seluruh dependensi di `requirements.txt` dan berada di dalam *Virtual Environment*.
```bash
uvicorn app:app --reload
```
- Endpoint API Utama berjalan di: `http://127.0.0.1:8000`
- UI Interaktif Klasik (Gradio) berjalan di: `http://127.0.0.1:8000/gradio`

### 2. Menjalankan Web Dashboard Kustom (Vite JS)
Buka terminal *baru* (jangan matikan terminal Python), lalu masuk ke folder frontend:
```bash
cd frontend
npm run dev
```

---

## 🌐 Panduan Deployment (Hugging Face Spaces)
Proyek ini dikonfigurasi untuk berjalan di sistem **Docker** Hugging Face.
1. Buat **Space Baru** di Hugging Face (Pilih SDK: **Docker** -> *Blank template*).
2. Lakukan *push* atau unggah file `app.py`, `Dockerfile`, `requirements.txt`, dan dataset `.csv` ke repositori Space tersebut.
3. Masuk ke tab **Settings** di Hugging Face Space Anda $\rightarrow$ Pilih **Variables and secrets**.
4. Tambahkan *New Secret* bernama `HF_TOKEN` dan isikan Token Akses Hugging Face Anda yang bertipe *Write*.
5. Sistem akan otomatis membangun *container* dan meluncurkan AI Anda!
