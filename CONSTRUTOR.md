# MENINO DA TI - Construtor de Executável

## 🔧 Sobre

Aplicativo paralelo que converte o **MENINO DA TI** (aplicação Python) em um arquivo `.exe` independente e distribuível para Windows.

---

## 🚀 Início Rápido

### 1. Interface Gráfica (Recomendado)
```bash
python gui_exe_builder.py
```
ou
```bash
build_exe_gui.bat
```

### 2. Com Seletor de Modo
```bash
python build_launcher.py
```
ou
```bash
build_launcher.bat
```

### 3. Linha de Comando
```bash
python build_exe.py
```

---

## 📋 Arquivos do Sistema de Build

### Módulos Python

| Arquivo | Descrição |
|---------|-----------|
| `exe_builder.py` | Módulo principal de build (classe `ExeBuilder`) |
| `gui_exe_builder.py` | Interface gráfica para construir |
| `build_launcher.py` | Seletor de modo (GUI ou CLI) |
| `build_exe.py` | Script CLI original |

### Scripts Batch

| Arquivo | Descrição |
|---------|-----------|
| `build_launcher.bat` | Inicia seletor de modo |
| `build_exe_gui.bat` | Abre interface gráfica |

### Documentação

| Arquivo | Descrição |
|---------|-----------|
| `GUIA_BUILD.md` | Guia completo de build (ESTE ARQUIVO) |
| `CONSTRUTOR.md` | Este documento |

---

## 🎯 Funcionalidades

✅ **Construção Automática** - Converte Python em .exe com um clique  
✅ **Interface Gráfica** - Barra de progresso visual  
✅ **Modo Console** - Para build não-interativo  
✅ **Múltiplos Pontos de Entrada** - Escolha qual módulo executar  
✅ **Pacote ZIP** - Cria pacote para distribuição  
✅ **Documentação Automática** - Gera README e manifest  
✅ **Privilégios Admin** - Executável solicita permissions  
✅ **Recurso Completo** - Inclui imagens e arquivos  

---

## 🔍 O Que É Incluído no Build

- ✅ Toda aplicação MENINO DA TI
- ✅ Interface gráfica (tkinter)
- ✅ Modo console com ASCII art
- ✅ Tela de carregamento com imagens
- ✅ Verificação de compatibilidade do SO
- ✅ Todas as dependências Python
- ✅ Recursos (imagens em img/)

---

## 💻 Interface Gráfica

### Tela Principal
```
╔══════════════════════════════════════════════════════════════════╗
║         🔧 Construtor de Executável - MENINO DA TI              ║
║    Converta a aplicação Python em arquivo .exe independente      ║
╚══════════════════════════════════════════════════════════════════╝

OPÇÕES DE BUILD:
┌─────────────────────────────────────────────────────────────────┐
│ Ponto de Entrada: [auto_launcher.py ▼]                          │
│ Tipo de Build:    ◉ Um único arquivo (.exe)                     │
│                   ○ Diretório com arquivos                      │
│ Opções:           ☑ Criar pacote ZIP para distribuição          │
└─────────────────────────────────────────────────────────────────┘

PROGRESSO:
[████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 45%

LOG:
[20:30:15] [1/6] Limpando builds anteriores...
[20:30:16]   - Removido: build
[20:30:16]   - Removido: dist

BOTÕES:
[🔨 Iniciar Build] [⛔ Cancelar] [📁 Abrir Pasta dist/]
```

### Campos Configuráveis

**Ponto de Entrada:**
- `auto_launcher.py` - Com seletor de modo (PADRÃO)
- `launcher.py` - Seletor visual de modo
- `main_gui.py` - Modo gráfico direto

**Tipo de Build:**
- `Arquivo Único` - Um .exe (150-200 MB) - Fácil distribuir
- `Diretório` - Pasta com arquivos - Inicializa mais rápido

**Opções:**
- `Criar ZIP` - Compacta para distribuição (Recomendado)

---

## 📊 Processo de Build

```
┌─────────────────────┐
│  1. Limpar Builds   │ Remover folders e arquivos antigos
└────────┬────────────┘
         ↓
┌─────────────────────┐
│2. Verificar Python  │ Conferir PyInstaller instalado
└────────┬────────────┘
         ↓
┌─────────────────────┐
│ 3. Construir Exe    │ PyInstaller converte Python→.exe
└────────┬────────────┘
         ↓
┌─────────────────────┐
│4. Verificar Saída   │ Confirmar que o .exe foi criado
└────────┬────────────┘
         ↓
┌─────────────────────┐
│5. Documentação      │ Gerar README e manifest.json
└────────┬────────────┘
         ↓
┌─────────────────────┐
│ 6. Criar ZIP (Opt) │ Compactar para distribuição
└────────┬────────────┘
         ↓
    ✅ CONCLUÍDO
```

---

## 📁 Estrutura de Saída

```
projeto/
├── dist/                                    [Resultado]
│   ├── MeninoDeTIHelper.exe                [Executável principal]
│   ├── LEIA-ME.txt                         [Instruções]
│   ├── manifest.json                       [Metadados]
│   └── MeninoDaTI_v1.0_20260119_203015.zip [Pacote ZIP]
│
├── build/                                   [Temporário - será deletado]
│   └── (arquivos intermediários)
│
└── *.spec                                   [Config PyInstaller - será deletado]
```

---

## 🎯 Exemplos de Uso

### Exemplo 1: Build Gráfico Padrão
```bash
python gui_exe_builder.py
# [Abre interface]
# [Clica em "Iniciar Build"]
# [Resultado em dist/]
```

### Exemplo 2: Build via CLI
```bash
python build_exe.py
# [Executa automaticamente]
# [Resultado em dist/]
```

### Exemplo 3: Programático
```python
from exe_builder import ExeBuilder

def progress(msg, percent):
    print(f"[{percent}%] {msg}")

builder = ExeBuilder(callback=progress)
success, message = builder.build(create_zip=True)

if success:
    print(f"✅ {message}")
else:
    print(f"❌ {message}")
```

---

## 🐛 Solução de Problemas

### "PyInstaller não encontrado"
```bash
pip install pyinstaller
```

### Build muito lento
- Não é anormal levar 3-5 minutos
- Feche outros programas
- Verifique espaço em disco

### Executável não funciona
- Execute como Administrador
- Verifique Windows Defender não está bloqueando
- Restaure arquivo `img/loading.png`

### Erro de permissão
- Execute o prompt como Administrador
- Ou use `python build_launcher.py`

---

## ⚠️ Requisitos

### Para Compilar
- Python 3.8+
- pip
- PyInstaller (instalado automaticamente)
- 500 MB de espaço

### Para Executar o .exe
- Windows 10 ou superior
- Privilégios de administrador
- Sem Python necessário

---

## 📊 Informações de Build

### Tamanho do Executável
- **Arquivo único**: 150-200 MB
- **Diretório**: ~100 MB (sem compactação)
- **ZIP**: 80-100 MB (compactado)

### Tempo de Build
- Primeira vez: 3-5 minutos (instala PyInstaller)
- Próximas: 1-3 minutos

### Compatibilidade
- ✅ Windows 10
- ✅ Windows 11
- ⚠️ Windows 7 (não suportado pela aplicação)

---

## 🔒 Segurança

O executável incluir:
- ✅ Verificação de SO
- ✅ Requisição de Admin
- ✅ Sem modificação do registro
- ✅ Sem DLL maliciosas

---

## 📈 Melhorias Futuras

- [ ] Compressão NSIS para instalador
- [ ] Ícone personalizado
- [ ] Certificado de código
- [ ] Assinatura digital
- [ ] Versioning automático
- [ ] GitHub Releases integration

---

## 📞 Suporte

### Documentação
- [GUIA_BUILD.md](GUIA_BUILD.md) - Guia completo
- [VERIFICACAO_SISTEMA.md](VERIFICACAO_SISTEMA.md) - Verificação de SO

### Arquivos Relacionados
- `exe_builder.py` - Classe principal
- `gui_exe_builder.py` - Interface
- `build_launcher.py` - Seletor
- `build_exe.py` - Script original

---

## 📜 Licença

Este construtor é parte do MENINO DA TI e segue a mesma licença.

---

**Versão:** 1.0  
**Data:** 19 de janeiro de 2026  
**Status:** ✅ Completo e Funcional  
**Mantido por:** exadmax
