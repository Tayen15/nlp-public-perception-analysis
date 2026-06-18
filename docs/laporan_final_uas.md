# Laporan Proyek Analisis Persepsi Publik (Sentimen & Stance Detection)

Dokumen ini merupakan panduan lengkap dan draf laporan final proyek untuk keperluan Ujian Akhir Semester (UAS). Materi di dalamnya telah disusun berdasarkan **Rubrik Penilaian** agar dapat dengan mudah disalin ke format Microsoft Word/PDF.

---

## 1. Latar Belakang & Tujuan
### Latar Belakang
Di era digital, media sosial dan platform berbagi video seperti YouTube menjadi wadah utama bagi masyarakat untuk menyuarakan opini mereka terhadap isu-usul sosial, kenegaraan, dan kinerja pemerintahan. Ribuan komentar yang masuk tidak mungkin dianalisis secara manual oleh analis manusia. Tanpa bantuan teknologi, pemerintah atau pemangku kebijakan akan kehilangan *feedback loop* (umpan balik) yang sangat berharga terkait apakah sebuah kebijakan didukung atau justru ditolak keras oleh publik.

### Tujuan
Proyek ini bertujuan untuk membangun sebuah sistem *Natural Language Processing* (NLP) *End-to-End* (dari hulu ke hilir) yang secara otomatis mengekstrak, memproses, dan menganalisis komentar publik. Sistem ini tidak hanya mendeteksi "emosi" kata (Sentimen: Positif/Negatif), tetapi juga mengekstrak "sikap" (Stance: Dukungan/Kritikan), sehingga pemerintah bisa memahami esensi penolakan/dukungan secara komprehensif.

---

## 2. Dataset
Sistem ini menggunakan **pendekatan dataset ganda** yang melebihi batas minimal 10.000 data:
1. **Dataset Supervised Training (IndoNLU)**: ±11.000 data ulasan berbahasa Indonesia yang digunakan untuk melatih dan melakukan pengujian arsitektur dasar (*Deep Learning*).
2. **Dataset Domain-Specific (Komentar YouTube)**: Ekstraksi (*Scraping*) mandiri sebanyak 6.632 komentar unik yang berisi opini riil (*real-case*) dari warga net mengenai kinerja pemerintahan dan regulasi publik.
**Total Data yang diolah: > 17.000 data.** Hal ini masuk ke dalam kategori *Kreativitas* karena melibatkan dataset mandiri pada ranah *real case*.

---

## 3. Pipeline / Metode NLP
Proyek ini mengimplementasikan tahapan pemrosesan bahasa alami (NLP pipeline) standar industri:
1. **Data Cleaning**: Menghapus *noise* dari teks komentar YouTube (menghilangkan URL, karakter khusus, *mention*, tagar, dan emoji).
2. **Case Folding**: Mengubah semua huruf menjadi huruf kecil (*lowercase*) untuk menjaga konsistensi.
3. **Tokenisasi**:
   - Untuk eksperimen model LSTM tradisional, tokenisasi dilakukan di level kata (*Word-level Tokenization*).
   - Untuk Transformer, digunakan **Subword Tokenization** (BPE / WordPiece) yang sangat tangguh dalam menangani kata-kata gaul/singkatan khas warga net Indonesia (*Out-of-Vocabulary/OOV problem*).
4. **Stopword Removal & Stemming**: Membuang kata hubung tak bermakna (yang, dan, di) serta mengembalikan kata ke bentuk dasarnya menggunakan pustaka Sastrawi.
5. **Word Embedding**: 
   - Pada model klasik, kata diubah menjadi vektor angka (Dense Vectors) menggunakan *Embedding Layer*.
   - Pada model Transformer, *embedding* telah direpresentasikan oleh *Contextualized Embeddings* (di mana makna vektor sebuah kata bergantung pada seluruh kata lain dalam kalimat tersebut).

---

## 4. Model yang Digunakan (Eksperimen Multi-Model)
Proyek ini mengeksplorasi dua arsitektur untuk membandingkan kinerja teknologi.
### A. Model Tradisional: LSTM (Long Short-Term Memory)
- **Alasan Pemilihan LSTM vs RNN biasa**: RNN menderita *Vanishing Gradient Problem*, yang berarti ia mudah "lupa" kata-kata di awal kalimat ketika memproses kalimat yang panjang. LSTM memiliki *Cell State* dan *Gates* (Forget, Input, Output) yang memungkinkannya mengingat konteks jarak jauh. 
- Di proyek ini, LSTM menjadi basis pedagogis (pendidikan) untuk memahami cara kerja jaringan saraf tiruan menganalisis urutan (sekuens) teks.

### B. Model State-of-the-Art (Transformer / HuggingFace)
- **Model 1: IndoBERT (w11wo/indonesian-roberta-base-sentiment-classifier)**: Digunakan untuk Klasifikasi Sentimen Utama.
- **Model 2: XLM-RoBERTa (Zero-Shot Stance Detection)**: Digunakan untuk mengekstrak sikap (*Stance*) spesifik: "mendukung pemerintah" atau "mengkritik pemerintah".
- **Kenapa Transformer Cocok?**: Mekanisme **Self-Attention** pada Transformer mampu melihat teks tidak secara berurutan (kiri-ke-kanan), melainkan keseluruhan kalimat secara bersamaan (Bidirectional). Ini sangat cocok untuk bahasa Indonesia yang strukturnya dinamis, sehingga konteks ironi, sarkasme, dan penekanan makna ditangkap jauh lebih baik dari LSTM.

---

## 5. Implementasi Sistem (End-to-End)
Arsitektur yang dibangun melampaui aplikasi Jupyter Notebook sederhana (*Production-Ready / Decoupled Architecture*):
1. **Data Engineering**: Jupyter Notebook (`public_perception_analysis.ipynb`) digunakan untuk pembersihan data, *training* LSTM, dan evaluasi awal (menghasilkan CSV hasil bersih).
2. **AI Backend Server**: Dibangun menggunakan **FastAPI**, menyediakan akses *endpoint* REST API berkecepatan tinggi yang memuat model Transformer ke dalam memori.
3. **Antarmuka (Frontend)**:
   - **Gradio UI**: Disediakan sebagai *dashboard* *machine learning* klasik (`/gradio`).
   - **Web App Kustom (Vite + Vanilla JS)**: Antarmuka *Dark Mode* modern yang dibangun secara terpisah untuk menunjukkan kapabilitas integrasi antara AI dan *Web Engineering*.
Ini menunjukkan bahwa sistem dapat digunakan secara riil (di-*deploy* lintas platform).

---

## 6. Hasil & Evaluasi (Eksperimen & Analisis Error)
### Hasil Perbandingan
Dalam *pipeline* Jupyter Notebook, LSTM dilatih menggunakan ribuan data IndoNLU. Namun, untuk data riil dari YouTube yang penuh singkatan dan sarkasme:
- **LSTM** terkadang terjebak pada kata-kata ambigu dan memiliki akurasi F1-Score yang lebih rendah karena tidak memahami *contextual nuances* sebaik Transformer.
- **IndoBERT** memberikan hasil luar biasa dalam mengklasifikasikan "Positif/Negatif/Netral" dengan probabilitas keyakinan yang tinggi.

### Analisis Error & Solusi Inovatif (Zero-Shot Integration)
- **Kelemahan Klasik (Error Analysis)**: Sentimen analis sering dikelabui oleh **Sarkasme**. Contoh: *"Bagus banget pak kebijakannya, sampai-sampai rakyat pada nangis saking bagusnya"*. Model sentimen dasar terkadang membaca kata "Bagus" sebagai sentimen Positif.
- **Solusi**: Itulah mengapa kami menambahkan **Zero-Shot Stance Detection (XLM-RoBERTa)**. Jika kalimat di atas dimasukkan, Stance Detection akan menyadari bahwa tujuan esensial dari kalimat tersebut masuk ke kelas label "mengkritik pemerintah". Sistem **Multi-Model** ini menutupi kelemahan satu sama lain.

---

## 7. Kesimpulan
Proyek ini membuktikan bahwa pengolahan teks komentar publik yang ekstensif (> 17.000 data) dapat dilakukan secara terstruktur menggunakan NLP. Penggunaan LSTM terbukti memberikan landasan pemahaman sekuens teks, namun penggunaan arsitektur berbasis *Self-Attention* (Transformer) adalah solusi mutlak untuk menangani data tidak terstruktur di dunia nyata (YouTube). Terlebih lagi, integrasi API independen dan Antarmuka Web Kustom membuktikan bahwa solusi ini sangat relevan untuk diadaptasi oleh lembaga negara sebagai dasbor analitik sentimen publik yang komprehensif.

---

## 💡 Panduan Presentasi untuk Anggota Tim (Tips Menjawab Pertanyaan Dosen)
Berikut adalah referensi jawaban jika ditanya saat demo:
1. **"Kenapa pakai 2 model (Sentimen & Zero Shot)?"**
   > *"Karena NLP punya kelemahan membaca sarkasme, Pak/Bu. Kadang netizen memuji padahal menyindir. Sentimen mendeteksi emosi katanya, lalu Zero-Shot menebak sikap aslinya (mendukung atau mengkritik). Ini meminimalisir kesalahan analisis."*
2. **"Apa susahnya pakai Transformer disbanding LSTM?"**
   > *"LSTM mengurutkan teks kata-per-kata dari kiri ke kanan. Jika kalimatnya panjang, LSTM bisa lupa konteks kata di depan. Transformer menggunakan fitur Self-Attention, sehingga ia bisa melihat semua kata sekaligus dan mengerti hubungan makna kata depan dengan kata paling belakang (Bidirectional)."*
3. **"Ini implementasinya bagaimana?"**
   > *"Aplikasi kami dipisah (Decoupled), Pak/Bu. Otak AI-nya berjalan di Python (FastAPI), sementara wajah aplikasinya (Web Dasbor) di-coding pakai JavaScript. Ini membuatnya ringan, tidak kaku, dan persis seperti arsitektur software komersial."*
