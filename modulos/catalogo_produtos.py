import json
import pandas as pd
import streamlit as st
from modulos.github_sync import obter_github_token


def render_catalogo_produtos(produtos: list, salvar_fn):
    """Renderiza catálogo profissional: tabela formatada à esquerda e ações em abas à direita."""
    h_left, h_right = st.columns([3, 1])
    with h_left:
        st.subheader("Catálogo de Produtos")
        status_sync = "Sincronização GitHub ativa" if obter_github_token() else "Modo local (configure GITHUB_TOKEN em Secrets para persistência na nuvem)"
        st.caption(status_sync)

    with h_right:
        with st.popover("Backup / Restaurar", use_container_width=True):
            if produtos:
                st.download_button(
                    "Baixar produtos.json",
                    data=json.dumps(produtos, ensure_ascii=False, indent=4),
                    file_name="produtos.json",
                    mime="application/json",
                    use_container_width=True,
                )
            up_bkp = st.file_uploader("Restaurar JSON", type=["json"])
            if up_bkp is not None and st.button("Aplicar Backup", type="primary", use_container_width=True):
                dados_bkp = json.loads(up_bkp.read().decode("utf-8"))
                if isinstance(dados_bkp, list) and dados_bkp:
                    produtos.clear()
                    produtos.extend(dados_bkp)
                    salvar_fn(produtos)
                    st.success("Catálogo restaurado.")
                    st.rerun()

    col_tabela, col_painel = st.columns([1.45, 1.0], gap="large")

    with col_tabela:
        if produtos:
            df_cat = pd.DataFrame([
                {
                    "SKU": p.get("sku", ""),
                    "Produto": p.get("nome", ""),
                    "Categoria": p.get("categoria", ""),
                    "Custo": float(p.get("custo_unitario", 0.0)),
                    "Embalagem": float(p.get("custo_embalagem", 0.0)),
                    "Peso": int(p.get("peso_g", 0)),
                }
                for p in produtos
            ])
            st.dataframe(
                df_cat,
                use_container_width=True,
                hide_index=True,
                height=420,
                column_config={
                    "Custo": st.column_config.NumberColumn("Custo Unit.", format="R$ %.2f"),
                    "Embalagem": st.column_config.NumberColumn("Embalagem", format="R$ %.2f"),
                    "Peso": st.column_config.NumberColumn("Peso", format="%d g"),
                },
            )
        else:
            st.info("Nenhum produto cadastrado.")

    with col_painel:
        tab_edit, tab_new = st.tabs(["Editar Produto", "Novo Produto"])

        with tab_edit:
            if not produtos:
                st.info("Cadastre um produto primeiro.")
            else:
                opcoes_edit = [f"{p.get('nome', '')} ({p.get('sku', '')})" for p in produtos]
                idx_edit = st.selectbox(
                    "Selecionar item",
                    range(len(opcoes_edit)),
                    format_func=lambda i: opcoes_edit[i],
                    key="sel_editar_produto_catalogo",
                )
                prod_edit = produtos[idx_edit]

                with st.form(f"form_editar_produto_{prod_edit.get('id', idx_edit)}"):
                    e1, e2 = st.columns([1.5, 0.9])
                    ed_nome = e1.text_input("Nome *", value=prod_edit.get("nome", ""))
                    ed_sku = e2.text_input("SKU *", value=prod_edit.get("sku", ""))
                    ed_cat = st.text_input("Categoria", value=prod_edit.get("categoria", "Geral"))

                    e3, e4, e5 = st.columns(3)
                    ed_custo_un = e3.number_input("Custo (R$)", min_value=0.0, value=float(prod_edit.get("custo_unitario", 0.0)), step=0.10)
                    ed_custo_emb = e4.number_input("Emb. (R$)", min_value=0.0, value=float(prod_edit.get("custo_embalagem", 0.30)), step=0.05)
                    ed_peso = e5.number_input("Peso (g)", min_value=0, value=int(prod_edit.get("peso_g", 100)), step=10)

                    ed_forn = st.text_input("Fornecedor", value=prod_edit.get("fornecedor", "Confecção Própria"))
                    ed_obs = st.text_input("Observações", value=prod_edit.get("observacoes", ""))

                    b1, b2 = st.columns(2)
                    salvar_ed = b1.form_submit_button("Salvar Alterações", type="primary", use_container_width=True)
                    excluir_ed = b2.form_submit_button("Excluir", use_container_width=True)

                    if salvar_ed:
                        nome_limpo = ed_nome.strip()
                        sku_limpo = ed_sku.strip().upper()
                        duplicado = any(i != idx_edit and p.get("sku", "").strip().upper() == sku_limpo for i, p in enumerate(produtos))
                        if not nome_limpo or not sku_limpo:
                            st.error("Preencha Nome e SKU.")
                        elif duplicado:
                            st.warning(f"SKU '{sku_limpo}' já existe.")
                        else:
                            produtos[idx_edit].update({
                                "nome": nome_limpo,
                                "sku": sku_limpo,
                                "categoria": ed_cat.strip() or "Geral",
                                "custo_unitario": float(ed_custo_un),
                                "custo_embalagem": float(ed_custo_emb),
                                "fornecedor": ed_forn.strip() or "Confecção Própria",
                                "peso_g": int(ed_peso),
                                "observacoes": ed_obs.strip(),
                            })
                            salvar_fn(produtos)
                            st.success("Produto atualizado.")
                            st.rerun()

                    if excluir_ed:
                        if len(produtos) <= 1:
                            st.warning("Mantenha ao menos 1 produto.")
                        else:
                            produtos.pop(idx_edit)
                            salvar_fn(produtos)
                            st.success("Produto removido.")
                            st.rerun()

        with tab_new:
            with st.form("form_novo_produto", clear_on_submit=True):
                c1, c2 = st.columns([1.5, 0.9])
                novo_nome = c1.text_input("Nome *")
                novo_sku = c2.text_input("SKU *")
                nova_cat = st.text_input("Categoria", value="Lingerie / Underwear")

                c3, c4, c5 = st.columns(3)
                novo_custo_un = c3.number_input("Custo (R$)", min_value=0.0, value=0.0, step=0.10)
                novo_custo_emb = c4.number_input("Emb. (R$)", min_value=0.0, value=0.30, step=0.05)
                novo_peso = c5.number_input("Peso (g)", min_value=0, value=65, step=5)

                novo_forn = st.text_input("Fornecedor", value="Confecção Própria")
                nova_obs = st.text_input("Observações")

                if st.form_submit_button("Cadastrar Produto", type="primary", use_container_width=True):
                    nome_limpo = novo_nome.strip()
                    sku_limpo = novo_sku.strip().upper()
                    if not nome_limpo or not sku_limpo:
                        st.error("Preencha Nome e SKU.")
                    elif any(p.get("sku", "").strip().upper() == sku_limpo for p in produtos):
                        st.warning(f"SKU '{sku_limpo}' já cadastrado.")
                    else:
                        novo_id = max((p.get("id", 0) for p in produtos), default=0) + 1
                        produtos.append({
                            "id": novo_id,
                            "nome": nome_limpo,
                            "sku": sku_limpo,
                            "categoria": nova_cat.strip() or "Geral",
                            "custo_unitario": float(novo_custo_un),
                            "custo_embalagem": float(novo_custo_emb),
                            "fornecedor": novo_forn.strip() or "Confecção Própria",
                            "peso_g": int(novo_peso),
                            "observacoes": nova_obs.strip(),
                        })
                        salvar_fn(produtos)
                        st.success(f"Produto '{nome_limpo}' cadastrado.")
                        st.rerun()
