# Guia: Publicando na Nuvem e Gerando o Aplicativo Android (.APK)

Este guia explica o passo a passo para colocar o **ORION Enterprise** na nuvem gratuitamente e instalar o aplicativo `.apk` no seu celular Android.

---

## Passo 1: Subir o Código para o GitHub

1. Acesse o seu [GitHub](https://github.com) e clique no botão verde **"New"** (ou crie um novo repositório com o nome `orion-enterprise`).
   - Pode deixar como **Privado** ou **Público**.
   - **Não** marque a opção de adicionar README ou .gitignore (já criamos tudo para você).
2. Copie o link do repositório gerado (ex: `https://github.com/SEU_USUARIO/orion-enterprise.git`).
3. Abra o terminal na pasta deste projeto e execute:
   ```bash
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/orion-enterprise.git
   git push -u origin main
   ```

---

## Passo 2: Hospedar Gratuitamente no Streamlit Community Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io) e faça login com a sua conta do GitHub.
2. Clique no botão **"New app"**.
3. Selecione:
   - **Repository:** `SEU_USUARIO/orion-enterprise`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** Escolha um subdomínio personalizado (ex: `orion-dualis.streamlit.app`).
4. Clique em **"Deploy!"**.
5. Em cerca de 2 a 3 minutos, seu sistema estará online com certificado de segurança SSL (HTTPS).

---

## Passo 3: Baixar o Aplicativo Android (.APK)

### Opção A: Pelo GitHub Actions (Automático)
Assim que você envia o código para o GitHub (Passo 1), o GitHub compila automaticamente o aplicativo Android:
1. No seu repositório no GitHub, clique na aba **"Actions"** no menu superior.
2. Clique no fluxo **"Compilar Aplicativo Android (.APK)"**.
3. Clique na execução mais recente e vá até a seção **"Artifacts"** no final da página.
4. Baixe o arquivo **`ORION-Enterprise-App`** (ele conterá o arquivo `.apk` pronto para instalar no seu celular).

### Opção B: Inserir a URL da Nuvem no App
Quando você abrir o aplicativo no celular pela primeira vez:
* Se o servidor padrão não estiver respondendo, o app exibirá uma tela amigável com um botão **"Tentar Novamente"**.
* Segure o dedo sobre o botão (clique longo) para abrir a caixa de diálogo e colar a sua URL da nuvem (ex: `https://orion-dualis.streamlit.app`).
* O app salvará esse endereço e abrirá diretamente o sistema em todas as próximas vezes!

---

## Dicas de Uso no Android
- **Upload de Planilhas:** O app possui integração nativa com o seletor de arquivos do Android, permitindo anexar relatórios `.xlsx` e `.csv` direto do celular ou do Google Drive.
- **Atualizar a Página:** Basta puxar a tela para baixo (*swipe-to-refresh*) para recarregar o sistema a qualquer momento.
- **Botão Voltar:** O botão físico/virtual de voltar do Android navega pelas páginas do sistema antes de fechar o app.
