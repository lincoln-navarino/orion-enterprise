---
name: android-apk-builder
description: Procedimentos de compilação, atualização de URL da nuvem e publicação do aplicativo Android (.APK) via GitHub Actions.
---

# 📱 Android APK Builder Skill

Esta Skill documenta o processo de deploy continuo e empacotamento do ORION Enterprise como um aplicativo nativo Android (`.apk`).

---

## 🚀 Workflow de Deploy & CI/CD

1. **Repositório GitHub:**
   * Branch principal: `main`
   * Script de envio rápido: [`ENVIAR_GITHUB.bat`](file:///c:/Users/Lincoln/Desktop/Aplicativo%20de%20gest%C3%A3o/ENVIAR_GITHUB.bat)

2. **Hospedagem Web (Streamlit Cloud):**
   * Servidor padrão: `share.streamlit.io`
   * Certificado: HTTPS obrigatório para funcionamento no PWA / Trusted Web Activity.

3. **Geração do APK via GitHub Actions:**
   * Ao realizar push na branch `main`, o fluxo `.github/workflows/` (se configurado) compila o artefato Android.
   * O arquivo `.apk` final fica disponível na aba **Actions > Artifacts**.

---

## 🔧 Troca Dinâmica de URL no Celular

* Se o aplicativo Android perder conexão com o servidor local, o usuário pode fazer um **clique longo** no botão "Tentar Novamente" para informar a nova URL da nuvem (ex: `https://orion-dualis.streamlit.app`).
