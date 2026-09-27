import streamlit as st
import pandas as pd
import numpy as np
import os
import json
import altair as alt

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

    /* Ocultar header do Streamlit */
    header[data-testid="stHeader"], .stAppHeader {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    /* Fundo da Aplicação */
    .stApp {
        background: linear-gradient(180deg, #050811 0%, #0B101D 50%, #060912 100%) !important;
        color: #F8FAFC !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    }

    /* Ocultar barra lateral se necessário ou estilizar limpo */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070B14 0%, #050810 100%) !important;
        border-right: 1px solid rgba(56,189,248,0.12) !important;
    }

    /* Estilização dos Inputs */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="base-input"],
    div[data-testid="stNumberInput"] input, div[data-testid="stTextInput"] input,
    input, textarea, select {
        background-color: #101625 !important;
        color: #FFFFFF !important;
        border: 1px solid #1E293B !important;
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Tabelas e Dataframes */
    div[data-testid="stDataFrame"], div[data-testid="stDataEditor"],
    div[role="grid"], div[role="row"], div[role="gridcell"] {
        background-color: #101625 !important;
        color-scheme: dark !important;
    }

    /* Cards e Containers */
    div[data-testid="stExpander"], div[data-testid="stForm"] {
        background-color: #101625 !important;
        border: 1px solid #1E293B !important;
        border-radius: 14px !important;
    }
    
    /* Badges e Tags Visualmente Marcantes */
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

    /* Top Navigation Bar Styling */
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

    /* Orion Card Glassmorphism */
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
# AUTENTICAÇÃO E CONTROLE DE ACESSO
# ---------------------------------------------------------
# ---------------------------------------------------------
# AUTENTICAÇÃO E CONTROLE DE SESSÃO PERSISTENTE
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

# Verificar e restaurar sessão persistente se ainda não autenticado nesta rodada
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
    "aba_ativa":             "Dashboard Geral",
    "produtos":              carregar_produtos_disco(PRODUTOS_PADRAO),
    "presets_taxas":         TAXAS_PADRAO,
    "perfil_fiscal":         p_salvo,
    "aliquota_simples_perc": aliq_salva,
    "roas_meta":             roas_salvo,
    "perfis_custom":         perf_salvo,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def taxas_para_preco(plataforma_nome, preco):
    cfg = st.session_state.presets_taxas.get(plataforma_nome, {"comissao": 14.0, "programa": 0.0, "taxa_fixa": 4.00})
    com_perc = cfg["comissao"] + cfg["programa"]
    taxa_f = cfg["taxa_fixa"]
    desc = f"Comissão {cfg['comissao']}% + Prog. {cfg['programa']}% + Taxa Fixa R$ {taxa_f:.2f}"
    return com_perc, taxa_f, desc

# ---------------------------------------------------------
# BARRA DE NAVEGAÇÃO SUPERIOR (TOP NAVBAR)
# ---------------------------------------------------------
st.markdown(f"""
<div class="nav-header">
    <div>
        <div class="nav-title">🛡️ ORION ENTERPRISE</div>
        <div class="nav-subtitle">Dualis Lingerie — Gestão de Precificação, Margens e Marketplaces</div>
    </div>
    <div style="display:flex;align-items:center;gap:12px">
        <span class="badge-pill badge-blue">👤 {st.session_state.usuario_logado}</span>
        <span class="badge-pill badge-purple">🏛️ {st.session_state.perfil_fiscal} ({st.session_state.aliquota_simples_perc:.1f}%)</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Seletor de Abas no Topo (Design Fluido sem Sidebar poluído)
abas_opcoes = ["📊 Dashboard Executivo", "🏷️ Catálogo & Precificação Mestre", "💰 Central de Vendas & Ads", "⚙️ Configurações Fiscais & Taxas"]

st.markdown("<style>div[data-testid='stSegmentedControl'] {width: 100% !important; margin-bottom: 20px !important;}</style>", unsafe_allow_html=True)
aba_selecionada = st.segmented_control("Navegação Principal", abas_opcoes, default="📊 Dashboard Executivo", label_visibility="collapsed")

# ---------------------------------------------------------
# MÓDULO 1: DASHBOARD EXECUTIVO & GRÁFICOS
# ---------------------------------------------------------
if aba_selecionada == "📊 Dashboard Executivo":
    st.markdown("### 📊 Visão Geral de Desempenho Executivo")
    st.markdown("<p style='color:#94A3B8;font-size:0.9rem'>Resumo consolidado de faturamento, investimentos em Ads, comissões de marketplaces e indicador de margem real.</p>", unsafe_allow_html=True)
    
    # Dados Simulados / Reais para o Dashboard Executivo
    dados_plataformas = pd.DataFrame([
        {"Plataforma": "Shopee", "Faturamento": 48500.00, "Ads": 4200.00, "Comissões": 9700.00, "Devoluções": 1200.00, "Pedidos": 1250},
        {"Plataforma": "TikTok Shop", "Faturamento": 32100.00, "Ads": 3800.00, "Comissões": 3210.00, "Devoluções": 950.00, "Pedidos": 840},
        {"Plataforma": "Mercado Livre", "Faturamento": 28900.00, "Ads": 1800.00, "Comissões": 4335.00, "Devoluções": 600.00, "Pedidos": 620},
        {"Plataforma": "Shein", "Faturamento": 15400.00, "Ads": 850.00, "Comissões": 2464.00, "Devoluções": 310.00, "Pedidos": 410},
    ])
    
    fat_total = dados_plataformas["Faturamento"].sum()
    ads_total = dados_plataformas["Ads"].sum()
    com_total = dados_plataformas["Comissões"].sum()
    dev_total = dados_plataformas["Devoluções"].sum()
    imp_total = fat_total * (st.session_state.aliquota_simples_perc / 100.0)
    cmv_estimado = fat_total * 0.28  # ~28% custo médio do produto
    lucro_estimado = fat_total - (ads_total + com_total + dev_total + imp_total + cmv_estimado)
    margem_perc = (lucro_estimado / fat_total * 100.0) if fat_total > 0 else 0.0

    # Cards de Métricas Principais (Flexbox Responsivo Cyber Navy)
    col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
    with col_m1:
        st.markdown(f"""
        <div class="orion-card">
            <div style="color:#94A3B8;font-size:0.75rem;font-weight:700;text-transform:uppercase">Faturamento Bruto</div>
            <div style="color:#38BDF8;font-family:'Outfit';font-size:1.5rem;font-weight:800;margin-top:4px">R$ {fat_total:,.2f}</div>
            <div style="color:#34D399;font-size:0.75rem;font-weight:700;margin-top:4px">▲ 3.120 Pedidos</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div class="orion-card">
            <div style="color:#94A3B8;font-size:0.75rem;font-weight:700;text-transform:uppercase">Investimento em Ads</div>
            <div style="color:#C084FC;font-family:'Outfit';font-size:1.5rem;font-weight:800;margin-top:4px">R$ {ads_total:,.2f}</div>
            <div style="color:#94A3B8;font-size:0.75rem;font-weight:700;margin-top:4px">ROAS Geral: {fat_total/ads_total:.1f}x</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""
        <div class="orion-card">
            <div style="color:#94A3B8;font-size:0.75rem;font-weight:700;text-transform:uppercase">Comissões de Canais</div>
            <div style="color:#FBBF24;font-family:'Outfit';font-size:1.5rem;font-weight:800;margin-top:4px">R$ {com_total:,.2f}</div>
            <div style="color:#94A3B8;font-size:0.75rem;font-weight:700;margin-top:4px">Média ~{(com_total/fat_total*100):.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m4:
        st.markdown(f"""
        <div class="orion-card">
            <div style="color:#94A3B8;font-size:0.75rem;font-weight:700;text-transform:uppercase">Devoluções / Trocas</div>
            <div style="color:#F87171;font-family:'Outfit';font-size:1.5rem;font-weight:800;margin-top:4px">R$ {dev_total:,.2f}</div>
            <div style="color:#F87171;font-size:0.75rem;font-weight:700;margin-top:4px">Taxa ~{(dev_total/fat_total*100):.1f}%</div>
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

    # GRÁFICOS VISUAIS DE ALTO IMPACTO (ALTAIR DARK THEME)
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.markdown("##### 📈 Faturamento vs. Investimento Ads por Plataforma")
        chart_bar = alt.Chart(dados_plataformas).transform_fold(
            ['Faturamento', 'Ads', 'Comissões'],
            as_=['Métrica', 'Valor']
        ).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
            x=alt.X('Plataforma:N', title=None, axis=alt.Axis(labelAngle=0, labelColor='#CBD5E1')),
            y=alt.Y('Valor:Q', title="Valor em Reais (R$)", axis=alt.Axis(labelColor='#CBD5E1')),
            color=alt.Color('Métrica:N', scale=alt.Scale(
                domain=['Faturamento', 'Ads', 'Comissões'],
                range=['#38BDF8', '#C084FC', '#FBBF24']
            )),
            xOffset='Métrica:N',
            tooltip=['Plataforma', 'Métrica', 'Valor']
        ).properties(height=320).configure_background(fill='transparent').configure_view(strokeWidth=0)
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
        ).properties(height=320).configure_background(fill='transparent').configure_view(strokeWidth=0)
        st.altair_chart(chart_donut, use_container_width=True)

    # ABA DE INTELIGÊNCIA COMERCIAL & ALERTAS (Integrada perfeitamente)
    with st.expander("💡 Insights de Inteligência Comercial & Alertas de Margem", expanded=True):
        col_i1, col_i2 = st.columns([1.2, 1])
        with col_i1:
            st.markdown("""
            * 🟢 **Melhor ROAS Atual:** Mercado Livre Classic apresenta o melhor retorno líquido por real investido em anúncios.
            * ⚠️ **Atenção em TikTok Shop:** O custo de comissão + Ads no TikTok está consumindo 21.8% da receita bruta. Recomendado reajustar preço relâmpago.
            * 📉 **Impacto de Devoluções:** Shopee lidera em devoluções (R$ 1.200,00). Verificar embalagens da categoria *Lingerie Gestante*.
            """)
        with col_i2:
            st.markdown("""
            <div style="background:#0E1424;border:1px solid #1E293B;padding:14px;border-radius:12px">
                <span class="badge-pill badge-green">Curva ABC: Top 3 Produtos</span>
                <ol style="margin-top:8px;padding-left:20px;color:#CBD5E1;font-size:0.88rem">
                    <li><b>Calcinha Gestante</b> (34% das vendas)</li>
                    <li><b>Calcinha Pala Dupla</b> (26% das vendas)</li>
                    <li><b>Cinta Cos Alto</b> (18% das vendas)</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------
# MÓDULO 2: CATÁLOGO & PRECIFICAÇÃO MESTRE (UNIFICADO)
# ---------------------------------------------------------
elif aba_selecionada == "🏷️ Catálogo & Precificação Mestre":
    st.markdown("### 🏷️ Catálogo Unificado & Precificação Praticada")
    st.markdown("<p style='color:#94A3B8;font-size:0.9rem'>Visualize todos os preços praticados em um único local, simule novas margens e salve os preços no disco sem mudar de tela.</p>", unsafe_allow_html=True)
    
    prods = st.session_state.produtos
    nool_prods = len(prods)
    
    # Barra de Ferramentas / Filtro
    col_t1, col_t2, col_t3 = st.columns([1.5, 1, 1])
    with col_t1:
        busca_prod = st.text_input("🔍 Buscar Produto por Nome ou SKU", placeholder="Digite para filtrar...").strip().lower()
    with col_t2:
        plataforma_sel = st.selectbox("🎯 Canal / Marketplace para Diagnóstico", ["Shopee", "TikTok Shop", "Shein", "Mercado Livre (Classic)"])
    with col_t3:
        perfil_sel = st.selectbox("🏛️ Perfil Fiscal (Simulador)", list(PERFIS_PRESETS_PADRAO.keys()), index=0)
        st.session_state.perfil_fiscal = perfil_sel
        st.session_state.aliquota_simples_perc = PERFIS_PRESETS_PADRAO[perfil_sel]["aliquota"]

    prods_filtrados = [p for p in prods if (busca_prod in p["nome"].lower() or busca_prod in p.get("sku", "").lower())]
    
    # MATRIZ GERAL DE PREÇOS PRATICADOS (TABELA COMPLETA)
    st.markdown("#### 📊 Matriz Geral de Preços Praticados & Margens Líquidas")
    
    tabela_dados = []
    simples_frac = st.session_state.aliquota_simples_perc / 100.0
    com_perc, taxa_f, _ = taxas_para_preco(plataforma_sel, 40.0)

    for p in prods_filtrados:
        cmv = p["custo_unitario"] + p["custo_embalagem"]
        precos_p = p.get("precos_praticados", {}).get(plataforma_sel, {})
        
        pr_cheio = precos_p.get("preco_cheio", 49.90)
        pr_oferta = precos_p.get("preco_oferta", 39.90)
        pr_relampago = precos_p.get("preco_relampago", 34.90)
        
        # Cálculo da margem no preço oferta (padrão de análise)
        com_rs = pr_oferta * (com_perc / 100.0) + taxa_f
        imp_rs = pr_oferta * simples_frac
        ads_rs = pr_oferta * (1.0 / st.session_state.roas_meta)
        lucro_rs = pr_oferta - (cmv + com_rs + imp_rs + ads_rs)
        margem_perc = (lucro_rs / pr_oferta * 100.0) if pr_oferta > 0 else 0.0

        tabela_dados.append({
            "SKU": p.get("sku", "-"),
            "Produto": p["nome"],
            "Categoria": p["categoria"],
            "CMV (R$)": f"R$ {cmv:.2f}",
            "Preço Cheio": f"R$ {pr_cheio:.2f}",
            "Preço Oferta": f"R$ {pr_oferta:.2f}",
            "Preço Relâmpago": f"R$ {pr_relampago:.2f}",
            "Lucro Oferta (R$)": f"R$ {lucro_rs:.2f}",
            "Margem Líquida (%)": f"{margem_perc:.1f}%",
            "Status Margem": "🟢 Excelente" if margem_perc >= 15 else ("🟡 Aceitável" if margem_perc >= 5 else "🔴 Atenção/Baixa")
        })

    df_precos = pd.DataFrame(tabela_dados)
    st.dataframe(df_precos, use_container_width=True, hide_index=True)

    st.markdown("---")
    
    # SIMULADOR VISUAL DE PRECIFICAÇÃO E EDIÇÃO POR PRODUTO
    st.markdown("#### ⚡ Simulador de Precificação & Edição de Produto")
    
    nomer_prods = [p["nome"] for p in prods_filtrados]
    if nomer_prods:
        prod_selecionado_nome = st.selectbox("Selecione um Produto para Ajustar Preços e Margens:", nomer_prods)
        idx_prod = next(i for i, p in enumerate(prods) if p["nome"] == prod_selecionado_nome)
        prod_obj = prods[idx_prod]

        col_s1, col_s2 = st.columns([1.2, 1])
        
        with col_s1:
            st.markdown(f"##### 📦 Ajustar Preços Praticados para: **{prod_obj['nome']}**")
            precos_existentes = prod_obj.get("precos_praticados", {}).get(plataforma_sel, {})
            
            val_cheio = st.number_input("Preço Cheio (R$)", value=float(precos_existentes.get("preco_cheio", 49.90)), step=1.0)
            val_oferta = st.number_input("Preço Oferta (R$)", value=float(precos_existentes.get("preco_oferta", 39.90)), step=1.0)
            val_relampago = st.number_input("Preço Oferta Relâmpago (R$)", value=float(precos_existentes.get("preco_relampago", 34.90)), step=1.0)
            
            if st.button("💾 Salvar Preços de Todos os Canais no Disco", type="primary", use_container_width=True):
                if "precos_praticados" not in st.session_state.produtos[idx_prod]:
                    st.session_state.produtos[idx_prod]["precos_praticados"] = {}
                
                st.session_state.produtos[idx_prod]["precos_praticados"][plataforma_sel] = {
                    "preco_cheio": val_cheio,
                    "preco_oferta": val_oferta,
                    "preco_relampago": val_relampago,
                    "usar_roas": True,
                    "roas_esperado": st.session_state.roas_meta
                }
                salvar_produtos_disco(st.session_state.produtos)
                st.success(f"✅ Preços salvos com sucesso para {prod_obj['nome']} em {plataforma_sel}!")
                st.rerun()

        with col_s2:
            st.markdown("##### 🧮 Diagnóstico Automático de Margem")
            cmv = prod_obj["custo_unitario"] + prod_obj["custo_embalagem"]
            
            # Recálculo instantâneo na Oferta
            com_rs = val_oferta * (com_perc / 100.0) + taxa_f
            imp_rs = val_oferta * simples_frac
            ads_rs = val_oferta * (1.0 / st.session_state.roas_meta)
            sobra = val_oferta - (cmv + com_rs + imp_rs + ads_rs)
            m_perc = (sobra / val_oferta * 100.0) if val_oferta > 0 else 0.0

            badge_class = "badge-green" if m_perc >= 15 else ("badge-yellow" if m_perc >= 5 else "badge-red")
            
            st.markdown(f"""
            <div style="background:#0E1526;border:1px solid #1E293B;padding:18px;border-radius:14px">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
                    <span style="color:#94A3B8;font-size:0.85rem;font-weight:700">MARGEM EM OFERTA</span>
                    <span class="badge-pill {badge_class}">{m_perc:.1f}% Líquido</span>
                </div>
                <div style="color:#F8FAFC;font-size:1.1rem;font-weight:700">Sobra por Peça: <span style="color:#38BDF8">R$ {sobra:.2f}</span></div>
                <hr style="border-color:#1E293B;margin:10px 0">
                <div style="font-size:0.8rem;color:#94A3B8">
                    • <b>Custo Produto + Embalagem (CMV):</b> R$ {cmv:.2f}<br>
                    • <b>Comissão {plataforma_sel}:</b> R$ {com_rs:.2f}<br>
                    • <b>Imposto ({st.session_state.perfil_fiscal}):</b> R$ {imp_rs:.2f}<br>
                    • <b>Ads Estimado (ROAS {st.session_state.roas_meta:.1f}x):</b> R$ {ads_rs:.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------
# MÓDULO 3: CENTRAL DE VENDAS & ADS (CONSOLIDADO)
# ---------------------------------------------------------
elif aba_selecionada == "💰 Central de Vendas & Ads":
    st.markdown("### 💰 Central de Relatórios de Vendas & Anúncios")
    st.markdown("<p style='color:#94A3B8;font-size:0.9rem'>Consolidação de relatórios exportados do Upseller, Shopee Ads e TikTok Ads.</p>", unsafe_allow_html=True)
    
    aba_rel = st.radio("Selecione o Relatório:", ["🛒 Relatório de Vendas (Upseller / Multi-loja)", "📢 Desempenho de Anúncios (Shopee & TikTok Ads)"], horizontal=True)
    
    if "Vendas" in aba_rel:
        st.markdown("#### 🛒 Consolidação de Vendas Multi-canal")
        st.info("💡 Coloque os relatórios `.xlsx` ou `.csv` na pasta `arquivos/Relatórios/Vendas/` para processamento automático.")
        
        # Exemplo de visualização demonstrativa limpa
        df_demo_vendas = pd.DataFrame([
            {"Data": "2026-09-25", "Canal": "Shopee", "Pedido": "260925SHP01", "Produto": "Calcinha Gestante", "Qtd": 3, "Valor Bruto": 119.70, "Status": "Concluído"},
            {"Data": "2026-09-25", "Canal": "TikTok Shop", "Pedido": "260925TTK02", "Produto": "Calcinha Pala Dupla", "Qtd": 2, "Valor Bruto": 79.80, "Status": "Concluído"},
            {"Data": "2026-09-26", "Canal": "Mercado Livre", "Pedido": "260926MLB03", "Produto": "Cinta Cos Alto", "Qtd": 1, "Valor Bruto": 69.90, "Status": "Concluído"},
        ])
        st.dataframe(df_demo_vendas, use_container_width=True, hide_index=True)
    else:
        st.markdown("#### 📢 Análise de Desempenho de Ads")
        col_ad1, col_ad2 = st.columns(2)
        with col_ad1:
            st.markdown("##### 🧡 Shopee Ads Summary")
            st.markdown("<span class='badge-pill badge-green'>ROAS Média: 6.8x</span> <span class='badge-pill badge-blue'>Investimento: R$ 4.200,00</span>", unsafe_allow_html=True)
        with col_ad2:
            st.markdown("##### 🎵 TikTok Ads Summary")
            st.markdown("<span class='badge-pill badge-yellow'>ROAS Média: 4.2x</span> <span class='badge-pill badge-purple'>Investimento: R$ 3.800,00</span>", unsafe_allow_html=True)

# ---------------------------------------------------------
# MÓDULO 4: CONFIGURAÇÕES FISCAIS & TAXAS
# ---------------------------------------------------------
elif aba_selecionada == "⚙️ Configurações Fiscais & Taxas":
    st.markdown("### ⚙️ Configurações de Alíquotas e Taxas de Canais")
    st.markdown("<p style='color:#94A3B8;font-size:0.9rem'>Ajuste as taxas de comissão dos marketplaces e alíquotas de imposto do Simples Nacional ou MEI.</p>", unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.markdown("#### 🏛️ Configuração do Perfil Fiscal")
        perf_atual = st.selectbox("Perfil Tributário Ativo", list(st.session_state.perfis_custom.keys()), index=0)
        aliq_val = st.number_input("Alíquota Efetiva do Imposto (%)", value=float(st.session_state.aliquota_simples_perc), step=0.5)
        roas_val = st.number_input("Meta Global de ROAS (x)", value=float(st.session_state.roas_meta), step=0.5)
        
        if st.button("💾 Salvar Configurações Fiscais no Disco", type="primary"):
            st.session_state.perfil_fiscal = perf_atual
            st.session_state.aliquota_simples_perc = aliq_val
            st.session_state.roas_meta = roas_val
            
            cfg_save = {
                "perfil_fiscal": perf_atual,
                "aliquota_simples_perc": aliq_val,
                "roas_meta": roas_val,
                "perfis_custom": st.session_state.perfis_custom
            }
            salvar_config_disco(cfg_save)
            st.success("✅ Configurações salvas no disco com sucesso!")
            st.rerun()

    with col_c2:
        st.markdown("#### 🛍️ Taxas Padrão por Marketplace")
        df_taxas = pd.DataFrame([
            {"Marketplace": k, "Comissão (%)": v["comissao"], "Programa Extra (%)": v["programa"], "Taxa Fixa (R$)": f"R$ {v['taxa_fixa']:.2f}"}
            for k, v in st.session_state.presets_taxas.items()
        ])
        st.dataframe(df_taxas, use_container_width=True, hide_index=True)
