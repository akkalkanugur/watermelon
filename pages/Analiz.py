import streamlit as st
import numpy as np
import cv2
from PIL import Image
import plotly.graph_objects as go
from karpuz_sec import (
    analyze_color, analyze_shape, analyze_stem, analyze_field_spot,
    analyze_webbing, analyze_size, analyze_defects, interpret_score, CRITERIA_WEIGHTS
)

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="🍉 Karpuz Analizi",
    page_icon="🍉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stilleri
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .upload-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #4ECDC4;
    }
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .score-high { color: #28a745; font-weight: bold; }
    .score-medium { color: #ffc107; font-weight: bold; }
    .score-low { color: #dc3545; font-weight: bold; }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .back-button {
        background: #6c757d;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        text-decoration: none;
        display: inline-block;
        margin-bottom: 1rem;
    }
    .back-button:hover {
        background: #5a6268;
        color: white;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

# Geri dönüş butonu
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.page_link("karpuz_sec_app.py", label="← Ana Sayfaya Dön", use_container_width=True)

# Ana başlık
st.markdown("""
<div class="main-header">
    <h1>🍉 Karpuz Lezzet Analizi</h1>
    <p>Fotoğraflarınızı yükleyin ve AI teknolojisi ile lezzet tahmini yapın!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📸 Fotoğraf Yükleme")
    st.markdown("Lütfen aşağıdaki fotoğrafları yükleyin:")
    
    image1 = st.file_uploader(
        "1️⃣ Karpuzun genel görünüşü", 
        type=["jpg", "jpeg", "png"], 
        key="genel1",
        help="Karpuzun tam görünüşünü içeren fotoğraf"
    )
    
    image2 = st.file_uploader(
        "2️⃣ Sapının net göründüğü bölge (isteğe bağlı)", 
        type=["jpg", "jpeg", "png"], 
        key="sap",
        help="Sapın net göründüğü yakın çekim fotoğraf"
    )
    
    image3 = st.file_uploader(
        "3️⃣ Karpuzun ikinci genel görünüşü (isteğe bağlı)", 
        type=["jpg", "jpeg", "png"], 
        key="genel2",
        help="Farklı açıdan çekilmiş genel görünüş"
    )
    
    analyze_btn = st.button("🚀 Analiz Et", type="primary", use_container_width=True)
    
    if analyze_btn and not image1:
        st.error("❌ Lütfen en az bir genel görünüş fotoğrafı yükleyin!")

# Ana içerik
if analyze_btn and image1:
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    scores = {}
    total_score = 0
    total_weight = 0
    
    def pil_to_cv(img):
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # 1. Genel Görünüş Analizi
    status_text.text("🔍 1. Genel görünüş analizi yapılıyor...")
    progress_bar.progress(20)
    
    if image1 is not None:
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("### 📸 Yüklenen Fotoğraflar")
            pil_img1 = Image.open(image1).convert("RGB")
            st.image(pil_img1, caption="Genel Görünüş", use_column_width=True)
            
            if image2:
                pil_img2 = Image.open(image2).convert("RGB")
                st.image(pil_img2, caption="Sap Bölgesi", use_column_width=True)
            
            if image3:
                pil_img3 = Image.open(image3).convert("RGB")
                st.image(pil_img3, caption="İkinci Görünüş", use_column_width=True)

        with col2:
            st.markdown("### 📊 Analiz Sonuçları")
            
            cv_img1 = pil_to_cv(pil_img1)
            
            # Metrikler için container
            metrics_container = st.container()
            
            with metrics_container:
                for func, name, key in [
                    (analyze_color, '🎨 Renk Analizi', 'color'),
                    (analyze_shape, '🔵 Şekil Analizi', 'shape'),
                    (analyze_field_spot, '🟡 Alan Lekesi', 'field_spot'),
                    (analyze_webbing, '🕸️ Webbing', 'webbing'),
                    (analyze_size, '📏 Boyut', 'size'),
                    (analyze_defects, '⚠️ Anomali', 'defects')
                ]:
                    try:
                        score, desc = func(cv_img1)
                        scores[key] = (score, desc)
                        
                        # Metrik kartı
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4>{name}</h4>
                            <p>{desc}</p>
                            <strong>Puan: {score:.1f}</strong>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    except Exception as e:
                        scores[key] = (None, f"Bulunamadı: {e}")
                        st.error(f"{name}: Bulunamadı")
            
            progress_bar.progress(50)
            status_text.text("🔄 3. görünüş analizi yapılıyor...")
            
            # 3. fotoğraf ile ek analiz
            if image3 is not None:
                cv_img3 = pil_to_cv(pil_img3)
                for func, name, key in [
                    (analyze_color, '🎨 Renk Analizi (2)', 'color'),
                    (analyze_shape, '🔵 Şekil Analizi (2)', 'shape'),
                    (analyze_field_spot, '🟡 Alan Lekesi (2)', 'field_spot'),
                    (analyze_webbing, '🕸️ Webbing (2)', 'webbing'),
                    (analyze_size, '📏 Boyut (2)', 'size'),
                    (analyze_defects, '⚠️ Anomali (2)', 'defects')
                ]:
                    try:
                        score, desc = func(cv_img3)
                        prev_score, _ = scores.get(key, (None, None))
                        if prev_score is None or (score is not None and score > prev_score):
                            scores[key] = (score, desc)
                        st.info(f"{name}: {desc} (Puan: {score:.1f})")
                    except Exception as e:
                        st.warning(f"{name}: Bulunamadı")
            
            progress_bar.progress(75)
            status_text.text("🌿 Sap analizi yapılıyor...")
            
            # Sap analizi
            if image2 is not None:
                try:
                    pil_img2 = Image.open(image2).convert("RGB")
                    cv_img2 = pil_to_cv(pil_img2)
                    score, desc = analyze_stem(cv_img2)
                    scores['stem'] = (score, desc)
                    st.success(f"🌿 Sap Analizi: {desc} (Puan: {score:.1f})")
                except Exception as e:
                    scores['stem'] = (None, f"Bulunamadı: {e}")
                    st.error("🌿 Sap: Bulunamadı")
            else:
                st.info("🌿 Sap analizi atlandı (fotoğraf yüklenmedi)")
            
            progress_bar.progress(90)
            status_text.text("📊 Sonuçlar hesaplanıyor...")
            
            # Puanlama
            for key, (score, desc) in scores.items():
                if score is not None:
                    total_score += score
                    total_weight += CRITERIA_WEIGHTS[key]
            
            if total_weight > 0:
                normalized_score = total_score / total_weight * 100
            else:
                normalized_score = 0
            
            progress_bar.progress(100)
            status_text.text("✅ Analiz tamamlandı!")
            
            # Sonuç kartı
            st.markdown("### 🎯 Final Sonuç")
            
            # Puan grafiği
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = normalized_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Lezzet Puanı"},
                delta = {'reference': 50},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 45], 'color': "lightgray"},
                        {'range': [45, 65], 'color': "yellow"},
                        {'range': [65, 85], 'color': "orange"},
                        {'range': [85, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))

            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

            # Sonuç metni
            result_text = interpret_score(normalized_score)
            if normalized_score > 85:
                st.success(f"## 🎉 {result_text}")
            elif normalized_score > 65:
                st.info(f"## 👍 {result_text}")
            elif normalized_score > 45:
                st.warning(f"## 🤔 {result_text}")
            else:
                st.error(f"## 😞 {result_text}")
            
            st.markdown(f"""
            <div class="result-card">
                <h3>📊 Detaylı Puanlama</h3>
                <p><strong>Toplam Puan:</strong> <span class="score-{'high' if normalized_score > 85 else 'medium' if normalized_score > 65 else 'low'}">{normalized_score:.1f}/100</span></p>
                <p><strong>Değerlendirme:</strong> {result_text}</p>
            </div>
            """, unsafe_allow_html=True)
        
    else:
        st.warning("❌ Genel görünüş fotoğrafı yüklenmedi.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🍉 Karpuz Lezzet Tahmini Uygulaması | Yapay Zeka Destekli Analiz</p>
    <p>Bu uygulama görsel analiz ile karpuz lezzetini tahmin etmeye çalışır.</p>
</div>
""", unsafe_allow_html=True) 