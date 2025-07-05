# 🍉 Karpuz Lezzet Tahmini Uygulaması

Bu uygulama, karpuz fotoğraflarını analiz ederek lezzet tahmini yapar.

## 📸 Nasıl Kullanılır?

1. **Genel Görünüş Fotoğrafı** - Karpuzun tam görünüşünü yükleyin
2. **Sap Bölgesi Fotoğrafı** (İsteğe bağlı) - Sapın net göründüğü fotoğraf
3. **İkinci Genel Görünüş** (İsteğe bağlı) - Farklı açıdan çekilmiş fotoğraf

## 🔍 Analiz Edilen Özellikler

- **Renk Analizi** - Yeşil tonları ve homojenlik
- **Şekil Analizi** - Simetri ve oran
- **Sap Durumu** - Kuruluk ve kahverengi ton
- **Alan Lekesi** - Alt kısımdaki sarı/turuncu leke
- **Webbing** - Kahverengi ağsı izler
- **Boyut** - Görsel alan oranı
- **Anomali** - Çatlak, çürük tespiti

## 🎯 Sonuç

Uygulama 100 üzerinden puan verir ve lezzet tahmini yapar:
- 85+ : Muhtemelen çok lezzetli
- 65-85 : Büyük ihtimalle lezzetli  
- 45-65 : Ortalama lezzette
- 45- : Muhtemelen tatsız

## 🚀 Deployment

Bu uygulama Streamlit Cloud'da host edilmektedir. 