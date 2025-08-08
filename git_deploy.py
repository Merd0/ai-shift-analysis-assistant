#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git deployment script - Terminal Unicode sorunlarini cozer
"""

import subprocess
import sys
import os

def run_git_command(command):
    """Git komutunu calistir"""
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
    print("=== Git Deployment v1.4.0 ===")
    print("AI Analiz Optimizasyonu ve Sistem Iyileştirmeleri")
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
    commit_message = "v1.4.0: AI analiz optimizasyonu ve sistem iyileştirmeleri"
    if not run_git_command(f'git commit -m "{commit_message}"'):
        print("Commit basarisiz! (Belki degisiklik yok)")
    
    # Tag olustur
    print("\n4. Tag olusturuluyor...")
    if not run_git_command("git tag v1.4.0"):
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
    print("v1.4.0 basariyla GitHub'a yuklendi!")
    print()
    print("Yeni ozellikler:")
    print("- AI maliyet uydurma onleme sistemi")
    print("- Sadece veriye dayali analiz")
    print("- Basit ve karli GUI")
    print("- Optimize edilmis prompt sistemi")
    print()
    print("GitHub'da yeni release olarak gorunecek!")
    
    return True

if __name__ == "__main__":
    main()

