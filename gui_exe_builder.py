"""
gui_exe_builder.py - Interface gráfica para construir executável do MENINO DA TI
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import os
from pathlib import Path
from exe_builder import ExeBuilder
from gui_utils import center_window


class ExeBuilderGUI:
    """Interface gráfica para construir executável"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("MENINO DA TI - Construtor de Executável")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        self.builder = None
        self.is_building = False
        self.build_thread = None
        
        self._setup_ui()
        center_window(self.root, 900, 700)
    
    def _setup_ui(self):
        """Configura a interface"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title = ttk.Label(
            title_frame,
            text="🔧 Construtor de Executável - MENINO DA TI",
            font=("Arial", 18, "bold")
        )
        title.pack()
        
        subtitle = ttk.Label(
            title_frame,
            text="Converta a aplicação Python em arquivo .exe independente",
            font=("Arial", 10),
            foreground="gray"
        )
        subtitle.pack()
        
        # Frame de opções
        options_frame = ttk.LabelFrame(main_frame, text="Opções de Build", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Ponto de entrada
        ttk.Label(options_frame, text="Ponto de Entrada:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_var = tk.StringVar(value="auto_launcher.py")
        entry_combo = ttk.Combobox(
            options_frame,
            textvariable=self.entry_var,
            values=["auto_launcher.py", "launcher.py", "main_gui.py"],
            state="readonly",
            width=40
        )
        entry_combo.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(options_frame, text="Arquivo principal a executar", font=("Arial", 8), foreground="gray").grid(row=0, column=2, sticky=tk.W, padx=5)
        
        # Arquivo único vs diretório
        ttk.Label(options_frame, text="Tipo de Build:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.build_type_var = tk.StringVar(value="onefile")
        onefile_radio = ttk.Radiobutton(
            options_frame,
            text="Um único arquivo (.exe)",
            variable=self.build_type_var,
            value="onefile"
        )
        onefile_radio.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(options_frame, text="Recomendado - Arquivo único", font=("Arial", 8), foreground="gray").grid(row=1, column=2, sticky=tk.W, padx=5)
        
        onedir_radio = ttk.Radiobutton(
            options_frame,
            text="Diretório com arquivos",
            variable=self.build_type_var,
            value="onedir"
        )
        onedir_radio.grid(row=2, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(options_frame, text="Mais rápido na inicialização", font=("Arial", 8), foreground="gray").grid(row=2, column=2, sticky=tk.W, padx=5)
        
        # Opções adicionais
        ttk.Label(options_frame, text="Opções:").grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.create_zip_var = tk.BooleanVar(value=True)
        zip_check = ttk.Checkbutton(
            options_frame,
            text="Criar pacote ZIP para distribuição",
            variable=self.create_zip_var
        )
        zip_check.grid(row=3, column=1, sticky=tk.W, padx=5)
        
        # Frame de progresso
        progress_frame = ttk.LabelFrame(main_frame, text="Progresso", padding="10")
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.progress_var = tk.IntVar(value=0)
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            length=400
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        progress_info_frame = ttk.Frame(progress_frame)
        progress_info_frame.pack(fill=tk.X)
        
        self.progress_label = ttk.Label(
            progress_info_frame,
            text="Aguardando início...",
            font=("Arial", 9)
        )
        self.progress_label.pack(side=tk.LEFT)
        
        self.progress_percent = ttk.Label(
            progress_info_frame,
            text="0%",
            font=("Arial", 9, "bold"),
            foreground="blue"
        )
        self.progress_percent.pack(side=tk.RIGHT)
        
        # Frame de log
        log_frame = ttk.LabelFrame(main_frame, text="Log de Construção", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=12,
            width=100,
            font=("Courier New", 9),
            bg="#f5f5f5"
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame de botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.build_btn = ttk.Button(
            button_frame,
            text="🔨 Iniciar Build",
            command=self._start_build,
            width=20
        )
        self.build_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.cancel_btn = ttk.Button(
            button_frame,
            text="⛔ Cancelar",
            command=self._cancel_build,
            state=tk.DISABLED,
            width=20
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.open_btn = ttk.Button(
            button_frame,
            text="📁 Abrir Pasta dist/",
            command=self._open_dist_folder,
            width=20
        )
        self.open_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Informações
        info_frame = ttk.LabelFrame(main_frame, text="ℹ️ Informações", padding="10")
        info_frame.pack(fill=tk.X)
        
        info_text = ttk.Label(
            info_frame,
            text="1. Clique em 'Iniciar Build' para converter a aplicação em .exe\n"
                 "2. O processo pode levar alguns minutos\n"
                 "3. O executável será salvo em 'dist/'\n"
                 "4. Use 'Abrir Pasta dist/' para acessar o arquivo gerado",
            justify=tk.LEFT,
            font=("Arial", 9)
        )
        info_text.pack()
    
    def _log(self, message: str):
        """Adiciona mensagem ao log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def _progress_callback(self, message: str, progress: int):
        """Callback de progresso"""
        self.progress_var.set(progress)
        self.progress_label.config(text=message)
        self.progress_percent.config(text=f"{progress}%")
        self._log(message)
    
    def _start_build(self):
        """Inicia o processo de build"""
        if self.is_building:
            messagebox.showwarning("Aviso", "Um build já está em execução!")
            return
        
        # Verificar arquivo de entrada
        entry_point = self.entry_var.get()
        if not Path(entry_point).exists():
            messagebox.showerror("Erro", f"Arquivo não encontrado: {entry_point}")
            return
        
        # Pedir confirmação
        response = messagebox.askyesno(
            "Confirmar",
            "Deseja iniciar o processo de build?\n\n"
            f"Ponto de entrada: {entry_point}\n"
            f"Tipo: {'Um arquivo' if self.build_type_var.get() == 'onefile' else 'Diretório'}\n"
            f"Criar ZIP: {'Sim' if self.create_zip_var.get() else 'Não'}\n\n"
            "Este processo pode levar alguns minutos."
        )
        
        if not response:
            return
        
        # Desabilitar botões
        self.is_building = True
        self.build_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        
        # Limpar log
        self.log_text.delete("1.0", tk.END)
        self._log("="*80)
        self._log("INICIANDO BUILD DO EXECUTÁVEL")
        self._log("="*80 + "\n")
        
        # Iniciar thread de build
        self.build_thread = threading.Thread(target=self._build_thread_func)
        self.build_thread.daemon = True
        self.build_thread.start()
    
    def _build_thread_func(self):
        """Função executada na thread de build"""
        try:
            entry_point = self.entry_var.get()
            one_file = self.build_type_var.get() == "onefile"
            create_zip = self.create_zip_var.get()
            
            # Criar builder
            self.builder = ExeBuilder(callback=self._progress_callback)
            
            # Executar build
            success, message = self.builder.build(create_zip=create_zip)
            
            # Finalizar
            self.root.after(self._finalize_build, success, message)
            
        except Exception as e:
            error_msg = f"Erro: {str(e)}"
            self.root.after(lambda msg=error_msg: self._finalize_build(False, msg))
    
    def _finalize_build(self, success: bool, message: str):
        """Finaliza o processo de build"""
        self.is_building = False
        self.build_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
        
        self._log("\n" + "="*80)
        
        if success:
            self._log("[SUCESSO] Build concluído com sucesso!")
            self._log("="*80)
            messagebox.showinfo("Sucesso", message)
            
            # Oferecer para abrir pasta
            if messagebox.askyesno("Abrir Pasta", "Deseja abrir a pasta 'dist/'?"):
                self._open_dist_folder()
        else:
            self._log("[FALHA] Build falhou!")
            self._log("="*80)
            messagebox.showerror("Erro", message)
    
    def _cancel_build(self):
        """Cancela o build em execução"""
        if messagebox.askyesno("Confirmar", "Deseja cancelar o build?"):
            # Nota: Cancelar processo já iniciado é complicado
            # Por enquanto, apenas mostramos a mensagem
            messagebox.showinfo("Aviso", "O build continuará em execução.\nO cancelamento só é possível encerrar após sua conclusão.")
    
    def _open_dist_folder(self):
        """Abre a pasta dist/ no explorador"""
        dist_path = Path.cwd() / "dist"
        
        if not dist_path.exists():
            messagebox.showwarning("Aviso", "Pasta 'dist/' não encontrada.\nExecute o build primeiro.")
            return
        
        try:
            import subprocess
            import sys
            
            if sys.platform == 'win32':
                os.startfile(dist_path)
            elif sys.platform == 'darwin':
                subprocess.run(['open', dist_path])
            else:
                subprocess.run(['xdg-open', dist_path])
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir pasta: {e}")


def main():
    """Função principal"""
    root = tk.Tk()
    app = ExeBuilderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
