"""
gui_progress_window.py - Janela de progresso com barra 0-100%
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from gui_constants import PROGRESS_WINDOW_WIDTH, PROGRESS_WINDOW_HEIGHT, LOG_TIMESTAMP_FORMAT
from gui_utils import center_window


class ProgressWindow:
    """Janela de progresso com barra de 0-100%"""
    
    def __init__(self, parent, title="Processando..."):
        """
        Inicializa a janela de progresso.
        
        Args:
            parent: Janela pai (Tk root)
            title: Título da janela
        """
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry(f"{PROGRESS_WINDOW_WIDTH}x{PROGRESS_WINDOW_HEIGHT}")
        self.window.resizable(False, False)
        self.window.transient(parent)
        
        # Centralizar
        center_window(self.window, PROGRESS_WINDOW_WIDTH, PROGRESS_WINDOW_HEIGHT)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface da janela de progresso"""
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título do passo atual
        self.step_var = tk.StringVar(value="Iniciando...")
        step_label = ttk.Label(
            main_frame,
            textvariable=self.step_var,
            font=("Arial", 14, "bold")
        )
        step_label.pack(pady=(0, 10))
        
        # Descrição do passo
        self.desc_var = tk.StringVar(value="Preparando ambiente...")
        desc_label = ttk.Label(
            main_frame,
            textvariable=self.desc_var,
            font=("Arial", 10)
        )
        desc_label.pack(pady=(0, 20))
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            length=600
        )
        self.progress_bar.pack(pady=10)
        
        # Porcentagem
        self.percent_var = tk.StringVar(value="0%")
        percent_label = ttk.Label(
            main_frame,
            textvariable=self.percent_var,
            font=("Arial", 20, "bold")
        )
        percent_label.pack(pady=10)
        
        # Frame de detalhes
        details_frame = ttk.LabelFrame(
            main_frame,
            text="Detalhes",
            padding="10"
        )
        details_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Área de texto com scroll para logs
        text_frame = ttk.Frame(details_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            height=10,
            font=("Consolas", 8),
            yscrollcommand=scrollbar.set
        )
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # Status bar
        self.status_var = tk.StringVar(value="Aguardando...")
        status_label = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            font=("Arial", 8),
            foreground="gray"
        )
        status_label.pack(pady=(5, 0))
        
    def update_progress(self, percent, step_text="", desc_text="", log_text=""):
        """
        Atualiza a barra de progresso.
        
        Args:
            percent: Porcentagem (0-100)
            step_text: Texto do passo
            desc_text: Descrição
            log_text: Texto do log
        """
        self.progress_var.set(percent)
        self.percent_var.set(f"{int(percent)}%")
        
        if step_text:
            self.step_var.set(step_text)
        if desc_text:
            self.desc_var.set(desc_text)
        if log_text:
            self.log(log_text)
            
        self.window.update()
        
    def log(self, message):
        """
        Adiciona mensagem ao log.
        
        Args:
            message: Mensagem para adicionar
        """
        timestamp = datetime.now().strftime(LOG_TIMESTAMP_FORMAT)
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.window.update()
        
    def set_status(self, status):
        """
        Atualiza o status.
        
        Args:
            status: Novo status
        """
        self.status_var.set(status)
        self.window.update()
        
    def close(self):
        """Fecha a janela"""
        self.window.destroy()
