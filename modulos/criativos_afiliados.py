import os
import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = os.path.join("arquivos", "orion_intel.db")


def _abrir_db():
    os.makedirs("arquivos", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS criativos_afiliados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plataforma TEXT NOT NULL,
            produto_nome TEXT NOT NULL,
            criador_afiliado TEXT NOT NULL,
            gancho_usado TEXT NOT NULL,
            link_video TEXT DEFAULT '',
            custo_amostra REAL DEFAULT 0,
            views INTEGER DEFAULT 0,
            pedidos INTEGER DEFAULT 0,
            faturamento REAL DEFAULT 0,
            criado_em TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    return conn


def render_painel_criativos(produtos: list):
    st.markdown("### 🎬 Painel de Criativos, Vídeos Curtos & Afiliados")
    st.caption("Acompanhe quais ganchos de vídeo e criadores geram mais pedidos no TikTok Shop e Shopee Vídeos.")

    conn = _abrir_db()
    prod_nomes = [p["nome"] for p in produtos] if produtos else ["Produto Geral"]

    with st.expander("➕ Registrar Vídeo / Afiliado / Amostra", expanded=False):
        with st.form("form_criativo_afiliado", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                plat = st.selectbox("Plataforma:", ["TikTok Shop", "Shopee Vídeos"])
            with c2:
                prod = st.selectbox("Produto:", prod_nomes)
            with c3:
                criador = st.text_input("Criador / @Afiliado *")

            gancho = st.text_input("Gancho dos 3 primeiros segundos *")
            link = st.text_input("Link do vídeo (opcional)")

            c4, c5, c6, c7 = st.columns(4)
            with c4:
                custo_amostra = st.number_input("Custo Amostra/Envio (R$)", min_value=0.0, value=0.0, step=1.0)
            with c5:
                views = st.number_input("Visualizações", min_value=0, value=0, step=100)
            with c6:
                pedidos = st.number_input("Pedidos Gerados", min_value=0, value=0, step=1)
            with c7:
                faturamento = st.number_input("Faturamento (R$)", min_value=0.0, value=0.0, step=10.0)

            if st.form_submit_button("💾 Salvar Criativo", type="primary"):
                if not criador.strip() or not gancho.strip():
                    st.error("Preencha o Criador/@Afiliado e o Gancho usado.")
                else:
                    conn.execute(
                        """
                        INSERT INTO criativos_afiliados (
                            plataforma, produto_nome, criador_afiliado, gancho_usado,
                            link_video, custo_amostra, views, pedidos, faturamento
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (plat, prod, criador.strip(), gancho.strip(), link.strip(), float(custo_amostra), int(views), int(pedidos), float(faturamento)),
                    )
                    conn.commit()
                    st.success("Criativo registrado!")
                    st.rerun()

    df = pd.read_sql_query("SELECT * FROM criativos_afiliados ORDER BY faturamento DESC, id DESC", conn)
    conn.close()

    if df.empty:
        st.info("Nenhum criativo ou afiliado registrado ainda. Use o botão acima para adicionar o primeiro vídeo/amostra.")
        return

    k1, k2, k3, k4 = st.columns(4)
    total_amostras = float(df["custo_amostra"].sum())
    total_fat = float(df["faturamento"].sum())
    total_ped = int(df["pedidos"].sum())
    roi = (total_fat / total_amostras) if total_amostras > 0 else 0.0

    k1.metric("Vídeos/Afiliados", len(df))
    k2.metric("Pedidos por Vídeo", total_ped)
    k3.metric("Faturamento Gerado", f"R$ {total_fat:,.2f}")
    k4.metric("ROI sobre Amostras", f"{roi:.1f}x" if total_amostras > 0 else "—")

    df["Conv. (%)"] = df.apply(lambda r: round((r["pedidos"] / r["views"] * 100), 2) if r["views"] > 0 else 0.0, axis=1)
    st.dataframe(
        df[["plataforma", "produto_nome", "criador_afiliado", "gancho_usado", "views", "pedidos", "Conv. (%)", "faturamento", "custo_amostra"]],
        use_container_width=True,
        hide_index=True,
    )
