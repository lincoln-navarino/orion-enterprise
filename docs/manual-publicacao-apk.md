# 📱 Manual de Publicação & Geração de APK Android

Este guia detalha o processo de hospedagem do **ORION Enterprise** na nuvem e o empacotamento do APK Android.

---

## 🔄 Fluxo de Publicação e Compilação

```mermaid
flowchart TD
    LocalCode[💻 Código Local Python] --> GitPush[⬆️ Git Push para o GitHub]
    
    subgraph Nuvem ["🌐 Hospedagem Cloud"]
        GitPush --> StreamlitCloud[☁️ Streamlit Community Cloud]
        StreamlitCloud --> URL["🔗 URL com HTTPS (orion-dualis.streamlit.app)"]
    end

    subgraph Mobile ["📱 Geração do App Android"]
        GitPush --> Actions[⚙️ GitHub Actions CI/CD]
        Actions --> BuildAPK["📦 Compilação do APK (Bubblewrap/TWA)"]
        BuildAPK --> DownloadAPK["📲 Download do Artifacts (.APK)"]
    end

    URL --> MobileApp["📱 Instalação no Celular Android"]
    DownloadAPK --> MobileApp
```

---

## 📑 Passo a Passo Resumido

1. **Subir o Código**: `ENVIAR_GITHUB.bat` ou comandos `git push origin main`.
2. **Hospedar no Streamlit Cloud**: Conectar o repositório em [share.streamlit.io](https://share.streamlit.io).
3. **Download do APK**: Acessar a aba **Actions** no repositório do GitHub e baixar o artefato compilado.

---

## 🔗 Links Relacionados (Foam Graph)

* [[index]]: Página Inicial.
* [[arquitetura-do-codigo]]: Arquitetura do sistema.
* [[integracoes-marketplaces]]: Leitura e upload de planilhas pelo celular.
