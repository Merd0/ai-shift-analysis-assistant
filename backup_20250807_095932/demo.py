#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Akıllı Üretim Günlüğü Asistanı - Demo Scripti
Bu script sistemi kolay test etmek için hazırlanmıştır.
"""

import os
import sys
import subprocess
import time

def check_requirements():
    """Gerekli paketlerin yüklü olup olmadığını kontrol et"""
    required_packages = ['pandas', 'openpyxl', 'numpy', 'openai']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} yüklü")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} eksik")
    
    if missing_packages:
        print(f"\n⚠️ Eksik paketler: {', '.join(missing_packages)}")
        install = input("Eksik paketleri yüklemek istiyor musunuz? (e/h): ")
        
        if install.lower() in ['e', 'evet', 'yes', 'y']:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
                print("✅ Tüm paketler yüklendi!")
                return True
            except subprocess.CalledProcessError:
                print("❌ Paket yükleme başarısız!")
                return False
        else:
            return False
    
    return True

def run_console_demo():
    """Konsol demo'sunu çalıştır"""
    print("\n" + "="*60)
    print("🤖 KONSOL DEMO - Excel Analiz Sistemi")
    print("="*60)
    
    try:
        from excel_analyzer import ExcelAnalyzer
        
        analyzer = ExcelAnalyzer()
        results = analyzer.analyze_all_files()
        
        if results:
            summary = analyzer.generate_summary_report(results)
            print(summary)
            
            # Temizlenmiş verileri kaydet
            analyzer.save_cleaned_data(results)
            
            print(f"\n✅ Demo tamamlandı!")
            print(f"📁 Temizlenmiş veriler 'cleaned_data/' klasöründe")
        else:
            print("❌ Excel dosyası bulunamadı!")
            
    except Exception as e:
        print(f"❌ Demo hatası: {str(e)}")

def run_gui_demo():
    """GUI demo'sunu çalıştır"""
    print("\n" + "="*60)
    print("🖥️ GUI DEMO - Grafik Arayüz")
    print("="*60)
    
    try:
        from vardiya_gui import VardiyaGUI
        
        print("🚀 GUI başlatılıyor...")
        app = VardiyaGUI()
        app.run()
        
    except Exception as e:
        print(f"❌ GUI hatası: {str(e)}")
        print("🔧 Tkinter yüklü olduğundan emin olun")

def show_menu():
    """Ana menüyü göster"""
    print("\n" + "="*60)
    print("🤖 AKİLLI ÜRETİM GÜNLÜĞÜ ASİSTANI - DEMO")
    print("="*60)
    print("1. 📊 Konsol Demo (Otomatik analiz)")
    print("2. 🖥️ GUI Demo (Grafik arayüz)")
    print("3. 📋 Sistem Bilgileri")
    print("4. 🔧 Paket Kontrol")
    print("5. ❌ Çıkış")
    print("="*60)

def show_system_info():
    """Sistem bilgilerini göster"""
    print("\n" + "="*60)
    print("📋 SİSTEM BİLGİLERİ")
    print("="*60)
    
    # Python versiyonu
    print(f"🐍 Python: {sys.version}")
    
    # Excel dosyaları
    excel_files = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.xls'))]
    print(f"📁 Excel dosyası: {len(excel_files)}")
    for file in excel_files:
        size_kb = os.path.getsize(file) / 1024
        print(f"   • {file} ({size_kb:.1f} KB)")
    
    # Klasörler
    if os.path.exists('cleaned_data'):
        clean_files = len([f for f in os.listdir('cleaned_data') if f.endswith('.xlsx')])
        print(f"🧹 Temizlenmiş dosya: {clean_files}")
    
    print("="*60)

def main():
    """Ana fonksiyon"""
    print("🚀 Demo başlatılıyor...")
    time.sleep(1)
    
    # Gerekli paketleri kontrol et
    if not check_requirements():
        print("❌ Gerekli paketler eksik. Demo durduruluyor.")
        return
    
    while True:
        show_menu()
        
        try:
            choice = input("\nSeçiminizi yapın (1-5): ").strip()
            
            if choice == '1':
                run_console_demo()
            elif choice == '2':
                run_gui_demo()
            elif choice == '3':
                show_system_info()
            elif choice == '4':
                check_requirements()
            elif choice == '5':
                print("👋 Demo sonlandırılıyor...")
                break
            else:
                print("❌ Geçersiz seçim! Lütfen 1-5 arasında bir sayı girin.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Demo kullanıcı tarafından sonlandırıldı.")
            break
        except Exception as e:
            print(f"❌ Beklenmeyen hata: {str(e)}")
        
        input("\nDevam etmek için Enter'a basın...")

if __name__ == "__main__":
    main()
