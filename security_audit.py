#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Güvenlik Audit Logging Sistemi
Akıllı Üretim Günlüğü için tüm kritik işlemleri güvenli şekilde loglar
"""

import logging
import json
import os
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional
import traceback

class SecurityAuditLogger:
    """
    Güvenlik ve işlem auditı için comprehensive logging sistemi
    
    Özellikler:
    - Günlük log dosyası rotasyonu
    - JSON formatında yapılandırılmış loglar
    - Session tracking
    - Farklı log seviyeleri
    - Güvenlik olayları özel takibi
    """
    
    def __init__(self, base_dir: Optional[str] = None):
        """
        Args:
            base_dir: Log dosyalarının saklanacağı ana dizin
        """
        # Log dizini ayarı
        if base_dir is None:
            base_dir = os.getcwd()
        
        self.log_dir = os.path.join(base_dir, 'logs')
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Session ID - bu uygulama çalışması için unique
        self.session_id = hashlib.md5(
            f"{datetime.now()}{os.getpid()}".encode()
        ).hexdigest()[:8]
        
        # Log dosyası adı (günlük)
        today = datetime.now().strftime('%Y%m%d')
        self.log_file = os.path.join(self.log_dir, f'audit_{today}.log')
        
        # Logger kurulumu
        self.setup_logger()
        
        # İlk log - session başlatma
        self.log_app_start()
        
        print(f"📝 Audit Logger başlatıldı:")
        print(f"   📁 Log dizini: {self.log_dir}")
        print(f"   📄 Log dosyası: {os.path.basename(self.log_file)}")
        print(f"   🆔 Session ID: {self.session_id}")
    
    def setup_logger(self):
        """Logger konfigürasyonu"""
        self.logger = logging.getLogger(f'SecurityAudit_{self.session_id}')
        self.logger.setLevel(logging.INFO)
        
        # Mevcut handler'ları temizle
        self.logger.handlers.clear()
        
        # Dosya handler
        file_handler = logging.FileHandler(
            self.log_file,
            mode='a',
            encoding='utf-8'
        )
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s|%(levelname)s|%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
    
    def _create_log_entry(self, event_type: str, details: Dict[str, Any]) -> str:
        """
        Standart log entry formatı oluştur
        
        Args:
            event_type: Log olayı tipi (APP_START, FILE_OPERATION, vb.)
            details: Olay detayları
            
        Returns:
            JSON formatında log string
        """
        entry = {
            "session_id": self.session_id,
            "event_type": event_type,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        return json.dumps(entry, ensure_ascii=False, separators=(',', ':'))
    
    # ========================================================================================
    # ANA LOG FONKSİYONLARI
    # ========================================================================================
    
    def log_app_start(self):
        """Uygulama başlangıcı"""
        try:
            import platform
            from version import get_version_string
            version = get_version_string()
        except:
            version = "1.4.3"
            
        self.logger.info(self._create_log_entry("APP_START", {
            "app_version": version,
            "user": os.getenv('USERNAME', os.getenv('USER', 'unknown')),
            "platform": platform.system() if 'platform' in locals() else 'unknown',
            "python_version": platform.python_version() if 'platform' in locals() else 'unknown',
            "working_directory": os.getcwd(),
            "log_file": self.log_file
        }))
    
    def log_file_operation(self, operation: str, file_path: str, success: bool, 
                          details: str = "", file_size: Optional[int] = None):
        """
        Dosya işlemleri
        
        Args:
            operation: İşlem tipi (SELECT, ANALYZE, EXPORT, vb.)
            file_path: Dosya yolu
            success: İşlem başarılı mı
            details: Ek detaylar
            file_size: Dosya boyutu (byte)
        """
        log_details = {
            "operation": operation,
            "success": success,
            "details": details
        }
        
        if file_path:
            log_details.update({
                "file_name": os.path.basename(file_path),
                "file_extension": os.path.splitext(file_path)[1].lower(),
                "file_size": file_size or (os.path.getsize(file_path) if os.path.exists(file_path) else 0)
            })
        
        self.logger.info(self._create_log_entry("FILE_OPERATION", log_details))
    
    def log_api_call(self, provider: str, model: str, success: bool,
                    token_usage: Optional[Dict[str, int]] = None, error: str = ""):
        """
        AI API çağrıları
        
        Args:
            provider: AI sağlayıcı (openai, anthropic, xai)
            model: Model adı
            success: Çağrı başarılı mı
            token_usage: Token kullanım bilgileri
            error: Hata mesajı (varsa)
        """
        log_details = {
            "provider": provider,
            "model": model,
            "success": success
        }
        
        if token_usage:
            log_details.update({
                "prompt_tokens": token_usage.get('prompt_tokens', 0),
                "completion_tokens": token_usage.get('completion_tokens', 0),
                "total_tokens": token_usage.get('total_tokens', 0)
            })
        
        if error:
            log_details["error"] = error
        
        self.logger.info(self._create_log_entry("API_CALL", log_details))
    
    def log_security_event(self, event_type: str, severity: str, description: str,
                          file_path: str = "", user_action: str = ""):
        """
        Güvenlik olayları
        
        Args:
            event_type: Olay tipi (FILE_VALIDATION, INVALID_INPUT, vb.)
            severity: Önem derecesi (LOW, MEDIUM, HIGH, CRITICAL)
            description: Olay açıklaması
            file_path: İlgili dosya (varsa)
            user_action: Kullanıcı eylemi
        """
        log_details = {
            "security_event": event_type,
            "severity": severity,
            "description": description
        }
        
        if file_path:
            log_details["file_name"] = os.path.basename(file_path)
            
        if user_action:
            log_details["user_action"] = user_action
        
        # Güvenlik olayları WARNING seviyesinde
        self.logger.warning(self._create_log_entry("SECURITY_EVENT", log_details))
    
    def log_export_operation(self, export_type: str, output_file: str, success: bool,
                           details: str = ""):
        """
        Rapor export işlemleri
        
        Args:
            export_type: Export tipi (PDF, EXCEL, WORD)
            output_file: Çıktı dosyası
            success: İşlem başarılı mı
            details: Ek bilgiler
        """
        log_details = {
            "export_type": export_type,
            "success": success,
            "details": details
        }
        
        if output_file:
            log_details.update({
                "output_file": os.path.basename(output_file),
                "output_size": os.path.getsize(output_file) if os.path.exists(output_file) else 0
            })
        
        self.logger.info(self._create_log_entry("EXPORT_OPERATION", log_details))
    
    def log_error(self, error_type: str, error_message: str, 
                 context: str = "", include_traceback: bool = True):
        """
        Sistem hataları
        
        Args:
            error_type: Hata tipi
            error_message: Hata mesajı
            context: Hata bağlamı
            include_traceback: Stack trace ekle
        """
        log_details = {
            "error_type": error_type,
            "error_message": str(error_message),
            "context": context
        }
        
        if include_traceback:
            log_details["stack_trace"] = traceback.format_exc()
        
        self.logger.error(self._create_log_entry("ERROR", log_details))
    
    def log_user_action(self, action: str, details: str = "", success: bool = True):
        """
        Kullanıcı eylemleri
        
        Args:
            action: Eylem (BUTTON_CLICK, TAB_CHANGE, vb.)
            details: Eylem detayları
            success: İşlem başarılı mı
        """
        self.logger.info(self._create_log_entry("USER_ACTION", {
            "action": action,
            "details": details,
            "success": success
        }))
    
    # ========================================================================================
    # YARDIMCI FONKSİYONLAR
    # ========================================================================================
    
    def get_log_stats(self) -> Dict[str, Any]:
        """Log istatistikleri"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                return {
                    "log_file": self.log_file,
                    "session_id": self.session_id,
                    "total_entries": len(lines),
                    "file_size": os.path.getsize(self.log_file),
                    "created": datetime.fromtimestamp(os.path.getctime(self.log_file)).isoformat()
                }
            else:
                return {"error": "Log dosyası bulunamadı"}
        except Exception as e:
            return {"error": str(e)}
    
    def close(self):
        """Logger'ı kapat"""
        self.log_user_action("APP_SHUTDOWN", "Uygulama kapatıldı")
        
        # Handler'ları kapat
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)


# ========================================================================================
# TEST FONKSİYONU
# ========================================================================================

def test_audit_logger():
    """Audit logger test"""
    print("🧪 Security Audit Logger Test")
    print("=" * 50)
    
    # Logger başlat
    logger = SecurityAuditLogger()
    
    # Test işlemleri
    logger.log_file_operation("TEST_SELECT", "test_file.xlsx", True, "Test dosyası", 1024)
    logger.log_api_call("openai", "gpt-4o-mini", True, {"total_tokens": 1500})
    logger.log_security_event("TEST_EVENT", "LOW", "Test güvenlik olayı")
    logger.log_error("TEST_ERROR", "Test hatası", "Test context")
    logger.log_user_action("BUTTON_CLICK", "Test butonu tıklandı")
    
    # İstatistikler
    stats = logger.get_log_stats()
    print(f"\n📊 Log İstatistikleri:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Log dosyasını göster
    print(f"\n📄 Son 5 log girişi:")
    try:
        with open(logger.log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[-5:]:
                print(f"   {line.strip()}")
    except:
        print("   Log dosyası okunamadı")
    
    logger.close()
    print("\n✅ Test tamamlandı!")


if __name__ == "__main__":
    test_audit_logger()
