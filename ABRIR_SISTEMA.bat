@echo off
chcp 65001 > nul
title ORION Enterprise - Dualis Lingerie

echo ====================================================================
echo           INICIANDO ORION ENTERPRISE - DUALIS LINGERIE
echo ====================================================================
echo.
echo  [1/2] Preparando o servidor local...
echo  [2/2] Abrindo o aplicativo no navegador...
echo.
echo  - O aplicativo abrira em: http://localhost:8501
echo  - Para ENCERRAR o servidor, feche esta janela.
echo.
echo ====================================================================
echo.

cd /d "%~dp0"

:: Aguarda 2 segundos e abre o navegador
timeout /t 2 /nobreak > nul
start http://localhost:8501

:: Inicia o aplicativo Streamlit
python -m streamlit run app.py

pause
