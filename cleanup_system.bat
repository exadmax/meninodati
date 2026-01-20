@echo off
REM Atalho para abrir o diálogo de limpeza do sistema
REM Este script pode ser executado sem privilégios de administrador

setlocal enabledelayedexpansion

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Erro: Python não está instalado ou não está no PATH
    echo.
    echo Por favor, instale Python 3.12+ em:
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Obter o diretório do script
cd /d "%~dp0"

REM Verificar se gui_cleanup_dialog.py existe
if not exist gui_cleanup_dialog.py (
    echo Erro: gui_cleanup_dialog.py não encontrado
    echo O arquivo deve estar no mesmo diretório que este script
    pause
    exit /b 1
)

REM Executar o diálogo de limpeza
echo Iniciando limpeza do sistema...
python -c "import tkinter as tk; from gui_cleanup_dialog import CleanupDialog; root = tk.Tk(); root.withdraw(); dialog = CleanupDialog(root); root.mainloop()"

if errorlevel 1 (
    echo Erro ao executar limpeza
    pause
    exit /b 1
)

exit /b 0
