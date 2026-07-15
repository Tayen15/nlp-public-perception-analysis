const API_URL = "https://tayen-nlp-public-perception-analysis.hf.space";

// Load Stats
async function loadStats() {
  try {
    const res = await fetch(`${API_URL}/api/stats`);
    const data = await res.json();

    document.getElementById("total-comments").innerText = data.total_comments.toLocaleString();
    document.getElementById("kpi-pos").innerText = data.stats.Positif.toLocaleString();
    document.getElementById("kpi-neg").innerText = data.stats.Negatif.toLocaleString();

    const total = data.stats.Positif + data.stats.Netral + data.stats.Negatif;
    if (total > 0) {
      setTimeout(() => {
        document.getElementById("bar-pos").style.width = `${(data.stats.Positif / total) * 100}%`;
        document.getElementById("txt-pos").innerText = data.stats.Positif.toLocaleString();

        document.getElementById("bar-net").style.width = `${(data.stats.Netral / total) * 100}%`;
        document.getElementById("txt-net").innerText = data.stats.Netral.toLocaleString();

        document.getElementById("bar-neg").style.width = `${(data.stats.Negatif / total) * 100}%`;
        document.getElementById("txt-neg").innerText = data.stats.Negatif.toLocaleString();
      }, 500);
    }

    const rcList = document.getElementById("recent-list");
    rcList.innerHTML = "";
    data.recent_comments.forEach((c) => {
      const tr = document.createElement("tr");
      
      let badgeClass = "b-net";
      if(c.sentiment.includes("Positif")) badgeClass = "b-pos";
      else if(c.sentiment.includes("Negatif")) badgeClass = "b-neg";

      tr.innerHTML = `
        <td style="font-weight: 500; color: var(--text-main);">${c.author}</td>
        <td style="color: var(--text-muted);">${c.text}</td>
        <td><span class="tbl-badge ${badgeClass}">${c.sentiment}</span></td>
      `;
      rcList.appendChild(tr);
    });
  } catch (err) {
    console.error("Gagal memuat statistik", err);
    document.getElementById("total-comments").innerText = "Error";
  }
}

// Predict Action
document.getElementById("predict-btn").addEventListener("click", async () => {
  const text = document.getElementById("user-input").value;
  if (!text.trim()) return alert("Silakan ketikkan opini terlebih dahulu!");

  const btn = document.getElementById("predict-btn");
  btn.disabled = true;
  btn.classList.add("loading-state");
  btn.innerHTML = `<i data-lucide="loader" class="spin"></i> Menganalisis...`;
  lucide.createIcons();

  try {
    const res = await fetch(`${API_URL}/api/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();

    const resBox = document.getElementById("result-box");
    resBox.classList.remove("hidden", "show");

    document.getElementById("res-sentiment").innerText = data.sentiment;
    document.getElementById("res-stance").innerText = data.stance;

    const sentBadge = document.getElementById("res-sentiment");
    const stanceBadge = document.getElementById("res-stance");

    const getBadgeBgColor = (val) => {
      if (val.includes("Positif")) return "var(--success)";
      if (val.includes("Negatif")) return "var(--danger)";
      return "var(--warning)";
    };

    sentBadge.style.backgroundColor = getBadgeBgColor(data.sentiment);
    sentBadge.style.color = "#ffffff";
    stanceBadge.style.backgroundColor = getBadgeBgColor(data.stance);
    stanceBadge.style.color = "#ffffff";

    setTimeout(() => resBox.classList.add("show"), 50);
  } catch (err) {
    alert("Gagal terhubung ke API Backend. Pastikan uvicorn berjalan.");
  } finally {
    btn.disabled = false;
    btn.classList.remove("loading-state");
    btn.innerHTML = `<i data-lucide="scan-text"></i> Analisis Teks`;
    lucide.createIcons();
  }
});

// Init
window.onload = loadStats;
