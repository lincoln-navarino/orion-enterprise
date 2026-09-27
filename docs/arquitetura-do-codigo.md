# 📐 Arquitetura do Código (Abas Fixas) — ORION Enterprise

Este documento descreve a nova estrutura com **4 Abas Fixas de Navegação** implementada no [`app.py`](file:///c:/Users/Lincoln/Desktop/Aplicativo%20de%20gest%C3%A3o/app.py).

---

## 🗺️ Estrutura de Abas Fixas

```mermaid
graph TD
    User([👤 Gestor Dualis]) --> TopNav["📱 Top Navbar (Abas Fixas)"]

    subgraph Abas ["🚀 4 Abas Fixas de Navegação (app.py)"]
        TopNav --> A1["📊 1. Dashboard"]
        TopNav --> A2["📦 2. Produtos & Precificação"]
        TopNav --> A3["📄 3. Central de Relatórios"]
        TopNav --> A4["🚚 4. Pagamentos a Fornecedores"]
    end

    subgraph A2_Sub ["Sub-abas de Produtos"]
        A2 --> A2_1["🏷️ Precificação de Kits (1 a 10 Peças por Marketplace)"]
        A2 --> A2_2["📈 Análise de Performance do Produto"]
    end

    subgraph A4_Sub ["Controle de Fornecedores"]
        A4 --> RegForn["➕ Registrar Peças Pegas + Valor Unitário"]
        A4 --> HistForn["📊 Histórico de Pagamentos (Pendente, Pago, Parcial)"]
    end

    subgraph Data ["💾 Arquivos JSON Persistentes"]
        A2_1 <-->|Salvar Kits| ProdJSON["arquivos/produtos.json"]
        A4 <-->|Salvar Lotes| FornJSON["arquivos/pagamentos_fornecedores.json"]
    end
```

---

## 🔗 Links Relacionados (Foam Graph)

* [[index]]: Página Inicial do Foam.
* [[licoes-aprendidas]]: Prevenção de erros e codificação UTF-8.
