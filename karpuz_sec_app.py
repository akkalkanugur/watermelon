import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="🍉 Karpuz Lezzet Tahmini",
    page_icon="🍉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS stilleri
st.markdown("""
<style>
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 20px;
        margin-bottom: 3rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #4ECDC4;
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .cta-button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        text-decoration: none;
        display: inline-block;
        font-weight: bold;
        font-size: 1.2rem;
        margin: 1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
    }
    .stat-item {
        text-align: center;
        padding: 1rem;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4ECDC4;
    }
    .stat-label {
        color: #666;
        font-size: 1rem;
    }
    .how-it-works {
        background: #f8f9fa;
        padding: 3rem 2rem;
        border-radius: 15px;
        margin: 2rem 0;
    }
    .step-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    .step-number {
        background: #4ECDC4;
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1 style="font-size: 3.5rem; margin-bottom: 1rem;">🍉 Karpuz Lezzet Tahmini</h1>
    <p style="font-size: 1.5rem; margin-bottom: 2rem;">Yapay Zeka Destekli Karpuz Analizi</p>
    <p style="font-size: 1.2rem; opacity: 0.9;">Fotoğrafınızı yükleyin, AI teknolojisi ile lezzet tahmini yapın!</p>
</div>
""", unsafe_allow_html=True)

# İstatistikler
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-item">
        <div class="stat-number">7</div>
        <div class="stat-label">Analiz Kriteri</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-item">
        <div class="stat-number">100%</div>
        <div class="stat-label">Ücretsiz</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-item">
        <div class="stat-number">⚡</div>
        <div class="stat-label">Anında Sonuç</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-item">
        <div class="stat-number">📱</div>
        <div class="stat-label">Mobil Uyumlu</div>
    </div>
    """, unsafe_allow_html=True)

# Özellikler
st.markdown("## 🚀 Özellikler")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🎨 Gelişmiş Renk Analizi</h3>
        <p>Yeşil tonları ve homojenlik analizi ile karpuzun olgunluk seviyesini tespit eder.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>🔵 Şekil Simetrisi</h3>
        <p>Karpuzun şekil oranlarını analiz ederek kalite değerlendirmesi yapar.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>🌿 Sap Durumu</h3>
        <p>Sapın kuruluk ve kahverengi tonlarını analiz ederek tazelik kontrolü yapar.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🟡 Alan Lekesi</h3>
        <p>Alt kısımdaki sarı/turuncu leke analizi ile olgunluk seviyesini belirler.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>🕸️ Webbing Analizi</h3>
        <p>Kahverengi ağsı izleri analiz ederek şeker içeriği tahmini yapar.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>⚠️ Anomali Tespiti</h3>
        <p>Çatlak, çürük ve diğer kusurları tespit ederek kalite kontrolü yapar.</p>
    </div>
    """, unsafe_allow_html=True)

# Nasıl Çalışır
st.markdown("## 📋 Nasıl Çalışır?")

st.markdown("""
<div class="how-it-works">
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
        <div class="step-card" style="flex: 1; min-width: 200px; margin: 0.5rem;">
            <div class="step-number">1</div>
            <h4>📸 Fotoğraf Yükleyin</h4>
            <p>Karpuzun genel görünüşünü, sapını ve farklı açılarını yükleyin</p>
        </div>
        <div class="step-card" style="flex: 1; min-width: 200px; margin: 0.5rem;">
            <div class="step-number">2</div>
            <h4>🤖 AI Analizi</h4>
            <p>Yapay zeka algoritması 7 farklı kriteri analiz eder</p>
        </div>
        <div class="step-card" style="flex: 1; min-width: 200px; margin: 0.5rem;">
            <div class="step-number">3</div>
            <h4>📊 Sonuç Alın</h4>
            <p>100 üzerinden puan ve detaylı lezzet tahmini alın</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Analiz Kriterleri
st.markdown("## 🔍 Analiz Kriterleri")

criteria_data = {
    'Kriter': ['Renk Analizi', 'Şekil Simetrisi', 'Sap Durumu', 'Alan Lekesi', 'Webbing', 'Boyut', 'Anomali'],
    'Ağırlık': [20, 15, 10, 25, 15, 5, 10],
    'Açıklama': [
        'Yeşil tonları ve homojenlik',
        'Şekil oranları ve simetri',
        'Sap kuruluk ve rengi',
        'Alt kısım sarı/turuncu leke',
        'Kahverengi ağsı izler',
        'Görsel alan oranı',
        'Çatlak ve kusur tespiti'
    ]
}

# Gauge chart ile ağırlık gösterimi
fig = go.Figure()

for i, (criterion, weight) in enumerate(zip(criteria_data['Kriter'], criteria_data['Ağırlık'])):
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=weight,
        title={'text': criterion},
        domain={'x': [i/7, (i+1)/7], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 30]},
            'bar': {'color': "#4ECDC4"},
            'steps': [
                {'range': [0, 10], 'color': "lightgray"},
                {'range': [10, 20], 'color': "yellow"},
                {'range': [20, 30], 'color': "orange"}
            ]
        }
    ))

fig.update_layout(
    height=300,
    showlegend=False,
    title="Analiz Kriterleri ve Ağırlıkları"
)

st.plotly_chart(fig, use_container_width=True)

# CTA Buton
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Analiz Yapmaya Başla", type="primary", use_container_width=True):
        st.switch_page("pages/Analiz.py")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <h3>🍉 Karpuz Lezzet Tahmini Uygulaması</h3>
    <p>Yapay Zeka Destekli Görsel Analiz Teknolojisi</p>
    <p>Bu uygulama eğitim amaçlı geliştirilmiştir. Sonuçlar tahminidir.</p>
</div>
""", unsafe_allow_html=True) 