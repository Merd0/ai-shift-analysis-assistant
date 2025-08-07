#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Akıllı Üretim Günlüğü Asistanı - Versiyon Bilgileri
"""

# Semantic Versioning: MAJOR.MINOR.PATCH
VERSION = "1.1.0"
VERSION_NAME = "Güvenlik Güncellemesi"
BUILD_DATE = "2025-01-08"
BUILD_NUMBER = 110

# Versiyon detayları
VERSION_INFO = {
    'major': 1,
    'minor': 1, 
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
    'date_filtering': True,
    'multi_export': True,
    'security_enhanced': True,  # v1.1.0'da eklendi
    'api_key_protection': True,  # v1.1.0'da eklendi
}

# Değişiklik özeti
CHANGELOG_SUMMARY = {
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
    print(f"🤖 Akıllı Üretim Günlüğü Asistanı")
    print(f"📦 Versiyon: {get_version_string()}")
    print(f"🏷️ Kod Adı: {VERSION_NAME}")
    print(f"📅 Yapım Tarihi: {BUILD_DATE}")
    print(f"🔧 Yapım Numarası: {BUILD_NUMBER}")
    print(f"✨ Aktif Özellikler: {len([f for f in FEATURES.values() if f])}/{len(FEATURES)}")

if __name__ == "__main__":
    print_version_info()
