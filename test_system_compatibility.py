"""
test_system_compatibility.py - Testes para verificação de compatibilidade

Executa testes da verificação de sistema, incluindo casos de sucesso e erro
"""
import sys
from system_check import SystemChecker


def test_current_system():
    """Testa o sistema atual"""
    print("\n" + "="*70)
    print("TESTE 1: Verificacao do Sistema Atual")
    print("="*70 + "\n")
    
    checker = SystemChecker()
    
    # Exibir informações
    checker.print_system_info()
    
    # Exibir compatibilidade
    is_compatible = checker.print_compatibility_status()
    
    if is_compatible:
        print("[TESTE PASSOU] Sistema compatível\n")
        return True
    else:
        print("[TESTE FALHOU] Sistema incompatível\n")
        return False


def test_windows_detection():
    """Testa detecção de versão do Windows"""
    print("\n" + "="*70)
    print("TESTE 2: Deteccao de Versao do Windows")
    print("="*70 + "\n")
    
    checker = SystemChecker()
    
    version = checker.get_windows_version()
    build = checker.get_windows_build()
    
    print(f"Versao detectada: {version}")
    print(f"Build detectado: {build}")
    
    if version:
        print(f"Release name: {checker.get_windows_release_name(version, build)}")
        print("[TESTE PASSOU] Versao detectada com sucesso\n")
        return True
    else:
        print("[TESTE FALHOU] Nao foi possivel detectar versao\n")
        return False


def test_architecture_detection():
    """Testa detecção de arquitetura"""
    print("\n" + "="*70)
    print("TESTE 3: Deteccao de Arquitetura")
    print("="*70 + "\n")
    
    checker = SystemChecker()
    
    arch = checker.architecture
    print(f"Arquitetura: {arch} bits")
    
    if arch in [32, 64]:
        print(f"[TESTE PASSOU] Arquitetura {arch}bits detectada\n")
        return True
    else:
        print(f"[TESTE FALHOU] Arquitetura desconhecida: {arch}bits\n")
        return False


def test_python_version():
    """Testa detecção de versão do Python"""
    print("\n" + "="*70)
    print("TESTE 4: Deteccao de Versao do Python")
    print("="*70 + "\n")
    
    checker = SystemChecker()
    
    python_ver = checker.python_version
    print(f"Python: {python_ver}")
    
    major, minor, micro = sys.version_info[:3]
    
    if major >= 3 and minor >= 8:
        print(f"[TESTE PASSOU] Python {major}.{minor} compativel\n")
        return True
    else:
        print(f"[TESTE FALHOU] Python {major}.{minor} é muito antigo\n")
        return False


def test_system_info_dict():
    """Testa obtenção de informações do sistema como dicionário"""
    print("\n" + "="*70)
    print("TESTE 5: Obter Informacoes do Sistema (Dict)")
    print("="*70 + "\n")
    
    checker = SystemChecker()
    info = checker.get_system_info()
    
    print("Informações obtidas:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    required_keys = [
        "sistema_operacional",
        "versao",
        "release",
        "arquitetura_bits",
        "python_versao"
    ]
    
    all_present = all(key in info for key in required_keys)
    
    if all_present:
        print("\n[TESTE PASSOU] Todas as informacoes obtidas\n")
        return True
    else:
        print("\n[TESTE FALHOU] Informacoes faltando\n")
        return False


def main():
    """Executa todos os testes"""
    print("\n")
    print("#"*70)
    print("# TESTES DE VERIFICACAO DE COMPATIBILIDADE DO SISTEMA")
    print("# MENINO DA TI")
    print("#"*70)
    
    results = {}
    
    results["test_1_current_system"] = test_current_system()
    results["test_2_windows_detection"] = test_windows_detection()
    results["test_3_architecture"] = test_architecture_detection()
    results["test_4_python_version"] = test_python_version()
    results["test_5_system_info_dict"] = test_system_info_dict()
    
    # Resumo
    print("\n" + "="*70)
    print("RESUMO DOS TESTES")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "[OK]" if result else "[FALHOU]"
        print(f"{status} {test_name}")
    
    print(f"\nTotal: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n[SUCESSO] Todos os testes passaram!\n")
        return 0
    else:
        print(f"\n[AVISO] {total - passed} teste(s) falharam\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
