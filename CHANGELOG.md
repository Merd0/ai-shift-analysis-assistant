# 📋 Değişiklik Günlüğü (Changelog)

Bu dosya projenin tüm önemli değişikliklerini takip eder.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) standardına uygun
Versiyonlama: [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH)

## [1.4.1] - 2025-08-08 - Excel Export & Analiz Tutarlılık Düzeltmeleri

### Bugfix / İyileştirme
- Excel export metni: ayraç/bullet temizleme, başlık birleştirme, wrap ve satır yüksekliği
- "=" ile başlayan satırlar formül olmaktan çıkarıldı (tek tırnak)
- Yüzde dağılımları kod tarafında normalize edilerek Toplam = %100
- Süre ve dağılım parsleme daha dayanıklı
- API timeout/retry/offline fallback kaldırıldı (shell here-doc sebebi)
- Artifacts klasör yapısı ve otomatik arşivleme

---

## [1.4.0] - 2025-01-08 - Güvenli İş Zekası Sistemi

### Güvenlik Kritik Düzeltmeler
- **CRITICAL**: AI'ın kafasından maliyet uydurması tamamen önlendi
- **Prompt Güvenlik**: Maliyet hesaplama bölümleri prompttan kaldırıldı
- **Veri Odaklı Analiz**: AI artık sadece Excel'deki verileri kullanıyor
- **Para Uydurma Yasağı**: TL, maliyet, ROI hesaplamaları yasaklandı

### Sistem İyileştirmeleri
- **GUI Basitleştirme**: Problemli toggle butonları kaldırıldı
- **Kararlı Arayüz**: Eski güvenilir ScrolledText sistemine dönüldü
- **Hata Giderme**: tkinter widget hatalarının tümü düzeltildi
- **Performans**: Daha hızlı ve kararlı çalışma

### Yeni Analiz Yaklaşımı
- **Operasyonel Etki Analizi**: Sadece gerçek duruş süreleri
- **Kaynak İhtiyacı**: Para yerine insan gücü ve teknik kaynaklar
- **Gerçekçi Öneriler**: Uygulanabilir, ölçülebilir öneriler
- **Teknik Zorluk**: Maliyet yerine uygulama zorluğu göstergesi

### Prompt Sistemi v2.2
- **Anti-Hallucination**: "Para uydurma yasak" uyarıları eklendi
- **Veri Odaklı**: Sadece Excel verilerine dayalı analiz
- **Operasyonel Odak**: Mali değil, operasyonel etki analizi
- **Güvenli Şablonlar**: Tüm maliyet bölümleri kaldırıldı

### Teknik Değişiklikler
- Prompt sistemi güvenlik güncellemesi
- GUI toggle sistemi tamamen kaldırıldı  
- Basit ve çalışan arayüz tasarımı
- Hata ayıklama ve stabilite iyileştirmeleri

---

## [1.1.0] - 2025-01-08 - Güvenlik Güncellemesi

### Güvenlik İyileştirmeleri
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

## [1.0.0] - 2025-01-07 - İlk Kararlı Sürüm

### Ana Özellikler
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
