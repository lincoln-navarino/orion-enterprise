---
name: frontend-design-master
description: Skill de desenvolvimento Frontend, UI/UX e Design System focado em criar interfaces modernas, elegantes, responsivas e de alto impacto visual no Streamlit e na Web.
---

# 🎨 Frontend Design & UI/UX Master Skill

Esta Skill foi projetada para garantir que o **ORION Enterprise** ofereça uma **experiência visual premium (WOW factor)**, alinhada às melhores práticas de design moderno de dashboards e aplicações web.

---

## 💎 1. Sistema de Design & Paleta de Cores

Evite cores primárias genéricas (vermelho puro, azul puro). Utilize uma paleta refinada e harmonizada:

### Dark Mode Premium (Deep Space & Cyber Navy)
* **Fundo da Aplicação:** `linear-gradient(180deg, #050811 0%, #0B101D 50%, #060912 100%)`
* **Cards & Seções:** `linear-gradient(135deg, #101625 0%, #0B101D 100%)` com bordas sutis `#1E293B`
* **Cores de Ação e Status:**
  * **Cyan (Destaque Principal / Ações):** `#38BDF8` (Brilho: `rgba(56, 189, 248, 0.25)`)
  * **Emerald (Sucesso / Lucro / Positivo):** `#34D399` (Fundo: `rgba(52, 211, 153, 0.15)`)
  * **Amber (Alerta / ROAS Médio):** `#FBBF24` (Fundo: `rgba(251, 191, 36, 0.15)`)
  * **Red (Crítico / Prejuízo):** `#F87171` (Fundo: `rgba(248, 113, 113, 0.15)`)
  * **Violet (Anúncios / Ads):** `#C084FC` (Fundo: `rgba(192, 132, 252, 0.15)`)

---

## ✒️ 2. Tipografia e Hierarquia Visual

1. **Fontes Obrigatórias:**
   * **Títulos e Métricas Numéricas:** `Outfit`, sans-serif (pesos: 700, 800) — confere aspecto moderno e financeiro.
   * **Texto de Corpo e Rótulos:** `Inter`, system-ui, sans-serif (pesos: 400, 500, 600).

2. **Hierarquia:**
   * **Valores de Métricas:** Destaque em 1.5rem a 2.0rem, fonte `Outfit`, peso 800.
   * **Labels:** Caixa alta (*uppercase*), fonte `Inter`, tamanho 0.8rem, cor `#94A3B8`, espaçamento entre letras `letter-spacing: 0.5px`.

---

## ✨ 3. Componentes Visualmente Impressionantes (WOW Factor)

### A. Metric Cards com Glassmorphism e Hover Soft
```css
.orion-metric-card {
    background: linear-gradient(135deg, #101625 0%, #0B101D 100%);
    border: 1px solid #1E293B;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}
.orion-metric-card:hover {
    border-color: #38BDF8;
    transform: translateY(-3px);
    box-shadow: 0 0 20px rgba(56, 189, 248, 0.2), 0 8px 25px rgba(0, 0, 0, 0.5);
}
```

### B. Badges / Pills Neon de Status
```html
<span class="neon-pill neon-pill-emerald">● Lucro +18.4%</span>
<span class="neon-pill neon-pill-amber">⚡ ROAS 4.2x</span>
<span class="neon-pill neon-pill-red">⚠️ Margem Crítica</span>
```

---

## 📱 4. Responsividade e Grid Layout

1. **Evitar Sobrecarga Visual:**
   * Utilize `st.columns([1, 1, 1])` para quebrar métricas grandes em blocos organizados.
   * Defina `min-width: 150px` em colunas para evitar estouro de texto em telas menores.

2. **Micro-interações:**
   * Botões devem ter estado ativo imediato, transição suave de cor de fundo em `0.2s` e elevação ao passar o mouse (*hover*).

---

## 🛠️ 5. Boas Práticas ao Aplicar no Streamlit

* **Injeção Única de CSS:** Concentrar o bloco `<style>` na parte inicial do código para manter o carregamento limpo e consistente.
* **Componentes HTML no Streamlit:** Utilizar `st.markdown(html, unsafe_allow_html=True)` apenas para componentes decorativos ou cards de alta fidelidade visual.
