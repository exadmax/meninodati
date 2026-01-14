"""
Menino de TI Helper - Sistema Gráfico de Atualização Automática
Versão 2.0 com Interface Gráfica Aprimorada e Barra de Progresso
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import logging
import sys
import os
import ctypes
from datetime import datetime
from powershell_manager import PowerShellManager
import re

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


def is_admin():
    """Verifica se o programa está executando como administrador"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


class AdminWarningDialog:
    """Diálogo de orientação para execução como administrador"""
    
    def __init__(self, parent):
        self.result = False
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("⚠️ Permissões de Administrador")
        self.dialog.geometry("600x500")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centralizar janela
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"600x500+{x}+{y}")
        
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
        

class ProgressWindow:
    """Janela de progresso com barra de 0-100%"""
    
    def __init__(self, parent, title="Processando..."):
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("700x450")
        self.window.resizable(False, False)
        self.window.transient(parent)
        
        # Centralizar
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.window.winfo_screenheight() // 2) - (450 // 2)
        self.window.geometry(f"700x450+{x}+{y}")
        
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
        """Atualiza a barra de progresso"""
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
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.window.update()
        
    def set_status(self, status):
        """Atualiza o status"""
        self.status_var.set(status)
        self.window.update()
        
    def close(self):
        """Fecha a janela"""
        self.window.destroy()


class MeninoDeTIHelperGUI:
    """Aplicação principal com interface gráfica aprimorada"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Menino de TI Helper - Sistema de Atualização Automática")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Verificar se é admin
        self.is_admin = is_admin()
        
        # Inicializar PowerShell manager
        self.ps_manager = PowerShellManager()
        
        # Estado
        self.is_running = False
        
        # Configurar UI
        self.setup_ui()
        
        # Verificar privilégios após UI estar pronta
        self.root.after(100, self.check_admin_privileges)
        
    def setup_ui(self):
        """Configura a interface principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            title_frame,
            text="🔧 Menino de TI Helper 🔧",
            font=("Arial", 24, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Sistema de Atualização Automática para Windows",
            font=("Arial", 11)
        )
        subtitle_label.pack()
        
        version_label = ttk.Label(
            title_frame,
            text="Versão 2.0 - Com Barra de Progresso Inteligente",
            font=("Arial", 9),
            foreground="gray"
        )
        version_label.pack()
        
        # Status de Admin
        self.admin_status_frame = ttk.Frame(main_frame)
        self.admin_status_frame.pack(fill=tk.X, pady=10)
        
        self.admin_status_var = tk.StringVar()
        self.admin_status_label = ttk.Label(
            self.admin_status_frame,
            textvariable=self.admin_status_var,
            font=("Arial", 10, "bold")
        )
        self.admin_status_label.pack()
        
        # Frame de informações
        info_frame = ttk.LabelFrame(main_frame, text="ℹ️ Informações", padding="15")
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = (
            "Este programa automatiza o processo de atualização do seu sistema:\n\n"
            "• Passo 1: Atualiza todos os aplicativos usando o Windows Package Manager (winget)\n"
            "  - Atualizações silenciosas com aceitação automática de licenças\n"
            "  - Progresso baseado na quantidade de aplicativos\n\n"
            "• Passo 2: Executa o Windows Update\n"
            "  - Instala automaticamente o módulo PSWindowsUpdate\n"
            "  - Baixa e instala atualizações do Windows\n"
            "  - Progresso traduzido do processo do Windows\n\n"
            "⏱️ O processo completo pode levar de 15 minutos a 1 hora, dependendo da quantidade de atualizações."
        )
        
        info_label = ttk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 9),
            justify=tk.LEFT
        )
        info_label.pack()
        
        # Frame de botões principais
        button_frame = ttk.LabelFrame(main_frame, text="🚀 Ações", padding="20")
        button_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Botão principal
        self.main_btn = ttk.Button(
            button_frame,
            text="▶️ INICIAR ATUALIZAÇÃO COMPLETA",
            command=self.start_full_update,
            style="Accent.TButton"
        )
        self.main_btn.pack(fill=tk.X, pady=10, ipady=15)
        
        # Botões secundários
        secondary_frame = ttk.Frame(button_frame)
        secondary_frame.pack(fill=tk.X, pady=10)
        
        self.apps_btn = ttk.Button(
            secondary_frame,
            text="📦 Apenas Aplicativos",
            command=self.start_apps_only
        )
        self.apps_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5), ipady=10)
        
        self.windows_btn = ttk.Button(
            secondary_frame,
            text="🪟 Apenas Windows Update",
            command=self.start_windows_only
        )
        self.windows_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0), ipady=10)
        
        # Botão de ajuda
        help_btn = ttk.Button(
            button_frame,
            text="❓ Como executar como Administrador",
            command=self.show_admin_help
        )
        help_btn.pack(fill=tk.X, pady=(20, 0))
        
        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_var = tk.StringVar(value="Pronto para iniciar")
        status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding="5"
        )
        status_label.pack(fill=tk.X)
        
    def check_admin_privileges(self):
        """Verifica privilégios de administrador"""
        if self.is_admin:
            self.admin_status_var.set("✅ Executando como Administrador")
            self.admin_status_label.config(foreground="green")
            self.status_var.set("Sistema pronto. Executando com privilégios de administrador.")
        else:
            self.admin_status_var.set("⚠️ NÃO está executando como Administrador")
            self.admin_status_label.config(foreground="red")
            self.status_var.set("AVISO: Recomenda-se executar como administrador para melhor funcionamento.")
            
            # Mostrar diálogo de aviso
            dialog = AdminWarningDialog(self.root)
            self.root.wait_window(dialog.dialog)
            
            if not dialog.result:
                # Usuário escolheu fechar
                self.root.quit()
                sys.exit(0)
                
    def show_admin_help(self):
        """Mostra ajuda sobre como executar como administrador"""
        dialog = AdminWarningDialog(self.root)
        
    def disable_buttons(self):
        """Desabilita todos os botões"""
        self.main_btn.config(state=tk.DISABLED)
        self.apps_btn.config(state=tk.DISABLED)
        self.windows_btn.config(state=tk.DISABLED)
        
    def enable_buttons(self):
        """Habilita todos os botões"""
        self.main_btn.config(state=tk.NORMAL)
        self.apps_btn.config(state=tk.NORMAL)
        self.windows_btn.config(state=tk.NORMAL)
        
    def start_full_update(self):
        """Inicia atualização completa"""
        if self.is_running:
            messagebox.showinfo("Em Execução", "Uma atualização já está em andamento.")
            return
            
        result = messagebox.askyesno(
            "Confirmar Atualização Completa",
            "Isso irá:\n\n"
            "1. Atualizar todos os aplicativos (com aceitação automática de licenças)\n"
            "2. Executar o Windows Update\n\n"
            "O processo pode levar bastante tempo.\n\n"
            "Deseja continuar?"
        )
        
        if result:
            self.is_running = True
            self.disable_buttons()
            thread = threading.Thread(target=self._run_full_update, daemon=True)
            thread.start()
            
    def start_apps_only(self):
        """Inicia atualização apenas de aplicativos"""
        if self.is_running:
            messagebox.showinfo("Em Execução", "Uma atualização já está em andamento.")
            return
            
        result = messagebox.askyesno(
            "Confirmar Atualização de Aplicativos",
            "Isso irá atualizar todos os aplicativos instalados usando winget.\n"
            "As licenças serão aceitas automaticamente.\n\n"
            "Deseja continuar?"
        )
        
        if result:
            self.is_running = True
            self.disable_buttons()
            thread = threading.Thread(target=self._run_apps_only, daemon=True)
            thread.start()
            
    def start_windows_only(self):
        """Inicia apenas Windows Update"""
        if self.is_running:
            messagebox.showinfo("Em Execução", "Uma atualização já está em andamento.")
            return
            
        result = messagebox.askyesno(
            "Confirmar Windows Update",
            "Isso irá:\n\n"
            "1. Instalar o módulo PSWindowsUpdate (se necessário)\n"
            "2. Executar o Windows Update\n\n"
            "O processo pode levar bastante tempo.\n\n"
            "Deseja continuar?"
        )
        
        if result:
            self.is_running = True
            self.disable_buttons()
            thread = threading.Thread(target=self._run_windows_only, daemon=True)
            thread.start()
            
    def _run_full_update(self):
        """Executa atualização completa em thread separada"""
        progress_win = None
        try:
            # Criar janela de progresso
            self.root.after(0, lambda: setattr(self, '_progress_win', 
                ProgressWindow(self.root, "Atualização Completa em Andamento")))
            
            # Aguardar criação da janela
            import time
            time.sleep(0.5)
            progress_win = getattr(self, '_progress_win', None)
            
            if not progress_win:
                raise Exception("Falha ao criar janela de progresso")
            
            # Passo 1: Aplicativos (0-50%)
            progress_win.update_progress(
                0,
                "Passo 1 de 2: Atualizando Aplicativos",
                "Preparando para atualizar aplicativos...",
                "Iniciando atualização de aplicativos"
            )
            
            self._update_apps_with_progress(progress_win, 0, 50)
            
            # Passo 2: Windows Update (50-100%)
            progress_win.update_progress(
                50,
                "Passo 2 de 2: Windows Update",
                "Preparando Windows Update...",
                "Iniciando Windows Update"
            )
            
            self._update_windows_with_progress(progress_win, 50, 100)
            
            # Concluído
            progress_win.update_progress(
                100,
                "✅ Atualização Concluída!",
                "Todas as atualizações foram aplicadas com sucesso.",
                "Processo finalizado com sucesso!"
            )
            
            time.sleep(2)
            
            self.root.after(0, lambda: messagebox.showinfo(
                "Concluído",
                "Atualização completa finalizada com sucesso!\n\n"
                "Seu sistema está atualizado."
            ))
            
        except Exception as e:
            logger.error(f"Erro na atualização completa: {str(e)}", exc_info=True)
            if progress_win:
                progress_win.log(f"ERRO: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror(
                "Erro",
                f"Ocorreu um erro durante a atualização:\n\n{str(e)}"
            ))
        finally:
            if progress_win:
                self.root.after(0, progress_win.close)
            self.is_running = False
            self.root.after(0, self.enable_buttons)
            self.root.after(0, lambda: self.status_var.set("Pronto para iniciar"))
            
    def _run_apps_only(self):
        """Executa apenas atualização de aplicativos"""
        progress_win = None
        try:
            import time
            
            self.root.after(0, lambda: setattr(self, '_progress_win',
                ProgressWindow(self.root, "Atualizando Aplicativos")))
            
            time.sleep(0.5)
            progress_win = getattr(self, '_progress_win', None)
            
            if not progress_win:
                raise Exception("Falha ao criar janela de progresso")
            
            progress_win.update_progress(
                0,
                "Atualizando Aplicativos",
                "Preparando para atualizar aplicativos...",
                "Iniciando processo"
            )
            
            self._update_apps_with_progress(progress_win, 0, 100)
            
            progress_win.update_progress(
                100,
                "✅ Aplicativos Atualizados!",
                "Todos os aplicativos foram atualizados.",
                "Processo finalizado"
            )
            
            time.sleep(2)
            
            self.root.after(0, lambda: messagebox.showinfo(
                "Concluído",
                "Atualização de aplicativos finalizada!"
            ))
            
        except Exception as e:
            logger.error(f"Erro: {str(e)}", exc_info=True)
            if progress_win:
                progress_win.log(f"ERRO: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("Erro", str(e)))
        finally:
            if progress_win:
                self.root.after(0, progress_win.close)
            self.is_running = False
            self.root.after(0, self.enable_buttons)
            
    def _run_windows_only(self):
        """Executa apenas Windows Update"""
        progress_win = None
        try:
            import time
            
            self.root.after(0, lambda: setattr(self, '_progress_win',
                ProgressWindow(self.root, "Windows Update em Andamento")))
            
            time.sleep(0.5)
            progress_win = getattr(self, '_progress_win', None)
            
            if not progress_win:
                raise Exception("Falha ao criar janela de progresso")
            
            progress_win.update_progress(
                0,
                "Windows Update",
                "Preparando Windows Update...",
                "Iniciando processo"
            )
            
            self._update_windows_with_progress(progress_win, 0, 100)
            
            progress_win.update_progress(
                100,
                "✅ Windows Atualizado!",
                "Windows Update concluído.",
                "Processo finalizado"
            )
            
            time.sleep(2)
            
            self.root.after(0, lambda: messagebox.showinfo(
                "Concluído",
                "Windows Update finalizado!"
            ))
            
        except Exception as e:
            logger.error(f"Erro: {str(e)}", exc_info=True)
            if progress_win:
                progress_win.log(f"ERRO: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("Erro", str(e)))
        finally:
            if progress_win:
                self.root.after(0, progress_win.close)
            self.is_running = False
            self.root.after(0, self.enable_buttons)
            
    def _update_apps_with_progress(self, progress_win, start_percent, end_percent):
        """Atualiza aplicativos com progresso detalhado"""
        progress_win.log("Verificando winget...")
        progress_win.update_progress(start_percent, desc_text="Verificando winget...")
        
        # Verificar winget
        is_installed, msg = self.ps_manager.install_winget_if_needed()
        if not is_installed:
            progress_win.log(f"ERRO: {msg}")
            raise Exception(msg)
        
        progress_win.log("Winget disponível")
        
        # Listar aplicativos desatualizados
        progress_win.log("Listando aplicativos desatualizados...")
        progress_win.update_progress(
            start_percent + (end_percent - start_percent) * 0.1,
            desc_text="Identificando aplicativos..."
        )
        
        apps_to_update = self.ps_manager.list_upgradable_apps()
        
        if not apps_to_update or len(apps_to_update) == 0:
            progress_win.log("Nenhum aplicativo precisa ser atualizado!")
            progress_win.update_progress(end_percent, desc_text="Sem atualizações necessárias")
            return
        
        app_count = len(apps_to_update)
        progress_win.log(f"Encontrados {app_count} aplicativos para atualizar")
        
        # Atualizar cada aplicativo
        percent_per_app = (end_percent - start_percent) * 0.9 / app_count
        
        for i, app in enumerate(apps_to_update):
            current_percent = start_percent + (end_percent - start_percent) * 0.1 + (i * percent_per_app)
            
            progress_win.log(f"Atualizando: {app['name']}")
            progress_win.update_progress(
                current_percent,
                desc_text=f"Atualizando {app['name']} ({i+1}/{app_count})..."
            )
            
            success = self.ps_manager.update_app_silent(app['id'])
            
            if success:
                progress_win.log(f"✓ {app['name']} atualizado")
            else:
                progress_win.log(f"✗ Falha ao atualizar {app['name']}")
        
        progress_win.update_progress(end_percent, desc_text="Aplicativos atualizados!")
        progress_win.log("Todos os aplicativos foram processados")
        
    def _update_windows_with_progress(self, progress_win, start_percent, end_percent):
        """Executa Windows Update com progresso"""
        # Instalar módulo (0-20% do range)
        progress_win.log("Verificando módulo PSWindowsUpdate...")
        progress_win.update_progress(
            start_percent,
            desc_text="Verificando módulo PSWindowsUpdate..."
        )
        
        module_success, module_msg = self.ps_manager.install_pswindowsupdate_module()
        progress_win.log(module_msg)
        
        if not module_success:
            raise Exception(module_msg)
        
        progress_win.update_progress(
            start_percent + (end_percent - start_percent) * 0.2,
            desc_text="Módulo PSWindowsUpdate pronto"
        )
        
        # Executar Windows Update (20-100% do range)
        progress_win.log("Iniciando Windows Update...")
        progress_win.log("Isso pode levar bastante tempo...")
        progress_win.update_progress(
            start_percent + (end_percent - start_percent) * 0.3,
            desc_text="Baixando e instalando atualizações do Windows..."
        )
        
        # Executar com callback de progresso
        def progress_callback(percent, message):
            actual_percent = start_percent + (end_percent - start_percent) * (0.3 + 0.7 * (percent / 100))
            progress_win.update_progress(actual_percent, desc_text=message)
            progress_win.log(message)
        
        success, output = self.ps_manager.run_windows_update_with_progress(progress_callback)
        
        if success:
            progress_win.log("✓ Windows Update concluído")
        else:
            progress_win.log("⚠ Windows Update completado com avisos")
            progress_win.log(output[:500])  # Mostrar primeiras linhas do output
        
        progress_win.update_progress(end_percent, desc_text="Windows Update concluído!")


def main():
    """Função principal"""
    try:
        root = tk.Tk()
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Centralizar janela
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (900 // 2)
        y = (root.winfo_screenheight() // 2) - (700 // 2)
        root.geometry(f"900x700+{x}+{y}")
        
        # Criar aplicação
        app = MeninoDeTIHelperGUI(root)
        
        # Executar
        root.mainloop()
        
    except Exception as e:
        logger.error(f"Erro fatal: {str(e)}", exc_info=True)
        messagebox.showerror("Erro Fatal", f"Erro fatal:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
