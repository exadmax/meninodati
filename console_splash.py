"""
console_splash.py - Tela de inicialização em modo console com arte ASCII
"""
import sys
import time
from typing import Callable

class ConsoleSplash:
    """Exibe tela ASCII de inicialização no console"""
    
    ASCII_ART = r"""
+-----------------------------------------------------------------------+
|  MENINO DA TI - DIAGNOSTICO v1.0                                [X]   |
+-----------------------------------------------------------------------+
|                                                                       |
|   __  __            _               ____         _____ ___            |
|  |  \/  | ___ _ __ (_)_ __   ___   |  _ \ __ _  |_   _|_ _|           |
|  | |\/| |/ _ \ '_ \| | '_ \ / _ \  | | | / _` |   | |  | |            |
|  | |  | |  __/ | | | | | | | (_) | | |_| | (_| |   | |  | |            |
|  |_|  |_|\___|_| |_|_|_| |_|\___/  |____/ \__,_|   |_| |___|          |
|                                                                       |
|                                                                       |
|  STATUS DO SISTEMA:                                                   |
"""
    
    STATUS_ITEMS = [
        "Verificando cabos de rede...",
        "Perguntando se reiniciou o modem...",
        "Carregando solucoes magicas..."
    ]
    
    FOOTER = """
|                                                                       |
|-----------------------------------------------------------------------|
|  Criado por Diogo Goes Zanetti                                        |
+-----------------------------------------------------------------------+
"""
    
    def __init__(self):
        self.progress = 0
        self.max_progress = 100
        
    def clear_screen(self):
        """Limpa a tela do console"""
        import os
        os.system('cls' if sys.platform == 'win32' else 'clear')
    
    def get_progress_bar(self, filled: int, total: int = 50) -> str:
        """Gera uma barra de progresso ASCII"""
        filled = max(0, min(filled, total))
        empty = total - filled
        return '[' + ('|' * filled) + ('.' * empty) + ']'
    
    def show(self, callback: Callable[[int], None] = None):
        """
        Exibe a tela de inicialização com progresso animado
        
        Args:
            callback: Função callback para relatar progresso (0-100)
        """
        self.clear_screen()
        
        # Exibe arte ASCII
        print(self.ASCII_ART)
        
        # Exibe itens de status com animação
        for i, status in enumerate(self.STATUS_ITEMS):
            if i < 2:
                print(f"|  [OK] {status:<60}|")
            else:
                print(f"|  [..] {status:<60}|")
            time.sleep(0.8)
            
            # Simula progresso
            progress_percent = int((i / len(self.STATUS_ITEMS)) * 65)
            self.progress = progress_percent
            
            if callback:
                callback(progress_percent)
        
        # Simula carregamento final
        print("|                                                                       |")
        print("|  PROGRESSO:                                                           |")
        
        # Animação da barra de progresso
        for step in range(26):  # De 65% a 100%
            progress_percent = 65 + step
            filled = int((progress_percent / 100) * 50)
            bar = self.get_progress_bar(filled)
            progress_line = f"|  {bar} {progress_percent}%{'':>9}|"
            print(progress_line, end='\r')
            
            self.progress = progress_percent
            if callback:
                callback(progress_percent)
            
            time.sleep(0.05)
        
        print()  # Nova linha após barra
        print(self.FOOTER)
        
        # Mensagem final
        time.sleep(1)
        print("\n  Inicializando aplicação...\n")
        time.sleep(0.5)
    
    def show_simple(self):
        """Exibe apenas a tela sem animação"""
        self.clear_screen()
        print(self.ASCII_ART)
        
        # Exibe itens de status
        for status in self.STATUS_ITEMS:
            print(f"|  [OK] {status:<60}|")
        
        # Barra no final
        print("|                                                                       |")
        print("|  PROGRESSO:                                                           |")
        bar = self.get_progress_bar(32)  # 65%
        print(f"|  {bar} 65%       |")
        print(self.FOOTER)


def test_console_splash():
    """Testa a tela de inicialização"""
    splash = ConsoleSplash()
    
    def progress_callback(progress: int):
        pass  # Callback para aplicação integrar
    
    splash.show(progress_callback)
    
    # Simula execução
    time.sleep(2)


if __name__ == "__main__":
    test_console_splash()
