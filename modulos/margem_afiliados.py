import streamlit as st
from modulos.ui_tema import estilizar_cards_metricas


def calcular_margem_real_afiliado(
    preco_venda: float,
    cmv_kit: float,
    comissao_canal_pct: float,
    taxa_fixa: float,
    imposto_pct: float,
    afiliado_pct: float,
    devolucao_pct: float,
    ads_pct: float,
    custo_embalagem: float,
):
    """Calcula lucro líquido real descontando comissão de afiliado e taxa de devoluções."""
    fator_retencao = max(0.0, 1.0 - (devolucao_pct / 100.0))
    receita_efetiva = preco_venda * fator_retencao

    taxa_canal_rs = receita_efetiva * (comissao_canal_pct / 100.0) + (taxa_fixa * fator_retencao)
    imposto_rs = receita_efetiva * (imposto_pct / 100.0)
    afiliado_rs = receita_efetiva * (afiliado_pct / 100.0)
    ads_rs = preco_venda * (ads_pct / 100.0)
    perda_emb_devolucao = custo_embalagem * (devolucao_pct / 100.0)

    custo_total = cmv_kit + taxa_canal_rs + imposto_rs + afiliado_rs + ads_rs + perda_emb_devolucao
    lucro_liquido = receita_efetiva - custo_total
    margem_real = (lucro_liquido / preco_venda * 100.0) if preco_venda > 0 else 0.0

    soma_pct = (comissao_canal_pct + imposto_pct + afiliado_pct) * fator_retencao + ads_pct + 20.0
    divisor = max(0.05, fator_retencao - (soma_pct / 100.0))
    preco_ideal_20 = (cmv_kit + taxa_fixa * fator_retencao + perda_emb_devolucao) / divisor

    return {
        "receita_efetiva": receita_efetiva,
        "afiliado_rs": afiliado_rs,
        "taxa_canal_rs": taxa_canal_rs,
        "imposto_rs": imposto_rs,
        "ads_rs": ads_rs,
        "lucro_liquido": lucro_liquido,
        "margem_real": margem_real,
        "preco_ideal_20": preco_ideal_20,
    }


def render_margem_afiliados(produtos: list, taxas_fn, perfis_fiscais: dict):
    st.markdown("### 🤝 Simulador de Margem Real — Afiliados (TikTok/Shopee) & Devoluções")
    st.caption("Descubra se o produto continua lucrativo pagando comissão para criadores/afiliados e descontando devoluções.")

    if not produtos:
        st.warning("Cadastre ao menos 1 produto para simular.")
        return

    c1, c2, c3, c4 = st.columns([1.4, 1.0, 0.8, 1.0])
    with c1:
        nomes = [p["nome"] for p in produtos]
        prod_nome = st.selectbox("Produto:", nomes, key="ma_prod")
        prod = next(p for p in produtos if p["nome"] == prod_nome)
    with c2:
        canal = st.selectbox("Canal:", ["TikTok Shop", "Shopee", "Mercado Livre (Classic)", "Mercado Livre (Premium)", "Shein"], key="ma_canal")
    with c3:
        qtd = st.number_input("Peças no Kit:", min_value=1, max_value=10, value=1, step=1, key="ma_qtd")
    with c4:
        perfil = st.selectbox("Perfil Fiscal:", list(perfis_fiscais.keys()), key="ma_fiscal")
        imposto_pct = float(perfis_fiscais[perfil]["aliquota"])

    cmv_kit = float(prod.get("custo_unitario", 0.0)) * qtd + float(prod.get("custo_embalagem", 0.0))
    com_padrao, taxa_padrao = taxas_fn(canal, 49.9)

    p1, p2, p3, p4, p5 = st.columns(5)
    with p1:
        preco = st.number_input("Preço de Venda (R$)", min_value=1.0, value=49.90, step=1.0, key="ma_preco")
    with p2:
        afiliado_pct = st.number_input("% Afiliado / Criador", min_value=0.0, max_value=50.0, value=10.0 if canal == "TikTok Shop" else 5.0, step=1.0, key="ma_afil")
    with p3:
        devolucao_pct = st.number_input("% Devolução / Cancel.", min_value=0.0, max_value=50.0, value=4.0, step=0.5, key="ma_dev")
    with p4:
        ads_pct = st.number_input("% Ads / ACOS", min_value=0.0, max_value=60.0, value=8.0, step=1.0, key="ma_ads")
    with p5:
        com_pct = st.number_input("% Comissão Canal", min_value=0.0, max_value=40.0, value=float(com_padrao), step=0.5, key="ma_com")

    res = calcular_margem_real_afiliado(
        preco_venda=preco,
        cmv_kit=cmv_kit,
        comissao_canal_pct=com_pct,
        taxa_fixa=float(taxa_padrao),
        imposto_pct=imposto_pct,
        afiliado_pct=afiliado_pct,
        devolucao_pct=devolucao_pct,
        ads_pct=ads_pct,
        custo_embalagem=float(prod.get("custo_embalagem", 0.0)),
    )

    m1, m2, m3, m4 = st.columns(4)
    margem = res["margem_real"]
    cor = "#EF4444" if margem < 10.0 else ("#F59E0B" if margem < 20.0 else "#10B981")
    status_txt = "CRÍTICO (<10%)" if margem < 10.0 else ("ATENÇÃO (10–19.9%)" if margem < 20.0 else "SAUDÁVEL (≥20%)")

    m1.metric("Lucro Líquido Real", f"R$ {res['lucro_liquido']:.2f}")
    m2.metric("Margem Real", f"{margem:.1f}%", status_txt)
    m3.metric("Comissão Afiliado", f"R$ {res['afiliado_rs']:.2f}")
    m4.metric("Preço Mín. p/ 20% Margem", f"R$ {res['preco_ideal_20']:.2f}")
    estilizar_cards_metricas()

    st.markdown(
        f"<div style='padding:10px 14px;border-radius:10px;border:1px solid {cor};background:#0E1424;color:{cor};font-weight:600;margin-bottom:12px'>"
        f"Diagnóstico {canal}: {status_txt} — CMV do Kit: R$ {cmv_kit:.2f} | Taxa Canal: R$ {res['taxa_canal_rs']:.2f} | Imposto: R$ {res['imposto_rs']:.2f} | Ads: R$ {res['ads_rs']:.2f}"
        f"</div>",
        unsafe_allow_html=True,
    )

    try:
        import plotly.graph_objects as go
        perda_dev = max(0.0, preco - res["receita_efetiva"])
        labels = ["CMV Kit", "Taxa Canal", "Afiliado", "Imposto", "Ads", "Devoluções", "Lucro Líquido"]
        values = [
            round(cmv_kit, 2),
            round(res["taxa_canal_rs"], 2),
            round(res["afiliado_rs"], 2),
            round(res["imposto_rs"], 2),
            round(res["ads_rs"], 2),
            round(perda_dev, 2),
            round(max(0.0, res["lucro_liquido"]), 2),
        ]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.55, textinfo="label+percent")])
        fig.update_layout(
            title=f"Composição do Preço (R$ {preco:.2f}) — {canal}",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=340,
            margin=dict(t=45, b=10, l=10, r=10),
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        pass
