import os
import sys
import pandas as pd
from googleapiclient.discovery import build
from dotenv import load_dotenv
from transformers import pipeline
from huggingface_hub import HfApi

# 1. Load Environment Variables
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
HF_REPO_ID = os.getenv("HF_REPO_ID") # contoh: "username/tayen-nlp-public-perception-analysis"

if not YOUTUBE_API_KEY:
    print("ERROR: YOUTUBE_API_KEY belum diatur di dalam file .env")
    sys.exit(1)

# Konfigurasi Scraping
SEARCH_KEYWORD = "kebijakan pemerintah indonesia"
MAX_COMMENTS = 6000
MAX_VIDEOS_TO_SEARCH = 20 # Cari 20 video teratas terkait keyword
CSV_FILENAME = "youtube_dataset.csv"

# 2. Fetch YouTube Videos & Comments
def fetch_youtube_comments():
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    
    print(f"Mencari video dengan kata kunci: '{SEARCH_KEYWORD}'...")
    try:
        search_response = youtube.search().list(
            q=SEARCH_KEYWORD,
            part="id,snippet",
            maxResults=MAX_VIDEOS_TO_SEARCH,
            type="video",
            order="relevance" # Anda bisa menggantinya menjadi "date" jika ingin murni yang paling baru diupload
        ).execute()
    except Exception as e:
        print(f"Gagal mencari video. Pastikan API Key benar. Error: {e}")
        return pd.DataFrame()
    
    video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
    print(f"Ditemukan {len(video_ids)} video. Memulai ekstraksi komentar...")
    
    comments_data = []
    
    for video_id in video_ids:
        if len(comments_data) >= MAX_COMMENTS:
            break
            
        print(f"  -> Mengambil komentar dari video ID: {video_id}")
        try:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                textFormat="plainText"
            )
            
            while request and len(comments_data) < MAX_COMMENTS:
                response = request.execute()
                for item in response.get("items", []):
                    top_level_comment = item["snippet"]["topLevelComment"]["snippet"]
                    comments_data.append({
                        "Author": top_level_comment["authorDisplayName"],
                        "Komentar": top_level_comment["textDisplay"],
                        "VideoID": video_id
                    })
                    
                    if len(comments_data) >= MAX_COMMENTS:
                        break
                        
                request = youtube.commentThreads().list_next(request, response)
                
        except Exception as e:
            # Sering terjadi jika komentar dimatikan (disabled) pada video tertentu
            print(f"     [Lewati] Gagal/Komentar dimatikan pada video {video_id}.")
            
    print(f"\nBerhasil mengumpulkan {len(comments_data)} komentar total.")
    return pd.DataFrame(comments_data)

# 3. NLP Processing
def process_comments(df):
    if df.empty:
        print("DataFrame kosong, tidak ada yang diproses.")
        return df
        
    print("\nMemuat model NLP (IndoBERT Sentiment)...")
    # Menonaktifkan peringatan symlink dari HF Hub
    os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
    
    try:
        sentiment_pipeline = pipeline("sentiment-analysis", model="w11wo/indonesian-roberta-base-sentiment-classifier")
    except Exception as e:
        print(f"Gagal memuat model. Error: {e}")
        return df
    
    print(f"Memproses klasifikasi sentimen untuk {len(df)} komentar...")
    sentimen_results = []
    total = len(df)
    
    for i, text in enumerate(df['Komentar']):
        if (i+1) % 500 == 0:
            print(f"  -> Proses {i+1}/{total} selesai...")
            
        try:
            # Truncate string secara manual (maksimal karakter agar tidak OOM/Melebihi max_length token)
            safe_text = str(text)[:512]
            res = sentiment_pipeline(safe_text, truncation=True, max_length=512)[0] 
            raw_sent = res['label'].lower()
            label_map = {'positive': 'Positif', 'negative': 'Negatif', 'neutral': 'Netral'}
            sentimen_results.append(label_map.get(raw_sent, 'Netral'))
        except:
            sentimen_results.append('Netral')
            
    df['Sentimen AI'] = sentimen_results
    return df

# 4. Upload to Hugging Face
def upload_to_huggingface(filepath):
    if not HF_TOKEN or not HF_REPO_ID:
        print("\nPeringatan: HF_TOKEN atau HF_REPO_ID tidak ditemukan di .env")
        print("Silakan upload file CSV secara manual ke Hugging Face Spaces Anda.")
        return
        
    print(f"\nMengunggah '{filepath}' ke repositori HF: {HF_REPO_ID}...")
    try:
        api = HfApi()
        api.upload_file(
            path_or_fileobj=filepath,
            path_in_repo=filepath, # simpan dengan nama yang sama di root repo
            repo_id=HF_REPO_ID,
            repo_type="space", 
            token=HF_TOKEN
        )
        print("✅ Upload berhasil! Dashboard HF Anda sekarang menggunakan data terbaru.")
    except Exception as e:
        print(f"❌ Gagal mengunggah file. Error: {e}")
        print("Silakan lakukan upload manual.")

# ==========================================
# ALUR UTAMA
# ==========================================
if __name__ == "__main__":
    print("=== MULAI PROSES PEMBARUAN DATA (PIPELINE) ===")
    
    # Tahap 1: Ambil data dari YouTube
    df = fetch_youtube_comments()
    
    if not df.empty:
        # Tahap 2: Jalankan Prediksi NLP (AI)
        df_processed = process_comments(df)
        
        # Tahap 3: Simpan dan Timpa (Overwrite) File CSV Lama
        df_processed.to_csv(CSV_FILENAME, index=False)
        print(f"\n✅ Data sukses ditimpa dan disimpan ke lokal: '{CSV_FILENAME}'")
        
        # Tahap 4: Upload Otomatis
        upload_to_huggingface(CSV_FILENAME)
    else:
        print("Tidak ada data yang disimpan.")
        
    print("\n=== PIPELINE SELESAI ===")
