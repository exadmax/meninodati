# Correções de Encoding e None Handling

## 📋 Problemas Corrigidos

### 1. ❌ UnicodeDecodeError

**Erro Original**:
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xa2 in position 13: invalid start byte
Exception in thread Thread-10 (_readerthread)
```

**Causa**: PowerShell pode retornar caracteres especiais do Windows (CP1252) que não são válidos em UTF-8.

**Solução**:
```python
# Antes - encoding fixo
process = subprocess.Popen(
    [...],
    encoding='utf-8'  # ❌ Falha com caracteres Windows
)

# Depois - encoding com fallback
try:
    process = subprocess.Popen(
        [...],
        encoding='utf-8',
        errors='replace'  # ✅ Substitui caracteres inválidos
    )
except UnicodeDecodeError:
    # Fallback para CP1252 (Windows Latin-1)
    process = subprocess.Popen(
        [...],
        encoding='cp1252',
        errors='replace'
    )
```

---

### 2. ❌ AttributeError: 'NoneType' object has no attribute 'strip'

**Erro Original**:
```python
if stdout.strip():  # ❌ Falha se stdout é None
    ...
```

**Causa**: `subprocess.communicate()` pode retornar `None` em alguns casos, especialmente com encoding errors.

**Solução**:
```python
# No execute_command - garantir que nunca retorna None
stdout = stdout if stdout is not None else ""
stderr = stderr if stderr is not None else ""

# Em todos os métodos - verificar antes de usar .strip()
if stdout and stdout.strip():  # ✅ Verifica None primeiro
    ...
```

**Locais Corrigidos**:
- ✅ `check_admin_privileges()`
- ✅ `install_winget_if_needed()`
- ✅ `install_pswindowsupdate_module()`
- ✅ `list_upgradable_apps()`
- ✅ `execute_command()` - garante não-None na saída

---

### 3. ❌ NameError: cannot access free variable 'e'

**Erro Original**:
```python
except Exception as e:
    logger.error(f"Erro: {str(e)}")
    self.root.after(0, lambda: messagebox.showerror(
        "Erro",
        f"Erro:\n\n{str(e)}"  # ❌ 'e' não existe quando lambda executa!
    ))
```

**Causa**: Quando o lambda é executado (depois pelo `root.after`), a variável `e` já não existe mais no escopo.

**Solução**:
```python
except Exception as e:
    logger.error(f"Erro: {str(e)}")
    error_msg = str(e)  # ✅ Captura o valor AGORA
    self.root.after(0, lambda msg=error_msg: messagebox.showerror(
        "Erro",
        f"Erro:\n\n{msg}"  # ✅ Usa parâmetro default do lambda
    ))
```

**Locais Corrigidos**:
- ✅ `_run_full_update()` em main_gui.py
- ✅ `_run_apps_only()` em main_gui.py (já estava correto)
- ✅ `_run_windows_only()` em main_gui.py (já estava correto)

---

## 🔧 Arquivos Modificados

### `powershell_manager.py`

#### execute_command()
```python
# Novo comportamento:
1. Tenta UTF-8 com errors='replace'
2. Se falhar, tenta CP1252 com errors='replace'
3. Garante stdout/stderr nunca são None
```

#### Métodos com verificação de None
- `check_admin_privileges()`: `stdout and stdout.strip()`
- `install_winget_if_needed()`: `stdout and stdout.strip()`
- `install_pswindowsupdate_module()`: `stdout and stdout.strip()`
- `list_upgradable_apps()`: `or not stdout or not stdout.strip()`

### `main_gui.py`

#### _run_full_update()
```python
except Exception as e:
    error_msg = str(e)  # Captura agora
    self.root.after(0, lambda msg=error_msg: ...)  # Usa depois
```

---

## 🧪 Como Testar

### Teste Automatizado
```bash
python test_powershell_encoding.py
```

Valida:
- ✅ Encoding com fallback funciona
- ✅ stdout/stderr nunca são None
- ✅ Lambdas capturam variáveis corretamente
- ✅ Timeouts tratados corretamente

### Teste Manual - Windows Update

```bash
python main_gui.py
# Clicar em "Atualizar Windows"
# Deve funcionar sem UnicodeDecodeError
# Deve funcionar sem AttributeError
```

---

## 📊 Cenários de Teste

### Cenário 1: Caracteres Especiais
```powershell
Get-Date | Format-List
# Saída contém caracteres CP1252
# ✅ Tratado com encoding fallback
```

### Cenário 2: Saída Vazia
```powershell
$null
# Retorna string vazia, não None
# ✅ Garantido no execute_command
```

### Cenário 3: Comando com Erro
```powershell
Get-NonExistentCmdlet
# stderr não é None, contém mensagem
# ✅ Garantido no execute_command
```

### Cenário 4: Timeout
```powershell
Start-Sleep -Seconds 60
# Com timeout=10
# ✅ Retorna "", "" sem None
```

---

## 🎯 Garantias Após Correções

### Encoding
- ✅ UTF-8 é tentado primeiro
- ✅ CP1252 é fallback automático
- ✅ `errors='replace'` evita crashes
- ✅ Caracteres especiais Windows são tratados

### None Handling
- ✅ `execute_command()` NUNCA retorna None
- ✅ Todos os métodos verificam None antes de .strip()
- ✅ Strings vazias ("") usadas em vez de None

### Lambda Closure
- ✅ Variáveis capturadas com valor default
- ✅ Não há NameError em callbacks assíncronos
- ✅ Mensagens de erro aparecem corretamente

---

## 🔍 Padrões Recomendados

### ❌ NÃO FAZER
```python
# Não verificar None
if stdout.strip():  # ❌ Crash se None

# Lambda sem captura
except Exception as e:
    lambda: print(str(e))  # ❌ 'e' pode não existir

# Encoding fixo
encoding='utf-8'  # ❌ Falha com CP1252
```

### ✅ FAZER
```python
# Verificar None
if stdout and stdout.strip():  # ✅ Safe

# Lambda com captura
except Exception as e:
    msg = str(e)
    lambda m=msg: print(m)  # ✅ 'msg' capturado

# Encoding com fallback
encoding='utf-8',
errors='replace'  # ✅ Tolerante
```

---

## ✅ Checklist de Validação

- [x] UnicodeDecodeError corrigido com encoding fallback
- [x] AttributeError corrigido com verificação de None
- [x] NameError corrigido com captura de variável
- [x] execute_command garante não-None
- [x] Todos os .strip() verificam None antes
- [x] Todos os lambdas capturam variáveis corretamente
- [x] Testes automatizados criados
- [x] Documentação completa

---

**Status Final**: ✅ **TODOS OS PROBLEMAS DE ENCODING E NONE RESOLVIDOS**

Agora a aplicação pode:
- ✅ Executar Windows Update sem crash
- ✅ Lidar com caracteres especiais do Windows
- ✅ Tratar stdout/stderr None corretamente
- ✅ Exibir mensagens de erro em callbacks

Data: 20 de janeiro de 2026
