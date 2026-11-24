import streamlit as st


def aplicar_tema_saas():
    """Injeta CSS limpo e minimalista estilo SaaS moderno (Linear/Stripe dark)."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
        .block-container { padding-top: 1.25rem !important; padding-bottom: 2.5rem !important; max-width: 1380px; }
        section[data-testid="stSidebar"] {
            background: #090D16 !important;
            border-right: 1px solid #1F2937 !important;
        }
        div[data-testid="stMetric"] {
            background: #111827;
            border: 1px solid #1F2937;
            border-radius: 10px;
            padding: 14px 16px;
        }
        div[data-testid="stMetricLabel"] p {
            color: #9CA3AF !important;
            font-weight: 500 !important;
            font-size: 0.78rem !important;
            letter-spacing: 0.02em;
        }
        div[data-testid="stMetricValue"] { color: #F9FAFB !important; font-weight: 700 !important; font-size: 1.45rem !important; }
        div[data-testid="stForm"] {
            background: #0F172A;
            border: 1px solid #1E293B;
            border-radius: 10px;
            padding: 1rem;
        }
        div[data-testid="stTabs"] button[role="tab"] {
            font-size: 0.86rem;
            font-weight: 600;
            padding: 8px 14px;
            color: #9CA3AF;
        }
        div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
            color: #F9FAFB;
        }
        .stButton > button[kind="primary"] {
            background: #4F46E5 !important;
            border: 1px solid #6366F1 !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }
        .stButton > button[kind="primary"]:hover { background: #4338CA !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def estilizar_cards_metricas():
    """Mantido para compatibilidade; estilização principal controlada via CSS limpo."""
    return


def render_menu_principal(abas_opcoes: list, total_produtos: int = 0) -> str:
    """Renderiza navegação lateral limpa sem poluição visual."""
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
            "<div style='padding:4px 4px 14px 4px'>"
            "<div style='font-size:1rem;font-weight:700;color:#F9FAFB;letter-spacing:-0.01em'>ORION ENTERPRISE</div>"
            "<div style='font-size:0.75rem;color:#6B7280'>Dualis Lingerie</div>"
            "</div>",
            unsafe_allow_html=True,
        )
        try:
            from streamlit_option_menu import option_menu
            rotulos = [a.split(" ", 1)[1] if " " in a else a for a in abas_opcoes]
            icones = [icones_mapa.get(a, "circle") for a in abas_opcoes]
            escolhido = option_menu(
                menu_title=None,
                options=rotulos,
                icons=icones,
                styles={
                    "container": {"padding": "0 !important", "background-color": "transparent"},
                    "icon": {"color": "#9CA3AF", "font-size": "14px"},
                    "nav-link": {
                        "font-size": "13px",
                        "font-weight": "500",
                        "color": "#D1D5DB",
                        "border-radius": "8px",
                        "margin": "2px 0",
                        "padding": "8px 10px",
                    },
                    "nav-link-selected": {"background-color": "#1E293B", "color": "#FFFFFF", "font-weight": "600"},
                },
            )
            selecionada = abas_opcoes[rotulos.index(escolhido)]
        except Exception:
            selecionada = st.radio("Navegação", abas_opcoes, label_visibility="collapsed")

        st.markdown("---")
        st.caption(f"Catálogo ativo: **{total_produtos} SKUs**")

    return selecionada
