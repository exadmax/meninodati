# -*- coding: utf-8 -*-
"""
Script de build para gerar executável do Menino de TI Helper
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build_folders():
    """Remove pastas de build anteriores"""
    print("[CLEANUP] Limpando builds anteriores...")
    folders_to_remove = ['build', 'dist', '__pycache__']
    
    for folder in folders_to_remove:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                print(f"  [OK] Removido: {folder}")
            except Exception as e:
                print(f"  ⚠ Aviso ao remover {folder}: {e}")
    
    # Remover arquivos .spec antigos
    for spec_file in Path('.').glob('*.spec'):
        try:
            spec_file.unlink()
            print(f"  ✓ Removido: {spec_file}")
        except Exception as e:
            print(f"  [WARN] Aviso ao remover {spec_file}: {e}")

def check_pyinstaller():
    """Verifica se PyInstaller está instalado"""
    print("[CHECK] Verificando PyInstaller...")
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'show', 'pyinstaller'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("  [OK] PyInstaller encontrado")
            return True
        else:
            print("  [NOT FOUND] PyInstaller não encontrado")
            return False
    except Exception as e:
        print(f"  [ERROR] Erro ao verificar PyInstaller: {e}")
        return False

def install_pyinstaller():
    """Instala PyInstaller"""
    print("📦 Instalando PyInstaller...")
    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', 'pyinstaller'],
            check=True
        )
        print("  [OK] PyInstaller instalado com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  [ERROR] Erro ao instalar PyInstaller: {e}")
        return False

def build_executable():
    """Gera o executável usando PyInstaller"""
    print("\n[BUILD] Construindo executável...")
    print("=" * 60)
    
    # Parâmetros do PyInstaller
    cmd = [
        sys.executable,
        '-m', 'PyInstaller',
        '--onefile',                    # Gerar um único arquivo
        '--windowed',                   # Não mostrar console (GUI app)
        '--name=MeninoDeTIHelper',      # Nome do executável
        '--icon=NONE',                   # Sem ícone por enquanto (pode adicionar depois)
        '--add-data=requirements.txt;.', # Incluir requirements.txt
        '--clean',                       # Limpar cache
        '--noconfirm',                   # Não pedir confirmação
        # Adicionar recursos do tkinter
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.scrolledtext',
        '--hidden-import=tkinter.messagebox',
        'main_gui.py'                    # Arquivo principal
    ]
    
    print(f"Comando: {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(cmd, check=True)
        
        print("\n" + "=" * 60)
        print("[SUCCESS] Build concluído com sucesso!")
        print("=" * 60)
        
        # Verificar se o executável foi criado
        exe_path = Path('dist') / 'MeninoDeTIHelper.exe'
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"\n[FILE] Executável criado:")
            print(f"   Localização: {exe_path.absolute()}")
            print(f"   Tamanho: {size_mb:.2f} MB")
            return True
        else:
            print("\n⚠ Aviso: Executável não encontrado em dist/")
            return False
            
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 60)
        print(f"❌ Erro durante o build: {e}")
        print("=" * 60)
        return False

def create_readme_for_exe():
    """Cria README para o executável"""
    print("\n📝 Criando README...")
    
    readme_content = """# Menino de TI Helper - Executável

## 📦 Instalação

O arquivo **MeninoDeTIHelper.exe** é um executável standalone que não requer instalação.

## 🚀 Como Usar

### IMPORTANTE: Executar como Administrador

Este programa **PRECISA** ser executado como Administrador para funcionar corretamente.

#### Método 1: Executar como Administrador (Recomendado)
1. Localize o arquivo `MeninoDeTIHelper.exe`
2. Clique com o botão DIREITO sobre o arquivo
3. Selecione **"Executar como administrador"**
4. Clique em **"Sim"** na janela de controle de conta de usuário (UAC)

#### Método 2: Sempre Executar como Administrador
1. Clique com o botão DIREITO sobre `MeninoDeTIHelper.exe`
2. Selecione **"Propriedades"**
3. Vá para a aba **"Compatibilidade"**
4. Marque a opção **"Executar este programa como administrador"**
5. Clique em **"OK"**
6. Agora você pode executar o programa normalmente (duplo clique)

## 🔧 Funcionalidades

- **Atualização Automática de Aplicativos**: Atualiza todos os programas instalados usando winget
- **Windows Update**: Executa atualizações do Windows automaticamente
- **Barra de Progresso Inteligente**: Mostra o progresso detalhado de 0 a 100%
- **Atualizações Silenciosas**: Todas as licenças são aceitas automaticamente
- **Interface Gráfica Intuitiva**: Fácil de usar com feedback visual

## ⚠️ Requisitos

- Windows 10/11
- Windows Package Manager (winget) - geralmente já instalado
- Conexão com a Internet

## 🐛 Solução de Problemas

### O programa não inicia
- Certifique-se de estar executando como Administrador
- Verifique se o Windows Defender ou antivírus não está bloqueando

### Winget não encontrado
- Instale o "App Installer" da Microsoft Store
- Ou baixe de: https://github.com/microsoft/winget-cli/releases

### Atualizações falham
- Execute como Administrador
- Verifique sua conexão com a Internet
- Aguarde e tente novamente (servidores podem estar ocupados)

## 📋 Logs

O programa gera arquivos de log com o nome:
`menino_ti_helper_YYYYMMDD_HHMMSS.log`

Esses logs podem ajudar a identificar problemas.

## 📧 Suporte

Para reportar problemas ou sugestões, abra uma issue no GitHub.

---
Desenvolvido por exadmax
"""
    
    try:
        readme_path = Path('dist') / 'README_EXECUTAVEL.txt'
        readme_path.parent.mkdir(exist_ok=True)
        readme_path.write_text(readme_content, encoding='utf-8')
        print(f"  [OK] README criado: {readme_path}")
        return True
    except Exception as e:
        print(f"  [WARN] Erro ao criar README: {e}")
        return False

def main():
    """Função principal"""
    # Forçar UTF-8 no stdout
    import io
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=" * 60)
    print("[BUILD] Menino de TI Helper - Build Script")
    print("=" * 60)
    print()
    
    # Etapa 1: Limpar builds anteriores
    clean_build_folders()
    print()
    
    # Etapa 2: Verificar e instalar PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
            print("\n❌ Falha ao preparar PyInstaller. Abortando.")
            return 1
    print()
    
    # Etapa 3: Construir executável
    if not build_executable():
        print("\n❌ Falha no build. Verifique os erros acima.")
        return 1
    
    # Etapa 4: Criar README
    create_readme_for_exe()
    
    print("\n" + "=" * 60)
    print("\n[SUCCESS] PROCESSO CONCLUÍDO!")
    print("=" * 60)
    print("\n📁 Seus arquivos estão em: dist/")
    print("   - MeninoDeTIHelper.exe (executável)")
    print("   - README_EXECUTAVEL.txt (instruções)")
    print("\n⚠️  IMPORTANTE: Execute o .exe como Administrador!")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
