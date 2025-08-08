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
    def __init__(self, api_key: str = "", provider: str = "openai", model: Optional[str] = None, base_url: Optional[str] = None,
                 max_tokens: Optional[int] = None, temperature: Optional[float] = None):
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

        # Model ve jenerasyon ayarları
        self.model = model or MODEL_NAME
        self.max_tokens = int(max_tokens if max_tokens is not None else MAX_TOKENS)
        self.temperature = float(temperature if temperature is not None else TEMPERATURE)
        
        # Çimento fabrikası spesifik context
        self.cement_context = self._load_cement_context()

        # Sağlayıcıya göre tahmini bağlam limitleri (token)
        self._context_limits = {
            "openai": 128000,
            "anthropic": 200000,
            "xai": 131072
        }

    def _approx_tokens(self, text: str) -> int:
        """Basit yaklaşık token hesabı (karakter/4)."""
        if not text:
            return 0
        return max(1, int(len(text) / 4))

    def _auto_adjust_generation_params(self, prompt: str, data_rows: int) -> None:
        """Satır sayısı ve prompt uzunluğuna göre max_tokens/sıcaklık ayarı yap."""
        # Bağlam limiti ve güvenli boşluk (%20 buffer)
        limit = self._context_limits.get(self.provider, 128000)
        prompt_tokens = self._approx_tokens(prompt)
        safe_room = int(limit * 0.8) - prompt_tokens
        safe_room = max(512, safe_room)

        # Satır bazlı hedef (çok uzun raporlar için)
        if data_rows < 1000:
            row_target = 4000
        elif data_rows < 5000:
            row_target = 8000
        elif data_rows < 15000:
            row_target = 12000
        else:
            row_target = 16000

        requested = self.max_tokens
        target = max(requested, row_target)
        # Üst sınır ve güvenli bağlam kısıtı
        target = min(target, safe_room, 20000)
        self.max_tokens = max(512, int(target))

        # Çok büyük veri için sıcaklığı bir miktar aşağı çek (tutarlılık)
        if data_rows >= 5000:
            self.temperature = min(self.temperature, 0.6)
        
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

        # Token/sıcaklık otomatik ayarı
        try:
            data_rows = int(len(data)) if data is not None else 0
        except Exception:
            data_rows = 0
        self._auto_adjust_generation_params(prompt, data_rows)
        
        # AI analizi çağır
        analysis = self._call_llm_api(prompt)
        
        return analysis

    def _summarize_data(self, data: pd.DataFrame) -> str:
        """Veriyi zengin şekilde özetleyip AI'a güçlü bağlam sağla (KPI + trend + top listeler).

        Ayrıca bazı dağılımları önceden hesaplayıp yüzde toplamını %100'e normalize eder.
        """

        lines: List[str] = []

        def _clean_count_series(series: pd.Series) -> pd.Series:
            """Kategori sayımları için metin serisini temizle.
            - Boş / NaN / None / Null / N/A / NA / NaT / '-' gibi değerleri çıkar
            - Aşırı boşlukları normalize et
            """
            try:
                s = series.astype(str).str.strip()
                # Lower-case kopya ile null benzerlerini tespit et
                s_lower = s.str.lower()
                null_like = [
                    '', 'nan', 'none', 'null', 'nat', 'n/a', 'na', 'n\\a', 'n.a', 'n.a.', '-', '--', '—', 'yok', 'bilinmiyor'
                ]
                mask = s_lower.isin(null_like)
                s = s[~mask]
                # Tek karakterlik anlamsız değerleri filtrele (örn: '.')
                s = s[s.str.len() >= 2]
                # Whitespace normalizasyonu
                s = s.str.replace(r"\s+", " ", regex=True)
                return s
            except Exception:
                return series.dropna()

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

        # Güncellik dağılımı: son 90/180/365 gün ve 24+ ay önceki kayıt sayıları
        if date_col_candidates:
            try:
                dc = date_col_candidates[0]
                dates = pd.to_datetime(data[dc], errors='coerce')
                now = pd.Timestamp.now(tz=None).normalize()
                last90 = (dates >= now - pd.Timedelta(days=90)).sum()
                last180 = (dates >= now - pd.Timedelta(days=180)).sum()
                last365 = (dates >= now - pd.Timedelta(days=365)).sum()
                older24m = (dates < now - pd.Timedelta(days=730)).sum()
                lines.append("- Güncellik (kayıt adedi): son 90g=%d | 180g=%d | 365g=%d | 24+ ay=%d" % (int(last90), int(last180), int(last365), int(older24m)))
                if older24m and last365 == 0:
                    lines.append("- Not: Kayıtların çoğu 24+ ay öncesi. Eylem planı üretimi sınırlı tutulacaktır.")
            except Exception:
                pass

        # Vardiya dağılımı (normalize + örnekleme hatalarına dayanıklı)
        shift_col = next((c for c in data.columns if 'vardiya' in c.lower()), None)
        if shift_col is not None:
            try:
                vc = _clean_count_series(data[shift_col]).value_counts()
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
                vc = _clean_count_series(data[equipment_col]).value_counts()
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
                vc = _clean_count_series(data[issue_col]).str.lower().value_counts()
                lines.append("\n⚠️ SORUN KATEGORİLERİ (ilk 10, normalize):")
                dist = _normalized_percentages(vc, top_n=10)
                for name, cnt, pct in dist:
                    lines.append(f"- {name}: {cnt} kayıt (%{pct})")
                if vc.sum() > 0:
                    lines.append("Toplam = %100")
            except Exception:
                pass

        # Duruş/Süre (dakika) + MTBF/MTTR hesaplamasına uygunluk
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
                # MTBF/MTTR için veri uygunluk sinyali (örnek: tarih/başlangıç-bitiş yoksa hesaplama yapılmaz)
                lines.append("- MTBF/MTTR: veri varsa hesaplanır; eksikse 'veri yok' yaz")

                # Haftalık ortalama duruş süresi (son 7 gün vs önceki 7 gün)
                if date_col_candidates:
                    try:
                        dc = date_col_candidates[0]
                        dates = pd.to_datetime(data[dc], errors='coerce')
                        df_tmp = pd.DataFrame({
                            'date': dates.dt.normalize(),
                            'dur_min': durations
                        })
                        now_d = pd.Timestamp.now().normalize()
                        last7_mask = df_tmp['date'] >= (now_d - pd.Timedelta(days=7))
                        prev7_mask = (df_tmp['date'] < (now_d - pd.Timedelta(days=7))) & (df_tmp['date'] >= (now_d - pd.Timedelta(days=14)))
                        mean_last7 = df_tmp.loc[last7_mask, 'dur_min'].dropna().mean()
                        mean_prev7 = df_tmp.loc[prev7_mask, 'dur_min'].dropna().mean()
                        if pd.notna(mean_prev7) or pd.notna(mean_last7):
                            last7_text = f"{mean_last7:.1f} dk" if pd.notna(mean_last7) else "veri yok"
                            prev7_text = f"{mean_prev7:.1f} dk" if pd.notna(mean_prev7) else "veri yok"
                            lines.append("- Haftalık ortalama (dk/kayıt): geçen hafta = %s | bu hafta = %s" % (prev7_text, last7_text))
                    except Exception:
                        pass
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
        
        # Çıktı kısıtları (halüsinasyon önleme + uzunluk kontrolü)
        constraints = f"""
\n---\n
🔒 ÇIKTI KISITLARI (Kesin Uyman Gerekir)
- Maksimum yanıt uzunluğu: {self.max_tokens} token (gereksiz tekrar, uzun alıntı yok)
- Veri dışı iddia üretme; belirsizse "veri yok" de
- Finansal rakam, TL/USD/₺, ROI vb. UYDURMA; geçerse kaldır
- Dış link, resim/grafik embed etme; düz metin ve gerekirse ASCII tablo
- Yüzdeler Toplam = %100 (±1), aksi durumda normalleştir ve belirt
 - Eylem Planı bölümlerinde placeholder/boş satır kullanma ("...", "devam eden öneriler" vb. YASAK)
  - Eylem Planı öneri adedi dinamik; sadece son 12 ayda yinelenen/etkisi süren sorunlara aksiyon üret. 24+ ay önceki münferit olaylara aksiyon yazma; gerekiyorsa "tarih eski — doğrulama/izleme" notu ekle.
  - Eylem formatı: [Öneri] – Dayanak veri (N/%, süre, tarih aralığı) – Sorumlu – Başarı metriği – Öncelik(1-10) – Zorluk(Kolay/Orta/Zor) – Süre
 - Yönetici Özetinde 8-15 kritik bulgu; gerekiyorsa daha fazla. Sırala: frekans, süre ve etki.
"""

        # System prompt + User prompt + kısıtlar
        full_prompt = f"{SYSTEM_PROMPT}\n\n{user_prompt}\n{constraints}"
        
        return full_prompt

    def _call_llm_api(self, prompt: str) -> Dict:
        """Seçili sağlayıcıya göre API çağrısı"""

        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                    top_p=0.9,
                    frequency_penalty=0.7,
                    presence_penalty=0.4,
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
                    "temperature": self.temperature,
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
                    "temperature": self.temperature
                }
                r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
                r.raise_for_status()
                data = r.json()
                analysis_text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                token_usage = data.get("usage", {})

            else:
                raise ValueError(f"Desteklenmeyen sağlayıcı: {self.provider}")

            analysis_text = self._sanitize_response(analysis_text)
            structured_analysis = self._parse_analysis_response(analysis_text)
            return {
                'analysis': structured_analysis,
                'raw_response': analysis_text,
                'token_usage': token_usage,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            # max_tokens/context hatasında otomatik düşür ve yeniden dene
            msg = str(e).lower()
            if any(k in msg for k in ["max_token", "context", "too many tokens", "reduce"]):
                try:
                    new_max = max(512, int(self.max_tokens * 0.75))
                    if new_max == self.max_tokens:
                        new_max = max(512, self.max_tokens - 512)
                    self.max_tokens = new_max
                    return self._call_llm_api(prompt)
                except Exception:
                    pass
            return {
                'error': f"AI analizi hatası: {str(e)}",
                'analysis': None,
                'token_usage': None,
                'timestamp': datetime.now().isoformat()
            }

    def _sanitize_response(self, text: str) -> str:
        """Basit halüsinasyon ve biçim temizliği: para/URL kaldır, aşırı uzunluğu kes."""
        if not text:
            return text
        try:
            # URL'ler
            text = re.sub(r"https?://\S+", "", text)
            # Para birimleri
            text = re.sub(r"(\₺|\$|USD|TL|TRY|EUR|€)", "", text, flags=re.IGNORECASE)
            # Yinelenen boş satırları sadeleştir
            text = re.sub(r"\n{3,}", "\n\n", text)
            # Yüzde %0 sorunlarını çöz
            text = re.sub(r"\(%\s*0\s*\)", "(≈%<1)", text)
            text = re.sub(r"%\s*0\b", "≈%<1", text)
            text = re.sub(r"(\d+)\s*\(\s*%\s*0\s*\)", r"\1 (≈%<1)", text)
            # Placeholder X/Y saat|dk -> veri yok
            text = re.sub(r"=\s*[XYxy]\s*(saat|dk|dakika)", "= veri yok", text)
            text = re.sub(r"\b[XYxy]\s*(saat|dk|dakika)\b", "veri yok", text)
            # Dayanak veri temizliği - daha kapsamlı
            text = re.sub(r"(?i)Dayanak\s*veri\s*:\s*(N/?A|NA|N\.A\.?|NONE|null|eksik|yok|boş)\b", "Dayanak veri: veri yok", text)
            text = re.sub(r"(?i)Dayanak\s*veri\s*:\s*veri\s*yok\s*—", "Dayanak veri: veri yok —", text)
            # Çok uzun Dayanak veri satırlarını kısalt
            text = re.sub(r"(?i)(Dayanak\s*veri\s*:\s*veri\s*yok)[\s—]*([^—]*—[^—]*—[^—]*—[^—]*—[^—]*)", r"\1 — \2", text)
            # Eylem planı alan adlarında bozulma: '-soru-' tekrarlarını düzelt
            text = re.sub(r"(?i)(?:[\-—]\s*soru\s*){2,}", " — Sorumlu — ", text)
            text = re.sub(r"(?i)(?<=[-—])\s*soru\s*(?=[-—])", " Sorumlu ", text)
            # Satır limiti (çok uzun raporları sınırlı tut)
            lines = text.splitlines()
            new_lines = []
            for line in lines:
                # MTBF/MTTR yer tutucu/uygunsuz değerleri bastır
                if re.search(r"\bMTBF\b|\bMTTR\b", line, flags=re.IGNORECASE):
                    # Sayı var mı? X/Y/N/A/NA/dash varsa veri yok kabul et
                    if not re.search(r"\d", line) or re.search(r"\b(X|Y|N/?A)\b|--|—", line, flags=re.IGNORECASE):
                        line = re.sub(r":.*$", ": veri yok (zaman damgalı arıza/onarım verisi eksik)", line)
                new_lines.append(line)
            if len(new_lines) > 4000:
                new_lines = new_lines[:4000] + ["... [çıktı kısaltıldı]"]
            text = "\n".join(new_lines)
            # Karakter üst limiti
            if len(text) > 120000:
                text = text[:120000] + "\n... [çıktı kısaltıldı]"
            return text
        except Exception:
            return text

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
