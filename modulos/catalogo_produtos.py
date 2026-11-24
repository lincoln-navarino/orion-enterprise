import pandas as pd
import streamlit as st


def render_catalogo_produtos(produtos: list, salvar_fn):
    """Renderiza gestão completa do catálogo: tabela resumo, cadastro e edição/exclusão."""
    st.markdown("### 📝 Catálogo de Produtos Cadastrados")

    if produtos:
        df_cat = pd.DataFrame([
            {
                "SKU": p.get("sku", ""),
                "Produto": p.get("nome", ""),
                "Categoria": p.get("categoria", ""),
                "Custo Unit. (R$)": float(p.get("custo_unitario", 0.0)),
                "Embalagem (R$)": float(p.get("custo_embalagem", 0.0)),
                "Fornecedor": p.get("fornecedor", ""),
                "Peso (g)": int(p.get("peso_g", 0)),
            }
            for p in produtos
        ])
        st.dataframe(df_cat, use_container_width=True, hide_index=True)

    col_add, col_edit = st.columns(2)

    with col_add:
        st.markdown("##### ➕ Adicionar Novo Produto")
        with st.form("form_novo_produto", clear_on_submit=True):
            c1, c2 = st.columns([1.4, 0.8])
            novo_nome = c1.text_input("Nome do Produto *")
            novo_sku = c2.text_input("SKU *")
            nova_cat = st.text_input("Categoria", value="Geral")

            c3, c4, c5 = st.columns(3)
            novo_custo_un = c3.number_input("Custo Unit. (R$)", min_value=0.0, value=0.0, step=0.10)
            novo_custo_emb = c4.number_input("Embalagem (R$)", min_value=0.0, value=0.30, step=0.05)
            novo_peso = c5.number_input("Peso (g)", min_value=0, value=100, step=10)

            novo_forn = st.text_input("Fornecedor", value="Confecção Própria")
            nova_obs = st.text_input("Observações")

            if st.form_submit_button("💾 Salvar Novo Produto", type="primary", use_container_width=True):
                nome_limpo = novo_nome.strip()
                sku_limpo = novo_sku.strip().upper()
                if not nome_limpo or not sku_limpo:
                    st.error("Preencha pelo menos Nome do Produto e SKU.")
                elif any(p.get("sku", "").strip().upper() == sku_limpo for p in produtos):
                    st.warning(f"Já existe um produto cadastrado com o SKU '{sku_limpo}'.")
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
                    st.success(f"Produto '{nome_limpo}' ({sku_limpo}) adicionado!")
                    st.rerun()

    with col_edit:
        st.markdown("##### ✏️ Editar ou Excluir Produto")
        if not produtos:
            st.info("Nenhum produto para editar.")
            return

        opcoes_edit = [f"{p.get('nome', '')} ({p.get('sku', '')})" for p in produtos]
        idx_edit = st.selectbox(
            "Selecione o produto:",
            range(len(opcoes_edit)),
            format_func=lambda i: opcoes_edit[i],
            key="sel_editar_produto_catalogo",
        )
        prod_edit = produtos[idx_edit]

        with st.form(f"form_editar_produto_{prod_edit.get('id', idx_edit)}"):
            e1, e2 = st.columns([1.4, 0.8])
            ed_nome = e1.text_input("Nome do Produto *", value=prod_edit.get("nome", ""))
            ed_sku = e2.text_input("SKU *", value=prod_edit.get("sku", ""))
            ed_cat = st.text_input("Categoria", value=prod_edit.get("categoria", "Geral"))

            e3, e4, e5 = st.columns(3)
            ed_custo_un = e3.number_input("Custo Unit. (R$)", min_value=0.0, value=float(prod_edit.get("custo_unitario", 0.0)), step=0.10)
            ed_custo_emb = e4.number_input("Embalagem (R$)", min_value=0.0, value=float(prod_edit.get("custo_embalagem", 0.30)), step=0.05)
            ed_peso = e5.number_input("Peso (g)", min_value=0, value=int(prod_edit.get("peso_g", 100)), step=10)

            ed_forn = st.text_input("Fornecedor", value=prod_edit.get("fornecedor", "Confecção Própria"))
            ed_obs = st.text_input("Observações", value=prod_edit.get("observacoes", ""))

            b1, b2 = st.columns(2)
            salvar_ed = b1.form_submit_button("💾 Salvar Alterações", type="primary", use_container_width=True)
            excluir_ed = b2.form_submit_button("🗑️ Excluir", use_container_width=True)

            if salvar_ed:
                nome_limpo = ed_nome.strip()
                sku_limpo = ed_sku.strip().upper()
                duplicado = any(i != idx_edit and p.get("sku", "").strip().upper() == sku_limpo for i, p in enumerate(produtos))
                if not nome_limpo or not sku_limpo:
                    st.error("Preencha Nome e SKU.")
                elif duplicado:
                    st.warning(f"Outro produto já usa o SKU '{sku_limpo}'.")
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
                    st.success(f"Produto '{nome_limpo}' atualizado!")
                    st.rerun()

            if excluir_ed:
                if len(produtos) <= 1:
                    st.warning("Mantenha pelo menos 1 produto no catálogo.")
                else:
                    removido = produtos.pop(idx_edit)
                    salvar_fn(produtos)
                    st.success(f"Produto '{removido.get('nome', '')}' removido.")
                    st.rerun()
