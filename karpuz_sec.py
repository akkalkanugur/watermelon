import cv2
import numpy as np
from PIL import Image
import sys

# --- Kriter ağırlıkları ---
CRITERIA_WEIGHTS = {
    'color': 20,
    'shape': 15,
    'stem': 10,
    'field_spot': 25,
    'webbing': 15,
    'size': 5,
    'defects': 10
}

# --- Yardımcı fonksiyonlar ---
def load_image(path):
    """Görüntüyü yükler ve hem OpenCV hem PIL formatında döndürür."""
    cv_img = cv2.imread(path)
    pil_img = Image.open(path)
    return cv_img, pil_img

def analyze_color(cv_img):
    """Karpuzun genel renk analizini yapar."""
    hsv = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)
    # Yeşil tonları için maske
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    green_ratio = np.sum(mask > 0) / (cv_img.shape[0] * cv_img.shape[1])
    # Koyu ve homojenlik için standart sapma
    stddev = np.std(hsv[:,:,2][mask > 0])
    score = 0
    if green_ratio > 0.5 and stddev < 40:
        score = CRITERIA_WEIGHTS['color']
    elif green_ratio > 0.3:
        score = CRITERIA_WEIGHTS['color'] * 0.7
    else:
        score = CRITERIA_WEIGHTS['color'] * 0.3
    return score, f"Yeşil oranı: {green_ratio:.2f}, Homojenlik: {stddev:.1f}"

def analyze_shape(cv_img):
    """Karpuzun şekil simetrisini analiz eder."""
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7,7), 0)
    _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return 0, "Karpuz tespit edilemedi."
    c = max(contours, key=cv2.contourArea)
    ellipse = cv2.fitEllipse(c) if len(c) >= 5 else None
    if ellipse:
        (x, y), (MA, ma), angle = ellipse
        ratio = min(MA, ma) / max(MA, ma)
        if ratio > 0.85:
            score = CRITERIA_WEIGHTS['shape']
        elif ratio > 0.7:
            score = CRITERIA_WEIGHTS['shape'] * 0.7
        else:
            score = CRITERIA_WEIGHTS['shape'] * 0.3
        return score, f"Şekil oranı: {ratio:.2f}"
    return CRITERIA_WEIGHTS['shape'] * 0.3, "Eliptik oran düşük."

def analyze_stem(cv_img):
    """Sapın kuru ve kahverengi olup olmadığını analiz eder (üst kısımda arar)."""
    h, w = cv_img.shape[:2]
    stem_region = cv_img[0:int(h*0.15), int(w*0.4):int(w*0.6)]
    hsv = cv2.cvtColor(stem_region, cv2.COLOR_BGR2HSV)
    # Kahverengi tonları
    lower_brown = np.array([10, 50, 20])
    upper_brown = np.array([30, 255, 200])
    mask = cv2.inRange(hsv, lower_brown, upper_brown)
    brown_ratio = np.sum(mask > 0) / (stem_region.shape[0] * stem_region.shape[1])
    if brown_ratio > 0.15:
        score = CRITERIA_WEIGHTS['stem']
    elif brown_ratio > 0.05:
        score = CRITERIA_WEIGHTS['stem'] * 0.5
    else:
        score = 0
    return score, f"Kahverengi sap oranı: {brown_ratio:.2f}"

def analyze_field_spot(cv_img):
    """Alan lekesinin (field spot) rengini ve büyüklüğünü analiz eder (alt kısımda arar)."""
    h, w = cv_img.shape[:2]
    spot_region = cv_img[int(h*0.8):h, int(w*0.2):int(w*0.8)]
    hsv = cv2.cvtColor(spot_region, cv2.COLOR_BGR2HSV)
    # Sarı/turuncu tonları
    lower_yellow = np.array([15, 40, 80])
    upper_yellow = np.array([35, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    yellow_ratio = np.sum(mask > 0) / (spot_region.shape[0] * spot_region.shape[1])
    if yellow_ratio > 0.3:
        score = CRITERIA_WEIGHTS['field_spot']
    elif yellow_ratio > 0.1:
        score = CRITERIA_WEIGHTS['field_spot'] * 0.5
    else:
        score = 0
    return score, f"Alan leke sarı oranı: {yellow_ratio:.2f}"

def analyze_webbing(cv_img):
    """Webbing/sugar spot (kahverengi ağsı izler) analizini yapar."""
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.sum(edges > 0) / (cv_img.shape[0] * cv_img.shape[1])
    # Webbing için orta yoğunluk iyi, çok az veya çok fazla kötü
    if 0.01 < edge_density < 0.04:
        score = CRITERIA_WEIGHTS['webbing']
    elif 0.005 < edge_density < 0.06:
        score = CRITERIA_WEIGHTS['webbing'] * 0.7
    else:
        score = CRITERIA_WEIGHTS['webbing'] * 0.3
    return score, f"Webbing kenar yoğunluğu: {edge_density:.3f}"

def analyze_size(cv_img):
    """Görselden tahmini boyut (alan) analizi yapar."""
    # Karpuzun alanı, görseldeki alanına göre tahmini yapılır
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return 0, "Karpuz tespit edilemedi."
    c = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(c)
    img_area = cv_img.shape[0] * cv_img.shape[1]
    area_ratio = area / img_area
    if area_ratio > 0.3:
        score = CRITERIA_WEIGHTS['size']
    elif area_ratio > 0.15:
        score = CRITERIA_WEIGHTS['size'] * 0.7
    else:
        score = CRITERIA_WEIGHTS['size'] * 0.3
    return score, f"Karpuz alan oranı: {area_ratio:.2f}"

def analyze_defects(cv_img):
    """Çatlak, çürük veya anormal lekeleri tespit eder."""
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    # Çok koyu veya çok açık alanlar anomali olarak sayılır
    dark_pixels = np.sum(gray < 30)
    bright_pixels = np.sum(gray > 220)
    total_pixels = gray.size
    defect_ratio = (dark_pixels + bright_pixels) / total_pixels
    if defect_ratio < 0.01:
        score = CRITERIA_WEIGHTS['defects']
    elif defect_ratio < 0.03:
        score = CRITERIA_WEIGHTS['defects'] * 0.7
    else:
        score = CRITERIA_WEIGHTS['defects'] * 0.3
    return score, f"Anomali oranı: {defect_ratio:.3f}"

def interpret_score(score):
    if score > 85:
        return "Bu karpuz muhtemelen çok lezzetli!"
    elif score > 65:
        return "Bu karpuz büyük ihtimalle lezzetli."
    elif score > 45:
        return "Bu karpuz ortalama lezzette olabilir."
    else:
        return "Bu karpuz muhtemelen tatsız veya olgunlaşmamış."

def main(image_path):
    cv_img, pil_img = load_image(image_path)
    results = {}
    total_score = 0
    print("Karpuz görsel analizi başlatıldı...\n")
    for func, name in [
        (analyze_color, 'Renk'),
        (analyze_shape, 'Şekil'),
        (analyze_stem, 'Sap'),
        (analyze_field_spot, 'Alan Lekesi'),
        (analyze_webbing, 'Webbing'),
        (analyze_size, 'Boyut'),
        (analyze_defects, 'Anomali')
    ]:
        score, desc = func(cv_img)
        results[name] = (score, desc)
        total_score += score
        print(f"{name}: {desc} (Puan: {score:.1f})")
    print(f"\nToplam Lezzet Puanı: {total_score:.1f} / 100")
    print(interpret_score(total_score))

if __name__ == "__main__":
    print("1- Karpuzun genel görünüşünün fotoğrafının yolunu girin:")
    image_path1 = input("Genel görünüş: ")
    print("2- Sapının net göründüğü bölgenin fotoğrafının yolunu girin (yoksa boş bırakın):")
    image_path2 = input("Sap bölgesi: ")
    print("3- Karpuzun ikinci genel görünüşünün fotoğrafının yolunu girin:")
    image_path3 = input("İkinci genel görünüş: ")

    results = {}
    total_score = 0
    total_weight = 0

    # 1. ve 3. fotoğraflar için analiz (her parametre için en yüksek skoru al)
    print("\n--- 1. Genel Görünüş Analizi ---")
    cv_img1, _ = load_image(image_path1)
    scores1 = {}
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
            scores1[key] = (score, desc)
            print(f"{name}: {desc} (Puan: {score:.1f})")
        except Exception as e:
            scores1[key] = (None, f"Bulunamadı: {e}")
            print(f"{name}: Bulunamadı")

    # 3. fotoğraf ile ek analiz (her parametre için en yüksek skoru al)
    if image_path3.strip():
        print("\n--- 3. Genel Görünüş Analizi (Ek) ---")
        cv_img3, _ = load_image(image_path3)
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
                prev_score, _ = scores1.get(key, (None, None))
                # En yüksek skoru al
                if prev_score is None or (score is not None and score > prev_score):
                    scores1[key] = (score, desc)
                print(f"{name} (2): {desc} (Puan: {score:.1f})")
            except Exception as e:
                print(f"{name} (2): Bulunamadı")
    else:
        print("\n3. genel görünüş fotoğrafı verilmedi.")

    # Sap analizi (2. fotoğraf varsa)
    if image_path2.strip():
        print("\n--- Sap Analizi (2. Fotoğraf) ---")
        try:
            cv_img2, _ = load_image(image_path2)
            score, desc = analyze_stem(cv_img2)
            scores1['stem'] = (score, desc)
            print(f"Sap: {desc} (Puan: {score:.1f})")
        except Exception as e:
            scores1['stem'] = (None, f"Bulunamadı: {e}")
            print("Sap: Bulunamadı")
    else:
        print("\nSap analizi atlandı (fotoğraf verilmedi).")

    # Puanlama: sadece bulunan parametrelerin ağırlıklarını ve puanlarını dikkate al
    for key, (score, desc) in scores1.items():
        if score is not None:
            total_score += score
            total_weight += CRITERIA_WEIGHTS[key]
    if total_weight > 0:
        normalized_score = total_score / total_weight * 100
    else:
        normalized_score = 0
    print(f"\nToplam Lezzet Puanı: {normalized_score:.1f} / 100")
    print(interpret_score(normalized_score))

# --- Açıklamalar ---
# - Görüntüdeki aydınlatma ve kalite değişkenliği sonucu etkileyebilir.
# - Görsel analiz, tat tahmini için sınırlıdır; dokunma, ses ve ağırlık gibi fiziksel faktörler eksiktir.
# - Geliştirme için: Derin öğrenme tabanlı segmentasyon, kullanıcıdan ağırlık girişi, çoklu açıdan fotoğraf desteği eklenebilir. 