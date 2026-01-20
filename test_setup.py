# -*- coding: utf-8 -*-
import io
import sys
# Force UTF-8 output
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

"""
Test Script - Menino de TI Helper
This script tests if the PowerShell integration is working correctly
Run this before using the main application to verify everything is set up correctly
"""
import sys
from powershell_manager import PowerShellManager


def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def test_powershell_basic():
    """Test basic PowerShell execution"""
    print_header("Teste 1: Execução Básica do PowerShell")
    
    ps = PowerShellManager()
    success, stdout, stderr = ps.execute_command("Write-Output 'Hello from PowerShell'")
    
    if success:
        print("✓ PowerShell está funcionando!")
        print(f"Saída: {stdout.strip()}")
        return True
    else:
        print("✗ Erro ao executar PowerShell")
        print(f"Erro: {stderr}")
        return False


def test_admin_check():
    """Test administrator privilege check"""
    print_header("Teste 2: Verificação de Privilégios de Administrador")
    
    ps = PowerShellManager()
    is_admin = ps.check_admin_privileges()
    
    if is_admin:
        print("✓ Executando como Administrador")
    else:
        print("⚠ NÃO está executando como Administrador")
        print("  Recomendação: Execute este script como administrador")
        print("  para obter todos os recursos")
    
    return True


def test_winget():
    """Test if winget is available"""
    print_header("Teste 3: Verificação do Winget")
    
    ps = PowerShellManager()
    is_installed, message = ps.install_winget_if_needed()
    
    if is_installed:
        print("✓ Winget está instalado e disponível")
        
        # Try to list one package as a test
        print("\nTestando winget com um comando simples...")
        success, stdout, stderr = ps.execute_command("winget --version")
        if success:
            print(f"✓ Versão do winget: {stdout.strip()}")
        return True
    else:
        print(f"✗ {message}")
        print("\nSolução:")
        print("1. Abra a Microsoft Store")
        print("2. Procure por 'App Installer'")
        print("3. Instale ou atualize o aplicativo")
        return False


def test_powershell_version():
    """Test PowerShell version"""
    print_header("Teste 4: Versão do PowerShell")
    
    ps = PowerShellManager()
    success, stdout, stderr = ps.execute_command("$PSVersionTable.PSVersion")
    
    if success:
        print("✓ PowerShell detectado:")
        print(stdout.strip())
        return True
    else:
        print("✗ Não foi possível detectar versão do PowerShell")
        print(f"Erro: {stderr}")
        return False


def test_python_dependencies():
    """Test if Python dependencies are installed"""
    print_header("Teste 5: Dependências Python")
    
    try:
        import tkinter
        print("[OK] tkinter está instalado")
        tkinter_ok = True
    except ImportError:
        print("✗ tkinter NÃO está instalado")
        print("  Solução: Reinstale o Python com suporte a tkinter")
        tkinter_ok = False
    
    try:
        from PIL import Image
        print("[OK] Pillow está instalado")
        pillow_ok = True
    except ImportError:
        print("⚠ Pillow NÃO está instalado (opcional)")
        print("  Para instalar: pip install Pillow")
        pillow_ok = True  # Not critical
    
    return tkinter_ok and pillow_ok


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("  MENINO DE TI HELPER - TESTE DE SISTEMA")
    print("="*70)
    
    print("\nEste script verifica se tudo está configurado corretamente")
    print("para executar o Menino de TI Helper.\n")
    
    # Run all tests
    results = []
    
    results.append(("PowerShell Básico", test_powershell_basic()))
    results.append(("Privilégios Admin", test_admin_check()))
    results.append(("Winget", test_winget()))
    results.append(("Versão PowerShell", test_powershell_version()))
    results.append(("Dependências Python", test_python_dependencies()))
    
    # Summary
    print_header("RESUMO DOS TESTES")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSOU" if result else "✗ FALHOU"
        print(f"{status:12} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 Todos os testes passaram!")
        print("Você está pronto para usar o Menino de TI Helper!")
        print("\nPara iniciar o aplicativo, execute:")
        print("  python main.py")
    else:
        print("\n⚠ Alguns testes falharam.")
        print("Por favor, resolva os problemas indicados acima antes de usar o aplicativo.")
        print("\nDica: Execute este script como Administrador para melhores resultados.")
    
    print("\n" + "="*60)
    
    return passed == total


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Erro fatal durante os testes: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
