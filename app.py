import streamlit as st
import pandas as pd
import numpy as np
import os
import json
import altair as alt

# ---------------------------------------------------------
# PERSISTÊNCIA DE DADOS EM ARQUIVO LOCAL (JSON) E PASTAS
# ---------------------------------------------------------
ARQUIVO_PRODUTOS   = os.path.join("arquivos", "produtos.json")
ARQUIVO_CFG        = os.path.join("arquivos", "configuracoes.json")
ARQUIVO_PAGAMENTOS = os.path.join("arquivos", "pagamentos_fornecedores.json")
DIR_RELATORIOS     = os.path.join("arquivos", "Relatórios")

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

def carregar_pagamentos_disco():
    defaults_pag = [
        {"id": 1, "data": "2026-09-20", "fornecedor": "Confecção Própria", "produto": "Calcinha Gestante", "qtd_pecas": 500, "valor_peca": 3.65, "total": 1825.00, "status": "Pago"},
        {"id": 2, "data": "2026-09-22", "fornecedor": "Malharia Dualis", "produto": "Cinta Cos Alto", "qtd_pecas": 200, "valor_peca": 7.80, "total": 1560.00, "status": "Pendente"},
    ]
    if os.path.exists(ARQUIVO_PAGAMENTOS):
        try:
            with open(ARQUIVO_PAGAMENTOS, "r", encoding="utf-8") as f:
                dados = json.load(f)
                if isinstance(dados, list):
                    return dados
        except Exception:
            pass
    salvar_pagamentos_disco(defaults_pag)
    return defaults_pag

def salvar_pagamentos_disco(lista_pagamentos):
    try:
        os.makedirs("arquivos", exist_ok=True)
        with open(ARQUIVO_PAGAMENTOS, "w", encoding="utf-8") as f:
            json.dump(lista_pagamentos, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Erro ao salvar pagamentos: {e}")
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
# CONFIGURAÇÃO DA PÁGINA & THEMA CYBER NAVY PREMIUM
# ---------------------------------------------------------
st.set_page_config(
    page_title="ORION Enterprise — Dualis Lingerie",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
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
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070B14 0%, #050810 100%) !important;
        border-right: 1px solid rgba(56,189,248,0.12) !important;
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
    div[role="grid"], div[role="row"], div[role="gridcell"] {
        background-color: #101625 !important;
        color-scheme: dark !important;
    }
    div[data-testid="stExpander"], div[data-testid="stForm"] {
        background-color: #101625 !important;
        border: 1px solid #1E293B !important;
        border-radius: 14px !important;
    }
    .badge-pill {
        display: inline-flex; align-items: center; gap: 5px;
        padding: 5px 14px; border-radius: 20px;
        font-weight: 800; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;
    }
    .badge-green { background: rgba(52,211,153,0.15); color: #34D399; border: 1px solid #34D399; }
    .badge-yellow { background: rgba(251,191,36,0.15); color: #FBBF24; border: 1px solid #FBBF24; }
    .badge-red { background: rgba(248,113,113,0.15); color: #F87171; border: 1px solid #F87171; }
    .badge-blue { background: rgba(56,189,248,0.15); color: #38BDF8; border: 1px solid #38BDF8; }
    .badge-purple { background: rgba(192,132,252,0.15); color: #C084FC; border: 1px solid #C084FC; }

    .nav-header {
        background: linear-gradient(135deg, #0E1526 0%, #0B1020 100%);
        border: 1px solid #1E293B;
        border-radius: 16px;
        padding: 16px 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 16px;
    }
    .nav-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 1.5rem;
        color: #F8FAFC;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .nav-subtitle {
        font-size: 0.82rem;
        color: #38BDF8;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }
    .orion-card {
        background: linear-gradient(135deg, #101625 0%, #0B101D 100%);
        border: 1px solid #1E293B; border-radius: 14px; padding: 20px;
        margin-bottom: 16px; box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .orion-card:hover { border-color: #38BDF8; transform: translateY(-2px); }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# AUTENTICAÇÃO E SESSÃO PERSISTENTE
# ---------------------------------------------------------
USUARIOS_AUTORIZADOS = {
    "Dualis": "Q1w2e3r4",
    "Rafael": "vasco",
    "Lincoln": "Mudar,123",
}

ARQUIVO_SESSAO_LOCAL = os.path.join("arquivos", "sessao_local.json")

def carregar_sessao_persistente():
    if os.path.exists(ARQUIVO_SESSAO_LOCAL):
        try:
            with open(ARQUIVO_SESSAO_LOCAL, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and data.get("autenticado") and data.get("usuario"):
                    return data.get("usuario")
        except Exception:
            pass
    return None

def salvar_sessao_persistente(usuario):
    try:
        os.makedirs("arquivos", exist_ok=True)
        with open(ARQUIVO_SESSAO_LOCAL, "w", encoding="utf-8") as f:
            json.dump({"autenticado": True, "usuario": usuario}, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erro ao salvar sessao: {e}")

def limpar_sessao_persistente():
    if os.path.exists(ARQUIVO_SESSAO_LOCAL):
        try:
            os.remove(ARQUIVO_SESSAO_LOCAL)
        except Exception:
            pass

user_persistente = carregar_sessao_persistente()
if "autenticado" not in st.session_state or not st.session_state["autenticado"]:
    if user_persistente:
        st.session_state["autenticado"] = True
        st.session_state["usuario_logado"] = user_persistente
    else:
        st.session_state["autenticado"] = False
        st.session_state["usuario_logado"] = ""

def tela_login():
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #101625, #080C16); border: 1px solid #1E293B; border-radius: 18px; padding: 36px 30px; box-shadow: 0 25px 60px rgba(0,0,0,0.7); margin-top: 40px; margin-bottom: 24px; text-align: center;">
            <div style="background: linear-gradient(135deg, #38BDF8, #0284C7); width: 60px; height: 60px; border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 28px; margin: 0 auto 16px auto; box-shadow: 0 0 25px rgba(56,189,248,0.4);">🛡️</div>
            <h2 style="font-family: 'Outfit', sans-serif; font-size: 26px; font-weight: 800; color: #F8FAFC; margin-bottom: 4px; letter-spacing: -0.5px;">ORION ENTERPRISE</h2>
            <div style="color: #38BDF8; font-size: 13px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 12px;">Dualis Lingerie</div>
            <p style="color: #94A3B8; font-size: 14px; margin: 0;">Área restrita. Informe suas credenciais de acesso.</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("form_login", clear_on_submit=False):
            usuario_input = st.text_input("Usuário", placeholder="Digite seu usuário").strip()
            senha_input = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            manter_conectado = st.checkbox("📌 Manter conectado neste computador (Auto-login)", value=True)
            st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
            btn_entrar = st.form_submit_button("Entrar no Sistema", use_container_width=True, type="primary")
            
            if btn_entrar:
                usuario_match = None
                for u in USUARIOS_AUTORIZADOS:
                    if u.lower() == usuario_input.lower():
                        usuario_match = u
                        break
                
                if usuario_match and USUARIOS_AUTORIZADOS[usuario_match] == senha_input:
                    st.session_state["autenticado"] = True
                    st.session_state["usuario_logado"] = usuario_match
                    if manter_conectado:
                        salvar_sessao_persistente(usuario_match)
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos.")

if not st.session_state.get("autenticado", False):
    tela_login()
    st.stop()

# ---------------------------------------------------------
# DADOS BASE E SESSION STATE
# ---------------------------------------------------------
PRODUTOS_PADRAO = [
    {"id": 1, "nome": "Calcinha Gestante",   "custo_unitario": 3.65, "custo_embalagem": 0.30, "categoria": "Lingerie Gestante",    "sku": "GEST-01", "fornecedor": "Confecção Própria", "peso_g": 80},
    {"id": 2, "nome": "Calcinha Pala Dupla", "custo_unitario": 3.90, "custo_embalagem": 0.30, "categoria": "Lingerie / Underwear", "sku": "PALA-02", "fornecedor": "Confecção Própria", "peso_g": 75},
    {"id": 3, "nome": "Cinta Cos Baixo",     "custo_unitario": 5.50, "custo_embalagem": 0.30, "categoria": "Cintas & Modeladores", "sku": "CINT-03", "fornecedor": "Confecção Própria", "peso_g": 120},
    {"id": 4, "nome": "Cinta Cos Alto",      "custo_unitario": 7.80, "custo_embalagem": 0.30, "categoria": "Cintas & Modeladores", "sku": "CINT-04", "fornecedor": "Confecção Própria", "peso_g": 150},
    {"id": 5, "nome": "Galena",              "custo_unitario": 6.00, "custo_embalagem": 0.30, "categoria": "Lingerie / Underwear", "sku": "GAL-05",  "fornecedor": "Confecção Própria", "peso_g": 90},
    {"id": 6, "nome": "Fio dental",          "custo_unitario": 1.00, "custo_embalagem": 0.30, "categoria": "Fio Dental",           "sku": "FIO-06",  "fornecedor": "Confecção Própria", "peso_g": 40},
    {"id": 7, "nome": "Regulagem",           "custo_unitario": 2.10, "custo_embalagem": 0.30, "categoria": "Lingerie / Underwear", "sku": "REG-07",  "fornecedor": "Confecção Própria", "peso_g": 65},
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

defaults = {
    "produtos":              carregar_produtos_disco(PRODUTOS_PADRAO),
    "pagamentos":            carregar_pagamentos_disco(),
    "presets_taxas":         TAXAS_PADRAO,
    "perfil_fiscal":         p_salvo,
    "aliquota_simples_perc": aliq_salva,
    "roas_meta":             roas_salvo,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def taxas_para_preco(plataforma_nome, preco):
    """
    Calcula automaticamente as comissões e taxas fixas oficiais de 2026 por patamar de preço.
    """
    if "Shopee" in plataforma_nome:
        if preco < 80.00:
            return 20.0, 4.00
        elif preco < 100.00:
            return 14.0, 16.00
        elif preco < 200.00:
            return 14.0, 20.00
        else:
            return 14.0, 26.00
            
    elif "TikTok" in plataforma_nome:
        if preco < 50.00:
            return 16.0, 4.00
        else:
            return 12.0, 6.00

    elif "Shein" in plataforma_nome:
        return 16.0, 3.00

    elif "Classic" in plataforma_nome:
        taxa_f = 6.00 if preco < 79.00 else 0.00
        return 12.0, taxa_f

    elif "Premium" in plataforma_nome:
        taxa_f = 6.00 if preco < 79.00 else 0.00
        return 16.5, taxa_f

    cfg = st.session_state.presets_taxas.get(plataforma_nome, {"comissao": 14.0, "programa": 0.0, "taxa_fixa": 4.00})
    return cfg["comissao"] + cfg["programa"], cfg["taxa_fixa"]

# ---------------------------------------------------------
# BARRA DE NAVEGAÇÃO SUPERIOR (TOP NAVBAR - ABAS FIXAS)
# ---------------------------------------------------------
st.markdown(f"""
<div class="nav-header">
    <div>
        <div class="nav-title">🛡️ ORION ENTERPRISE</div>
        <div class="nav-subtitle">Dualis Lingerie — Gestão Integrada de Vendas, Precificação e Fornecedores</div>
    </div>
    <div style="display:flex;align-items:center;gap:12px">
        <span class="badge-pill badge-blue">👤 {st.session_state.usuario_logado}</span>
        <span class="badge-pill badge-purple">🏛️ {st.session_state.perfil_fiscal} ({st.session_state.aliquota_simples_perc:.1f}%)</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ABAS FIXAS DO NAVEGADOR
abas_opcoes = [
    "📊 Dashboard",
    "📦 Produtos & Precificação",
    "📄 Central de Relatórios",
    "🚚 Pagamentos a Fornecedores"
]

st.markdown("<style>div[data-testid='stSegmentedControl'] {width: 100% !important; margin-bottom: 24px !important;}</style>", unsafe_allow_html=True)
aba_selecionada = st.segmented_control("Navegação Principal", abas_opcoes, default="📊 Dashboard", label_visibility="collapsed")

# ---------------------------------------------------------
# ABA 1: DASHBOARD
# ---------------------------------------------------------
if aba_selecionada == "📊 Dashboard":
    st.markdown("### 📊 Visão Geral de Desempenho Executivo")
    st.markdown("<p style='color:#94A3B8;font-size:0.9rem'>Consolidação estratégica de vendas, investimentos em Ads, comissões de canais e lucro líquido real.</p>", unsafe_allow_html=True)
    
    # BARRA DE FILTROS DINÂMICOS DO DASHBOARD
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        ano_filtro = st.selectbox("📅 Ano de Referência", ["2026", "2025", "2027", "Todos os Anos"], index=0)
    with col_f2:
        mes_filtro = st.selectbox("🗓️ Mês de Referência", ["Todos os Meses", "01-Janeiro", "02-Fevereiro", "03-Março", "04-Abril", "05-Maio", "06-Junho", "07-Julho", "08-Agosto", "09-Setembro", "10-Outubro", "11-Novembro", "12-Dezembro"], index=9)
    with col_f3:
        plat_filtro = st.selectbox("🎯 Plataforma / Marketplace", ["Todas as Plataformas", "Shopee", "TikTok Shop", "Mercado Livre", "Shein"], index=0)

    # Base de dados com suporte a filtros de Ano, Mês e Plataforma
    dados_brutos = pd.DataFrame([
        {"Plataforma": "Shopee", "Faturamento": 48500.00, "Ads": 4200.00, "Comissões": 9700.00, "Devoluções": 1200.00, "Pedidos": 1250, "Mês": "09-Setembro", "Ano": "2026"},
        {"Plataforma": "TikTok Shop", "Faturamento": 32100.00, "Ads": 3800.00, "Comissões": 3210.00, "Devoluções": 950.00, "Pedidos": 840, "Mês": "09-Setembro", "Ano": "2026"},
        {"Plataforma": "Mercado Livre", "Faturamento": 28900.00, "Ads": 1800.00, "Comissões": 4335.00, "Devoluções": 600.00, "Pedidos": 620, "Mês": "09-Setembro", "Ano": "2026"},
        {"Plataforma": "Shein", "Faturamento": 15400.00, "Ads": 850.00, "Comissões": 2464.00, "Devoluções": 310.00, "Pedidos": 410, "Mês": "09-Setembro", "Ano": "2026"},

        {"Plataforma": "Shopee", "Faturamento": 42100.00, "Ads": 3900.00, "Comissões": 8420.00, "Devoluções": 1100.00, "Pedidos": 1100, "Mês": "08-Agosto", "Ano": "2026"},
        {"Plataforma": "TikTok Shop", "Faturamento": 29800.00, "Ads": 3400.00, "Comissões": 2980.00, "Devoluções": 880.00, "Pedidos": 790, "Mês": "08-Agosto", "Ano": "2026"},
        {"Plataforma": "Mercado Livre", "Faturamento": 26500.00, "Ads": 1600.00, "Comissões": 3975.00, "Devoluções": 550.00, "Pedidos": 580, "Mês": "08-Agosto", "Ano": "2026"},
        {"Plataforma": "Shein", "Faturamento": 13900.00, "Ads": 750.00, "Comissões": 2224.00, "Devoluções": 290.00, "Pedidos": 370, "Mês": "08-Agosto", "Ano": "2026"},
    ])

    # Filtragem Dinâmica
    dados_plataformas = dados_brutos.copy()
    if ano_filtro != "Todos os Anos":
        dados_plataformas = dados_plataformas[dados_plataformas["Ano"] == ano_filtro]
    if mes_filtro != "Todos os Meses":
        dados_plataformas = dados_plataformas[dados_plataformas["Mês"] == mes_filtro]
    if plat_filtro != "Todas as Plataformas":
        dados_plataformas = dados_plataformas[dados_plataformas["Plataforma"] == plat_filtro]

    if len(dados_plataformas) == 0:
        dados_plataformas = dados_brutos[dados_brutos["Mês"] == "09-Setembro"]

    st.markdown(f"""
    <div style="margin:12px 0 16px 0;display:flex;gap:10px">
        <span class="badge-pill badge-blue">📅 Ano: {ano_filtro}</span>
        <span class="badge-pill badge-purple">🗓️ Mês: {mes_filtro}</span>
        <span class="badge-pill badge-green">🎯 Canal: {plat_filtro}</span>
    </div>
    """, unsafe_allow_html=True)

    fat_total = dados_plataformas["Faturamento"].sum()
    ads_total = dados_plataformas["Ads"].sum()
    com_total = dados_plataformas["Comissões"].sum()
    dev_total = dados_plataformas["Devoluções"].sum()
    ped_total = dados_plataformas["Pedidos"].sum()
    imp_total = fat_total * (st.session_state.aliquota_simples_perc / 100.0)
    cmv_estimado = fat_total * 0.28
    lucro_estimado = fat_total - (ads_total + com_total + dev_total + imp_total + cmv_estimado)
    margem_perc = (lucro_estimado / fat_total * 100.0) if fat_total > 0 else 0.0

    col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
    with col_m1:
        st.markdown(f"""
        <div class="orion-card">
            <div style="color:#94A3B8;font-size:0.75rem;font-weight:700;text-transform:uppercase">Faturamento Bruto</div>
            <div style="color:#38BDF8;font-family:'Outfit';font-size:1.5rem;font-weight:800;margin-top:4px">R$ {fat_total:,.2f}</div>
            <div style="color:#34D399;font-size:0.75rem;font-weight:700;margin-top:4px">▲ {ped_total:,} Pedidos</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div class="orion-card">
            <div style="color:#94A3B8;font-size:0.75rem;font-weight:700;text-transform:uppercase">Investimento em Ads</div>
            <div style="color:#C084FC;font-family:'Outfit';font-size:1.5rem;font-weight:800;margin-top:4px">R$ {ads_total:,.2f}</div>
            <div style="color:#94A3B8;font-size:0.75rem;font-weight:700;margin-top:4px">ROAS Geral: {(fat_total/ads_total if ads_total>0 else 0):.1f}x</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""
        <div class="orion-card">
            <div style="color:#94A3B8;font-size:0.75rem;font-weight:700;text-transform:uppercase">Comissões de Canais</div>
            <div style="color:#FBBF24;font-family:'Outfit';font-size:1.5rem;font-weight:800;margin-top:4px">R$ {com_total:,.2f}</div>
            <div style="color:#94A3B8;font-size:0.75rem;font-weight:700;margin-top:4px">Média ~{(com_total/fat_total*100 if fat_total>0 else 0):.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m4:
        st.markdown(f"""
        <div class="orion-card">
            <div style="color:#94A3B8;font-size:0.75rem;font-weight:700;text-transform:uppercase">Devoluções / Trocas</div>
            <div style="color:#F87171;font-family:'Outfit';font-size:1.5rem;font-weight:800;margin-top:4px">R$ {dev_total:,.2f}</div>
            <div style="color:#F87171;font-size:0.75rem;font-weight:700;margin-top:4px">Taxa ~{(dev_total/fat_total*100 if fat_total>0 else 0):.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m5:
        st.markdown(f"""
        <div class="orion-card" style="border-color:#34D399">
            <div style="color:#94A3B8;font-size:0.75rem;font-weight:700;text-transform:uppercase">Lucro Líquido Real</div>
            <div style="color:#34D399;font-family:'Outfit';font-size:1.5rem;font-weight:800;margin-top:4px">R$ {lucro_estimado:,.2f}</div>
            <div style="color:#34D399;font-size:0.75rem;font-weight:700;margin-top:4px">Margem Real: {margem_perc:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("##### 📈 Faturamento vs. Investimento Ads por Plataforma")
        df_chart_melt = pd.melt(
            dados_plataformas,
            id_vars=['Plataforma'],
            value_vars=['Faturamento', 'Ads', 'Comissões'],
            var_name='Métrica',
            value_name='Valor'
        )
        chart_bar = alt.Chart(df_chart_melt).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
            x=alt.X('Plataforma:N', title=None, axis=alt.Axis(labelAngle=0, labelColor='#CBD5E1')),
            y=alt.Y('Valor:Q', title="Valor em Reais (R$)", axis=alt.Axis(labelColor='#CBD5E1')),
            color=alt.Color('Métrica:N', scale=alt.Scale(
                domain=['Faturamento', 'Ads', 'Comissões'],
                range=['#38BDF8', '#C084FC', '#FBBF24']
            )),
            tooltip=['Plataforma', 'Métrica', 'Valor']
        ).properties(height=320)
        st.altair_chart(chart_bar, use_container_width=True)

    with col_g2:
        st.markdown("##### 🍩 Distribuição do Faturamento por Marketplace")
        chart_donut = alt.Chart(dados_plataformas).mark_arc(innerRadius=60).encode(
            theta=alt.Theta(field="Faturamento", type="quantitative"),
            color=alt.Color(field="Plataforma", type="nominal", scale=alt.Scale(
                domain=['Shopee', 'TikTok Shop', 'Mercado Livre', 'Shein'],
                range=['#EE4D2D', '#00F2FE', '#FFE600', '#FF4081']
            )),
            tooltip=['Plataforma', 'Faturamento', 'Pedidos']
        ).properties(height=320)
        st.altair_chart(chart_donut, use_container_width=True)

# ---------------------------------------------------------
# ABA 2: PRODUTOS (PRECIFICAÇÃO DE KITS 1 A 10 & ANÁLISE)
# ---------------------------------------------------------
elif aba_selecionada == "📦 Produtos & Precificação":
    sub_aba_prod = st.radio("Selecione a Visão:", ["🏷️ Precificação Atual de Kits (1 a 10 Peças)", "📈 Análise de Performance do Produto"], horizontal=True)
    
    prods = st.session_state.produtos
    
    if "Precificação" in sub_aba_prod:
        st.markdown("### 🏷️ Precificação por Kits (1 a 10 Peças) — 3 Campos de Preço")
        st.markdown("<p style='color:#94A3B8;font-size:0.9rem'>Preço Relâmpago (base mínima com lucro + Ads + comissão), Oferta Normal (~11% desconto) e Preço Cheio (~19% desconto).</p>", unsafe_allow_html=True)
        
        col_p1, col_p2, col_p3 = st.columns([1.5, 1, 1])
        with col_p1:
            prod_nomes = [p["nome"] for p in prods]
            prod_sel_nome = st.selectbox("Selecione o Produto:", prod_nomes)
            idx_prod = next(i for i, p in enumerate(prods) if p["nome"] == prod_sel_nome)
            prod_obj = prods[idx_prod]
        with col_p2:
            plat_sel = st.selectbox("Marketplace / Canal:", ["Shopee", "TikTok Shop", "Shein", "Mercado Livre (Classic)", "Mercado Livre (Premium)"])
        with col_p3:
            perfil_tributario = st.selectbox("Perfil Fiscal:", list(PERFIS_PRESETS_PADRAO.keys()), index=0)
            aliq_imp = PERFIS_PRESETS_PADRAO[perfil_tributario]["aliquota"]

        com_padrao, taxa_f_padrao = taxas_para_preco(plat_sel, 50.0)
        custo_un = prod_obj["custo_unitario"]
        custo_emb = prod_obj["custo_embalagem"]
        
        # Painel Interativo de Parâmetros Editáveis por Canal
        with st.expander(f"⚙️ Ajustar Métricas & Regras de Precificação — {plat_sel}", expanded=True):
            modo_comissao = st.radio("Cálculo de Comissão:", ["🤖 Automático Oficial 2026 (Por Faixa de Preço)", "✏️ Manual Customizado"], horizontal=True)
            
            col_cfg1, col_cfg2, col_cfg3, col_cfg4 = st.columns(4)
            with col_cfg1:
                if "Automático" in modo_comissao:
                    st.markdown("**Comissão do Canal:**")
                    st.markdown("<span class='badge-pill badge-blue'>🤖 Regra 2026 Ativa</span>", unsafe_allow_html=True)
                    com_perc_manual = None
                else:
                    com_perc_manual = st.number_input("Comissão do Canal (%)", value=float(com_padrao), step=0.5)
            with col_cfg2:
                if "Automático" in modo_comissao:
                    st.markdown("**Taxa Fixa:**")
                    st.markdown("<span class='badge-pill badge-purple'>🤖 Faixa Dinâmica</span>", unsafe_allow_html=True)
                    taxa_f_manual = None
                else:
                    taxa_f_manual = st.number_input("Taxa Fixa por Item (R$)", value=float(taxa_f_padrao), step=0.50)
            with col_cfg3:
                usar_ads = st.checkbox("📢 Incluir Custo de Ads / ROAS", value=True)
                roas_val = st.number_input("Meta ROAS (x)", value=float(st.session_state.roas_meta), step=0.5) if usar_ads else 0.0
            with col_cfg4:
                st.markdown("**Margem Relâmpago (Piso):**")
                st.markdown("<span class='badge-pill badge-green'>🔒 20.0% FIXA</span>", unsafe_allow_html=True)

        st.markdown(f"##### 📋 Precificação de Kits (1 a 10 Peças) — **{prod_obj['nome']}** na **{plat_sel}**")
        st.caption(f"CMV Unitário: R$ {custo_un:.2f} | Embalagem: R$ {custo_emb:.2f} | Imposto: {aliq_imp:.1f}% | Margem Mínima: 20.0% | Ads: {'Ativado (' + str(roas_val) + 'x)' if usar_ads else 'OFF'}")

        precos_salvos_kits = prod_obj.get("precos_kits", {}).get(plat_sel, {})
        margem_meta_perc = 20.0
        acos_perc = (100.0 / roas_val) if (usar_ads and roas_val > 0) else 0.0

        dados_kits_tabela = []
        for qtd in range(1, 11):
            key_qtd = str(qtd)
            cmv_kit = (custo_un * qtd) + custo_emb
            
            # Estimativa de faixa para aplicar a comissão oficial 2026 ou usar manual
            estimativa_preco = (cmv_kit * 2.2) + 4.00
            if "Automático" in modo_comissao:
                com_perc, taxa_f = taxas_para_preco(plat_sel, estimativa_preco)
            else:
                com_perc = com_perc_manual if com_perc_manual is not None else com_padrao
                taxa_f = taxa_f_manual if taxa_f_manual is not None else taxa_f_padrao

            fator_deducao = (1.0 - (com_perc / 100.0) - (aliq_imp / 100.0) - (acos_perc / 100.0) - (margem_meta_perc / 100.0))
            if fator_deducao <= 0.05:
                fator_deducao = 0.20

            relampago_sugerido = round((cmv_kit + taxa_f) / fator_deducao, 2)
            
            # Recalcular comissão exata sobre a sugestão final
            if "Automático" in modo_comissao:
                com_perc, taxa_f = taxas_para_preco(plat_sel, relampago_sugerido)
                fator_deducao = (1.0 - (com_perc / 100.0) - (aliq_imp / 100.0) - (acos_perc / 100.0) - (margem_meta_perc / 100.0))
                if fator_deducao <= 0.05:
                    fator_deducao = 0.20
                relampago_sugerido = round((cmv_kit + taxa_f) / fator_deducao, 2)

            oferta_sugerida = round(relampago_sugerido / 0.89, 2)
            cheio_sugerido = round(oferta_sugerida / 0.81, 2)

            p_relampago = float(precos_salvos_kits.get(key_qtd, {}).get("preco_relampago", relampago_sugerido))
            p_oferta = float(precos_salvos_kits.get(key_qtd, {}).get("preco_oferta", oferta_sugerida))
            p_cheio = float(precos_salvos_kits.get(key_qtd, {}).get("preco_cheio", cheio_sugerido))

            # Recálculo final da comissão sobre o preço relâmpago praticado
            if "Automático" in modo_comissao:
                com_perc, taxa_f = taxas_para_preco(plat_sel, p_relampago)

            comissao_rs = (p_relampago * (com_perc / 100.0)) + taxa_f
            imposto_rs = p_relampago * (aliq_imp / 100.0)
            ads_rs = (p_relampago * (acos_perc / 100.0)) if usar_ads else 0.0
            sobra_rs = p_relampago - (cmv_kit + comissao_rs + imposto_rs + ads_rs)
            margem_pct = (sobra_rs / p_relampago * 100.0) if p_relampago > 0 else 0.0

            dados_kits_tabela.append({
                "Qtd Peças": f"Kit {qtd}x",
                "CMV Kit (R$)": cmv_kit,
                "⚡ Preço Relâmpago (R$)": p_relampago,
                "🔥 Oferta Normal (R$)": p_oferta,
                "🏷️ Preço Cheio (R$)": p_cheio,
                "Lucro Relâmpago (R$)": round(sobra_rs, 2),
                "Margem Relâmpago (%)": round(margem_pct, 1),
                "Status": "🟢 Excelente" if margem_pct >= 20 else ("🟡 Aceitável" if margem_pct >= 10 else "🔴 Atenção")
            })

        df_kits_display = pd.DataFrame(dados_kits_tabela)

        with st.form("form_kits"):
            st.markdown("##### ✏️ Edição dos 3 Campos de Preço por Kit (1 a 10 unidades)")
            df_edited = st.data_editor(
                df_kits_display[["Qtd Peças", "CMV Kit (R$)", "⚡ Preço Relâmpago (R$)", "🔥 Oferta Normal (R$)", "🏷️ Preço Cheio (R$)", "Lucro Relâmpago (R$)", "Margem Relâmpago (%)", "Status"]],
                disabled=["Qtd Peças", "CMV Kit (R$)", "Lucro Relâmpago (R$)", "Margem Relâmpago (%)", "Status"],
                column_config={
                    "⚡ Preço Relâmpago (R$)": st.column_config.NumberColumn(format="R$ %.2f", min_value=1.0, step=1.0),
                    "🔥 Oferta Normal (R$)": st.column_config.NumberColumn(format="R$ %.2f", min_value=1.0, step=1.0),
                    "🏷️ Preço Cheio (R$)": st.column_config.NumberColumn(format="R$ %.2f", min_value=1.0, step=1.0),
                },
                use_container_width=True,
                hide_index=True
            )
            
            st.markdown("""
            <div style="background:#0E1424;border:1px solid #1E293B;padding:14px;border-radius:12px;margin-top:10px">
                <span style="color:#38BDF8;font-weight:700">💡 Estratégia de Descontos Automáticos:</span>
                <ul style="color:#94A3B8;font-size:0.85rem;margin-top:4px;padding-left:18px">
                    <li><b>⚡ Preço Relâmpago (Piso Mínimo):</b> Cobre CMV + Comissões + Imposto + Ads com lucro garantido.</li>
                    <li><b>🔥 Oferta Normal:</b> ~11% superior para destacar o selo de desconto relâmpago.</li>
                    <li><b>🏷️ Preço Cheio:</b> ~19% superior à Oferta Normal para destacar a promoção De / Por.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

            btn_salvar_kits = st.form_submit_button("💾 Salvar Tabela Completa de Kits no Disco", type="primary", use_container_width=True)
            if btn_salvar_kits:
                if "precos_kits" not in st.session_state.produtos[idx_prod]:
                    st.session_state.produtos[idx_prod]["precos_kits"] = {}
                if plat_sel not in st.session_state.produtos[idx_prod]["precos_kits"]:
                    st.session_state.produtos[idx_prod]["precos_kits"][plat_sel] = {}

                for row in df_edited.to_dict(orient="records"):
                    qtd_str = str(row["Qtd Peças"].replace("Kit ", "").replace("x", "").strip())
                    st.session_state.produtos[idx_prod]["precos_kits"][plat_sel][qtd_str] = {
                        "preco_relampago": float(row["⚡ Preço Relâmpago (R$)"]),
                        "preco_oferta": float(row["🔥 Oferta Normal (R$)"]),
                        "preco_cheio": float(row["🏷️ Preço Cheio (R$)"])
                    }
                
                salvar_produtos_disco(st.session_state.produtos)
                st.success(f"✅ Tabela de 3 preços para os 10 kits de {prod_obj['nome']} em {plat_sel} foi salva com sucesso no disco!")
                st.rerun()

    else:
        st.markdown("### 📈 Análise de Performance por Produto")
        prod_sel_perf = st.selectbox("Selecione o Produto para Analisar:", [p["nome"] for p in prods])
        
        col_an1, col_an2, col_an3 = st.columns(3)
        with col_an1:
            st.markdown("""
            <div class="orion-card">
                <div style="color:#94A3B8;font-size:0.8rem">TOTAL DE VENDAS</div>
                <div style="color:#38BDF8;font-size:1.6rem;font-weight:800">1.250 Unidades</div>
            </div>
            """, unsafe_allow_html=True)
        with col_an2:
            st.markdown("""
            <div class="orion-card">
                <div style="color:#94A3B8;font-size:0.8rem">FATURAMENTO ACUMULADO</div>
                <div style="color:#34D399;font-size:1.6rem;font-weight:800">R$ 48.500,00</div>
            </div>
            """, unsafe_allow_html=True)
        with col_an3:
            st.markdown("""
            <div class="orion-card">
                <div style="color:#94A3B8;font-size:0.8rem">MARGEM MÉDIA REAL</div>
                <div style="color:#FBBF24;font-size:1.6rem;font-weight:800">18.4%</div>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------
# ABA 3: CENTRAL DE RELATÓRIOS
# ---------------------------------------------------------
elif aba_selecionada == "📄 Central de Relatórios":
    st.markdown("### 📄 Central de Relatórios de Vendas & Ads")
    st.markdown("<p style='color:#94A3B8;font-size:0.9rem'>Faça o upload dos relatórios exportados da Shopee, TikTok Shop, Shein, Mercado Livre e Upseller.</p>", unsafe_allow_html=True)
    
    col_r1, col_r2 = st.columns([1.5, 1])
    with col_r1:
        st.markdown("##### 📤 Importar Novo Relatório")
        tipo_rel = st.selectbox("Tipo de Relatório:", ["Vendas", "Ads / Anúncios"])
        plat_rel = st.selectbox("Plataforma / Origem:", ["Shopee", "TikTok Shop", "Shein", "Mercado Livre", "Upseller"])
        ano_rel  = st.selectbox("Ano:", ["2025", "2026", "2027"])
        mes_rel  = st.selectbox("Mês:", ['01-Janeiro', '02-Fevereiro', '03-Março', '04-Abril', '05-Maio', '06-Junho', '07-Julho', '08-Agosto', '09-Setembro', '10-Outubro', '11-Novembro', '12-Dezembro'])

        uploaded_file = st.file_uploader("Selecione o arquivo (.csv ou .xlsx)", type=["csv", "xlsx"])
        if uploaded_file is not None:
            if st.button("💾 Salvar Relatório na Pasta do Sistema", type="primary"):
                pasta_destino = os.path.join(DIR_RELATORIOS, tipo_rel, ano_rel, mes_rel, plat_rel)
                os.makedirs(pasta_destino, exist_ok=True)
                caminho_final = os.path.join(pasta_destino, uploaded_file.name)
                
                with open(caminho_final, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.success(f"✅ Relatório **{uploaded_file.name}** salvo com sucesso em `{pasta_destino}`!")

    with col_r2:
        st.markdown("##### 📁 Relatórios Armazenados em Disco")
        st.markdown("""
        <div style="background:#0E1424;border:1px solid #1E293B;padding:16px;border-radius:12px">
            <span style="color:#34D399;font-weight:700">● Sistema de Diretórios Ativo:</span>
            <ul style="color:#CBD5E1;font-size:0.85rem;margin-top:8px;padding-left:18px">
                <li><code>arquivos/Relatórios/Vendas/</code></li>
                <li><code>arquivos/Relatórios/Ads/</code></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# ABA 4: PAGAMENTOS A FORNECEDORES
# ---------------------------------------------------------
elif aba_selecionada == "🚚 Pagamentos a Fornecedores":
    st.markdown("### 🚚 Central de Pagamentos a Fornecedores")
    st.markdown("<p style='color:#94A3B8;font-size:0.9rem'>Registre os lotes de confecção adquiridos, peças pegas, valores unitários e acompanhe o histórico de pagamentos.</p>", unsafe_allow_html=True)
    
    col_f1, col_f2 = st.columns([1.2, 1.8])
    
    with col_f1:
        st.markdown("##### ➕ Registrar Novo Lote / Pagamento")
        with st.form("form_fornecedor"):
            data_lote = st.date_input("Data da Compra / Entrada")
            fornecedor_input = st.text_input("Fornecedor / Oficina", placeholder="Ex: Confecção Própria, Malharia Dualis").strip()
            prod_forn = st.selectbox("Produto Adquirido:", [p["nome"] for p in st.session_state.produtos])
            qtd_pecas = st.number_input("Quantidade de Peças Pegas", min_value=1, value=100, step=10)
            valor_peca = st.number_input("Valor por Peça (R$)", min_value=0.10, value=3.65, step=0.10)
            status_pag = st.selectbox("Status do Pagamento", ["Pendente", "Pago", "Parcial"])
            
            total_calculado = qtd_pecas * valor_peca
            st.markdown(f"**Total do Lote:** <span style='color:#38BDF8;font-weight:800;font-size:1.1rem'>R$ {total_calculado:,.2f}</span>", unsafe_allow_html=True)
            
            btn_add_forn = st.form_submit_button("💾 Salvar Registro de Fornecedor", type="primary", use_container_width=True)
            if btn_add_forn:
                novo_reg = {
                    "id": len(st.session_state.pagamentos) + 1,
                    "data": str(data_lote),
                    "fornecedor": fornecedor_input if fornecedor_input else "Confecção Própria",
                    "produto": prod_forn,
                    "qtd_pecas": int(qtd_pecas),
                    "valor_peca": float(valor_peca),
                    "total": float(total_calculado),
                    "status": status_pag
                }
                st.session_state.pagamentos.append(novo_reg)
                salvar_pagamentos_disco(st.session_state.pagamentos)
                st.success("✅ Registro de fornecedor salvo no disco com sucesso!")
                st.rerun()

    with col_f2:
        st.markdown("##### 📊 Histórico de Registros de Pagamento")
        df_pags = pd.DataFrame(st.session_state.pagamentos)
        if len(df_pags) > 0:
            df_display = df_pags.rename(columns={
                "data": "Data", "fornecedor": "Fornecedor", "produto": "Produto",
                "qtd_pecas": "Peças", "valor_peca": "Valor Peça (R$)", "total": "Total (R$)", "status": "Status"
            })
            st.dataframe(df_display[["Data", "Fornecedor", "Produto", "Peças", "Valor Peça (R$)", "Total (R$)", "Status"]], use_container_width=True, hide_index=True)
            
            tot_geral = df_pags["total"].sum()
            tot_pago = df_pags[df_pags["status"] == "Pago"]["total"].sum()
            tot_pend = df_pags[df_pags["status"] == "Pendente"]["total"].sum()
            
            st.markdown(f"""
            <div style="display:flex;gap:12px;margin-top:16px">
                <span class="badge-pill badge-blue">Total Lotes: R$ {tot_geral:,.2f}</span>
                <span class="badge-pill badge-green">Pago: R$ {tot_pago:,.2f}</span>
                <span class="badge-pill badge-yellow">Pendente: R$ {tot_pend:,.2f}</span>
            </div>
            """, unsafe_allow_html=True)
