# 📐 Arquitetura do Código (Repaginação) — ORION Enterprise

Este documento descreve a nova arquitetura do aplicativo de gestão ([`app.py`](file:///c:/Users/Lincoln/Desktop/Aplicativo%20de%20gest%C3%A3o/app.py)), desenvolvida com navegação por Top Navbar, gráficos executivos em Altair e precificação mestre unificada.

---

## 📊 Grafo da Nova Estrutura Unificada

```mermaid
graph TD
    User([👤 Usuário / Gestor]) --> TopNav["📱 Top Navbar (Navegação Superior)"]

    subgraph Modulos ["🚀 Módulos do Sistema (app.py)"]
        TopNav --> M1["📊 Dashboard Executivo"]
        TopNav --> M2["🏷️ Catálogo & Precificação Mestre"]
        TopNav --> M3["💰 Central de Vendas & Ads"]
        TopNav --> M4["⚙️ Configurações Fiscais & Taxas"]
    end

    subgraph M1_Details ["Detalhamento Dashboard"]
        M1 --> KPI["Cards de Faturamento, Ads, Comissões e Devoluções"]
        M1 --> Charts["Gráficos Altair (Faturamento vs Ads + Donut de Marketplaces)"]
        M1 --> Insights["Insights de Inteligência Comercial & Curva ABC"]
    end

    subgraph M2_Details ["Detalhamento Precificação"]
        M2 --> Matriz["Matriz Geral de Preços Praticados (Todos os Produtos)"]
        M2 --> Simulador["Simulador Dinâmico com Recálculo Instantâneo de Margem"]
    end

    subgraph Storage ["💾 Persistência em Disco"]
        Matriz <-->|JSON UTF-8| ProdJSON["arquivos/produtos.json"]
        M4 <-->|JSON UTF-8| CfgJSON["arquivos/configuracoes.json"]
    end
```

---

## 🔗 Links Relacionados (Foam Graph)

* [[index]]: Página Inicial do Foam.
* [[licoes-aprendidas]]: Prevenção de erros e codificação UTF-8 no Windows.
* [[regras-fiscais]]: Alíquotas e margem de ROAS.
