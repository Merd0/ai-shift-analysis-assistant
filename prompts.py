#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Çimento Fabrikası Vardiya Analizi için Optimize Edilmiş Prompt Şablonları
Token verimliliği ve kaliteli çıktı için tasarlanmış
"""

class CimentoPrompts:
    """Çimento fabrikası için özel prompt şablonları"""
    
    @staticmethod
    def get_system_prompt() -> str:
        """Sistem rolü için optimize edilmiş prompt"""
        return """Sen çimento fabrikası vardiya analizi uzmanısın. 

UZMANLIK ALANLARIN:
- Çimento üretim süreçleri (hammadde → klinker → çimento)
- Ekipman analizi (değirmenler, fırınlar, filtreler)
- Kalite kontrol (CSO parametreleri, kimyasal analiz)
- Arıza teşhis ve çözüm önerileri
- Üretim optimizasyonu

GÖREVIN:
Vardiya kayıtlarını analiz ederek:
✓ Sorunları kategorize etmek
✓ Çözüm önerileri sunmak  
✓ Trend analizi yapmak
✓ Yönetici raporu hazırlamak

KURALLARIN:
- Sadece verilen bilgileri kullan
- Çimento terminolojisi kullan
- Kısa ve net cümleler
- Sayısal veriler belirt
- Spekülasyon yapma"""

    @staticmethod
    def get_analysis_prompt_template() -> str:
        """Analiz için ana prompt şablonu"""
        return """
## VERİ ANALİZİ GÖREVİ

### HEDEF:
{date_range} vardiya verilerini analiz ederek çimento üretim sürecindeki:
- Sorunları tespit et
- Çözümleri değerlendir  
- İyileştirme önerileri sun

### VERİ:
{data_summary}

### ÇIKTI FORMATI:
Aşağıdaki başlıklar altında TÜRKÇE rapor hazırla:

**📊 ÜRETIM DURUMU:**
- Genel durum (Normal/Sorunlu/Kritik)
- Toplam duruş: X saat Y dakika
- Etkilenen ekipmanlar

**⚠️ SORUNLAR:**
[EKIPMAN] - [SORUN] - [SÜRE] - [ETKİ]
Örnek: ÇD2 - Aşırı ısınma - 45 dk - Üretim durdu

**✅ ÇÖZÜMLER:**
- Alınan aksiyonlar
- Etkililik durumu
- Süre bilgileri

**🎯 ÖNERİLER:**
1. Acil aksiyonlar
2. Önleyici bakım
3. Süreç iyileştirme

**📈 TREND:**
- Tekrarlanan sorunlar
- Risk faktörleri

RAPOR BAŞLA:
"""

    @staticmethod
    def get_equipment_analysis_prompt() -> str:
        """Ekipman analizi için özel prompt"""
        return """
## EKİPMAN ANALİZ RAPORU

### EKIPMAN GRUPLARI:
🔸 DEĞIRMENLER: ÇD1, ÇD2, ÇD3, ÇD4 (Ham öğütme) | ÇİM1, ÇİM2 (Çimento öğütme)
🔸 FIRINLAR: F1, F2 (Klinker üretimi)
🔸 SILOLAR: Silo 1-8 (Depolama)
🔸 YARDIMCI: Filtreler, konveyörler, bunkerlar

### SIKÇA YAŞANAN SORUNLAR:
- Aşırı ısınma → Soğutma sistemi kontrol
- Titreşim → Yatak kontrolü, balans
- Tıkanma → Temizlik, malzeme kontrolü
- Elektrik → Sigorta, motor kontrol

### ANALİZ YÖNTEMİ:
1. Hangi ekipman en çok sorun yaşıyor?
2. Sorun tipleri ve sıklığı
3. Ortalama çözüm süreleri
4. Önleyici bakım önerileri

VERİ: {equipment_data}

RAPOR:
"""

    @staticmethod
    def get_quality_analysis_prompt() -> str:
        """Kalite analizi için özel prompt"""
        return """
## KALİTE PARAMETRELERİ ANALİZİ

### CSO PARAMETRELERİ:
- CSO 1-7: Çimento kalite göstergeleri
- Normal aralıklar: CSO1(1.8-2.5), CSO2(2.8-3.5), CSO3(8-12)
- Spek dışı değerler → Üretim ayarları

### LABORATUVAR SONUÇLARI:
- Kimyasal analiz (XRF)
- Fiziksel testler
- Numune sonuçları

### DEĞERLENDİRME:
1. Spek dışı değerler var mı?
2. Trend analizi (yükseliyor/düşüyor)
3. Üretim etkisi
4. Düzeltici aksiyonlar

KALİTE VERİSİ: {quality_data}

RAPOR:
"""

    @staticmethod
    def get_manager_summary_prompt() -> str:
        """Yönetici özet raporu için prompt"""
        return """
## YÖNETİCİ ÖZET RAPORU

### HEDEF KİTLE: 
Üretim müdürü, vardiya amiri, teknik müdür

### İÇERİK:
- Kritik sorunlar (2-3 madde)
- Alınan aksiyonlar
- Öncelikli öneriler
- Maliyet etkileri

### FORMAT:
✓ Maksimum 1 sayfa
✓ Bullet points
✓ Sayısal veriler
✓ Acil aksiyonlar vurgulansın

DETAYLI ANALİZ: {detailed_analysis}

YÖNETİCİ RAPORU:
"""

    @staticmethod
    def get_trend_analysis_prompt() -> str:
        """Trend analizi için prompt"""
        return """
## TREND ANALİZİ RAPORU

### AMAÇ:
{period} dönemindeki vardiya verilerinde:
- Tekrarlanan sorunları tespit et
- Artan/azalan trendleri belirle
- Risk faktörlerini analiz et

### ANALİZ YÖNTEMİ:
1. Sorun sıklığı (günlük/haftalık)
2. Ekipman bazlı karşılaştırma
3. Vardiya bazlı analiz
4. Mevsimsel etkiler

### ÇIKTI:
- En sık yaşanan 5 sorun
- Artan trend gösteren riskler
- Önleyici aksiyon önerileri
- Maliyet etki analizi

VERİ: {trend_data}

TREND RAPORU:
"""

    @staticmethod
    def create_custom_prompt(template: str, **kwargs) -> str:
        """Özel prompt oluşturucu"""
        try:
            return template.format(**kwargs)
        except KeyError as e:
            return f"Prompt hatası: Eksik parametre {e}"

    @staticmethod
    def get_token_optimized_prompt(data_summary: str, max_length: int = 1000) -> str:
        """Token optimizasyonu için kısaltılmış prompt"""
        
        # Veri özetini kısalt
        if len(data_summary) > max_length:
            data_summary = data_summary[:max_length] + "...[veri kısaltıldı]"
        
        return f"""
VARDİYA ANALİZİ:

VERİ: {data_summary}

RAPOR (kısa format):
📊 DURUM: [Normal/Sorunlu/Kritik]
⚠️ SORUNLAR: [Ekipman-Sorun-Süre]
✅ ÇÖZÜMLER: [Alınan aksiyonlar]
🎯 ÖNERİ: [En önemli 2 öneri]
📈 TREND: [Dikkat edilecek nokta]

BAŞLA:
"""


# Test fonksiyonu
def test_prompts():
    """Prompt şablonlarını test et"""
    prompts = CimentoPrompts()
    
    print("🧪 Prompt Şablonları Test Ediliyor...")
    print("\n" + "="*50)
    
    # System prompt test
    system = prompts.get_system_prompt()
    print("📋 SYSTEM PROMPT:")
    print(system[:200] + "...")
    
    # Analysis prompt test
    analysis = prompts.get_analysis_prompt_template()
    print("\n📊 ANALYSIS PROMPT:")
    print(analysis[:300] + "...")
    
    # Token optimized test
    sample_data = "Çimento üretiminde ÇD2 değirmeninde aşırı ısınma sorunu yaşandı." * 50
    optimized = prompts.get_token_optimized_prompt(sample_data, max_length=200)
    print("\n⚡ TOKEN OPTİMİZED PROMPT:")
    print(optimized)
    
    print("\n✅ Tüm prompt şablonları test edildi!")


if __name__ == "__main__":
    test_prompts()
