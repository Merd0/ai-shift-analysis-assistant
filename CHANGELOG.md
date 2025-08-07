# 📋 Değişiklik Günlüğü (Changelog)

Bu dosya projenin tüm önemli değişikliklerini takip eder.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) standardına uygun
Versiyonlama: [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH)

## [Yayınlanmamış] - Geliştirme Aşamasında

### Planlanan
- Web tabanlı arayüz
- Grafik ve dashboard
- Oracle veritabanı entegrasyonu
- Email raporlama

---

## [1.1.0] - 2025-01-08 🔒 GÜVENLİK GÜNCELLEMESİ

### 🔒 Güvenlik İyileştirmeleri
- **CRITICAL**: API key'leri koddan kaldırıldı
- Kullanıcılar artık kendi API key'lerini GUI'de girecek
- API key güvenlik kontrolü eklendi
- Config dosyası güvenli hale getirildi

### ✨ Yeni Özellikler
- API key yardım linki eklendi (OpenAI platform)
- Güvenlik uyarı mesajları eklendi
- API key doğrulama sistemi

### 🔧 Teknik İyileştirmeler
- `CimentoVardiyaAI` sınıfı API key parametresi alacak şekilde güncellendi
- Config dosyasından güvenlik riski kaldırıldı
- GUI'de API key girişi zorunlu hale getirildi

### 📚 Dokümantasyon
- Güvenlik notları eklendi
- API key alma rehberi eklendi

---

## [1.0.0] - 2025-01-07 🚀 İLK KARARLI SÜRÜM

### ✨ Ana Özellikler
- **KVKK Uyumlu Veri Temizleme**: Kişisel verileri otomatik tespit ve kaldırma
- **AI Destekli Analiz**: OpenAI GPT-4o-mini ile vardiya analizi
- **Modern GUI**: Tkinter tabanlı kullanıcı dostu arayüz
- **Excel İşleme**: Otomatik Excel dosyası okuma ve analiz
- **Tarih Filtreleme**: 1/7/30/60/90/180 gün seçenekleri
- **Çoklu Export**: PDF/Excel/Word rapor seçenekleri

### 🔒 KVKK Uyumluluğu
- Kişisel veri tespit algoritması
- Otomatik kolon temizleme
- Güvenli veri saklama
- İçerik skoru hesaplama

### 🤖 AI Analiz Türleri
- Genel özet ve durum değerlendirmesi
- Sorun analizi ve kategorilendirme
- Çözüm önerileri ve eylem planları
- Trend analizi ve eğilimler
- Performans metrikleri hesaplama

### 🖥️ GUI Özellikleri
- 4 ana sekme: Dosya Analizi, Tarih Filtresi, AI Analizi, Raporlar
- Gerçek zamanlı progress gösterimi
- Hata yönetimi ve kullanıcı bildirimleri
- Responsive tasarım

### 🛠️ Teknik Özellikler
- Python 3.8+ uyumluluğu
- Pandas, OpenPyXL, NumPy entegrasyonu
- OpenAI API entegrasyonu
- Modüler kod yapısı
- Comprehensive error handling

### 📁 Proje Yapısı
```
akilli_uretim_gunlugu_asistani/
├── 📄 excel_analyzer.py      # Ana analiz motoru
├── 🖥️ vardiya_gui.py         # GUI arayüzü
├── 🤖 ai_analyzer.py         # AI analiz sistemi
├── 🎮 demo.py               # Demo scripti
├── ⚙️ config.py             # Konfigürasyon
├── 📋 requirements.txt      # Python paketleri
├── 📖 README.md            # Dokümantasyon
└── 📁 cleaned_data/        # Temizlenmiş veriler
```

### 🎯 Test Edildi
- ✅ 4,427 kayıtlık gerçek üretim verisi
- ✅ KVKK temizleme algoritması
- ✅ AI analiz doğruluğu
- ✅ GUI fonksiyonalitesi
- ✅ Export işlemleri

---

## Versiyon Notları

### Semantic Versioning Açıklaması:
- **MAJOR** (1.x.x): Uyumsuz API değişiklikleri
- **MINOR** (x.1.x): Yeni özellikler (geriye uyumlu)
- **PATCH** (x.x.1): Hata düzeltmeleri (geriye uyumlu)

### Güvenlik Seviyesi:
- 🔴 **CRITICAL**: Acil güvenlik güncellemesi
- 🟡 **SECURITY**: Güvenlik iyileştirmesi
- 🟢 **FEATURE**: Yeni özellik
- 🔵 **BUGFIX**: Hata düzeltmesi

### Yayın Döngüsü:
- **Alpha**: Geliştirme aşaması
- **Beta**: Test aşaması
- **RC**: Yayın adayı
- **Stable**: Kararlı sürüm
