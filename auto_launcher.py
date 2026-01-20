# -*- coding: utf-8 -*-
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


def show_console_menu():
    """Exibe menu interativo no console"""
    while True:
        try:
            print("\n" + "="*75)
            print("MENU PRINCIPAL - MENINO DA TI")
            print("="*75)
            print("\n[1] 🔧 Verificar Status do Sistema")
            print("[2] 📦 Atualizar Aplicativos (winget)")
            print("[3] 🪟 Atualizar Windows")
            print("[4] 🚀 Atualizar Tudo (Aplicativos + Windows)")
            print("[5] 🧹 Limpeza do Sistema")
            print("[6] ℹ️  Informações do Sistema")
            print("[0] ❌ Sair")
            print("\n" + "="*75)
            
            escolha = input("\nDigite sua escolha: ").strip()
            
            if escolha == "0":
                print("\n👋 Encerrando aplicação...")
                print("Obrigado por usar o Menino da TI!")
                break
            
            elif escolha == "1":
                verificar_status_sistema()
            
            elif escolha == "2":
                atualizar_aplicativos()
            
            elif escolha == "3":
                atualizar_windows()
            
            elif escolha == "4":
                atualizar_tudo()
            
            elif escolha == "5":
                limpeza_sistema()
            
            elif escolha == "6":
                mostrar_informacoes_sistema()
            
            else:
                print("\n❌ Opção inválida! Por favor, escolha uma opção de 0 a 6.")
                input("\nPressione Enter para continuar...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Encerrando aplicação...")
            print("Obrigado por usar o Menino da TI!")
            break
        except EOFError:
            print("\n\n👋 Entrada encerrada. Saindo...")
            break
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            print("Continuando operação normal...")
            input("\nPressione Enter para continuar...")


def verificar_status_sistema():
    """Verifica status do sistema"""
    print("\n" + "="*75)
    print("VERIFICANDO STATUS DO SISTEMA")
    print("="*75 + "\n")
    
    try:
        from powershell_manager import PowerShellManager
        ps_manager = PowerShellManager()
        
        # Verificar privilégios de administrador
        if ps_manager.check_admin_privileges():
            print("✓ Executando como Administrador")
        else:
            print("⚠️  NÃO está executando como Administrador")
            print("   Algumas operações podem falhar.\n")
        
        # Verificar winget
        print("Verificando winget...")
        is_installed, msg = ps_manager.install_winget_if_needed()
        if is_installed:
            print("✓ Winget disponível")
        else:
            print(f"⚠️  {msg}")
        
        print("\n✓ Verificação concluída!")
    
    except Exception as e:
        print(f"❌ Erro ao verificar sistema: {e}")
    
    input("\nPressione Enter para voltar ao menu...")


def atualizar_aplicativos():
    """Atualiza aplicativos com winget"""
    print("\n" + "="*75)
    print("ATUALIZANDO APLICATIVOS")
    print("="*75 + "\n")
    
    print("Escolha o método de atualização:\n")
    print("[1] 🚀 Atualização Rápida (atualiza tudo de uma vez)")
    print("[2] 📊 Atualização Detalhada (atualiza um por um com progresso)")
    print("[0] ❌ Cancelar\n")
    
    escolha = input("Digite sua escolha: ").strip()
    
    if escolha == "0":
        print("\n❌ Operação cancelada.")
        input("\nPressione Enter para voltar ao menu...")
        return
    
    confirmacao = input("\nDeseja prosseguir com a atualização de aplicativos? (S/N): ").strip().upper()
    
    if confirmacao != 'S':
        print("\n❌ Operação cancelada.")
        input("\nPressione Enter para voltar ao menu...")
        return
    
    try:
        from powershell_manager import PowerShellManager
        ps_manager = PowerShellManager()
        
        print("\nVerificando winget...")
        is_installed, msg = ps_manager.install_winget_if_needed()
        
        if not is_installed:
            print(f"❌ {msg}")
            input("\nPressione Enter para voltar ao menu...")
            return
        
        if escolha == "1":
            # Método rápido - atualiza tudo de uma vez
            print("\n🔄 Iniciando atualização rápida (bulk update)...")
            print("Isso pode levar vários minutos...\n")
            
            success, output = ps_manager.update_all_apps_with_winget()
            
            if output:
                print(output)
            
            if success:
                print("\n✓ Aplicativos atualizados com sucesso!")
            else:
                print("\n⚠️  Houve problemas na atualização de aplicativos.")
        
        else:
            # Método detalhado - atualiza um por um
            print("\n🔄 Iniciando atualização detalhada...")
            print("Listando aplicativos para atualizar...\n")
            
            def progress_callback(current, total, app_name, success):
                if success is None:
                    print(f"[{current}/{total}] Atualizando: {app_name}...")
                elif success:
                    print(f"[{current}/{total}] ✓ {app_name} - Atualizado com sucesso")
                else:
                    print(f"[{current}/{total}] ✗ {app_name} - Falha na atualização")
            
            successful, failed, failed_apps = ps_manager.update_apps_individually(progress_callback)
            
            print(f"\n{'='*75}")
            print("RESUMO DA ATUALIZAÇÃO")
            print('='*75)
            print(f"\n✓ Atualizados com sucesso: {successful}")
            print(f"✗ Falharam: {failed}")
            
            if failed_apps:
                print("\nAplicativos que falharam:")
                for app in failed_apps:
                    print(f"  - {app['name']} ({app['id']})")
    
    except Exception as e:
        print(f"\n❌ Erro ao atualizar aplicativos: {e}")
    
    input("\nPressione Enter para voltar ao menu...")


def atualizar_windows():
    """Atualiza o Windows"""
    print("\n" + "="*75)
    print("ATUALIZANDO WINDOWS")
    print("="*75 + "\n")
    
    confirmacao = input("Deseja prosseguir com o Windows Update? (S/N): ").strip().upper()
    
    if confirmacao != 'S':
        print("\n❌ Operação cancelada.")
        input("\nPressione Enter para voltar ao menu...")
        return
    
    try:
        from powershell_manager import PowerShellManager
        ps_manager = PowerShellManager()
        
        print("\nVerificando módulo PSWindowsUpdate...")
        module_success, module_msg = ps_manager.install_pswindowsupdate_module()
        print(module_msg)
        
        if not module_success:
            input("\nPressione Enter para voltar ao menu...")
            return
        
        print("\n🔄 Iniciando Windows Update...")
        print("Isso pode levar muito tempo...\n")
        
        success, output = ps_manager.run_windows_update()
        
        if output:
            print(output)
        
        if success or "No updates available" in output or "não há atualizações" in output.lower():
            print("\n✓ Windows Update concluído!")
        else:
            print("\n⚠️  Houve problemas no Windows Update.")
    
    except Exception as e:
        print(f"\n❌ Erro ao executar Windows Update: {e}")
    
    input("\nPressione Enter para voltar ao menu...")


def atualizar_tudo():
    """Atualiza aplicativos e Windows"""
    print("\n" + "="*75)
    print("ATUALIZAÇÃO COMPLETA (APLICATIVOS + WINDOWS)")
    print("="*75 + "\n")
    
    confirmacao = input("Deseja prosseguir com a atualização completa? (S/N): ").strip().upper()
    
    if confirmacao != 'S':
        print("\n❌ Operação cancelada.")
        input("\nPressione Enter para voltar ao menu...")
        return
    
    print("\n" + "="*75)
    print("ETAPA 1/2: ATUALIZANDO APLICATIVOS")
    print("="*75 + "\n")
    
    try:
        from powershell_manager import PowerShellManager
        ps_manager = PowerShellManager()
        
        # Etapa 1: Aplicativos
        is_installed, msg = ps_manager.install_winget_if_needed()
        
        if is_installed:
            print("🔄 Atualizando aplicativos...")
            success, output = ps_manager.update_all_apps_with_winget()
            
            if output:
                print(output)
            
            if success:
                print("\n✓ Aplicativos atualizados!")
            else:
                print("\n⚠️  Problemas ao atualizar aplicativos.")
        else:
            print(f"⚠️  {msg}")
        
        # Etapa 2: Windows
        print("\n" + "="*75)
        print("ETAPA 2/2: ATUALIZANDO WINDOWS")
        print("="*75 + "\n")
        
        module_success, module_msg = ps_manager.install_pswindowsupdate_module()
        print(module_msg)
        
        if module_success:
            print("\n🔄 Executando Windows Update...")
            success, output = ps_manager.run_windows_update()
            
            if output:
                print(output)
            
            if success or "No updates available" in output:
                print("\n✓ Windows Update concluído!")
            else:
                print("\n⚠️  Problemas no Windows Update.")
        
        print("\n" + "="*75)
        print("ATUALIZAÇÃO COMPLETA FINALIZADA")
        print("="*75)
    
    except Exception as e:
        print(f"\n❌ Erro durante atualização: {e}")
    
    input("\nPressione Enter para voltar ao menu...")


def limpeza_sistema():
    """Executa limpeza do sistema"""
    print("\n" + "="*75)
    print("LIMPEZA DO SISTEMA")
    print("="*75 + "\n")
    
    print("🧹 Limpeza de sistema incluirá:")
    print("  - Arquivos temporários")
    print("  - Cache do sistema")
    print("  - Lixeira")
    print("  - Arquivos de log antigos\n")
    
    confirmacao = input("Deseja prosseguir com a limpeza? (S/N): ").strip().upper()
    
    if confirmacao != 'S':
        print("\n❌ Operação cancelada.")
        input("\nPressione Enter para voltar ao menu...")
        return
    
    try:
        from cleanup_manager import CleanupManager
        cleanup = CleanupManager()
        
        print("\n🔄 Iniciando limpeza do sistema...\n")
        
        # Executar limpeza
        results = cleanup.run_all_cleanup()
        
        print("\n✓ Limpeza concluída!")
        print(f"\nEspaço liberado: {results.get('total_freed', 'N/A')}")
    
    except ImportError:
        print("⚠️  Módulo de limpeza não disponível.")
    except Exception as e:
        print(f"\n❌ Erro durante limpeza: {e}")
    
    input("\nPressione Enter para voltar ao menu...")


def mostrar_informacoes_sistema():
    """Mostra informações detalhadas do sistema"""
    print("\n" + "="*75)
    print("INFORMAÇÕES DO SISTEMA")
    print("="*75 + "\n")
    
    try:
        system_checker = SystemChecker()
        system_checker.print_system_info()
        system_checker.print_compatibility_status()
    
    except Exception as e:
        print(f"❌ Erro ao obter informações: {e}")
    
    input("\nPressione Enter para voltar ao menu...")


def launch_console_mode():
    """Inicia a aplicação em modo console"""
    print("\n" + "="*75)
    print("INICIANDO MENINO DA TI EM MODO CONSOLE")
    print("="*75 + "\n")
    
    splash = ConsoleSplash()
    splash.show()
    
    print("\n✓ Aplicação iniciada em modo console!")
    print("\n")
    
    # Inicia o menu interativo
    show_console_menu()


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
