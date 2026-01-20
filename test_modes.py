# -*- coding: utf-8 -*-
import io
import sys
# Force UTF-8 output
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

"""
test_modes.py - Teste dos modos console e gráfico
"""
import sys
import time
from console_splash import ConsoleSplash


def test_console_mode():
    """Testa o modo console"""
    print("\n" + "="*75)
    print("TESTE DO MODO CONSOLE")
    print("="*75)
    
    splash = ConsoleSplash()
    splash.show()
    
    print("[OK] Modo console iniciado com sucesso!")
    print("\nO modo console estaria pronto para processar comandos de diagnóstico.")
    time.sleep(2)


def main():
    """Função principal"""
    test_console_mode()


if __name__ == "__main__":
    main()
