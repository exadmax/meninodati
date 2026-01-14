# 📑 Índice de Arquivos - Menino de TI Helper v2.0

## 🎯 Começar Aqui

Se você é **novo no projeto**, comece por:

1. **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** 
   - ⏱️ 5 minutos de leitura
   - Guia rápido para começar
   - Para usuários e desenvolvedores

2. **[README_V2.md](README_V2.md)**
   - ⏱️ 15 minutos de leitura
   - Manual completo do usuário
   - Instalação, uso e troubleshooting

---

## 📂 Estrutura Completa dos Arquivos

### 🚀 Arquivos Principais (Para Executar)

| Arquivo | Descrição | Quando Usar |
|---------|-----------|-------------|
| **main_gui.py** | 🆕 Aplicação principal v2.0 | **Execute este para GUI moderna** |
| main.py | 📜 Versão antiga (referência) | Mantido para compatibilidade |
| powershell_manager.py | ⚙️ Gerenciador PowerShell | Usado internamente |

**Como executar:**
```bash
python main_gui.py
```

---

### 🛠️ Ferramentas de Build

| Arquivo | Descrição | Quando Usar |
|---------|-----------|-------------|
| **build_exe.py** | 🔨 Script de build para .exe | Gerar executável Windows |
| requirements.txt | 📦 Dependências Python | Instalar bibliotecas |

**Como usar:**
```bash
# Instalar dependências
pip install -r requirements.txt

# Gerar executável
python build_exe.py
```

---

### 📚 Documentação (Leia Antes de Usar)

#### Para Usuários Finais

| Arquivo | Conteúdo | Tempo | Prioridade |
|---------|----------|-------|------------|
| **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** | Início rápido | 5 min | 🔥 Alta |
| **[README_V2.md](README_V2.md)** | Manual completo | 15 min | 🔥 Alta |
| [GUIA_DE_USO.md](GUIA_DE_USO.md) | Guia original | 10 min | ⚡ Média |

#### Para Desenvolvedores

| Arquivo | Conteúdo | Tempo | Prioridade |
|---------|----------|-------|------------|
| **[PASSO_A_PASSO.md](PASSO_A_PASSO.md)** | Guia de desenvolvimento detalhado | 30 min | 🔥 Alta |
| **[GUIA_DE_BUILD.md](GUIA_DE_BUILD.md)** | Como fazer build do .exe | 10 min | 🔥 Alta |
| **[RESUMO_IMPLEMENTACAO.md](RESUMO_IMPLEMENTACAO.md)** | Resumo executivo | 15 min | ⚡ Média |

#### Gerais

| Arquivo | Conteúdo |
|---------|----------|
| **[README.md](README.md)** | README original do projeto |
| **[LICENSE](LICENSE)** | Licença MIT |
| **[INDEX.md](INDEX.md)** | Este arquivo (índice) |

---

### 🗂️ Scripts Auxiliares

| Arquivo | Descrição | Sistema |
|---------|-----------|---------|
| run.bat | Script de execução | Windows (CMD) |
| run_admin.bat | Execução como admin | Windows (CMD) |
| run.ps1 | Script PowerShell | Windows (PS) |
| test_setup.py | Teste de configuração | Python |

---

## 🎓 Guia de Leitura por Perfil

### 👤 Sou Usuário Final

**Quero usar o programa:**

1. ✅ [INICIO_RAPIDO.md](INICIO_RAPIDO.md) - Como começar
2. ✅ [README_V2.md](README_V2.md) - Manual completo
3. ⚠️ Execute: `MeninoDeTIHelper.exe` como Administrador

**Tempo total:** 20 minutos de leitura + uso do programa

---

### 👨‍💻 Sou Desenvolvedor

**Quero entender e modificar o código:**

1. ✅ [INICIO_RAPIDO.md](INICIO_RAPIDO.md) - Setup rápido
2. ✅ [PASSO_A_PASSO.md](PASSO_A_PASSO.md) - Arquitetura detalhada
3. ✅ [RESUMO_IMPLEMENTACAO.md](RESUMO_IMPLEMENTACAO.md) - Visão geral
4. 💻 Examine: `main_gui.py` - Código principal
5. 💻 Examine: `powershell_manager.py` - Lógica PowerShell

**Tempo total:** 1 hora de leitura + exploração do código

---

### 🔨 Quero Fazer o Build

**Preciso gerar o executável:**

1. ✅ [GUIA_DE_BUILD.md](GUIA_DE_BUILD.md) - Instruções detalhadas
2. 🔧 Execute: `python build_exe.py`
3. 📦 Output: `dist/MeninoDeTIHelper.exe`

**Tempo total:** 15 minutos de leitura + 5 minutos de build

---

### 🐛 Tenho um Problema

**Encontrei um erro:**

1. ✅ [README_V2.md](README_V2.md) - Seção "Solução de Problemas"
2. 🔍 Verifique: Logs gerados (`menino_ti_helper_*.log`)
3. 📋 Abra: Issue no GitHub com detalhes

---

## 📖 Documentação por Tópico

### 🎨 Interface Gráfica

**Arquivos Relevantes:**
- `main_gui.py` (linhas 1-900)
- [PASSO_A_PASSO.md](PASSO_A_PASSO.md) - Passo 1

**Classes:**
- `MeninoDeTIHelperGUI` - Interface principal
- `ProgressWindow` - Janela de progresso
- `AdminWarningDialog` - Diálogo de admin

---

### 📊 Sistema de Progresso

**Arquivos Relevantes:**
- `main_gui.py` (classe `ProgressWindow`)
- [PASSO_A_PASSO.md](PASSO_A_PASSO.md) - Passo 3

**Métodos:**
- `update_progress()` - Atualiza barra
- `_update_apps_with_progress()` - Progresso de apps
- `_update_windows_with_progress()` - Progresso do Windows

---

### 🔐 Privilégios Administrativos

**Arquivos Relevantes:**
- `main_gui.py` (função `is_admin()`)
- `build_exe.py` (flag `--uac-admin`)
- [PASSO_A_PASSO.md](PASSO_A_PASSO.md) - Passo 2

**Como Funciona:**
1. Runtime: `ctypes.windll.shell32.IsUserAnAdmin()`
2. Executável: Manifesto UAC embutido
3. Diálogo: Orientação educativa

---

### 📦 Atualização de Aplicativos

**Arquivos Relevantes:**
- `powershell_manager.py` - Métodos:
  - `list_upgradable_apps()`
  - `update_app_silent()`
- [PASSO_A_PASSO.md](PASSO_A_PASSO.md) - Passo 4

**Comandos PowerShell:**
```powershell
winget upgrade --all --silent --accept-source-agreements --accept-package-agreements
```

---

### 🪟 Windows Update

**Arquivos Relevantes:**
- `powershell_manager.py` - Métodos:
  - `install_pswindowsupdate_module()`
  - `run_windows_update_with_progress()`
- [PASSO_A_PASSO.md](PASSO_A_PASSO.md) - Passo 5

**Módulo PowerShell:**
- PSWindowsUpdate (instalado automaticamente)

---

### 🏗️ Build do Executável

**Arquivos Relevantes:**
- `build_exe.py` - Script completo
- [GUIA_DE_BUILD.md](GUIA_DE_BUILD.md) - Instruções detalhadas

**Ferramenta:**
- PyInstaller 6.3.0

**Flags Importantes:**
```
--onefile       : Arquivo único
--windowed      : Sem console
--uac-admin     : Solicita admin
```

---

## 🔍 Busca Rápida

### Encontrar Informações Sobre...

| Tópico | Onde Encontrar |
|--------|----------------|
| Como instalar | [README_V2.md](README_V2.md) → Instalação |
| Como executar como admin | [README_V2.md](README_V2.md) → Execução como Administrador |
| Como gerar .exe | [GUIA_DE_BUILD.md](GUIA_DE_BUILD.md) |
| Arquitetura do código | [PASSO_A_PASSO.md](PASSO_A_PASSO.md) |
| Solução de problemas | [README_V2.md](README_V2.md) → Solução de Problemas |
| Progresso 0-100% | [PASSO_A_PASSO.md](PASSO_A_PASSO.md) → Passo 3 |
| Atualizações silenciosas | [PASSO_A_PASSO.md](PASSO_A_PASSO.md) → Passo 4 |
| Windows Update | [PASSO_A_PASSO.md](PASSO_A_PASSO.md) → Passo 5 |
| Verificação de admin | [PASSO_A_PASSO.md](PASSO_A_PASSO.md) → Passo 1, 2 |
| Fluxo completo | [RESUMO_IMPLEMENTACAO.md](RESUMO_IMPLEMENTACAO.md) |

---

## 📊 Estatísticas da Documentação

### Volume de Conteúdo

| Categoria | Arquivos | Linhas Aprox. |
|-----------|----------|---------------|
| Código Python | 3 | 2.000 |
| Documentação | 7 | 5.000 |
| Scripts Auxiliares | 4 | 200 |
| **TOTAL** | **14** | **7.200** |

### Tempo de Leitura Estimado

| Perfil | Documentos | Tempo |
|--------|-----------|-------|
| Usuário Final | 2 docs | 20 min |
| Desenvolvedor | 4 docs | 60 min |
| Build/Deploy | 1 doc | 15 min |

---

## 🗺️ Mapa de Navegação

```
📁 meninodati/
│
├── 🚀 COMEÇAR AQUI
│   ├── INICIO_RAPIDO.md          ← Leia primeiro (5 min)
│   └── README_V2.md              ← Leia segundo (15 min)
│
├── 💻 EXECUTAR PROGRAMA
│   ├── main_gui.py               ← Execute este (v2.0)
│   ├── requirements.txt          ← Instale dependências
│   └── powershell_manager.py     ← Usado internamente
│
├── 🔨 FAZER BUILD
│   ├── GUIA_DE_BUILD.md          ← Leia antes de buildar
│   └── build_exe.py              ← Execute para gerar .exe
│
├── 📚 DOCUMENTAÇÃO TÉCNICA
│   ├── PASSO_A_PASSO.md          ← Arquitetura completa
│   ├── RESUMO_IMPLEMENTACAO.md   ← Resumo executivo
│   └── GUIA_DE_USO.md            ← Guia original
│
├── 📋 REFERÊNCIA
│   ├── INDEX.md                  ← Este arquivo (índice)
│   ├── README.md                 ← README original
│   └── LICENSE                   ← Licença MIT
│
└── 🛠️ SCRIPTS AUXILIARES
    ├── run.bat
    ├── run_admin.bat
    ├── run.ps1
    └── test_setup.py
```

---

## ✅ Checklist de Primeiro Uso

### Para Usuários

- [ ] Li o [INICIO_RAPIDO.md](INICIO_RAPIDO.md)
- [ ] Baixei o `MeninoDeTIHelper.exe`
- [ ] Executei como Administrador
- [ ] Programa abriu corretamente
- [ ] Interface está funcionando

### Para Desenvolvedores

- [ ] Clonei o repositório
- [ ] Li o [INICIO_RAPIDO.md](INICIO_RAPIDO.md)
- [ ] Instalei dependências (`pip install -r requirements.txt`)
- [ ] Executei `python main_gui.py`
- [ ] Li o [PASSO_A_PASSO.md](PASSO_A_PASSO.md)
- [ ] Entendi a arquitetura
- [ ] Fiz modificações de teste
- [ ] Gerei build com `python build_exe.py`
- [ ] Testei o executável

---

## 🆘 Precisa de Ajuda?

### Fluxograma de Suporte

```
Tenho uma dúvida
      ↓
      ├─ Sobre USO → Leia README_V2.md
      │
      ├─ Sobre CÓDIGO → Leia PASSO_A_PASSO.md
      │
      ├─ Sobre BUILD → Leia GUIA_DE_BUILD.md
      │
      ├─ Erro/Bug → Veja README_V2.md (Solução de Problemas)
      │            → Verifique os logs
      │            → Abra issue no GitHub
      │
      └─ Contribuir → Leia PASSO_A_PASSO.md
                    → Fork no GitHub
                    → Envie Pull Request
```

---

## 🎯 Objetivos de Cada Documento

### INICIO_RAPIDO.md
**Objetivo:** Fazer você usar/desenvolver em 5 minutos  
**Público:** Todos  
**Quando Ler:** Primeira vez usando o projeto

### README_V2.md
**Objetivo:** Manual completo do usuário  
**Público:** Usuários finais  
**Quando Ler:** Quer entender todas as funcionalidades

### PASSO_A_PASSO.md
**Objetivo:** Ensinar a arquitetura completa  
**Público:** Desenvolvedores  
**Quando Ler:** Quer modificar ou entender o código

### GUIA_DE_BUILD.md
**Objetivo:** Ensinar a gerar o executável  
**Público:** Desenvolvedores/Packagers  
**Quando Ler:** Precisa criar o .exe

### RESUMO_IMPLEMENTACAO.md
**Objetivo:** Visão geral do projeto  
**Público:** Todos  
**Quando Ler:** Quer entender o que foi feito

### GUIA_DE_USO.md
**Objetivo:** Guia original do projeto  
**Público:** Usuários  
**Quando Ler:** Referência histórica

---

## 📅 Histórico de Versões da Documentação

### v2.0 (2026-01-14) - Atual
- ✨ Criado INDEX.md (este arquivo)
- ✨ Criado INICIO_RAPIDO.md
- ✨ Criado PASSO_A_PASSO.md
- ✨ Criado GUIA_DE_BUILD.md
- ✨ Criado RESUMO_IMPLEMENTACAO.md
- ✨ Criado README_V2.md
- 🔄 Atualizado requirements.txt

### v1.0 (Versão Anterior)
- ✅ README.md original
- ✅ GUIA_DE_USO.md

---

## 🔗 Links Rápidos

### Documentação
- [📖 Manual Completo](README_V2.md)
- [🚀 Início Rápido](INICIO_RAPIDO.md)
- [👨‍💻 Guia de Desenvolvimento](PASSO_A_PASSO.md)
- [🔨 Guia de Build](GUIA_DE_BUILD.md)
- [📋 Resumo](RESUMO_IMPLEMENTACAO.md)

### Código
- [🎨 Interface Principal](main_gui.py)
- [⚙️ PowerShell Manager](powershell_manager.py)
- [🛠️ Build Script](build_exe.py)

### Outros
- [📄 Licença](LICENSE)
- [📖 README Original](README.md)
- [📘 Guia Original](GUIA_DE_USO.md)

---

## 💡 Dicas de Navegação

1. **Use Ctrl+F** para buscar termos específicos
2. **Links internos** te levam para outros documentos
3. **Comece sempre pelo INICIO_RAPIDO.md**
4. **Consulte este INDEX** quando estiver perdido

---

**📚 Este índice foi criado para facilitar sua navegação pelo projeto!**

---

**Última Atualização:** 14 de Janeiro de 2026  
**Versão:** 2.0  
**Autor:** exadmax

