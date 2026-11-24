import streamlit as st


def aplicar_tema_saas():
    """Injeta CSS moderno estilo SaaS escuro para cards, métricas e espaçamento."""
    st.markdown(
        """
        <style>
        .block-container { padding-top: 1.4rem !important; padding-bottom: 2.5rem !important; }
        div[data-testid="stMetric"] {
            background: linear-gradient(145deg, #111827, #0B1120);
            border: 1px solid #1E293B;
            border-left: 4px solid #6366F1;
            border-radius: 12px;
            padding: 14px 16px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
        }
        div[data-testid="stMetricLabel"] p { color: #94A3B8 !important; font-weight: 600 !important; font-size: 0.8rem !important; }
        div[data-testid="stMetricValue"] { color: #F8FAFC !important; font-weight: 800 !important; }
        div[data-testid="stExpander"] {
            background: #0E1424;
            border: 1px solid #1E293B !important;
            border-radius: 12px !important;
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #6366F1, #4F46E5) !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def estilizar_cards_metricas():
    """Aplica estilização extra via streamlit-extras quando disponível."""
    try:
        from streamlit_extras.metric_cards import style_metric_cards
        style_metric_cards(
            background_color="#0F172A",
            border_left_color="#6366F1",
            border_color="#1E293B",
            box_shadow=True,
        )
    except Exception:
        pass


def render_menu_principal(abas_opcoes: list) -> str:
    """Renderiza menu horizontal SaaS com ícones (streamlit-option-menu) e fallback seguro."""
    icones_mapa = {
        "📊 Dashboard": "speedometer2",
        "📦 Produtos & Precificação": "box-seam",
        "📄 Central de Relatórios": "file-earmark-spreadsheet",
        "🚚 Pagamentos a Fornecedores": "truck",
        "🎬 Criativos & Afiliados": "camera-reels",
        "🧠 Otimizador IA": "stars",
    }
    try:
        from streamlit_option_menu import option_menu
        rotulos = [a.split(" ", 1)[1] if " " in a else a for a in abas_opcoes]
        icones = [icones_mapa.get(a, "circle") for a in abas_opcoes]
        escolhido = option_menu(
            menu_title=None,
            options=rotulos,
            icons=icones,
            orientation="horizontal",
            styles={
                "container": {"padding": "4px !important", "background-color": "#0E1424", "border": "1px solid #1E293B", "border-radius": "12px", "margin-bottom": "20px"},
                "icon": {"color": "#818CF8", "font-size": "15px"},
                "nav-link": {"font-size": "13px", "font-weight": "600", "color": "#CBD5E1", "border-radius": "8px", "margin": "0 3px", "padding": "8px 12px"},
                "nav-link-selected": {"background-color": "#4F46E5", "color": "#FFFFFF"},
            },
        )
        idx = rotulos.index(escolhido)
        return abas_opcoes[idx]
    except Exception:
        return st.segmented_control("Navegação Principal", abas_opcoes, default=abas_opcoes[0], label_visibility="collapsed")
