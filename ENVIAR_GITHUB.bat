@echo off
chcp 65001 > nul
title Enviando ORION para o GitHub...

echo ====================================================================
echo           ENVIANDO PROJETO ORION ENTERPRISE PARA O GITHUB
echo ====================================================================
echo.
echo Repositorio: https://github.com/lincoln-navarino/orion-enterprise.git
echo.
echo Se for solicitada autenticacao, autorize na janela ou navegador.
echo.

git branch -M main
git push -u origin main

echo.
if %errorlevel% equ 0 (
    echo ====================================================================
    echo [SUCESSO] O codigo foi enviado com sucesso para o GitHub!
    echo ====================================================================
) else (
    echo ====================================================================
    echo [ATENCAO] Houve uma falha no envio. Verifique a mensagem acima.
    echo ====================================================================
)
echo.
pause
