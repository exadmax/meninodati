@echo off
REM build_exe_gui.bat - Inicia construtor de executável com interface gráfica

setlocal enabledelayedexpansion

REM Mudar para o diretório do script
cd /d "%~dp0"

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERRO] Python nao foi encontrado no PATH!
    echo.
    echo Por favor, instale Python 3.8+ ou adicione-o ao PATH do sistema.
    echo.
    pause
    exit /b 1
)

REM Verificar dependências
echo.
echo ========================================
echo MENINO DA TI - CONSTRUTOR DE EXECUTAVEL
echo Interface Grafica
echo ========================================
echo.
echo Verificando dependências...

python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo.
    echo [AVISO] PyInstaller não encontrado
    echo Instalando PyInstaller...
    python -m pip install pyinstaller
)

echo.
echo Iniciando interface gráfica...
echo.

REM Executar o construtor gráfico
python gui_exe_builder.py

if errorlevel 1 (
    echo.
    echo [ERRO] Erro ao executar construtor.
    echo.
    pause
    exit /b 1
)

pause
exit /b 0
