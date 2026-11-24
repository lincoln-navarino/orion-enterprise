import base64
import json
import os
import urllib.error
import urllib.request
import streamlit as st


def obter_github_token() -> str:
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        try:
            token = str(st.secrets.get("GITHUB_TOKEN", "")).strip()
        except Exception:
            token = ""
    return token


def sincronizar_arquivo_github(caminho_relativo: str, conteudo_str: str, mensagem: str) -> tuple[bool, str]:
    """Envia o JSON atualizado para o GitHub via Contents API quando GITHUB_TOKEN estiver configurado."""
    token = obter_github_token()
    if not token:
        return False, "GITHUB_TOKEN não configurado."

    repo = os.environ.get("GITHUB_REPO", "lincoln-navarino/orion-enterprise")
    branch = os.environ.get("GITHUB_BRANCH", "master")
    url = f"https://api.github.com/repos/{repo}/contents/{caminho_relativo}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "Orion-Enterprise-App",
        "Content-Type": "application/json",
    }

    sha = None
    try:
        req_get = urllib.request.Request(f"{url}?ref={branch}", headers=headers, method="GET")
        with urllib.request.urlopen(req_get, timeout=10) as resp:
            sha = json.loads(resp.read().decode("utf-8")).get("sha")
    except urllib.error.HTTPError as err:
        if err.code != 404:
            return False, f"Erro ao consultar GitHub ({err.code})."
    except Exception as exc:
        return False, f"Falha de rede GitHub: {exc}"

    payload = {
        "message": mensagem,
        "content": base64.b64encode(conteudo_str.encode("utf-8")).decode("ascii"),
        "branch": branch,
    }
    if sha:
        payload["sha"] = sha

    try:
        req_put = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="PUT")
        with urllib.request.urlopen(req_put, timeout=12):
            return True, f"Sincronizado no GitHub ({branch})."
    except Exception as exc:
        return False, f"Erro ao gravar no GitHub: {exc}"
