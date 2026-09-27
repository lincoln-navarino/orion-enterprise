---
name: marketplace-reconciliation
description: Procedimentos de importação, limpeza e conciliação de relatórios de vendas e ads (Shopee, TikTok, Shein, Mercado Livre).
---

# 🛍️ Marketplace Data Reconciliation Skill

Esta Skill define os procedimentos de importação, padronização e cálculo de dados provenientes das plataformas de e-commerce e anúncios.

---

## 📋 Mapeamento de Canais

1. **Shopee:**
   * Tipo: Vendas (CSV de Pedidos) e Ads (Relatório de Desempenho de Anúncios).
   * Colunas-chave: Código do Pedido, Valor Total, Taxa de Comissão, Taxa de Frete.

2. **TikTok Shop / Ads:**
   * Script Auxiliar: Utilizar [`organizar_tiktok.py`](file:///c:/Users/Lincoln/Desktop/Aplicativo%20de%20gest%C3%A3o/organizar_tiktok.py) para tratar exportações brutas do TikTok.
   * Tratamento: Converte delimitadores e formata datas para o padrão ISO.

3. **Shein & Mercado Livre:**
   * Trata formatos `.xlsx` e `.csv` parseando colunas de frete, comissão e liquidação líquida.

---

## 📂 Estrutura de Salvamento em Disco

```
arquivos/Relatórios/{Tipo: Vendas|Ads}/{Ano: 2025|2026|2027}/{Mês}/{Marketplace}/
```
Sempre valide a integridade dos cabeçalhos dos arquivos antes de tentar somar métricas de faturamento e ROAS no [`app.py`](file:///c:/Users/Lincoln/Desktop/Aplicativo%20de%20gest%C3%A3o/app.py).
