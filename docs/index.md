# 🛡️ ORION Enterprise — Base de Conhecimento & Grafo do Projeto

Bem-vindo à base de conhecimento do **ORION Enterprise (Dualis Lingerie)**. Esta documentação foi organizada utilizando a estrutura **Foam** integrada com diagramas de **Code Architecture Graph (Mermaid.js)**.

---

## 🗺️ Grafo de Conhecimento (Navegação)

Utilize os links wikilinks abaixo para navegar pelos módulos de conhecimento e arquitetura:

* 📐 **[[arquitetura-do-codigo]]**: Mapeamento completo do sistema, funções Python, fluxo de dados de [`app.py`](file:///c:/Users/Lincoln/Desktop/Aplicativo%20de%20gest%C3%A3o/app.py) e persistência JSON.
* 🛍️ **[[integracoes-marketplaces]]**: Lógica de importação e conciliação de vendas (Shopee, TikTok, Shein, Mercado Livre).
* 📊 **[[regras-fiscais]]**: Configuração de perfis tributários (Simples Nacional, MEI) e metas de ROAS.
* 📱 **[[manual-publicacao-apk]]**: Guia passo a passo para gerar e distribuir o APK Android via PWA / Trusted Web Activity / Bubblewrap.
* ⚠️ **[[licoes-aprendidas]]**: Registro de erros conhecidos, limitações técnicas e boas práticas que devem ser evitadas.

---

## 🏗️ Estrutura do Workspace

```
Aplicativo de gestão/
├── app.py                         # Aplicação Principal em Streamlit (~2.800 linhas)
├── organizar_tiktok.py            # Script auxiliar para tratamento de relatórios TikTok
├── COMO_PUBLICAR_E_GERAR_APK.md   # Guia original de APK
├── requirements.txt               # Dependências Python
├── arquivos/                      # Banco de Dados JSON local e relatórios salvos
│   ├── produtos.json
│   ├── configuracoes.json
│   └── Relatórios/
│       ├── Vendas/
│       └── Ads/
├── docs/                          # Foam Knowledge Base & Diagramas de Arquitetura
│   ├── index.md
│   ├── arquitetura-do-codigo.md
│   ├── integracoes-marketplaces.md
│   ├── regras-fiscais.md
│   └── manual-publicacao-apk.md
└── .vscode/                       # Configurações do VS Code & Foam
    ├── settings.json
    └── extensions.json
```

---

> [!TIP]
> **Dica Foam no VS Code:** Pressione `Ctrl + Shift + P` e digite `Foam: Show Graph` para abrir a visualização interativa do grafo de notas!
