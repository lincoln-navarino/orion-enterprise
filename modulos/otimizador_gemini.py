import json
import os
import sqlite3
import streamlit as st

DB_PATH = os.path.join("arquivos", "orion_intel.db")

REGRAS_SEO_CANAL = {
    "Shopee": {
        "limite_titulo": 120,
        "regras": "Marca/Tipo + Produto + Palavras-chave de cauda longa + Variação. Evitar termos que geram bloqueio como 'réplica'.",
    },
    "TikTok Shop": {
        "limite_titulo": 120,
        "regras": "Gancho emocional/benefício imediato + Nome do produto. Foco em retenção nos 3 primeiros segundos de vídeo.",
    },
    "Mercado Livre": {
        "limite_titulo": 60,
        "regras": "Produto + Marca + Modelo + Especificação. Sem termos promocionais ('promoção', 'frete grátis'). Foto principal fundo branco.",
    },
}


def _abrir_db():
    os.makedirs("arquivos", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cerebro_insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plataforma TEXT NOT NULL,
            categoria TEXT NOT NULL,
            tipo TEXT NOT NULL CHECK (tipo IN ('erro_evitar', 'padrao_vencedor')),
            regra_aprendida TEXT NOT NULL,
            peso_confianca REAL DEFAULT 1.0,
            criado_em TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    return conn


def _obter_api_key():
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        try:
            key = str(st.secrets.get("GEMINI_API_KEY", "")).strip()
        except Exception:
            key = ""
    return key


def render_otimizador_gemini(produtos: list):
    st.markdown("### 🧠 Otimizador de Anúncios com Gemini + Memória Neural")
    st.caption("Consulta obrigatoriamente a base de erros e padrões vencedores da plataforma antes de gerar títulos, copy ou roteiro de 15s.")

    conn = _abrir_db()
    tab_otim, tab_mem = st.tabs(["✨ Gerador SEO & Roteiro 15s", "📚 Cérebro Neural (Erros & Padrões)"])

    with tab_mem:
        with st.form("form_cerebro_regra", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                plat_r = st.selectbox("Plataforma:", ["Shopee", "TikTok Shop", "Mercado Livre", "Geral"], key="cr_plat")
            with c2:
                tipo_r = st.selectbox("Tipo:", ["erro_evitar", "padrao_vencedor"], key="cr_tipo")
            with c3:
                cat_r = st.text_input("Categoria (ex: seo_titulo, imagem, video)", value="seo_titulo", key="cr_cat")
            regra_txt = st.text_input("Regra aprendida *", placeholder="Ex: Nunca usar termo 'cinta modeladora médica' no TikTok Shop.")
            if st.form_submit_button("💾 Gravar no Cérebro Neural", type="primary"):
                if not regra_txt.strip():
                    st.error("Descreva a regra aprendida.")
                else:
                    conn.execute(
                        "INSERT INTO cerebro_insights (plataforma, categoria, tipo, regra_aprendida) VALUES (?, ?, ?, ?)",
                        (plat_r, cat_r.strip() or "geral", tipo_r, regra_txt.strip()),
                    )
                    conn.commit()
                    st.success("Regra salva no Cérebro Neural!")
                    st.rerun()

        rows = conn.execute("SELECT id, plataforma, categoria, tipo, regra_aprendida, peso_confianca FROM cerebro_insights ORDER BY id DESC").fetchall()
        if rows:
            for rid, rplat, rcat, rtipo, rregra, rpeso in rows:
                cor = "#EF4444" if rtipo == "erro_evitar" else "#10B981"
                tag = "ERRO A EVITAR" if rtipo == "erro_evitar" else "PADRÃO VENCEDOR"
                st.markdown(f"<span style='color:{cor};font-weight:700'>[{tag} — {rplat} / {rcat}]</span> {rregra}", unsafe_allow_html=True)
        else:
            st.info("Nenhuma regra registrada ainda. Cadastre erros a evitar ou padrões que converteram bem.")

    with tab_otim:
        prod_nomes = [p["nome"] for p in produtos] if produtos else ["Produto"]
        c1, c2 = st.columns(2)
        with c1:
            prod_sel = st.selectbox("Produto do Catálogo:", prod_nomes, key="ot_prod")
            prod_obj = next((p for p in produtos if p["nome"] == prod_sel), {"nome": prod_sel, "observacoes": ""})
        with c2:
            plat_ot = st.selectbox("Canal Alvo:", ["Shopee", "TikTok Shop", "Mercado Livre"], key="ot_plat")

        titulo_atual = st.text_input("Título Atual do Anúncio:", value=prod_obj.get("nome", ""))
        dores_conc = st.text_area("Dores / Reclamações dos Concorrentes (opcional):", placeholder="Ex: aperta demais na cintura, enrola ao sentar...")

        api_key = _obter_api_key()
        if not api_key:
            api_key = st.text_input("GEMINI_API_KEY (ou configure em Secrets no Streamlit Cloud):", type="password", key="ot_apikey")

        if st.button("🧠 Consultar Cérebro & Gerar Otimização", type="primary"):
            insights = conn.execute(
                "SELECT tipo, regra_aprendida FROM cerebro_insights WHERE plataforma IN (?, 'Geral') ORDER BY peso_confianca DESC, id DESC LIMIT 10",
                (plat_ot,),
            ).fetchall()
            erros = [r[1] for r in insights if r[0] == "erro_evitar"]
            padroes = [r[1] for r in insights if r[0] == "padrao_vencedor"]

            st.markdown("#### 🔍 Consulta Prévia à Memória Neural")
            if erros or padroes:
                for e in erros:
                    st.error(f"Evitar: {e}")
                for p in padroes:
                    st.success(f"Replicar: {p}")
            else:
                st.caption("Consulta realizada: nenhuma restrição cadastrada para este canal ainda.")

            if not api_key:
                st.warning("Configure `GEMINI_API_KEY` nos Secrets do Streamlit Cloud (ou no campo acima) para gerar a otimização com o Gemini.")
            else:
                try:
                    from google import genai
                    seo = REGRAS_SEO_CANAL[plat_ot]
                    prompt = (
                        f"Atue como especialista de SEO e conversão para {plat_ot}.\n"
                        f"Limite de título: {seo['limite_titulo']} caracteres. Regras: {seo['regras']}\n"
                        f"ERROS PROIBIDOS: {' | '.join(erros) if erros else 'Nenhum.'}\n"
                        f"PADRÕES VENCEDORES: {' | '.join(padroes) if padroes else 'Nenhum.'}\n"
                        f"Produto: {prod_obj.get('nome')} | Detalhes: {prod_obj.get('observacoes', '')}\n"
                        f"Título atual: {titulo_atual}\n"
                        f"Dores de concorrentes: {dores_conc or 'Nenhuma informada.'}\n"
                        "Retorne JSON com: titulo_otimizado, bullet_points (lista), descricao_otimizada, roteiro_video_15s (gancho_3s, demonstracao_8s, cta_4s)."
                    )
                    client = genai.Client(api_key=api_key)
                    resp = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt,
                        config={"response_mime_type": "application/json"},
                    )
                    dados = json.loads(resp.text or "{}")
                    st.success("Otimização gerada com sucesso!")
                    st.text_input("Título Otimizado:", value=dados.get("titulo_otimizado", ""))
                    st.text_area("Descrição Otimizada:", value=dados.get("descricao_otimizada", ""), height=160)
                    if dados.get("roteiro_video_15s"):
                        st.json(dados["roteiro_video_15s"])
                except Exception as exc:
                    st.error(f"Erro ao chamar Gemini: {exc}")

    conn.close()
