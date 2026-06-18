// GANTI URL DI BAWAH INI DENGAN URL HUGGING FACE SPACES ANDA SAAT DEPLOY FRONTEND
// Contoh: "https://nama-anda-nlp-uas.hf.space"
const API_URL = "http://127.0.0.1:8000";

// Load Stats
async function loadStats() {
    try {
        const res = await fetch(`${API_URL}/api/stats`);
        const data = await res.json();
        
        document.getElementById('total-comments').innerText = data.total_comments.toLocaleString();
        
        const total = data.stats.Positif + data.stats.Netral + data.stats.Negatif;
        if(total > 0) {
            // Animasi Bar
            setTimeout(() => {
                document.getElementById('bar-pos').style.width = `${(data.stats.Positif/total)*100}%`;
                document.getElementById('txt-pos').innerText = data.stats.Positif.toLocaleString();
                
                document.getElementById('bar-net').style.width = `${(data.stats.Netral/total)*100}%`;
                document.getElementById('txt-net').innerText = data.stats.Netral.toLocaleString();
                
                document.getElementById('bar-neg').style.width = `${(data.stats.Negatif/total)*100}%`;
                document.getElementById('txt-neg').innerText = data.stats.Negatif.toLocaleString();
            }, 500);
        }

        const rcList = document.getElementById('recent-list');
        rcList.innerHTML = '';
        data.recent_comments.forEach(c => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${c.author}</strong>: "${c.text.substring(0, 80)}..." <br/><span style="color:#818cf8; font-size:0.85rem; margin-top:5px; display:inline-block;">AI Predict: ${c.sentiment}</span>`;
            rcList.appendChild(li);
        });
    } catch (err) {
        console.error("Gagal memuat statistik", err);
        document.getElementById('total-comments').innerText = "API Offline";
    }
}

// Predict Action
document.getElementById('predict-btn').addEventListener('click', async () => {
    const text = document.getElementById('user-input').value;
    if(!text.trim()) return alert('Silakan ketikkan opini terlebih dahulu!');
    
    const btn = document.getElementById('predict-btn');
    btn.disabled = true;
    btn.classList.add('loading-state');
    btn.innerText = "Menganalisis dengan AI...";
    
    try {
        const res = await fetch(`${API_URL}/api/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        const data = await res.json();
        
        const resBox = document.getElementById('result-box');
        resBox.classList.remove('hidden', 'show');
        
        // Render Hasil
        document.getElementById('res-sentiment').innerText = data.sentiment;
        document.getElementById('res-stance').innerText = data.stance;
        
        // Warnai badge sesuai hasil
        const sentBadge = document.getElementById('res-sentiment');
        const stanceBadge = document.getElementById('res-stance');
        
        const getBadgeColor = (val) => {
            if(val.includes('Positif')) return '#4ade80';
            if(val.includes('Negatif')) return '#f87171';
            return '#facc15';
        };
        
        sentBadge.style.color = getBadgeColor(data.sentiment);
        stanceBadge.style.color = getBadgeColor(data.stance);

        // Munculkan dengan animasi
        setTimeout(() => resBox.classList.add('show'), 50);

    } catch (err) {
        alert("Gagal terhubung ke API Backend. Pastikan uvicorn berjalan.");
    } finally {
        btn.disabled = false;
        btn.classList.remove('loading-state');
        btn.innerText = "Analisis Menggunakan AI";
    }
});

// Init
window.onload = loadStats;
