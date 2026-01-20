"""
build_launcher.py - Launcher para o construtor de executável
Oferece opções de build via CLI ou GUI
"""
import sys
import tkinter as tk
from tkinter import ttk
import subprocess
from gui_utils import center_window


class BuildLauncher:
    """Seletor de opções de build"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("MENINO DA TI - Construtor de Executável")
        self.root.geometry("700x400")
        self.root.resizable(False, False)
        
        self.selected_mode = None
        self._setup_ui()
        center_window(self.root, 700, 400)
    
    def _setup_ui(self):
        """Configura a interface"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = ttk.Label(
            main_frame,
            text="🔧 Construtor de Executável",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(0, 5))
        
        subtitle = ttk.Label(
            main_frame,
            text="MENINO DA TI - Converter Python em .exe",
            font=("Arial", 11),
            foreground="gray"
        )
        subtitle.pack(pady=(0, 20))
        
        # Frame de opções
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Botão GUI
        gui_btn = tk.Button(
            button_frame,
            text="🖥️  Interface Gráfica\n\nJanela com progresso visual\nMais fácil de usar",
            command=self._select_gui,
            font=("Arial", 11),
            relief=tk.RAISED,
            borderwidth=2,
            bg="#e8f4f8",
            cursor="hand2",
            height=5
        )
        gui_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Botão CLI
        cli_btn = tk.Button(
            button_frame,
            text="📟 Modo Console\n\nExecução em linha de comando\nMais direto",
            command=self._select_cli,
            font=("Arial", 11),
            relief=tk.RAISED,
            borderwidth=2,
            bg="#f8f4e8",
            cursor="hand2",
            height=5
        )
        cli_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Frame de informações
        info_frame = ttk.LabelFrame(main_frame, text="ℹ️ Informação", padding="10")
        info_frame.pack(fill=tk.X, pady=(20, 0))
        
        info_text = ttk.Label(
            info_frame,
            text="O construtor converterá o MENINO DA TI em um executável (.exe) independente.\n"
                 "Escolha a interface que preferir: gráfica ou console.",
            wraplength=600,
            justify=tk.LEFT,
            font=("Arial", 9)
        )
        info_text.pack()
    
    def _select_gui(self):
        """Seleciona modo GUI"""
        self.selected_mode = "gui"
        self.root.quit()
    
    def _select_cli(self):
        """Seleciona modo CLI"""
        self.selected_mode = "cli"
        self.root.quit()
    
    def get_selected_mode(self):
        """Retorna o modo selecionado"""
        return self.selected_mode


def main():
    """Função principal"""
    launcher_root = tk.Tk()
    launcher = BuildLauncher(launcher_root)
    
    launcher_root.mainloop()
    
    mode = launcher.get_selected_mode()
    
    if mode == "gui":
        try:
            from gui_exe_builder import main as gui_main
            gui_main()
        except Exception as e:
            print(f"Erro ao iniciar interface gráfica: {e}")
            print("Iniciando em modo console como fallback...")
            subprocess.run([sys.executable, "build_exe.py"])
    
    elif mode == "cli":
        subprocess.run([sys.executable, "build_exe.py"])
    
    else:
        print("Nenhuma opção selecionada.")


if __name__ == "__main__":
    main()
