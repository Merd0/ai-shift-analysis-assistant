#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Akıllı Üretim Günlüğü - GUI Arayüzü
KVKK uyumlu Excel analiz sistemi için kullanıcı dostu arayüz
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import os
from datetime import datetime, timedelta
import threading
from excel_analyzer import ExcelAnalyzer, KVKKDataCleaner

class VardiyaGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🤖 Akıllı Üretim Günlüğü Asistanı")
        self.window.geometry("1000x700")
        self.window.configure(bg='#f0f0f0')
        
        # Analyzer'ı başlat
        self.analyzer = ExcelAnalyzer()
        self.current_data = None
        self.analysis_results = None
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        """Stil ayarları"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Özel stiller
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f0f0f0')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), background='#f0f0f0')
        style.configure('Info.TLabel', font=('Arial', 10), background='#f0f0f0')
        
    def create_widgets(self):
        """Ana widget'ları oluştur"""
        # Ana başlık
        title_frame = tk.Frame(self.window, bg='#f0f0f0', pady=10)
        title_frame.pack(fill='x')
        
        title_label = ttk.Label(title_frame, text="🤖 Akıllı Üretim Günlüğü Asistanı", 
                               style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="KVKK Uyumlu Vardiya Analiz Sistemi", 
                                  style='Info.TLabel')
        subtitle_label.pack()
        
        # Notebook (sekmeler)
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Sekmeler
        self.create_file_analysis_tab()
        self.create_date_filter_tab()
        self.create_ai_analysis_tab()
        self.create_reports_tab()
        
    def create_file_analysis_tab(self):
        """Dosya analizi sekmesi"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📁 Dosya Analizi")
        
        # Dosya seçimi
        file_frame = ttk.LabelFrame(frame, text="Excel Dosyası Seç", padding=10)
        file_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(file_frame, text="📂 Excel Dosyası Seç", 
                  command=self.select_file).pack(side='left', padx=5)
        
        self.file_label = ttk.Label(file_frame, text="Dosya seçilmedi", style='Info.TLabel')
        self.file_label.pack(side='left', padx=10)
        
        # KVKK uyumluluk
        kvkk_frame = ttk.LabelFrame(frame, text="🔒 KVKK Uyumluluk", padding=10)
        kvkk_frame.pack(fill='x', padx=10, pady=5)
        
        self.kvkk_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(kvkk_frame, text="Kişisel verileri otomatik temizle", 
                       variable=self.kvkk_var).pack(anchor='w')
        
        ttk.Label(kvkk_frame, text="• İsim, telefon, TC no gibi kişisel veriler kaldırılır", 
                 style='Info.TLabel').pack(anchor='w', padx=20)
        ttk.Label(kvkk_frame, text="• Sadece işle ilgili veriler analiz edilir", 
                 style='Info.TLabel').pack(anchor='w', padx=20)
        
        # Analiz butonu
        ttk.Button(frame, text="🔍 Dosyayı Analiz Et", 
                  command=self.analyze_file).pack(pady=10)
        
        # Sonuç alanı
        result_frame = ttk.LabelFrame(frame, text="📊 Analiz Sonuçları", padding=10)
        result_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=15, width=80)
        self.result_text.pack(fill='both', expand=True)
        
    def create_date_filter_tab(self):
        """Tarih filtreleme sekmesi"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📅 Tarih Filtresi")
        
        # Tarih seçimi
        date_frame = ttk.LabelFrame(frame, text="Analiz Dönemi Seç", padding=10)
        date_frame.pack(fill='x', padx=10, pady=5)
        
        self.date_options = {
            "Son 1 gün": 1,
            "Son 7 gün": 7,
            "Son 30 gün": 30,
            "Son 60 gün": 60,
            "Son 90 gün": 90,
            "Son 180 gün": 180,
            "Tüm veriler": 0,
            "Özel tarih aralığı": "custom"
        }
        
        self.date_var = tk.StringVar(value="Son 30 gün")
        
        for option in self.date_options.keys():
            ttk.Radiobutton(date_frame, text=option, variable=self.date_var, 
                           value=option).pack(anchor='w')
        
        # Özel tarih aralığı
        custom_frame = ttk.LabelFrame(frame, text="Özel Tarih Aralığı", padding=10)
        custom_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(custom_frame, text="Başlangıç (YYYY-MM-DD):").grid(row=0, column=0, sticky='w', padx=5)
        self.start_date_entry = ttk.Entry(custom_frame, width=15)
        self.start_date_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(custom_frame, text="Bitiş (YYYY-MM-DD):").grid(row=1, column=0, sticky='w', padx=5)
        self.end_date_entry = ttk.Entry(custom_frame, width=15)
        self.end_date_entry.grid(row=1, column=1, padx=5)
        
        # Filtreleme butonu
        ttk.Button(frame, text="📊 Tarihe Göre Filtrele", 
                  command=self.apply_date_filter).pack(pady=10)
        
        # Filtrelenmiş veri özeti
        summary_frame = ttk.LabelFrame(frame, text="📈 Veri Özeti", padding=10)
        summary_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.summary_text = scrolledtext.ScrolledText(summary_frame, height=10, width=80)
        self.summary_text.pack(fill='both', expand=True)
        
    def create_ai_analysis_tab(self):
        """AI analizi sekmesi"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🤖 AI Analizi")
        
        # API ayarları
        api_frame = ttk.LabelFrame(frame, text="🔑 OpenAI API Ayarları", padding=10)
        api_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(api_frame, text="API Key:").grid(row=0, column=0, sticky='w')
        self.api_key_entry = ttk.Entry(api_frame, width=50, show='*')
        self.api_key_entry.grid(row=0, column=1, padx=5, sticky='ew')
        
        ttk.Label(api_frame, text="Model:").grid(row=1, column=0, sticky='w')
        self.model_var = tk.StringVar(value="gpt-4o-mini")
        model_combo = ttk.Combobox(api_frame, textvariable=self.model_var, 
                                  values=["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"])
        model_combo.grid(row=1, column=1, padx=5, sticky='w')
        
        api_frame.columnconfigure(1, weight=1)
        
        # Analiz seçenekleri
        options_frame = ttk.LabelFrame(frame, text="📋 Analiz Seçenekleri", padding=10)
        options_frame.pack(fill='x', padx=10, pady=5)
        
        self.analysis_options = {
            'genel_ozet': tk.BooleanVar(value=True),
            'sorun_analizi': tk.BooleanVar(value=True),
            'cozum_onerileri': tk.BooleanVar(value=True),
            'trend_analizi': tk.BooleanVar(value=True),
            'performans_metrikleri': tk.BooleanVar(value=False)
        }
        
        option_labels = {
            'genel_ozet': '📊 Genel Özet',
            'sorun_analizi': '⚠️ Sorun Analizi',
            'cozum_onerileri': '💡 Çözüm Önerileri',
            'trend_analizi': '📈 Trend Analizi',
            'performans_metrikleri': '🎯 Performans Metrikleri'
        }
        
        for key, var in self.analysis_options.items():
            ttk.Checkbutton(options_frame, text=option_labels[key], 
                           variable=var).pack(anchor='w')
        
        # AI analizi butonu
        ttk.Button(frame, text="🤖 AI Analizi Başlat", 
                  command=self.start_ai_analysis).pack(pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(frame, mode='indeterminate')
        self.progress.pack(fill='x', padx=10, pady=5)
        
        # AI analiz sonuçları
        ai_result_frame = ttk.LabelFrame(frame, text="🤖 AI Analiz Sonuçları", padding=10)
        ai_result_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.ai_result_text = scrolledtext.ScrolledText(ai_result_frame, height=15, width=80)
        self.ai_result_text.pack(fill='both', expand=True)
        
    def create_reports_tab(self):
        """Raporlar sekmesi"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📄 Raporlar")
        
        # Rapor seçenekleri
        report_frame = ttk.LabelFrame(frame, text="📋 Rapor Türü", padding=10)
        report_frame.pack(fill='x', padx=10, pady=5)
        
        self.report_type = tk.StringVar(value="detayli")
        
        ttk.Radiobutton(report_frame, text="📊 Detaylı Rapor", 
                       variable=self.report_type, value="detayli").pack(anchor='w')
        ttk.Radiobutton(report_frame, text="📈 Özet Rapor", 
                       variable=self.report_type, value="ozet").pack(anchor='w')
        ttk.Radiobutton(report_frame, text="📉 Sorun Odaklı Rapor", 
                       variable=self.report_type, value="sorun").pack(anchor='w')
        
        # Export seçenekleri
        export_frame = ttk.LabelFrame(frame, text="💾 Export Seçenekleri", padding=10)
        export_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(export_frame, text="📄 PDF Rapor Oluştur", 
                  command=self.export_pdf).pack(side='left', padx=5)
        ttk.Button(export_frame, text="📊 Excel Rapor Oluştur", 
                  command=self.export_excel).pack(side='left', padx=5)
        ttk.Button(export_frame, text="📝 Word Rapor Oluştur", 
                  command=self.export_word).pack(side='left', padx=5)
        
        # Rapor önizleme
        preview_frame = ttk.LabelFrame(frame, text="👁️ Rapor Önizleme", padding=10)
        preview_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.report_preview = scrolledtext.ScrolledText(preview_frame, height=20, width=80)
        self.report_preview.pack(fill='both', expand=True)
        
    def select_file(self):
        """Excel dosyası seç"""
        file_path = filedialog.askopenfilename(
            title="Excel Dosyası Seç",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        
        if file_path:
            self.current_file = file_path
            self.file_label.config(text=os.path.basename(file_path))
            
    def analyze_file(self):
        """Seçilen dosyayı analiz et"""
        if not hasattr(self, 'current_file'):
            messagebox.showerror("Hata", "Lütfen önce bir Excel dosyası seçin!")
            return
        
        try:
            # Progress göster
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "🔍 Dosya analiz ediliyor...\n\n")
            self.window.update()
            
            # Dosyayı analiz et
            self.analysis_results = self.analyzer.analyze_excel_file(self.current_file)
            
            if 'hata' in self.analysis_results:
                messagebox.showerror("Hata", f"Analiz hatası: {self.analysis_results['hata']}")
                return
            
            # Sonuçları göster
            self.display_analysis_results()
            
            # Temizlenmiş veriyi sakla
            self.current_data = self.analysis_results.get('temiz_veri')
            
        except Exception as e:
            messagebox.showerror("Hata", f"Beklenmeyen hata: {str(e)}")
    
    def display_analysis_results(self):
        """Analiz sonuçlarını göster"""
        results = self.analysis_results
        text = []
        
        text.append("🎉 ANALİZ TAMAMLANDI!\n")
        text.append("=" * 50 + "\n\n")
        
        # Temel bilgiler
        basic = results.get('temel_bilgiler', {})
        text.append(f"📁 Dosya: {basic.get('dosya_adi', 'N/A')}\n")
        text.append(f"📊 Boyut: {basic.get('dosya_boyutu', 'N/A')}\n")
        text.append(f"📈 Satır sayısı: {basic.get('satir_sayisi', 0):,}\n")
        text.append(f"📋 Orijinal kolon sayısı: {basic.get('kolon_sayisi', 0)}\n\n")
        
        # KVKK temizlik
        kvkk = results.get('kvkk_temizlik', {})
        text.append("🔒 KVKK UYUMLULUK:\n")
        if kvkk.get('kaldirilan_kolonlar'):
            text.append(f"   ❌ Kaldırılan kolonlar: {', '.join(kvkk['kaldirilan_kolonlar'])}\n")
        else:
            text.append("   ✅ Kişisel veri tespit edilmedi\n")
        text.append(f"   📊 Temiz kolon sayısı: {kvkk.get('temiz_kolon_sayisi', 0)}\n\n")
        
        # Tarih kolonları
        date_cols = results.get('tarih_kolonlari', [])
        if date_cols:
            text.append(f"📅 Tarih kolonları: {', '.join(date_cols)}\n\n")
        
        # Temiz kolonlar
        clean_cols = kvkk.get('temiz_kolonlar', [])
        text.append("📋 ANALİZ İÇİN HAZIR KOLONLAR:\n")
        for i, col in enumerate(clean_cols, 1):
            text.append(f"   {i}. {col}\n")
        
        text.append("\n✅ Veri AI analizi için hazır!\n")
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "".join(text))
    
    def apply_date_filter(self):
        """Tarih filtresini uygula"""
        if self.current_data is None:
            messagebox.showwarning("Uyarı", "Önce bir dosya analiz edin!")
            return
        
        # Tarih aralığını hesapla
        selected = self.date_var.get()
        
        if selected == "Özel tarih aralığı":
            try:
                start_date = datetime.strptime(self.start_date_entry.get(), "%Y-%m-%d")
                end_date = datetime.strptime(self.end_date_entry.get(), "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Hata", "Geçersiz tarih formatı! YYYY-MM-DD kullanın.")
                return
        elif selected == "Tüm veriler":
            start_date = None
            end_date = None
        else:
            days = self.date_options[selected]
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
        
        # Filtreleme uygula
        filtered_data = self.filter_data_by_date(self.current_data, start_date, end_date)
        
        # Özet göster
        self.show_filtered_summary(filtered_data, start_date, end_date)
    
    def filter_data_by_date(self, df, start_date, end_date):
        """Veriyi tarihe göre filtrele"""
        if start_date is None or end_date is None:
            return df
        
        # Tarih kolonunu bul
        date_columns = self.analysis_results.get('tarih_kolonlari', [])
        if not date_columns:
            return df
        
        date_col = date_columns[0]  # İlk tarih kolonunu kullan
        
        try:
            df_copy = df.copy()
            df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')
            
            # Filtreleme
            mask = (df_copy[date_col] >= start_date) & (df_copy[date_col] <= end_date)
            return df_copy[mask]
            
        except Exception as e:
            messagebox.showerror("Hata", f"Tarih filtreleme hatası: {str(e)}")
            return df
    
    def show_filtered_summary(self, filtered_df, start_date, end_date):
        """Filtrelenmiş veri özetini göster"""
        summary = []
        
        if start_date and end_date:
            summary.append(f"📅 Tarih Aralığı: {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}\n")
        else:
            summary.append("📅 Tarih Aralığı: Tüm veriler\n")
        
        summary.append(f"📊 Toplam kayıt: {len(filtered_df):,}\n")
        summary.append(f"📈 Orijinal kayıt: {len(self.current_data):,}\n")
        summary.append(f"📉 Filtrelenen kayıt: {len(self.current_data) - len(filtered_df):,}\n\n")
        
        # Kolon bazında özet
        summary.append("📋 KOLON ÖZETİ:\n")
        for col in filtered_df.columns:
            non_null = filtered_df[col].count()
            unique_vals = filtered_df[col].nunique()
            summary.append(f"   • {col}: {non_null:,} değer, {unique_vals:,} benzersiz\n")
        
        summary.append("\n✅ Filtrelenmiş veri AI analizi için hazır!")
        
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, "".join(summary))
        
        # Filtrelenmiş veriyi güncelle
        self.filtered_data = filtered_df
    
    def start_ai_analysis(self):
        """AI analizini başlat"""
        if not hasattr(self, 'filtered_data') and self.current_data is None:
            messagebox.showwarning("Uyarı", "Önce veri yükleyin ve filtreleyin!")
            return
        
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showerror("Hata", "Lütfen OpenAI API key'ini girin!")
            return
        
        # Analizi thread'de çalıştır
        self.progress.start()
        self.ai_result_text.delete(1.0, tk.END)
        self.ai_result_text.insert(tk.END, "🤖 AI analizi başlatılıyor...\n\n")
        
        threading.Thread(target=self.run_ai_analysis, args=(api_key,), daemon=True).start()
    
    def run_ai_analysis(self, api_key):
        """AI analizini çalıştır (thread'de)"""
        try:
            import openai
            
            # OpenAI client'ı ayarla
            client = openai.OpenAI(api_key=api_key)
            
            # Analiz edilecek veriyi hazırla
            data_to_analyze = getattr(self, 'filtered_data', self.current_data)
            
            # Seçili analiz türlerini al
            selected_analyses = [key for key, var in self.analysis_options.items() if var.get()]
            
            # AI prompt'unu oluştur
            prompt = self.create_ai_prompt(data_to_analyze, selected_analyses)
            
            # AI'ya gönder
            response = client.chat.completions.create(
                model=self.model_var.get(),
                messages=[
                    {"role": "system", "content": "Sen bir üretim analisti uzmanısın. Vardiya verilerini analiz edip detaylı raporlar hazırlarsın."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Sonucu GUI'de göster
            result = response.choices[0].message.content
            self.window.after(0, self.display_ai_result, result)
            
        except Exception as e:
            self.window.after(0, self.display_ai_error, str(e))
        finally:
            self.window.after(0, self.progress.stop)
    
    def create_ai_prompt(self, data, selected_analyses):
        """AI için prompt oluştur"""
        data_sample = data.head(20).to_string()  # İlk 20 satırı örnek olarak al
        
        prompt = f"""
Vardiya verileri analizi yapılacak. Aşağıdaki veriler SoftExpert sisteminden alınmıştır:

VERİ ÖRNEĞİ:
{data_sample}

TOPLAM KAYIT SAYISI: {len(data)}

Lütfen aşağıdaki analizleri yap:
"""
        
        if 'genel_ozet' in selected_analyses:
            prompt += "\n1. GENEL ÖZET: Verilerin genel durumu, ana bulgular"
        
        if 'sorun_analizi' in selected_analyses:
            prompt += "\n2. SORUN ANALİZİ: Tespit edilen problemler, sık yaşanan durumlar"
        
        if 'cozum_onerileri' in selected_analyses:
            prompt += "\n3. ÇÖZÜM ÖNERİLERİ: Sorunlar için pratik çözüm önerileri"
        
        if 'trend_analizi' in selected_analyses:
            prompt += "\n4. TREND ANALİZİ: Zaman içindeki değişimler, eğilimler"
        
        if 'performans_metrikleri' in selected_analyses:
            prompt += "\n5. PERFORMANS METRİKLERİ: Sayısal göstergeler, KPI'lar"
        
        prompt += """

RAPOR FORMATI:
- Türkçe yazın
- Madde madde düzenleyin  
- Sayısal verilerle destekleyin
- Eylem planları önerin
- Yönetici raporu formatında yazın
"""
        
        return prompt
    
    def display_ai_result(self, result):
        """AI sonucunu göster"""
        self.ai_result_text.delete(1.0, tk.END)
        self.ai_result_text.insert(tk.END, f"🤖 AI ANALİZ SONUCU\n{'='*50}\n\n{result}")
        
        # Rapor önizlemesine de kopyala
        self.report_preview.delete(1.0, tk.END)
        self.report_preview.insert(tk.END, result)
    
    def display_ai_error(self, error):
        """AI hatasını göster"""
        self.ai_result_text.delete(1.0, tk.END)
        self.ai_result_text.insert(tk.END, f"❌ AI Analiz Hatası:\n\n{error}")
        messagebox.showerror("AI Hatası", f"AI analizi başarısız: {error}")
    
    def export_pdf(self):
        """PDF rapor export et"""
        messagebox.showinfo("Bilgi", "PDF export özelliği geliştirilecek!")
    
    def export_excel(self):
        """Excel rapor export et"""
        if not hasattr(self, 'filtered_data') and self.current_data is None:
            messagebox.showwarning("Uyarı", "Export edilecek veri yok!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Excel Rapor Kaydet",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                data_to_export = getattr(self, 'filtered_data', self.current_data)
                data_to_export.to_excel(file_path, index=False)
                messagebox.showinfo("Başarılı", f"Rapor kaydedildi: {file_path}")
            except Exception as e:
                messagebox.showerror("Hata", f"Export hatası: {str(e)}")
    
    def export_word(self):
        """Word rapor export et"""
        messagebox.showinfo("Bilgi", "Word export özelliği geliştirilecek!")
    
    def run(self):
        """Uygulamayı çalıştır"""
        self.window.mainloop()

def main():
    """Ana fonksiyon"""
    app = VardiyaGUI()
    app.run()

if __name__ == "__main__":
    main()
