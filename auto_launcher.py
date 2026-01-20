"""
auto_launcher.py - Launcher automático que detecta argumentos de modo
Permite executar com: python auto_launcher.py console  ou  python auto_launcher.py gui
"""
import sys
import os
import tkinter as tk
from tkinter import ttk

from console_splash import ConsoleSplash
from splash_screen import SplashScreen
from gui_utils import center_window
from system_check import SystemChecker


def launch_console_mode():
    """Inicia a aplicação em modo console"""
    print("\n" + "="*75)
    print("INICIANDO MENINO DA TI EM MODO CONSOLE")
    print("="*75 + "\n")
    
    splash = ConsoleSplash()
    splash.show()
    
    print("✓ Aplicação iniciada em modo console!")
    print("\nAguardando comandos...\n")


def launch_gui_mode():
    """Inicia a aplicação em modo gráfico"""
    try:
        from gui_main_window import MeninoDeTIHelperGUI
        
        # Criar janela principal (mas não exibir ainda)
        root = tk.Tk()
        root.withdraw()
        
        # Mostrar splash screen
        image_path = os.path.join(os.path.dirname(__file__), 'img', 'loading.png')
        splash = SplashScreen(root, image_path=image_path, duration=3.0)
        
        # Quando splash terminar, mostrar aplicação principal
        def show_main_window():
            root.deiconify()
            app = MeninoDeTIHelperGUI(root)
        
        splash.set_complete_callback(show_main_window)
        root.mainloop()
    except Exception as e:
        print(f"Erro ao iniciar modo gráfico: {e}")
        print("Iniciando modo console como fallback...")
        launch_console_mode()


def launch_launcher_mode():
    """Abre o seletor de modo"""
    class ModeLauncher:
        """Janela para escolher entre modo console e modo gráfico"""
        
        def __init__(self, root):
            self.root = root
            self.root.title("MENINO DA TI - Seletor de Modo")
            self.root.geometry("700x500")
            self.root.resizable(False, False)
            
            self.selected_mode = None
            
            self._setup_ui()
            center_window(self.root, 700, 500)
        
        def _setup_ui(self):
            """Configura a interface de seleção"""
            main_frame = ttk.Frame(self.root, padding="20")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Título
            title = ttk.Label(
                main_frame,
                text="🔧 MENINO DA TI 🔧",
                font=("Arial", 22, "bold")
            )
            title.pack(pady=(0, 5))
            
            subtitle = ttk.Label(
                main_frame,
                text="Escolha o Modo de Inicialização",
                font=("Arial", 12)
            )
            subtitle.pack(pady=(0, 20))
            
            # Frame para botões
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill=tk.BOTH, expand=True, pady=10)
            
            # Botão modo console
            console_btn = tk.Button(
                button_frame,
                text="📟 Modo Console\n\nInterface com arte ASCII\nDiagnostico em linha de comando",
                command=self._select_console,
                font=("Arial", 10),
                relief=tk.RAISED,
                borderwidth=2,
                bg="#f0f0f0",
                cursor="hand2"
            )
            console_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
            
            # Botão modo gráfico
            gui_btn = tk.Button(
                button_frame,
                text="🖥️  Modo Gráfico\n\nInterface completa\nCom tela de carregamento",
                command=self._select_gui,
                font=("Arial", 10),
                relief=tk.RAISED,
                borderwidth=2,
                bg="#f0f0f0",
                cursor="hand2"
            )
            gui_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
            
            # Frame inferior com informações
            info_frame = ttk.LabelFrame(main_frame, text="ℹ️ Informação", padding="10")
            info_frame.pack(fill=tk.X, pady=(10, 0))
            
            info_text = ttk.Label(
                info_frame,
                text="Você pode executar a aplicação em modo console (sem interface gráfica) "
                     "ou em modo gráfico (com interface completa e tela de carregamento).",
                wraplength=600,
                justify=tk.LEFT,
                font=("Arial", 9)
            )
            info_text.pack()
        
        def _select_console(self):
            """Seleciona modo console"""
            self.selected_mode = "console"
            self.root.quit()
        
        def _select_gui(self):
            """Seleciona modo gráfico"""
            self.selected_mode = "gui"
            self.root.quit()
        
        def get_selected_mode(self):
            """Retorna o modo selecionado"""
            return self.selected_mode
    
    # Criar janela de seleção
    launcher_root = tk.Tk()
    launcher = ModeLauncher(launcher_root)
    
    launcher_root.mainloop()
    
    # Obter modo selecionado
    return launcher.get_selected_mode()


def main():
    """Função principal"""
    # Verificar compatibilidade do sistema
    print("\n" + "="*75)
    print("MENINO DA TI - VERIFICAÇÃO DE SISTEMA")
    print("="*75 + "\n")
    
    system_checker = SystemChecker()
    system_checker.print_system_info()
    
    is_compatible = system_checker.print_compatibility_status()
    
    if not is_compatible:
        print("\n[ERRO] Este aplicativo requer Windows 10 ou superior!")
        print("Por favor, atualize seu sistema operacional para continuar.\n")
        input("Pressione Enter para sair...")
        sys.exit(1)
    
    # Verificar argumentos da linha de comando
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        # Se nenhum argumento, abrir seletor de modo
        mode = launch_launcher_mode()
    
    if mode == "console":
        launch_console_mode()
    elif mode == "gui":
        launch_gui_mode()
    else:
        print("Modo inválido! Use: python auto_launcher.py [console|gui]")
        sys.exit(1)


if __name__ == "__main__":
    main()
