# Analisis Persepsi Publik Terhadap Isu Kenegaraan di YouTube

## Latar Belakang Project
Seiring dengan masifnya penggunaan media sosial di Indonesia, YouTube menjadi salah satu platform utama bagi masyarakat untuk menyuarakan opini mereka terkait isu-isu kenegaraan dan politik (seperti kunjungan kenegaraan, kebijakan publik, dll). Opini ini sangat kaya akan informasi namun sulit dianalisis secara manual karena volumenya yang sangat besar.

## Rumusan Masalah
Bagaimana cara mengklasifikasikan komentar publik di YouTube secara otomatis tidak hanya berdasarkan sentimennya (Positif/Netral/Negatif), tetapi juga mengekstrak persepsi atau *stance* spesifik masyarakat, yaitu membedakan antara **Dukungan** dan **Kritik** terhadap pemberitaan kenegaraan?

## Tujuan Project
- Membangun sistem *Natural Language Processing* (NLP) *end-to-end* yang mampu melakukan dua *task* utama: **Analisis Sentimen** dan **Analisis Persepsi (Dukungan vs Kritik)**.
- Membandingkan performa antara arsitektur klasik (RNN/LSTM) dengan arsitektur modern (Transformer/IndoBERT) dalam memahami bahasa Indonesia pada platform media sosial.

## Rencana Dataset
- **Data Training**: Dataset standar publik berbahasa Indonesia (seperti IndoNLU) akan digunakan untuk membangun dasar pemahaman bahasa (*pre-training/fine-tuning*).
- **Data Uji (Studi Kasus)**: Data riil berupa komentar dari YouTube pada video-video pemberitaan kenegaraan spesifik (misalnya studi kasus video kunjungan Prabowo & Mayor Teddy atau isu kenegaraan lainnya).

## Pipeline NLP
1. **Pengumpulan Data**: Penarikan komentar secara dinamis menggunakan YouTube API.
2. **Preprocessing**: *Cleaning* (menghapus *stopwords*, *mentions*, emoji) menggunakan pustaka Sastrawi dan Regex.
3. **Representasi Teks**: Tokenisasi dan *Word Embeddings*.
4. **Pemodelan**: *Training* dua jenis model terpisah untuk Sentimen dan Persepsi.
5. **Evaluasi**: Menggunakan metrik *Accuracy*, *Precision*, *Recall*, dan *F1-Score*.

## Rencana Perbandingan Model
Eksperimen akan menguji dua teknologi berikut secara *head-to-head*:
1. **Model RNN/LSTM/GRU**: Dibangun *from scratch* menggunakan PyTorch untuk melihat kemampuan menangkap konteks sekuensial dasar.
2. **Transformer (Hugging Face)**: Melakukan *fine-tuning* pada *pre-trained model* (IndoBERT) untuk melihat keunggulan *attention mechanism* pada teks kompleks/slang.

## Rencana Deployment
Sistem akan di-deploy menggunakan antarmuka **Gradio** dan di-hosting ke **Hugging Face Spaces**. Sistem ini akan menerima teks input dan secara langsung menampilkan klasifikasi sentimen serta dimensi persepsi (Dukungan/Kritik).

## Struktur Folder
```
uas-nlp-public-perception/
├── README.md                          # Dokumentasi utama project
├── requirements.txt                   # Daftar dependency Python
├── .gitignore                         # File ignore untuk Git
├── app.py                             # Script deployment / antarmuka Gradio
├── public_perception_analysis.ipynb   # Notebook workspace untuk semua eksperimen NLP
├── data/
│   ├── raw/                           # Data mentah (hasil crawling / download)
│   └── processed/                     # Data bersih siap training
├── models/                            # Tempat menyimpan model yang sudah di-train (.pth / .bin)
├── outputs/
│   ├── figures/                       # Grafik hasil visualisasi/evaluasi
│   └── metrics/                       # Log evaluasi dan metrik performa
└── reports/                           # Laporan final (PDF/Markdown)
```

## Roadmap Project
- [ ] Pengumpulan data (API YouTube & Dataset Publik)
- [ ] *Cleaning* dan *Preprocessing* teks
- [ ] Pembuatan dan Pelatihan Model Sentimen Utama
- [ ] Pembuatan dan Pelatihan Model Dimensi Persepsi (Dukungan/Kritik)
- [ ] Evaluasi dan Komparasi Model (RNN vs Transformer)
- [ ] *Deployment* ke Hugging Face Spaces dengan Gradio

## Cara Menjalankan Project

### 1. Eksperimen (Notebook)
Untuk melakukan *training*, evaluasi, dan pemrosesan data:
1. Pastikan *virtual environment* sudah aktif.
2. Install dependency: `pip install -r requirements.txt`
3. Jalankan Jupyter: `jupyter lab` atau `jupyter notebook`
4. Buka file `public_perception_analysis.ipynb` dan ikuti *cell* secara berurutan.

### 2. Aplikasi (Gradio)
Untuk menjalankan antarmuka prediksi *real-time*:
1. Pastikan *virtual environment* sudah aktif.
2. Jalankan perintah: `python app.py`
3. Buka tautan lokal (contoh: `http://127.0.0.1:7860`) di peramban Anda.
