# Laporan Proyek Analisis Persepsi Publik (Sentimen & Stance Detection)

Dokumen ini merupakan laporan akademik komprehensif untuk keperluan Ujian Akhir Semester (UAS). 

---

## 1. Latar Belakang & Tujuan
**Latar Belakang:** Di era digital, YouTube menjadi wadah utama bagi masyarakat untuk menyuarakan opini terkait isu kenegaraan. Tanpa bantuan AI, pemerintah kehilangan *feedback loop* yang berharga.  
**Tujuan:** Membangun sistem *Natural Language Processing* (NLP) *End-to-End* yang mengekstrak, memproses, dan menganalisis komentar publik. Sistem ini mendeteksi emosi kata (Sentimen: Positif/Negatif) dan mengekstrak "sikap" asli (Stance: Dukungan/Kritikan).

## 2. Dataset (>17.000 Data)
Proyek ini memenuhi batas minimal 10.000 data:
1. **Dataset Supervised (IndoNLU)**: ±11.000 data ulasan berbahasa Indonesia untuk melatih arsitektur *Deep Learning* dasar (LSTM).
2. **Dataset Domain-Specific (Scraping Mandiri)**: 6.632 komentar YouTube riil mengenai kinerja pemerintahan. Ini merupakan poin kreativitas tambahan (*real-case*).

## 3. Pipeline / Metode NLP
1. **Data Cleaning**: Menghapus URL, tagar, emoji, dan karakter khusus.
2. **Case Folding**: Mengubah teks menjadi *lowercase*.
3. **Tokenisasi**: *Word-level* (LSTM) dan *Subword BPE/WordPiece* (Transformer) untuk mengatasi kata gaul.
4. **Stopword Removal & Stemming**: Menggunakan Sastrawi.
5. **Word Embedding**: *Dense Vectors* untuk LSTM, *Contextualized Embeddings* untuk Transformer.

## 4. Model yang Digunakan (Eksperimen Multi-Model)
- **A. LSTM (Tradisional)**: Basis pedagogis karena LSTM mengingat konteks jarak jauh melalui *Cell State* (mengatasi kelemahan RNN biasa).
- **B. Transformer (HuggingFace)**: Menggunakan IndoBERT (Klasifikasi Sentimen) dan XLM-RoBERTa (Zero-Shot Stance Detection). Transformer membaca kalimat secara utuh (*Bidirectional / Self-Attention*), sehingga jauh lebih pintar memahami bahasa slang dan dinamis.

## 5. Implementasi Sistem (End-to-End)
Arsitektur dipisah (*Decoupled Production-Ready*):
- **Data Engineering**: Eksperimen dilakukan di Jupyter Notebook.
- **AI Backend**: Menggunakan **FastAPI** untuk REST API yang asinkronus dan cepat.
- **Frontend Kustom**: Web Dasbor elegan dibangun menggunakan Vite + Vanilla JS (di-deploy terpisah), disamping antarmuka *default* bawaan yaitu **Gradio**.

## 6. Hasil & Evaluasi (Analisis Error)
- **LSTM** sering kebingungan dengan teks YouTube karena keterbatasan pemahaman konteks informal.
- **Analisis Error (Kelemahan Sentimen)**: Model NLP sering tertipu **Sarkasme**. Contoh: *"Bagus sekali kebijakannya, bikin rakyat miskin"*. Model Sentimen membaca "Bagus" sebagai Positif.
- **Solusi / Tuning**: Oleh sebab itu, kami menambahkan model kedua yaitu **Zero-Shot Stance Detection**. Stance Detection akan menelaah sikap (mendukung/mengkritik). Hasilnya sistem tidak lagi tertipu oleh sarkasme!

## 7. Kesimpulan
Proyek ini membuktikan pengolahan >17.000 komentar secara sukses. LSTM memberikan dasar teori sekuensial, sedangkan sistem *Multi-Model Transformer* adalah solusi industri untuk menangani bahasa riil (sarkasme/slang). Implementasi *FastAPI* dan *Web Dasbor* membuktikan AI ini siap diaplikasikan di lembaga pemerintahan.

---
### 💡 FAQ & Tips Presentasi
- **Tanya**: Kenapa butuh 2 model AI (Sentimen dan Zero-Shot)?
- **Jawab**: *Karena Sentimen hanya membaca emosi kata dan rentan tertipu sarkasme netizen. Zero-Shot bertugas membaca 'Sikap' (apakah dia mengkritik atau mendukung). Keduanya bekerja sama menutupi kelemahan satu sama lain.*
- **Tanya**: Kenapa Transformer lebih baik dari LSTM?
- **Jawab**: *LSTM membaca dari kiri ke kanan sehingga gampang lupa konteks di depan jika kalimatnya panjang. Transformer menggunakan fitur Self-Attention yang melihat semua susunan kata bolak-balik sekaligus, sehingga sangat tajam memahami bahasa gaul Indonesia.*
