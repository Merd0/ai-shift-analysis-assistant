#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Akıllı Üretim Günlüğü Asistanı - Versiyon Bilgileri
"""

# Bu dosyanın amacı:
# - Semantik versiyon bilgilerini ve özellik bayraklarını merkezi olarak tutmak
# - GUI ve CLI'da gösterilecek özet/veri sağlayıcı yardımcı fonksiyonlar sunmak

# Semantic Versioning: MAJOR.MINOR.PATCH
VERSION = "1.5.2"
VERSION_NAME = "Gelişmiş Analiz Optimizasyonları"
BUILD_DATE = "2025-01-12"
BUILD_NUMBER = 151

# Versiyon detayları
VERSION_INFO = {
    'major': 1,
    'minor': 5, 
    'patch': 0,
    'pre_release': None,  # alpha, beta, rc
    'build': BUILD_NUMBER
}

# Özellik bayrakları
FEATURES = {
    'kvkk_compliance': True,
    'ai_analysis': True,
    'gui_interface': True,
    'excel_processing': True,
    'pdf_export': True,           # v1.2.0'da eklendi
    'date_filtering': True,
    'multi_export': True,
    'security_enhanced': True,
    'api_key_protection': True,
    'business_intelligence': True,  # v1.2.0'da eklendi
    'advanced_reporting': True,     # v1.2.0'da eklendi
    'smart_recommendations': True,  # v1.2.0'da eklendi
    'cost_impact_analysis': False,  # v1.4.0'da kaldırıldı (güvenlik)
    'trend_prediction': True,       # v1.2.0'da eklendi
    'secure_prompt_system': True,   # v1.4.0'da eklendi
    'no_cost_hallucination': True,  # v1.4.0'da eklendi
    'data_only_analysis': True,     # v1.4.0'da eklendi
    'multi_ai_provider': True,      # v1.4.3'te eklendi
    'dynamic_model_selection': True, # v1.4.3'te eklendi
    'enhanced_documentation': True,  # v1.4.3'te eklendi
    'token_usage_tracking': True,    # v1.4.3'te eklendi
    'context_limit_management': True, # v1.4.3'te eklendi
    'security_audit_logging': True,   # v1.5.0'da eklendi
    'file_security_validation': True, # v1.5.0'da eklendi
    'secure_file_processing': True,   # v1.5.0'da eklendi
    'comprehensive_audit_trail': True, # v1.5.0'da eklendi
    'session_tracking': True,         # v1.5.0'da eklendi
    'malware_protection': True,       # v1.5.0'da eklendi
    'path_traversal_protection': True, # v1.5.0'da eklendi
    'file_integrity_validation': True # v1.5.0'da eklendi
}

# Değişiklik özeti
CHANGELOG_SUMMARY = {
    '1.5.1': {
        'date': '2025-01-12',
        'type': 'enhancement',
        'title': 'Gelişmiş Analiz Optimizasyonları',
        'highlights': [
            'Advanced Yüzdelik Analiz Sistemi - Pareto 80/20 kuralı',
            'Anti-hallucination sistemi güçlendirildi',
            'Similasyon placeholder sorunu çözüldü',
            'GPT-4-turbo modeli kaldırıldı (token/maliyet optimizasyonu)',
            'Maliyet uyarı dialog sistemi eklendi',
            'Enhanced Prompt System tam entegrasyonu',
            'Zorunlu %100 yüzdelik normalize sistemi',
            'Minimum %5 kategori kuralı uygulandı',
            'Proactive analysis template\'leri iyileştirildi',
            'Sanitization engine placeholder temizliği eklendi'
        ]
    },
    '1.5.0': {
        'date': '2025-01-12',
        'type': 'security',
        'title': 'Gelişmiş Güvenlik ve Audit Sistemi',
        'highlights': [
            'Kapsamlı Security Audit Logging sistemi eklendi',
            'Dosya güvenlik validation ve malware koruması',
            'Path traversal ve file injection saldırı koruması',
            'Magic number file signature doğrulaması',
            'Session tracking ve kullanıcı aktivite izleme',
            'JSON formatında yapılandırılmış audit log\'ları',
            'Otomatik log rotasyonu ve güvenli saklama',
            'File integrity validation ve boyut kontrolleri',
            'Comprehensive security event monitoring',
            'Güvenli dosya işleme altyapısı'
        ]
    },
    '1.4.3': {
        'date': '2025-01-08',
        'type': 'enhancement',
        'title': 'Gelişmiş AI Sağlayıcı Sistemi ve Kod Kalitesi',
        'highlights': [
            'Çoklu AI Sağlayıcı Desteği (OpenAI, Anthropic Claude, xAI Grok)',
            'Dinamik model seçimi ve provider switching sistemi',
            'Kapsamlı kod dokümantasyonu ve yorum satırları eklendi',
            'AI analiz kalitesi artırma sistemleri (anti-hallucination)',
            'Gelişmiş prompt engineering ve kısıt sistemleri',
            'Provider-specific API parametre optimizasyonu',
            'Token usage tracking ve context limit yönetimi',
            'Sağlayıcı bazlı model listesi ve validasyon',
            'Base URL konfigürasyonu (xAI için özel endpoint)',
        ]
    },
    '1.4.2': {
        'date': '2025-01-08',
        'type': 'quality',
        'title': 'Gelişmiş Kalite ve Temizlik Sistemi',
        'highlights': [
            '%0 placeholder sorunu çözüldü (≈%<1 dönüşümü)',
            'Dayanak veri: N/A temizliği güçlendirildi',
            '-soru- tekrar hatası düzeltildi (— Sorumlu — formatı)',
            'Excel çıktısında kapsamlı metin temizliği',
            'X/Y saat placeholder\'ları "veri yok" ile değiştirildi',
            'Yönetici Aksiyon Panosu 7-10 madde ile güçlendirildi',
            'Haftalık ortalama duruş süresi hesaplama eklendi',
            'Prompt sistem kuralları netleştirildi'
        ]
    },
    '1.4.1': {
        'date': '2025-08-08',
        'type': 'bugfix',
        'title': 'Excel Export & Analiz Tutarlılık Düzeltmeleri',
        'highlights': [
            'Excel export metin bozulması düzeltildi (ayraç/bullet temizliği, wrap)',
            'Excel’de "=" başlı satırlar formül olarak algılanmıyor (tek tırnak kaçışı)',
            'Dağılım yüzdeleri normalize edilip %100’e tamamlanıyor',
            'Süre/dağılım parse işlemleri daha dayanıklı',
            'API timeout/retry/offline fallback geri alındı (gerçek neden shell here-doc idi)',
            'Artifacts dizinlerine otomatik arşivleme'
        ]
    },
    '1.4.0': {
        'date': '2025-01-08',
        'type': 'security',
        'title': 'Güvenli İş Zekası Sistemi',
        'highlights': [
            'Maliyet Uydurma Önleme Sistemi',
            'Sadece Veriye Dayalı Analiz',
            'Güvenli Prompt Sistemi',
            'Basit ve Çalışan GUI',
            'Toggle Butonları Kaldırıldı',
            'Operasyonel Etki Analizi',
            'Kaynak İhtiyacı Analizi',
            'Gerçekçi Öneriler Sistemi'
        ]
    },
    '1.2.0': {
        'date': '2025-01-08',
        'type': 'feature',
        'title': 'İş Zekası Rapor Sistemi',
        'highlights': [
            'Gelişmiş AI Prompt Sistemi (v2.1)',
            'Yönetici Odaklı Stratejik Raporlama',
            'PDF Export Özelliği',
            'Kök Neden Analizi',
            'Zaman Trendleri ve Risk Tahmini',
            'Maliyet Etkisi Analizi',
            'SMART Eylem Planı',
            'Yönetici Aksiyon Panosu'
        ]
    },
    '1.1.0': {
        'date': '2025-01-08',
        'type': 'security',
        'title': 'Güvenlik Güncellemesi',
        'highlights': [
            'API key\'leri koddan kaldırıldı',
            'Kullanıcı bazlı API key girişi',
            'Güvenlik kontrolü eklendi',
            'Config dosyası güvenli hale getirildi'
        ]
    },
    '1.0.0': {
        'date': '2025-01-07',
        'type': 'major',
        'title': 'İlk Kararlı Sürüm',
        'highlights': [
            'KVKK uyumlu veri temizleme',
            'AI destekli analiz sistemi',
            'Modern GUI arayüzü',
            'Excel işleme ve export'
        ]
    }
}

def get_version_string():
    """Tam versiyon string'ini döndür"""
    # Örnek: 1.4.2 (Build 142) veya 1.4.2-rc.142
    if VERSION_INFO['pre_release']:
        return f"{VERSION}-{VERSION_INFO['pre_release']}.{VERSION_INFO['build']}"
    return f"{VERSION} (Build {VERSION_INFO['build']})"

def get_version_info():
    """Versiyon bilgilerini döndür"""
    return {
        'version': VERSION,
        'version_name': VERSION_NAME,
        'build_date': BUILD_DATE,
        'build_number': BUILD_NUMBER,
        'full_version': get_version_string(),
        'features': FEATURES
    }

def print_version_info():
    """Versiyon bilgilerini konsola yazdır"""
    # CLI çıktısı: paket/uygulama bilgisini hızlıca gözlemlemek için
    print(f"Akıllı Üretim Günlüğü Asistanı")
    print(f"Versiyon: {get_version_string()}")
    print(f"Kod Adı: {VERSION_NAME}")
    print(f"Yapım Tarihi: {BUILD_DATE}")
    print(f"Yapım Numarası: {BUILD_NUMBER}")
    print(f"Aktif Özellikler: {len([f for f in FEATURES.values() if f])}/{len(FEATURES)}")

if __name__ == "__main__":
    print_version_info()
