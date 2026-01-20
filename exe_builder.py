"""
exe_builder.py - Módulo avançado para construção de executável
Fornece funções reutilizáveis para o build do MENINO DA TI
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Tuple, Callable
import json
from datetime import datetime


class ExeBuilder:
    """Construtor de executável para MENINO DA TI"""
    
    def __init__(self, callback: Callable[[str, int], None] = None):
        """
        Inicializa o construtor
        
        Args:
            callback: Função para relatar progresso (mensagem, percentual)
        """
        self.callback = callback
        self.project_path = Path.cwd()
        self.build_dir = self.project_path / 'build'
        self.dist_dir = self.project_path / 'dist'
        self.exe_path = self.dist_dir / 'MeninoDeTIHelper.exe'
        
    def log(self, message: str, progress: int = None):
        """Log com callback"""
        if self.callback:
            self.callback(message, progress or 0)
        else:
            print(message)
    
    def clean_build_folders(self) -> bool:
        """Remove pastas de build anteriores"""
        self.log("[1/6] Limpando builds anteriores...", 10)
        
        try:
            folders_to_remove = ['build', 'dist', '__pycache__', '.pytest_cache']
            
            for folder in folders_to_remove:
                folder_path = self.project_path / folder
                if folder_path.exists():
                    shutil.rmtree(folder_path)
                    self.log(f"  - Removido: {folder}", 15)
            
            # Remover arquivos .spec
            for spec_file in self.project_path.glob('*.spec'):
                spec_file.unlink()
                self.log(f"  - Removido: {spec_file.name}", 15)
            
            return True
        except Exception as e:
            self.log(f"[ERRO] Erro ao limpar builds: {e}", 15)
            return False
    
    def check_pyinstaller(self) -> bool:
        """Verifica se PyInstaller está instalado"""
        self.log("[2/6] Verificando PyInstaller...", 20)
        
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'show', 'pyinstaller'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                self.log("  - PyInstaller encontrado", 25)
                return True
            else:
                self.log("  - PyInstaller não encontrado", 25)
                return False
        except Exception as e:
            self.log(f"[ERRO] Erro ao verificar PyInstaller: {e}", 25)
            return False
    
    def install_pyinstaller(self) -> bool:
        """Instala PyInstaller"""
        self.log("[2/6] Instalando PyInstaller...", 25)
        
        try:
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', 'pyinstaller', '--quiet'],
                check=True,
                timeout=120
            )
            self.log("  - PyInstaller instalado", 30)
            return True
        except Exception as e:
            self.log(f"[ERRO] Erro ao instalar PyInstaller: {e}", 30)
            return False
    
    def build_executable(self, 
                        entry_point: str = 'auto_launcher.py',
                        icon_path: str = None,
                        one_file: bool = True) -> bool:
        """
        Constrói o executável
        
        Args:
            entry_point: Arquivo de entrada (padrão: auto_launcher.py)
            icon_path: Caminho para ícone (opcional)
            one_file: Se True, gera um arquivo único
        
        Returns:
            True se sucesso, False se falha
        """
        self.log("[3/6] Construindo executável...", 35)
        
        # Verificar arquivo de entrada
        entry_file = self.project_path / entry_point
        if not entry_file.exists():
            self.log(f"[ERRO] Arquivo de entrada não encontrado: {entry_point}", 40)
            return False
        
        # Construir comando PyInstaller
        cmd = [
            sys.executable,
            '-m', 'PyInstaller',
            '--onefile' if one_file else '--onedir',
            '--windowed',
            '--name=MeninoDeTIHelper',
            '--add-data=requirements.txt;.',
            '--add-data=img;img',
            '--clean',
            '--noconfirm',
            '--hidden-import=tkinter',
            '--hidden-import=tkinter.ttk',
            '--hidden-import=tkinter.scrolledtext',
            '--hidden-import=tkinter.messagebox',
            '--uac-admin',
        ]
        
        # Adicionar ícone se fornecido
        if icon_path:
            icon_file = self.project_path / icon_path
            if icon_file.exists():
                cmd.append(f'--icon={icon_file}')
                self.log(f"  - Usando ícone: {icon_path}", 40)
        
        cmd.append(str(entry_file))
        
        try:
            self.log(f"  - Executando PyInstaller...", 45)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                self.log(f"[ERRO] PyInstaller falhou:\n{result.stderr}", 50)
                return False
            
            self.log("  - Executável construído", 70)
            return True
            
        except subprocess.TimeoutExpired:
            self.log("[ERRO] Timeout durante o build (timeout de 5 minutos)", 50)
            return False
        except Exception as e:
            self.log(f"[ERRO] Erro durante build: {e}", 50)
            return False
    
    def verify_executable(self) -> bool:
        """Verifica se o executável foi criado com sucesso"""
        self.log("[4/6] Verificando executável...", 75)
        
        if self.exe_path.exists():
            size_mb = self.exe_path.stat().st_size / (1024 * 1024)
            self.log(f"  - Executável encontrado: {self.exe_path.name}", 80)
            self.log(f"  - Tamanho: {size_mb:.2f} MB", 80)
            return True
        else:
            self.log(f"[ERRO] Executável não encontrado em {self.dist_dir}", 80)
            return False
    
    def create_readme(self) -> bool:
        """Cria README para o executável"""
        self.log("[5/6] Criando documentação...", 85)
        
        readme_content = """# MENINO DA TI - Executável Independente

## Sobre

Este é um executável standalone do MENINO DA TI Helper que não requer Python instalado.

**Versão:** 1.0
**Data de Build:** """ + datetime.now().strftime("%d de %B de %Y às %H:%M:%S") + """

## Como Executar

### IMPORTANTE: Execute como Administrador!

O programa requer privilégios de administrador para funcionar corretamente.

#### Opção 1: Execução Rápida (Recomendado)
1. Localize **MeninoDeTIHelper.exe**
2. Clique com o botão DIREITO
3. Selecione **"Executar como administrador"**
4. Clique **"Sim"** na janela de confirmação

#### Opção 2: Sempre Como Administrador
1. Clique direito no **MeninoDeTIHelper.exe**
2. Selecione **"Propriedades"**
3. Vá para aba **"Compatibilidade"**
4. Marque **"Executar este programa como um administrador"**
5. Clique **"OK"**

## Requisitos

- **Windows:** Windows 10 ou superior
- **Memória:** 512 MB mínimo (1 GB recomendado)
- **Espaço:** 200 MB disponível
- **Internet:** Para atualizações do sistema

## Funcionalidades

✓ Verificação automática de compatibilidade do SO
✓ Modo Console com arte ASCII
✓ Modo Gráfico com interface completa
✓ Tela de carregamento animada
✓ Barra de progresso inteligente
✓ Suporte a Windows 10 e Windows 11

## Troubleshooting

### Programa não inicia
- Verifique se está executando como Administrador
- Desabilite temporariamente o antivírus/Windows Defender
- Tente executar em modo de compatibilidade (Windows 10)

### "Arquivo suspeito" ou "Perigo detectado"
- SmartScreen/Defender pode bloquear executáveis desconhecidos
- Clique em "Mais informações" → "Executar assim mesmo"
- Ou desabilite SmartScreen temporariamente

### Performance lenta
- Feche outros programas
- Verifique espaço em disco
- Reinicie o computador

## Logs

O programa gera logs em:
```
menino_ti_helper_YYYYMMDD_HHMMSS.log
```

Verifique estes logs se encontrar problemas.

## Desinstalação

Para remover o programa:
1. Delete o arquivo **MeninoDeTIHelper.exe**
2. Delete o arquivo **README_EXECUTAVEL.txt**
3. Pronto!

Não há registro no Windows nem instalação de sistema.

## Informações Técnicas

- **Baseado em:** Python 3.12.10
- **GUI Framework:** Tkinter
- **Empacotador:** PyInstaller 6.3.0
- **Tipo:** Aplicação Standalone

## Suporte

Para reportar problemas ou sugestões:
- GitHub: https://github.com/exadmax/meninodati
- Issues: https://github.com/exadmax/meninodati/issues

---

Desenvolvido com ❤️ por exadmax
Última atualização: """ + datetime.now().strftime("%d/%m/%Y") + """
"""
        
        try:
            readme_path = self.dist_dir / 'LEIA-ME.txt'
            readme_path.write_text(readme_content, encoding='utf-8')
            self.log(f"  - Documentação criada: LEIA-ME.txt", 90)
            
            # Também criar um arquivo de manifest
            manifest_data = {
                "nome": "MENINO DA TI",
                "versao": "1.0",
                "data_build": datetime.now().isoformat(),
                "python_versao": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "tamanho_bytes": self.exe_path.stat().st_size if self.exe_path.exists() else 0,
                "arquivo_executavel": "MeninoDeTIHelper.exe"
            }
            
            manifest_path = self.dist_dir / 'manifest.json'
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest_data, f, indent=2, ensure_ascii=False)
            
            self.log(f"  - Manifest criado: manifest.json", 90)
            return True
            
        except Exception as e:
            self.log(f"[ERRO] Erro ao criar documentação: {e}", 90)
            return False
    
    def create_distribution_package(self) -> bool:
        """Cria um pacote de distribuição zip"""
        self.log("[6/6] Criando pacote de distribuição...", 95)
        
        try:
            import zipfile
            
            zip_name = f'MeninoDeTI_v1.0_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
            zip_path = self.project_path / 'dist' / zip_name
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                # Adicionar executável
                zf.write(self.exe_path, 'MeninoDeTIHelper.exe')
                
                # Adicionar README
                readme_path = self.dist_dir / 'LEIA-ME.txt'
                if readme_path.exists():
                    zf.write(readme_path, 'LEIA-ME.txt')
                
                # Adicionar manifest
                manifest_path = self.dist_dir / 'manifest.json'
                if manifest_path.exists():
                    zf.write(manifest_path, 'manifest.json')
            
            size_mb = zip_path.stat().st_size / (1024 * 1024)
            self.log(f"  - Pacote criado: {zip_name} ({size_mb:.2f} MB)", 100)
            
            return True
            
        except Exception as e:
            self.log(f"[ERRO] Erro ao criar pacote: {e}", 100)
            return False
    
    def build(self, create_zip: bool = True) -> Tuple[bool, str]:
        """
        Executa o processo completo de build
        
        Args:
            create_zip: Se True, cria pacote zip também
        
        Returns:
            (sucesso: bool, mensagem: str)
        """
        try:
            # Etapa 1: Limpar
            if not self.clean_build_folders():
                return False, "Falha ao limpar builds anteriores"
            
            # Etapa 2: Verificar/Instalar PyInstaller
            if not self.check_pyinstaller():
                if not self.install_pyinstaller():
                    return False, "Falha ao instalar PyInstaller"
            
            # Etapa 3: Construir executável
            if not self.build_executable():
                return False, "Falha ao construir executável"
            
            # Etapa 4: Verificar executável
            if not self.verify_executable():
                return False, "Executável não foi criado corretamente"
            
            # Etapa 5: Criar documentação
            if not self.create_readme():
                self.log("[AVISO] Erro ao criar documentação, continuando...", 85)
            
            # Etapa 6: Criar pacote (opcional)
            if create_zip:
                if not self.create_distribution_package():
                    self.log("[AVISO] Erro ao criar pacote zip, continuando...", 95)
            
            self.log("[COMPLETO] Build finalizado com sucesso!", 100)
            return True, f"Executável pronto em: {self.dist_dir}"
            
        except Exception as e:
            return False, f"Erro durante build: {str(e)}"


def main():
    """Teste da classe"""
    builder = ExeBuilder()
    
    def progress_callback(message: str, progress: int):
        print(f"[{progress}%] {message}")
    
    builder.callback = progress_callback
    
    success, message = builder.build()
    print(f"\n{message}")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
