@echo off
REM Menino de TI Helper - Launcher Script
REM This script launches the Menino de TI Helper application

echo ========================================
echo    Menino de TI Helper - Iniciando
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao esta instalado ou nao esta no PATH
    echo Por favor, instale o Python 3.7 ou superior
    echo.
    pause
    exit /b 1
)

echo Python encontrado!
echo.

REM Check if requirements are installed
echo Verificando dependencias...
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo AVISO: tkinter nao encontrado. Instalando dependencias...
    pip install -r requirements.txt
)

echo.
echo Iniciando Menino de TI Helper...
echo.

REM Run the application
python main.py

if errorlevel 1 (
    echo.
    echo ERRO: O aplicativo encontrou um problema.
    echo Verifique os logs para mais detalhes.
    pause
)
