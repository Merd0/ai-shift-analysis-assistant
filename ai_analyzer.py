#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Destekli Vardiya Devir Analiz Asistanı
Çimento Fabrikası Vardiya Defteri Analizi için Optimize Edilmiş AI Sistemi
"""

import openai
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
import re
from config import MODEL_NAME, MAX_TOKENS, TEMPERATURE

class CimentoVardiyaAI:
    def __init__(self, api_key: str = ""):
        """
        Çimento fabrikası vardiya analizi için AI sistemi
        
        Args:
            api_key: OpenAI API key (güvenlik için parametre olarak alınır)
        """
        if not api_key:
            raise ValueError("⚠️ API Key gerekli! Lütfen GUI'de API key'inizi girin.")
        
        openai.api_key = api_key
        self.model = MODEL_NAME
        self.max_tokens = MAX_TOKENS
        self.temperature = TEMPERATURE
        
        # Çimento fabrikası spesifik context
        self.cement_context = self._load_cement_context()
        
    def _load_cement_context(self) -> str:
        """Çimento fabrikası için optimize edilmiş context"""
        return """
# ÇİMENTO FABRİKASI VARDİYA DEFTERİ ANALİZ SİSTEMİ

## AMAÇ:
Çimento üretim sürecindeki vardiya kayıtlarını analiz ederek:
- Üretim sorunlarını tespit etmek
- Ekipman arızalarını kategorize etmek  
- Çözüm önerileri sunmak
- Yönetici raporları oluşturmak

## ÇİMENTO ÜRETİM SÜRECİ BİLGİSİ:
1. HAMMADDE HAZIRLAMA: Kireçtaşı, kil, demir cevheri karışımı
2. ÖĞÜTME: Ham karışım öğütücülerde (ÇD1, ÇD2, ÇD3, ÇD4) ince hale getirilir
3. FIRINDA YAKMA: 1450°C'de klinker üretimi (Fırın 1, Fırın 2)
4. ÇİMENTO ÖĞÜTME: Klinker + alçı karışımı (ÇİM1, ÇİM2)
5. DEPOLAMA: Silolarda (Silo 1-8) depolama
6. PAKETLEME/YÜKLEME: Torba veya dökme sevkiyat

## TEMEL EKİPMANLAR:
- ÇD1,ÇD2,ÇD3,ÇD4: Çiğ değirmenler
- ÇİM1,ÇİM2: Çimento değirmenleri  
- F1,F2: Fırınlar
- Silo 1-8: Depolama siloları
- CSO: Çimento kalite parametreleri
- XRF: Kimyasal analiz cihazı
- Bunker, Konveyör, Filtre sistemleri

## SIKÇA YAŞANAN SORUNLAR:
- Aşırı ısınma (özellikle değirmenlerde)
- Filtre tıkanması
- Konveyör arızaları
- Kalite spek dışı değerler
- Hammadde besleme sorunları
- Elektrik kesintileri
- Yedek parça eksiklikleri

## ANALİZ ÇIKTI FORMATI:
1. GÜNLÜK ÖZET: Üretim miktarı, duruş süreleri
2. SORUNLAR: Yaşanan arızalar, nedenleri, süreleri
3. ÇÖZÜMLER: Alınan aksiyonlar, etkililik
4. ÖNERİLER: Önleyici bakım, iyileştirme önerileri
5. TREND: Tekrarlanan sorunlar, risk analizi
"""

    def analyze_shift_data(self, data: pd.DataFrame, date_range: str = "günlük") -> Dict:
        """Vardiya verilerini analiz et"""
        
        # Veriyi özetleyerek token tasarrufu
        summary_data = self._summarize_data(data)
        
        # AI prompt oluştur
        prompt = self._create_analysis_prompt(summary_data, date_range)
        
        # AI analizi çağır
        analysis = self._call_openai_api(prompt)
        
        return analysis

    def _summarize_data(self, data: pd.DataFrame) -> str:
        """Veriyi özetleyerek token kullanımını optimize et"""
        
        summary_parts = []
        
        # Temel istatistikler
        summary_parts.append(f"📊 GENEL BİLGİ:")
        summary_parts.append(f"- Toplam kayıt: {len(data)} adet")
        summary_parts.append(f"- Tarih aralığı: {data['Tarih'].min()} - {data['Tarih'].max()}")
        
        # Açıklama verilerini özetle (en uzun kolonlar genelde açıklama)
        description_columns = [col for col in data.columns if 
                             any(keyword in col.lower() for keyword in 
                                ['açıklama', 'iletil', 'takip', 'kalite', 'arıza', 'bakım'])]
        
        if description_columns:
            summary_parts.append(f"\n🔍 ÖNEMLİ KAYITLAR:")
            
            # Her kolondaki önemli kayıtları özetle
            for col in description_columns[:3]:  # Sadece ilk 3 kolonu al (token tasarrufu)
                non_empty = data[col].dropna()
                if len(non_empty) > 0:
                    # En uzun ve en kısa kayıtları örnek olarak al
                    samples = non_empty.head(5).tolist()  # Sadece 5 örnek
                    summary_parts.append(f"\n{col}:")
                    for i, sample in enumerate(samples, 1):
                        # Çok uzun metinleri kısalt
                        sample_text = str(sample)[:200] + "..." if len(str(sample)) > 200 else str(sample)
                        summary_parts.append(f"  {i}. {sample_text}")
        
        # CSO verilerini özetle (varsa)
        cso_columns = [col for col in data.columns if 'cso' in col.lower()]
        if cso_columns:
            summary_parts.append(f"\n📈 KALİTE PARAMETRELERİ (CSO):")
            for col in cso_columns[:5]:  # Sadece 5 CSO parametresi
                if data[col].dtype in ['int64', 'float64']:
                    avg_val = data[col].mean()
                    min_val = data[col].min()
                    max_val = data[col].max()
                    summary_parts.append(f"  {col}: Ort={avg_val:.1f}, Min={min_val:.1f}, Max={max_val:.1f}")
        
        return "\n".join(summary_parts)

    def _create_analysis_prompt(self, summary_data: str, date_range: str) -> str:
        """Çimento fabrikası için optimize edilmiş prompt"""
        
        prompt = f"""
{self.cement_context}

## ANALİZ EDİLECEK VERİ ({date_range.upper()}):
{summary_data}

## GÖREV:
Bu çimento fabrikası vardiya verilerini analiz ederek aşağıdaki formatta TÜRKÇE rapor hazırla:

### 📊 GÜNLÜK ÖZET:
- Üretim durumu (normal/sorunlu)
- Toplam duruş sayısı ve süresi
- En aktif vardiya (gece/gündüz)

### ⚠️ TESPİT EDİLEN SORUNLAR:
- Ekipman arızaları (ÇD, ÇİM, Fırın, vb.)
- Kalite sorunları (CSO değerleri)
- Operasyonel sorunlar
- Her sorun için: [EKİPMAN] - [SORUN] - [SÜRE/ETKİ]

### ✅ UYGULANAN ÇÖZÜMLER:
- Alınan aksiyonlar
- Çözüm süreleri
- Etkililiği

### 🎯 ÖNERİLER:
- Önleyici bakım önerileri
- Süreç iyileştirmeleri
- Risk azaltma önerileri

### 📈 TREND ANALİZİ:
- Tekrarlanan sorunlar
- Risk faktörleri
- Dikkat edilmesi gerekenler

## ÖNEMLİ KURALLAR:
1. Sadece verilen bilgileri kullan, ek bilgi ekleme
2. Çimento üretim terminolojisi kullan
3. Kısa ve net cümleler
4. Sayısal veriler varsa belirt
5. Spekülasyon yapma, sadece gözlem

RAPOR:
"""
        return prompt

    def _call_openai_api(self, prompt: str) -> Dict:
        """OpenAI API çağrısı - optimize edilmiş"""
        
        try:
            client = openai.OpenAI(api_key=openai.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "Sen çimento fabrikası vardiya analizi uzmanısın. Verilen verileri analiz ederek profesyonel raporlar hazırlarsın."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=0.9,  # Token verimliliği için
                frequency_penalty=0.1,  # Tekrarları azalt
                presence_penalty=0.1   # Çeşitliliği artır
            )
            
            analysis_text = response.choices[0].message.content
            
            # Yanıtı yapılandırılmış formata çevir
            structured_analysis = self._parse_analysis_response(analysis_text)
            
            # Token kullanımını logla
            token_usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
                'estimated_cost': response.usage.total_tokens * 0.00015 / 1000  # GPT-4o-mini fiyatı
            }
            
            return {
                'analysis': structured_analysis,
                'raw_response': analysis_text,
                'token_usage': token_usage,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'error': f"AI analizi hatası: {str(e)}",
                'analysis': None,
                'token_usage': None,
                'timestamp': datetime.now().isoformat()
            }

    def _parse_analysis_response(self, response_text: str) -> Dict:
        """AI yanıtını yapılandırılmış formata çevir"""
        
        sections = {
            'günlük_özet': '',
            'sorunlar': [],
            'çözümler': [],
            'öneriler': [],
            'trend_analizi': ''
        }
        
        # Basit parsing (regex ile bölümleri ayır)
        current_section = None
        lines = response_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Bölüm başlıklarını tespit et
            if '📊' in line or 'GÜNLÜK ÖZET' in line:
                current_section = 'günlük_özet'
                continue
            elif '⚠️' in line or 'SORUNLAR' in line:
                current_section = 'sorunlar'
                continue
            elif '✅' in line or 'ÇÖZÜMLER' in line:
                current_section = 'çözümler'
                continue
            elif '🎯' in line or 'ÖNERİLER' in line:
                current_section = 'öneriler'
                continue
            elif '📈' in line or 'TREND' in line:
                current_section = 'trend_analizi'
                continue
            
            # İçeriği ilgili bölüme ekle
            if current_section:
                if current_section in ['sorunlar', 'çözümler', 'öneriler']:
                    if line.startswith('-') or line.startswith('•'):
                        sections[current_section].append(line[1:].strip())
                else:
                    sections[current_section] += line + '\n'
        
        return sections

    def generate_manager_report(self, analysis: Dict, period: str = "günlük") -> str:
        """Yönetici için özet rapor oluştur"""
        
        if analysis.get('error'):
            return f"❌ Rapor oluşturulamadı: {analysis['error']}"
        
        structured = analysis['analysis']
        token_info = analysis.get('token_usage', {})
        
        report = f"""
🏭 ÇİMENTO FABRİKASI VARDİYA RAPORU
{'='*50}
📅 Rapor Tipi: {period.title()}
🕐 Oluşturma: {datetime.now().strftime('%d.%m.%Y %H:%M')}

{structured.get('günlük_özet', 'Özet bulunamadı')}

⚠️ KRİTİK SORUNLAR ({len(structured.get('sorunlar', []))} adet):
"""
        
        for i, sorun in enumerate(structured.get('sorunlar', [])[:5], 1):  # Sadece ilk 5 sorun
            report += f"{i}. {sorun}\n"
        
        report += f"""
🎯 ÖNCELIKLI AKSIYONLAR ({len(structured.get('öneriler', []))} adet):
"""
        
        for i, öneri in enumerate(structured.get('öneriler', [])[:3], 1):  # Sadece ilk 3 öneri
            report += f"{i}. {öneri}\n"
        
        if token_info:
            report += f"""
📊 SİSTEM BİLGİSİ:
- Token kullanımı: {token_info.get('total_tokens', 0)}
- Tahmini maliyet: ${token_info.get('estimated_cost', 0):.4f}
"""
        
        return report

    def save_analysis(self, analysis: Dict, filename: str = None) -> str:
        """Analizi dosyaya kaydet"""
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"vardiya_analizi_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, ensure_ascii=False, indent=2)
            return filename
        except Exception as e:
            return f"Kayıt hatası: {str(e)}"


# Test fonksiyonu
def test_ai_system():
    """AI sistemini test et"""
    print("🤖 AI Vardiya Analiz Sistemi Test Ediliyor...")
    
    ai = CimentoVardiyaAI()
    
    # Örnek veri oluştur (gerçek veri yerine)
    sample_data = pd.DataFrame({
        'Tarih': ['2025-08-07', '2025-08-07', '2025-08-07'],
        'Vardiya': ['07:00-15:00', '15:00-23:00', '23:00-07:00'],
        'Açıklama': [
            'ÇD2 saat 10:30da durdu. Aşırı ısınma nedeniyle. Soğutma sistemi kontrol edildi.',
            'Fırın 1 normal çalışıyor. CSO değerleri spek içinde.',
            'ÇİM2 öğütücüsünde titreşim var. Bakım ekibi bilgilendirildi.'
        ],
        'CSO 1': [2.1, 2.3, 2.2],
        'CSO 2': [3.1, 3.0, 3.2]
    })
    
    # Analiz et
    result = ai.analyze_shift_data(sample_data)
    
    if result.get('error'):
        print(f"❌ Hata: {result['error']}")
        return
    
    # Yönetici raporu oluştur
    manager_report = ai.generate_manager_report(result)
    print(manager_report)
    
    # Dosyaya kaydet
    saved_file = ai.save_analysis(result)
    print(f"\n💾 Analiz kaydedildi: {saved_file}")


if __name__ == "__main__":
    test_ai_system()
