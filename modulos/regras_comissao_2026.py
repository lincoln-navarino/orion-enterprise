import pandas as pd
import streamlit as st


def calcular_taxa_oficial_2026(
    plataforma_nome: str,
    preco: float,
    tiktok_frete_gratis: bool = True,
    shopee_cpf_alto_volume: bool = False,
) -> tuple[float, float, float]:
    """
    Retorna (comissao_pct_efetiva, taxa_fixa_rs, taxa_total_rs) pelas regras oficiais 2026.
    """
    p = max(0.0, float(preco))

    if "Shopee" in plataforma_nome:
        adicional_cpf = 3.00 if shopee_cpf_alto_volume else 0.0
        if p < 9.00:
            taxa_total = (p * 0.50) + adicional_cpf
            return 50.0, adicional_cpf, taxa_total
        if p < 80.00:
            pct, fixa = 20.0, 4.50 + adicional_cpf
        elif p < 100.00:
            pct, fixa = 14.0, 16.00 + adicional_cpf
        elif p < 200.00:
            pct, fixa = 14.0, 20.00 + adicional_cpf
        else:
            pct, fixa = 14.0, 26.00 + adicional_cpf
        return pct, fixa, (p * (pct / 100.0)) + fixa

    if "TikTok" in plataforma_nome:
        pct_base = 10.0 if p < 50.00 else 6.0
        fixa = 4.00 if p < 50.00 else 6.00
        frete_rs = min(p * 0.06, 50.00) if tiktok_frete_gratis else 0.0
        taxa_total = (p * (pct_base / 100.0)) + fixa + frete_rs
        pct_efetivo = ((taxa_total - fixa) / p * 100.0) if p > 0 else pct_base
        return round(pct_efetivo, 2), fixa, taxa_total

    if "Shein" in plataforma_nome:
        return 16.0, 3.00, (p * 0.16) + 3.00

    if "Classic" in plataforma_nome:
        fixa = 6.00 if p < 79.00 else 0.0
        return 12.0, fixa, (p * 0.12) + fixa

    if "Premium" in plataforma_nome:
        fixa = 6.00 if p < 79.00 else 0.0
        return 16.5, fixa, (p * 0.165) + fixa

    return 14.0, 4.00, (p * 0.14) + 4.00


def analisar_armadilha_kit(plataforma_nome: str, preco: float) -> dict:
    """Identifica zonas onde subir pouco o preço aumenta a taxa mais do que o ganho."""
    p = float(preco)
    _, _, taxa_atual = calcular_taxa_oficial_2026(plataforma_nome, p)
    pct_real = (taxa_atual / p * 100.0) if p > 0 else 0.0

    if "Shopee" in plataforma_nome:
        if 80.00 <= p < 100.00:
            return {
                "armadilha": True,
                "nivel": "warning",
                "mensagem": f"Zona de Armadilha Shopee (R$ 80–R$ 99,99): taxa fixa sobe para R$ 16,00 ({pct_real:.1f}% do preço). Avalie travar o kit em R$ 79,90 ou subir para R$ 192+.",
            }
        if 100.00 <= p < 165.00:
            return {
                "armadilha": True,
                "nivel": "warning",
                "mensagem": f"Degrau Shopee R$ 100–R$ 199,99: taxa fixa de R$ 20,00 pesa {pct_real:.1f}% sobre R$ {p:.2f}. Kits maiores diluídos acima de R$ 175 reduzem o peso da taxa.",
            }
        if 200.00 <= p < 220.00:
            return {
                "armadilha": True,
                "nivel": "info",
                "mensagem": f"Atenção ao degrau de R$ 200,00 (taxa fixa R$ 26,00). Em R$ 199,90 a taxa fixa é R$ 20,00 (R$ 6,00 menor).",
            }

    if "TikTok" in plataforma_nome and 42.00 <= p < 50.00:
        return {
            "armadilha": True,
            "nivel": "info",
            "mensagem": f"Ponto de Virada TikTok Shop: a partir de R$ 50,00 a comissão cai de 10% para 6%. Subir o kit para R$ 50,00+ reduz a alíquota em 4%.",
        }

    return {
        "armadilha": False,
        "nivel": "ok",
        "mensagem": f"Faixa equilibrada em {plataforma_nome}: custo total de plataforma de R$ {taxa_atual:.2f} ({pct_real:.1f}%).",
    }


def render_auditoria_equilibrio_kits(prod_obj: dict, plat_sel: str, rows_kits: list):
    """Exibe painel estratégico apontando quais kits pagam menos taxa proporcional."""
    if not rows_kits:
        return

    st.markdown("#### Auditoria Estratégica de Faixas (Equilíbrio dos Kits)")
    st.caption("Mostra o peso real da comissão + taxa fixa em cada kit para evitar cruzar degraus que corroem seu lucro.")

    analises = []
    alertas = 0
    for r in rows_kits:
        qtd = r.get("Qtd Peças", "")
        preco = float(r.get("🔥 Oferta Normal (R$)", 0.0))
        _, fixa, taxa_total = calcular_taxa_oficial_2026(plat_sel, preco)
        peso_pct = (taxa_total / preco * 100.0) if preco > 0 else 0.0
        diag = analisar_armadilha_kit(plat_sel, preco)
        if diag["armadilha"]:
            alertas += 1
        analises.append({
            "Kit": qtd,
            "Preço Oferta": preco,
            "Taxa Fixa": fixa,
            "Taxa Total": round(taxa_total, 2),
            "Peso Real (%)": round(peso_pct, 1),
            "Status Estratégico": "Ajustar Faixa" if diag["armadilha"] else "Equilibrado",
        })

    if alertas > 0:
        st.warning(f"{alertas} kit(s) estão em faixa de transição desfavorável em {plat_sel}. Confira a tabela abaixo antes de publicar.")
    else:
        st.success(f"Todos os 10 kits estão em faixas equilibradas para {plat_sel}.")

    st.dataframe(
        pd.DataFrame(analises),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Preço Oferta": st.column_config.NumberColumn(format="R$ %.2f"),
            "Taxa Fixa": st.column_config.NumberColumn(format="R$ %.2f"),
            "Taxa Total": st.column_config.NumberColumn(format="R$ %.2f"),
            "Peso Real (%)": st.column_config.NumberColumn(format="%.1f%%"),
        },
    )
