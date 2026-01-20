"""
splash_screen.py - Tela de inicialização com loading em modo gráfico
"""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import threading
import time
from typing import Callable

class SplashScreen:
    """Tela de splash com imagem de carregamento"""
    
    def __init__(self, parent=None, image_path: str = None, duration: float = 3.0):
        """
        Inicializa a tela de splash
        
        Args:
            parent: Janela pai (opcional)
            image_path: Caminho para a imagem loading.png
            duration: Duração da animação em segundos
        """
        self.root = tk.Toplevel(parent) if parent else tk.Tk()
        self.root.title("Carregando...")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.95)
        
        self.duration = duration
        self.image_path = image_path
        self.start_time = time.time()
        self.is_running = True
        self._callback = None
        self._complete_callback = None
        
        # Construir interface
        self._setup_ui()
        self._center_window()
        
        # Iniciar animação
        self._animate()
    
    def _setup_ui(self):
        """Configura a interface da tela de splash"""
        main_frame = ttk.Frame(self.root, relief=tk.SUNKEN, borderwidth=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Título
        title = ttk.Label(
            main_frame,
            text="🔧 MENINO DA TI 🔧",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=(15, 10))
        
        # Imagem de carregamento se existir
        self.photo_image = None
        self.image_label = None
        if self.image_path and os.path.exists(self.image_path):
            try:
                image = Image.open(self.image_path)
                # Redimensionar se necessário
                image.thumbnail((300, 200), Image.Resampling.LANCZOS)
                self.photo_image = ImageTk.PhotoImage(image)
                
                # Manter referência ao label também
                self.image_label = ttk.Label(main_frame, image=self.photo_image)
                self.image_label.pack(pady=10)
                # Garantir que a imagem não seja coletada pelo garbage collector
                self.image_label.image = self.photo_image
            except Exception as e:
                print(f"⚠️  Aviso: Não foi possível carregar imagem de splash: {e}")
                # Continuar sem imagem - não é erro crítico
                self.photo_image = None
                self.image_label = None
        
        # Texto de carregamento
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.status_label = ttk.Label(
            text_frame,
            text="Carregando componentes...",
            font=("Arial", 11)
        )
        self.status_label.pack()
        
        # Barra de progresso com animação
        self.progress_var = tk.DoubleVar(value=0)
        progress_bar = ttk.Progressbar(
            text_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            length=250
        )
        progress_bar.pack(fill=tk.X, pady=(10, 5))
        
        # Percentual
        self.percent_label = ttk.Label(
            text_frame,
            text="0%",
            font=("Arial", 9),
            foreground="gray"
        )
        self.percent_label.pack()
        
        # Subtítulo
        subtitle = ttk.Label(
            main_frame,
            text="Diagnostico de Sistema v1.0",
            font=("Arial", 9),
            foreground="gray"
        )
        subtitle.pack(pady=(0, 15))
    
    def _center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def _animate(self):
        """Anima o progresso da barra"""
        if not self.is_running:
            return
        
        elapsed = time.time() - self.start_time
        progress = min((elapsed / self.duration) * 100, 100)
        
        self.progress_var.set(progress)
        self.percent_label.config(text=f"{int(progress)}%")
        
        # Status alternado
        statuses = [
            "Carregando componentes...",
            "Inicializando sistema...",
            "Preparando interface...",
            "Quase pronto...",
        ]
        status_index = int((progress / 100) * len(statuses))
        if status_index < len(statuses):
            self.status_label.config(text=statuses[status_index])
        
        if self._callback:
            self._callback(int(progress))
        
        # Verificar se terminou
        if progress >= 100:
            self.is_running = False
            if self._complete_callback:
                self._complete_callback()
            self.root.after(500, self._close)
        else:
            self.root.after(50, self._animate)
    
    def _close(self):
        """Fecha a janela de splash"""
        try:
            self.root.destroy()
        except:
            pass
    
    def set_progress_callback(self, callback: Callable[[int], None]):
        """Define callback para progresso (0-100)"""
        self._callback = callback
    
    def set_complete_callback(self, callback: Callable[[], None]):
        """Define callback para quando terminar"""
        self._complete_callback = callback
    
    def close(self):
        """Fecha a splash screen"""
        self.is_running = False
        self._close()
    
    def mainloop(self):
        """Mantém a janela aberta"""
        self.root.mainloop()


def test_splash():
    """Testa a tela de splash"""
    root = tk.Tk()
    root.withdraw()
    
    # Caminho da imagem
    image_path = os.path.join(os.path.dirname(__file__), 'img', 'loading.png')
    
    splash = SplashScreen(root, image_path=image_path, duration=3.0)
    
    root.after(3500, root.quit)
    root.mainloop()


if __name__ == "__main__":
    test_splash()
