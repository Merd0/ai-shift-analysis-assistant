# Akıllı Üretim Günlüğü Asistanı

**KVKK Uyumlu Vardiya Analiz Sistemi** | **v1.4.2 - Gelişmiş Kalite ve Temizlik Sistemi**

[![Version](https://img.shields.io/badge/version-1.4.2-blue.svg)](CHANGELOG.md)
[![Security](https://img.shields.io/badge/security-enhanced-green.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](requirements.txt)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Bu sistem, SoftExpert'ten alınan vardiya defteri kayıtlarını analiz edip günün özeti, sorunlar ve çözümleri gibi ana noktaları listeler. Kişisel verileri otomatik olarak temizleyerek KVKK uyumluluğu sağlar.

## v1.4.2 – Öne Çıkanlar

- **%0 placeholder sorunu çözüldü** (≈%<1 dönüşümü)
- **"Dayanak veri: N/A" temizliği güçlendirildi** → "Dayanak veri: veri yok"
- **"-soru- soru-" tekrar hatası düzeltildi** → "— Sorumlu —"
- **Excel çıktısında kapsamlı metin temizliği**
- **X/Y saat placeholder'ları** "veri yok" ile değiştirildi
- **Yönetici Aksiyon Panosu** 7-10 spesifik madde ile güçlendirildi
- **Haftalık ortalama duruş süresi** hesaplama eklendi

## v1.4.1 – Önceki Güncellemeler

- Excel export metin/format düzeltmeleri (ayraç/bullet temizliği, wrap)
- Excel'de "=" ile başlayan satırlar formül algılanmıyor (tek tırnak kaçışı)
- Dağılım yüzdeleri normalize edilerek Toplam = %100
- Süre/dağılım parse işlemleri daha dayanıklı
- API timeout/retry/offline fallback kaldırıldı
- `artifacts/` klasörlerine otomatik arşivleme

## v1.4.0 – Güvenli İş Zekası Sistemi

- **Maliyet Uydurma Önleme Sistemi** - Sadece veriye dayalı analiz
- **Güvenli Prompt Sistemi** - Halüsinasyon önleme kuralları
- **Operasyonel Etki Analizi** - Gerçekçi iş etkisi değerlendirmesi
- **Kaynak İhtiyacı Analizi** - Pratik kaynak planlaması
- **Basit ve Çalışan GUI** - Karmaşıklık azaltıldı
- **Toggle Butonları Kaldırıldı** - Daha stabil arayüz

## 🔒 **v1.1.0 Güvenlik Güncellemesi**

**CRITICAL UPDATE**: API key güvenliği artırıldı!
- ❌ **Kaldırıldı**: Kodda sabit API key'ler
- ✅ **Eklendi**: Kullanıcı bazlı API key girişi
- 🔐 **Güvenli**: Her kullanıcı kendi key'ini kullanır
- 💡 **Yardım**: API key alma rehberi eklendi

[📋 Tüm değişiklikleri gör](CHANGELOG.md)

## ✨ Özellikler

### 🔒 KVKK Uyumluluğu
- Kişisel verileri otomatik tespit ve temizleme
- İsim, telefon, TC no gibi bilgileri kaldırma
- Sadece işle ilgili verileri analiz etme

### 📊 Veri Analizi
- Excel dosyalarını otomatik okuma ve analiz
- Tarih bazlı filtreleme (1/7/30/60/90/180 gün)
- Özel tarih aralığı seçimi
- Otomatik kolon tespit sistemi

### 🤖 AI Destekli Analiz
- OpenAI GPT-4o-mini entegrasyonu
- Genel özet ve sorun analizi
- Çözüm önerileri ve trend analizi
- Performans metrikleri hesaplama

### 🖥️ Kullanıcı Dostu Arayüz
- Modern GUI arayüzü
- Sekme bazlı organizasyon
- Gerçek zamanlı progress gösterimi
- Çoklu export seçenekleri

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- Windows 10/11

### Hızlı Kurulum
```bash
# Projeyi indirin
git clone <repo-url>
cd akilli_uretim_gunlugu_asistani

# Gerekli paketleri yükleyin
pip install -r requirements.txt
```

### Manuel Kurulum
```bash
pip install pandas openpyxl numpy openai
```

## 📖 Kullanım

### 🎮 Demo ile Başlayın
```bash
python demo.py
```

Demo menüsünden seçenekleri keşfedin:
1. **Konsol Demo**: Otomatik analiz
2. **GUI Demo**: Grafik arayüz
3. **Sistem Bilgileri**: Durum kontrolü

### 🖥️ GUI Uygulaması
```bash
python vardiya_gui.py
```

**Adımlar:**
1. **Dosya Analizi**: Excel dosyası seçin ve analiz edin
2. **Tarih Filtresi**: Analiz dönemini belirleyin
3. **AI Analizi**: OpenAI API key'i girin ve analiz başlatın
4. **Raporlar**: Sonuçları PDF/Excel olarak export edin

### 📋 Konsol Analizi
```bash
python excel_analyzer.py
```

Workspace'teki tüm Excel dosyalarını otomatik analiz eder.

## 📁 Proje Yapısı

```
akilli_uretim_gunlugu_asistani/
├── 📄 excel_analyzer.py      # Ana analiz motoru
├── 🖥️ vardiya_gui.py         # GUI arayüzü
├── 🎮 demo.py               # Demo scripti
├── 📋 requirements.txt      # Python paketleri
├── 📖 README.md            # Bu dosya
├── 📊 *.xlsx               # Excel dosyaları
└── 📁 cleaned_data/        # Temizlenmiş veriler
    ├── clean_file1.xlsx
    └── clean_file2.xlsx
```

## 🔧 Konfigürasyon

### OpenAI API Ayarları
1. [OpenAI hesabı](https://platform.openai.com/) oluşturun
2. API key alın
3. GUI'de API key'i girin

<!-- Finansal tahmin içerikleri kaldırıldı -->

### Tarih Filtreleme
- **Hazır seçenekler**: 1, 7, 30, 60, 90, 180 gün
- **Özel aralık**: YYYY-MM-DD formatında
- **Tüm veriler**: Filtresiz analiz

## 📊 Veri Yapısı

### Desteklenen Formatlar
- ✅ Excel (.xlsx, .xls)
- ✅ SoftExpert export formatları
- ✅ Türkçe kolon isimleri

### Otomatik Tespit Edilen Kolonlar
- 📅 **Tarih**: Tarih, Date, Zaman, Time
- 🔒 **Kişisel**: İsim, Ad, Telefon, TC, Email
- ✅ **Güvenli**: Vardiya, Sorun, Çözüm, Makine

## 🤖 AI Analiz Türleri

### 📊 Genel Özet
- Dönem içi ana durumlar
- Sayısal göstergeler
- Genel performans değerlendirmesi

### ⚠️ Sorun Analizi
- Sık yaşanan problemler
- Sorun kategorileri
- Etki analizi

### 💡 Çözüm Önerileri
- Pratik çözüm önerileri
- Eylem planları
- Önleyici tedbirler

### 📈 Trend Analizi
- Zaman içindeki değişimler
- Mevsimsel etkiler
- Performans eğilimleri

## 🛡️ KVKK Uyumluluğu

### Otomatik Temizlenen Veriler
- 👤 İsim, soyisim
- 📞 Telefon numaraları
- 🆔 TC kimlik numaraları
- 📧 Email adresleri
- 🏠 Adres bilgileri

### Korunan Veriler
- 📅 Tarih/zaman bilgileri
- 🏭 Vardiya bilgileri
- ⚙️ Makine/ekipman verileri
- 📋 Sorun/çözüm açıklamaları
- 📊 Üretim metrikleri

## 🔍 Örnekler

### Konsol Çıktısı
```
🤖 AKILLI ÜRETİM GÜNLÜĞÜ - EXCEL ANALİZ RAPORU
============================================================

📊 GENEL ÖZET:
   • Toplam dosya: 4
   • Toplam satır: 13,244
   • KVKK nedeniyle kaldırılan kolon: 2

📁 DOSYA DETAYLARI:
   📄 vardiya_kayitlari.xlsx
      • Boyut: 177.9 KB
      • Satır: 2,070
      • Orijinal kolon: 9
      • Temiz kolon: 9
      • Tarih kolonları: Tarih, Vardiya
```

### AI Analiz Örneği
```
🤖 AI ANALİZ SONUCU
==================================================

1. GENEL ÖZET:
   • Son 30 günde 156 vardiya kaydı analiz edildi
   • Toplam 23 farklı sorun türü tespit edildi
   • Ortalama günlük 5.2 kayıt

2. SORUN ANALİZİ:
   • En sık sorun: Malzeme gecikmesi (%34)
   • İkinci sırada: Makine arızası (%28)
   • Üçüncü sırada: Personel eksikliği (%18)

3. ÇÖZÜM ÖNERİLERİ:
   • Tedarikçi alternatifi geliştirin
   • Preventif bakım planı oluşturun
   • Vardiya planlamasını optimize edin
```

## 🔧 Geliştirme

### Yeni Özellikler Ekleme
1. `excel_analyzer.py` - Veri işleme
2. `vardiya_gui.py` - Arayüz geliştirme
3. `demo.py` - Test senaryoları

### Test Etme
```bash
# Konsol testi
python excel_analyzer.py

# GUI testi
python vardiya_gui.py

# Demo testi
python demo.py
```

## 🆘 Sorun Giderme

### Sık Karşılaşılan Sorunlar

**❌ Excel dosyası okunamıyor**
- Dosya formatını kontrol edin (.xlsx, .xls)
- Dosyanın başka bir programda açık olmadığından emin olun

**❌ API hatası alıyorum**
- OpenAI API key'inin doğru olduğunu kontrol edin
- İnternet bağlantınızı kontrol edin
- API kotanızı kontrol edin

**❌ GUI açılmıyor**
- Python Tkinter yüklü olduğundan emin olun
- `python -m tkinter` ile test edin

### Loglama
Sistem otomatik olarak hataları konsola yazdırır. Detaylı debug için:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📞 Destek

Sorunlarınız için:
1. Demo'yu çalıştırıp test edin
2. Hata mesajlarını kaydedin
3. Excel dosya formatını kontrol edin

## 🎯 Gelecek Özellikler

### Planlanan Geliştirmeler
- 📱 Web tabanlı arayüz
- 📊 Grafik ve dashboard
- 🔄 Oracle veritabanı entegrasyonu
- 📧 Email raporlama
- 🤖 Gelişmiş ML modelleri

### Katkıda Bulunma
1. Fork yapın
2. Feature branch oluşturun
3. Commit yapın
4. Pull request gönderin

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

---

**🚀 Hemen başlamak için `python demo.py` komutunu çalıştırın!**
