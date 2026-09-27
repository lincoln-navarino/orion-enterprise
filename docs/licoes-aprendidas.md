# ⚠️ Lições Aprendidas & Prevenção de Erros — ORION Enterprise

Este documento registra **erros conhecidos, limitações técnicas e boas práticas obrigatórias** que devem ser respeitados tanto pelos desenvolvedores quanto pelas IAs que trabalham neste repositório.

---

## 🚫 Erros Críticos que NÃO Podem Ser Cometidos

### 1. Codificação de Arquivos no Windows (`encoding='utf-8'`)
* ❌ **Erro:** Abrir arquivos `.json`, `.csv` ou `.py` sem especificar `encoding='utf-8'`.
* ✅ **Regra:** Sempre usar `open(caminho, 'r', encoding='utf-8')` e `open(caminho, 'w', encoding='utf-8')`. No Windows, o padrão padrão da linguagem pode corromper caracteres acentuados ou falhar no parse de JSON.

### 2. Execução de Scripts PowerShell vs CMD no Windows
* ❌ **Erro:** Tentar rodar scripts `.ps1` ou comandos como `npx` direto no PowerShell sem tratar a `ExecutionPolicy`.
* ✅ **Regra:** Para chamadas de sistema e MCP, utilizar `cmd /c npx.cmd` ou chamar executáveis diretos para evitar bloqueios de segurança do PowerShell.

### 3. Preservação do Banco de Dados JSON Local
* ❌ **Erro:** Sobrescrever `arquivos/produtos.json` ou `arquivos/configuracoes.json` com estruturas vazias durante salvamentos.
* ✅ **Regra:** Sempre validar se os dados existem antes de salvar (`isinstance(dados, list)` ou `isinstance(dados, dict)`).

### 4. Manutenção das Pastas de Relatórios
* ❌ **Erro:** Assumir que as pastas em `arquivos/Relatórios` já existem.
* ✅ **Regra:** Garantir que a função `garantir_estrutura_pastas()` seja executada na inicialização do [`app.py`](file:///c:/Users/Lincoln/Desktop/Aplicativo%20de%20gest%C3%A3o/app.py).

---

## 📝 Como Adicionar Novos Conhecimentos ou Erros Evitados

Sempre que encontrar um bug corrigido ou uma regra nova:
1. Adicione um novo tópico neste documento (`[[licoes-aprendidas]]`).
2. Se for uma regra rigorosa de desenvolvimento, a IA também registrará no servidor de memória (**MCP Server Memory**).

---

## 🔗 Links Relacionados (Foam Graph)

* [[index]]: Página Inicial.
* [[arquitetura-do-codigo]]: Arquitetura e persistência do sistema.
