"""
gui_utils.py - Funções utilitárias para a GUI
"""
import ctypes
import logging

logger = logging.getLogger(__name__)


def is_admin():
    """
    Verifica se o programa está executando como administrador.
    
    Returns:
        bool: True se está como admin, False caso contrário
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        logger.error(f"Erro ao verificar privilégios de admin: {e}")
        return False


def center_window(window, width, height):
    """
    Centraliza uma janela Tkinter na tela.
    
    Args:
        window: Janela Tkinter
        width: Largura da janela
        height: Altura da janela
    """
    try:
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
    except Exception as e:
        logger.warning(f"Erro ao centralizar janela: {e}")
