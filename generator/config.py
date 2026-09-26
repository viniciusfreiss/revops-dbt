from datetime import date

# Semente fixa. Rodar o gerador duas vezes produz exatamente os mesmos dados.
SEED = 42

# Período simulado
START_DATE = date(2026, 1, 1)
END_DATE = date(2026, 6, 30)

# Quantidade de pessoas que visitam o portal ou o app
N_VISITORS = 20_000

# Parte das pessoas que chegam pelo app (o resto chega pela web)
APP_SHARE = 0.4

# Número máximo de sessões antes do cadastro
MAX_SESSIONS = 6

# Intervalo médio, em dias, entre uma sessão e a próxima
MEAN_DAYS_BETWEEN_SESSIONS = 3

# Para cada canal
#   arrival_weight  peso do canal na origem das sessões
#   signup_prob     chance de uma sessão desse canal terminar em cadastro
CHANNELS = {
    "google":   {"arrival_weight": 0.25, "signup_prob": 0.030},
    "meta":     {"arrival_weight": 0.25, "signup_prob": 0.015},
    "tiktok":   {"arrival_weight": 0.10, "signup_prob": 0.008},
    "linkedin": {"arrival_weight": 0.05, "signup_prob": 0.040},
    "bing":     {"arrival_weight": 0.05, "signup_prob": 0.020},
    "organic":  {"arrival_weight": 0.15, "signup_prob": 0.025},
    "direct":   {"arrival_weight": 0.15, "signup_prob": 0.035},
}

# Campanhas de cada canal pago. O id vira o utm_campaign dos eventos
# e o campaign_id da tabela de mídia.
CAMPAIGNS = {
    "google":   ["ggl_search_marca", "ggl_search_renda_fixa", "ggl_pmax"],
    "meta":     ["meta_prospeccao", "meta_remarketing"],
    "tiktok":   ["ttk_awareness"],
    "linkedin": ["lnk_investidor_qualificado"],
    "bing":     ["bing_search_renda_fixa"],
}

# utm_medium de cada canal pago
PAID_MEDIUM = {
    "google": "cpc",
    "bing": "cpc",
    "meta": "paid_social",
    "tiktok": "paid_social",
    "linkedin": "paid_social",
}

# Produtos da esteira. Os mesmos ids vão para o seed de produtos no dbt.
PRODUCTS = ["cri_imob_01", "cra_agro_01", "deb_infra_01", "ccb_empresa_01"]

# Navegação dentro de uma sessão
MAX_EXTRA_EVENTS_PER_SESSION = 4   # eventos além do primeiro page_viewed
PRODUCT_VIEW_SHARE = 0.3           # parte desses eventos que é visualização de produto

# Funil de KYC depois do cadastro
KYC_SUBMIT_RATE = 0.75     # cadastrados que enviam o KYC
KYC_APPROVAL_RATE = 0.85   # enviados que são aprovados