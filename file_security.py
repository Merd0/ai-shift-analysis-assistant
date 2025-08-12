#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dosya Güvenlik Validation Sistemi  
Excel dosyalarının güvenli şekilde yüklenmesi ve işlenmesi için
"""

import os
import re
from typing import Tuple, Optional, List
import pandas as pd
from datetime import datetime

class SecureFileValidator:
    """
    Kapsamlı dosya güvenlik kontrolü
    
    Kontrol edilen güvenlik faktörleri:
    - Dosya boyutu limitleri
    - Dosya uzantısı doğrulaması  
    - Magic number kontrolü (gerçek dosya formatı)
    - Path traversal saldırı önleme
    - Makro içerik tespiti
    - Zararlı Excel formül kontrolü
    - Dosya bütünlüğü kontrolü
    """
    
    # Güvenlik limitleri
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    MIN_FILE_SIZE = 1024              # 1KB (çok küçük dosyalar şüpheli)
    
    # Desteklenen dosya türleri
    ALLOWED_EXTENSIONS = {'.xlsx', '.xls'}
    
    # Excel dosya imzaları (Magic Numbers)
    EXCEL_SIGNATURES = {
        b'PK\x03\x04': '.xlsx',      # ZIP-based Office format
        b'PK\x05\x06': '.xlsx',      # Empty ZIP
        b'PK\x07\x08': '.xlsx',      # Spanned ZIP  
        b'\xd0\xcf\x11\xe0': '.xls', # OLE2 Compound Document
        b'\x09\x08\x04\x00': '.xls', # Alternative OLE2
    }
    
    # Tehlikeli Excel formülleri
    DANGEROUS_FORMULAS = [
        'cmd', 'powershell', 'system', 'shell', 'exec',
        'macro', 'vba', 'script', 'dde', 'msqry32',
        'regsvr32', 'rundll32', 'mshta', 'wscript', 'cscript'
    ]
    
    def __init__(self, enable_magic_check: bool = True):
        """
        Args:
            enable_magic_check: python-magic kütüphanesi kullanılsın mı
        """
        self.enable_magic_check = enable_magic_check
        
        # python-magic kütüphanesi mevcut mu?
        self.magic_available = False
        try:
            import magic
            self.magic_available = True
            print("🔍 Magic number detection: Aktif")
        except ImportError:
            print("⚠️ python-magic kütüphanesi yok - basit kontrol aktif")
            print("   Kurulum: pip install python-magic-bin")
    
    def validate_file(self, file_path: str, detailed_check: bool = True) -> Tuple[bool, str, dict]:
        """
        Kapsamlı dosya güvenlik kontrolü
        
        Args:
            file_path: Kontrol edilecek dosya yolu
            detailed_check: Detaylı içerik kontrolü yapılsın mı
            
        Returns:
            Tuple[bool, str, dict]: (Güvenli_mi, Hata_mesajı, Detay_bilgileri)
        """
        details = {
            "file_path": file_path,
            "checks_performed": [],
            "warnings": [],
            "file_info": {}
        }
        
        try:
            # 1. Temel varlık kontrolü
            check_result, message = self._check_file_exists(file_path)
            details["checks_performed"].append("file_exists")
            if not check_result:
                return False, message, details
            
            # 2. Dosya bilgilerini topla
            details["file_info"] = self._get_file_info(file_path)
            
            # 3. Boyut kontrolü  
            check_result, message = self._check_file_size(file_path)
            details["checks_performed"].append("file_size")
            if not check_result:
                return False, message, details
                
            # 4. Path traversal kontrolü
            check_result, message = self._check_path_traversal(file_path)
            details["checks_performed"].append("path_traversal")
            if not check_result:
                return False, message, details
            
            # 5. Uzantı kontrolü
            check_result, message = self._check_file_extension(file_path)
            details["checks_performed"].append("file_extension")
            if not check_result:
                return False, message, details
            
            # 6. Magic number kontrolü
            check_result, message = self._check_magic_numbers(file_path)
            details["checks_performed"].append("magic_numbers")
            if not check_result:
                return False, message, details
            
            # 7. Detaylı içerik kontrolü (opsiyonel)
            if detailed_check:
                # Excel makro kontrolü
                check_result, message = self._check_excel_macros(file_path)
                details["checks_performed"].append("macro_check")
                if not check_result:
                    details["warnings"].append(message)
                    # Makro varsa uyarı ver ama engellemeyebiliriz
                    
                # Excel formül güvenlik kontrolü
                check_result, message = self._check_dangerous_formulas(file_path)
                details["checks_performed"].append("formula_check")
                if not check_result:
                    return False, message, details
            
            # 8. Pandas ile format doğrulama (son test)
            check_result, message = self._test_pandas_reading(file_path)
            details["checks_performed"].append("pandas_test")
            if not check_result:
                return False, f"Excel format hatası: {message}", details
            
            # Tüm kontroller başarılı
            success_message = f"✅ Dosya güvenlik kontrollerinden geçti ({len(details['checks_performed'])} kontrol)"
            return True, success_message, details
            
        except Exception as e:
            return False, f"Dosya validasyon hatası: {str(e)}", details
    
    def _check_file_exists(self, file_path: str) -> Tuple[bool, str]:
        """Dosya varlık kontrolü"""
        if not file_path:
            return False, "Dosya yolu boş"
            
        if not os.path.exists(file_path):
            return False, "Dosya bulunamadı"
            
        if not os.path.isfile(file_path):
            return False, "Belirtilen yol bir dosya değil"
            
        return True, "Dosya mevcut"
    
    def _check_file_size(self, file_path: str) -> Tuple[bool, str]:
        """Dosya boyutu kontrolü"""
        try:
            file_size = os.path.getsize(file_path)
            
            if file_size < self.MIN_FILE_SIZE:
                return False, f"Dosya çok küçük: {file_size} byte (Min: {self.MIN_FILE_SIZE})"
                
            if file_size > self.MAX_FILE_SIZE:
                size_mb = file_size / (1024 * 1024)
                limit_mb = self.MAX_FILE_SIZE / (1024 * 1024)
                return False, f"Dosya çok büyük: {size_mb:.1f}MB (Limit: {limit_mb:.0f}MB)"
            
            return True, f"Dosya boyutu uygun: {file_size:,} byte"
            
        except OSError as e:
            return False, f"Dosya boyutu okunamadı: {str(e)}"
    
    def _check_path_traversal(self, file_path: str) -> Tuple[bool, str]:
        """Path traversal saldırı kontrolü"""
        try:
            # Dosya yolunu normalize et
            abs_path = os.path.abspath(file_path)
            
            # Çalışma dizinini al
            work_dir = os.path.abspath(os.getcwd())
            
            # Path traversal kontrolü - dosya çalışma dizini dışında mı?
            if not abs_path.startswith(work_dir):
                return False, "Güvenlik: Dosya çalışma dizini dışında (Path traversal saldırısı)"
            
            # Şüpheli path karakterleri
            suspicious_patterns = ['../', '..\\', '%2e%2e', '%2f', '%5c']
            file_path_lower = file_path.lower()
            
            for pattern in suspicious_patterns:
                if pattern in file_path_lower:
                    return False, f"Güvenlik: Şüpheli path karakteri tespit edildi: {pattern}"
            
            return True, "Path güvenlik kontrolü geçti"
            
        except Exception as e:
            return False, f"Path kontrol hatası: {str(e)}"
    
    def _check_file_extension(self, file_path: str) -> Tuple[bool, str]:
        """Dosya uzantısı kontrolü"""
        _, ext = os.path.splitext(file_path.lower())
        
        if not ext:
            return False, "Dosya uzantısı yok"
            
        if ext not in self.ALLOWED_EXTENSIONS:
            return False, f"Desteklenmeyen dosya türü: {ext} (İzin verilen: {', '.join(self.ALLOWED_EXTENSIONS)})"
        
        return True, f"Dosya uzantısı geçerli: {ext}"
    
    def _check_magic_numbers(self, file_path: str) -> Tuple[bool, str]:
        """Magic number (dosya imzası) kontrolü"""
        try:
            with open(file_path, 'rb') as f:
                header = f.read(16)  # İlk 16 byte
                
            if len(header) < 4:
                return False, "Dosya çok küçük - magic number kontrol edilemedi"
            
            # Excel imzalarını kontrol et
            for signature, expected_ext in self.EXCEL_SIGNATURES.items():
                if header.startswith(signature):
                    file_ext = os.path.splitext(file_path.lower())[1]
                    if file_ext == expected_ext:
                        return True, f"Magic number doğru: {signature.hex()} ({expected_ext})"
                    else:
                        return False, f"Dosya uzantısı ve magic number uyumsuz: {file_ext} vs {expected_ext}"
            
            # python-magic ile daha detaylı kontrol
            if self.magic_available:
                try:
                    import magic
                    file_type = magic.from_file(file_path, mime=True)
                    excel_mime_types = [
                        'application/vnd.ms-excel',
                        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    ]
                    
                    if file_type not in excel_mime_types:
                        return False, f"Magic number Excel formatı değil: {file_type}"
                        
                except Exception:
                    pass  # Magic kontrol başarısız olursa devam et
            
            return False, f"Bilinmeyen dosya imzası: {header[:8].hex()}"
            
        except Exception as e:
            return False, f"Magic number kontrol hatası: {str(e)}"
    
    def _check_excel_macros(self, file_path: str) -> Tuple[bool, str]:
        """Excel makro varlık kontrolü"""
        try:
            file_ext = os.path.splitext(file_path.lower())[1]
            
            if file_ext == '.xlsx':
                # XLSX dosyaları ZIP arşividir
                import zipfile
                try:
                    with zipfile.ZipFile(file_path, 'r') as zip_file:
                        file_list = zip_file.namelist()
                        
                        # Makro dosyalarını ara
                        macro_indicators = [
                            'vbaProject.bin',     # VBA makro dosyası
                            'macros/',            # Makro dizini
                            '/vbaProject',        # VBA project
                            'customUI/',          # Custom UI (makro içerebilir)
                            '.xlsm',              # Makro enabled dosya
                        ]
                        
                        for indicator in macro_indicators:
                            for file_name in file_list:
                                if indicator in file_name.lower():
                                    return False, f"⚠️ Makro tespit edildi: {file_name}"
                        
                        return True, "Makro bulunamadı"
                        
                except zipfile.BadZipFile:
                    return False, "XLSX dosyası bozuk (ZIP formatı değil)"
                    
            elif file_ext == '.xls':
                # .xls dosyaları için basit kontrol
                # OLE2 compound document içeriğini tam parse etmek karmaşık
                # Basit string search yapalım
                try:
                    with open(file_path, 'rb') as f:
                        content = f.read(8192)  # İlk 8KB yeterli
                        
                    # VBA/Macro string'lerini ara
                    macro_strings = [b'VBA', b'macro', b'Module1', b'ThisWorkbook', b'Sub ']
                    
                    for macro_str in macro_strings:
                        if macro_str in content:
                            return False, f"⚠️ Potansiyel makro tespit edildi: {macro_str.decode('ascii', errors='ignore')}"
                    
                    return True, "Makro bulunamadı"
                    
                except Exception:
                    return True, "Makro kontrolü yapılamadı"
            
            return True, "Makro kontrolü tamamlandı"
            
        except Exception as e:
            return True, f"Makro kontrol hatası: {str(e)} (devam ediliyor)"
    
    def _check_dangerous_formulas(self, file_path: str) -> Tuple[bool, str]:
        """Tehlikeli Excel formüllerini tespit et"""
        try:
            # Pandas ile Excel'i oku ve formülleri kontrol et
            # Not: Pandas otomatik olarak formülleri değerlendirir, 
            # bu yüzden ham formül içeriğini göremeyebiliriz
            
            # Basit binary search ile tehlikeli string'leri ara
            with open(file_path, 'rb') as f:
                content = f.read(16384).lower()  # İlk 16KB
            
            for dangerous_term in self.DANGEROUS_FORMULAS:
                if dangerous_term.encode() in content:
                    return False, f"🚨 Tehlikeli formül tespit edildi: {dangerous_term}"
            
            return True, "Tehlikeli formül bulunamadı"
            
        except Exception as e:
            return True, f"Formül kontrol hatası: {str(e)} (devam ediliyor)"
    
    def _test_pandas_reading(self, file_path: str) -> Tuple[bool, str]:
        """Pandas ile dosyayı okuyabilir miyiz test et"""
        try:
            # Sadece ilk birkaç satırı oku (hızlı test)
            df = pd.read_excel(file_path, nrows=5, engine='openpyxl')
            
            if df.empty:
                return False, "Excel dosyası boş"
            
            return True, f"Pandas test başarılı - {len(df)} satır okundu"
            
        except Exception as e:
            return False, f"Pandas okuma hatası: {str(e)}"
    
    def _get_file_info(self, file_path: str) -> dict:
        """Dosya bilgilerini topla"""
        try:
            stat = os.stat(file_path)
            
            return {
                "file_name": os.path.basename(file_path),
                "file_size": stat.st_size,
                "file_size_mb": round(stat.st_size / (1024*1024), 2),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "extension": os.path.splitext(file_path)[1].lower()
            }
        except Exception:
            return {"error": "Dosya bilgileri alınamadı"}


# ========================================================================================
# KOLAY KULLANIM FONKSİYONU
# ========================================================================================

def validate_excel_file(file_path: str, detailed: bool = True) -> Tuple[bool, str]:
    """
    Excel dosyasını güvenlik kontrolünden geçir (basit kullanım)
    
    Args:
        file_path: Excel dosya yolu
        detailed: Detaylı kontrol (makro, formül kontrolü)
        
    Returns:
        Tuple[bool, str]: (Güvenli_mi, Mesaj)
    """
    validator = SecureFileValidator()
    is_valid, message, details = validator.validate_file(file_path, detailed)
    
    return is_valid, message


# ========================================================================================  
# TEST FONKSİYONU
# ========================================================================================

def test_file_validator():
    """File validator test"""
    print("🧪 Secure File Validator Test")
    print("=" * 50)
    
    validator = SecureFileValidator()
    
    # Test dosyaları oluştur
    test_files = [
        ("test_valid.xlsx", b'PK\x03\x04' + b'\x00' * 1000),  # Geçerli XLSX
        ("test_too_small.xlsx", b'PK'),                        # Çok küçük
        ("test_wrong_ext.txt", b'PK\x03\x04' + b'\x00' * 100), # Yanlış uzantı
        ("test_wrong_magic.xlsx", b'INVALID' + b'\x00' * 100), # Yanlış magic
    ]
    
    for filename, content in test_files:
        try:
            with open(filename, 'wb') as f:
                f.write(content)
            
            print(f"\n🔍 Test: {filename}")
            is_valid, message, details = validator.validate_file(filename, detailed_check=False)
            print(f"   Sonuç: {'✅ Geçti' if is_valid else '❌ Başarısız'}")
            print(f"   Mesaj: {message}")
            print(f"   Kontroller: {', '.join(details['checks_performed'])}")
            
            # Test dosyasını sil
            os.remove(filename)
            
        except Exception as e:
            print(f"   Hata: {e}")
    
    print("\n✅ Test tamamlandı!")


if __name__ == "__main__":
    test_file_validator()
