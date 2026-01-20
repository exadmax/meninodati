"""
system_check.py - Verificação de compatibilidade do sistema operacional
Verifica SO, versão do Windows e requisitos mínimos
"""
import sys
import platform
import struct
from typing import Tuple, Dict


class SystemChecker:
    """Verifica compatibilidade do sistema operacional"""
    
    # Versões mínimas suportadas
    MIN_WINDOWS_VERSION = (10, 0)  # Windows 10
    MIN_WINDOWS_BUILD = 14393  # Windows 10 Build 14393 (initial release)
    
    SUPPORTED_OS = ["Windows", "Linux", "Darwin"]  # macOS é Darwin
    
    def __init__(self):
        self.system = platform.system()
        self.release = platform.release()
        self.version = platform.version()
        self.architecture = struct.calcsize("P") * 8  # 32 ou 64 bits
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    def get_windows_version(self) -> Tuple[int, int]:
        """Obtém versão do Windows como tupla (major, minor)"""
        try:
            import winreg
            # Ler versão do Windows do registro
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                r'SOFTWARE\Microsoft\Windows NT\CurrentVersion')
            current_version, _ = winreg.QueryValueEx(key, 'CurrentVersion')
            winreg.CloseKey(key)
            
            parts = current_version.split('.')
            if len(parts) >= 2:
                return (int(parts[0]), int(parts[1]))
        except:
            pass
        
        # Fallback: usar release do platform
        if self.release == "11":
            return (10, 0)  # Windows 11 é considerado 10.0 internamente
        elif self.release == "10":
            return (10, 0)  # Windows 10
        elif self.release == "8.1":
            return (6, 3)
        elif self.release == "8":
            return (6, 2)
        elif self.release == "7":
            return (6, 1)
        
        return None
    
    def get_windows_build(self) -> int:
        """Obtém número de build do Windows"""
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SOFTWARE\Microsoft\Windows NT\CurrentVersion')
            build, _ = winreg.QueryValueEx(key, 'CurrentBuildNumber')
            winreg.CloseKey(key)
            return int(build)
        except:
            pass
        
        return None
    
    def get_windows_release_name(self, version: Tuple[int, int], build: int) -> str:
        """Retorna nome amigável da versão do Windows"""
        if version is None:
            # Usar release do platform como fallback
            if self.release == "11":
                return "Windows 11"
            elif self.release == "10":
                return "Windows 10"
            elif self.release == "8.1":
                return "Windows 8.1"
            elif self.release == "8":
                return "Windows 8"
            elif self.release == "7":
                return "Windows 7"
            return "Desconhecido"
        
        # Windows 10/11
        if version == (10, 0):
            if self.release == "11" or (build and build >= 22000):
                return "Windows 11"
            elif build and build >= 19041:
                return "Windows 10 21H2"
            elif build and build >= 19041:
                return "Windows 10 20H2"
            else:
                return "Windows 10"
        
        # Windows 8.1
        elif version == (6, 3):
            return "Windows 8.1"
        
        # Windows 8
        elif version == (6, 2):
            return "Windows 8"
        
        # Windows 7
        elif version == (6, 1):
            return "Windows 7"
        
        # Windows Vista
        elif version == (6, 0):
            return "Windows Vista"
        
        # Windows XP
        elif version == (5, 1):
            return "Windows XP"
        
        return f"Windows {version[0]}.{version[1]}"
    
    def is_compatible(self) -> Tuple[bool, str]:
        """
        Verifica compatibilidade do sistema
        
        Returns:
            (is_compatible: bool, message: str)
        """
        if self.system not in self.SUPPORTED_OS:
            return False, f"SO não suportado: {self.system}. Suportados: {', '.join(self.SUPPORTED_OS)}"
        
        # Verificações específicas para Windows
        if self.system == "Windows":
            # Usar release como indicador principal
            release_lower = self.release.lower()
            
            # Windows 11 ou 10 são compatíveis
            if release_lower in ["11", "10"]:
                return True, "Windows compatível"
            
            # Windows 8.1 ou inferior não são suportados
            if release_lower in ["8.1", "8", "7", "vista", "xp"]:
                version_names = {
                    "8.1": "Windows 8.1",
                    "8": "Windows 8",
                    "7": "Windows 7",
                    "vista": "Windows Vista",
                    "xp": "Windows XP"
                }
                release_name = version_names.get(release_lower, f"Windows {release_lower}")
                return False, (
                    f"Windows incompatível: {release_name}\n"
                    f"Versão mínima: Windows 10"
                )
            
            # Fallback para verificação de build
            version = self.get_windows_version()
            build = self.get_windows_build()
            
            if version is None:
                return False, "Não foi possível determinar a versão do Windows"
            
            # Verificar versão mínima
            if version < self.MIN_WINDOWS_VERSION:
                release_name = self.get_windows_release_name(version, build)
                return False, (
                    f"Windows incompatível: {release_name} ({version[0]}.{version[1]})\n"
                    f"Versão mínima: Windows 10"
                )
        
        return True, "Sistema compatível"
    
    def get_system_info(self) -> Dict:
        """Retorna dicionário com informações do sistema"""
        windows_version = None
        windows_build = None
        windows_release = None
        
        if self.system == "Windows":
            windows_version = self.get_windows_version()
            windows_build = self.get_windows_build()
            if windows_version:
                windows_release = self.get_windows_release_name(windows_version, windows_build)
        
        return {
            "sistema_operacional": self.system,
            "versao": self.version,
            "release": self.release,
            "arquitetura_bits": self.architecture,
            "python_versao": self.python_version,
            "windows_versao": windows_version,
            "windows_build": windows_build,
            "windows_release": windows_release
        }
    
    def print_system_info(self):
        """Exibe informações do sistema no console"""
        info = self.get_system_info()
        
        print("\n" + "="*70)
        print("INFORMACOES DO SISTEMA")
        print("="*70)
        print(f"Sistema Operacional: {info['sistema_operacional']}")
        print(f"Versao: {info['versao']}")
        print(f"Release: {info['release']}")
        print(f"Arquitetura: {info['arquitetura_bits']} bits")
        print(f"Python: {info['python_versao']}")
        
        if info['windows_versao']:
            print(f"\nWindows:")
            print(f"  Release: {info['windows_release']}")
            print(f"  Versao: {info['windows_versao'][0]}.{info['windows_versao'][1]}")
            if info['windows_build']:
                print(f"  Build: {info['windows_build']}")
        
        print("="*70 + "\n")
    
    def print_compatibility_status(self):
        """Exibe status de compatibilidade"""
        is_compatible, message = self.is_compatible()
        
        status_symbol = "[OK]" if is_compatible else "[!]"
        status_text = "COMPATIVEL" if is_compatible else "INCOMPATIVEL"
        
        print("\n" + "="*70)
        print("VERIFICACAO DE COMPATIBILIDADE")
        print("="*70)
        print(f"{status_symbol} {status_text}")
        print(f"\n{message}\n")
        print("="*70 + "\n")
        
        return is_compatible


def main():
    """Função para teste"""
    checker = SystemChecker()
    
    checker.print_system_info()
    is_compatible = checker.print_compatibility_status()
    
    if not is_compatible:
        print("AVISO: Este aplicativo pode não funcionar corretamente neste sistema!")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
