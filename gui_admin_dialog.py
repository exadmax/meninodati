"""
gui_admin_dialog.py - Diálogo de orientação para execução como administrador
"""
import tkinter as tk
from tkinter import ttk
from gui_constants import ADMIN_WINDOW_WIDTH, ADMIN_WINDOW_HEIGHT
from gui_utils import center_window


class AdminWarningDialog:
    """Diálogo de orientação para execução como administrador"""
    
    def __init__(self, parent):
        """
        Inicializa o diálogo de aviso.
        
        Args:
            parent: Janela pai (Tk root)
        """
        self.result = False
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("⚠️ Permissões de Administrador")
        self.dialog.geometry(f"{ADMIN_WINDOW_WIDTH}x{ADMIN_WINDOW_HEIGHT}")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centralizar janela
        center_window(self.dialog, ADMIN_WINDOW_WIDTH, ADMIN_WINDOW_HEIGHT)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface do diálogo"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Ícone de aviso
        warning_label = ttk.Label(
            main_frame,
            text="⚠️",
            font=("Arial", 48)
        )
        warning_label.pack(pady=(0, 10))
        
        # Título
        title = ttk.Label(
            main_frame,
            text="Este aplicativo requer privilégios de Administrador",
            font=("Arial", 14, "bold"),
            wraplength=550
        )
        title.pack(pady=10)
        
        # Descrição
        desc = ttk.Label(
            main_frame,
            text="Para executar atualizações do sistema e aplicativos, "
                 "é necessário executar este programa como Administrador.",
            font=("Arial", 10),
            wraplength=550
        )
        desc.pack(pady=10)
        
        # Frame de instruções
        instructions_frame = ttk.LabelFrame(
            main_frame,
            text="📋 Como executar como Administrador",
            padding="15"
        )
        instructions_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        instructions = [
            "1. Feche este programa",
            "2. Localize o arquivo 'MeninoDeTIHelper.exe' no seu computador",
            "3. Clique com o botão DIREITO do mouse sobre o arquivo",
            "4. Selecione a opção 'Executar como administrador'",
            "5. Na janela de confirmação (UAC), clique em 'Sim'",
            "",
            "OU",
            "",
            "1. Clique com o botão DIREITO sobre o arquivo",
            "2. Selecione 'Propriedades'",
            "3. Vá para a aba 'Compatibilidade'",
            "4. Marque 'Executar este programa como administrador'",
            "5. Clique em 'OK' e execute o programa normalmente"
        ]
        
        for instruction in instructions:
            if instruction == "" or instruction == "OU":
                label = ttk.Label(
                    instructions_frame,
                    text=instruction,
                    font=("Arial", 9, "bold")
                )
            else:
                label = ttk.Label(
                    instructions_frame,
                    text=instruction,
                    font=("Arial", 9)
                )
            label.pack(anchor=tk.W, pady=2)
        
        # Frame de botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20, fill=tk.X)
        
        # Botão continuar mesmo assim
        continue_btn = ttk.Button(
            button_frame,
            text="Continuar Mesmo Assim (Não Recomendado)",
            command=self.continue_anyway
        )
        continue_btn.pack(side=tk.LEFT, padx=5)
        
        # Botão fechar
        close_btn = ttk.Button(
            button_frame,
            text="Fechar Programa",
            command=self.close_program
        )
        close_btn.pack(side=tk.RIGHT, padx=5)
        
    def continue_anyway(self):
        """Continua sem privilégios de admin"""
        self.result = True
        self.dialog.destroy()
        
    def close_program(self):
        """Fecha o programa"""
        self.result = False
        self.dialog.destroy()
