# MENINO DA TI - Guia de Build para Executável

## 📦 Visão Geral

Este guia explica como construir um arquivo `.exe` independente a partir do código Python do MENINO DA TI.

---

## 🚀 Começar Rapidamente

### Opção 1: Interface Gráfica (Recomendado)
```bash
python gui_exe_builder.py
# ou
build_exe_gui.bat
```

### Opção 2: Seletor de Modo
```bash
python build_launcher.py
# ou
build_launcher.bat
```

### Opção 3: Linha de Comando
```bash
python build_exe.py
```

---

## 🔧 Pré-Requisitos

### Obrigatório
- ✅ Python 3.8+ instalado
- ✅ Pip (gerenciador de pacotes)
- ✅ 500 MB de espaço em disco

### Será Instalado Automaticamente
- ✅ PyInstaller 6.3.0+
- ✅ Pillow (para imagens)

### Opcional
- Ícone personalizado (.ico)

---

## 📖 Como Usar (Interface Gráfica)

### Passo 1: Iniciar o Construtor
```bash
python gui_exe_builder.py
```

### Passo 2: Configurar Opções
A janela abrirá com as seguintes opções:

**Ponto de Entrada:**
- `auto_launcher.py` (padrão) - Com seletor de modo
- `launcher.py` - Seletor de modo apenas
- `main_gui.py` - Modo gráfico direto

**Tipo de Build:**
- `Um único arquivo` (padrão) - Mais fácil de distribuir
- `Diretório com arquivos` - Mais rápido na inicialização

**Opções:**
- ✅ `Criar pacote ZIP para distribuição` (padrão)

### Passo 3: Iniciar Build
1. Clique em **"🔨 Iniciar Build"**
2. Confirme as opções na janela de diálogo
3. Aguarde o processo completar (pode levar alguns minutos)

### Passo 4: Resultado
Após o build:
- Executável criado em `dist/MeninoDeTIHelper.exe`
- Documentação em `dist/LEIA-ME.txt`
- Pacote ZIP em `dist/MeninoDaTI_v1.0_YYYYMMDD_HHMMSS.zip`
- Manifest em `dist/manifest.json`

---

## 💻 Como Usar (Linha de Comando)

### Build Simples
```bash
python build_exe.py
```

### Build com Arquivo Único (Padrão)
```bash
pyinstaller --onefile --windowed --name=MeninoDeTIHelper \
    --uac-admin --add-data requirements.txt;. \
    --add-data img;img auto_launcher.py
```

### Build em Diretório
```bash
pyinstaller --onedir --windowed --name=MeninoDeTIHelper \
    --uac-admin --add-data requirements.txt;. \
    --add-data img;img auto_launcher.py
```

---

## 📁 Estrutura de Output

Após o build com sucesso:

```
projeto/
├── dist/
│   ├── MeninoDeTIHelper.exe          # Executável principal
│   ├── LEIA-ME.txt                   # Documentação
│   ├── manifest.json                 # Metadados do build
│   └── MeninoDaTI_v1.0_*.zip         # Pacote distribuição
├── build/                            # Arquivos temporários
└── *.spec                            # Configuração PyInstaller
```

---

## 🎯 Opções de Build Disponíveis

### Ponto de Entrada
| Arquivo | Descrição | Uso |
|---------|-----------|-----|
| `auto_launcher.py` | Seletor de modo com verificação | **Padrão** |
| `launcher.py` | Seletor visual de modo | Alternativo |
| `main_gui.py` | Modo gráfico direto | Simples |

### Tipo de Build
| Tipo | Vantagem | Desvantagem |
|------|----------|------------|
| **Arquivo Único** | Fácil distribuir | Inicialização mais lenta |
| **Diretório** | Inicialização rápida | Mais arquivos |

---

## 🔍 O que É Incluído no Executável

✅ Toda a aplicação Python  
✅ Imagens e recursos (img/)  
✅ Requisitos (requirements.txt)  
✅ Bibliotecas necessárias (tkinter, Pillow, etc.)  
✅ Suporte a privilégios de admin  

---

## ⚠️ Requisitos de Execução do .exe

O executável gerado requer:

- ✅ Windows 10 ou superior
- ✅ Execução como Administrador
- ✅ Sem necessidade de Python instalado
- ✅ Tamanho: ~150-200 MB

---

## 🛠️ Solução de Problemas

### "PyInstaller não encontrado"
```bash
pip install pyinstaller
```

### "Arquivo xxx não encontrado"
- Certifique-se de estar no diretório correto
- Verifique se o arquivo existe

### Build falha silenciosamente
- Verifique se há espaço em disco
- Tente limpar: `rmdir /s build dist`
- Reinicie o prompt de comando

### Executável muito grande (>300 MB)
- Use `--onedir` em vez de `--onefile`
- Compacte com ZIP

### Executável não inicia
- Execute como Administrador
- Verifique logs em `menino_ti_helper_*.log`
- Restaure o arquivo `img/loading.png` se faltando

---

## 🚀 Distribuindo o Executável

### Opção 1: Arquivo Único
```
Enviar: MeninoDeTIHelper.exe (150-200 MB)
```

### Opção 2: Pacote ZIP (Recomendado)
```
Enviar: MeninoDaTI_v1.0_*.zip (80-100 MB)

Conteúdo:
- MeninoDeTIHelper.exe
- LEIA-ME.txt
- manifest.json
```

### Opção 3: Instalador (Avançado)
Para criar um instalador NSIS:
```bash
pip install pyinstaller-nsis
```

---

## 📊 Arquivos Criados

| Arquivo | Descrição | Tamanho |
|---------|-----------|---------|
| `MeninoDeTIHelper.exe` | Executável principal | 150-200 MB |
| `LEIA-ME.txt` | Instruções de uso | ~5 KB |
| `manifest.json` | Metadados do build | ~1 KB |
| `MeninoDaTI_v*.zip` | Pacote compactado | 80-100 MB |

---

## 🔐 Segurança

### Certificação de Código
Para remover aviso de "Arquivo desconhecido":
```bash
# Requer certificado valid
pyinstaller --codesign-identity "Developer ID" ...
```

### SmartScreen do Windows
- Primeiro upload: Windows pode bloquear
- Clique em "Mais informações" → "Executar mesmo assim"
- Após alguns dias: bloqueio removido automaticamente

---

## 🎓 Exemplos de Uso

### Build Padrão
```bash
python build_exe.py
```

### Build Rápido (Diretório)
```bash
python -c "
from exe_builder import ExeBuilder
builder = ExeBuilder()
builder.build_executable(one_file=False)
"
```

### Build Personalizado
```python
from exe_builder import ExeBuilder

builder = ExeBuilder()
success, msg = builder.build(
    create_zip=True,
    one_file=True
)

if success:
    print(f"Sucesso: {msg}")
else:
    print(f"Erro: {msg}")
```

---

## 📚 Referências

- [PyInstaller Docs](https://pyinstaller.readthedocs.io/)
- [Python Packaging](https://packaging.python.org/)
- [Windows App Distribution](https://docs.microsoft.com/en-us/windows/deployment/)

---

## ❓ Perguntas Frequentes

**P: Qual é o tamanho do executável?**  
R: Aproximadamente 150-200 MB para um arquivo único

**P: O executável funciona sem Python?**  
R: Sim, é completamente independente

**P: Preciso de permissão de admin para executar?**  
R: Sim, por design (necessário para atualizações do sistema)

**P: Posso distribuir o .exe?**  
R: Sim, é permitido distribuir

**P: Como desinstalar?**  
R: Apenas delete o arquivo .exe

**P: Posso usar em empresas?**  
R: Sim, é open source (verifique a licença)

---

## 📞 Suporte

Problemas ao compilar?

1. Execute: `python system_check.py`
2. Verifique se Python 3.8+ está instalado
3. Abra uma issue no GitHub com a saída do erro

---

**Versão:** 1.0  
**Última Atualização:** 19 de janeiro de 2026  
**Status:** ✅ Completo e Testado
