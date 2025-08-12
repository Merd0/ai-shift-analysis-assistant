# OpenAI API Configuration
# Amaç: Varsayılan model/parametre ve sağlayıcı listelerini merkezî konfig ile yönetmek
# GÜVENLİK: API key'ler kodda saklanmaz; kullanıcı GUI'de girer (runtime'da bellek içi tutulur)
OPENAI_API_KEY = ""  # Boş - güvenlik için

# Varsayılan model ayarları (OpenAI)
# Not: GUI/AI katmanı bu varsayılanları override edebilir (kullanıcı tercihi)
MODEL_NAME = "gpt-4o-mini"
MAX_TOKENS = 12000
TEMPERATURE = 0.7

# Dil
LANGUAGE = "Turkish"

# Sağlayıcı ve model listeleri (GUI ve analiz tarafından kullanılır)
# Not: Gerçek erişim, ilgili sağlayıcının hesabında yetkilendirilen modellere bağlıdır
#      Bu liste UI tarafında combobox doldurma ve doğrulama amaçlıdır
# 🚀 ENHANCED PROVIDER LIST - Performance & Cost Ratings
# Her model tam performans ile çalışır (maliyet uyarı sistemi aktif)
PROVIDERS = {
    "openai": {
        "label": "OpenAI",
        "models": [
            {
                "name": "gpt-4o-mini",
                "label": "GPT-4o Mini", 
                "performance": "🏆 EXCELLENT",
                "cost": "💰 LOW",
                "speed": "⚡ FAST",
                "quality": "📊 HIGH",
                "recommended": True,
                "cost_level": "low",
                "notes": "✅ Test sonucu: En iyi token efficiency, tam yanıtlar"
            },
            {
                "name": "gpt-4o",
                "label": "GPT-4o",
                "performance": "🥇 VERY GOOD", 
                "cost": "💰💰 MEDIUM",
                "speed": "⚡ FAST",
                "quality": "📊 VERY HIGH",
                "recommended": True,
                "cost_level": "medium",
                "notes": "✅ Dengeli seçim, orta maliyet"
            },

            {
                "name": "gpt-3.5-turbo", 
                "label": "GPT-3.5 Turbo",
                "performance": "🥉 GOOD",
                "cost": "💰 VERY LOW",
                "speed": "⚡⚡ VERY FAST", 
                "quality": "📊 MEDIUM",
                "recommended": False,
                "cost_level": "very_low",
                "notes": "💡 Hızlı test için, kalite düşük"
            }
        ]
    },
    "anthropic": {
        "label": "Anthropic Claude",
        "models": [
            {
                "name": "claude-3-5-sonnet-20240620",
                "label": "Claude 3.5 Sonnet",
                "performance": "🏆 EXCELLENT",
                "cost": "💰💰 MEDIUM",
                "speed": "⚡ FAST", 
                "quality": "📊 VERY HIGH",
                "recommended": True,
                "cost_level": "medium",
                "notes": "✅ Alternatif olarak test edilebilir"
            },
            {
                "name": "claude-3-opus-20240229",
                "label": "Claude 3 Opus",
                "performance": "🥇 VERY GOOD",
                "cost": "💰💰💰 HIGH",
                "speed": "🐌 SLOW",
                "quality": "📊 EXCELLENT", 
                "recommended": False,
                "cost_level": "high",
                "notes": "⚠️ Pahalı, yavaş"
            },
            {
                "name": "claude-3-sonnet-20240229", 
                "label": "Claude 3 Sonnet",
                "performance": "🥈 GOOD",
                "cost": "💰💰 MEDIUM",
                "speed": "⚡ FAST",
                "quality": "📊 HIGH",
                "recommended": True,
                "cost_level": "medium",
                "notes": "✅ Dengeli performans"
            },
            {
                "name": "claude-3-haiku-20240307",
                "label": "Claude 3 Haiku", 
                "performance": "🥉 GOOD",
                "cost": "💰 LOW",
                "speed": "⚡⚡ VERY FAST",
                "quality": "📊 MEDIUM",
                "recommended": False,
                "cost_level": "low",
                "notes": "💡 Hızlı test için"
            }
        ]
    },
    "xai": {
        "label": "xAI Grok",
        "models": [
            {
                "name": "grok-2",
                "label": "Grok-2",
                "performance": "❓ UNTESTED", 
                "cost": "💰💰 MEDIUM",
                "speed": "❓ UNKNOWN",
                "quality": "❓ UNKNOWN",
                "recommended": False,
                "cost_level": "medium",
                "notes": "⚠️ Henüz test edilmedi"
            },
            {
                "name": "grok-beta",
                "label": "Grok Beta",
                "performance": "❓ UNTESTED",
                "cost": "💰💰 MEDIUM", 
                "speed": "❓ UNKNOWN",
                "quality": "❓ UNKNOWN",
                "recommended": False,
                "cost_level": "medium",
                "notes": "⚠️ Beta versiyon, kararsız"
            }
        ],
        "base_url": "https://api.x.ai/v1"
    }
}

DEFAULT_PROVIDER = "openai"  # GUI açılışında seçili sağlayıcı

# 💡 COST WARNING SYSTEM - Helper functions
def get_model_info(provider: str, model_name: str) -> dict:
    """Model bilgilerini getir"""
    try:
        provider_data = PROVIDERS.get(provider, {})
        models = provider_data.get("models", [])
        
        for model in models:
            if isinstance(model, dict) and model.get("name") == model_name:
                return model
            elif isinstance(model, str) and model == model_name:
                # Backward compatibility - old format
                return {"name": model_name, "label": model_name, "cost_level": "unknown"}
        
        return {"name": model_name, "label": model_name, "cost_level": "unknown"}
    except Exception:
        return {"name": model_name, "label": model_name, "cost_level": "unknown"}

def should_show_cost_warning(provider: str, model_name: str) -> tuple[bool, str]:
    """Maliyet uyarısı gösterilmeli mi?"""
    model_info = get_model_info(provider, model_name)
    cost_level = model_info.get("cost_level", "unknown")
    
    if cost_level == "high":
        return True, f"⚠️ YÜKSEK MALİYET UYARISI\n\n'{model_info.get('label', model_name)}' modeli yüksek token maliyetlerine sahiptir.\n\n{model_info.get('notes', '')}\n\nDevam etmek istiyor musunuz?"
    elif cost_level == "medium" and not model_info.get("recommended", False):
        return True, f"💰 MALİYET BİLGİSİ\n\n'{model_info.get('label', model_name)}' modeli orta düzey token maliyetlerine sahiptir.\n\n{model_info.get('notes', '')}\n\nDevam etmek istiyor musunuz?"
    
    return False, ""

def get_recommended_models() -> list:
    """Önerilen modelleri getir"""
    recommended = []
    for provider_key, provider_data in PROVIDERS.items():
        models = provider_data.get("models", [])
        for model in models:
            if isinstance(model, dict) and model.get("recommended", False):
                recommended.append({
                    "provider": provider_key,
                    "model": model["name"],
                    "label": f"{provider_data['label']} - {model['label']}",
                    "performance": model.get("performance", ""),
                    "cost": model.get("cost", ""),
                    "notes": model.get("notes", "")
                })
    return recommended

# GÜVENLİK NOTU:
# Bu dosyada API key tutulmaz. Kullanıcı GUI'de sağlayıcıya uygun key'i girer.
# Çevresel değişkenler üzerinden okuma tercih edilecekse, GUI tarafında ele alınmalıdır.
