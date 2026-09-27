---
name: streamlit-orion-dev
description: Guias de desenvolvimento, padrões de UI, CSS customizado e gerenciamento de estado (st.session_state) para o app.py do ORION Enterprise.
---

# 🎨 Streamlit Orion Dev Skill

Esta Skill orienta o desenvolvimento e manutenção do arquivo [`app.py`](file:///c:/Users/Lincoln/Desktop/Aplicativo%20de%20gest%C3%A3o/app.py), garantindo consistência visual, alta performance e controle rígido de estado.

---

## 💎 Padrões de Design & UI (Orion Dark Theme)

1. **Paleta de Cores Tailwind/Custom:**
   * Fundo Principal: `#050811` a `#0B101D` (Gradientes escuros)
   * Cards e Containers: `#101625` com borda `#1E293B`
   * Destaques / Ação Principal: Cyan `#38BDF8`, Emerald `#34D399`, Amber `#FBBF24`, Red `#F87171`
   * Tipografia: `Inter` (corpo) e `Outfit` (títulos e métricas numéricas)

2. **Métricas Responsivas:**
   * Sempre utilizer a classe CSS `.orion-card` ou seletores customizados de `st.metric` para garantir leitura em dispositivos móveis e desktops.

---

## ⚡ Gerenciamento de Estado (`st.session_state`)

1. **Inicialização de Variáveis:**
   ```python
   if "autenticado" not in st.session_state:
       st.session_state["autenticado"] = False
   if "produtos" not in st.session_state:
       st.session_state["produtos"] = carregar_produtos_disco(PRODUTOS_PADRAO)
   ```

2. **Persistência Implicada:**
   Sempre que alterar um item em `st.session_state.produtos` ou `st.session_state.configuracoes`, invoque a função de salvamento em disco correspondente:
   ```python
   salvar_produtos_disco(st.session_state.produtos)
   st.rerun()
   ```
