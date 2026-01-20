# Correções de Parsing do Winget

## 📋 Problemas Identificados

### ❌ Erro: IDs Inválidos Sendo Parseados

**Sintoma**:
```
Updating application: 25.3.2
Updating application: Desktop  
Updating application: Client
Updating application: Acrobat
```

**Causa**:
O parsing antigo era muito simplista e assumia que a estrutura sempre seria:
```
Nome ID Versão Disponível
```

Mas na realidade, o formato do `winget upgrade` é:
```
Nome Completo do App    Package.ID.Format    Versão    Disponível    Source
```

O parser estava pegando partes aleatórias da linha como IDs (números de versão, palavras do nome, etc).

---

## ✅ Soluções Implementadas

### 1. Parser Melhorado com Regex

**Novo algoritmo de parsing**:

1. **Encontra cabeçalho e separador**: Localiza as linhas com "Name", "Id", "Version" e os traços separadores
2. **Usa regex para identificar IDs**: Procura padrões `Package.ID.Format` (contém ponto)
3. **Valida IDs**: Filtra IDs inválidos:
   - Deve ter pelo menos 4 caracteres
   - Deve conter pelo menos um ponto
   - Não pode ser apenas números (ex: "25.3.2")
   - Deve seguir o padrão `Vendor.Product`

**Código**:
```python
# Procurar por padrão de ID com pontos (ex: Microsoft.Edge)
match = re.search(r'(\S+\.\S+)', line)

if match:
    app_id = match.group(1)
    
    # Validar que é um ID real
    if len(app_id) > 3 and '.' in app_id and not app_id.replace('.', '').isdigit():
        # ID válido!
```

### 2. Método `update_app_silent` Melhorado

**Melhorias**:

- ✅ **Validação de ID** antes de tentar atualizar
- ✅ **Tentativa com `--exact`** primeiro (mais preciso)
- ✅ **Fallback sem `--exact`** se falhar
- ✅ **Tratamento de erros conhecidos**:
  - "No applicable update found" → Não é erro (já atualizado)
  - "No package found" → ID inválido
  - "installer failed" → Problema no instalador
- ✅ **Logs mais detalhados**

### 3. Novo Método: `update_apps_individually`

Atualiza apps um por um com progresso detalhado:

```python
successful, failed, failed_apps = ps_manager.update_apps_individually(progress_callback)

# Retorna:
# - successful: quantidade de sucesso
# - failed: quantidade de falhas  
# - failed_apps: lista com detalhes dos que falharam
```

**Vantagens**:
- 📊 Progresso detalhado
- 🎯 Identifica exatamente qual app falhou
- 🔄 Callback personalizado para UI
- 📝 Lista de apps com falha

### 4. Menu Console Atualizado

Agora oferece duas opções:

**Opção 1: Atualização Rápida**
```bash
winget upgrade --all --silent
```
- Mais rápido
- Atualiza tudo de uma vez
- Menos detalhes

**Opção 2: Atualização Detalhada**
```
[1/13] Atualizando: Microsoft Edge...
[1/13] ✓ Microsoft Edge - Atualizado com sucesso
[2/13] Atualizando: Google Chrome...
[2/13] ✓ Google Chrome - Atualizado com sucesso
...
```
- Progresso detalhado
- Identifica falhas específicas
- Resumo ao final

---

## 🧪 Como Testar

### Teste 1: Validar Parsing
```bash
python test_winget_parsing.py
```

Valida:
- ✅ Parser identifica IDs corretamente
- ✅ Filtra IDs inválidos
- ✅ Lista apps reais do sistema

### Teste 2: Modo Console
```bash
python auto_launcher.py console
# Escolher opção [2] Atualizar Aplicativos
# Escolher opção [2] Atualização Detalhada
```

Valida:
- ✅ IDs corretos sendo usados
- ✅ Progresso detalhado
- ✅ Resumo de sucesso/falha

### Teste 3: Modo GUI
```bash
python main_gui.py
# Clicar em "Atualizar Aplicativos"
```

Valida:
- ✅ Nenhum erro de ID inválido
- ✅ Apps atualizando corretamente

---

## 📊 Exemplos de IDs Válidos vs Inválidos

### ✅ IDs Válidos
```
Microsoft.Edge
Google.Chrome
Adobe.Acrobat.Reader.64-bit
Docker.DockerDesktop
Anysphere.Cursor
Discord.Discord
```

**Padrão**: `Vendor.Product[.Variant]`

### ❌ IDs Inválidos (Agora Filtrados)
```
25.3.2          ← Apenas versão
Desktop         ← Palavra solta
Client          ← Palavra solta
Acrobat         ← Parte do nome
```

---

## 🔧 Arquivos Modificados

### `powershell_manager.py`

1. **`list_upgradable_apps()`**
   - Parser com regex robusto
   - Validação de IDs
   - Suporte a JSON (futuro)

2. **`update_app_silent()`**
   - Validação de ID
   - Tentativa com --exact
   - Tratamento de erros conhecido

3. **`update_apps_individually()` (NOVO)**
   - Atualização com progresso
   - Callback personalizado
   - Estatísticas detalhadas

### `auto_launcher.py`

1. **`atualizar_aplicativos()`**
   - Menu com 2 opções
   - Atualização rápida ou detalhada
   - Resumo de resultados

---

## 🎯 Resultados Esperados

### Antes (Logs com Erro)
```
INFO - Updating application: 25.3.2
ERROR - Command failed with return code 1
WARNING - Failed to update 25.3.2

INFO - Updating application: Desktop
ERROR - Command failed with return code 1
WARNING - Failed to update Desktop
```

### Depois (Logs Corretos)
```
INFO - Updating application: Microsoft.Edge
INFO - Successfully updated: Microsoft.Edge

INFO - Updating application: Google.Chrome  
INFO - Successfully updated: Google.Chrome

INFO - Updating application: Adobe.Acrobat.Reader.64-bit
INFO - No update needed for Adobe.Acrobat.Reader.64-bit (already up to date)
```

---

## ✅ Checklist de Validação

- [x] Parser identifica IDs corretamente usando regex
- [x] IDs inválidos são filtrados
- [x] Método de atualização valida IDs antes de usar
- [x] Tentativa com --exact para maior precisão
- [x] Tratamento de erros conhecidos do winget
- [x] Menu console oferece 2 métodos (rápido/detalhado)
- [x] Progresso detalhado com callback
- [x] Resumo de sucesso/falha ao final
- [x] Testes automatizados criados
- [x] Documentação completa

---

## 🚀 Uso Recomendado

### Para Usuários Finais
Use **Atualização Rápida** (opção 1):
- Mais rápido
- Atualiza tudo de uma vez
- Ideal para uso regular

### Para Diagnóstico/Debug
Use **Atualização Detalhada** (opção 2):
- Vê exatamente o que está falhando
- Progresso app por app
- Identifica problemas específicos

---

**Status Final**: ✅ **PARSING DO WINGET CORRIGIDO**

Data: 20 de janeiro de 2026
