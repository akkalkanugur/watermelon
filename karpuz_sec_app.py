import streamlit as st
import numpy as np
import cv2
from PIL import Image
from karpuz_sec import (
    analyze_color, analyze_shape, analyze_stem, analyze_field_spot,
    analyze_webbing, analyze_size, analyze_defects, interpret_score, CRITERIA_WEIGHTS
)

st.title("Karpuz Lezzet Tahmini Uygulaması")
st.write("Lütfen aşağıdaki fotoğrafları yükleyin:")

image1 = st.file_uploader("1- Karpuzun genel görünüşü", type=["jpg", "jpeg", "png"], key="genel1")
image2 = st.file_uploader("2- Sapının net göründüğü bölge (isteğe bağlı)", type=["jpg", "jpeg", "png"], key="sap")
image3 = st.file_uploader("3- Karpuzun ikinci genel görünüşü (isteğe bağlı)", type=["jpg", "jpeg", "png"], key="genel2")

analyze_btn = st.button("Analiz Et")

if analyze_btn:
    scores = {}
    total_score = 0
    total_weight = 0
    # 1. ve 3. fotoğrafı işle
    def pil_to_cv(img):
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    st.subheader("1. Genel Görünüş Analizi")
    if image1 is not None:
        pil_img1 = Image.open(image1).convert("RGB")
        cv_img1 = pil_to_cv(pil_img1)
        for func, name, key in [
            (analyze_color, 'Renk', 'color'),
            (analyze_shape, 'Şekil', 'shape'),
            (analyze_field_spot, 'Alan Lekesi', 'field_spot'),
            (analyze_webbing, 'Webbing', 'webbing'),
            (analyze_size, 'Boyut', 'size'),
            (analyze_defects, 'Anomali', 'defects')
        ]:
            try:
                score, desc = func(cv_img1)
                scores[key] = (score, desc)
                st.write(f"{name}: {desc} (Puan: {score:.1f})")
            except Exception as e:
                scores[key] = (None, f"Bulunamadı: {e}")
                st.write(f"{name}: Bulunamadı")
    else:
        st.warning("Genel görünüş fotoğrafı yüklenmedi.")

    # 3. fotoğraf ile ek analiz (her parametre için en yüksek skoru al)
    if image3 is not None:
        st.subheader("3. Genel Görünüş Analizi (Ek)")
        pil_img3 = Image.open(image3).convert("RGB")
        cv_img3 = pil_to_cv(pil_img3)
        for func, name, key in [
            (analyze_color, 'Renk', 'color'),
            (analyze_shape, 'Şekil', 'shape'),
            (analyze_field_spot, 'Alan Lekesi', 'field_spot'),
            (analyze_webbing, 'Webbing', 'webbing'),
            (analyze_size, 'Boyut', 'size'),
            (analyze_defects, 'Anomali', 'defects')
        ]:
            try:
                score, desc = func(cv_img3)
                prev_score, _ = scores.get(key, (None, None))
                if prev_score is None or (score is not None and score > prev_score):
                    scores[key] = (score, desc)
                st.write(f"{name} (2): {desc} (Puan: {score:.1f})")
            except Exception as e:
                st.write(f"{name} (2): Bulunamadı")

    # Sap analizi (2. fotoğraf varsa)
    if image2 is not None:
        st.subheader("Sap Analizi (2. Fotoğraf)")
        try:
            pil_img2 = Image.open(image2).convert("RGB")
            cv_img2 = pil_to_cv(pil_img2)
            score, desc = analyze_stem(cv_img2)
            scores['stem'] = (score, desc)
            st.write(f"Sap: {desc} (Puan: {score:.1f})")
        except Exception as e:
            scores['stem'] = (None, f"Bulunamadı: {e}")
            st.write("Sap: Bulunamadı")
    else:
        st.info("Sap analizi atlandı (fotoğraf yüklenmedi).")

    # Puanlama: sadece bulunan parametrelerin ağırlıklarını ve puanlarını dikkate al
    for key, (score, desc) in scores.items():
        if score is not None:
            total_score += score
            total_weight += CRITERIA_WEIGHTS[key]
    if total_weight > 0:
        normalized_score = total_score / total_weight * 100
    else:
        normalized_score = 0
    st.markdown(f"### Toplam Lezzet Puanı: {normalized_score:.1f} / 100")
    st.success(interpret_score(normalized_score)) 