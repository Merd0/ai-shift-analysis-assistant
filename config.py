# OpenAI API Configuration
# GÜVENLİK: API key'ler kodda saklanmaz; kullanıcı GUI'de girer
OPENAI_API_KEY = ""  # Boş - güvenlik için

# Varsayılan model ayarları (OpenAI)
MODEL_NAME = "gpt-4o-mini"
MAX_TOKENS = 6000
TEMPERATURE = 0.7

# Dil
LANGUAGE = "Turkish"

# Sağlayıcı ve model listeleri (GUI ve analiz tarafından kullanılır)
# Not: Gerçek erişim, ilgili sağlayıcının hesabında yetkilendirilen modellere bağlıdır
PROVIDERS = {
    "openai": {
        "label": "OpenAI",
        "models": [
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-4.1",
            "gpt-5"  # Hesabında varsa
        ]
    },
    "anthropic": {
        "label": "Anthropic Claude",
        "models": [
            "claude-3-5-sonnet-20240620",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307"
        ]
    },
    "xai": {
        "label": "xAI Grok",
        "models": [
            "grok-2",
            "grok-beta"
        ],
        "base_url": "https://api.x.ai/v1"
    }
}

DEFAULT_PROVIDER = "openai"

# GÜVENLİK NOTU:
# Bu dosyada API key tutulmaz. Kullanıcı GUI'de sağlayıcıya uygun key'i girer.
