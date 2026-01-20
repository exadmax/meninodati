"""
gui_cleanup_dialog.py - Interface gráfica para limpeza de cache e temporários
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from cleanup_manager import CleanupManager, get_cleanup_info
from gui_utils import center_window
import logging

logger = logging.getLogger(__name__)


class CleanupDialog:
    """Diálogo para limpeza de cache, temporários e lixeira"""
    
    def __init__(self, parent):
        """
        Inicializa o diálogo de limpeza.
        
        Args:
            parent: Janela pai
        """
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("🧹 Limpeza do Sistema")
        self.dialog.geometry("800x600")
        self.dialog.resizable(True, True)
        self.dialog.grab_set()
        
        # Variáveis de estado
        self.is_cleaning = False
        self.cleanup_manager = None
        self.cleanup_thread = None
        
        # Opções de limpeza
        self.clean_cache_var = tk.BooleanVar(value=True)
        self.clean_temp_var = tk.BooleanVar(value=True)
        self.clean_recycle_var = tk.BooleanVar(value=True)
        
        # Setup UI
        self.setup_ui()
        self.load_cleanup_info()
        
        # Centralizar janela
        center_window(self.dialog, 800, 600)
    
    def setup_ui(self):
        """Configura a interface do diálogo"""
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame,
            text="🧹 Limpeza do Sistema",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(
            main_frame,
            text="Libere espaço limpando cache, arquivos temporários e lixeira de forma segura",
            font=("Arial", 10),
            foreground="gray"
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Frame de opções
        options_frame = ttk.LabelFrame(main_frame, text="📋 Opções de Limpeza", padding="15")
        options_frame.pack(fill=tk.X, pady=10)
        
        # Cache
        cache_frame = ttk.Frame(options_frame)
        cache_frame.pack(fill=tk.X, pady=10)
        
        cache_check = ttk.Checkbutton(
            cache_frame,
            text="🗂️ Limpar Cache",
            variable=self.clean_cache_var
        )
        cache_check.pack(side=tk.LEFT)
        
        self.cache_info_label = ttk.Label(
            cache_frame,
            text="Verificando...",
            font=("Arial", 9),
            foreground="gray"
        )
        self.cache_info_label.pack(side=tk.RIGHT)
        
        cache_desc = ttk.Label(
            options_frame,
            text="  • Cache de navegadores, Windows e aplicativos\n  • Arquivos de dados em cache local",
            font=("Arial", 9),
            foreground="darkgray"
        )
        cache_desc.pack(fill=tk.X, padx=(30, 0))
        
        # Temporários
        temp_frame = ttk.Frame(options_frame)
        temp_frame.pack(fill=tk.X, pady=10)
        
        temp_check = ttk.Checkbutton(
            temp_frame,
            text="📁 Limpar Arquivos Temporários",
            variable=self.clean_temp_var
        )
        temp_check.pack(side=tk.LEFT)
        
        self.temp_info_label = ttk.Label(
            temp_frame,
            text="Verificando...",
            font=("Arial", 9),
            foreground="gray"
        )
        self.temp_info_label.pack(side=tk.RIGHT)
        
        temp_desc = ttk.Label(
            options_frame,
            text="  • Pasta Temp do Windows (%TEMP%)\n  • Arquivos temporários de aplicativos",
            font=("Arial", 9),
            foreground="darkgray"
        )
        temp_desc.pack(fill=tk.X, padx=(30, 0))
        
        # Lixeira
        recycle_frame = ttk.Frame(options_frame)
        recycle_frame.pack(fill=tk.X, pady=10)
        
        recycle_check = ttk.Checkbutton(
            recycle_frame,
            text="🗑️ Esvaziar Lixeira",
            variable=self.clean_recycle_var
        )
        recycle_check.pack(side=tk.LEFT)
        
        self.recycle_info_label = ttk.Label(
            recycle_frame,
            text="Verificando...",
            font=("Arial", 9),
            foreground="gray"
        )
        self.recycle_info_label.pack(side=tk.RIGHT)
        
        recycle_desc = ttk.Label(
            options_frame,
            text="  • Recycle Bin (Lixeira do Windows)",
            font=("Arial", 9),
            foreground="darkgray"
        )
        recycle_desc.pack(fill=tk.X, padx=(30, 0))
        
        # Aviso de segurança
        warning_frame = ttk.LabelFrame(main_frame, text="⚠️ Aviso Importante", padding="10")
        warning_frame.pack(fill=tk.X, pady=10)
        
        warning_text = (
            "Esta ferramenta foi desenvolvida com segurança em mente:\n"
            "✓ Apenas arquivos de cache e temporários são deletados\n"
            "✓ Nenhum arquivo de usuario é afetado\n"
            "✓ Pastas não são deletadas, apenas seu conteúdo\n"
            "✓ Arquivos em uso são preservados"
        )
        
        warning_label = ttk.Label(
            warning_frame,
            text=warning_text,
            font=("Arial", 9),
            justify=tk.LEFT
        )
        warning_label.pack(fill=tk.X)
        
        # Frame de progresso (inicialmente oculto)
        progress_frame = ttk.LabelFrame(main_frame, text="📊 Progresso", padding="15")
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            value=0,
            length=400
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_var = tk.StringVar(value="Clique em 'Iniciar Limpeza' para começar")
        self.progress_label = ttk.Label(
            progress_frame,
            textvariable=self.progress_var,
            font=("Arial", 9)
        )
        self.progress_label.pack(fill=tk.X)
        
        # Frame de log (inicialmente oculto)
        log_frame = ttk.LabelFrame(main_frame, text="📝 Log de Operações", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scrollbar para log
        scrollbar = ttk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(
            log_frame,
            height=8,
            font=("Courier", 8),
            yscrollcommand=scrollbar.set
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # Frame de botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.start_btn = ttk.Button(
            button_frame,
            text="▶️ Iniciar Limpeza",
            command=self.start_cleanup
        )
        self.start_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.cancel_btn = ttk.Button(
            button_frame,
            text="✖️ Fechar",
            command=self.dialog.destroy,
            state=tk.DISABLED
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=5)
        
        self.close_btn = ttk.Button(
            button_frame,
            text="✖️ Fechar",
            command=self.dialog.destroy
        )
        self.close_btn.pack(side=tk.RIGHT, padx=(5, 0))
    
    def load_cleanup_info(self):
        """Carrega informações sobre o que pode ser limpo"""
        def load_info_thread():
            try:
                info = get_cleanup_info()
                
                # Formatar tamanhos
                def format_size(bytes_size):
                    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                        if bytes_size < 1024.0:
                            return f"{bytes_size:.1f} {unit}"
                        bytes_size /= 1024.0
                    return f"{bytes_size:.1f} PB"
                
                # Atualizar labels
                cache_size = format_size(info['cache_size'])
                temp_size = format_size(info['temp_size'])
                recycle_size = format_size(info['recycle_size'])
                
                self.cache_info_label.config(
                    text=f"({len(info['cache_folders'])} pastas, ~{cache_size})"
                )
                self.temp_info_label.config(
                    text=f"({len(info['temp_folders'])} pastas, ~{temp_size})"
                )
                self.recycle_info_label.config(
                    text=f"(~{recycle_size})"
                )
                
            except Exception as e:
                logger.error(f"Erro ao carregar informações: {e}")
        
        # Executar em thread para não congelar UI
        thread = threading.Thread(target=load_info_thread, daemon=True)
        thread.start()
    
    def add_log_message(self, message: str, level: str = "INFO"):
        """
        Adiciona mensagem ao log.
        
        Args:
            message: Mensagem para logar
            level: Nível (INFO, WARNING, ERROR, SUCCESS)
        """
        self.log_text.config(state=tk.NORMAL)
        
        # Tag para cores
        if level == "SUCCESS":
            self.log_text.insert(tk.END, f"✓ {message}\n", "success")
        elif level == "ERROR":
            self.log_text.insert(tk.END, f"✗ {message}\n", "error")
        elif level == "WARNING":
            self.log_text.insert(tk.END, f"⚠ {message}\n", "warning")
        else:
            self.log_text.insert(tk.END, f"→ {message}\n", "info")
        
        # Rolar para o fim
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.log_text.update()
    
    def configure_log_tags(self):
        """Configura tags de cores para o log"""
        self.log_text.tag_config("success", foreground="green")
        self.log_text.tag_config("error", foreground="red")
        self.log_text.tag_config("warning", foreground="orange")
        self.log_text.tag_config("info", foreground="blue")
    
    def cleanup_thread_func(self):
        """Função executada em thread para limpeza"""
        try:
            # Determinar o que limpar
            cleanup_options = []
            if self.clean_cache_var.get():
                cleanup_options.append("cache")
            if self.clean_temp_var.get():
                cleanup_options.append("temp")
            if self.clean_recycle_var.get():
                cleanup_options.append("recycle")
            
            if not cleanup_options:
                self.add_log_message("Nenhuma opção selecionada!", "WARNING")
                return
            
            # Criar gerenciador
            self.cleanup_manager = CleanupManager(self.progress_callback)
            
            self.add_log_message("Iniciando limpeza do sistema...", "INFO")
            
            # Executar limpeza
            if len(cleanup_options) == 3:
                # Limpeza completa
                results = self.cleanup_manager.cleanup_all()
            else:
                # Limpeza seletiva
                results = {
                    'cache': None,
                    'temp': None,
                    'recycle': None,
                    'summary': {
                        'total_files': 0,
                        'total_bytes': 0
                    }
                }
                
                if "cache" in cleanup_options:
                    self.add_log_message("Limpando cache...", "INFO")
                    results['cache'] = self.cleanup_manager.clean_cache()
                    results['summary']['total_files'] += results['cache']['files_deleted']
                    results['summary']['total_bytes'] += results['cache']['bytes_freed']
                
                if "temp" in cleanup_options:
                    self.add_log_message("Limpando temporários...", "INFO")
                    results['temp'] = self.cleanup_manager.clean_temp_files()
                    results['summary']['total_files'] += results['temp']['files_deleted']
                    results['summary']['total_bytes'] += results['temp']['bytes_freed']
                
                if "recycle" in cleanup_options:
                    self.add_log_message("Esvaziando lixeira...", "INFO")
                    results['recycle'] = self.cleanup_manager.empty_recycle_bin()
                    results['summary']['total_bytes'] += results['recycle']['size_freed']
            
            # Formatar resultados
            def format_size(bytes_size):
                for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                    if bytes_size < 1024.0:
                        return f"{bytes_size:.1f} {unit}"
                    bytes_size /= 1024.0
                return f"{bytes_size:.1f} PB"
            
            # Adicionar resumo
            self.add_log_message("", "INFO")  # Linha em branco
            self.add_log_message("=" * 50, "INFO")
            self.add_log_message("RESUMO DA LIMPEZA", "SUCCESS")
            self.add_log_message("=" * 50, "INFO")
            self.add_log_message(f"Arquivos deletados: {results['summary']['total_files']}", "SUCCESS")
            self.add_log_message(f"Espaço liberado: {format_size(results['summary']['total_bytes'])}", "SUCCESS")
            self.add_log_message("Limpeza concluída com sucesso!", "SUCCESS")
            
        except Exception as e:
            self.add_log_message(f"Erro durante limpeza: {e}", "ERROR")
            logger.error(f"Erro durante limpeza: {e}", exc_info=True)
    
    def progress_callback(self, message: str, progress: int):
        """
        Callback para atualizar progresso.
        
        Args:
            message: Mensagem de progresso
            progress: Percentual (0-100)
        """
        # Atualizar barra de progresso
        self.progress_bar['value'] = progress
        self.progress_var.set(f"[{progress}%] {message}")
        
        # Adicionar ao log
        self.add_log_message(message, "INFO")
        
        # Forçar atualização da UI
        self.dialog.update_idletasks()
    
    def start_cleanup(self):
        """Inicia a limpeza"""
        # Confirmar
        response = messagebox.askyesno(
            "Confirmar Limpeza",
            "Tem certeza que deseja iniciar a limpeza?\n\n"
            "Apenas arquivos de cache e temporários serão deletados.\n"
            "Nenhum arquivo de usuário será afetado.",
            icon=messagebox.WARNING
        )
        
        if not response:
            return
        
        # Configurar UI para limpeza
        self.is_cleaning = True
        self.start_btn.config(state=tk.DISABLED)
        self.close_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        
        # Limpar log anterior
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # Configurar tags
        self.configure_log_tags()
        
        # Resetar barra de progresso
        self.progress_bar['value'] = 0
        self.progress_var.set("Iniciando limpeza...")
        
        # Iniciar thread de limpeza
        self.cleanup_thread = threading.Thread(
            target=self.cleanup_thread_func,
            daemon=True
        )
        self.cleanup_thread.start()
        
        # Aguardar conclusão
        def wait_for_cleanup():
            if self.cleanup_thread and self.cleanup_thread.is_alive():
                self.dialog.after(100, wait_for_cleanup)
            else:
                # Limpeza concluída
                self.is_cleaning = False
                self.start_btn.config(state=tk.NORMAL)
                self.close_btn.config(state=tk.NORMAL)
                self.cancel_btn.config(state=tk.DISABLED)
        
        wait_for_cleanup()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    dialog = CleanupDialog(root)
    root.mainloop()
