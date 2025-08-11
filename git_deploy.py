#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git deployment script - Terminal Unicode sorunlarini cozer
"""

# Amaç:
# - Git add/commit/tag/push adımlarını tek komutla koordine etmek
# - Windows/terminal unicode çıktılarında sorun yaşamamak için text/encoding parametreleriyle çalışmak

import subprocess
import sys
import os

def run_git_command(command):
    """Git komutunu calistir"""
    # Başarılı/başarısız durumları konsola yazdırır ve boolean döndürür
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✓ {command}")
            if result.stdout:
                print(f"  {result.stdout.strip()}")
            return True
        else:
            print(f"✗ {command}")
            if result.stderr:
                print(f"  Hata: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"✗ {command} - Exception: {e}")
        return False

def main():
    """Ana deployment fonksiyonu"""
    # Sürüm etiketleme ve ana dal push işlemlerini sıralı olarak yürütür
    print("=== Git Deployment v1.4.3 ===")
    print("LLM Provider Seçimi ve Gelişmiş AI Entegrasyonu")
    print()
    
    # Git durumunu kontrol et
    print("1. Git durumu kontrol ediliyor...")
    run_git_command("git status --porcelain")
    
    # Dosyalari ekle
    print("\n2. Dosyalar git'e ekleniyor...")
    if not run_git_command("git add -A"):
        print("Git add basarisiz!")
        return False
    
    # Commit yap
    print("\n3. Commit yapiliyor...")
    commit_message = "v1.4.3: LLM provider seçimi ve gelişmiş AI entegrasyonu"
    if not run_git_command(f'git commit -m "{commit_message}"'):
        print("Commit basarisiz! (Belki degisiklik yok)")
    
    # Tag olustur
    print("\n4. Tag olusturuluyor...")
    if not run_git_command("git tag v1.4.3"):
        print("Tag olusturma basarisiz! (Belki zaten var)")
    
    # Push yap
    print("\n5. GitHub'a push yapiliyor...")
    if run_git_command("git push origin main"):
        print("✓ Ana branch push edildi")
    else:
        print("✗ Ana branch push basarisiz")
        return False
    
    # Tag'leri push et
    print("\n6. Tag'ler push ediliyor...")
    if run_git_command("git push origin --tags"):
        print("✓ Tag'ler push edildi")
    else:
        print("✗ Tag push basarisiz")
    
    print("\n=== DEPLOYMENT TAMAMLANDI ===")
    print("v1.4.3 basariyla GitHub'a yuklendi!")
    print()
    print("Yeni ozellikler:")
    print("- Çoklu LLM provider desteği (OpenAI/Anthropic/XAI)")
    print("- Model seçim dropdown menüsü")
    print("- Gelişmiş API çağrı sistemi")
    print("- Anti-hallucination iyileştirmeleri")
    print("- Requests kütüphanesi entegrasyonu")
    print("- Prompt normalizasyon geliştirmeleri")
    print()
    print("GitHub'da yeni release olarak gorunecek!")
    
    return True

if __name__ == "__main__":
    main()

