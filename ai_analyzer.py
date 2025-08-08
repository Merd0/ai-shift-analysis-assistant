#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Destekli Vardiya Devir Analiz Asistanı
Çimento Fabrikası Vardiya Defteri Analizi için Optimize Edilmiş AI Sistemi
"""

from openai import OpenAI
import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
import re
from config import MODEL_NAME, MAX_TOKENS, TEMPERATURE

class CimentoVardiyaAI:
    def __init__(self, api_key: str = "", provider: str = "openai", model: Optional[str] = None, base_url: Optional[str] = None):
        """
        Çimento fabrikası vardiya analizi için AI sistemi
        
        Args:
            api_key: OpenAI API key (güvenlik için parametre olarak alınır)
        """
        if not api_key:
            raise ValueError("⚠️ API Key gerekli! Lütfen GUI'de API key'inizi girin.")

        # Sağlayıcı seçimi
        self.provider = provider.lower().strip()
        self.api_key = api_key

        # OpenAI istemcisi (varsayılan)
        self.client = None
        if self.provider == "openai":
            self.client = OpenAI(api_key=api_key)

        # Model seçimi
        self.model = model or MODEL_NAME
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

    def analyze_shift_data(self, data: pd.DataFrame, date_range: str = "günlük", 
                          analysis_options: List[str] = None, user_question: str = "") -> Dict:
        """
        Vardiya verilerini gelişmiş AI sistemi ile analiz et
        
        Args:
            data: Analiz edilecek vardiya verileri
            date_range: Analiz periyodu ("günlük", "haftalık", vb.)
            analysis_options: İstenilen rapor bölümleri listesi
            user_question: Kullanıcının özel sorusu
            
        Returns:
            Dict: AI analiz sonuçları
        """
        
        # Veriyi özetleyerek token tasarrufu
        summary_data = self._summarize_data(data)
        
        # Yeni gelişmiş AI prompt oluştur
        prompt = self._create_analysis_prompt(summary_data, date_range, analysis_options, user_question)
        
        # AI analizi çağır
        analysis = self._call_llm_api(prompt)
        
        return analysis

    def _summarize_data(self, data: pd.DataFrame) -> str:
        """Veriyi zengin şekilde özetleyip AI'a güçlü bağlam sağla (KPI + trend + top listeler).

        Ayrıca bazı dağılımları önceden hesaplayıp yüzde toplamını %100'e normalize eder.
        """

        lines: List[str] = []

        # Tarih bilgisi (varsa)
        date_col_candidates = [c for c in data.columns if any(k in c.lower() for k in ['tarih', 'date'])]
        date_range_text = "N/A"
        if date_col_candidates:
            dc = date_col_candidates[0]
            try:
                dates = pd.to_datetime(data[dc], errors='coerce')
                min_d = dates.min()
                max_d = dates.max()
                if pd.notna(min_d) and pd.notna(max_d):
                    date_range_text = f"{min_d.date()} - {max_d.date()}"
            except Exception:
                pass

        # Genel
        lines.append("📊 GENEL BİLGİ:")
        lines.append(f"- Toplam kayıt: {len(data)}")
        lines.append(f"- Tarih aralığı: {date_range_text}")

        # Vardiya dağılımı (normalize + örnekleme hatalarına dayanıklı)
        shift_col = next((c for c in data.columns if 'vardiya' in c.lower()), None)
        if shift_col is not None:
            try:
                vc = data[shift_col].astype(str).str.strip().replace({'': None}).dropna().value_counts()
                dist = vc.head(10)
                lines.append("\n🕒 VARDİYA DAĞILIMI (ilk 10):")
                for k, v in dist.items():
                    lines.append(f"- {k}: {int(v)}")
            except Exception:
                pass

        # Normalize edici yardımcı
        def _normalized_percentages(vc: pd.Series, top_n: int = 10) -> List[Tuple[str, int, int]]:
            """value_counts serisini ilk top_n için (ad, adet, %) ve bir 'Diğer' ile %100'e
            tamamlayarak döndürür. Yüzdeler tamsayıya yuvarlanır ve son kaleme fark eklenir.
            """
            items = vc.head(top_n)
            total = int(vc.sum()) if vc.sum() else 0
            result: List[Tuple[str, int, int]] = []
            if total == 0:
                return result
            percents = []
            names = list(items.index.astype(str))
            counts = list(items.astype(int).values)
            for c in counts:
                percents.append(int(round(c * 100.0 / total)))
            diff = 100 - sum(percents)
            if percents:
                percents[-1] += diff
            for n, c, p in zip(names, counts, percents):
                result.append((n, int(c), int(p)))
            # Diğer
            others = total - sum(counts)
            if others > 0:
                p_other = max(0, 100 - sum([p for _, _, p in result]))
                result.append(("Diğer", int(others), int(p_other)))
            return result

        # Ekipman dağılımı
        equipment_col = next((c for c in data.columns if any(k in c.lower() for k in ['ekipman', 'makine', 'ünite', 'unite', 'unit'])), None)
        if equipment_col is not None:
            try:
                vc = data[equipment_col].astype(str).str.strip().replace({'': None}).dropna().value_counts()
                lines.append("\n🏭 EKİPMAN DAĞILIMI (ilk 10, normalize):")
                dist = _normalized_percentages(vc, top_n=10)
                for name, cnt, pct in dist:
                    lines.append(f"- {name}: {cnt} kayıt (%{pct})")
                if vc.sum() > 0:
                    lines.append("Toplam = %100")
            except Exception:
                pass

        # Sorun / Kategori dağılımı
        issue_col = next((c for c in data.columns if any(k in c.lower() for k in ['sorun', 'arıza', 'ariza', 'problem', 'kategori'])), None)
        if issue_col is not None:
            try:
                vc = data[issue_col].astype(str).str.strip().replace({'': None}).dropna().str.lower().value_counts()
                lines.append("\n⚠️ SORUN KATEGORİLERİ (ilk 10, normalize):")
                dist = _normalized_percentages(vc, top_n=10)
                for name, cnt, pct in dist:
                    lines.append(f"- {name}: {cnt} kayıt (%{pct})")
                if vc.sum() > 0:
                    lines.append("Toplam = %100")
            except Exception:
                pass

        # Duruş/Süre (dakika)
        duration_col = next((c for c in data.columns if any(k in c.lower() for k in ['süre', 'sure', 'dakika', 'dk'])), None)
        if duration_col is not None:
            try:
                # Metin içindeki sayıları da yakalamaya çalış (ör. "45 dk", "~30")
                cleaned = (
                    data[duration_col]
                    .astype(str)
                    .str.extract(r'(\d+[\.,]?\d*)', expand=False)
                )
                durations = pd.to_numeric(cleaned.str.replace(',', '.', regex=False), errors='coerce')
                total_min = durations.fillna(0).sum()
                avg_min = durations.dropna().mean() if durations.notna().any() else 0
                lines.append("\n⏱️ Duruş Süresi (dakika):")
                lines.append(f"- Toplam: {int(total_min)} dk")
                lines.append(f"- Ortalama: {avg_min:.1f} dk/kayıt")
            except Exception:
                pass

        # Trend özeti (son 7 gün vs önceki 7 gün)
        if date_col_candidates:
            dc = date_col_candidates[0]
            try:
                df_copy = data.copy()
                df_copy[dc] = pd.to_datetime(df_copy[dc], errors='coerce')
                daily_counts = df_copy.groupby(df_copy[dc].dt.date).size().sort_index()
                if len(daily_counts) >= 14:
                    last7 = daily_counts[-7:].sum()
                    prev7 = daily_counts[-14:-7].sum()
                    delta = last7 - prev7
                    trend = "↑" if delta > 0 else ("↓" if delta < 0 else "=")
                    lines.append("\n📈 Trend (kayıt adedi):")
                    lines.append(f"- Son 7 gün: {int(last7)} | Önceki 7: {int(prev7)} | Fark: {int(delta)} {trend}")
            except Exception:
                pass

        # Açıklamalardan kısa örnekler
        description_columns = [col for col in data.columns if any(keyword in col.lower() for keyword in ['açıklama', 'aciklama', 'iletil', 'takip', 'kalite', 'arıza', 'ariza', 'bakım', 'bakim', 'not', 'yorum'])]
        if description_columns:
            lines.append("\n🔍 ÖRNEK KAYITLAR (max 3 kolon x 3 örnek):")
            for col in description_columns[:3]:
                non_empty = data[col].dropna().astype(str)
                if len(non_empty) > 0:
                    samples = non_empty.head(3).tolist()
                    lines.append(f"- {col}:")
                    for i, sample in enumerate(samples, 1):
                        sample_text = sample[:200] + "..." if len(sample) > 200 else sample
                        lines.append(f"  {i}. {sample_text}")

        return "\n".join(lines)

    def _create_analysis_prompt(self, summary_data: str, date_range: str, analysis_options: List[str] = None, user_question: str = "") -> str:
        """Yeni gelişmiş prompt sistemi ile analiz prompt'u oluştur"""
        
        # Yeni prompt sistemini import et
        from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
        
        # Varsayılan analiz seçenekleri
        if analysis_options is None:
            analysis_options = [
                "🎯 Yönetici Özeti",
                "📊 Performans Karnesi", 
                "🔍 Kök Neden Analizi",
                "📈 Zaman Trendleri ve Risk Tahmini",
                "💡 SMART Eylem Planı",
                "📌 Yönetici Aksiyon Panosu"
            ]
        
        # Analiz seçeneklerini formatla
        formatted_options = "\n".join([f"✅ {option}" for option in analysis_options])
        
        # Yeni prompt template'ini kullan
        user_prompt = USER_PROMPT_TEMPLATE.format(
            data_summary=summary_data,
            analysis_options=formatted_options,
            user_question=user_question if user_question else "Yok"
        )
        
        # System prompt + User prompt kombinasyonu
        full_prompt = f"{SYSTEM_PROMPT}\n\n{user_prompt}"
        
        return full_prompt

    def _call_llm_api(self, prompt: str) -> Dict:
        """Seçili sağlayıcıya göre API çağrısı"""

        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=self.max_tokens,
                    temperature=0.8,
                    top_p=0.95,
                    frequency_penalty=0.6,
                    presence_penalty=0.6,
                )
                analysis_text = response.choices[0].message.content
                token_usage = {
                    'prompt_tokens': getattr(response.usage, 'prompt_tokens', None),
                    'completion_tokens': getattr(response.usage, 'completion_tokens', None),
                    'total_tokens': getattr(response.usage, 'total_tokens', None),
                }

            elif self.provider == "anthropic":
                # Claude Messages API
                url = "https://api.anthropic.com/v1/messages"
                headers = {
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                }
                payload = {
                    "model": self.model,
                    "max_tokens": self.max_tokens,
                    "temperature": 0.8,
                    "messages": [{"role": "user", "content": prompt}]
                }
                r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
                r.raise_for_status()
                data = r.json()
                # Claude yanıtı
                parts = data.get("content", [])
                analysis_text = "".join([p.get("text", "") for p in parts]) if isinstance(parts, list) else data.get("content", "")
                token_usage = data.get("usage", {})

            elif self.provider == "xai":
                # xAI Grok (OpenAI uyumlu style olabilir; burada basit REST örneği)
                base = "https://api.x.ai/v1"
                url = f"{base}/chat/completions"
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": self.max_tokens,
                    "temperature": 0.8
                }
                r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
                r.raise_for_status()
                data = r.json()
                analysis_text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                token_usage = data.get("usage", {})

            else:
                raise ValueError(f"Desteklenmeyen sağlayıcı: {self.provider}")

            structured_analysis = self._parse_analysis_response(analysis_text)
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
            'trend_analizi': '',
            'yüzde_kontrol': []
        }
        
        # Basit parsing (regex ile bölümleri ayır)
        current_section = None
        lines = response_text.split('\n')
        
        total_percent_accumulator: List[int] = []
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
        
            # Basit yüzde tutarlılık yakalama (örn: "%15")
            try:
                import re as _re
                matches = _re.findall(r"%(\d{1,3})", line.replace('％','%'))
                if matches:
                    total_percent_accumulator.extend([int(m) for m in matches])
            except Exception:
                pass
        
        # Normalize/tutarlılık notu
        if total_percent_accumulator:
            total = sum([p for p in total_percent_accumulator if 0 <= p <= 100])
            sections['yüzde_kontrol'].append(f"Yüzde toplamı (ham): %{total}")
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
