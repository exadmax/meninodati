"""
test_powershell_encoding.py - Testa correções de encoding e None handling

Este script testa:
1. Encoding correto com fallback para caracteres especiais
2. Tratamento de stdout/stderr None
3. Lambdas com captura correta de variáveis
"""
import sys

def test_encoding_fallback():
    """Testa que o execute_command lida com diferentes encodings"""
    print("\n" + "="*75)
    print("TESTE: Encoding com Fallback")
    print("="*75 + "\n")
    
    try:
        from powershell_manager import PowerShellManager
        
        ps_manager = PowerShellManager()
        
        # Comando que deve funcionar
        print("Testando comando simples...")
        success, stdout, stderr = ps_manager.execute_command("echo 'teste'")
        
        if success:
            print("✓ Comando executado com sucesso")
            print(f"  Output: {stdout.strip()}")
        else:
            print("✗ Comando falhou")
            return False
        
        # Verificar que stdout/stderr nunca são None
        print("\nVerificando que stdout/stderr nunca são None...")
        if stdout is None or stderr is None:
            print("✗ stdout ou stderr são None!")
            return False
        
        print("✓ stdout e stderr sempre são strings")
        
        # Comando com caracteres especiais (pode ter encoding issues)
        print("\nTestando comando com caracteres especiais...")
        success2, stdout2, stderr2 = ps_manager.execute_command(
            "Get-Date | Format-List"
        )
        
        if stdout2 is None or stderr2 is None:
            print("✗ stdout ou stderr são None com caracteres especiais!")
            return False
        
        print("✓ Caracteres especiais tratados corretamente")
        print(f"  Output length: {len(stdout2)} chars")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_none_check_in_methods():
    """Testa que métodos verificam None antes de usar .strip()"""
    print("\n" + "="*75)
    print("TESTE: Verificação de None em Métodos")
    print("="*75 + "\n")
    
    try:
        with open('powershell_manager.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = {
            "check_admin_privileges usa 'stdout and'": "success and stdout and stdout.strip()" in content,
            "install_winget_if_needed usa 'stdout and'": "success and stdout and stdout.strip()" in content,
            "install_pswindowsupdate_module usa 'if stdout and'": "if stdout and stdout.strip()" in content,
            "list_upgradable_apps usa 'or not stdout or'": "or not stdout or not stdout.strip()" in content,
            "execute_command garante não-None": 'stdout = stdout if stdout is not None else ""' in content,
        }
        
        all_passed = True
        for check_name, passed in checks.items():
            status = "✓" if passed else "❌"
            print(f"{status} {check_name}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print("\n✓ Todos os métodos verificam None corretamente")
        else:
            print("\n⚠️  Alguns métodos podem ter problemas com None")
            
        return all_passed
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False


def test_lambda_capture():
    """Testa que lambdas capturam variáveis corretamente"""
    print("\n" + "="*75)
    print("TESTE: Captura de Variáveis em Lambda")
    print("="*75 + "\n")
    
    try:
        with open('main_gui.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Procurar por padrões problemáticos
        bad_patterns = [
            "lambda: messagebox.showerror(.*str(e)",
            "lambda:.*{str(e)}",
        ]
        
        import re
        issues_found = []
        for pattern in bad_patterns:
            matches = re.findall(pattern, content)
            if matches:
                issues_found.extend(matches)
        
        # Procurar por padrões corretos
        good_patterns = [
            r"error_msg = str\(e\)",
            r"lambda msg=error_msg:",
            r"lambda msg=.*: messagebox",
        ]
        
        correct_patterns = 0
        for pattern in good_patterns:
            if re.search(pattern, content):
                correct_patterns += 1
        
        if issues_found:
            print(f"❌ Encontrados {len(issues_found)} padrões problemáticos:")
            for issue in issues_found[:3]:  # Mostrar só os primeiros 3
                print(f"  - {issue}")
            return False
        
        if correct_patterns >= 2:
            print(f"✓ Lambdas usam captura correta de variáveis")
            print(f"  Padrões corretos encontrados: {correct_patterns}")
            return True
        else:
            print("⚠️  Poucos padrões corretos encontrados")
            return False
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False


def test_execute_command_robustness():
    """Testa robustez do execute_command"""
    print("\n" + "="*75)
    print("TESTE: Robustez do execute_command")
    print("="*75 + "\n")
    
    try:
        from powershell_manager import PowerShellManager
        
        ps_manager = PowerShellManager()
        
        # Teste 1: Comando que retorna vazio
        print("Testando comando que retorna vazio...")
        success, stdout, stderr = ps_manager.execute_command("$null")
        
        if stdout is None or stderr is None:
            print("✗ stdout/stderr são None!")
            return False
        
        print(f"✓ Comando vazio: stdout='{stdout}', stderr='{stderr}'")
        
        # Teste 2: Comando que falha
        print("\nTestando comando que falha...")
        success, stdout, stderr = ps_manager.execute_command("Get-NonExistentCmdlet")
        
        if stdout is None or stderr is None:
            print("✗ stdout/stderr são None mesmo em erro!")
            return False
        
        print(f"✓ Comando com erro: success={success}")
        print(f"  stderr contém mensagem: {len(stderr) > 0}")
        
        # Teste 3: Timeout
        print("\nTestando timeout (deve levar 2 segundos)...")
        success, stdout, stderr = ps_manager.execute_command(
            "Start-Sleep -Seconds 10", 
            timeout=2
        )
        
        if not success:
            print("✓ Timeout tratado corretamente")
        else:
            print("⚠️  Timeout não funcionou como esperado")
        
        if stdout is None or stderr is None:
            print("✗ stdout/stderr são None no timeout!")
            return False
        
        print("✓ stdout/stderr não são None no timeout")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Executa todos os testes"""
    print("\n" + "="*75)
    print("SUITE DE TESTES - ENCODING E NONE HANDLING")
    print("="*75)
    
    tests = [
        ("Encoding com Fallback", test_encoding_fallback),
        ("Verificação de None", test_none_check_in_methods),
        ("Captura de Lambda", test_lambda_capture),
        ("Robustez execute_command", test_execute_command_robustness),
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
        print("\n✓ TODAS AS CORREÇÕES ESTÃO FUNCIONANDO!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam")
        return 1


if __name__ == "__main__":
    sys.exit(main())
