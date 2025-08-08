#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Akıllı Üretim Günlüğü Asistanı - Versiyon Bilgileri
"""

# Semantic Versioning: MAJOR.MINOR.PATCH
VERSION = "1.4.0"
VERSION_NAME = "Güvenli İş Zekası Sistemi"
BUILD_DATE = "2025-01-08"
BUILD_NUMBER = 140

# Versiyon detayları
VERSION_INFO = {
    'major': 1,
    'minor': 4, 
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
    'data_only_analysis': True      # v1.4.0'da eklendi
}

# Değişiklik özeti
CHANGELOG_SUMMARY = {
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
    print(f"Akıllı Üretim Günlüğü Asistanı")
    print(f"Versiyon: {get_version_string()}")
    print(f"Kod Adı: {VERSION_NAME}")
    print(f"Yapım Tarihi: {BUILD_DATE}")
    print(f"Yapım Numarası: {BUILD_NUMBER}")
    print(f"Aktif Özellikler: {len([f for f in FEATURES.values() if f])}/{len(FEATURES)}")

if __name__ == "__main__":
    print_version_info()
