"""
Menino de TI Helper - Windows Update Automation Tool
Automatically updates all applications and runs Windows Update
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import logging
import sys
from datetime import datetime
from powershell_manager import PowerShellManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'menino_ti_helper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MeninoDeTIHelper:
    """Main application class for Menino de TI Helper"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Menino de TI Helper")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Initialize PowerShell manager
        self.ps_manager = PowerShellManager()
        
        # Track if updates are running
        self.is_running = False
        
        # Setup UI
        self.setup_ui()
        
        # Check admin privileges on startup
        self.root.after(100, self.check_prerequisites)
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="🔧 Menino de TI Helper 🔧",
            font=("Arial", 20, "bold")
        )
        title_label.grid(row=0, column=0, pady=10)
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="Atualizador Automático de Aplicativos e Windows Update",
            font=("Arial", 10)
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 20))
        
        # Control buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=10)
        
        # Update All button
        self.update_all_btn = ttk.Button(
            button_frame,
            text="▶ Atualizar Tudo (Apps + Windows)",
            command=self.start_full_update,
            width=35
        )
        self.update_all_btn.grid(row=0, column=0, padx=5)
        
        # Update Apps Only button
        self.update_apps_btn = ttk.Button(
            button_frame,
            text="📦 Atualizar Apenas Aplicativos",
            command=self.start_apps_update,
            width=35
        )
        self.update_apps_btn.grid(row=0, column=1, padx=5)
        
        # Windows Update Only button
        self.windows_update_btn = ttk.Button(
            button_frame,
            text="🪟 Atualizar Apenas Windows",
            command=self.start_windows_update,
            width=35
        )
        self.windows_update_btn.grid(row=1, column=0, padx=5, pady=5, columnspan=2)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="Progresso", padding="10")
        progress_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.rowconfigure(1, weight=1)
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Pronto para iniciar")
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(
            progress_frame,
            wrap=tk.WORD,
            height=20,
            font=("Consolas", 9)
        )
        self.output_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar at bottom
        self.status_var = tk.StringVar(value="Aguardando...")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
    def log_output(self, message: str, level: str = "INFO"):
        """Log message to both the UI and logger"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {level}: {message}\n"
        
        # Update UI in thread-safe way
        self.root.after(0, self._append_to_output, formatted_message)
        
        # Log to file
        if level == "ERROR":
            logger.error(message)
        elif level == "WARNING":
            logger.warning(message)
        else:
            logger.info(message)
    
    def _append_to_output(self, text: str):
        """Append text to output widget (must be called from main thread)"""
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        
    def update_status(self, status: str):
        """Update status bar"""
        self.root.after(0, self.status_var.set, status)
        
    def update_progress(self, progress: str):
        """Update progress label"""
        self.root.after(0, self.progress_var.set, progress)
        
    def set_buttons_state(self, state: str):
        """Enable or disable buttons"""
        self.root.after(0, self._set_buttons_state_impl, state)
        
    def _set_buttons_state_impl(self, state: str):
        """Implementation of button state change (must be called from main thread)"""
        self.update_all_btn.config(state=state)
        self.update_apps_btn.config(state=state)
        self.windows_update_btn.config(state=state)
        
    def check_prerequisites(self):
        """Check if prerequisites are met"""
        self.log_output("Verificando pré-requisitos...")
        
        # Check admin privileges
        if not self.ps_manager.check_admin_privileges():
            self.log_output("AVISO: Não está executando como Administrador!", "WARNING")
            self.log_output("Algumas operações podem falhar. Recomenda-se executar como Administrador.", "WARNING")
            messagebox.showwarning(
                "Aviso de Privilégios",
                "O aplicativo não está sendo executado como Administrador.\n\n"
                "Para melhor funcionamento, clique com botão direito no aplicativo\n"
                "e selecione 'Executar como administrador'."
            )
        else:
            self.log_output("✓ Executando como Administrador")
        
        # Check winget
        is_installed, msg = self.ps_manager.install_winget_if_needed()
        if is_installed:
            self.log_output("✓ Winget está disponível")
        else:
            self.log_output(f"✗ {msg}", "WARNING")
            
        self.log_output("Verificação de pré-requisitos concluída")
        self.update_status("Pronto")
        
    def start_full_update(self):
        """Start full update (apps + Windows)"""
        if self.is_running:
            messagebox.showinfo("Já em execução", "Uma atualização já está em andamento.")
            return
            
        result = messagebox.askyesno(
            "Confirmar Atualização Completa",
            "Isso irá atualizar todos os aplicativos e o Windows.\n"
            "O processo pode levar bastante tempo.\n\n"
            "Deseja continuar?"
        )
        
        if result:
            self.is_running = True
            self.set_buttons_state(tk.DISABLED)
            self.output_text.delete(1.0, tk.END)
            thread = threading.Thread(target=self._run_full_update, daemon=True)
            thread.start()
    
    def start_apps_update(self):
        """Start apps update only"""
        if self.is_running:
            messagebox.showinfo("Já em execução", "Uma atualização já está em andamento.")
            return
            
        result = messagebox.askyesno(
            "Confirmar Atualização de Aplicativos",
            "Isso irá atualizar todos os aplicativos usando winget.\n\n"
            "Deseja continuar?"
        )
        
        if result:
            self.is_running = True
            self.set_buttons_state(tk.DISABLED)
            self.output_text.delete(1.0, tk.END)
            thread = threading.Thread(target=self._run_apps_update, daemon=True)
            thread.start()
    
    def start_windows_update(self):
        """Start Windows Update only"""
        if self.is_running:
            messagebox.showinfo("Já em execução", "Uma atualização já está em andamento.")
            return
            
        result = messagebox.askyesno(
            "Confirmar Windows Update",
            "Isso irá executar o Windows Update.\n"
            "O processo pode levar bastante tempo.\n\n"
            "Deseja continuar?"
        )
        
        if result:
            self.is_running = True
            self.set_buttons_state(tk.DISABLED)
            self.output_text.delete(1.0, tk.END)
            thread = threading.Thread(target=self._run_windows_update, daemon=True)
            thread.start()
    
    def _run_full_update(self):
        """Run full update in background thread"""
        try:
            self.log_output("="*60)
            self.log_output("INICIANDO ATUALIZAÇÃO COMPLETA")
            self.log_output("="*60)
            
            # Step 1: Update apps
            self.update_progress("1/2 - Atualizando aplicativos...")
            self.update_status("Atualizando aplicativos com winget...")
            self._run_apps_update_impl()
            
            # Step 2: Update Windows
            self.update_progress("2/2 - Atualizando Windows...")
            self.update_status("Executando Windows Update...")
            self._run_windows_update_impl()
            
            self.log_output("="*60)
            self.log_output("ATUALIZAÇÃO COMPLETA FINALIZADA")
            self.log_output("="*60)
            self.update_progress("Concluído!")
            self.update_status("Atualização completa finalizada")
            
            self.root.after(0, messagebox.showinfo, "Concluído", 
                          "Atualização completa finalizada com sucesso!")
            
        except Exception as e:
            self.log_output(f"Erro durante atualização completa: {str(e)}", "ERROR")
            self.update_status("Erro durante atualização")
            self.root.after(0, messagebox.showerror, "Erro", 
                          f"Ocorreu um erro durante a atualização:\n{str(e)}")
        finally:
            self.is_running = False
            self.set_buttons_state(tk.NORMAL)
    
    def _run_apps_update(self):
        """Run apps update in background thread"""
        try:
            self.log_output("="*60)
            self.log_output("INICIANDO ATUALIZAÇÃO DE APLICATIVOS")
            self.log_output("="*60)
            
            self.update_progress("Atualizando aplicativos...")
            self.update_status("Atualizando aplicativos com winget...")
            
            self._run_apps_update_impl()
            
            self.log_output("="*60)
            self.log_output("ATUALIZAÇÃO DE APLICATIVOS FINALIZADA")
            self.log_output("="*60)
            self.update_progress("Concluído!")
            self.update_status("Atualização de aplicativos finalizada")
            
            self.root.after(0, messagebox.showinfo, "Concluído", 
                          "Atualização de aplicativos finalizada!")
            
        except Exception as e:
            self.log_output(f"Erro durante atualização de aplicativos: {str(e)}", "ERROR")
            self.update_status("Erro durante atualização")
            self.root.after(0, messagebox.showerror, "Erro", 
                          f"Ocorreu um erro:\n{str(e)}")
        finally:
            self.is_running = False
            self.set_buttons_state(tk.NORMAL)
    
    def _run_windows_update(self):
        """Run Windows Update in background thread"""
        try:
            self.log_output("="*60)
            self.log_output("INICIANDO WINDOWS UPDATE")
            self.log_output("="*60)
            
            self.update_progress("Atualizando Windows...")
            self.update_status("Executando Windows Update...")
            
            self._run_windows_update_impl()
            
            self.log_output("="*60)
            self.log_output("WINDOWS UPDATE FINALIZADO")
            self.log_output("="*60)
            self.update_progress("Concluído!")
            self.update_status("Windows Update finalizado")
            
            self.root.after(0, messagebox.showinfo, "Concluído", 
                          "Windows Update finalizado!")
            
        except Exception as e:
            self.log_output(f"Erro durante Windows Update: {str(e)}", "ERROR")
            self.update_status("Erro durante Windows Update")
            self.root.after(0, messagebox.showerror, "Erro", 
                          f"Ocorreu um erro:\n{str(e)}")
        finally:
            self.is_running = False
            self.set_buttons_state(tk.NORMAL)
    
    def _run_apps_update_impl(self):
        """Implementation of apps update"""
        self.log_output("Verificando winget...")
        is_installed, msg = self.ps_manager.install_winget_if_needed()
        
        if not is_installed:
            self.log_output(msg, "ERROR")
            raise Exception(msg)
        
        self.log_output("Iniciando atualização de aplicativos com winget...")
        self.log_output("Isso pode levar vários minutos dependendo da quantidade de atualizações...")
        
        success, output = self.ps_manager.update_all_apps_with_winget()
        
        # Display output
        if output:
            for line in output.split('\n'):
                if line.strip():
                    self.log_output(line)
        
        if success:
            self.log_output("✓ Aplicativos atualizados com sucesso!")
        else:
            self.log_output("✗ Houve problemas na atualização de aplicativos", "WARNING")
            self.log_output("Verifique o log acima para mais detalhes", "WARNING")
    
    def _run_windows_update_impl(self):
        """Implementation of Windows Update"""
        self.log_output("Verificando módulo PSWindowsUpdate...")
        
        # Install module if needed
        module_success, module_msg = self.ps_manager.install_pswindowsupdate_module()
        self.log_output(module_msg)
        
        if not module_success:
            raise Exception(module_msg)
        
        self.log_output("Iniciando Windows Update...")
        self.log_output("Isso pode levar muito tempo dependendo das atualizações disponíveis...")
        self.log_output("Por favor, seja paciente...")
        
        success, output = self.ps_manager.run_windows_update()
        
        # Display output
        if output:
            for line in output.split('\n'):
                if line.strip():
                    self.log_output(line)
        
        if success or "No updates available" in output or "não há atualizações" in output.lower():
            self.log_output("✓ Windows Update concluído!")
        else:
            self.log_output("✗ Houve problemas no Windows Update", "WARNING")
            self.log_output("Verifique o log acima para mais detalhes", "WARNING")


def show_splash_screen():
    """Show splash screen on startup"""
    splash = tk.Tk()
    splash.title("Menino de TI Helper")
    splash.geometry("400x300")
    splash.resizable(False, False)
    
    # Center the window
    splash.update_idletasks()
    x = (splash.winfo_screenwidth() // 2) - (400 // 2)
    y = (splash.winfo_screenheight() // 2) - (300 // 2)
    splash.geometry(f"400x300+{x}+{y}")
    
    # Remove window decorations for splash
    splash.overrideredirect(True)
    
    # Create splash content
    frame = ttk.Frame(splash, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Title
    title = ttk.Label(
        frame,
        text="🔧 Menino de TI Helper 🔧",
        font=("Arial", 18, "bold")
    )
    title.pack(pady=20)
    
    # Subtitle
    subtitle = ttk.Label(
        frame,
        text="Atualizador Automático para Windows 11",
        font=("Arial", 10)
    )
    subtitle.pack(pady=5)
    
    # Version
    version = ttk.Label(
        frame,
        text="Versão 1.0",
        font=("Arial", 8)
    )
    version.pack(pady=5)
    
    # Loading message
    loading = ttk.Label(
        frame,
        text="Carregando...",
        font=("Arial", 9)
    )
    loading.pack(pady=20)
    
    # Progress bar
    progress = ttk.Progressbar(frame, mode='indeterminate', length=300)
    progress.pack(pady=10)
    progress.start(10)
    
    # Info
    info = ttk.Label(
        frame,
        text="Atualiza aplicativos e Windows automaticamente",
        font=("Arial", 8),
        foreground="gray"
    )
    info.pack(side=tk.BOTTOM, pady=10)
    
    # Close splash after 3 seconds
    splash.after(3000, splash.destroy)
    splash.mainloop()


def main():
    """Main entry point"""
    try:
        # Show splash screen
        show_splash_screen()
        
        # Create main application
        root = tk.Tk()
        
        # Center the main window
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (800 // 2)
        y = (root.winfo_screenheight() // 2) - (600 // 2)
        root.geometry(f"800x600+{x}+{y}")
        
        app = MeninoDeTIHelper(root)
        
        # Run the application
        root.mainloop()
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        messagebox.showerror("Erro Fatal", f"Ocorreu um erro fatal:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
