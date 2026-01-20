# -*- coding: utf-8 -*-
"""
TEST AUTOMATION FRAMEWORK
Sistema de automacao de testes para Menino de TI Helper
"""

import sys
import os

# Force UTF-8
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from powershell_manager import PowerShellManager
from cleanup_manager import CleanupManager
import time


def test_powershell_manager():
    """Testes do PowerShell Manager"""
    print("\n[TEST] PowerShell Manager")
    print("=" * 60)
    
    ps = PowerShellManager()
    passed = 0
    total = 3
    
    # Teste 1: Comando basico
    print("[TEST-001] Executando comando basico...", end="")
    try:
        success, stdout, stderr = ps.execute_command("Write-Output 'Test'")
        if success and "Test" in stdout:
            print(" [OK]")
            passed += 1
        else:
            print(" [FAIL]")
    except Exception as e:
        print(f" [ERROR]: {str(e)}")
    
    # Teste 2: Winget
    print("[TEST-002] Verificando Winget...", end="")
    try:
        success, stdout, stderr = ps.execute_command("winget --version")
        if success:
            print(" [OK]")
            passed += 1
        else:
            print(" [FAIL]")
    except Exception as e:
        print(f" [ERROR]: {str(e)}")
    
    # Teste 3: Admin check
    print("[TEST-003] Verificando privilégios Admin...", end="")
    try:
        cmd = "$([Security.Principal.WindowsIdentity]::GetCurrent() | ForEach-Object {[Security.Principal.WindowsPrincipal]$_ | ForEach-Object {$_.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)}})"
        success, stdout, stderr = ps.execute_command(cmd)
        if success:
            print(" [OK]")
            passed += 1
        else:
            print(" [FAIL]")
    except Exception as e:
        print(f" [ERROR]: {str(e)}")
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    return passed == total


def test_cleanup_manager():
    """Testes do Cleanup Manager"""
    print("\n[TEST] Cleanup Manager")
    print("=" * 60)
    
    cleanup = CleanupManager()
    passed = 0
    total = 2
    
    # Teste 1: Cache folders
    print("[TEST-004] Obtendo pastas de cache...", end="")
    try:
        folders = cleanup.get_cache_folders()
        if isinstance(folders, list):
            print(f" [OK] ({len(folders)} pastas)")
            passed += 1
        else:
            print(" [FAIL]")
    except Exception as e:
        print(f" [ERROR]: {str(e)}")
    
    # Teste 2: Temp folders
    print("[TEST-005] Obtendo pastas temporarias...", end="")
    try:
        folders = cleanup.get_temp_folders()
        if isinstance(folders, list):
            print(f" [OK] ({len(folders)} pastas)")
            passed += 1
        else:
            print(" [FAIL]")
    except Exception as e:
        print(f" [ERROR]: {str(e)}")
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    return passed == total


def test_module_imports():
    """Testes de importacao de modulos"""
    print("\n[TEST] Module Imports")
    print("=" * 60)
    
    modules = [
        'main_gui',
        'gui_main_window',
        'powershell_manager',
        'cleanup_manager',
        'gui_utils',
        'gui_constants'
    ]
    
    passed = 0
    for module in modules:
        print(f"[TEST-{206+modules.index(module)}] Importando {module}...", end="")
        try:
            __import__(module)
            print(" [OK]")
            passed += 1
        except Exception as e:
            print(f" [FAIL]: {str(e)}")
    
    print(f"\nResultado: {passed}/{len(modules)} testes passaram")
    return passed == len(modules)


def main():
    """Executor principal"""
    print("\n" + "="*60)
    print("AUTOMATION FRAMEWORK TEST SUITE".center(60))
    print("="*60)
    
    results = []
    
    # Executar testes
    results.append(("PowerShell Manager", test_powershell_manager()))
    results.append(("Cleanup Manager", test_cleanup_manager()))
    results.append(("Module Imports", test_module_imports()))
    
    # Resumo final
    print("\n" + "="*60)
    print("RESUMO FINAL".center(60))
    print("="*60)
    
    total = len(results)
    passed = sum(1 for _, r in results if r)
    
    for name, result in results:
        status = "[OK]" if result else "[FAIL]"
        print(f"{name:40s} {status}")
    
    print(f"\nTotal: {passed}/{total} suites passaram")
    print("="*60 + "\n")
    
    return all(r for _, r in results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
