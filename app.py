import streamlit as st
import pandas as pd
import numpy as np
import os
import json
import textwrap

# ---------------------------------------------------------
# PERSISTÊNCIA DE DADOS EM ARQUIVO LOCAL (JSON) E PASTAS
# ---------------------------------------------------------
ARQUIVO_PRODUTOS = os.path.join("arquivos", "produtos.json")
ARQUIVO_CFG      = os.path.join("arquivos", "configuracoes.json")
DIR_RELATORIOS   = os.path.join("arquivos", "Relatórios")

def garantir_estrutura_pastas():
    """Garante que a árvore completa de pastas para Vendas e Ads exista no disco."""
    tipos = ['Vendas', 'Ads']
    anos = ['2025', '2026', '2027']
    meses = ['01-Janeiro', '02-Fevereiro', '03-Março', '04-Abril', '05-Maio', '06-Junho', '07-Julho', '08-Agosto', '09-Setembro', '10-Outubro', '11-Novembro', '12-Dezembro']
    plataformas = ['Shopee', 'TikTok', 'Shein', 'Mercado Livre']
    for t in tipos:
        for a in anos:
            for m in meses:
                for p in plataformas:
                    pasta = os.path.join(DIR_RELATORIOS, t, a, m, p)
                    os.makedirs(pasta, exist_ok=True)

garantir_estrutura_pastas()

def carregar_produtos_disco(produtos_padrao):
    if os.path.exists(ARQUIVO_PRODUTOS):
        try:
            with open(ARQUIVO_PRODUTOS, "r", encoding="utf-8") as f:
                dados = json.load(f)
                if isinstance(dados, list) and len(dados) > 0:
                    return dados
        except Exception:
            pass
    salvar_produtos_disco(produtos_padrao)
    return produtos_padrao

def salvar_produtos_disco(lista_produtos):
    try:
        os.makedirs("arquivos", exist_ok=True)
        with open(ARQUIVO_PRODUTOS, "w", encoding="utf-8") as f:
            json.dump(lista_produtos, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Erro ao salvar produtos: {e}")
        return False

PERFIS_PRESETS_PADRAO = {
    "Simples Nacional (~10%)": {"aliquota": 10.0, "roas": 8.0},
    "MEI (4%)":              {"aliquota": 4.0,  "roas": 8.0},
    "MEI Zero (0%)":         {"aliquota": 0.0,  "roas": 10.0},
    "Personalizado":         {"aliquota": 10.0, "roas": 8.0},
}

def carregar_config_disco():
    defaults_cfg = {
        "perfil_fiscal": "Simples Nacional (~10%)",
        "aliquota_simples_perc": 10.0,
        "roas_meta": 8.0,
        "perfis_custom": PERFIS_PRESETS_PADRAO.copy()
    }
    if os.path.exists(ARQUIVO_CFG):
        try:
            with open(ARQUIVO_CFG, "r", encoding="utf-8") as f:
                dados = json.load(f)
                if isinstance(dados, dict):
                    defaults_cfg.update(dados)
                    if "perfis_custom" not in defaults_cfg:
                        defaults_cfg["perfis_custom"] = PERFIS_PRESETS_PADRAO.copy()
                    return defaults_cfg
        except Exception:
            pass
    salvar_config_disco(defaults_cfg)
    return defaults_cfg

def salvar_config_disco(cfg_dict):
    try:
        os.makedirs("arquivos", exist_ok=True)
        with open(ARQUIVO_CFG, "w", encoding="utf-8") as f:
            json.dump(cfg_dict, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Erro ao salvar configuracoes: {e}")
        return False





# ---------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="ORION Enterprise — Dualis Lingerie",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@500;600;700;800&display=swap');

    header[data-testid="stHeader"], .stAppHeader {
        background: transparent !important;
        background-color: transparent !important;
    }
    .stApp {
        background: linear-gradient(180deg, #050811 0%, #0B101D 50%, #060912 100%) !important;
        color: #F8FAFC !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    }
    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="base-input"],
    div[data-testid="stNumberInput"] input, div[data-testid="stTextInput"] input,
    input, textarea, select {
        background-color: #101625 !important;
        color: #FFFFFF !important;
        border: 1px solid #1E293B !important;
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stDataFrame"], div[data-testid="stDataEditor"],
    div[role="grid"], div[role="row"], div[role="gridcell"], iframe {
        background-color: #101625 !important;
        color-scheme: dark !important;
    }
    table, th, td {
        background-color: #101625 !important;
        color: #F8FAFC !important;
        border-color: #1E293B !important;
    }
    ul[data-baseweb="menu"], div[data-baseweb="popover"], div[data-baseweb="menu"] {
        background-color: #101625 !important;
        color: #FFFFFF !important;
        border: 1px solid #1E293B !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.7) !important;
    }
    li[data-baseweb="option"] { background-color: #101625 !important; color: #CBD5E1 !important; }
    li[data-baseweb="option"]:hover, li[aria-selected="true"] {
        background-color: #1E293B !important; color: #38BDF8 !important;
    }
    div[data-testid="stExpander"], div[data-testid="stForm"] {
        background-color: #101625 !important;
        border: 1px solid #1E293B !important;
        border-radius: 14px !important;
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #101625 0%, #0B101D 100%) !important;
        border: 1px solid #1E293B !important;
        padding: 16px 20px !important;
        border-radius: 12px !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #94A3B8 !important; font-weight: 700 !important;
        font-size: 0.85rem !important; text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    div[data-testid="stMetricValue"] {
        color: #38BDF8 !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
    }
    .stAlert {
        background-color: #101625 !important;
        border: 1px solid #1E293B !important;
        color: #F8FAFC !important;
        border-radius: 12px !important;
    }
    .badge-pill {
        display: inline-block; padding: 5px 14px; border-radius: 20px;
        font-weight: 800; font-size: 0.88rem;
    }
    .badge-green { background-color: rgba(52,211,153,0.15); color: #34D399; border: 1px solid #34D399; }
    .badge-yellow { background-color: rgba(251,191,36,0.15); color: #FBBF24; border: 1px solid #FBBF24; }
    .badge-red { background-color: rgba(248,113,113,0.15); color: #F87171; border: 1px solid #F87171; }
    .orion-card {
        background: linear-gradient(135deg, #101625 0%, #0B101D 100%);
        border: 1px solid #1E293B; border-radius: 14px; padding: 22px;
        margin-bottom: 16px; box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .orion-card:hover { border-color: #38BDF8; transform: translateY(-2px); }
    .card-label { color: #94A3B8; font-size: 0.82rem; text-transform: uppercase; font-weight: 700; letter-spacing: 0.6px; }
    .card-value { color: #FFFFFF; font-family: 'Outfit', sans-serif; font-size: 1.85rem; font-weight: 800; margin-top: 6px; }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px; background-color: #0E1424; padding: 8px 14px;
        border-radius: 14px; border: 1px solid #1E293B;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px; border-radius: 10px; color: #94A3B8; font-weight: 700; padding: 0 18px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E293B !important; color: #38BDF8 !important;
        border-bottom: 2px solid #38BDF8 !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070B14 0%, #050810 50%, #080D18 100%) !important;
        border-right: 1px solid rgba(56,189,248,0.12) !important;
    }
    [data-testid="stSidebar"] > div:first-child { padding-top: 1.5rem !important; }
    div[data-testid="stSidebar"] div.stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #0E1526 0%, #0B101D 100%) !important;
        color: #94A3B8 !important; border: 1px solid #1E293B !important;
        border-radius: 12px !important; padding: 12px 16px !important;
        text-align: left !important; display: flex !important;
        justify-content: flex-start !important; align-items: center !important;
        font-family: 'Inter', sans-serif !important; font-weight: 600 !important;
        font-size: 0.9rem !important; transition: all 0.2s ease-in-out !important;
        margin-bottom: 6px !important;
    }
    div[data-testid="stSidebar"] div.stButton > button:hover {
        background: linear-gradient(135deg, #162035 0%, #10172A 100%) !important;
        color: #F8FAFC !important; border-color: rgba(56,189,248,0.4) !important;
        transform: translateX(4px) !important;
    }
    div[data-testid="stSidebar"] div.stButton > button[kind="primary"],
    div[data-testid="stSidebar"] div.stButton > button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(90deg, rgba(56,189,248,0.18) 0%, rgba(14,21,38,0.95) 100%) !important;
        color: #38BDF8 !important; border: 1px solid #38BDF8 !important;
        box-shadow: 0 4px 15px rgba(56,189,248,0.2), inset 4px 0 0 0 #38BDF8 !important;
        font-weight: 700 !important;
    }
    /* DESIGN DOS BOXES CLICÁVEIS DE PRODUTO (Estilo Cards de Métricas Orion) */
    div[data-testid="stMainBlockContainer"] div.stButton > button[kind="primary"],
    div[data-testid="stMainBlockContainer"] div.stButton > button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #0F172A 0%, #080D1A 100%) !important;
        border: 1px solid #1E293B !important;
        border-left: 4px solid #38BDF8 !important;
        border-radius: 12px !important;
        color: #F8FAFC !important;
        padding: 14px 20px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        text-align: left !important;
        display: flex !important;
        justify-content: flex-start !important;
        align-items: center !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
        transition: all 0.2s ease-in-out !important;
        margin-bottom: 8px !important;
    }
    div[data-testid="stMainBlockContainer"] div.stButton > button[kind="primary"]:hover,
    div[data-testid="stMainBlockContainer"] div.stButton > button[data-testid="stBaseButton-primary"]:hover {
        background: linear-gradient(135deg, #162035 0%, #10172A 100%) !important;
        border-color: #38BDF8 !important;
        box-shadow: 0 0 20px rgba(56,189,248,0.25), 0 6px 20px rgba(0,0,0,0.4) !important;
        transform: translateY(-2px) translateX(4px) !important;
        color: #38BDF8 !important;
    }
    .alert-critical {
        background: linear-gradient(135deg, rgba(248,113,113,0.12) 0%, rgba(15,10,18,0.9) 100%);
        border: 1px solid rgba(248,113,113,0.4); border-left: 4px solid #F87171;
        border-radius: 12px; padding: 14px 18px; margin-bottom: 10px;
        color: #F8FAFC;
    }
    .alert-warning {
        background: linear-gradient(135deg, rgba(251,191,36,0.12) 0%, rgba(15,10,18,0.9) 100%);
        border: 1px solid rgba(251,191,36,0.4); border-left: 4px solid #FBBF24;
        border-radius: 12px; padding: 14px 18px; margin-bottom: 10px;
        color: #F8FAFC;
    }
    .canal-card {
        background: linear-gradient(135deg, #0E1526 0%, #0B1020 100%);
        border: 1px solid #1E293B; border-radius: 16px; padding: 20px 22px;
        height: 100%;
    }
    .periodo-badge {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border: 1px solid #334155; border-radius: 14px; padding: 14px 20px;
        margin-bottom: 20px;
    }
    /* RESPONSIVE METRIC CARDS & FLEXBOX WRAPPING */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #0F172A 0%, #080D1A 100%) !important;
        border: 1px solid #1E293B !important;
        border-radius: 12px !important;
        padding: 12px 14px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
        transition: transform 0.2s ease, border-color 0.2s ease !important;
    }
    div[data-testid="stMetric"]:hover {
        border-color: #38BDF8 !important;
        transform: translateY(-2px) !important;
    }
    /* LINHA DE PRODUTO COMPACTA E ELEGANTE */
    .prod-row-box {
        background: linear-gradient(90deg, #0E1526 0%, #080D1A 100%);
        border: 1px solid #1E293B;
        border-left: 4px solid #38BDF8;
        border-radius: 12px;
        padding: 12px 18px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.25);
    }
    .prod-row-box:hover {
        border-color: #38BDF8;
        box-shadow: 0 0 20px rgba(56,189,248,0.2), 0 6px 20px rgba(0,0,0,0.4);
        transform: translateX(4px);
    }
    .neon-pill {
        display: inline-flex; align-items: center; gap: 5px;
        padding: 4px 10px; border-radius: 20px;
        font-size: 0.72rem; font-weight: 700; text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .neon-pill-cyan { background: rgba(56,189,248,0.12); color: #38BDF8; border: 1px solid rgba(56,189,248,0.3); }
    .neon-pill-purple { background: rgba(168,85,247,0.12); color: #C084FC; border: 1px solid rgba(168,85,247,0.3); }
    .neon-pill-emerald { background: rgba(52,211,153,0.12); color: #34D399; border: 1px solid rgba(52,211,153,0.3); }
    .neon-pill-amber { background: rgba(251,191,36,0.12); color: #FBBF24; border: 1px solid rgba(251,191,36,0.3); }
    .neon-metric-box {
        background: rgba(15,23,42,0.6);
        border: 1px solid rgba(30,41,59,0.8);
        border-radius: 10px;
        padding: 8px 12px;
        text-align: center;
    }
    div[data-testid="stMetricLabel"] {
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        color: #94A3B8 !important;
        white-space: normal !important;
        word-wrap: break-word !important;
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.25rem !important;
        font-weight: 800 !important;
        color: #38BDF8 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    div[data-testid="stColumn"] {
        min-width: 150px !important;
    }
</style>
""", unsafe_allow_html=True)

def render_kpi_cards(cards):
    """
    Renders a responsive flexbox grid of KPI metric cards that adapts automatically to any screen size.
    """
    items = []
    for c in cards:
        lbl = c.get("label", "")
        val = c.get("value", "")
        sub = c.get("sub", "")
        color = c.get("color", "#38BDF8")
        sub_html = f'<div style="color:{color};font-size:0.75rem;font-weight:700;margin-top:4px">{sub}</div>' if sub else ""
        card_html = (
            f'<div style="flex:1 1 170px;min-width:145px;background:linear-gradient(135deg,#0F172A 0%,#080D1A 100%);'
            f'border:1px solid #1E293B;border-radius:12px;padding:14px 16px;box-shadow:0 6px 18px rgba(0,0,0,.35);">'
            f'<div style="color:#94A3B8;font-size:0.78rem;font-weight:700;font-family:\'Outfit\',sans-serif;margin-bottom:6px">{lbl}</div>'
            f'<div style="color:{color};font-size:1.25rem;font-weight:800;font-family:\'Outfit\',sans-serif;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{val}</div>'
            f'{sub_html}'
            f'</div>'
        )
        items.append(card_html)
    container_html = f'<div style="display:flex;flex-wrap:wrap;gap:12px;margin-bottom:20px;width:100%">{"".join(items)}</div>'
    st.markdown(container_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# DADOS BASE E SESSION STATE
# ---------------------------------------------------------
PRODUTOS_PADRAO = [
    {"id": 1, "nome": "Calcinha Gestante",   "custo_unitario": 3.65, "custo_embalagem": 0.30, "categoria": "Lingerie Gestante",    "sku": "GEST-01", "fornecedor": "Confecção Própria", "peso_g": 80,  "observacoes": "Algodão antialérgico com cós elástico anatômico"},
    {"id": 2, "nome": "Calcinha Pala Dupla", "custo_unitario": 3.90, "custo_embalagem": 0.30, "categoria": "Lingerie / Underwear", "sku": "PALA-02", "fornecedor": "Confecção Própria", "peso_g": 75,  "observacoes": "Pala dupla de alta sustentação"},
    {"id": 3, "nome": "Cinta Cos Baixo",     "custo_unitario": 5.50, "custo_embalagem": 0.30, "categoria": "Cintas & Modeladores", "sku": "CINT-03", "fornecedor": "Confecção Própria", "peso_g": 120, "observacoes": "Cós baixo com compressão média"},
    {"id": 4, "nome": "Cinta Cos Alto",      "custo_unitario": 7.80, "custo_embalagem": 0.30, "categoria": "Cintas & Modeladores", "sku": "CINT-04", "fornecedor": "Confecção Própria", "peso_g": 150, "observacoes": "Cós alto compressão forte com barbatanas"},
    {"id": 5, "nome": "Galena",              "custo_unitario": 6.00, "custo_embalagem": 0.30, "categoria": "Lingerie / Underwear", "sku": "GAL-05",  "fornecedor": "Confecção Própria", "peso_g": 90,  "observacoes": "Renda Galena de alta durabilidade"},
    {"id": 6, "nome": "Fio dental",          "custo_unitario": 1.00, "custo_embalagem": 0.30, "categoria": "Fio Dental",           "sku": "FIO-06",  "fornecedor": "Confecção Própria", "peso_g": 40,  "observacoes": "Microfibra leve sem costura"},
    {"id": 7, "nome": "Regulagem",           "custo_unitario": 2.10, "custo_embalagem": 0.30, "categoria": "Lingerie / Underwear", "sku": "REG-07",  "fornecedor": "Confecção Própria", "peso_g": 65,  "observacoes": "Alça com regulagem reforçada"},
]

TAXAS_PADRAO = {
    "Shopee":                   {"comissao": 14.0, "programa": 6.0,  "taxa_fixa": 4.00},
    "TikTok Shop":              {"comissao": 10.0, "programa": 0.0,  "taxa_fixa": 4.00},
    "Shein":                    {"comissao": 16.0, "programa": 0.0,  "taxa_fixa": 3.00},
    "Mercado Livre (Classic)":  {"comissao": 12.0, "programa": 0.0,  "taxa_fixa": 6.00},
    "Mercado Livre (Premium)":  {"comissao": 16.5, "programa": 0.0,  "taxa_fixa": 6.00},
}

cfg_salva  = carregar_config_disco()
p_salvo    = cfg_salva.get("perfil_fiscal", "Simples Nacional (~10%)")
aliq_salva = float(cfg_salva.get("aliquota_simples_perc", 10.0))
roas_salvo = float(cfg_salva.get("roas_meta", 8.0))
perf_salvo = cfg_salva.get("perfis_custom", PERFIS_PRESETS_PADRAO.copy())

defaults = {
    "aba":                   "dashboard",
    "produtos":              carregar_produtos_disco(PRODUTOS_PADRAO),
    "presets_taxas":         TAXAS_PADRAO,
    "perfil_fiscal":         p_salvo,
    "aliquota_simples_perc": aliq_salva,
    "roas_meta":             roas_salvo,
    "perfis_custom":         perf_salvo,
    "sb_perfil_sel":         p_salvo,
    "sb_aliq_input":         aliq_salva,
    "sb_roas_input":         roas_salvo,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------------------------------------------------
# CARREGAMENTO DE DADOS
# ---------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_upseller():
    pasta = os.path.join("arquivos", "Relatorios", "relatorio de vendas", "Upseller")
    fallbacks = [
        os.path.join("arquivos", "Relatórios", "relatório de vendas", "Upseller"),
        pasta,
    ]
    for p in fallbacks:
        if not os.path.exists(p):
            continue
        files = [f for f in os.listdir(p) if f.endswith(".xlsx")]
        if not files:
            continue
        try:
            df = pd.read_excel(os.path.join(p, files[0]))
            for col in ["Valor de Vendas", "Preco Medio", "Preço Médio"]:
                if col in df.columns:
                    df[col] = pd.to_numeric(
                        df[col].astype(str).str.replace(",", "."), errors="coerce"
                    ).fillna(0.0)
            for col in ["Unidades Vendidas", "Pedidos Validos", "Pedidos Válidos"]:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
            # Normalize column names
            col_map = {}
            for c in df.columns:
                nc = c.strip()
                if "Pedidos" in nc and "lid" in nc:
                    col_map[c] = "Pedidos Válidos"
                elif "Unidades" in nc:
                    col_map[c] = "Unidades Vendidas"
                elif "Valor" in nc and "Venda" in nc:
                    col_map[c] = "Valor de Vendas"
                elif "Preco" in nc or "Preço" in nc:
                    col_map[c] = "Preço Médio"
                elif "Produto" in nc:
                    col_map[c] = "Produtos"
                elif "SKU" in nc and "Principal" in nc:
                    col_map[c] = "SKU Principal"
                elif "Loja" in nc or "Canal" in nc or "Plataforma" in nc:
                    col_map[c] = "Loja"
            df = df.rename(columns=col_map)
            for need in ["Pedidos Válidos", "Unidades Vendidas", "Valor de Vendas", "Preço Médio", "Produtos", "Loja"]:
                if need not in df.columns:
                    df[need] = 0 if "Pedidos" in need or "Unidades" in need else (0.0 if "Valor" in need or "Preço" in need else "")
            return df
        except Exception:
            continue
    return None

@st.cache_data(show_spinner=False)
def load_shopee_anuncios():
    paths = [
        os.path.join("arquivos", "Anuncios", "anuncios shopee.xlsx"),
        os.path.join("arquivos", "Anúncios", "anuncios shopee.xlsx"),
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                return pd.read_excel(path)
            except Exception:
                continue
    return None

@st.cache_data(show_spinner=False)
def load_shopee_ads():
    import glob, io
    pastas = [
        os.path.join("arquivos", "Relatórios", "ads", "shopee"),
        os.path.join("arquivos", "Relatorios", "ads", "shopee"),
        os.path.join("arquivos", "Anuncios"),
    ]
    for pasta in pastas:
        if not os.path.exists(pasta):
            continue
        files = glob.glob(os.path.join(pasta, "*.csv"))
        files = sorted(files, key=os.path.getmtime, reverse=True)
        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8-sig", errors="ignore") as fp:
                    lines = fp.readlines()
                header_idx = None
                for idx, l in enumerate(lines):
                    if any(term in l for term in ["Nome do Anúncio", "Nome do Anncio", "Anúncio / Nome do Produto", "Anncia / Nome do Produto", "Impressões", "Impresses"]):
                        header_idx = idx
                        break
                if header_idx is not None:
                    df = pd.read_csv(io.StringIO("".join(lines[header_idx:])))
                    if len(df) > 0:
                        if "Anúncio / Nome do Produto" in df.columns:
                            df.rename(columns={"Anúncio / Nome do Produto": "Nome do Anúncio"}, inplace=True)
                        elif "Anncia / Nome do Produto" in df.columns:
                            df.rename(columns={"Anncia / Nome do Produto": "Nome do Anúncio"}, inplace=True)

                        num_cols = ["GMV", "Despesas", "Itens Vendidos", "Conversões", "Cliques", "Impressões"]
                        for c in num_cols:
                            if c in df.columns:
                                df[c] = pd.to_numeric(df[c].astype(str).str.replace(",", "."), errors="coerce").fillna(0)
                        return df
            except Exception:
                continue
    return None

@st.cache_data(show_spinner=False)
def load_tiktok_ads():
    import glob
    pasta = os.path.join("arquivos", "Relatórios", "ads", "tik tok")
    if not os.path.exists(pasta):
        pasta = os.path.join("arquivos", "Relatorios", "ads", "tik tok")
    if not os.path.exists(pasta):
        return None
    files = glob.glob(os.path.join(pasta, "*.xlsx")) + glob.glob(os.path.join(pasta, "*.csv"))
    if not files:
        return None
    file_path = sorted(files, key=os.path.getmtime, reverse=True)[0]
    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        for c in ["Custo", "Receita bruta (Loja atual)", "Pedidos de SKU (loja atual)", "ROI (loja atual)"]:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c].astype(str).str.replace(",", "."), errors="coerce").fillna(0)
        return df
    except Exception:
        return None

@st.cache_data(show_spinner=False)
def load_shopee_orders():
    import glob
    pastas = [
        os.path.join("arquivos", "Relatórios", "relatório de vendas", "shopee"),
        os.path.join("arquivos", "Relatorios", "relatorio de vendas", "shopee"),
    ]
    for pasta in pastas:
        if not os.path.exists(pasta):
            continue
        files = glob.glob(os.path.join(pasta, "*.xlsx")) + glob.glob(os.path.join(pasta, "*.csv"))
        files = sorted(files, key=os.path.getmtime, reverse=True)
        for f in files:
            try:
                if f.endswith(".csv"):
                    df = pd.read_csv(f)
                else:
                    df = pd.read_excel(f)
                if len(df) > 0:
                    return df, os.path.basename(f), True
                elif len(df) == 0:
                    return None, os.path.basename(f), False
            except Exception:
                continue
    return None, "", False

def parse_money(v):
    if pd.isna(v) or v is None:
        return 0.0
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).replace("BRL", "").replace("R$", "").strip()
    if not s:
        return 0.0
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    return float(pd.to_numeric(s, errors="coerce") or 0.0)

@st.cache_data(show_spinner=False)
def load_vendas_organizadas(ano_filtro="Todos", mes_filtro="Todos", plat_filtro="Todas"):
    import glob
    base_dir = os.path.join("arquivos", "Relatórios", "Vendas")
    if not os.path.exists(base_dir):
        base_dir = os.path.join("arquivos", "Relatorios", "Vendas")
    if not os.path.exists(base_dir):
        return None

    registros = []
    for ano in sorted(os.listdir(base_dir)):
        p_ano = os.path.join(base_dir, ano)
        if not os.path.isdir(p_ano): continue
        if ano_filtro != "Todos" and str(ano) != str(ano_filtro): continue

        for mes in sorted(os.listdir(p_ano)):
            p_mes = os.path.join(p_ano, mes)
            if not os.path.isdir(p_mes): continue
            if mes_filtro != "Todos" and not mes.startswith(str(mes_filtro).split(" ")[0]): continue

            for plat in sorted(os.listdir(p_mes)):
                p_plat = os.path.join(p_mes, plat)
                if not os.path.isdir(p_plat): continue
                if plat_filtro != "Todas" and plat_filtro.lower() not in plat.lower(): continue

                for f in glob.glob(os.path.join(p_plat, "*.*")):
                    if not (f.endswith(".xlsx") or f.endswith(".csv") or f.endswith(".xls")): continue
                    try:
                        df = pd.read_csv(f) if f.endswith(".csv") else pd.read_excel(f)
                        if len(df) == 0: continue

                        cols_map = {str(c).lower().strip(): c for c in df.columns}

                        # Identificar colunas do pedido
                        col_id_ped = cols_map.get("id do pedido") or cols_map.get("order id") or cols_map.get("id pedido")
                        col_prod   = cols_map.get("nome do produto") or cols_map.get("product name") or cols_map.get("produtos") or cols_map.get("produto")
                        col_var    = cols_map.get("nome da variação") or cols_map.get("nome da variao") or cols_map.get("variation") or cols_map.get("variação") or cols_map.get("sku principal")
                        col_qtd    = cols_map.get("quantidade") or cols_map.get("quantity") or cols_map.get("unidades vendidas") or cols_map.get("unidades")
                        col_val    = cols_map.get("valor total") or cols_map.get("order amount") or cols_map.get("sku subtotal after discount") or cols_map.get("valor de vendas")
                        col_stat   = cols_map.get("status do pedido") or cols_map.get("order status") or cols_map.get("status")

                        if col_prod and col_val:
                            for _, r in df.iterrows():
                                qtd_k = int(pd.to_numeric(str(r.get(col_qtd, 1)).replace(",", "."), errors="coerce") or 1)
                                p_nome = str(r.get(col_prod, "Produto"))
                                p_var  = str(r.get(col_var, "Geral")) if col_var else "Geral"
                                mult = get_kit_multiplier(p_nome, p_var)
                                pecas_f = max(qtd_k * mult, 1)

                                # Tratamento financeiro correto com parse_money
                                val_tot = parse_money(r.get(col_val, 0.0))

                                # Repasse líquido: se tiver taxas detalhadas deduz, senão aplica tarifa padrão do canal
                                tax_com = parse_money(r.get("Taxa de comissão líquida", 0.0))
                                tax_srv = parse_money(r.get("Taxa de serviço líquida", 0.0))
                                tax_tx  = parse_money(r.get("Taxa de transação", r.get("Taxa de transaço", 0.0)))

                                if tax_com > 0 or tax_srv > 0 or tax_tx > 0:
                                    rep_real = val_tot - (tax_com + tax_srv + tax_tx)
                                elif "Total global" in df.columns:
                                    rep_real = parse_money(r.get("Total global", val_tot))
                                else:
                                    # Aplicar regra de comissão estimada do canal
                                    com_f, tf_f, _ = taxas_para_preco(plat, val_tot)
                                    rep_real = max(val_tot * (1.0 - com_f / 100.0) - tf_f, 0.0)

                                registros.append({
                                    "Ano": str(ano), "Mês": mes, "Plataforma": plat,
                                    "ID Pedido": str(r.get(col_id_ped, "Pedido")) if col_id_ped else "Pedido",
                                    "Produto": p_nome,
                                    "Variação": p_var,
                                    "Kits Vendidos": qtd_k,
                                    "Peças Físicas": pecas_f,
                                    "Quantidade": pecas_f,
                                    "Valor Total": val_tot,
                                    "Repasse Líquido": rep_real,
                                    "Status": str(r.get(col_stat, "Concluído")) if col_stat else "Concluído",
                                    "Arquivo": os.path.basename(f)
                                })
                        elif "Pedidos Válidos" in df.columns or "Valor de Vendas" in df.columns:
                            col_p = "Produtos" if "Produtos" in df.columns else "Produto"
                            col_sku = "SKU Principal" if "SKU Principal" in df.columns else col_p
                            col_un = "Unidades Vendidas" if "Unidades Vendidas" in df.columns else "Unidades"
                            col_v = "Valor de Vendas" if "Valor de Vendas" in df.columns else "Valor Total"
                            for _, r in df.iterrows():
                                qtd_k = int(r.get(col_un, 1))
                                mult = get_kit_multiplier(r.get(col_p, ""), r.get(col_sku, ""))
                                pecas_f = qtd_k * mult
                                registros.append({
                                    "Ano": ano, "Mês": mes, "Plataforma": plat,
                                    "ID Pedido": "Agrupado",
                                    "Produto": str(r.get(col_p, "Produto")),
                                    "Variação": str(r.get(col_sku, "Geral")),
                                    "Kits Vendidos": qtd_k,
                                    "Peças Físicas": pecas_f,
                                    "Quantidade": pecas_f,
                                    "Valor Total": float(r.get(col_v, 0.0)),
                                    "Repasse Líquido": float(r.get(col_v, 0.0)),
                                    "Status": "Concluído",
                                    "Arquivo": os.path.basename(f)
                                })
                    except Exception:
                        continue

    return pd.DataFrame(registros) if registros else None

@st.cache_data(show_spinner=False)
def load_ads_organizados(ano_filtro="Todos", mes_filtro="Todos", plat_filtro="Todas"):
    import glob, io
    base_dir = os.path.join("arquivos", "Relatórios", "Ads")
    if not os.path.exists(base_dir):
        base_dir = os.path.join("arquivos", "Relatorios", "Ads")
    if not os.path.exists(base_dir):
        return None

    registros = []
    for ano in sorted(os.listdir(base_dir)):
        p_ano = os.path.join(base_dir, ano)
        if not os.path.isdir(p_ano): continue
        if ano_filtro != "Todos" and str(ano) != str(ano_filtro): continue

        for mes in sorted(os.listdir(p_ano)):
            p_mes = os.path.join(p_ano, mes)
            if not os.path.isdir(p_mes): continue
            if mes_filtro != "Todos" and not mes.startswith(str(mes_filtro).split(" ")[0]): continue

            for plat in sorted(os.listdir(p_mes)):
                p_plat = os.path.join(p_mes, plat)
                if not os.path.isdir(p_plat): continue
                if plat_filtro != "Todas" and plat_filtro.lower() not in plat.lower(): continue

                for f in glob.glob(os.path.join(p_plat, "*.*")):
                    if not (f.endswith(".xlsx") or f.endswith(".csv") or f.endswith(".xls")): continue
                    try:
                        if f.endswith(".csv"):
                            with open(f, "r", encoding="utf-8-sig", errors="ignore") as fp:
                                lines = fp.readlines()
                            header_idx = None
                            for idx, l in enumerate(lines):
                                if any(term in l for term in ["Nome do Anúncio", "Nome do Anncio", "Anúncio / Nome do Produto", "Impressões", "Impresses"]):
                                    header_idx = idx
                                    break
                            df = pd.read_csv(io.StringIO("".join(lines[header_idx:]))) if header_idx is not None else pd.read_csv(f)
                        else:
                            df = pd.read_excel(f)
                        if len(df) == 0: continue

                        # Mapeamento flexível de colunas
                        cols_lower = {str(c).lower().strip(): c for c in df.columns}
                        
                        col_anuncio = None
                        for term in ['nome do anúncio', 'nome do anncio', 'anúncio / nome do produto', 'anncia / nome do produto', 'nome da campanha', 'campaign name', 'ad name', 'produto', 'item']:
                            if term in cols_lower:
                                col_anuncio = cols_lower[term]
                                break
                        if not col_anuncio and "por dia" in cols_lower:
                            col_anuncio = cols_lower["por dia"]
                        elif not col_anuncio and len(df.columns) > 0:
                            col_anuncio = df.columns[0]

                        col_desp = None
                        for term in ['despesas', 'despesa', 'custo', 'cost', 'spend', 'investimento', 'valor gasto', 'total cost']:
                            if term in cols_lower:
                                col_desp = cols_lower[term]
                                break

                        col_gmv = None
                        for term in ['gmv', 'receita bruta (loja atual)', 'receita bruta', 'valor de vendas', 'vendas', 'revenue', 'conversion value']:
                            if term in cols_lower:
                                col_gmv = cols_lower[term]
                                break

                        col_conv = None
                        for term in ['conversões', 'conversoes', 'pedidos de sku (loja atual)', 'pedidos de sku', 'pedidos', 'compras', 'itens vendidos', 'total orders']:
                            if term in cols_lower:
                                col_conv = cols_lower[term]
                                break

                        if col_desp:
                            for _, r in df.iterrows():
                                item_nome = str(r.get(col_anuncio, "Campanha")).strip()
                                # Ignorar linhas de totalização ou traços em relatórios diários
                                if item_nome in ["-", "Total", "TOTAL", "Total global", "Média"]:
                                    continue
                                    
                                inv = parse_money(r.get(col_desp, 0.0))
                                fat = parse_money(r.get(col_gmv, 0.0)) if col_gmv else 0.0
                                ped = float(pd.to_numeric(str(r.get(col_conv, 0)).replace(',', '.'), errors='coerce') or 0.0) if col_conv else 0.0
                                
                                if inv > 0 or fat > 0:
                                    registros.append({
                                        'Ano': str(ano), 'Mês': mes, 'Plataforma': plat,
                                        'Anúncio': f"TikTok Ads ({item_nome})" if plat.lower() == "tiktok" and item_nome else item_nome,
                                        'Investimento': inv,
                                        'Faturamento GMV': fat,
                                        'Pedidos': ped,
                                        'ROAS': (fat / inv) if inv > 0 else 0.0,
                                        'Arquivo': os.path.basename(f)
                                    })
                    except Exception:
                        continue

    return pd.DataFrame(registros) if registros else None


vendas_df   = load_upseller()
anuncios_df = load_shopee_anuncios()


# ---------------------------------------------------------
# FUNÇÕES AUXILIARES
# ---------------------------------------------------------
def format_canal(loja_str):
    s = str(loja_str)
    if "Shopee"  in s: return "🟠 Shopee BR"
    if "TikTok"  in s or "tiktok" in s.lower(): return "🎵 TikTok Shop BR"
    if "Mercado" in s: return "📦 Mercado Livre"
    if "Shein"   in s: return "👗 Shein"
    return f"🏪 {s[:30]}"

def filtrar_produto(df, nome_produto):
    if df is None or len(df) == 0:
        return pd.DataFrame()
    palavras = nome_produto.lower().split()
    mask = pd.Series([True] * len(df), index=df.index)
    for p in palavras[:2]:
        if len(p) > 2:
            m_prod = df["Produtos"].astype(str).str.lower().str.contains(p, na=False)
            m_sku  = df.get("SKU Principal", pd.Series([""] * len(df))).astype(str).str.lower().str.contains(p, na=False)
            mask &= (m_prod | m_sku)
    result = df[mask].copy()
    if len(result) == 0:
        first = palavras[0] if palavras else ""
        if len(first) > 2:
            result = df[df["Produtos"].astype(str).str.lower().str.contains(first, na=False)].copy()
    return result

def parse_model(name_str):
    s = str(name_str).upper()
    if 'GESTANTE' in s or 'CG' in s or 'PÓS PARTO' in s or 'POS PARTO' in s or 'HOT PANT' in s:
        return 'Calcinha Gestante & Pós Parto'
    elif 'CINTA' in s or 'REDUTORA' in s or 'GALENA' in s or 'COMPRESS' in s:
        return 'Cintas & Modeladores'
    elif 'FIO' in s or 'REGULAGEM' in s or 'FIO DENTAL' in s:
        return 'Calcinhas Fio Dental'
    elif 'MICROFIBRA' in s or 'CALÇOLA' in s or 'CALCOLA' in s or 'PALA DUPLA' in s or 'SALA' in s or 'DIÁRIO' in s:
        return 'Calcinhas Conforto / Dia a Dia'
    return 'Outros Modelos'

def parse_kit(name_str, var_str):
    s = (str(name_str) + ' ' + str(var_str)).upper()
    if 'KIT 10' in s or '10 PEÇAS' in s or '10X' in s or '10 PECA' in s:
        return 'Kit 10 Peças'
    elif 'KIT 5' in s or '5 PEÇAS' in s or '5X' in s or '5 PECA' in s or 'KIT 3 E 5' in s:
        return 'Kit 5 Peças'
    elif 'KIT 3' in s or '3 PEÇAS' in s or '3X' in s or '3 PECA' in s:
        return 'Kit 3 Peças'
    elif 'KIT 2' in s or '2 PEÇAS' in s or '2X' in s or '2 PECA' in s:
        return 'Kit 2 Peças'
    elif 'KIT' in s:
        return 'Kits Diversos'
    return 'Unidade Avulsa (1x)'

def get_kit_multiplier(name_str, var_str=''):
    s = (str(name_str) + ' ' + str(var_str)).upper()
    if 'KIT 10' in s or '10 PEÇAS' in s or '10X' in s or '10 PECA' in s:
        return 10
    elif 'KIT 5' in s or '5 PEÇAS' in s or '5X' in s or '5 PECA' in s or 'KIT 3 E 5' in s:
        return 5
    elif 'KIT 3' in s or '3 PEÇAS' in s or '3X' in s or '3 PECA' in s:
        return 3
    elif 'KIT 2' in s or '2 PEÇAS' in s or '2X' in s or '2 PECA' in s:
        return 2
    return 1

def parse_size(var_str):
    import re
    s = str(var_str).upper().strip()
    if 'XG' in s or 'EXG' in s or 'XXG' in s or '48' in s or 'PLUS' in s:
        return 'XG'
    elif 'GG' in s:
        return 'GG'
    elif re.search(r'\bG\b', s) or ',G' in s or ', G' in s or 'G,' in s or 'TAMANHO G' in s:
        return 'G'
    elif re.search(r'\bM\b', s) or ',M' in s or ', M' in s or 'M,' in s or 'TAMANHO M' in s:
        return 'M'
    elif re.search(r'\bP\b', s) or ',P' in s or ', P' in s or 'P,' in s or 'TAMANHO P' in s:
        return 'P'
    elif 'ÚNICO' in s or 'UNICO' in s or 'REGULAGEM' in s:
        return 'Tamanho Único'
    return 'XG'

def calcular_preco_sugerido(canal_name, custo_fisico, target_margin_frac, usar_roas=True):
    simples = st.session_state.aliquota_simples_perc / 100.0
    if usar_roas and st.session_state.get("roas_meta", 0) > 0:
        acos = 1.0 / st.session_state.roas_meta
    else:
        acos = 0.0

    if "TikTok" in canal_name:
        com1, tf1 = 0.10, 4.00
        ded1 = com1 + simples + acos
        d1 = 1.0 - ded1 - target_margin_frac
        pv1 = (custo_fisico + tf1) / d1 if d1 > 0 else 0.0
        if 0 < pv1 < 50.0:
            return pv1, 10.0, 4.00, "10.0% + R$4,00 (<R$50)"
        com2, tf2 = 0.06, 6.00
        ded2 = com2 + simples + acos
        d2 = 1.0 - ded2 - target_margin_frac
        pv2 = (custo_fisico + tf2) / d2 if d2 > 0 else 0.0
        return pv2, 6.0, 6.00, "6.0% + R$6,00 (>=R$50)"

    taxas   = st.session_state.presets_taxas.get(canal_name, {"comissao": 14.0, "programa": 0.0, "taxa_fixa": 4.00})
    com_tot = taxas["comissao"] + taxas["programa"]
    tf      = taxas["taxa_fixa"]
    ded     = (com_tot / 100.0) + simples + acos
    d       = 1.0 - ded - target_margin_frac
    pv      = (custo_fisico + tf) / d if d > 0 else 0.0
    return pv, com_tot, tf, f"{com_tot:.1f}% + R${tf:.2f}"

def taxas_para_preco(canal_name, preco):
    if "TikTok" in canal_name:
        if preco >= 50.0:
            return 6.0, 6.00, "TikTok >=R$50 -> 6% + R$6,00"
        return 10.0, 4.00, "TikTok <R$50 -> 10% + R$4,00"
    taxas   = st.session_state.presets_taxas.get(canal_name, {"comissao": 14.0, "programa": 0.0, "taxa_fixa": 4.00})
    com_tot = taxas["comissao"] + taxas["programa"]
    tf      = taxas["taxa_fixa"]
    return com_tot, tf, f"{canal_name}: {com_tot:.1f}% + R${tf:.2f}"

# ---------------------------------------------------------
# CALLBACKS DE FISCAL & ADS NA SIDEBAR
# ---------------------------------------------------------
def cb_mudar_perfil_fiscal():
    p = st.session_state.sb_perfil_sel
    st.session_state.perfil_fiscal = p
    perfis_dict = st.session_state.get("perfis_custom", PERFIS_PRESETS_PADRAO)
    if p in perfis_dict and p != "Personalizado":
        aliq = perfis_dict[p]["aliquota"]
        roas = perfis_dict[p]["roas"]
        st.session_state.aliquota_simples_perc = aliq
        st.session_state.roas_meta = roas
        st.session_state.sb_aliq_input = aliq
        st.session_state.sb_roas_input = roas
    salvar_config_disco({
        "perfil_fiscal": st.session_state.perfil_fiscal,
        "aliquota_simples_perc": float(st.session_state.aliquota_simples_perc),
        "roas_meta": float(st.session_state.roas_meta),
        "perfis_custom": st.session_state.perfis_custom
    })

def cb_mudar_aliq_input():
    val = st.session_state.sb_aliq_input
    st.session_state.aliquota_simples_perc = val
    st.session_state.perfil_fiscal = "Personalizado"
    st.session_state.sb_perfil_sel = "Personalizado"
    salvar_config_disco({
        "perfil_fiscal": "Personalizado",
        "aliquota_simples_perc": float(val),
        "roas_meta": float(st.session_state.roas_meta),
        "perfis_custom": st.session_state.perfis_custom
    })

def cb_mudar_roas_input():
    val = st.session_state.sb_roas_input
    st.session_state.roas_meta = val
    st.session_state.perfil_fiscal = "Personalizado"
    st.session_state.sb_perfil_sel = "Personalizado"
    salvar_config_disco({
        "perfil_fiscal": "Personalizado",
        "aliquota_simples_perc": float(st.session_state.aliquota_simples_perc),
        "roas_meta": float(val),
        "perfis_custom": st.session_state.perfis_custom
    })

# ---------------------------------------------------------
# BARRA LATERAL — 5 BOTÕES DIRETOS
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0F172A,#080D1A);border:1px solid #1E293B;border-radius:14px;padding:18px 16px;margin-bottom:22px;box-shadow:0 10px 25px rgba(0,0,0,.5)">
        <div style="display:flex;align-items:center;gap:14px">
            <div style="background:linear-gradient(135deg,#38BDF8,#0284C7);width:42px;height:42px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.4rem;box-shadow:0 0 18px rgba(56,189,248,.4)">&#128737;</div>
            <div>
                <div style="color:#F8FAFC;font-weight:800;font-size:1.05rem;font-family:'Outfit',sans-serif">ORION ENTERPRISE</div>
                <div style="color:#34D399;font-size:0.72rem;font-weight:600;margin-top:3px">
                    &#9679; Dualis Lingerie
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    abas_config = [
        ("dashboard",     "🏠  Painel Geral"),
        ("catalogo",      "📦  Catálogo de Produtos"),
        ("precificacao",  "🎯  Calculadora & Simulador"),
        ("inteligencia",  "📊  Inteligência Comercial"),
    ]
    abas_util = [
        ("importar",      "📤  Importar Dados"),
        ("configuracoes", "⚙️  Configurações"),
    ]

    for key, label in abas_config:
        btn_type = "primary" if st.session_state.aba == key else "secondary"
        if st.button(label, key=f"nav_{key}", use_container_width=True, type=btn_type):
            st.session_state.aba = key
            st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='border-top:1px solid #1E293B;margin:4px 0 12px 0'></div>", unsafe_allow_html=True)

    for key, label in abas_util:
        btn_type = "primary" if st.session_state.aba == key else "secondary"
        if st.button(label, key=f"nav_{key}", use_container_width=True, type=btn_type):
            st.session_state.aba = key
            st.rerun()

    # ---------------------------------------------------------
    # PAINEL RECOLHÍVEL DE PERFIL FISCAL & ADS (SIDEBAR EXPANDER)
    # ---------------------------------------------------------
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    with st.expander("🏛️ Perfil Fiscal & Ads", expanded=False):
        perfis_dict = st.session_state.perfis_custom
        perfil_opts = list(perfis_dict.keys())

        st.selectbox(
            "Perfil Fiscal Ativo:",
            perfil_opts,
            key="sb_perfil_sel",
            on_change=cb_mudar_perfil_fiscal
        )

        st.number_input(
            "Alíquota Simples (%):",
            min_value=0.0,
            max_value=30.0,
            step=0.5,
            key="sb_aliq_input",
            on_change=cb_mudar_aliq_input
        )

        st.number_input(
            "ROAS Meta (Ads):",
            min_value=1.0,
            max_value=50.0,
            step=0.5,
            key="sb_roas_input",
            on_change=cb_mudar_roas_input
        )

        acos_sb = 1.0 / max(st.session_state.roas_meta, 0.1) * 100
        st.markdown(f"""
        <div style="background:#101625;border:1px solid #1E293B;border-radius:10px;padding:8px 12px;margin-top:8px;margin-bottom:12px;display:flex;justify-content:space-between;align-items:center">
            <span style="color:#64748B;font-size:0.72rem;font-weight:700">ACoS RESULTANTE</span>
            <span style="color:#34D399;font-weight:800;font-size:0.9rem">{acos_sb:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)

        with st.popover("➕ Criar Novo Perfil", use_container_width=True):
            st.markdown("##### ⚙️ Cadastrar Perfil Fiscal Customizado")
            novo_nome_p = st.text_input("Nome do Perfil:", placeholder="Ex: Simples Anexo III (6%)")
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                novo_aliq_p = st.number_input("Alíquota (%):", min_value=0.0, max_value=30.0, value=6.0, step=0.5, key="new_prof_aliq")
            with c_p2:
                novo_roas_p = st.number_input("ROAS Meta:", min_value=1.0, max_value=50.0, value=8.0, step=0.5, key="new_prof_roas")
            
            if st.button("💾 Salvar Perfil", use_container_width=True, type="primary", key="btn_save_new_profile"):
                if novo_nome_p.strip():
                    nome_p = novo_nome_p.strip()
                    st.session_state.perfis_custom[nome_p] = {"aliquota": float(novo_aliq_p), "roas": float(novo_roas_p)}
                    st.session_state.perfil_fiscal = nome_p
                    st.session_state.aliquota_simples_perc = float(novo_aliq_p)
                    st.session_state.roas_meta = float(novo_roas_p)
                    st.session_state.sb_perfil_sel = nome_p
                    st.session_state.sb_aliq_input = float(novo_aliq_p)
                    st.session_state.sb_roas_input = float(novo_roas_p)
                    salvar_config_disco({
                        "perfil_fiscal": nome_p,
                        "aliquota_simples_perc": float(novo_aliq_p),
                        "roas_meta": float(novo_roas_p),
                        "perfis_custom": st.session_state.perfis_custom
                    })
                    st.success(f"Perfil '{nome_p}' salvo!")
                    st.rerun()
                else:
                    st.error("Digite um nome válido!")

aba = st.session_state.aba

# Backward compat: redirecionar chaves antigas → novas
if aba in ("relatorios", "analise_ads", "gerencial", "analise_skus"):
    aba = "inteligencia"
    st.session_state.aba = aba

# ==========================================================
# MÓDULO 0 — PAINEL GERAL (DASHBOARD)
# ==========================================================
if aba == "dashboard":
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0E1424,#070B14);border:1px solid #1E293B;padding:22px 28px;border-radius:16px;margin-bottom:24px;box-shadow:0 15px 35px rgba(0,0,0,.6)">
        <div style="color:#38BDF8;font-family:'Outfit',sans-serif;font-size:1.7rem;font-weight:800">🏠 Painel Geral — Dualis Lingerie</div>
        <div style="color:#94A3B8;font-size:0.95rem;margin-top:6px">Visão executiva simplificada: Está dando lucro? Quanto? Qual produto mais vende?</div>
    </div>
    """, unsafe_allow_html=True)

    meses_list = ["Todos", "01-Janeiro", "02-Fevereiro", "03-Março", "04-Abril", "05-Maio", "06-Junho", "07-Julho", "08-Agosto", "09-Setembro", "10-Outubro", "11-Novembro", "12-Dezembro"]

    df1, df2, df3 = st.columns(3)
    with df1:
        dash_ano = st.selectbox("📅 Ano:", ["2026", "2025", "Todos"], index=0, key="dash_ano")
    with df2:
        dash_mes = st.selectbox("🗓️ Mês:", meses_list, index=0, key="dash_mes")
    with df3:
        dash_plat = st.selectbox("🏪 Plataforma:", ["Todas", "Shopee", "TikTok", "Mercado Livre", "Shein"], index=0, key="dash_plat")

    st.markdown("---")

    df_v_dash = load_vendas_organizadas(ano_filtro=dash_ano, mes_filtro=dash_mes, plat_filtro=dash_plat)
    df_a_dash = load_ads_organizados(ano_filtro=dash_ano, mes_filtro=dash_mes, plat_filtro=dash_plat)

    # --- Cálculos centrais ---
    cost_map_dash = {p['nome']: float(p.get('custo_fabricacao', p.get('custo_unitario', 3.65))) for p in st.session_state.produtos if 'nome' in p}
    def _unit_cost_dash(p_name):
        n_up = str(p_name).upper()
        if 'GESTANTE' in n_up or 'CG' in n_up or 'PÓS PARTO' in n_up or 'HOT PANT' in n_up:
            return cost_map_dash.get('Calcinha Gestante e Pós Parto Cintura Alta', 3.65)
        elif 'CINTA' in n_up or 'REDUTORA' in n_up or 'GALENA' in n_up:
            return cost_map_dash.get('Cinta Modeladora', 6.00)
        elif 'FIO' in n_up or 'REGULAGEM' in n_up:
            return cost_map_dash.get('Calcinha Fio Dental Regulagem', 2.10)
        return 3.65

    fat_d = rep_d = cmv_d = pecas_d = 0.0
    pedidos_d = 0
    if df_v_dash is not None and len(df_v_dash) > 0:
        fat_d = df_v_dash["Valor Total"].sum()
        rep_d = df_v_dash["Repasse Líquido"].sum()
        pedidos_d = df_v_dash["ID Pedido"].nunique() if "ID Pedido" in df_v_dash.columns else len(df_v_dash)
        pecas_d = df_v_dash["Peças Físicas"].sum() if "Peças Físicas" in df_v_dash.columns else df_v_dash["Quantidade"].sum()
        df_v_dash["_CMV"] = df_v_dash["Peças Físicas"] * df_v_dash["Produto"].apply(_unit_cost_dash)
        cmv_d = df_v_dash["_CMV"].sum()

    ads_d = df_a_dash["Investimento"].sum() if df_a_dash is not None and len(df_a_dash) > 0 else 0.0
    lucro_d = rep_d - ads_d - cmv_d
    margem_d = (lucro_d / fat_d * 100) if fat_d > 0 else 0.0

    # Semáforo geral
    if margem_d >= 15:
        badge_geral = "🟢 SAUDÁVEL"
        cor_lucro = "#34D399"
    elif margem_d >= 5:
        badge_geral = "🟡 APERTADA"
        cor_lucro = "#FBBF24"
    else:
        badge_geral = "🔴 CRÍTICA"
        cor_lucro = "#F87171"

    # --- Cards KPI ---
    render_kpi_cards([
        {"label": "💰 Faturamento Bruto", "value": f"R$ {fat_d:,.2f}", "color": "#F8FAFC"},
        {"label": "💵 Repasse Depositado", "value": f"R$ {rep_d:,.2f}", "color": "#38BDF8"},
        {"label": "📢 (-) Ads", "value": f"R$ {ads_d:,.2f}", "color": "#FBBF24"},
        {"label": "✂️ (-) Produção", "value": f"R$ {cmv_d:,.2f}", "sub": f"{int(pecas_d):,} peças", "color": "#EF4444"},
        {"label": f"💚 Lucro Líquido ({badge_geral})", "value": f"R$ {lucro_d:,.2f}", "sub": f"Margem: {margem_d:.1f}%", "color": cor_lucro},
    ])

    # --- Duas colunas: DRE Visual + Ranking de Produtos ---
    col_dre, col_rank = st.columns([1, 1.2])

    with col_dre:
        dre_card_html = textwrap.dedent(f"""
        <div style="background:linear-gradient(135deg,#0E1526 0%,#0B1020 100%);border:1px solid #38BDF8;border-radius:16px;padding:20px;box-shadow:0 10px 30px rgba(56,189,248,.12)">
            <div style="color:#38BDF8;font-weight:800;font-size:1.1rem;margin-bottom:14px">📊 DRE EXECUTIVO DE CAIXA</div>
            <div style="display:grid;gap:8px">
                <div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #1E293B">
                    <span style="color:#94A3B8;font-size:0.85rem;font-weight:600">1. Faturamento Bruto</span>
                    <span style="color:#F8FAFC;font-weight:800;font-size:0.95rem">R$ {fat_d:,.2f}</span>
                </div>
                <div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #1E293B">
                    <span style="color:#94A3B8;font-size:0.85rem;font-weight:600">2. (-) Taxas da Plataforma</span>
                    <span style="color:#FBBF24;font-weight:700;font-size:0.95rem">- R$ {(fat_d - rep_d):,.2f}</span>
                </div>
                <div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #1E293B">
                    <span style="color:#94A3B8;font-size:0.85rem;font-weight:600">= Repasse Depositado</span>
                    <span style="color:#38BDF8;font-weight:800;font-size:0.95rem">R$ {rep_d:,.2f}</span>
                </div>
                <div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #1E293B">
                    <span style="color:#94A3B8;font-size:0.85rem;font-weight:600">3. (-) Investimento Ads</span>
                    <span style="color:#FBBF24;font-weight:700;font-size:0.95rem">- R$ {ads_d:,.2f}</span>
                </div>
                <div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #1E293B">
                    <span style="color:#94A3B8;font-size:0.85rem;font-weight:600">4. (-) Custo de Produção ({int(pecas_d):,} un)</span>
                    <span style="color:#EF4444;font-weight:700;font-size:0.95rem">- R$ {cmv_d:,.2f}</span>
                </div>
                <div style="display:flex;justify-content:space-between;padding:10px 0 4px 0;border-top:2px solid #38BDF8;margin-top:4px">
                    <span style="color:#F8FAFC;font-size:0.95rem;font-weight:800">= LUCRO LÍQUIDO REAL</span>
                    <span style="color:{cor_lucro};font-weight:800;font-size:1.2rem">R$ {lucro_d:,.2f}</span>
                </div>
                <div style="text-align:right;color:{cor_lucro};font-size:0.8rem;font-weight:700">{badge_geral} — Margem {margem_d:.1f}%</div>
            </div>
        </div>
        """).strip()
        st.markdown(dre_card_html, unsafe_allow_html=True)

    with col_rank:
        st.markdown("""<div style="color:#38BDF8;font-weight:800;font-size:1.1rem;margin-bottom:10px">🏆 Ranking de Produtos por Lucro</div>""", unsafe_allow_html=True)

        if df_v_dash is not None and len(df_v_dash) > 0:
            df_v_dash["Modelo_D"] = df_v_dash["Produto"].apply(parse_model)
            rank = df_v_dash.groupby("Modelo_D").agg(
                Pedidos=("ID Pedido", "nunique"),
                Pecas=("Peças Físicas", "sum"),
                Faturamento=("Valor Total", "sum"),
                Repasse=("Repasse Líquido", "sum"),
                CMV=("_CMV", "sum")
            ).reset_index()
            rank["Lucro"] = rank["Repasse"] - rank["CMV"]
            rank["Margem"] = (rank["Lucro"] / rank["Faturamento"] * 100).round(1)
            rank["Status"] = rank["Margem"].apply(lambda m: "🟢" if m >= 15 else ("🟡" if m >= 5 else "🔴"))
            rank = rank.sort_values("Lucro", ascending=False)

            st.dataframe(
                rank[["Status", "Modelo_D", "Pecas", "Faturamento", "Lucro", "Margem"]],
                column_config={
                    "Status":     st.column_config.TextColumn("", width="small"),
                    "Modelo_D":   st.column_config.TextColumn("Produto / Modelo", width="medium"),
                    "Pecas":      st.column_config.NumberColumn("Peças", format="%d"),
                    "Faturamento": st.column_config.NumberColumn("Faturamento (R$)", format="R$ %.2f"),
                    "Lucro":      st.column_config.NumberColumn("Lucro (R$)", format="R$ %.2f"),
                    "Margem":     st.column_config.NumberColumn("Margem %", format="%.1f%%"),
                },
                use_container_width=True, hide_index=True
            )
        else:
            st.info("Importe relatórios de vendas para visualizar o ranking de produtos.")

    st.markdown("---")

    # --- DRE Comparativo Mês a Mês ---
    st.subheader("📈 DRE Comparativo Mês a Mês")
    if df_v_dash is not None and len(df_v_dash) > 0:
        dre_mm = df_v_dash.groupby("Mês").agg(
            Faturamento=("Valor Total", "sum"),
            Repasse=("Repasse Líquido", "sum"),
            Pecas=("Peças Físicas", "sum"),
            CMV=("_CMV", "sum")
        ).reset_index()

        if df_a_dash is not None and len(df_a_dash) > 0:
            ads_map = df_a_dash.groupby("Mês")["Investimento"].sum().to_dict()
            dre_mm["Ads"] = dre_mm["Mês"].map(lambda m: ads_map.get(m, 0.0))
        else:
            dre_mm["Ads"] = 0.0

        dre_mm["Lucro"] = dre_mm["Repasse"] - dre_mm["Ads"] - dre_mm["CMV"]
        dre_mm["Margem"] = (dre_mm["Lucro"] / dre_mm["Faturamento"] * 100).round(1)
        dre_mm["Status"] = dre_mm["Margem"].apply(lambda m: "🟢" if m >= 15 else ("🟡" if m >= 5 else "🔴"))

        st.dataframe(
            dre_mm,
            column_config={
                "Mês":          st.column_config.TextColumn("Mês"),
                "Faturamento":  st.column_config.NumberColumn("Faturamento (R$)", format="R$ %.2f"),
                "Repasse":      st.column_config.NumberColumn("Repasse (R$)", format="R$ %.2f"),
                "Ads":          st.column_config.NumberColumn("Ads (R$)", format="R$ %.2f"),
                "CMV":          st.column_config.NumberColumn("Produção (R$)", format="R$ %.2f"),
                "Lucro":        st.column_config.NumberColumn("Lucro (R$)", format="R$ %.2f"),
                "Margem":       st.column_config.NumberColumn("Margem %", format="%.1f%%"),
                "Status":       st.column_config.TextColumn(""),
            },
            use_container_width=True, hide_index=True
        )

        # --- Desempenho e Margem por Marketplace ---
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        st.subheader("🏬 Lucratividade & Margem Real por Marketplace")
        st.caption("Comparativo de retenção financeira: quanto sobra líquido de cada canal de venda.")
        
        by_plat_d = df_v_dash.groupby("Plataforma").agg(
            Pedidos=("ID Pedido", "nunique"),
            Pecas=("Peças Físicas", "sum"),
            Faturamento=("Valor Total", "sum"),
            Repasse=("Repasse Líquido", "sum"),
            CMV=("_CMV", "sum")
        ).reset_index()
        
        by_plat_d["Lucro"] = by_plat_d["Repasse"] - by_plat_d["CMV"]
        by_plat_d["Margem"] = (by_plat_d["Lucro"] / by_plat_d["Faturamento"] * 100).round(1)
        by_plat_d["Retencao"] = (by_plat_d["Repasse"] / by_plat_d["Faturamento"] * 100).round(1)
        by_plat_d["Status"] = by_plat_d["Margem"].apply(lambda m: "🟢 SAUDÁVEL" if m >= 15 else ("🟡 APERTADA" if m >= 5 else "🔴 CRÍTICA"))
        by_plat_d = by_plat_d.sort_values("Lucro", ascending=False)
        
        st.dataframe(
            by_plat_d,
            column_config={
                "Plataforma":   st.column_config.TextColumn("Marketplace", width="medium"),
                "Pedidos":      st.column_config.NumberColumn("Pedidos", format="%d"),
                "Pecas":        st.column_config.NumberColumn("Peças", format="%d"),
                "Faturamento":  st.column_config.NumberColumn("Faturamento (R$)", format="R$ %.2f"),
                "Repasse":      st.column_config.NumberColumn("Repasse Líquido (R$)", format="R$ %.2f"),
                "Retencao":     st.column_config.NumberColumn("Taxa Retenção Repasse", format="%.1f%%"),
                "Lucro":        st.column_config.NumberColumn("Lucro Bruto Caixa (R$)", format="R$ %.2f"),
                "Margem":       st.column_config.NumberColumn("Margem Real %", format="%.1f%%"),
                "Status":       st.column_config.TextColumn("Saúde Financeira", width="small"),
            },
            use_container_width=True, hide_index=True
        )
    else:
        st.info("Importe relatórios de vendas para visualizar o DRE e a lucratividade por marketplace.")


# ==========================================================
# MÓDULO 1 — CATÁLOGO DE PRODUTOS & HUB EXCLUSIVO
# ==========================================================
elif aba == "catalogo":
    if "prod_hub_id" not in st.session_state:
        st.session_state.prod_hub_id = None

    produtos = st.session_state.produtos
    for p in produtos:
        if "sku" not in p: p["sku"] = f"SKU-{p.get('id', 1):02d}"
        if "fornecedor" not in p: p["fornecedor"] = "Confecção Própria"
        if "peso_g" not in p: p["peso_g"] = 80
        if "observacoes" not in p: p["observacoes"] = ""

    # ---------------------------------------------------------
    # VISÃO 1: LISTA ELEGANTE DE PRODUTOS (VITRINE DO CATÁLOGO)
    # ---------------------------------------------------------
    if st.session_state.prod_hub_id is None:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#0E1424,#070B14);border:1px solid #1E293B;padding:22px 28px;border-radius:16px;margin-bottom:24px;box-shadow:0 15px 35px rgba(0,0,0,.6)">
            <div style="color:#38BDF8;font-family:'Outfit',sans-serif;font-size:1.7rem;font-weight:800">📦 Catálogo de Produtos</div>
            <div style="color:#94A3B8;font-size:0.95rem;margin-top:6px">Clique em qualquer produto da lista para abrir o <b>Hub Exclusivo</b> com ficha técnica, precificação e análise de vendas por SKU e tamanho.</div>
        </div>
        """, unsafe_allow_html=True)

        total_prods = len(produtos)
        custo_medio_aq = sum(p.get("custo_unitario", 0.0) for p in produtos) / max(total_prods, 1)
        custo_medio_emb = sum(p.get("custo_embalagem", 0.0) for p in produtos) / max(total_prods, 1)
        categorias = len(set(p.get("categoria", "Geral") for p in produtos))

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📦 Total de Produtos", f"{total_prods} itens")
        c2.metric("🏷️ Categorias Únicas", f"{categorias} categorias")
        c3.metric("💵 Custo Médio Aquisição", f"R$ {custo_medio_aq:.2f}/un")
        c4.metric("📦 Custo Médio Embalagem", f"R$ {custo_medio_emb:.2f}/kit")

        st.markdown("---")

        # Barra de Pesquisa e Filtros
        col_b1, col_b2, col_b3 = st.columns([2, 1.5, 1])
        with col_b1:
            busca_query = st.text_input("🔍 Buscar Produto ou SKU:", "", key="cat_search_input")
        with col_b2:
            cats_list = ["Todas"] + sorted(list(set(p.get("categoria", "Outros") for p in produtos)))
            cat_filtro = st.selectbox("🏷️ Filtrar por Categoria:", cats_list, key="cat_filter_sel")
        with col_b3:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            with st.popover("➕ Novo Item"):
                st.markdown("#### ➕ Cadastrar Novo Produto")
                with st.form(key="form_novo_prod"):
                    n_nome = st.text_input("Nome do Produto:")
                    n_sku  = st.text_input("SKU Principal:")
                    n_cat  = st.selectbox("Categoria:", ["Lingerie Gestante", "Lingerie / Underwear", "Cintas & Modeladores", "Fio Dental", "Acessórios", "Outros"])
                    n_cu   = st.number_input("Custo Aquisição (R$):", min_value=0.0, value=5.00, step=0.5)
                    n_emb  = st.number_input("Custo Embalagem (R$):", min_value=0.0, value=0.30, step=0.05)
                    n_forn = st.text_input("Fornecedor:", value="Confecção Própria")
                    if st.form_submit_button("Cadastrar", type="primary"):
                        novo_id = max([p.get("id", 0) for p in produtos], default=0) + 1
                        novo_prod = {
                            "id": novo_id, "nome": n_nome or f"Produto {novo_id}", "sku": n_sku or f"SKU-{novo_id:02d}",
                            "categoria": n_cat, "custo_unitario": n_cu, "custo_embalagem": n_emb,
                            "fornecedor": n_forn, "peso_g": 80, "observacoes": ""
                        }
                        st.session_state.produtos.append(novo_prod)
                        salvar_produtos_disco(st.session_state.produtos)
                        st.success(f"'{n_nome}' cadastrado!")
                        st.rerun()

        # Filtragem da lista
        prods_filtrados = produtos
        if cat_filtro != "Todas":
            prods_filtrados = [p for p in prods_filtrados if p.get("categoria") == cat_filtro]
        if busca_query.strip():
            bq = busca_query.lower()
            prods_filtrados = [p for p in prods_filtrados if bq in p.get("nome", "").lower() or bq in p.get("sku", "").lower()]

        # Expander opcional de Edição Rápida em Planilha
        with st.expander("✏️ Edição Rápida de Custos em Tabela (Planilha)"):
            df_cat = pd.DataFrame(produtos)
            df_cat_ed = st.data_editor(
                df_cat[["id", "nome", "sku", "categoria", "custo_unitario", "custo_embalagem", "fornecedor"]],
                column_config={
                    "id":              st.column_config.NumberColumn("ID", disabled=True, width="small"),
                    "nome":            st.column_config.TextColumn("Nome do Produto", width="medium", required=True),
                    "sku":             st.column_config.TextColumn("SKU Principal", width="small"),
                    "categoria":       st.column_config.SelectboxColumn("Categoria", options=["Lingerie Gestante", "Lingerie / Underwear", "Cintas & Modeladores", "Fio Dental", "Acessórios", "Outros"]),
                    "custo_unitario":  st.column_config.NumberColumn("Custo Aquisição (R$)", format="R$ %.2f", min_value=0.0, step=0.05),
                    "custo_embalagem": st.column_config.NumberColumn("Custo Embalagem (R$)", format="R$ %.2f", min_value=0.0, step=0.05),
                    "fornecedor":      st.column_config.TextColumn("Fornecedor", width="medium"),
                },
                use_container_width=True, hide_index=True, key="ed_cat_expander"
            )
            if st.button("💾 Salvar Planilha", key="btn_salvar_planilha_exp", type="primary"):
                records = df_cat_ed.to_dict("records")
                for i, r in enumerate(records):
                    r["id"] = i + 1
                    orig = next((p for p in produtos if p.get("id") == r["id"]), {})
                    r["peso_g"] = orig.get("peso_g", 80)
                    r["observacoes"] = orig.get("observacoes", "")
                st.session_state.produtos = records
                salvar_produtos_disco(records)
                st.success("✅ Custos atualizados no arquivo produtos.json!")
                st.rerun()

        st.subheader("🛍️ Lista de Produtos — Dualis Lingerie")
        st.caption("Clique no nome de qualquer produto para abrir o **Hub Exclusivo** com ficha técnica, precificação por canal e análise de vendas.")

        if not prods_filtrados:
            st.warning("Nenhum produto encontrado com os filtros aplicados.")
        else:
            for p in prods_filtrados:
                sku_str  = p.get("sku", "SKU")
                cat_str  = p.get("categoria", "Geral")
                nome_str = p.get("nome", "Produto")
                p_id     = p.get("id", 1)
                c_un     = float(p.get("custo_fabricacao", p.get("custo_unitario", 3.65)))

                # Definir ícone temático
                if "Gestante" in cat_str:
                    icon_cat = "🤱"
                elif "Cinta" in cat_str or "Modelador" in cat_str:
                    icon_cat = "⏳"
                elif "Fio" in cat_str:
                    icon_cat = "🩲"
                else:
                    icon_cat = "✨"

                btn_label = f"{icon_cat}   {nome_str}   │   SKU: {sku_str}"
                if st.button(btn_label, key=f"btn_hub_p_{p_id}", use_container_width=True, type="primary"):
                    st.session_state.prod_hub_id = p_id
                    st.rerun()

        # --- FIM DA LISTA DE PRODUTOS ---

    # ---------------------------------------------------------
    # VISÃO 2: HUB EXCLUSIVO DO PRODUTO SELECIONADO
    # ---------------------------------------------------------
    else:
        prod_id = st.session_state.prod_hub_id
        idx_prod, prod_info = next(((i, p) for i, p in enumerate(produtos) if p["id"] == prod_id), (0, produtos[0]))

        # Cabeçalho com botão de Voltar e Alternador Rápido de Modelos
        h_col1, h_col2 = st.columns([1.4, 2.6])
        with h_col1:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            if st.button("← Voltar ao Catálogo", key="btn_back_to_catalog", use_container_width=True, type="primary"):
                st.session_state.prod_hub_id = None
                st.rerun()
        with h_col2:
            all_prod_names = [p["nome"] for p in produtos]
            curr_idx = next((i for i, p in enumerate(produtos) if p["id"] == prod_id), 0)
            sel_quick = st.selectbox(
                "🔄 Alternar Modelo / Produto Rapidamente:",
                options=all_prod_names,
                index=curr_idx,
                key=f"hub_quick_switch_{prod_id}"
            )
            if sel_quick != prod_info["nome"]:
                target_p = next((p for p in produtos if p["nome"] == sel_quick), None)
                if target_p:
                    st.session_state.prod_hub_id = target_p["id"]
                    st.rerun()

        hub_hdr_html = textwrap.dedent(f"""
        <div style="background:linear-gradient(135deg,#0E1424,#070B14);border:1px solid #38BDF8;border-radius:16px;padding:22px 28px;margin-top:10px;margin-bottom:24px;box-shadow:0 15px 35px rgba(56,189,248,.15)">
            <div style="display:flex;align-items:center;gap:16px">
                <div style="background:linear-gradient(135deg,#38BDF8,#0284C7);color:#050811;width:52px;height:52px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:1.8rem;font-weight:800;box-shadow:0 0 20px rgba(56,189,248,0.4)">💎</div>
                <div>
                    <div style="color:#38BDF8;font-family:'Outfit',sans-serif;font-size:1.8rem;font-weight:800">Hub Exclusivo: {prod_info['nome']}</div>
                    <div style="color:#94A3B8;font-size:0.9rem;margin-top:2px">
                        <b>SKU:</b> <span style="color:#38BDF8;font-weight:700">{prod_info.get('sku','—')}</span> │ 
                        <b>Categoria:</b> <span style="color:#F8FAFC">{prod_info.get('categoria','—')}</span> │ 
                        <b>Fornecedor:</b> <span style="color:#F8FAFC">{prod_info.get('fornecedor','—')}</span>
                    </div>
                </div>
            </div>
        </div>
        """).strip()
        st.markdown(hub_hdr_html, unsafe_allow_html=True)

        hub_tab1, hub_tab2, hub_tab3, hub_tab4 = st.tabs([
            "📝 Ficha Técnica & Cadastro",
            "💰 Precificação Sugerida por Plataforma",
            "🏷️ Preços Praticados & Margem Real",
            "📊 Análise de Vendas, SKUs & Tamanhos"
        ])

        # --- ABA 1: FICHA TÉCNICA ---
        with hub_tab1:
            st.subheader("📝 Ficha Técnica & Informações Operacionais")
            st.caption("Edite e mantenha os dados técnicos deste produto sempre atualizados.")

            with st.form(key=f"form_hub_ficha_{prod_info['id']}"):
                fc1, fc2, fc3 = st.columns(3)
                with fc1:
                    f_nome = st.text_input("Nome do Produto", value=prod_info.get("nome", ""), key=f"h_fnome_{prod_info['id']}")
                    f_sku  = st.text_input("SKU Principal", value=prod_info.get("sku", ""), key=f"h_fsku_{prod_info['id']}")
                with fc2:
                    cats_opt = ["Lingerie Gestante", "Lingerie / Underwear", "Cintas & Modeladores", "Fio Dental", "Acessórios", "Outros"]
                    cat_idx = cats_opt.index(prod_info.get("categoria")) if prod_info.get("categoria") in cats_opt else 0
                    f_cat  = st.selectbox("Categoria", cats_opt, index=cat_idx, key=f"h_fcat_{prod_info['id']}")
                    f_forn = st.text_input("Fornecedor / Origem", value=prod_info.get("fornecedor", "Confecção Própria"), key=f"h_fforn_{prod_info['id']}")
                with fc3:
                    f_cu   = st.number_input("Custo Aquisição / Peça (R$)", min_value=0.0, value=float(prod_info.get("custo_unitario", 0.0)), step=0.05, key=f"h_fcu_{prod_info['id']}")
                    f_emb  = st.number_input("Custo Embalagem / Pedido (R$)", min_value=0.0, value=float(prod_info.get("custo_embalagem", 0.0)), step=0.05, key=f"h_femb_{prod_info['id']}")

                fc4, fc5 = st.columns([1, 3])
                with fc4:
                    f_peso = st.number_input("Peso Estimado (g)", min_value=0, value=int(prod_info.get("peso_g", 80)), step=5, key=f"h_fpeso_{prod_info['id']}")
                with fc5:
                    f_obs  = st.text_area("Observações Internas / Ficha de Produção", value=prod_info.get("observacoes", ""), height=68, key=f"h_fobs_{prod_info['id']}")

                if st.form_submit_button("💾 Salvar Ficha Técnica do Produto", type="primary"):
                    st.session_state.produtos[idx_prod]["nome"] = f_nome
                    st.session_state.produtos[idx_prod]["sku"] = f_sku
                    st.session_state.produtos[idx_prod]["categoria"] = f_cat
                    st.session_state.produtos[idx_prod]["fornecedor"] = f_forn
                    st.session_state.produtos[idx_prod]["custo_unitario"] = f_cu
                    st.session_state.produtos[idx_prod]["custo_embalagem"] = f_emb
                    st.session_state.produtos[idx_prod]["peso_g"] = f_peso
                    st.session_state.produtos[idx_prod]["observacoes"] = f_obs
                    salvar_produtos_disco(st.session_state.produtos)
                    st.success(f"✅ Ficha técnica de '{f_nome}' salva no disco!")
                    st.rerun()

        # --- ABA 2: PRECIFICAÇÃO SUGERIDA POR PLATAFORMA ---
        with hub_tab2:
            st.subheader("💰 Precificação Sugerida & Margem por Marketplace")
            st.caption("Simule o preço de venda ideal e veja a sobra de caixa exata em cada plataforma.")

            pc1, pc2, pc3 = st.columns([1.5, 1.5, 2])
            with pc1:
                kits_opt = {
                    "1 Peça (1x)": 1,
                    "Kit 2 Peças (2x)": 2,
                    "Kit 3 Peças (3x)": 3,
                    "Kit 4 Peças (4x)": 4,
                    "Kit 5 Peças (5x)": 5,
                    "Kit 6 Peças (6x)": 6,
                    "Kit 8 Peças (8x)": 8,
                    "Kit 10 Peças (10x)": 10,
                    "Kit 12 Peças (12x)": 12,
                    "✏️ Outra Quantidade (Personalizado)": 0
                }
                kit_sel = st.selectbox("Formato do Kit:", list(kits_opt.keys()), index=2, key=f"h_prec_kit_{prod_info['id']}")
                if kits_opt[kit_sel] == 0:
                    qtd_k = st.number_input("Qtd de Peças no Kit:", min_value=1, max_value=200, value=4, step=1, key=f"h_prec_custom_qtd_{prod_info['id']}")
                else:
                    qtd_k = kits_opt[kit_sel]
            with pc2:
                margem_target_perc = st.slider("Margem Alvo Desejada (%):", min_value=5.0, max_value=50.0, value=25.0, step=1.0, key=f"h_prec_mg_{prod_info['id']}")
            with pc3:
                st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
                usar_roas_hub = st.checkbox("🎯 Considerar Meta ROAS", value=True, key=f"h_prec_roas_cb_{prod_info['id']}", help="Desmarque para calcular sem custos de Ads/ROAS")
                simular_preco_hub = st.checkbox("🏷️ Simular no Preço que Eu Busco (R$)", value=False, key=f"h_prec_sim_cb_{prod_info['id']}", help="Marque para simular a margem real de um preço de venda específico")

            c_fisico_kit = (prod_info["custo_unitario"] * qtd_k) + prod_info["custo_embalagem"]
            simples_f = st.session_state.aliquota_simples_perc / 100.0
            acos_f    = (1.0 / st.session_state.roas_meta) if (usar_roas_hub and st.session_state.roas_meta > 0) else 0.0
            target_frac = margem_target_perc / 100.0

            preco_buscado_hub = None
            if simular_preco_hub:
                st.markdown("---")
                sim_col1, sim_col2 = st.columns([1.5, 2.5])
                with sim_col1:
                    preco_buscado_hub = st.number_input(
                        "💡 Digite o Preço que Você Busca / Preço de Venda Simulado (R$):",
                        min_value=0.01,
                        value=39.90,
                        step=1.0,
                        key=f"h_prec_buscado_val_{prod_info['id']}"
                    )
                with sim_col2:
                    st.info(f"Simulando o preço de venda fixo de **R$ {preco_buscado_hub:.2f}** em todas as plataformas. Veja a margem e sobra de caixa resultantes abaixo.")

            roas_lbl_hub = f"{st.session_state.roas_meta:.1f}x" if usar_roas_hub else "DESABILITADO (0%)"
            roas_col_hub = "#A78BFA" if usar_roas_hub else "#94A3B8"

            st.markdown(f"""
            <div style="background:#101625;border:1px solid #1E293B;border-radius:10px;padding:12px 18px;margin-bottom:16px;display:flex;gap:24px;align-items:center;flex-wrap:wrap">
                <div><span style="color:#64748B;font-size:0.7rem;font-weight:700">CMV DO KIT ({qtd_k}x)</span><br><span style="color:#38BDF8;font-weight:800;font-size:1.1rem">R$ {c_fisico_kit:.2f}</span></div>
                <div><span style="color:#64748B;font-size:0.7rem;font-weight:700">SIMPLES NACIONAL</span><br><span style="color:#FBBF24;font-weight:800;font-size:1.1rem">{st.session_state.aliquota_simples_perc:.1f}%</span></div>
                <div><span style="color:#64748B;font-size:0.7rem;font-weight:700">META ROAS</span><br><span style="color:{roas_col_hub};font-weight:800;font-size:1.1rem">{roas_lbl_hub}</span></div>
                <div><span style="color:#64748B;font-size:0.7rem;font-weight:700">MARGEM ALVO</span><br><span style="color:#34D399;font-weight:800;font-size:1.1rem">{margem_target_perc:.0f}%</span></div>
            </div>
            """, unsafe_allow_html=True)

            plat_rows = []
            for canal_nome in st.session_state.presets_taxas.keys():
                pv_sug, com_tot, tf, desc_regra = calcular_preco_sugerido(canal_nome, c_fisico_kit, target_frac, usar_roas=usar_roas_hub)
                
                pv_efetivo = preco_buscado_hub if (simular_preco_hub and preco_buscado_hub is not None) else pv_sug
                com_s, tf_s, desc_tarifa = taxas_para_preco(canal_nome, pv_efetivo)
                
                com_rs  = pv_efetivo * (com_s / 100.0)
                imp_rs  = pv_efetivo * simples_f
                ads_rs  = pv_efetivo * acos_f
                ded_rs  = com_rs + imp_rs + ads_rs + tf_s
                sobra   = pv_efetivo - ded_rs - c_fisico_kit
                margem  = (sobra / pv_efetivo * 100) if pv_efetivo > 0 else 0

                if margem < 10:
                    status_str = "🔴 CRÍTICA"
                elif margem < 20:
                    status_str = "🟡 APERTADA"
                else:
                    status_str = "🟢 SAUDÁVEL"

                row_dict = {
                    "Plataforma": canal_nome,
                    "Regra Aplicada": desc_tarifa,
                    "Preço Sugerido": f"R$ {pv_sug:.2f}",
                }
                
                if simular_preco_hub:
                    row_dict["Preço Buscado"] = f"R$ {pv_efetivo:.2f}"
                
                row_dict.update({
                    "CMV Kit": f"R$ {c_fisico_kit:.2f}",
                    "Comissão (R$)": f"R$ {com_rs:.2f}",
                    "Taxa Fixa (R$)": f"R$ {tf_s:.2f}",
                    "Impostos (R$)": f"R$ {imp_rs:.2f}",
                    "Ads (R$)": f"R$ {ads_rs:.2f}" if usar_roas_hub else "R$ 0.00 (Off)",
                    "Sobra de Caixa": f"R$ {sobra:.2f}",
                    "Margem Real": f"{margem:.1f}%",
                    "Status": status_str
                })
                plat_rows.append(row_dict)

            col_configs = {
                "Plataforma":     st.column_config.TextColumn("Plataforma", width="medium"),
                "Regra Aplicada": st.column_config.TextColumn("Regra Vigente", width="medium"),
                "Preço Sugerido": st.column_config.TextColumn("Preço Sugerido", width="small"),
                "Sobra de Caixa": st.column_config.TextColumn("Sobra de Caixa", width="small"),
                "Margem Real":    st.column_config.TextColumn("Margem Real", width="small"),
                "Status":         st.column_config.TextColumn("Saúde da Margem", width="small"),
            }
            if simular_preco_hub:
                col_configs["Preço Buscado"] = st.column_config.TextColumn("Preço Buscado (Simulad.)", width="small")

            st.dataframe(
                pd.DataFrame(plat_rows),
                column_config=col_configs,
                use_container_width=True, hide_index=True
            )

        # --- ABA 3: PREÇOS PRATICADOS ATUALMENTE ---
        with hub_tab3:
            st.subheader("🏷️ Gestão de Preços Praticados Atualmente")
            st.caption("Cadastre e monitore os preços praticados por marketplace (Cheio, Oferta e Oferta Relâmpago) com diagnóstico de margem de lucro em tempo real.")

            # Inicializar estrutura de preços praticados se não existir no produto
            if "precos_praticados" not in st.session_state.produtos[idx_prod] or not isinstance(st.session_state.produtos[idx_prod]["precos_praticados"], dict):
                st.session_state.produtos[idx_prod]["precos_praticados"] = {}

            precos_dict = st.session_state.produtos[idx_prod]["precos_praticados"]

            # Garantir dados padrão para todas as plataformas ativas
            for p_nome in st.session_state.presets_taxas.keys():
                if p_nome not in precos_dict:
                    precos_dict[p_nome] = {
                        "preco_cheio": 49.90,
                        "preco_oferta": 39.90,
                        "preco_relampago": 34.90,
                        "usar_roas": True,
                        "roas_esperado": float(st.session_state.get("roas_meta", 8.0))
                    }

            # Seletor de Formato de Kit para cálculo de CMV
            pr_col1, pr_col2 = st.columns([2, 2])
            with pr_col1:
                kits_opt_pr = {
                    "1 Peça (1x)": 1,
                    "Kit 2 Peças (2x)": 2,
                    "Kit 3 Peças (3x)": 3,
                    "Kit 4 Peças (4x)": 4,
                    "Kit 5 Peças (5x)": 5,
                    "Kit 6 Peças (6x)": 6,
                    "Kit 8 Peças (8x)": 8,
                    "Kit 10 Peças (10x)": 10,
                    "Kit 12 Peças (12x)": 12,
                    "✏️ Outra Quantidade (Personalizado)": 0
                }
                kit_pr_sel = st.selectbox("Formato do Kit para Análise:", list(kits_opt_pr.keys()), index=2, key=f"h_pr_kit_{prod_info['id']}")
                if kits_opt_pr[kit_pr_sel] == 0:
                    qtd_k_pr = st.number_input("Qtd de Peças no Kit:", min_value=1, max_value=200, value=4, step=1, key=f"h_pr_custom_qtd_{prod_info['id']}")
                else:
                    qtd_k_pr = kits_opt_pr[kit_pr_sel]

            with pr_col2:
                st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
                st.caption(f"CMV do Kit ({qtd_k_pr}x): **R$ {((prod_info['custo_unitario'] * qtd_k_pr) + prod_info['custo_embalagem']):.2f}** | Simples Nacional: **{st.session_state.aliquota_simples_perc:.1f}%**")

            cmv_pr = (prod_info["custo_unitario"] * qtd_k_pr) + prod_info["custo_embalagem"]

            with st.expander("⚙️ Cadastrar / Atualizar Preços Praticados por Marketplace", expanded=True):
                with st.form(key=f"form_precos_praticados_{prod_info['id']}"):
                    st.markdown("#### 📝 Tabela de Preços e Metas ROAS por Canal")
                    novos_dados_precos = {}
                    
                    def calc_micro_margem(p_channel, p_price, cmv_val, roas_active, roas_target):
                        if p_price <= 0:
                            return "<div style='font-size:0.73rem;color:#64748B;margin-top:2px;'>Margem: —</div>"
                        simples_f = st.session_state.aliquota_simples_perc / 100.0
                        acos_f = (1.0 / roas_target) if (roas_active and roas_target > 0) else 0.0
                        com_s, tf_s, _ = taxas_para_preco(p_channel, p_price)
                        com_rs = p_price * (com_s / 100.0)
                        imp_rs = p_price * simples_f
                        ads_rs = p_price * acos_f
                        ded_rs = com_rs + imp_rs + ads_rs + tf_s
                        sobra = p_price - ded_rs - cmv_val
                        margem = (sobra / p_price * 100.0) if p_price > 0 else 0.0
                        
                        if margem < 10:
                            col = "#F87171"
                            badge = "🔴"
                        elif margem < 20:
                            col = "#FBBF24"
                            badge = "🟡"
                        else:
                            col = "#34D399"
                            badge = "🟢"
                        return f"<div style='font-size:0.73rem;color:{col};font-weight:600;margin-top:3px;'>{badge} Margem: <b>{margem:.1f}%</b> (R$ {sobra:.2f})</div>"

                    for p_nome in st.session_state.presets_taxas.keys():
                        dados_p = precos_dict.get(p_nome, {})
                        st.markdown(f"**🏬 {p_nome}**")
                        c1, c2, c3, c4, c5 = st.columns([1.2, 1.2, 1.2, 1, 1.2])
                        
                        with c4:
                            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
                            val_roas_cb = st.checkbox(f"Meta ROAS", value=bool(dados_p.get("usar_roas", True)), key=f"pr_roas_cb_{p_nome}_{prod_info['id']}")
                        with c5:
                            val_roas_num = st.number_input(f"Meta ROAS (x)", min_value=0.5, max_value=50.0, value=float(dados_p.get("roas_esperado", st.session_state.get("roas_meta", 8.0))), step=0.5, key=f"pr_roas_num_{p_nome}_{prod_info['id']}")
                        
                        with c1:
                            val_cheio = st.number_input(f"Preço Cheio (R$)", min_value=0.01, value=float(dados_p.get("preco_cheio", 49.90)), step=1.0, key=f"pr_cheio_{p_nome}_{prod_info['id']}")
                            st.markdown(calc_micro_margem(p_nome, val_cheio, cmv_pr, val_roas_cb, val_roas_num), unsafe_allow_html=True)
                        with c2:
                            val_oferta = st.number_input(f"Oferta Normal (R$)", min_value=0.01, value=float(dados_p.get("preco_oferta", 39.90)), step=1.0, key=f"pr_oferta_{p_nome}_{prod_info['id']}")
                            st.markdown(calc_micro_margem(p_nome, val_oferta, cmv_pr, val_roas_cb, val_roas_num), unsafe_allow_html=True)
                        with c3:
                            val_relampago = st.number_input(f"Oferta Relâmpago (R$)", min_value=0.01, value=float(dados_p.get("preco_relampago", 34.90)), step=1.0, key=f"pr_relampago_{p_nome}_{prod_info['id']}")
                            st.markdown(calc_micro_margem(p_nome, val_relampago, cmv_pr, val_roas_cb, val_roas_num), unsafe_allow_html=True)
                        
                        novos_dados_precos[p_nome] = {
                            "preco_cheio": val_cheio,
                            "preco_oferta": val_oferta,
                            "preco_relampago": val_relampago,
                            "usar_roas": val_roas_cb,
                            "roas_esperado": val_roas_num
                        }
                        st.markdown("<hr style='margin:8px 0;border-color:#1E293B'>", unsafe_allow_html=True)

                    if st.form_submit_button("💾 Salvar Preços Praticados", type="primary", use_container_width=True):
                        st.session_state.produtos[idx_prod]["precos_praticados"] = novos_dados_precos
                        salvar_produtos_disco(st.session_state.produtos)
                        st.success("✅ Preços praticados salvos no disco!")
                        st.rerun()

            st.markdown("---")
            st.subheader("📊 Diagnóstico de Margem de Lucro dos Preços Praticados")

            rows_praticados = []
            simples_frac = st.session_state.aliquota_simples_perc / 100.0
            
            for p_nome, p_cfg in precos_dict.items():
                tipos_preco = [
                    ("🏷️ Preço Cheio", p_cfg.get("preco_cheio", 49.90)),
                    ("🔥 Oferta Normal", p_cfg.get("preco_oferta", 39.90)),
                    ("⚡ Oferta Relâmpago", p_cfg.get("preco_relampago", 34.90))
                ]
                
                usar_r = p_cfg.get("usar_roas", True)
                roas_v = p_cfg.get("roas_esperado", st.session_state.get("roas_meta", 8.0))
                acos_pr = (1.0 / roas_v) if (usar_r and roas_v > 0) else 0.0
                roas_txt = f"{roas_v:.1f}x" if usar_r else "OFF (0%)"

                for t_label, pr_val in tipos_preco:
                    com_s, tf_s, desc_tarifa = taxas_para_preco(p_nome, pr_val)
                    com_rs  = pr_val * (com_s / 100.0)
                    imp_rs  = pr_val * simples_frac
                    ads_rs  = pr_val * acos_pr
                    ded_rs  = com_rs + imp_rs + ads_rs + tf_s
                    sobra   = pr_val - ded_rs - cmv_pr
                    margem  = (sobra / pr_val * 100) if pr_val > 0 else 0.0

                    if margem < 10:
                        status_badge = "🔴 CRÍTICA"
                    elif margem < 20:
                        status_badge = "🟡 APERTADA"
                    else:
                        status_badge = "🟢 SAUDÁVEL"

                    rows_praticados.append({
                        "Plataforma": p_nome,
                        "Modalidade de Preço": t_label,
                        "Preço Praticado": f"R$ {pr_val:.2f}",
                        "Meta ROAS": roas_txt,
                        "Comissão + TF": f"R$ {(com_rs + tf_s):.2f}",
                        "Impostos": f"R$ {imp_rs:.2f}",
                        "Ads (ROAS)": f"R$ {ads_rs:.2f}" if usar_r else "R$ 0.00",
                        "Deduções Totais": f"R$ {ded_rs:.2f}",
                        "Sobra de Caixa": f"R$ {sobra:.2f}",
                        "Margem Real": f"{margem:.1f}%",
                        "Saúde": status_badge
                    })

            df_pr = pd.DataFrame(rows_praticados)
            st.dataframe(
                df_pr,
                column_config={
                    "Plataforma":          st.column_config.TextColumn("Plataforma", width="medium"),
                    "Modalidade de Preço": st.column_config.TextColumn("Modalidade / Oferta", width="medium"),
                    "Preço Praticado":     st.column_config.TextColumn("Preço de Venda", width="small"),
                    "Sobra de Caixa":      st.column_config.TextColumn("Sobra de Caixa", width="small"),
                    "Margem Real":         st.column_config.TextColumn("Margem Real", width="small"),
                    "Saúde":               st.column_config.TextColumn("Saúde da Margem", width="small"),
                },
                use_container_width=True, hide_index=True
            )

        # --- ABA 4: ANÁLISE DE VENDAS REAIS POR SKU E TAMANHO ---
        with hub_tab4:
            st.subheader(f"📊 Análise de Vendas, SKUs & Variações / Tamanhos — {prod_info['nome']}")
            
            df_v_org_hub = load_vendas_organizadas(plat_filtro="Shopee")
            if df_v_org_hub is None or len(df_v_org_hub) == 0:
                st.warning("Nenhum relatório de vendas encontrado nas pastas. Use o menu **📤 Importar Dados** para carregar os arquivos.")
            else:
                words_p = [w.lower() for w in prod_info['nome'].split() if len(w) > 2]
                df_p_audit = df_v_org_hub[df_v_org_hub["Produto"].apply(lambda s: any(w in str(s).lower() for w in words_p))].copy()
                
                if len(df_p_audit) == 0:
                    mod_p = parse_model(prod_info['nome'])
                    df_p_audit = df_v_org_hub[df_v_org_hub.apply(lambda r: parse_model(r['Produto']) == mod_p, axis=1)].copy()

                if len(df_p_audit) == 0:
                    st.info(f"Nenhum registro de vendas encontrado nas pastas para **{prod_info['nome']}**.")
                else:
                    fat_p   = df_p_audit["Valor Total"].sum()
                    rep_p   = df_p_audit["Repasse Líquido"].sum()
                    ped_p   = df_p_audit["ID Pedido"].nunique()
                    un_p    = df_p_audit["Peças Físicas"].sum() if "Peças Físicas" in df_p_audit.columns else df_p_audit["Quantidade"].sum()
                    
                    c_unit  = float(prod_info.get("custo_fabricacao", prod_info.get("custo_unitario", 3.65)))
                    cmv_p   = un_p * c_unit
                    lucro_p = rep_p - cmv_p
                    mg_p    = (lucro_p / fat_p * 100) if fat_p > 0 else 0.0

                    render_kpi_cards([
                        {"label": "💰 Faturamento Bruto", "value": f"R$ {fat_p:,.2f}", "color": "#F8FAFC"},
                        {"label": "💵 Repasse Líquido", "value": f"R$ {rep_p:,.2f}", "color": "#38BDF8"},
                        {"label": "📦 Pedidos Realizados", "value": f"{ped_p:,}", "color": "#FBBF24"},
                        {"label": "👕 Peças Entregues", "value": f"{int(un_p):,} un", "sub": f"Média: {(un_p/ped_p):.1f} un/ped", "color": "#A78BFA"},
                        {"label": "✂️ Custo Produção (CMV)", "value": f"R$ {cmv_p:,.2f}", "color": "#EF4444"},
                        {"label": "💚 Lucro Operacional", "value": f"R$ {lucro_p:,.2f}", "sub": f"Margem: {mg_p:.1f}%", "color": "#34D399"},
                    ])

                    st.markdown("---")

                    st.subheader("📐 Desempenho por Variação e Tamanho do Anúncio")
                    st.caption("Agrupamento das vendas por variação, tamanho e kits do anúncio.")

                    by_var = df_p_audit.groupby(["Variação", "Plataforma"]).agg(
                        Pedidos=("ID Pedido", "nunique"),
                        Kits=("Kits Vendidos", "sum") if "Kits Vendidos" in df_p_audit.columns else ("ID Pedido", "count"),
                        PecasFisicas=("Peças Físicas", "sum"),
                        Faturamento=("Valor Total", "sum"),
                        RepasseLiquido=("Repasse Líquido", "sum")
                    ).reset_index().sort_values("Faturamento", ascending=False)

                    st.dataframe(
                        by_var,
                        column_config={
                            "Variação":       st.column_config.TextColumn("Variação / Cor / Tamanho Anúncio", width="large"),
                            "Plataforma":     st.column_config.TextColumn("Canal"),
                            "Pedidos":        st.column_config.NumberColumn("Pedidos Realizados"),
                            "Kits":           st.column_config.NumberColumn("Kits Vendidos"),
                            "PecasFisicas":   st.column_config.NumberColumn("Peças Físicas"),
                            "Faturamento":    st.column_config.NumberColumn("Faturamento (R$)", format="R$ %.2f"),
                            "RepasseLiquido": st.column_config.NumberColumn("Repasse Líquido (R$)", format="R$ %.2f"),
                        },
                        use_container_width=True, hide_index=True
                    )

# ==========================================================
# MÓDULO 2.2 — CALCULADORA & SIMULADOR DE MARGEM (MENU DIRETO)
# ==========================================================
# ==========================================================
# MÓDULO 2.2 — ENGENHARIA DE PREÇOS & SIMULADOR DE COMBOS
# ==========================================================
elif aba == "precificacao":
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0E1424,#070B14);border:1px solid #1E293B;padding:22px 28px;border-radius:16px;margin-bottom:24px;box-shadow:0 15px 35px rgba(0,0,0,.6)">
        <div style="color:#38BDF8;font-family:'Outfit',sans-serif;font-size:1.7rem;font-weight:800">🎯 Engenharia de Preços & Estratégia de Combos</div>
        <div style="color:#94A3B8;font-size:0.95rem;margin-top:6px">Laboratório de formação de preço multi-canal (Shopee, TikTok, Shein, ML), simulação de combos promocionais e cálculo de Break-Even ROAS.</div>
    </div>
    """, unsafe_allow_html=True)

    produtos = st.session_state.produtos
    nomes_prods = [p["nome"] for p in produtos]

    sim_tipo_modo = st.radio("Selecione o Formato da Estratégia:", ["📦 Kit de Peça Única (1x a 20x)", "🎁 Combo Promocional Multi-Peças (Cross-Selling)"], horizontal=True, key="prec_modo_estrategia")

    if sim_tipo_modo == "📦 Kit de Peça Única (1x a 20x)":
        kits_map = {
            "1 Peça (1x)": 1,
            "Kit 2 Peças (2x)": 2,
            "Kit 3 Peças (3x)": 3,
            "Kit 4 Peças (4x)": 4,
            "Kit 5 Peças (5x)": 5,
            "Kit 6 Peças (6x)": 6,
            "Kit 8 Peças (8x)": 8,
            "Kit 10 Peças (10x)": 10,
            "Kit 12 Peças (12x)": 12,
            "✏️ Outra Quantidade (Personalizado)": 0
        }

        pc1, pc2, pc3, pc4 = st.columns([1.8, 1.5, 1, 1.2])
        with pc1:
            prod_sel_p = st.selectbox("Produto Base:", nomes_prods, key="prec_produto_tab")
        with pc2:
            kit_sel_p  = st.selectbox("Kit / Formato:", list(kits_map.keys()), index=2, key="prec_kit_tab")
            if kits_map[kit_sel_p] == 0:
                qtd_kit = st.number_input("Qtd de Peças no Kit:", min_value=1, max_value=200, value=4, step=1, key="prec_custom_qtd_cat")
            else:
                qtd_kit = kits_map[kit_sel_p]
        with pc3:
            margem_p   = st.number_input("Margem Alvo (%):", min_value=5.0, max_value=60.0, value=25.0, step=1.0, key="prec_margem_tab")
        with pc4:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            usar_roas_cat = st.checkbox("🎯 Meta ROAS", value=True, key="prec_roas_cat_cb", help="Desmarque para desabilitar o custo de Ads/ROAS")

        prod_obj_p = next((p for p in produtos if p["nome"] == prod_sel_p), produtos[0])
        custo_aq_kit = prod_obj_p["custo_unitario"] * qtd_kit
        custo_emb_kit = prod_obj_p["custo_embalagem"]
        custo_fis = custo_aq_kit + custo_emb_kit
        nome_kit_desc = f"{prod_obj_p['nome']} (Kit {qtd_kit}x)"

    else:
        # Modo Combo Multi-Peças
        st.markdown("##### 🎁 Monte a Composição do Combo Promocional:")
        combo_c1, combo_c2 = st.columns(2)
        with combo_c1:
            p1_combo = st.selectbox("Item 1 do Combo:", nomes_prods, index=0, key="cb_p1_sel")
            q1_combo = st.number_input("Qtd Peças Item 1:", min_value=1, max_value=50, value=3, step=1, key="cb_p1_qtd")
        with combo_c2:
            p2_combo = st.selectbox("Item 2 do Combo (Cross-Sell):", ["(Nenhum - Apenas Item 1)"] + nomes_prods, index=1 if len(nomes_prods) > 1 else 0, key="cb_p2_sel")
            q2_combo = st.number_input("Qtd Peças Item 2:", min_value=0, max_value=50, value=1 if p2_combo != "(Nenhum - Apenas Item 1)" else 0, step=1, key="cb_p2_qtd")

        margem_p = st.number_input("Margem Alvo (%):", min_value=5.0, max_value=60.0, value=25.0, step=1.0, key="prec_margem_tab_combo")
        usar_roas_cat = st.checkbox("🎯 Meta ROAS", value=True, key="prec_roas_cat_cb_combo")

        p1_obj = next((p for p in produtos if p["nome"] == p1_combo), produtos[0])
        custo_p1 = p1_obj["custo_unitario"] * q1_combo
        custo_p2 = 0.0
        p2_nome_str = ""
        if p2_combo != "(Nenhum - Apenas Item 1)" and q2_combo > 0:
            p2_obj = next((p for p in produtos if p["nome"] == p2_combo), None)
            if p2_obj:
                custo_p2 = p2_obj["custo_unitario"] * q2_combo
                p2_nome_str = f" + {q2_combo}x {p2_obj['nome']}"

        custo_emb_kit = max(p1_obj.get("custo_embalagem", 0.30), 0.50)
        custo_aq_kit = custo_p1 + custo_p2
        custo_fis = custo_aq_kit + custo_emb_kit
        qtd_kit = q1_combo + q2_combo
        nome_kit_desc = f"Combo: {q1_combo}x {p1_obj['nome']}{p2_nome_str}"

    target_frac = margem_p / 100.0
    roas_lbl_cat = f"{st.session_state.roas_meta:.1f}x" if usar_roas_cat else "DESABILITADO"
    roas_col_cat = "#A78BFA" if usar_roas_cat else "#94A3B8"

    st.markdown(f"""
    <div style="background:#101625;border:1px solid #1E293B;border-radius:10px;padding:14px 20px;margin-bottom:18px;display:flex;gap:28px;align-items:center;flex-wrap:wrap">
        <div>
            <span style="color:#64748B;font-size:0.72rem;font-weight:700">COMPOSIÇÃO: {nome_kit_desc}</span><br>
            <span style="color:#38BDF8;font-weight:800;font-size:1.15rem">CMV Total: R$ {custo_fis:.2f}</span>
            <span style="color:#64748B;font-size:0.72rem;margin-left:8px">(R$ {custo_aq_kit:.2f} produtos + R$ {custo_emb_kit:.2f} embalagem)</span>
        </div>
        <div><span style="color:#64748B;font-size:0.72rem;font-weight:700">SIMPLES NACIONAL</span><br><span style="color:#FBBF24;font-weight:800;font-size:1.1rem">{st.session_state.aliquota_simples_perc:.1f}%</span></div>
        <div><span style="color:#64748B;font-size:0.72rem;font-weight:700">META ROAS</span><br><span style="color:{roas_col_cat};font-weight:800;font-size:1.1rem">{roas_lbl_cat}</span></div>
        <div><span style="color:#64748B;font-size:0.72rem;font-weight:700">MARGEM ALVO</span><br><span style="color:#34D399;font-weight:800;font-size:1.1rem">{margem_p:.0f}%</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Matriz comparativa com Break-Even ROAS
    tabela_rows = []
    first_price = 29.90
    for canal in st.session_state.presets_taxas.keys():
        pv, com_tot, tf, regra = calcular_preco_sugerido(canal, custo_fis, target_frac, usar_roas=usar_roas_cat)
        if canal == list(st.session_state.presets_taxas.keys())[0]:
            first_price = pv
        simples_f = st.session_state.aliquota_simples_perc / 100.0
        acos_f    = (1.0 / st.session_state.roas_meta) if (usar_roas_cat and st.session_state.roas_meta > 0) else 0.0
        com_rs = pv * (com_tot / 100.0)
        imp_rs = pv * simples_f
        ads_rs = pv * acos_f
        ded_rs = com_rs + imp_rs + ads_rs + tf
        lucro  = pv - ded_rs - custo_fis
        
        # Cálculo de Break-Even ROAS
        margem_contribuicao = pv - (com_rs + imp_rs + tf + custo_fis)
        be_roas_str = f"{(pv / margem_contribuicao):.2f}x" if margem_contribuicao > 0 else "—"

        tabela_rows.append({
            "Marketplace": canal,
            "Regra Tarifária": regra,
            "Custo CMV": f"R$ {custo_fis:.2f}",
            "Preço Sugerido": f"R$ {pv:.2f}",
            "Deduções Totais": f"R$ {ded_rs:.2f}",
            "Lucro Líquido":  f"R$ {lucro:.2f}",
            "Margem Alvo": f"{margem_p:.0f}%",
            "Break-Even ROAS": be_roas_str
        })

    st.subheader("📋 Matriz Comparativa de Formação de Preço Multi-Canal")
    st.caption("O **Break-Even ROAS** indica o retorno mínimo em anúncios para não ficar no prejuízo.")
    st.dataframe(pd.DataFrame(tabela_rows), use_container_width=True, hide_index=True)

    st.markdown("---")

    # Simulador de sobra de caixa What-If
    st.subheader("🎯 Simulador What-If: Se vender por R$_____, quanto sobra no bolso?")
    sim_c1, sim_c2 = st.columns([1, 1.5])
    with sim_c1:
        canais_lista = list(st.session_state.presets_taxas.keys())
        canal_sim  = st.selectbox("Canal de Venda:", canais_lista, key="sim_canal_tab")
        preco_sim  = st.number_input("Preço de Venda Simulado (R$):", min_value=0.01, value=max(first_price, 9.99), step=1.0, key="sim_preco_tab")

        simples_s = st.session_state.aliquota_simples_perc / 100.0
        acos_s    = (1.0 / st.session_state.roas_meta) if (usar_roas_cat and st.session_state.roas_meta > 0) else 0.0
        com_s, tf_s, desc_s = taxas_para_preco(canal_sim, preco_sim)
        com_rs_s  = preco_sim * (com_s / 100.0)
        imp_rs_s  = preco_sim * simples_s
        ads_rs_s  = preco_sim * acos_s
        cmv_s     = custo_fis
        ded_s     = com_rs_s + imp_rs_s + ads_rs_s + tf_s
        sobra_s   = preco_sim - ded_s - cmv_s
        margem_s  = sobra_s / preco_sim * 100 if preco_sim > 0 else 0
        st.caption(f"Tarifa Vigente: **{desc_s}**")

    with sim_c2:
        if margem_s < 10:
            badge_s = '<span class="badge-pill badge-red">🔴 MARGEM CRÍTICA</span>'
        elif margem_s < 20:
            badge_s = '<span class="badge-pill badge-yellow">🟡 MARGEM APERTADA</span>'
        else:
            badge_s = '<span class="badge-pill badge-green">🟢 MARGEM SAUDÁVEL</span>'

        st.markdown(badge_s, unsafe_allow_html=True)
        cor_sobra = "#34D399" if sobra_s >= 0 else "#F87171"
        ads_txt_sim = f"ADS (ROAS {st.session_state.roas_meta:.0f}x)" if usar_roas_cat else "ADS (Desabilitado)"
        sim_res_html = textwrap.dedent(f"""
        <div style="background:#101625;border:1px solid #1E293B;border-radius:12px;padding:18px 20px;margin-top:10px">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:14px">
                <div><div style="color:#64748B;font-size:0.72rem;font-weight:700">PREÇO DE VENDA</div><div style="color:#F8FAFC;font-weight:800;font-size:1.3rem">R$ {preco_sim:.2f}</div></div>
                <div><div style="color:#64748B;font-size:0.72rem;font-weight:700">CMV DO COMBO/KIT</div><div style="color:#F87171;font-weight:800;font-size:1.3rem">- R$ {cmv_s:.2f}</div></div>
                <div><div style="color:#64748B;font-size:0.72rem;font-weight:700">COMISSÃO ({com_s:.1f}%)</div><div style="color:#FBBF24;font-weight:700">- R$ {com_rs_s:.2f}</div></div>
                <div><div style="color:#64748B;font-size:0.72rem;font-weight:700">TAXA FIXA</div><div style="color:#FBBF24;font-weight:700">- R$ {tf_s:.2f}</div></div>
                <div><div style="color:#64748B;font-size:0.72rem;font-weight:700">IMPOSTOS ({st.session_state.aliquota_simples_perc:.1f}%)</div><div style="color:#FBBF24;font-weight:700">- R$ {imp_rs_s:.2f}</div></div>
                <div><div style="color:#64748B;font-size:0.72rem;font-weight:700">{ads_txt_sim}</div><div style="color:#FBBF24;font-weight:700">- R$ {ads_rs_s:.2f}</div></div>
            </div>
            <div style="border-top:1px solid #1E293B;padding-top:14px;display:flex;justify-content:space-between;align-items:center">
                <div style="color:#94A3B8;font-weight:700">SOBRA DE CAIXA REAL</div>
                <div style="color:{cor_sobra};font-family:'Outfit',sans-serif;font-size:2rem;font-weight:800">R$ {sobra_s:.2f}</div>
            </div>
            <div style="text-align:right;margin-top:4px">
                <span style="color:#38BDF8;font-weight:700;font-size:1.1rem">{margem_s:.1f}% de margem real</span>
            </div>
        </div>
        """).strip()
        st.markdown(sim_res_html, unsafe_allow_html=True)

# ==========================================================
# MÓDULO 4 — CONFIGURAÇÕES
# ==========================================================
elif aba == "configuracoes":
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0E1424,#070B14);border:1px solid #1E293B;padding:22px 28px;border-radius:16px;margin-bottom:24px;box-shadow:0 15px 35px rgba(0,0,0,.6)">
        <div style="color:#38BDF8;font-family:'Outfit',sans-serif;font-size:1.7rem;font-weight:800">⚙️ Configurações</div>
        <div style="color:#94A3B8;font-size:0.95rem;margin-top:6px">Parametros da empresa: custos dos produtos, aliquota fiscal, ROAS e tarifas dos canais.</div>
    </div>
    """, unsafe_allow_html=True)

    tab_prod, tab_fiscal, tab_canais = st.tabs(["📦 Produtos & Custos", "🏢 Fiscal & Ads", "🏬 Tarifas dos Canais"])

    with tab_prod:
        st.subheader("Catalogo de Produtos — Custos de Fabricacao")
        df_cat = pd.DataFrame(st.session_state.produtos)
        df_cat_ed = st.data_editor(
            df_cat[["id", "nome", "custo_unitario", "custo_embalagem", "categoria"]],
            column_config={
                "id":             st.column_config.NumberColumn("ID", disabled=True),
                "nome":           st.column_config.TextColumn("Produto", width="medium"),
                "custo_unitario": st.column_config.NumberColumn("Custo Aquisicao (R$)", format="R$ %.2f", min_value=0.0, step=0.05),
                "custo_embalagem":st.column_config.NumberColumn("Custo Embalagem (R$)", format="R$ %.2f", min_value=0.0, step=0.05),
                "categoria":      st.column_config.SelectboxColumn("Categoria", options=["Lingerie Gestante","Lingerie / Underwear","Cintas & Modeladores","Fio Dental","Acessorios","Outros"]),
            },
            use_container_width=True, num_rows="dynamic", key="ed_cat"
        )
        if st.button("💾 Salvar Catalogo", key="btn_cat"):
            st.session_state.produtos = df_cat_ed.to_dict("records")
            st.success("Catalogo salvo!")
            st.rerun()

    with tab_fiscal:
        st.subheader("Parametros Fiscais & Publicidade Paga")
        st.caption("Você pode alternar e gerenciar perfis na barra lateral. As alterações são sincronizadas e salvas automaticamente.")

        perfis_dict = st.session_state.get("perfis_custom", PERFIS_PRESETS_PADRAO)
        perfis_opts = list(perfis_dict.keys())
        cur_p = st.session_state.perfil_fiscal if st.session_state.perfil_fiscal in perfis_opts else perfis_opts[0]

        fc1, fc2 = st.columns(2)
        with fc1:
            st.markdown("#### Tributação Ativa")
            sel_tab_perfil = st.selectbox("Perfil Fiscal:", perfis_opts, index=perfis_opts.index(cur_p), key="cfg_page_perfil_sel")
            if sel_tab_perfil != st.session_state.perfil_fiscal:
                st.session_state.perfil_fiscal = sel_tab_perfil
                if sel_tab_perfil in perfis_dict and sel_tab_perfil != "Personalizado":
                    aliq = perfis_dict[sel_tab_perfil]["aliquota"]
                    roas = perfis_dict[sel_tab_perfil]["roas"]
                    st.session_state.aliquota_simples_perc = aliq
                    st.session_state.roas_meta = roas
                    st.session_state.sb_aliq_input = aliq
                    st.session_state.sb_roas_input = roas
                salvar_config_disco({
                    "perfil_fiscal": st.session_state.perfil_fiscal,
                    "aliquota_simples_perc": float(st.session_state.aliquota_simples_perc),
                    "roas_meta": float(st.session_state.roas_meta),
                    "perfis_custom": st.session_state.perfis_custom
                })
                st.rerun()

            st.metric("Alíquota Vigente (%)", f"{st.session_state.aliquota_simples_perc:.1f}%")

        with fc2:
            st.markdown("#### Publicidade Paga (Ads)")
            st.metric("ROAS Meta", f"{st.session_state.roas_meta:.1f}x")
            acos_perc = 1.0 / max(st.session_state.roas_meta, 0.1) * 100
            st.metric("ACoS resultante", f"{acos_perc:.1f}%", help="Custo de Ads como % do faturamento")

        st.success("✅ Todos os parâmetros fiscais e metas de Ads estão salvos e sincronizados no disco.")

    with tab_canais:
        st.subheader("Tarifas por Canal de Venda")
        st.markdown("""
**Regras especiais vigentes:**
- **TikTok Shop (15/07/2026):** Preco < R$50 → 10% + R$4,00 | Preco >= R$50 → 6% + R$6,00 *(aplicado dinamicamente)*
- **Mercado Livre Classico:** 10-14% (sem parcelamento) | **Premium:** 15-19% (ate 10x sem juros)
        """)
        df_tx2 = pd.DataFrame([
            {"Canal": k, "Comissao Base (%)": float(v["comissao"]), "Programa / Frete (%)": float(v["programa"]), "Taxa Fixa (R$)": float(v["taxa_fixa"])}
            for k, v in st.session_state.presets_taxas.items()
        ])
        df_tx2_ed = st.data_editor(df_tx2, column_config={
            "Canal":                  st.column_config.TextColumn("Canal", disabled=True),
            "Comissao Base (%)":      st.column_config.NumberColumn("Comissao (%)",    format="%.1f%%", min_value=0.0, step=0.5),
            "Programa / Frete (%)":   st.column_config.NumberColumn("Programa (%)",   format="%.1f%%", min_value=0.0, step=0.5),
            "Taxa Fixa (R$)":         st.column_config.NumberColumn("Taxa Fixa (R$)", format="R$ %.2f", min_value=0.0, step=0.5),
        }, use_container_width=True, key="ed_tx_cfg")
        if st.button("💾 Salvar Tarifas", key="btn_tx_cfg"):
            for row in df_tx2_ed.to_dict("records"):
                st.session_state.presets_taxas[row["Canal"]] = {
                    "comissao": float(row["Comissao Base (%)"]),
                    "programa": float(row["Programa / Frete (%)"]),
                    "taxa_fixa": float(row["Taxa Fixa (R$)"])
                }
            st.success("Tarifas atualizadas!")
            st.rerun()

# ==========================================================
# MÓDULO 3 — INTELIGÊNCIA COMERCIAL (VENDAS + ADS + DRE + SKUS)
# ==========================================================
elif aba == "inteligencia":
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0E1424,#070B14);border:1px solid #1E293B;padding:22px 28px;border-radius:16px;margin-bottom:24px;box-shadow:0 15px 35px rgba(0,0,0,.6)">
        <div style="color:#38BDF8;font-family:'Outfit',sans-serif;font-size:1.7rem;font-weight:800">📊 Inteligência Comercial</div>
        <div style="color:#94A3B8;font-size:0.95rem;margin-top:6px">Central unificada: vendas auditadas, publicidade (Ads), grade de tamanhos/modelos e DRE detalhado.</div>
    </div>
    """, unsafe_allow_html=True)

    meses_list = ["Todos", "01-Janeiro", "02-Fevereiro", "03-Março", "04-Abril", "05-Maio", "06-Junho", "07-Julho", "08-Agosto", "09-Setembro", "10-Outubro", "11-Novembro", "12-Dezembro"]

    # --- BARRA GLOBAL DE FILTROS ---
    st.markdown("""
    <div style="background:#101625;border:1px solid #1E293B;border-radius:12px;padding:12px 18px;margin-bottom:14px">
        <div style="color:#38BDF8;font-weight:700;font-size:0.85rem;margin-bottom:4px">🎯 PERÍODO & CANAL GLOBAIS (SINCRONIZAÇÃO AUTOMÁTICA EM TODAS AS ABAS)</div>
    </div>
    """, unsafe_allow_html=True)

    ic_f1, ic_f2, ic_f3 = st.columns([1, 1.2, 1.2])
    with ic_f1:
        ano_ic = st.selectbox("📅 Ano:", ["2026", "2025", "Todos"], index=0, key="ic_global_ano")
    with ic_f2:
        mes_ic = st.selectbox("🗓️ Mês:", meses_list, index=0, key="ic_global_mes")
    with ic_f3:
        plat_ic = st.selectbox("🏪 Plataforma:", ["Todas", "Shopee", "TikTok", "Mercado Livre", "Shein"], index=0, key="ic_global_plat")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    ic_tab1, ic_tab2, ic_tab3, ic_tab4 = st.tabs([
        "🛒 Vendas Auditadas",
        "📢 Publicidade (Ads)",
        "🧠 Modelos & Tamanhos",
        "📈 DRE Detalhado"
    ])

    # === SUB-ABA 1: VENDAS AUDITADAS ===
    with ic_tab1:
        st.subheader("🛒 Desempenho Consolidado de Pedidos & Faturamento")
        st.caption(f"Filtro ativo: Ano **{ano_ic}** • Mês **{mes_ic}** • Plataforma **{plat_ic}**")

        df_v_org = load_vendas_organizadas(ano_filtro=ano_ic, mes_filtro=mes_ic, plat_filtro=plat_ic)

        if df_v_org is None or len(df_v_org) == 0:
            st.warning(f"Nenhum relatório de vendas encontrado nas pastas para: Ano **{ano_ic}** • Mês **{mes_ic}** • Plataforma **{plat_ic}**.")
            st.info("Utilize o menu **'📤 Importar Dados'** na barra lateral para salvar novas planilhas organizadas no disco.")
        else:
            pedidos_unicos = df_v_org["ID Pedido"].nunique() if "ID Pedido" in df_v_org.columns else len(df_v_org)
            faturamento_tot = df_v_org["Valor Total"].sum()
            repasse_tot = df_v_org["Repasse Líquido"].sum()
            kits_tot = df_v_org["Kits Vendidos"].sum() if "Kits Vendidos" in df_v_org.columns else len(df_v_org)
            pecas_tot = df_v_org["Peças Físicas"].sum() if "Peças Físicas" in df_v_org.columns else df_v_org["Quantidade"].sum()
            ticket_m = faturamento_tot / pedidos_unicos if pedidos_unicos > 0 else 0.0

            # Cálculo do CMV Físico Total de Produção
            cost_map_cat = {p['nome']: float(p.get('custo_fabricacao', p.get('custo_unitario', 3.65))) for p in st.session_state.produtos if 'nome' in p}
            def get_item_unit_cost(p_name):
                n_up = str(p_name).upper()
                if 'GESTANTE' in n_up or 'CG' in n_up or 'PÓS PARTO' in n_up or 'HOT PANT' in n_up:
                    return cost_map_cat.get('Calcinha Gestante e Pós Parto Cintura Alta', 3.65)
                elif 'CINTA' in n_up or 'REDUTORA' in n_up or 'GALENA' in n_up:
                    return cost_map_cat.get('Cinta Modeladora', 6.00)
                elif 'FIO' in n_up or 'REGULAGEM' in n_up:
                    return cost_map_cat.get('Calcinha Fio Dental Regulagem', 2.10)
                return 3.65

            df_v_org['UnitCost'] = df_v_org['Produto'].apply(get_item_unit_cost)
            df_v_org['CMV_Item'] = df_v_org['Peças Físicas'] * df_v_org['UnitCost']
            
            cmv_tot = df_v_org['CMV_Item'].sum()
            lucro_op = repasse_tot - cmv_tot
            mg_op_perc = (lucro_op / faturamento_tot * 100) if faturamento_tot > 0 else 0.0

            render_kpi_cards([
                {"label": "💰 Faturamento Bruto", "value": f"R$ {faturamento_tot:,.2f}", "color": "#F8FAFC"},
                {"label": "💵 Repasse Líquido", "value": f"R$ {repasse_tot:,.2f}", "color": "#38BDF8"},
                {"label": "📦 Pedidos Concluídos", "value": f"{pedidos_unicos:,}", "color": "#F8FAFC"},
                {"label": "👕 Peças Físicas", "value": f"{pecas_tot:,} un", "color": "#A78BFA"},
                {"label": "✂️ Custo Produção (CMV)", "value": f"R$ {cmv_tot:,.2f}", "color": "#EF4444"},
                {"label": "💚 Lucro Operacional Real", "value": f"R$ {lucro_op:,.2f}", "sub": f"Margem: {mg_op_perc:.1f}%", "color": "#34D399"},
            ])

            st.markdown("---")
            st.subheader("📦 Detalhamento de Vendas por Produto, Variação e Canal")
            
            grp_p = df_v_org.groupby(["Plataforma", "Produto", "Variação"]).agg(
                Pedidos=("ID Pedido", "nunique"),
                Quantidade=("Quantidade", "sum"),
                Faturamento=("Valor Total", "sum"),
                RepasseLiquido=("Repasse Líquido", "sum")
            ).reset_index().sort_values("Faturamento", ascending=False)

            st.dataframe(
                grp_p,
                column_config={
                    "Plataforma":     st.column_config.TextColumn("Plataforma"),
                    "Produto":        st.column_config.TextColumn("Produto", width="large"),
                    "Variação":       st.column_config.TextColumn("Variação / Cor / Tamanho"),
                    "Pedidos":        st.column_config.NumberColumn("Pedidos"),
                    "Quantidade":     st.column_config.NumberColumn("Peças"),
                    "Faturamento":    st.column_config.NumberColumn("Faturamento (R$)", format="R$ %.2f"),
                    "RepasseLiquido": st.column_config.NumberColumn("Repasse Líquido (R$)", format="R$ %.2f"),
                },
                use_container_width=True, hide_index=True
            )

    # === SUB-ABA 2: PUBLICIDADE (ADS) ===
    with ic_tab2:
        st.subheader("📢 Desempenho de Mídia Paga (ROAS, ACoS & CPA)")
        st.caption(f"Filtro ativo: Ano **{ano_ic}** • Mês **{mes_ic}** • Plataforma **{plat_ic}**")

        df_ads_org = load_ads_organizados(ano_filtro=ano_ic, mes_filtro=mes_ic, plat_filtro=plat_ic)

        if df_ads_org is None or len(df_ads_org) == 0:
            st.info(f"Nenhum relatório de Ads encontrado nas pastas para: Ano **{ano_ic}** • Mês **{mes_ic}** • Plataforma **{plat_ic}**.")
            st.info("Utilize o menu **'📤 Importar Dados'** na barra lateral para carregar relatórios de anúncios.")
        else:
            ads_inv = df_ads_org["Investimento"].sum()
            ads_fat = df_ads_org["Faturamento GMV"].sum()
            ads_ped = df_ads_org["Pedidos"].sum()
            roas_ads_real = ads_fat / ads_inv if ads_inv > 0 else 0.0
            acos_ads_real = ads_inv / ads_fat * 100 if ads_fat > 0 else 0.0
            cpa_ads_real  = ads_inv / ads_ped if ads_ped > 0 else 0.0

            roas_meta_def = float(st.session_state.get("roas_meta", 8.0))
            st_ads_badge = "🟢 DENTRO DA META" if roas_ads_real >= roas_meta_def else "🔴 ABAIXO DA META"

            render_kpi_cards([
                {"label": "🎯 ROAS Real no Período", "value": f"{roas_ads_real:.2f}x", "sub": f"Meta: {roas_meta_def:.1f}x ({st_ads_badge})", "color": "#34D399" if roas_ads_real >= roas_meta_def else "#F87171"},
                {"label": "💸 Investimento Total Ads", "value": f"R$ {ads_inv:,.2f}", "color": "#FBBF24"},
                {"label": "💰 Faturamento Gerado Ads", "value": f"R$ {ads_fat:,.2f}", "color": "#38BDF8"},
                {"label": "📊 ACoS Real Ads", "value": f"{acos_ads_real:.2f}%", "color": "#F8FAFC"},
                {"label": "🎯 CPA Médio / Pedido", "value": f"R$ {cpa_ads_real:.2f}", "color": "#A78BFA"},
            ])

            st.markdown("---")

            tab_ad1, tab_ad2, tab_ad3 = st.tabs(["📊 Resumo por Mês & Plataforma", "📢 Detalhamento por Anúncio", "📈 Oscilação Histórica de ROAS"])

            with tab_ad1:
                st.subheader("📊 Resumo Consolidado por Mês & Plataforma")
                df_ads_m = df_ads_org.groupby(["Ano", "Mês", "Plataforma"]).agg(
                    Investimento=("Investimento", "sum"),
                    FaturamentoGMV=("Faturamento GMV", "sum"),
                    Pedidos=("Pedidos", "sum")
                ).reset_index()

                df_ads_m["ROAS Real"] = df_ads_m.apply(lambda r: r["FaturamentoGMV"] / r["Investimento"] if r["Investimento"] > 0 else 0.0, axis=1)
                df_ads_m["ACoS Real"] = df_ads_m.apply(lambda r: (r["Investimento"] / r["FaturamentoGMV"] * 100) if r["FaturamentoGMV"] > 0 else 0.0, axis=1)
                df_ads_m["Status"] = df_ads_m["ROAS Real"].apply(lambda r: "🟢 DENTRO DA META" if r >= roas_meta_def else "🔴 ABAIXO DA META")

                st.dataframe(
                    df_ads_m,
                    column_config={
                        "Ano":            st.column_config.TextColumn("Ano"),
                        "Mês":            st.column_config.TextColumn("Mês"),
                        "Plataforma":     st.column_config.TextColumn("Plataforma"),
                        "Investimento":   st.column_config.NumberColumn("Investimento (R$)", format="R$ %.2f"),
                        "FaturamentoGMV": st.column_config.NumberColumn("Faturamento GMV (R$)", format="R$ %.2f"),
                        "Pedidos":        st.column_config.NumberColumn("Pedidos Ads"),
                        "ROAS Real":      st.column_config.NumberColumn("ROAS Real (x)", format="%.2fx"),
                        "ACoS Real":      st.column_config.NumberColumn("ACoS Real (%)", format="%.2f%%"),
                        "Status":         st.column_config.TextColumn("Status vs Meta"),
                    },
                    use_container_width=True, hide_index=True
                )

            with tab_ad2:
                st.subheader("📢 Detalhamento por Anúncio / Campanha Carregada")
                st.dataframe(
                    df_ads_org.sort_values("Investimento", ascending=False),
                    column_config={
                        "Anúncio":         st.column_config.TextColumn("Anúncio / Campanha", width="large"),
                        "Plataforma":      st.column_config.TextColumn("Plataforma"),
                        "Mês":             st.column_config.TextColumn("Mês"),
                        "Investimento":    st.column_config.NumberColumn("Investimento (R$)", format="R$ %.2f"),
                        "Faturamento GMV": st.column_config.NumberColumn("Faturamento GMV (R$)", format="R$ %.2f"),
                        "Pedidos":         st.column_config.NumberColumn("Pedidos Ads"),
                        "ROAS":            st.column_config.NumberColumn("ROAS Real (x)", format="%.2fx"),
                        "Arquivo":         st.column_config.TextColumn("Arquivo Origem", width="medium"),
                    },
                    use_container_width=True, hide_index=True
                )

            with tab_ad3:
                st.subheader("📈 Oscilação Histórica de ROAS por Período")
                st.caption("Acompanhe o retorno sobre o investimento em anúncios ao longo dos meses.")
                df_ads_hist = df_ads_org.groupby("Mês").agg(
                    Investimento=("Investimento", "sum"),
                    FaturamentoGMV=("Faturamento GMV", "sum")
                ).reset_index()
                df_ads_hist["ROAS"] = df_ads_hist.apply(lambda r: r["FaturamentoGMV"] / r["Investimento"] if r["Investimento"] > 0 else 0.0, axis=1)

                st.dataframe(
                    df_ads_hist,
                    column_config={
                        "Mês":            st.column_config.TextColumn("Mês / Período"),
                        "Investimento":   st.column_config.NumberColumn("Investimento (R$)", format="R$ %.2f"),
                        "FaturamentoGMV": st.column_config.NumberColumn("Faturamento (R$)", format="R$ %.2f"),
                        "ROAS":           st.column_config.NumberColumn("ROAS Real (x)", format="%.2fx"),
                    },
                    use_container_width=True, hide_index=True
                )

    # === SUB-ABA 3: MODELOS & TAMANHOS ===
    with ic_tab3:
        st.subheader("🧠 Análise de Linhas, Modelos & Grade de Tamanhos")
        st.caption(f"Filtro ativo: Ano **{ano_ic}** • Mês **{mes_ic}** • Plataforma **{plat_ic}**")

        df_sk = load_vendas_organizadas(ano_filtro=ano_ic, mes_filtro=mes_ic, plat_filtro=plat_ic)

        if df_sk is None or len(df_sk) == 0:
            st.warning(f"Nenhum relatório de vendas encontrado nas pastas para: Ano **{ano_ic}** • Mês **{mes_ic}** • Plataforma **{plat_ic}**.")
        else:
            df_sk["Modelo_Parsed"]  = df_sk.apply(lambda r: parse_model(r["Produto"]), axis=1)
            df_sk["Kit_Parsed"]     = df_sk.apply(lambda r: parse_kit(r["Produto"], r.get("Variação", "")), axis=1)
            df_sk["Tamanho_Parsed"] = df_sk.apply(lambda r: parse_size(r.get("Variação", "")), axis=1)

            # Champion Highlights
            mod_camp = df_sk.groupby("Modelo_Parsed")["Valor Total"].sum().idxmax()
            mod_camp_val = df_sk.groupby("Modelo_Parsed")["Valor Total"].sum().max()
            pct_mod_camp = (mod_camp_val / df_sk["Valor Total"].sum() * 100) if df_sk["Valor Total"].sum() > 0 else 0.0

            sz_camp = df_sk.groupby("Tamanho_Parsed")["Quantidade"].sum().idxmax()
            sz_camp_cnt = df_sk.groupby("Tamanho_Parsed")["Quantidade"].sum().max()

            kit_camp = df_sk.groupby("Kit_Parsed")["Valor Total"].sum().idxmax()
            kit_camp_val = df_sk.groupby("Kit_Parsed")["Valor Total"].sum().max()

            ik1, ik2, ik3, ik4 = st.columns(4)
            ik1.metric("👑 Modelo Mais Vendido", f"{mod_camp}", f"{pct_mod_camp:.1f}% do Faturamento")
            ik2.metric("📏 Tamanho Campeão", f"Tamanho {sz_camp}", f"{sz_camp_cnt:,} peças vendidas")
            ik3.metric("📦 Kit de Maior Saída", f"{kit_camp}", f"R$ {kit_camp_val:,.2f} faturados")
            ik4.metric("💡 Faturamento da Amostra", f"R$ {df_sk['Valor Total'].sum():,.2f}")

            st.markdown("---")

            tab_m1, tab_m2, tab_m3, tab_m4 = st.tabs(["👑 Modelo / Linha de Produto", "📏 Grade de Tamanhos (P ➔ XG)", "📦 Formato de Kits", "🤖 Diagnóstico de IA Comercial"])

            with tab_m1:
                st.subheader("👑 Desempenho por Modelo / Linha de Produto (Agrupado por IA)")
                grp_m = df_sk.groupby("Modelo_Parsed").agg(
                    Pedidos=("ID Pedido", "nunique"),
                    Quantidade=("Quantidade", "sum"),
                    Faturamento=("Valor Total", "sum"),
                    RepasseLiquido=("Repasse Líquido", "sum")
                ).reset_index().sort_values("Faturamento", ascending=False)

                grp_m["% Faturamento"] = (grp_m["Faturamento"] / df_sk["Valor Total"].sum() * 100)

                st.dataframe(
                    grp_m,
                    column_config={
                        "Modelo_Parsed":  st.column_config.TextColumn("Modelo / Linha Agrupada", width="large"),
                        "Pedidos":        st.column_config.NumberColumn("Pedidos"),
                        "Quantidade":     st.column_config.NumberColumn("Peças"),
                        "Faturamento":    st.column_config.NumberColumn("Faturamento (R$)", format="R$ %.2f"),
                        "RepasseLiquido": st.column_config.NumberColumn("Repasse Líquido (R$)", format="R$ %.2f"),
                        "% Faturamento":  st.column_config.NumberColumn("% Faturamento", format="%.1f%%"),
                    },
                    use_container_width=True, hide_index=True
                )

            with tab_m2:
                st.subheader("📏 Demanda da Grade de Tamanhos (P ➔ M ➔ G ➔ GG ➔ XG ➔ Tamanho Único)")
                st.caption("Filtre por produto do catálogo ou linha para analisar a curva de demanda de tamanhos individual.")

                prods_cat_opts = sorted(list(set([p.get("nome") for p in st.session_state.produtos if p.get("nome")])))
                modelos_opts = sorted(list(df_sk["Modelo_Parsed"].unique()))
                
                filtro_prod_opts = ["🌐 Todos os Produtos (Visão Geral da Marca)"] + [f"📦 {p}" for p in prods_cat_opts] + [f"🏷️ Modelo: {m}" for m in modelos_opts]
                
                sel_prod_sz = st.selectbox("🔍 Filtrar Grade por Produto do Catálogo ou Modelo:", filtro_prod_opts, index=0, key="sel_prod_sz_subtab_filter")

                df_sk_sz = df_sk.copy()
                if sel_prod_sz != "🌐 Todos os Produtos (Visão Geral da Marca)":
                    if sel_prod_sz.startswith("📦 "):
                        nome_p = sel_prod_sz.replace("📦 ", "").strip()
                        words_p = [w.lower() for w in nome_p.split() if len(w) > 2]
                        df_sk_sz = df_sk_sz[df_sk_sz["Produto"].apply(lambda s: any(w in str(s).lower() for w in words_p))]
                    elif sel_prod_sz.startswith("🏷️ Modelo: "):
                        mod_p = sel_prod_sz.replace("🏷️ Modelo: ", "").strip()
                        df_sk_sz = df_sk_sz[df_sk_sz["Modelo_Parsed"] == mod_p]

                if len(df_sk_sz) == 0:
                    st.warning(f"Nenhuma venda encontrada para '{sel_prod_sz}' no período selecionado.")
                else:
                    grp_sz = df_sk_sz.groupby("Tamanho_Parsed").agg(
                        Pedidos=("ID Pedido", "nunique"),
                        Quantidade=("Quantidade", "sum"),
                        Faturamento=("Valor Total", "sum")
                    ).reset_index()

                    size_order = ["P", "M", "G", "GG", "XG", "Tamanho Único"]
                    grp_sz["Order_Key"] = grp_sz["Tamanho_Parsed"].apply(lambda x: size_order.index(x) if x in size_order else 99)
                    grp_sz = grp_sz.sort_values("Order_Key").drop(columns=["Order_Key"])

                    grp_sz["% Demanda"] = (grp_sz["Quantidade"] / df_sk_sz["Quantidade"].sum() * 100)

                    st.dataframe(
                        grp_sz,
                        column_config={
                            "Tamanho_Parsed": st.column_config.TextColumn("Tamanho Grade"),
                            "Pedidos":        st.column_config.NumberColumn("Pedidos Únicos"),
                            "Quantidade":     st.column_config.NumberColumn("Peças Vendidas"),
                            "Faturamento":    st.column_config.NumberColumn("Faturamento (R$)", format="R$ %.2f"),
                            "% Demanda":      st.column_config.NumberColumn("% Demanda da Grade", format="%.1f%%"),
                        },
                        use_container_width=True, hide_index=True
                    )

            with tab_m3:
                st.subheader("📦 Preferência por Formato de Kit (1x, 2x, 3x, 5x, 10x)")
                grp_kt = df_sk.groupby("Kit_Parsed").agg(
                    Pedidos=("ID Pedido", "nunique"),
                    Quantidade=("Quantidade", "sum"),
                    Faturamento=("Valor Total", "sum")
                ).reset_index().sort_values("Faturamento", ascending=False)

                grp_kt["% Participação"] = (grp_kt["Faturamento"] / df_sk["Valor Total"].sum() * 100)

                st.dataframe(
                    grp_kt,
                    column_config={
                        "Kit_Parsed":     st.column_config.TextColumn("Formato do Kit"),
                        "Pedidos":        st.column_config.NumberColumn("Pedidos Únicos"),
                        "Quantidade":     st.column_config.NumberColumn("Quantidade Vendida"),
                        "Faturamento":    st.column_config.NumberColumn("Faturamento (R$)", format="R$ %.2f"),
                        "% Participação": st.column_config.NumberColumn("% Participação", format="%.1f%%"),
                    },
                    use_container_width=True, hide_index=True
                )

            with tab_m4:
                st.subheader("🤖 Diagnóstico de IA Comercial — Dualis Lingerie")
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#0E1526 0%,#0B1020 100%);border:1px solid #1E293B;border-radius:14px;padding:22px;margin-bottom:16px">
                    <div style="color:#38BDF8;font-weight:800;font-size:1.15rem;margin-bottom:10px">💡 Recomendações Estratégicas de Gestão Comercial</div>
                    <ul style="color:#E2E8F0;font-size:0.95rem;line-height:1.7">
                        <li><b>Concentração no Modelo Campeão:</b> O modelo <b>{mod_camp}</b> representa <b>{pct_mod_camp:.1f}%</b> de todo o faturamento da amostra. Manter 70% da capacidade de produção focada nesta linha.</li>
                        <li><b>Prioridade na Grade de Tamanhos:</b> O tamanho <b>{sz_camp}</b> lidera o volume de vendas. Evite rupturas garantindo estoque reforçado nos tamanhos GG e G.</li>
                        <li><b>Formato de Kit Preferido:</b> O formato <b>{kit_camp}</b> gera a maior margem e ticket por pedido. Mantenha os Kits de 3 e 5 peças como destaque nos anúncios.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

    # === SUB-ABA 4: DRE DETALHADO ===
    with ic_tab4:
        st.subheader("📈 Demonstração do Resultado do Exercício (DRE Gerencial)")

        tipo_per_g = st.radio("Modo do Período DRE:", ["🎯 Utilizar Filtro Global", "📆 Intervalo Personalizado de Meses"], horizontal=True, key="dre_tipo_per")

        meses_cods = ["01-Janeiro", "02-Fevereiro", "03-Março", "04-Abril", "05-Maio", "06-Junho", "07-Julho", "08-Agosto", "09-Setembro", "10-Outubro", "11-Novembro", "12-Dezembro"]

        if tipo_per_g == "🎯 Utilizar Filtro Global":
            ano_g = ano_ic
            mes_g = mes_ic
            plat_g = plat_ic
            df_v_g = load_vendas_organizadas(ano_filtro=ano_g, mes_filtro=mes_g, plat_filtro=plat_g)
            df_a_g = load_ads_organizados(ano_filtro=ano_g, mes_filtro=mes_g, plat_filtro=plat_g)
            lbl_periodo_dre = f"Ano {ano_g} • Mês {mes_g} • Plataforma {plat_g}"
        else:
            g_f1, g_f2, g_f3, g_f4 = st.columns(4)
            with g_f1:
                ano_g = st.selectbox("📅 Ano:", ["2026", "2025"], index=0, key="dre_g_ano_range")
            with g_f2:
                mes_ini = st.selectbox("🗓️ Mês Inicial (De):", meses_cods, index=0, key="dre_g_mes_ini")
            with g_f3:
                mes_fim = st.selectbox("🗓️ Mês Final (Até):", meses_cods, index=5, key="dre_g_mes_fim")
            with g_f4:
                plat_g = st.selectbox("🏪 Plataforma:", ["Todas", "Shopee", "TikTok", "Mercado Livre", "Shein"], index=0, key="dre_g_plat_range")

            idx_ini = meses_cods.index(mes_ini)
            idx_fim = meses_cods.index(mes_fim)

            if idx_ini > idx_fim:
                st.warning("⚠️ O Mês Inicial não pode ser posterior ao Mês Final. Invertendo ordem...")
                idx_ini, idx_fim = idx_fim, idx_ini

            meses_range = [m.split("-")[0] for m in meses_cods[idx_ini:idx_fim+1]]
            lbl_periodo_dre = f"Ano {ano_g} • Período: de {meses_cods[idx_ini]} até {meses_cods[idx_fim]} • Plataforma {plat_g}"

            df_v_all = load_vendas_organizadas(ano_filtro=ano_g, mes_filtro="Todos", plat_filtro=plat_g)
            df_a_all = load_ads_organizados(ano_filtro=ano_g, mes_filtro="Todos", plat_filtro=plat_g)

            if df_v_all is not None and len(df_v_all) > 0:
                df_v_g = df_v_all[df_v_all["Mês"].apply(lambda m: any(str(m).startswith(c) for c in meses_range))].copy()
            else:
                df_v_g = None

            if df_a_all is not None and len(df_a_all) > 0:
                df_a_g = df_a_all[df_a_all["Mês"].apply(lambda m: any(str(m).startswith(c) for c in meses_range))].copy()
            else:
                df_a_g = None

        st.markdown("---")

        fat_g = df_v_g["Valor Total"].sum() if df_v_g is not None and len(df_v_g) > 0 else 0.0
        rep_g = df_v_g["Repasse Líquido"].sum() if df_v_g is not None and len(df_v_g) > 0 else 0.0
        pecas_g = df_v_g["Peças Físicas"].sum() if df_v_g is not None and len(df_v_g) > 0 else 0.0

        cost_map_cat = {p['nome']: float(p.get('custo_fabricacao', p.get('custo_unitario', 3.65))) for p in st.session_state.produtos if 'nome' in p}
        def get_item_unit_cost_g(p_name):
            n_up = str(p_name).upper()
            if 'GESTANTE' in n_up or 'CG' in n_up or 'PÓS PARTO' in n_up or 'HOT PANT' in n_up:
                return cost_map_cat.get('Calcinha Gestante e Pós Parto Cintura Alta', 3.65)
            elif 'CINTA' in n_up or 'REDUTORA' in n_up or 'GALENA' in n_up:
                return cost_map_cat.get('Cinta Modeladora', 6.00)
            elif 'FIO' in n_up or 'REGULAGEM' in n_up:
                return cost_map_cat.get('Calcinha Fio Dental Regulagem', 2.10)
            return 3.65

        if df_v_g is not None and len(df_v_g) > 0:
            df_v_g['CMV_Item'] = df_v_g['Peças Físicas'] * df_v_g['Produto'].apply(get_item_unit_cost_g)
            cmv_g = df_v_g['CMV_Item'].sum()
        else:
            cmv_g = 0.0

        ads_inv_g = df_a_g["Investimento"].sum() if df_a_g is not None and len(df_a_g) > 0 else 0.0

        lucro_liquido_g = rep_g - ads_inv_g - cmv_g
        margem_liquida_g = (lucro_liquido_g / fat_g * 100) if fat_g > 0 else 0.0
        mer_global_g = (fat_g / ads_inv_g) if ads_inv_g > 0 else 0.0

        render_kpi_cards([
            {"label": "💰 Faturamento Bruto", "value": f"R$ {fat_g:,.2f}", "color": "#F8FAFC"},
            {"label": "💵 Repasse Depositado", "value": f"R$ {rep_g:,.2f}", "color": "#38BDF8"},
            {"label": "📢 (-) Investimento Ads", "value": f"R$ {ads_inv_g:,.2f}", "color": "#FBBF24"},
            {"label": "✂️ (-) CMV Produção", "value": f"R$ {cmv_g:,.2f}", "color": "#EF4444"},
            {"label": "🏆 LUCRO LÍQUIDO REAL", "value": f"R$ {lucro_liquido_g:,.2f}", "sub": f"Margem Real: {margem_liquida_g:.1f}%", "color": "#34D399"},
            {"label": "📈 ROAS Global (MER)", "value": f"{mer_global_g:.2f}x" if ads_inv_g > 0 else "N/A", "color": "#A78BFA"},
        ])

        st.markdown("---")

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0E1526 0%,#0B1020 100%);border:1px solid #38BDF8;border-radius:16px;padding:24px;margin-bottom:24px;box-shadow:0 15px 35px rgba(56,189,248,.15)">
            <div style="color:#38BDF8;font-weight:800;font-size:1.25rem;margin-bottom:12px">📊 DRE EXECUTIVO DE CAIXA — {lbl_periodo_dre}</div>
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px">
                <div><span style="color:#64748B;font-size:0.75rem;font-weight:700">1. FATURAMENTO BRUTO</span><br><span style="color:#F8FAFC;font-weight:800;font-size:1.3rem">R$ {fat_g:,.2f}</span></div>
                <div><span style="color:#64748B;font-size:0.75rem;font-weight:700">2. REPASSE DEPOSITADO</span><br><span style="color:#38BDF8;font-weight:800;font-size:1.3rem">R$ {rep_g:,.2f}</span></div>
                <div><span style="color:#64748B;font-size:0.75rem;font-weight:700">3. (-) ADS</span><br><span style="color:#FBBF24;font-weight:800;font-size:1.3rem">- R$ {ads_inv_g:,.2f}</span></div>
                <div><span style="color:#64748B;font-size:0.75rem;font-weight:700">4. (-) PRODUÇÃO ({int(pecas_g):,} UN)</span><br><span style="color:#EF4444;font-weight:800;font-size:1.3rem">- R$ {cmv_g:,.2f}</span></div>
                <div style="grid-column:span 2"><span style="color:#64748B;font-size:0.75rem;font-weight:700">5. (=) LUCRO LÍQUIDO REAL</span><br><span style="color:#34D399;font-weight:800;font-size:1.6rem">R$ {lucro_liquido_g:,.2f}</span> <span style="color:#34D399;font-weight:700;font-size:1.1rem">({margem_liquida_g:.1f}% Margem)</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("🗓️ DRE Comparativo Mês a Mês")

        if df_v_g is not None and len(df_v_g) > 0:
            dre_m = df_v_g.groupby("Mês").agg(
                Faturamento=("Valor Total", "sum"),
                RepasseLiquido=("Repasse Líquido", "sum"),
                PecasFisicas=("Peças Físicas", "sum"),
                CMV_Total=("CMV_Item", "sum")
            ).reset_index()

            if df_a_g is not None and len(df_a_g) > 0:
                ads_m = df_a_g.groupby("Mês")["Investimento"].sum().to_dict()
                dre_m["Investimento_Ads"] = dre_m["Mês"].map(lambda m: ads_m.get(m, 0.0))
            else:
                dre_m["Investimento_Ads"] = 0.0

            dre_m["Lucro_Liquido"] = dre_m["RepasseLiquido"] - dre_m["Investimento_Ads"] - dre_m["CMV_Total"]
            dre_m["Margem_Liquida"] = (dre_m["Lucro_Liquido"] / dre_m["Faturamento"] * 100)

            st.dataframe(
                dre_m,
                column_config={
                    "Mês":              st.column_config.TextColumn("Mês / Período"),
                    "Faturamento":      st.column_config.NumberColumn("Faturamento Bruto (R$)", format="R$ %.2f"),
                    "RepasseLiquido":   st.column_config.NumberColumn("Repasse Depositado (R$)", format="R$ %.2f"),
                    "Investimento_Ads": st.column_config.NumberColumn("Investimento Ads (R$)", format="R$ %.2f"),
                    "CMV_Total":        st.column_config.NumberColumn("Custo Produção (R$)", format="R$ %.2f"),
                    "Lucro_Liquido":    st.column_config.NumberColumn("Lucro Líquido Real (R$)", format="R$ %.2f"),
                    "Margem_Liquida":   st.column_config.NumberColumn("Margem Real (%)", format="%.1f%%"),
                },
                use_container_width=True, hide_index=True
            )
        else:
            st.info("Importe relatórios de vendas para visualizar o DRE detalhado.")


# ==========================================================
# MÓDULO 5 — IMPORTAR & GERENCIAR PASTAS DE RELATÓRIOS
# ==========================================================
elif aba == "importar":
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0E1424,#070B14);border:1px solid #1E293B;padding:22px 28px;border-radius:16px;margin-bottom:24px;box-shadow:0 15px 35px rgba(0,0,0,.6)">
        <div style="color:#38BDF8;font-family:'Outfit',sans-serif;font-size:1.7rem;font-weight:800">📤 Importar & Organizar Relatórios</div>
        <div style="color:#94A3B8;font-size:0.95rem;margin-top:6px">Você pode <b>colar os arquivos diretamente nas pastas do computador</b> enquanto baixa das plataformas ou fazer o upload pelo formulário abaixo.</div>
    </div>
    """, unsafe_allow_html=True)

    abs_path_relatorios = os.path.abspath(DIR_RELATORIOS)

    col_imp1, col_imp2 = st.columns([1.2, 1])

    with col_imp1:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0F172A 0%,#080D1A 100%);border:1px solid #38BDF8;border-radius:14px;padding:20px;margin-bottom:20px;box-shadow:0 8px 25px rgba(56,189,248,.1)">
            <div style="color:#38BDF8;font-weight:800;font-size:1.15rem;margin-bottom:10px">📁 Opção 1: Colar Direto no Computador (Recomendado)</div>
            <div style="color:#CBD5E1;font-size:0.88rem;line-height:1.6;margin-bottom:14px">
                Todas as pastas de <b>Anos (2025, 2026, 2027)</b>, <b>Meses (01 a 12)</b> e <b>Plataformas (Shopee, TikTok, Shein, Mercado Livre)</b> já estão criadas no seu Windows.<br><br>
                <b>Caminho no seu PC:</b><br>
                <code style="background:#020617;padding:4px 8px;border-radius:6px;color:#34D399;font-size:0.82rem;word-break:break-all">{abs_path_relatorios}</code>
            </div>
            <div style="color:#94A3B8;font-size:0.8rem">
                <b>Estrutura:</b><br>
                • <code>Vendas / [Ano] / [Mês] / [Plataforma] / seu_arquivo.xlsx</code><br>
                • <code>Ads / [Ano] / [Mês] / [Plataforma] / seu_arquivo.csv</code>
            </div>
        </div>
        """, unsafe_allow_html=True)

        c_btn1, c_btn2 = st.columns(2)
        with c_btn1:
            if st.button("📂 Abrir Pasta no Windows", key="btn_open_folder_explorer", use_container_width=True, type="primary"):
                try:
                    os.startfile(abs_path_relatorios)
                    st.success("Pasta aberta no Windows Explorer!")
                except Exception as e_open:
                    st.info(f"Abra manualmente o caminho: {abs_path_relatorios}")

        with c_btn2:
            if st.button("🔄 Recarregar Dados das Pastas", key="btn_clear_cache_folders", use_container_width=True):
                st.cache_data.clear()
                st.success("✅ Cache limpo e pastas relidas com sucesso!")
                st.rerun()

    with col_imp2:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#0F172A 0%,#080D1A 100%);border:1px solid #1E293B;border-radius:14px;padding:20px;margin-bottom:20px">
            <div style="color:#F8FAFC;font-weight:800;font-size:1.15rem;margin-bottom:10px">📤 Opção 2: Enviar pelo Aplicativo</div>
            <div style="color:#94A3B8;font-size:0.85rem;margin-bottom:12px">O app salvará automaticamente na pasta correspondente.</div>
        </div>
        """, unsafe_allow_html=True)

        with st.form(key="form_import_page_unificado"):
            tipo_u = st.selectbox("Tipo de Relatório:", ["🛒 Vendas Realizadas", "📢 Publicidade (Ads)"], index=0, key="pg_u_form_tipo")
            ano_u = st.selectbox("Ano:", ["2026", "2025", "2027"], index=0, key="pg_u_form_ano")
            mes_u = st.selectbox("Mês:", ["01-Janeiro", "02-Fevereiro", "03-Março", "04-Abril", "05-Maio", "06-Junho", "07-Julho", "08-Agosto", "09-Setembro", "10-Outubro", "11-Novembro", "12-Dezembro"], index=7, key="pg_u_form_mes")
            plat_u = st.selectbox("Plataforma:", ["Shopee", "TikTok", "Mercado Livre", "Shein"], index=0, key="pg_u_form_plat")

            file_u = st.file_uploader("Planilha (.xlsx, .xls ou .csv):", type=["xlsx", "xls", "csv"], key="pg_upl_file_unificado_input")

            if st.form_submit_button("📤 Salvar na Pasta", type="primary", use_container_width=True):
                if file_u is not None:
                    pasta_alvo = "Vendas" if "Vendas" in tipo_u else "Ads"
                    pasta_dest = os.path.join(DIR_RELATORIOS, pasta_alvo, ano_u, mes_u, plat_u)
                    os.makedirs(pasta_dest, exist_ok=True)
                    dest_path = os.path.join(pasta_dest, file_u.name)
                    with open(dest_path, "wb") as fout:
                        fout.write(file_u.getbuffer())
                    st.success(f"✅ Arquivo salvo em: Relatórios/{pasta_alvo}/{ano_u}/{mes_u}/{plat_u}/")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error("Selecione um arquivo para upload.")

    st.markdown("---")

    # Auditoria de Arquivos Detectados nas Pastas
    st.subheader("📋 Relatórios Detectados no Disco (Auditoria em Tempo Real)")
    st.caption("Lista de todas as planilhas encontradas na estrutura de pastas organizadas.")

    import glob
    arquivos_encontrados = []
    for tipo_dir in ["Vendas", "Ads"]:
        path_tipo = os.path.join(DIR_RELATORIOS, tipo_dir)
        if not os.path.exists(path_tipo): continue
        for ano_dir in sorted(os.listdir(path_tipo)):
            path_ano = os.path.join(path_tipo, ano_dir)
            if not os.path.isdir(path_ano): continue
            for mes_dir in sorted(os.listdir(path_ano)):
                path_mes = os.path.join(path_ano, mes_dir)
                if not os.path.isdir(path_mes): continue
                for plat_dir in sorted(os.listdir(path_mes)):
                    path_plat = os.path.join(path_mes, plat_dir)
                    if not os.path.isdir(path_plat): continue
                    for f in glob.glob(os.path.join(path_plat, "*.*")):
                        if f.endswith(".xlsx") or f.endswith(".csv") or f.endswith(".xls"):
                            sz_kb = os.path.getsize(f) / 1024.0
                            arquivos_encontrados.append({
                                "Tipo": "🛒 Vendas" if tipo_dir == "Vendas" else "📢 Ads",
                                "Ano": ano_dir,
                                "Mês": mes_dir,
                                "Plataforma": plat_dir,
                                "Arquivo": os.path.basename(f),
                                "Tamanho": f"{sz_kb:.1f} KB",
                                "Caminho Completo": f
                            })

    if arquivos_encontrados:
        df_audit_arq = pd.DataFrame(arquivos_encontrados)
        st.dataframe(
            df_audit_arq[["Tipo", "Ano", "Mês", "Plataforma", "Arquivo", "Tamanho"]],
            column_config={
                "Tipo":       st.column_config.TextColumn("Tipo de Dado", width="small"),
                "Ano":        st.column_config.TextColumn("Ano", width="small"),
                "Mês":        st.column_config.TextColumn("Mês", width="medium"),
                "Plataforma": st.column_config.TextColumn("Canal", width="medium"),
                "Arquivo":    st.column_config.TextColumn("Nome do Arquivo", width="large"),
                "Tamanho":    st.column_config.TextColumn("Tamanho", width="small"),
            },
            use_container_width=True, hide_index=True
        )
    else:
        st.info("Nenhum relatório encontrado ainda nas pastas. Cole seus arquivos ou envie pelo formulário acima.")

