# 🔧 Instalador PowerShell - Guia Completo

## 📋 Visão Geral

O **Instalador PowerShell** é uma ferramenta gráfica que:
- ✅ Verifica se Python está instalado
- ✅ Instala Python automaticamente via winget (se necessário)
- ✅ Instala pacotes necessários (Pillow, requests)
- ✅ Executa a aplicação automaticamente

## 🚀 Como Usar

### Opção 1: Duplo-Clique (Recomendado)
```bash
install.bat
```
Simplesmente duplo-clique no arquivo e deixe o instalador fazer o trabalho.

### Opção 2: PowerShell Direto
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
.\installer.ps1
```

### Opção 3: Com Privilégios de Admin
```powershell
# Execute como administrador no PowerShell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
.\installer.ps1
```

## 🎯 O Que Ele Faz

### Passo 1: Verificação do Sistema
- Verifica se Python está instalado
- Obtém a versão do Python
- Valida privilégios administrativos

### Passo 2: Instalação de Python (se necessário)
- Usa `winget install Python.Python.3.12`
- Baixa a versão mais recente
- Instala automaticamente

### Passo 3: Atualização do Pip
```bash
python -m pip install --upgrade pip
```

### Passo 4: Instalação de Pacotes
- Pillow (processamento de imagens)
- requests (requisições HTTP)

### Passo 5: Execução da Aplicação
- Procura por `main_gui.py`, `auto_launcher.py` ou `main.py`
- Executa automaticamente

## 🖥️ Interface Gráfica

```
┌─────────────────────────────────────────────┐
│ 🔧 MENINO DA TI - Instalador                │
│ Assistente de Instalação                    │
├─────────────────────────────────────────────┤
│ Status: Inicializando...                    │
│                                             │
│ ═══════════════════════════════════════════ │
│ [Log box com mensagens de instalação]       │
│                                             │
│ ═══════════════════════════════════════════ │
│                                             │
│ [████████░░░░░░░░░░░░░░░░░░░░░░░░] 35%    │
│                                             │
│ ▶ Iniciar Instalação    ✖ Cancelar         │
└─────────────────────────────────────────────┘
```

### Componentes da Interface

1. **Título**: "🔧 MENINO DA TI"
2. **Subtítulo**: "Assistente de Instalação"
3. **Status**: Mostra o progresso atual
4. **Log Box**: Mostra todas as operações em tempo real
5. **Barra de Progresso**: Visualização de progresso (0-100%)
6. **Botões**: Iniciar e Cancelar

## 📊 Fluxo de Instalação

```
Iniciar
  ↓
Verificar Python
  ├─ Encontrado → Continuar
  └─ Não encontrado → Instalar via winget
  ↓
Atualizar Pip
  ↓
Instalar Pacotes (Pillow, requests)
  ↓
Concluído ✓
  ↓
Executar Aplicação
```

## ⚙️ Requisitos do Sistema

### Mínimo
- Windows 10 ou superior
- PowerShell 5.0+
- Conexão com internet

### Recomendado
- Windows 11
- Privilégios de administrador
- 500 MB de espaço livre em disco
- Conexão de internet estável

## 🔐 Segurança

### O Instalador Faz:
✅ Verifica privilégios
✅ Valida arquivos
✅ Log de todas as operações
✅ Tratamento de erros
✅ Não modifica sistema além do necessário

### O Instalador NÃO Faz:
❌ Não acessa dados pessoais
❌ Não modifica configurações do sistema
❌ Não instala software desnecessário
❌ Não coleta informações

## 🆘 Troubleshooting

### Problema: "PowerShell não está instalado"
**Solução:**
1. Instale PowerShell 5.0+ de: https://github.com/PowerShell/PowerShell
2. Execute novamente

### Problema: "Erro ao executar script"
**Solução:**
1. Execute como administrador
2. Use `Set-ExecutionPolicy -ExecutionPolicy Bypass`
3. Verifique se o arquivo não está corrompido

### Problema: "Python não instala via winget"
**Solução:**
1. Instale Python manualmente de: https://www.python.org/downloads/
2. Coloque na pasta do projeto
3. Execute novamente

### Problema: "Pacotes não instalam"
**Solução:**
1. Verifique conexão com internet
2. Execute como administrador
3. Tente `pip install pillow requests` manualmente

### Problema: "Aplicação não encontrada"
**Solução:**
1. Verifique se `main_gui.py` ou `main.py` existem
2. Mova-os para o mesmo diretório do instalador
3. Execute novamente

## 📋 Opções Avançadas

### Instalar Versão Específica do Python

Editar `installer.ps1`:

```powershell
# Procure por esta linha:
winget install -e --id Python.Python.3.12

# E altere para (exemplo: Python 3.11):
winget install -e --id Python.Python.3.11
```

### Adicionar Pacotes Extras

No array `$REQUIRED_PACKAGES`:

```powershell
$REQUIRED_PACKAGES = @(
    "requests",
    "pillow",
    "numpy",      # Adicionar
    "pandas"      # Adicionar
)
```

### Personalizar Interface

Alterar tamanho da janela:

```powershell
$form.Width = 600   # Largura em pixels
$form.Height = 550  # Altura em pixels
```

## 📈 Monitoramento

### Log Console

Durante a instalação, você verá:

```
[14:30:45] ═══════════════════════════════════════════════════════
[14:30:45] INSTALADOR - MENINO DA TI
[14:30:45] ═══════════════════════════════════════════════════════
[14:30:45]
[14:30:45] [1/5] Verificando Python...
[14:30:46] ✓ Python já está instalado (versão: 3.12.1)
[14:30:46]
[14:30:46] [2/5] Atualizando pip...
[14:30:52] ✓ Pip atualizado
[14:30:52]
[14:30:52] [3/5] Instalando pacotes necessários...
[14:30:55] ✓ requests instalado com sucesso
[14:30:58] ✓ pillow instalado com sucesso
```

## 🔄 Atualizações

### Verificar Atualizações do Instalador

```powershell
git pull  # Se estiver usando Git
```

### Versão Atual

Editar `installer.ps1`:

```powershell
$INSTALLER_VERSION = "1.0"
```

## 📞 Suporte

### Se Algo Não Funcionar:

1. **Verifique requisitos**
   - Windows 10+
   - PowerShell 5.0+
   - Conexão com internet

2. **Tente como admin**
   - Clique direito em `install.bat`
   - Selecione "Executar como administrador"

3. **Verifique conexão**
   - Teste internet
   - Tente ping google.com

4. **Limpe e reinstale**
   - Desinstale Python manualmente
   - Execute novamente

## 🎓 Exemplos

### Exemplo 1: Instalação Limpa
```
1. Duplo-clique em install.bat
2. Aguarde conclusão
3. Aplicação abre automaticamente
```

### Exemplo 2: Atualizar Pacotes
```powershell
pip install --upgrade pillow requests
```

### Exemplo 3: Verificar Instalação
```powershell
python --version
pip show pillow
pip show requests
```

## 📊 Estatísticas

### Tamanho
- Código PowerShell: ~400 linhas
- Script Batch: ~35 linhas
- Documentação: ~400 linhas

### Tempo de Execução
- Verificação: < 1 segundo
- Instalação Python: 2-5 minutos
- Instalação de pacotes: 1-3 minutos
- **Total: 3-8 minutos** (primeira execução)

### Tempo de Execução (Subsequente)
- Verificação: < 1 segundo
- Instalação de pacotes: 10-30 segundos
- **Total: <1 minuto**

## 🚀 Performance

### Otimizações Implementadas
- ✅ Verifica antes de instalar
- ✅ Usa flags silenciosas (`-q`)
- ✅ Log em tempo real
- ✅ Threading para UI responsiva
- ✅ Atualização dinâmica de progresso

## 📝 Notas de Versão

### v1.0 (19/01/2026)
- ✅ Interface gráfica Windows Forms
- ✅ Verificação de Python
- ✅ Instalação via winget
- ✅ Instalação de pacotes
- ✅ Log em tempo real
- ✅ Barra de progresso
- ✅ Execução automática da app
- ✅ Tratamento completo de erros

## 📄 Licença

Este instalador faz parte do Menino da TI e segue a mesma licença.

---

**Versão:** 1.0  
**Data:** 19 de janeiro de 2026  
**Status:** ✅ COMPLETO E TESTADO  
**Suporte:** Documentação Completa

---

## 🎉 Resumo

O instalador PowerShell torna extremamente fácil instalar e executar o MENINO DA TI:

1. **Baixe** `install.bat`
2. **Duplo-clique** para executar
3. **Aguarde** a conclusão
4. **Pronto!** Aplicação funciona

Simples assim! 🚀
