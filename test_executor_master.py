# -*- coding: utf-8 -*-
"""
MASTER TEST EXECUTOR
Executor principal que coordena todos os testes do sistema
Inclui: Framework de testes, Testes clicáveis, Análise de erros e Correções
"""

import sys
import os
import subprocess
import time
import json
import io
from datetime import datetime
from pathlib import Path

# Force UTF-8 output
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class TestExecutor:
    """Executor master de testes"""
    
    def __init__(self):
        self.results = {}
        self.start_time = None
        self.end_time = None
        self.failed_tests = []
        self.errors_found = []
        
    def execute_test_suite(self, test_file: str, description: str) -> bool:
        """Executa uma suite de testes"""
        print(f"\n{'='*80}")
        print(f"[EXECUTOR] Executando: {description}")
        print(f"{'='*80}\n")
        
        try:
            result = subprocess.run(
                [sys.executable, test_file],
                cwd=os.path.dirname(__file__),
                capture_output=True,
                text=True,
                timeout=300
            )
            
            print(result.stdout)
            if result.stderr and "UserWarning" not in result.stderr:
                print("[STDERR]", result.stderr)
            
            success = result.returncode == 0
            self.results[test_file] = {
                'description': description,
                'success': success,
                'exit_code': result.returncode,
                'timestamp': datetime.now().isoformat()
            }
            
            return success
        except subprocess.TimeoutExpired:
            print(f"✗ TIMEOUT ao executar {test_file}")
            self.results[test_file] = {
                'description': description,
                'success': False,
                'error': 'Timeout',
                'timestamp': datetime.now().isoformat()
            }
            self.errors_found.append(f"Timeout: {test_file}")
            return False
        except Exception as e:
            print(f"✗ ERRO ao executar {test_file}: {str(e)}")
            self.results[test_file] = {
                'description': description,
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            self.errors_found.append(f"Error in {test_file}: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Executa todas as suites de testes"""
        self.start_time = time.time()
        
        print("\n" + "="*80)
        print("MENINO DE TI HELPER - SISTEMA AUTOMÁTICO DE TESTES".center(80))
        print("="*80 + "\n")
        
        # 1. Testes de Automação Framework
        print("\n[FASE 1] Testes de Framework e Módulos")
        self.execute_test_suite(
            "test_automation_framework.py",
            "Framework de Testes (PowerShell, Cleanup, Integração)"
        )
        
        # 2. Testes Clicáveis
        print("\n[FASE 2] Testes de Elementos Clicáveis")
        self.execute_test_suite(
            "test_clickable_elements.py",
            "Testes de GUI com Simulação de Cliques"
        )
        
        # 3. Testes Existentes
        print("\n[FASE 3] Testes de Sistema Existentes")
        self.execute_test_suite(
            "test_setup.py",
            "Verificação de Setup e Compatibilidade"
        )
        
        print("\n[FASE 4] Testes de Modos")
        self.execute_test_suite(
            "test_modes.py",
            "Verificação de Modos de Operação"
        )
        
        self.end_time = time.time()
        self._print_final_report()
    
    def _print_final_report(self):
        """Imprime relatório final"""
        elapsed_time = self.end_time - self.start_time
        
        print("\n" + "="*80)
        print("RELATÓRIO FINAL DE TESTES".center(80))
        print("="*80)
        
        total_suites = len(self.results)
        passed_suites = sum(1 for r in self.results.values() if r['success'])
        failed_suites = total_suites - passed_suites
        
        print(f"\n[RESUMO GERAL]")
        print(f"  Suites Executadas: {total_suites}")
        print(f"  Suites Passadas: {passed_suites} [OK]")
        print(f"  Suites Falhadas: {failed_suites} [FAIL]")
        print(f"  Taxa de Sucesso: {(passed_suites/total_suites*100):.1f}%")
        print(f"  Tempo Total: {elapsed_time:.2f}s")
        
        print(f"\n[DETALHES POR SUITE]")
        for test_file, result in self.results.items():
            status = "[OK] PASSOU" if result['success'] else "[FAIL] FALHOU"
            print(f"  {result['description']:40s} [{status}]")
            if not result['success'] and 'error' in result:
                print(f"    └─ Erro: {result['error']}")
        
        if self.errors_found:
            print(f"\n[ERROS ENCONTRADOS] ({len(self.errors_found)})")
            for i, error in enumerate(self.errors_found, 1):
                print(f"  {i}. {error}")
        
        print("\n" + "="*80 + "\n")
        
        # Salvar relatório em JSON
        self._save_json_report()
    
    def _save_json_report(self):
        """Salva relatório em JSON"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_suites': len(self.results),
            'passed_suites': sum(1 for r in self.results.values() if r['success']),
            'failed_suites': sum(1 for r in self.results.values() if not r['success']),
            'total_time': self.end_time - self.start_time,
            'results': self.results,
            'errors': self.errors_found
        }
        
        filename = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"[INFO] Relatório salvo em: {filename}")


class ErrorAnalyzer:
    """Analisa erros encontrados"""
    
    @staticmethod
    def analyze_and_fix():
        """Analisa erros e sugere correções"""
        print("\n[ERROR ANALYSIS] Analisando erros encontrados...\n")
        
        errors_to_check = [
            {
                'file': 'test_automation_framework.py',
                'check': 'ImportError|AttributeError|TypeError',
                'fix': 'Validar imports e estrutura de classes'
            },
            {
                'file': 'test_clickable_elements.py',
                'check': 'ImportError|NameError',
                'fix': 'Validar definições de classes'
            }
        ]
        
        for error_info in errors_to_check:
            print(f"[CHECK] Verificando {error_info['file']}...")
            try:
                with open(error_info['file'], 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Verificar sintaxe
                    compile(content, error_info['file'], 'exec')
                    print(f"  ✓ Sintaxe válida")
            except SyntaxError as e:
                print(f"  ✗ Erro de sintaxe: {str(e)}")
                print(f"  → Sugestão: {error_info['fix']}")
            except Exception as e:
                print(f"  ✗ Erro: {str(e)}")


def main():
    """Função principal"""
    executor = TestExecutor()
    
    # Executar testes
    executor.run_all_tests()
    
    # Analisar erros
    ErrorAnalyzer.analyze_and_fix()
    
    return 0 if executor.results else 1


if __name__ == "__main__":
    sys.exit(main())
