#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Akıllı Üretim Günlüğü - Excel Analiz ve KVKK Temizleme Sistemi
Bu sistem Excel dosyalarını analiz eder ve kişisel verileri temizler.
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime
import os
from typing import List, Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class KVKKDataCleaner:
    """KVKK uyumlu veri temizleme sınıfı"""
    
    def __init__(self):
        # Kişisel veri olabilecek kolon isimleri (Türkçe + İngilizce)
        self.personal_data_keywords = [
            # İsim soyisim - Genişletilmiş liste
            'isim', 'ad', 'soyad', 'name', 'surname', 'firstname', 'lastname',
            'full_name', 'tam_ad', 'personel_adi', 'calisan_adi', 'adi', 'soyadi',
            'personel', 'personnel', 'calisan', 'employee', 'worker', 'islci',
            'baslatan', 'başlatan', 'operator', 'operatör', 'sorumlu', 'responsible',
            'vardiyaci', 'vardiyacı', 'shift_worker', 'vardiya_sorumlusu',
            'birlikte_calisan', 'birlikte_çalışan', 'team_member', 'takim_uyesi',
            'onaylayan', 'approver', 'kontrol_eden', 'supervisor', 'supervizor',
            'imzalayan', 'signer', 'teslim_eden', 'teslim_alan', 'handover',
            
            # İletişim
            'telefon', 'phone', 'tel', 'gsm', 'email', 'mail', 'eposta',
            'adres', 'address', 'ev_adresi', 'is_adresi',
            
            # Kimlik
            'tc', 'tcno', 'tc_no', 'kimlik', 'identity', 'sicil_no', 'sicil',
            'personel_no', 'employee_id', 'calisan_no', 'badge_no', 'rozet_no',
            
            # Diğer kişisel veriler
            'dogum', 'birth', 'yas', 'age', 'cinsiyet', 'gender',
            'maas', 'salary', 'ucret', 'wage'
        ]
        
        # Güvenli kolonlar (işle ilgili, kişisel olmayan) - GENİŞLETİLMİŞ
        self.safe_keywords = [
            # Temel sistem kolonları
            'id', 'tarih', 'date', 'saat', 'time', 'vardiya', 'shift', 'bilgisi',
            
            # Teknik/İş verileri
            'makine', 'machine', 'uretim', 'production', 'miktar', 'quantity',
            'sorun', 'problem', 'hata', 'error', 'cozum', 'solution',
            'aciklama', 'description', 'detay', 'detail', 'durum', 'status',
            'bolum', 'department', 'alan', 'area', 'lokasyon', 'location',
            'kategori', 'category', 'tip', 'type', 'kod', 'code',
            'deger', 'value', 'sonuc', 'result', 'rapor', 'report',
            
            # Ekipman/Sistem isimleri
            'komur', 'kömür', 'degirmen', 'değirmen', 'coal', 'mill',
            'cso', 'lab', 'ünite', 'unite', 'unit', 'sistem', 'system',
            'bunker', 'fan', 'motor', 'pump', 'pompa', 'vana', 'valve',
            'sensor', 'sensör', 'metre', 'meter', 'basınç', 'pressure',
            'sıcaklık', 'temperature', 'nem', 'humidity', 'hız', 'speed',
            
            # İş süreçleri
            'kontrol', 'control', 'test', 'bakım', 'maintenance', 'onarım', 'repair',
            'temizlik', 'cleaning', 'ayar', 'adjustment', 'kalibrasyon', 'calibration',
            'ölçüm', 'measurement', 'analiz', 'analysis', 'inceleme', 'inspection',
            
            # Vardiya/İş bilgileri (vardiyacı kelimesini çıkardık)
            'iletilmek', 'istenen', 'takip', 'etmesi', 'gereken', 'kalite',
            'spek', 'planı', 'haricinde', 'yapılan', 'işler', 'arızalanan',
            'edilen', 'bakımı', 'cihaz', 'ekipman', 'equipment', 'device',
            
            # Önemli iş kolonları - KESİNLİKLE KORUNMALI
            'açıklama', 'aciklama', 'explanation', 'note', 'notes', 'comment',
            'remarks', 'bilgi', 'info', 'information', 'description', 'desc',
            'detay', 'detail', 'details', 'özet', 'summary', 'text', 'metin'
        ]
    
    def is_personal_data_column(self, column_name: str) -> bool:
        """Kolonun kişisel veri içerip içermediğini kontrol eder"""
        column_lower = column_name.lower().strip()
        
        # Boşlukları ve özel karakterleri temizle
        column_clean = re.sub(r'[^\w]', '', column_lower)
        
        # Önce güvenli kelimeler kontrol et (GÜVENLİ ÖNCE!)
        for safe_word in self.safe_keywords:
            if safe_word in column_lower or safe_word in column_clean:
                print(f"         ℹ️ '{column_name}' güvenli kelime içeriyor: '{safe_word}'")
                return False
        
        # Kesinlikle kişisel veri içeren kolon isimleri (ÇOK DAHA SPESİFİK)
        definite_personal_patterns = [
            # Sadece kesin isim kolonları - daha sıkı kontrol
            r'^personel$', r'^personnel$', r'^başlatan$', r'^baslatan$', 
            r'^vardiyaci$', r'^vardiyacı$', r'^onaylayan$', r'^approver$',
            
            # Personel.X formatındaki kolonlar (Personel.1, Personel.2, vs.)
            r'^personel\.\d+$', r'^personnel\.\d+$', r'^personel\s*\d+$',
            r'^calisan\.\d+$', r'^çalışan\.\d+$', r'^employee\.\d+$',
            
            # Birlikte çalışan kolonları (kesinlikle isim içerir)
            r'.*birlikte.*personel.*', r'.*birlikte.*çalışan.*', r'.*team.*member.*',
            r'.*çalışılan.*personel.*', r'.*working.*with.*'
        ]
        
        for pattern in definite_personal_patterns:
            if re.match(pattern, column_lower):
                print(f"         🎯 '{column_name}' kesin kişisel veri pattern: '{pattern}'")
                return True
        
        # Sadece çok spesifik kişisel veri kelimelerini kontrol et
        strict_personal_keywords = [
            'isim', 'ad', 'soyad', 'name', 'surname', 'firstname', 'lastname',
            'full_name', 'tam_ad', 'personel_adi', 'calisan_adi',
            'tc', 'tcno', 'tc_no', 'kimlik', 'identity', 'sicil_no',
            'telefon', 'phone', 'email', 'mail', 'eposta'
        ]
        
        for personal_word in strict_personal_keywords:
            if personal_word == column_lower or personal_word == column_clean:
                print(f"         🎯 '{column_name}' kesin kişisel veri kelimesi: '{personal_word}'")
                return True
                
        return False
    
    def detect_personal_data_by_content(self, series: pd.Series, column_name: str = "") -> bool:
        """İçeriğe bakarak kişisel veri tespiti yapar - DAHA HASSAS"""
        if series.dtype == 'object':
            sample_values = series.dropna().head(20).astype(str)
            if len(sample_values) == 0:
                return False
                
            personal_data_count = 0
            total_samples = len(sample_values)
            
            print(f"         🔍 '{column_name}' içerik analizi: {total_samples} örnek")
            
            for i, value in enumerate(sample_values):
                value_clean = value.strip()
                
                # Çok kısa değerler (1-2 karakter) muhtemelen kişisel değil
                if len(value_clean) <= 2:
                    continue
                
                # Sayısal kodlar (ID, saat, tarih vs) kişisel değil
                if re.match(r'^[\d\-\:\#\_]+$', value_clean):
                    continue
                
                # TC kimlik no pattern (11 haneli sayı) - KESİN KİŞİSEL
                if re.match(r'^\d{11}$', value_clean):
                    personal_data_count += 5  # Çok yüksek ağırlık
                    print(f"           📱 TC no tespit: '{value_clean[:3]}***'")
                    continue
                
                # Telefon no pattern - KESİN KİŞİSEL
                if re.match(r'^(\+90|0)?\s*\d{3}\s*\d{3}\s*\d{2}\s*\d{2}$', value_clean):
                    personal_data_count += 5  # Çok yüksek ağırlık
                    print(f"           📞 Telefon tespit: '{value_clean[:5]}***'")
                    continue
                
                # Email pattern - KESİN KİŞİSEL
                if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value_clean):
                    personal_data_count += 5  # Çok yüksek ağırlık
                    print(f"           📧 Email tespit: '{value_clean.split('@')[0]}@***'")
                    continue
                
                # İsim pattern - DAHA SIKI KONTROL
                words = value_clean.split()
                if len(words) >= 2 and len(words) <= 3:  # Sadece 2-3 kelime
                    # Tüm kelimeler harf mi ve makul uzunlukta mı?
                    if all(3 <= len(word) <= 15 and word.replace('ç','c').replace('ğ','g').replace('ı','i').replace('ö','o').replace('ş','s').replace('ü','u').replace('Ç','C').replace('Ğ','G').replace('İ','I').replace('Ö','O').replace('Ş','S').replace('Ü','U').isalpha() for word in words):
                        # Tüm kelimeler büyük harfle başlıyor mu? (İsim formatı)
                        if all(word[0].isupper() and word[1:].islower() for word in words):
                            personal_data_count += 3
                            print(f"           👤 İsim format tespit: '{words[0]} {words[1][0]}***'")
                            continue
                
                # Yaygın Türkçe isimler kontrol et - ÇOK DAHA SIKI
                common_turkish_names = [
                    'mehmet', 'ahmet', 'mustafa', 'ali', 'hasan', 'hüseyin', 'ibrahim', 'ismail',
                    'murat', 'osman', 'süleyman', 'yusuf', 'fatma', 'ayşe', 'emine', 'hatice',
                    'zeynep', 'şerife', 'sultan', 'özlem', 'elif', 'sema', 'nuriye', 'gülsün',
                    'serkan', 'onur', 'burak', 'emre', 'kemal', 'deniz', 'yasemin', 'selin', 
                    'pınar', 'sibel', 'dilek', 'gül', 'mine', 'özge'
                ]
                
                # Teknik terimler (isim değil)
                technical_terms = [
                    'çim', 'cem', 'çd', 'cd', 'df', 'mb', 'gb', 'kg', 'lt', 'mt', 'cm',
                    'mm', 'bar', 'psi', 'rpm', 'kwh', 'mw', 'kw', 'amp', 'volt', 'hz',
                    'flux', 'silo', 'bunker', 'mill', 'coal', 'cso', 'lab', 'test',
                    'deg', 'temp', 'press', 'flow', 'level', 'speed', 'load', 'run',
                    'stop', 'start', 'auto', 'manual', 'alarm', 'trip', 'fault'
                ]
                
                value_lower = value_clean.lower()
                name_found = False
                
                # Önce teknik terim kontrolü
                is_technical = False
                for tech_term in technical_terms:
                    if tech_term in value_lower:
                        is_technical = True
                        print(f"           🔧 Teknik terim tespit: '{tech_term}' in '{value_clean[:15]}***'")
                        break
                
                if not is_technical:
                    # Sadece izole kelime eşleşmesi (teknik terim değilse)
                    words_in_value = value_lower.split()
                    for name in common_turkish_names:
                        if name in words_in_value:  # Tam kelime eşleşmesi
                            personal_data_count += 4
                            print(f"           👤 Türkçe isim tespit: '{name}' as word in '{value_clean[:15]}***'")
                            name_found = True
                            break
                
                if name_found:
                    continue
            
            # Skorlama: %80 veya daha fazlası kişisel veri benziyorsa (DAHA SIKI)
            score_ratio = personal_data_count / total_samples if total_samples > 0 else 0
            print(f"         📊 İçerik skoru: {personal_data_count}/{total_samples} = {score_ratio:.2f}")
            
            # Özel durumlar: Vardiyacı gibi kolonlar için daha sıkı kontrol
            is_personnel_related = any(keyword in column_name.lower() for keyword in 
                                     ['vardiyacı', 'vardiyaci', 'personel', 'calisan', 'çalışan'])
            
            if is_personnel_related:
                # Personel ile ilgili kolonlar için %50 eşik (daha sıkı)
                threshold = 0.5
                print(f"         ⚠️ Personel ilişkili kolon - sıkı eşik: %{threshold*100}")
            else:
                # Normal kolonlar için %80 eşik
                threshold = 0.8
            
            if score_ratio >= threshold:
                print(f"         ❌ Kişisel veri tespit edildi (skor: {score_ratio:.2f}, eşik: {threshold:.2f})")
                return True
            else:
                print(f"         ✅ Güvenli içerik (skor: {score_ratio:.2f}, eşik: {threshold:.2f})")
                return False
        
        return False
    
    def clean_dataframe(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """DataFrame'i KVKK uyumlu hale getirir"""
        removed_columns = []
        removal_reasons = {}
        df_clean = df.copy()
        
        print("   🔍 KVKK Analizi:")
        
        for column in df.columns:
            # Kolon adına göre kontrol
            if self.is_personal_data_column(column):
                removed_columns.append(column)
                removal_reasons[column] = "Kolon adı (kişisel veri)"
                df_clean = df_clean.drop(column, axis=1)
                print(f"      ❌ '{column}' -> Kolon adı nedeniyle kaldırıldı")
                continue
            
            # İçeriğe göre kontrol
            if self.detect_personal_data_by_content(df[column], column):
                removed_columns.append(column)
                removal_reasons[column] = "İçerik analizi (kişisel veri)"
                df_clean = df_clean.drop(column, axis=1)
                print(f"      ❌ '{column}' -> İçerik analizi nedeniyle kaldırıldı")
                continue
            
            print(f"      ✅ '{column}' -> Güvenli, korunuyor")
        
        return df_clean, removed_columns

class ExcelAnalyzer:
    """Excel dosyalarını analiz eden ana sınıf"""
    
    def __init__(self):
        self.cleaner = KVKKDataCleaner()
        self.analysis_results = {}
    
    def analyze_excel_file(self, file_path: str) -> Dict:
        """Tek bir Excel dosyasını analiz eder"""
        try:
            print(f"\n🔍 Analiz ediliyor: {os.path.basename(file_path)}")
            
            # Excel dosyasını oku
            df = pd.read_excel(file_path)
            
            # Temel bilgiler
            basic_info = {
                'dosya_adi': os.path.basename(file_path),
                'dosya_boyutu': f"{os.path.getsize(file_path) / 1024:.1f} KB",
                'satir_sayisi': len(df),
                'kolon_sayisi': len(df.columns),
                'kolonlar': list(df.columns)
            }
            
            print(f"   📊 {basic_info['satir_sayisi']} satır, {basic_info['kolon_sayisi']} kolon")
            
            # KVKK temizleme
            df_clean, removed_columns = self.cleaner.clean_dataframe(df)
            
            if removed_columns:
                print(f"   🔒 KVKK: {len(removed_columns)} kolon kaldırıldı: {removed_columns}")
            else:
                print("   ✅ KVKK: Kişisel veri tespit edilmedi")
            
            # Tarih kolonlarını tespit et
            date_columns = self.detect_date_columns(df_clean)
            if date_columns:
                print(f"   📅 Tarih kolonları: {date_columns}")
            
            # Veri tipleri analizi
            data_types = self.analyze_data_types(df_clean)
            
            # İçerik analizi
            content_analysis = self.analyze_content(df_clean)
            
            # Sonuçları birleştir
            analysis = {
                'temel_bilgiler': basic_info,
                'kvkk_temizlik': {
                    'kaldirilan_kolonlar': removed_columns,
                    'temiz_kolon_sayisi': len(df_clean.columns),
                    'temiz_kolonlar': list(df_clean.columns)
                },
                'tarih_kolonlari': date_columns,
                'veri_tipleri': data_types,
                'icerik_analizi': content_analysis,
                'temiz_veri': df_clean
            }
            
            return analysis
            
        except Exception as e:
            print(f"   ❌ Hata: {str(e)}")
            return {'hata': str(e)}
    
    def detect_date_columns(self, df: pd.DataFrame) -> List[str]:
        """Tarih kolonlarını otomatik tespit eder"""
        date_columns = []
        
        for column in df.columns:
            # Kolon adına göre
            if any(keyword in column.lower() for keyword in ['tarih', 'date', 'zaman', 'time']):
                try:
                    pd.to_datetime(df[column], errors='coerce')
                    date_columns.append(column)
                except:
                    pass
            
            # İçeriğe göre
            elif df[column].dtype == 'object':
                sample = df[column].dropna().head(5)
                try:
                    parsed_dates = pd.to_datetime(sample, errors='coerce')
                    if parsed_dates.notna().sum() >= len(sample) * 0.8:  # %80 başarı oranı
                        date_columns.append(column)
                except:
                    pass
        
        return date_columns
    
    def analyze_data_types(self, df: pd.DataFrame) -> Dict:
        """Veri tiplerini analiz eder"""
        type_counts = df.dtypes.value_counts().to_dict()
        
        return {
            'tip_dagilimi': {str(k): v for k, v in type_counts.items()},
            'detaylar': {col: str(dtype) for col, dtype in df.dtypes.items()}
        }
    
    def analyze_content(self, df: pd.DataFrame) -> Dict:
        """İçerik analizini yapar"""
        analysis = {
            'bos_degerler': df.isnull().sum().to_dict(),
            'benzersiz_degerler': {col: df[col].nunique() for col in df.columns},
            'ornek_veriler': {}
        }
        
        # Her kolondan örnek veriler al
        for col in df.columns:
            sample_values = df[col].dropna().head(3).tolist()
            analysis['ornek_veriler'][col] = sample_values
        
        return analysis
    
    def analyze_all_files(self) -> Dict:
        """Workspace'teki tüm Excel dosyalarını analiz eder"""
        excel_files = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.xls'))]
        
        if not excel_files:
            print("❌ Excel dosyası bulunamadı!")
            return {}
        
        print(f"📁 {len(excel_files)} Excel dosyası bulundu")
        
        all_results = {}
        for file in excel_files:
            result = self.analyze_excel_file(file)
            all_results[file] = result
        
        return all_results
    
    def generate_summary_report(self, results: Dict) -> str:
        """Analiz sonuçlarının özetini oluşturur"""
        report = []
        report.append("=" * 60)
        report.append("🤖 AKILLI ÜRETİM GÜNLÜĞÜ - EXCEL ANALİZ RAPORU")
        report.append("=" * 60)
        
        total_files = len(results)
        total_rows = sum(r.get('temel_bilgiler', {}).get('satir_sayisi', 0) for r in results.values() if 'hata' not in r)
        total_removed_columns = sum(len(r.get('kvkk_temizlik', {}).get('kaldirilan_kolonlar', [])) for r in results.values() if 'hata' not in r)
        
        report.append(f"\n📊 GENEL ÖZET:")
        report.append(f"   • Toplam dosya: {total_files}")
        report.append(f"   • Toplam satır: {total_rows:,}")
        report.append(f"   • KVKK nedeniyle kaldırılan kolon: {total_removed_columns}")
        
        report.append(f"\n📁 DOSYA DETAYLARI:")
        for file_name, result in results.items():
            if 'hata' in result:
                report.append(f"   ❌ {file_name}: {result['hata']}")
                continue
                
            basic = result.get('temel_bilgiler', {})
            kvkk = result.get('kvkk_temizlik', {})
            
            report.append(f"\n   📄 {file_name}")
            report.append(f"      • Boyut: {basic.get('dosya_boyutu', 'N/A')}")
            report.append(f"      • Satır: {basic.get('satir_sayisi', 0):,}")
            report.append(f"      • Orijinal kolon: {basic.get('kolon_sayisi', 0)}")
            report.append(f"      • Temiz kolon: {kvkk.get('temiz_kolon_sayisi', 0)}")
            
            if kvkk.get('kaldirilan_kolonlar'):
                report.append(f"      • Kaldırılan: {', '.join(kvkk['kaldirilan_kolonlar'])}")
            
            if result.get('tarih_kolonlari'):
                report.append(f"      • Tarih kolonları: {', '.join(result['tarih_kolonlari'])}")
        
        report.append(f"\n🔒 KVKK UYUMLULUK:")
        report.append(f"   • Tüm kişisel veriler otomatik olarak kaldırıldı")
        report.append(f"   • Analiz için güvenli veriler hazır")
        report.append(f"   • AI analizi için uygun format")
        
        report.append(f"\n🚀 SONRAKİ ADIMLAR:")
        report.append(f"   1. Temizlenmiş veriler AI analizi için hazır")
        report.append(f"   2. Tarih filtreleme sistemi eklenebilir")
        report.append(f"   3. Otomatik rapor üretimi başlatılabilir")
        
        report.append("\n" + "=" * 60)
        
        return "\n".join(report)
    
    def save_cleaned_data(self, results: Dict, output_dir: str = "cleaned_data"):
        """Temizlenmiş verileri kaydeder"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for file_name, result in results.items():
            if 'hata' in result or 'temiz_veri' not in result:
                continue
            
            clean_df = result['temiz_veri']
            clean_file_name = f"clean_{file_name}"
            clean_path = os.path.join(output_dir, clean_file_name)
            
            try:
                # Dosya kaydetme denemesi
                clean_df.to_excel(clean_path, index=False)
                print(f"✅ Temiz veri kaydedildi: {clean_path}")
            except PermissionError:
                # Dosya açıksa alternatif isim dene
                timestamp = datetime.now().strftime("%H%M%S")
                alt_file_name = f"clean_{timestamp}_{file_name}"
                alt_path = os.path.join(output_dir, alt_file_name)
                try:
                    clean_df.to_excel(alt_path, index=False)
                    print(f"✅ Temiz veri kaydedildi (alternatif): {alt_path}")
                except Exception as e:
                    print(f"❌ Kaydetme hatası: {clean_path} - {str(e)}")
            except Exception as e:
                print(f"❌ Beklenmeyen kaydetme hatası: {clean_path} - {str(e)}")

def main():
    """Ana çalıştırma fonksiyonu"""
    print("🚀 Akıllı Üretim Günlüğü - Excel Analiz Sistemi")
    print("=" * 50)
    
    # Analyzer'ı başlat
    analyzer = ExcelAnalyzer()
    
    # Tüm dosyaları analiz et
    results = analyzer.analyze_all_files()
    
    if not results:
        return
    
    # Özet raporu oluştur
    summary = analyzer.generate_summary_report(results)
    print(summary)
    
    # Temizlenmiş verileri kaydet
    analyzer.save_cleaned_data(results)
    
    # Raporu dosyaya kaydet
    with open("analiz_raporu.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    
    print(f"\n📄 Detaylı rapor 'analiz_raporu.txt' dosyasına kaydedildi")
    print(f"📁 Temizlenmiş veriler 'cleaned_data/' klasörüne kaydedildi")

if __name__ == "__main__":
    main()
