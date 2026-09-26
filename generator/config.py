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

# Métricas de entrega de cada canal pago
#   cpc                 custo médio por clique, em BRL
#   ctr                 cliques divididos por impressões
#   click_to_session    parte dos cliques que vira sessão registrada no Segment
AD_METRICS = {
    "google":   {"cpc": 3.50,  "ctr": 0.045, "click_to_session": 0.85},
    "meta":     {"cpc": 1.40,  "ctr": 0.012, "click_to_session": 0.70},
    "tiktok":   {"cpc": 0.80,  "ctr": 0.008, "click_to_session": 0.60},
    "linkedin": {"cpc": 12.00, "ctr": 0.006, "click_to_session": 0.80},
    "bing":     {"cpc": 2.50,  "ctr": 0.040, "click_to_session": 0.85},
}

# Ciclos de deal depois do KYC aprovado
MAX_DEALS_PER_USER = 4           # cada deal é um produto diferente
MAX_SESSIONS_PER_DEAL = 4        # sessões antes da simulação de cada deal
WIN_RATE_FIRST_DEAL = 0.45       # chance de o primeiro deal virar aporte
WIN_RATE_REPEAT_DEAL = 0.60      # chance dos deals seguintes
REPEAT_AFTER_WIN = 0.35          # chance de abrir outro deal depois de um ganho
REPEAT_AFTER_LOSS = 0.20         # chance de abrir outro deal depois de uma perda
MEAN_DAYS_BETWEEN_DEALS = 30

# Valor do aporte segue uma lognormal (mediana em BRL e dispersão)
INVESTMENT_MEDIAN = 15_000
INVESTMENT_SIGMA = 0.9
INVESTMENT_MIN = 1_000

# Canais das sessões depois do cadastro (o usuário já conhece a marca)
RETURN_CHANNELS = {
    "direct": 0.35,
    "meta": 0.25,
    "google": 0.15,
    "organic": 0.15,
    "linkedin": 0.05,
    "bing": 0.03,
    "tiktok": 0.02,
}