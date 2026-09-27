---
name: json-data-guard
description: Boas práticas de persistência em arquivos JSON, tratamento UTF-8 no Windows, criação de backups e prevenção de corrupção de dados.
---

# 🛡️ JSON Data Guard Skill

Esta Skill garante a integridade dos dados locais armazenados em `arquivos/produtos.json` e `arquivos/configuracoes.json`.

---

## 🔒 Regras de Leitura e Escrita

1. **Codificação Única (UTF-8 Mandatory):**
   ```python
   with open("arquivos/produtos.json", "r", encoding="utf-8") as f:
       dados = json.load(f)
   ```

2. **Validação de Payload:**
   Antes de sobrescrever o arquivo em disco, valide se o tipo de dado é compatível (`list` para produtos, `dict` para configurações):
   ```python
   def salvar_produtos_disco(lista_produtos):
       if not isinstance(lista_produtos, list):
           print("Erro: Payload inválido para produtos.")
           return False
       # código de salvamento
   ```

3. **Estratégia de Backup:**
   Manter backups periódicos na pasta `arquivos_backup/` antes de atualizações estruturais ou migrations de schema.
