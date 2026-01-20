# MENINO DA TI - Verificação de Sistema - Quick Start

## 🚀 Começar Rapidamente

### 1. Verificar Compatibilidade do Sistema
```bash
python system_check.py
```

### 2. Executar Modo Console
```bash
python auto_launcher.py console
```

### 3. Executar Modo Gráfico
```bash
python auto_launcher.py gui
```

### 4. Executar com Seletor de Modo
```bash
python launcher.py
# ou
launcher.bat
```

---

## ✅ Checagem de Sistema - O que é Verificado?

| Item | Verificado | Requerimento |
|------|-----------|--------------|
| SO | ✓ | Windows 10+ |
| Versão Windows | ✓ | 10.0 ou superior |
| Build Windows | ✓ | Build 14393+ |
| Python | ✓ | 3.8+ |
| Arquitetura | ✓ | 32/64 bits |

---

## 📊 Saída da Verificação

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

---

## ❌ Se Receber Erro de Incompatibilidade

**Erro:** "Windows incompatível: Windows 7"

**Solução:**
1. Atualize para Windows 10 ou superior
2. Use Windows Update
3. Visite: https://www.microsoft.com/pt-br/windows/

---

## 🧪 Testar Verificação

```bash
python test_system_compatibility.py
```

**Resultado esperado:** 5/5 testes passarem

---

## 📚 Mais Informações

- **Documentação Completa:** [VERIFICACAO_SISTEMA.md](VERIFICACAO_SISTEMA.md)
- **Sumário de Implementação:** [VERIFICACAO_SUMARIO.md](VERIFICACAO_SUMARIO.md)
- **Inicialização:** [INICIALIZACAO.md](INICIALIZACAO.md)

---

## 🔧 Requisitos Mínimos

- ✅ **Windows 10** ou superior
- ✅ **Python 3.8+** (recomendado 3.10+)
- ✅ **64 bits** (recomendado)

---

## 📋 Arquivos Relacionados

| Arquivo | Descrição |
|---------|-----------|
| `system_check.py` | Módulo de verificação |
| `auto_launcher.py` | Launcher com verificação integrada |
| `launcher.py` | Seletor de modo com verificação |
| `test_system_compatibility.py` | Testes automatizados |
| `VERIFICACAO_SISTEMA.md` | Documentação completa |
| `VERIFICACAO_SUMARIO.md` | Sumário de implementação |

---

## 💡 Dicas

1. **Sempre execute com verificação:**
   - Use `auto_launcher.py` em vez de rodar diretamente

2. **Para debug:**
   ```bash
   python system_check.py
   ```

3. **Para Windows antigo:**
   - Atualize via Windows Update
   - Ou faça upgrade para Windows 10

---

## 📞 Suporte

Se encontrar problemas:

1. Execute: `python system_check.py`
2. Verifique a saída de compatibilidade
3. Consulte [VERIFICACAO_SISTEMA.md](VERIFICACAO_SISTEMA.md) para soluções

---

**Versão:** 1.0  
**Data:** 19 de janeiro de 2026  
**Status:** ✅ Completo e Testado
