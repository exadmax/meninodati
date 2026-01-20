# Verificação de Compatibilidade do Sistema - MENINO DA TI

## Visão Geral

A aplicação MENINO DA TI agora inclui um sistema automático de verificação de compatibilidade que garante que o aplicativo funcione corretamente no seu sistema operacional.

## Requisitos Mínimos

### Sistema Operacional
- **Windows 10** ou superior (Windows 11 totalmente suportado)
- ❌ **NÃO suportado**: Windows 7, Windows 8, Windows 8.1, Windows Vista, Windows XP

### Versão do Python
- **Python 3.8** ou superior (recomendado 3.10+)
- 64 bits (recomendado)

### Dependências
- tkinter (incluído no Python)
- Pillow (para processamento de imagens)
- sys, platform (bibliotecas padrão)

## Como Funciona a Verificação

A verificação é automática e ocorre **antes** de qualquer interface ser mostrada. O sistema verifica:

1. **Sistema Operacional**: Detecta Windows, Linux ou macOS
2. **Versão do Windows**: Verifica se é Windows 10 ou superior
3. **Arquitetura**: Detecta se é 32 bits ou 64 bits
4. **Versão do Python**: Informa a versão do Python em execução

### Fluxo de Verificação

```
Iniciar Aplicação
        ↓
Verificar SO
        ↓
┌───────────────────────┐
│ É Windows 10/11?      │
└───┬───────────────┬───┘
    │ SIM           │ NÃO
    ↓               ↓
PROSSEGUIR      ERRO: Versão
                Incompatível
                    ↓
                SOLICITA ATUALIZAR
                    ↓
                ENCERRAR
```

## Informações Exibidas

Quando você executa a aplicação, verá uma tela como esta:

```
======================================================================
INFORMACOES DO SISTEMA
======================================================================
Sistema Operacional: Windows
Versao: 10.0.26200
Release: 11
Arquitetura: 64 bits
Python: 3.12.10

Windows:
  Release: Windows 11
  Versao: 10.0
  Build: 26200
======================================================================


======================================================================
VERIFICACAO DE COMPATIBILIDADE
======================================================================
[OK] COMPATIVEL

Windows compatível

======================================================================
```

## Mensagens de Erro Comuns

### ❌ "Windows incompatível: Windows 8.1"
```
Significa: Seu sistema está usando Windows 8.1 ou anterior

Solução: Atualize para Windows 10 ou superior
         - Visite: https://www.microsoft.com/pt-br/windows/
         - Ou use Windows Update
```

### ❌ "Windows incompatível: Windows 7"
```
Significa: Seu sistema está usando Windows 7

Solução: Atualize para Windows 10 ou superior
         - Windows 7 não é mais suportado
         - Use Windows Update para atualizar
```

### ❌ "Versão do Windows 10 muito antiga"
```
Significa: Seu Windows 10 é muito antigo

Solução: Execute Windows Update para atualizar
         - Ir para Configurações > Atualização e Segurança
         - Clicar em "Verificar atualizações"
```

## Como Verificar Sua Versão do Windows

### Método 1: Usando o Comando
```powershell
# Abra PowerShell como administrador e execute:
[System.Environment]::OSVersion.VersionString
```

### Método 2: Usando Configurações
1. Pressione `Windows + I` para abrir Configurações
2. Vá para: Sobre
3. Procure por "Versão do Windows"

### Método 3: Usando o Painel de Controle
1. Pressione `Windows + R`
2. Digite: `msinfo32.exe`
3. Procure por "Versão do S.O."

## Como Atualizar o Windows

### Para Windows 8.1 → Windows 10
1. Visite: https://www.microsoft.com/pt-br/windows/windows-10-upgrade
2. Baixe o "Windows 10 Installation Media"
3. Siga as instruções de instalação

### Para Windows 10 → Windows 11
1. Verifique compatibilidade em: https://www.microsoft.com/pt-br/windows/windows-11-upgrade
2. Vá para Configurações > Atualização e Segurança
3. Clique em "Verificar atualizações"

### Atualizações de Build do Windows 10
1. Pressione `Windows + I`
2. Vá para: Atualização e Segurança
3. Clique em "Verificar atualizações"
4. Reinicie se necessário

## Testando a Verificação

Execute diretamente o módulo de verificação:

```bash
python system_check.py
```

Você verá:
- Informações completas do seu sistema
- Status de compatibilidade
- Recomendações se houver problemas

## Código de Verificação

O módulo `system_check.py` fornece a classe `SystemChecker` que pode ser importada:

```python
from system_check import SystemChecker

# Criar verificador
checker = SystemChecker()

# Verificar compatibilidade
is_compatible, message = checker.is_compatible()

if not is_compatible:
    print(f"Erro: {message}")
else:
    print("Sistema compatível!")

# Obter informações detalhadas
info = checker.get_system_info()
print(f"Windows Version: {info['windows_release']}")
print(f"Build: {info['windows_build']}")
print(f"Arquitetura: {info['arquitetura_bits']} bits")
```

## Compatibilidade Por Versão do Windows

| Versão | Suporte | Status |
|--------|---------|--------|
| Windows 11 | ✅ | Totalmente Suportado |
| Windows 10 | ✅ | Totalmente Suportado |
| Windows 8.1 | ❌ | Não Suportado |
| Windows 8 | ❌ | Não Suportado |
| Windows 7 | ❌ | Não Suportado |
| Windows Vista | ❌ | Não Suportado |
| Windows XP | ❌ | Não Suportado |

## FAQ

**P: Posso usar em Windows 7?**
R: Não, a aplicação requer Windows 10 ou superior.

**P: Meu Windows 10 é antigo, preciso atualizar?**
R: Sim, execute Windows Update para atualizar para a versão mais recente.

**P: A aplicação funciona em Linux?**
R: Parcialmente. O módulo está preparado para Linux, mas atualmente é otimizado para Windows.

**P: Posso executar em máquina virtual?**
R: Sim, desde que esteja em Windows 10 ou superior.

**P: O que fazer se a verificação falhar?**
R: Atualize seu Windows para Windows 10 ou superior usando Windows Update.

---

**Versão**: 1.0  
**Data**: 19 de janeiro de 2026  
**Criador**: MENINO DA TI - Sistema de Verificação
