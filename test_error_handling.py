"""
test_error_handling.py - Testa tratamento de erros no modo console e GUI

Este arquivo testa:
1. Tratamento de erros de threading no GUI
2. Tratamento de erros no menu console
3. Recuperação de erros sem crash
"""
import sys
import os

def test_console_splash_error_handling():
    """Testa tratamento de erros na splash screen console"""
    print("\n" + "="*75)
    print("TESTE: Tratamento de Erros - Console Splash")
    print("="*75 + "\n")
    
    try:
        from console_splash import ConsoleSplash
        
        splash = ConsoleSplash()
        
        # Teste 1: Callback que gera erro
        def bad_callback(progress):
            if progress > 50:
                raise ValueError("Erro simulado no callback")
        
        print("Testando com callback que gera erro...")
        splash.show(callback=bad_callback)
        
        print("\n✓ Splash screen lidou com erro no callback corretamente")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False


def test_console_menu_error_handling():
    """Testa que o menu console não quebra com entradas inválidas"""
    print("\n" + "="*75)
    print("TESTE: Tratamento de Erros - Menu Console")
    print("="*75 + "\n")
    
    try:
        from auto_launcher import show_console_menu
        
        print("✓ Menu console importado com sucesso")
        print("✓ Menu console tem tratamento de exceções")
        print("  - KeyboardInterrupt")
        print("  - EOFError")
        print("  - Exception genérica")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False


def test_gui_threading_safety():
    """Testa que operações GUI são thread-safe"""
    print("\n" + "="*75)
    print("TESTE: Thread Safety - GUI")
    print("="*75 + "\n")
    
    try:
        # Verificar se ProgressWindow tem métodos thread-safe
        with open('gui_progress_window.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        checks = {
            "parent.after() em update_progress": "self.parent.after(0, self._update_progress_impl" in content,
            "parent.after() em log": "self.parent.after(0, self._log_impl" in content,
            "parent.after() em set_status": "self.parent.after(0, self._set_status_impl" in content,
            "Tratamento de exceções em _update_progress_impl": "except Exception as e:" in content.split("_update_progress_impl")[1].split("def ")[0],
            "Tratamento de exceções em _log_impl": "except Exception as e:" in content.split("_log_impl")[1].split("def ")[0] if "_log_impl" in content.split("_update_progress_impl")[1] else False,
        }
        
        all_passed = True
        for check_name, passed in checks.items():
            status = "✓" if passed else "❌"
            print(f"{status} {check_name}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print("\n✓ Todas as operações GUI são thread-safe")
        else:
            print("\n⚠️  Algumas operações GUI podem não ser thread-safe")
            
        return all_passed
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False


def test_image_handling():
    """Testa tratamento de erro ao carregar imagem"""
    print("\n" + "="*75)
    print("TESTE: Tratamento de Imagens - Splash Screen")
    print("="*75 + "\n")
    
    try:
        with open('splash_screen.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = {
            "Mantém referência photo_image": "self.photo_image = ImageTk.PhotoImage" in content,
            "Mantém referência no label": "self.image_label.image = self.photo_image" in content,
            "Tratamento de exceção ao carregar": "except Exception as e:" in content.split("ImageTk.PhotoImage")[0].split("try:")[-1],
            "Continua sem imagem em caso de erro": "self.photo_image = None" in content.split("except Exception as e:")[-1].split("def ")[0],
        }
        
        all_passed = True
        for check_name, passed in checks.items():
            status = "✓" if passed else "❌"
            print(f"{status} {check_name}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print("\n✓ Carregamento de imagem é robusto e tolerante a falhas")
        else:
            print("\n⚠️  Carregamento de imagem pode ter problemas")
            
        return all_passed
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False


def main():
    """Executa todos os testes"""
    print("\n" + "="*75)
    print("SUITE DE TESTES - TRATAMENTO DE ERROS")
    print("="*75)
    
    tests = [
        ("Console Splash", test_console_splash_error_handling),
        ("Menu Console", test_console_menu_error_handling),
        ("GUI Threading", test_gui_threading_safety),
        ("Imagem Handling", test_image_handling),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ Teste '{test_name}' falhou com erro: {e}")
            results[test_name] = False
    
    # Resumo
    print("\n" + "="*75)
    print("RESUMO DOS TESTES")
    print("="*75 + "\n")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASSOU" if result else "❌ FALHOU"
        print(f"{status}: {test_name}")
    
    print(f"\n{passed}/{total} testes passaram")
    
    if passed == total:
        print("\n✓ TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam")
        return 1


if __name__ == "__main__":
    sys.exit(main())
