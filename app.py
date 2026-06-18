import os
from dotenv import load_dotenv

load_dotenv()

# Set HF_HOME before importing transformers
os.environ["HF_HOME"] = "./hf_cache"

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from transformers import pipeline
import gradio as gr

app = FastAPI(title="NLP Public Perception API & Gradio")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load NLP Models
print("Memuat model NLP...")
try:
    sentiment_pipeline = pipeline("sentiment-analysis", model="w11wo/indonesian-roberta-base-sentiment-classifier")
    has_sentiment_model = True
except Exception as e:
    print(f"Gagal memuat model sentimen: {e}")
    has_sentiment_model = False

try:
    zero_shot_pipeline = pipeline("zero-shot-classification", model="joeddav/xlm-roberta-large-xnli")
    has_stance_model = True
except Exception as e:
    print(f"Gagal memuat model Zero-Shot: {e}")
    has_stance_model = False

print("Model siap digunakan.")

from fastapi.responses import RedirectResponse

# API ENDPOINT

@app.get("/")
def read_root():
    # Otomatis alihkan (redirect) halaman utama ke UI Gradio
    return RedirectResponse(url="/gradio")

class PredictRequest(BaseModel):
    text: str

@app.get("/api/stats")
def get_dashboard_stats():
    if os.path.exists("youtube_dataset.csv"):
        df = pd.read_csv("youtube_dataset.csv")
        
        if "Sentimen AI" not in df.columns:
            stats = {"Positif": len(df)//3, "Netral": len(df)//3, "Negatif": len(df) - 2*(len(df)//3)}
        else:
            counts = df["Sentimen AI"].value_counts().to_dict()
            stats = {
                "Positif": counts.get("Positif", 0),
                "Netral": counts.get("Netral", 0),
                "Negatif": counts.get("Negatif", 0)
            }
            
        recent_comments = []
        for _, row in df.head(5).iterrows():
            recent_comments.append({
                "author": row.get("Author", "Anonim"),
                "text": row.get("Komentar", ""),
                "sentiment": row.get("Sentimen AI", "Netral")
            })
            
        return {
            "total_comments": len(df),
            "stats": stats,
            "recent_comments": recent_comments
        }
    else:
        return {"total_comments": 0, "stats": {"Positif": 0, "Netral": 0, "Negatif": 0}, "recent_comments": []}

@app.post("/api/predict")
def predict_text(req: PredictRequest):
    text = req.text
    
    # Sentiment Analysis
    try:
        sent_res = sentiment_pipeline(text, truncation=True, max_length=512)[0]
        raw_sent = sent_res['label'].lower()
        label_map = {'positive': 'Positif', 'negative': 'Negatif', 'neutral': 'Netral'}
        sentiment = label_map.get(raw_sent, 'Netral')
    except:
        sentiment = "Netral"
        
    # Zero-Shot Stance Detection
    try:
        candidate_labels = ["mendukung pemerintah", "mengkritik pemerintah"]
        zs_res = zero_shot_pipeline(text, candidate_labels, truncation=True, max_length=512)
        best_label = zs_res['labels'][0]
        if "mendukung" in best_label:
            perception = "Dukungan (Positif)"
        else:
            perception = "Kritikan (Negatif)"
    except:
        perception = "Netral (Gagal)"
        
    return {"text": text, "sentiment": sentiment, "stance": perception}

# ==========================================
# 2. Gradio Interface
# ==========================================

def analyze_perception_gradio(text):
    if not text.strip():
        return "Teks kosong", "Tidak diketahui"

    if has_sentiment_model:
        try:
            sent_result = sentiment_pipeline(text, truncation=True, max_length=512)
            label_sent = sent_result[0]["label"].title()
            score_sent = sent_result[0]["score"] * 100
            sentiment = f"{label_sent} ({score_sent:.1f}%)"
        except:
            sentiment = "Error Sentimen"
    else:
        sentiment = "Model tidak tersedia"

    if has_stance_model:
        try:
            candidate_labels = ["dukungan", "kritikan", "netral"]
            result = zero_shot_pipeline(text, candidate_labels, truncation=True, max_length=512)
            top_label = result["labels"][0].title()
            top_score = result["scores"][0] * 100
            perception = f"{top_label} ({top_score:.1f}%)"
        except:
            perception = "Error Stance"
    else:
        if "Positif" in sentiment: perception = "Dukungan"
        elif "Negatif" in sentiment: perception = "Kritikan"
        else: perception = "Netral"

    return sentiment, perception

with gr.Blocks(title="NLP Analysis") as demo:
    gr.Markdown("# Analisis Persepsi Publik")
    gr.Markdown("Klasifikasi sentimen dan stance menggunakan IndoBERT & Zero-Shot ML.")

    with gr.Row():
        with gr.Column():
            input_text = gr.Textbox(lines=5, label="Input Komentar", placeholder="Contoh: Kebijakan ini sangat merugikan.")
            submit_btn = gr.Button("Analisis", variant="primary")
            gr.Examples(
                examples=["Sangat mendukung regulasi baru ini.", "Aturannya tidak jelas dan menyusahkan."],
                inputs=input_text
            )

        with gr.Column():
            out_sentiment = gr.Label(label="Sentimen")
            out_perception = gr.Label(label="Stance")

    submit_btn.click(fn=analyze_perception_gradio, inputs=input_text, outputs=[out_sentiment, out_perception])

app = gr.mount_gradio_app(app, demo, path="/gradio")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
