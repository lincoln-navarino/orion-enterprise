import csv
import io
import re
import urllib.request
import pandas as pd
import streamlit as st

DEFAULT_SHEET_URL = "https://docs.google.com/spreadsheets/d/14X47hALBujpRievJI4Ey2g6FnqjKZOQhO83wd-jVSBU/edit?usp=sharing"


def _to_float_br(val: str) -> float:
    s = str(val or "").replace("R$", "").replace(" ", "").strip()
    if not s:
        return 0.0
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0


def extrair_sheet_id(url: str) -> str:
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", url or "")
    return match.group(1) if match else ""


@st.cache_data(ttl=120, show_spinner=False)
def carregar_planilha_pagamentos_google(url: str) -> dict:
    """Lê a planilha pública do Google Sheets via CSV e extrai custos, compras e pagamentos."""
    sheet_id = extrair_sheet_id(url)
    if not sheet_id:
        raise ValueError("Link do Google Sheets inválido.")

    export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    req = urllib.request.Request(export_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=12) as resp:
        texto = resp.read().decode("utf-8", errors="replace")

    rows = list(csv.reader(io.StringIO(texto)))
    custos = {}
    pagamentos = []
    compras = []
    headers_compra = []

    for row in rows:
        cols = [c.strip() for c in row] + [""] * max(0, 10 - len(row))

        # Bloco 1: Custo de Aquisição (cols 0 e 1 antes da linha 'Data de Compra')
        if not headers_compra and cols[0] and cols[1] and cols[0].lower() not in ("ca", "data de compra"):
            val_custo = _to_float_br(cols[1])
            if val_custo > 0:
                custos[cols[0]] = val_custo

        # Bloco 2: Cabeçalho de Data de Compra
        if cols[0].lower() == "data de compra":
            headers_compra = [c for c in cols[1:8] if c]
            continue

        # Linhas de compras (Data de Compra + quantidades por produto)
        if headers_compra and cols[0] and re.match(r"^\d{2}/\d{2}/\d{2,4}$", cols[0]):
            total_pecas = 0
            total_rs = 0.0
            detalhes = {}
            for idx, prod_nome in enumerate(headers_compra):
                qtd = int(_to_float_br(cols[1 + idx]))
                if qtd > 0:
                    total_pecas += qtd
                    custo_un = custos.get(prod_nome, 0.0)
                    total_rs += qtd * custo_un
                    detalhes[prod_nome] = qtd
            if total_pecas > 0:
                compras.append({
                    "Data": cols[0],
                    "Peças": total_pecas,
                    "Valor Lote (R$)": round(total_rs, 2),
                    "Itens": ", ".join(f"{k}: {v}" for k, v in detalhes.items()),
                })

        # Bloco 3: Pagamentos (cols 8 = Dia, cols 9 = valor)
        if cols[8] and cols[9] and cols[8].lower() != "dia":
            val_pag = _to_float_br(cols[9])
            if val_pag > 0:
                pagamentos.append({"Data": cols[8], "Valor Pago (R$)": val_pag})

    return {
        "custos": custos,
        "compras": compras,
        "pagamentos": pagamentos,
        "total_comprado": sum(c["Valor Lote (R$)"] for c in compras),
        "total_pecas": sum(c["Peças"] for c in compras),
        "total_pago": sum(p["Valor Pago (R$)"] for p in pagamentos),
    }


def render_conexao_google_sheets():
    """Renderiza painel conectado ao Google Sheets de controle de pagamentos."""
    st.subheader("Sincronização com Google Sheets (Controle Real)")
    c1, c2 = st.columns([3.2, 0.8])
    url_sheet = c1.text_input("Link da Planilha Google Sheets", value=DEFAULT_SHEET_URL, key="gs_url_pagamentos")
    if c2.button("Atualizar Agora", type="primary", use_container_width=True, key="gs_btn_sync"):
        st.cache_data.clear()

    try:
        dados = carregar_planilha_pagamentos_google(url_sheet)
    except Exception as exc:
        st.error(f"Não foi possível ler a planilha (verifique se está compartilhada como 'Qualquer pessoa com o link'): {exc}")
        return

    saldo_pendente = dados["total_comprado"] - dados["total_pago"]
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Comprado", f"R$ {dados['total_comprado']:,.2f}")
    m2.metric("Total Pago", f"R$ {dados['total_pago']:,.2f}")
    m3.metric("Saldo Pendente", f"R$ {saldo_pendente:,.2f}")
    m4.metric("Peças Compradas", f"{dados['total_pecas']:,}".replace(",", "."))

    t1, t2, t3 = st.tabs(["Pagamentos Realizados", "Lotes Comprados", "Custos da Planilha"])
    with t1:
        df_pag = pd.DataFrame(dados["pagamentos"])
        if not df_pag.empty:
            st.dataframe(
                df_pag,
                use_container_width=True,
                hide_index=True,
                column_config={"Valor Pago (R$)": st.column_config.NumberColumn(format="R$ %.2f")},
            )
    with t2:
        df_comp = pd.DataFrame(dados["compras"])
        if not df_comp.empty:
            st.dataframe(
                df_comp,
                use_container_width=True,
                hide_index=True,
                column_config={"Valor Lote (R$)": st.column_config.NumberColumn(format="R$ %.2f")},
            )
    with t3:
        df_cust = pd.DataFrame([{"Produto": k, "Custo Aquisição": v} for k, v in dados["custos"].items()])
        if not df_cust.empty:
            st.dataframe(
                df_cust,
                use_container_width=True,
                hide_index=True,
                column_config={"Custo Aquisição": st.column_config.NumberColumn(format="R$ %.2f")},
            )
