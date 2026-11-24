import streamlit as st


def aplicar_tema_saas():
    """Injeta CSS moderno estilo SaaS escuro para sidebar, cards, abas e métricas."""
    st.markdown(
        """
        <style>
        .block-container { padding-top: 1.2rem !important; padding-bottom: 2.5rem !important; max-width: 1400px; }
        section[data-testid="stSidebar"] {
            background: #0A0F1D !important;
            border-right: 1px solid #1E293B !important;
        }
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


def render_menu_principal(abas_opcoes: list, total_produtos: int = 0) -> str:
    """Renderiza navegação vertical limpa na Sidebar liberando 100% da área útil."""
    icones_mapa = {
        "📊 Dashboard": "speedometer2",
        "📦 Produtos & Precificação": "box-seam",
        "📄 Central de Relatórios": "file-earmark-spreadsheet",
        "🚚 Pagamentos a Fornecedores": "truck",
        "🎬 Criativos & Afiliados": "camera-reels",
        "🧠 Otimizador IA": "stars",
    }
    with st.sidebar:
        st.markdown(
            "<div style='padding:6px 4px 12px 4px'>"
            "<div style='font-size:1.1rem;font-weight:800;color:#F8FAFC'>🛡️ ORION ENTERPRISE</div>"
            "<div style='font-size:0.75rem;color:#94A3B8'>Dualis Lingerie • Gestão Integrada</div>"
            "</div>",
            unsafe_allow_html=True,
        )
        try:
            from streamlit_option_menu import option_menu
            rotulos = [a.split(" ", 1)[1] if " " in a else a for a in abas_opcoes]
            icones = [icones_mapa.get(a, "circle") for a in abas_opcoes]
            escolhido = option_menu(
                menu_title="Navegação",
                options=rotulos,
                icons=icones,
                menu_icon="grid",
                styles={
                    "container": {"padding": "6px !important", "background-color": "#0E1424", "border": "1px solid #1E293B", "border-radius": "12px"},
                    "menu-title": {"font-size": "11px", "color": "#64748B", "text-transform": "uppercase", "letter-spacing": "0.08em"},
                    "icon": {"color": "#818CF8", "font-size": "15px"},
                    "nav-link": {"font-size": "13px", "font-weight": "600", "color": "#CBD5E1", "border-radius": "8px", "margin": "3px 0", "padding": "9px 12px"},
                    "nav-link-selected": {"background-color": "#4F46E5", "color": "#FFFFFF"},
                },
            )
            selecionada = abas_opcoes[rotulos.index(escolhido)]
        except Exception:
            selecionada = st.radio("Navegação Principal", abas_opcoes, label_visibility="collapsed")

        st.markdown("---")
        st.caption(f"📦 Produtos no catálogo: **{total_produtos}**")
        st.caption("⚡ Dica: no celular, toque no `>` no topo para recolher/abrir o menu.")

    return selecionada
