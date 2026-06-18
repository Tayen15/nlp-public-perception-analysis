# Laporan Proyek UAS: Analisis Sentimen Komentar Sosial Media

## 1. Latar Belakang & Tujuan
*(Tuliskan 1-2 paragraf di sini. Contoh: Proyek ini bertujuan menganalisis opini publik (sentimen) terhadap tokoh politik, dalam hal ini Prabowo dan Mayor Teddy, berdasarkan komentar di YouTube. Tujuannya untuk melihat perbandingan efektivitas model RNN dan Transformer pada data teks Bahasa Indonesia).*

## 2. Dataset
*(Jelaskan dua jenis data yang digunakan)*
- **Data Latih (Training)**: Kami menggunakan dataset publik **IndoNLU (SmSA)** yang berisi ~11.000 data teks berbahasa Indonesia dengan label Positif, Negatif, dan Netral. Memenuhi syarat minimal 10.000 data.
- **Data Uji (Aplikasi)**: Komentar yang diambil secara *real-time* dari YouTube menggunakan Google API, difokuskan pada video kunjungan kenegaraan Prabowo & Mayor Teddy.

## 3. Pipeline / Metode NLP
*(Jelaskan alur data Anda)*
1. **Data Ingestion**: Menarik komentar via API YouTube.
2. **Preprocessing**: 
   - *Cleaning* (menghapus URL, mention, simbol).
   - *Stopword Removal* dan *Stemming* menggunakan pustaka `Sastrawi` (khusus untuk RNN).
3. **Modeling**: Melatih model dengan dataset IndoNLU (11k data).
4. **Evaluasi & Inference**: Mengukur performa model dan melakukan prediksi pada data komentar YouTube.

## 4. Model yang Digunakan
*(Proyek ini memenuhi syarat 2 teknologi bebas)*
1. **RNN (LSTM)**: Dibangun menggunakan PyTorch dari awal (*from scratch*). Menggunakan arsitektur embedding layer, LSTM cell, dan fully connected layer.
2. **Transformer (Hugging Face)**: Menggunakan model *pre-trained* berbahasa Indonesia (IndoBERT) yang di-*fine-tune* khusus untuk klasifikasi 3 kelas.

## 5. Implementasi Sistem
*(Tuliskan teknologi yang dipakai)*
- **Bahasa**: Python
- **Pustaka Utama**: PyTorch, Transformers (Hugging Face), Scikit-Learn, Sastrawi.
- **Aplikasi Antarmuka**: Dibangun menggunakan **Gradio** dan siap di-deploy ke **Hugging Face Spaces** agar pengguna bisa memasukkan teks/komentar dan langsung melihat hasil prediksi.

## 6. Hasil & Evaluasi
*(Bagian ini diisi setelah Anda menjalankan training hingga selesai)*
- Akurasi Model RNN: ...
- Akurasi Model Transformer: ... (Biasanya Transformer lebih tinggi)
- Analisis singkat mengapa model yang satu lebih baik dari yang lain.

## 7. Kesimpulan
*(1 paragraf kesimpulan)*
Model Transformer berbasis arsitektur BERT terbukti lebih andal dalam menangani konteks dan slang bahasa Indonesia dibandingkan LSTM tradisional, terlihat dari hasil pengujian dan prediksi sentimen di komentar YouTube.
