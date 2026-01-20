# 🧹 Limpeza do Sistema - Documentação Completa

## 📋 Índice
1. [Visão Geral](#visão-geral)
2. [Como Usar](#como-usar)
3. [O que é Limpado](#o-que-é-limpado)
4. [Segurança](#segurança)
5. [Exemplos de Uso](#exemplos-de-uso)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

O **Sistema de Limpeza** é um componente do Menino da TI que libera espaço em disco removendo com segurança:
- **Cache** de navegadores e aplicativos
- **Arquivos temporários** do Windows
- **Lixeira** (Recycle Bin)

### ✨ Destaques
- ✅ **Seguro**: Apenas arquivos de cache são deletados
- ✅ **Seletivo**: Escolha o que limpar
- ✅ **Informativo**: Mostra tamanho que será liberado
- ✅ **Rápido**: Otimizado para melhor performance
- ✅ **Amigável**: Interface visual clara

---

## 🚀 Como Usar

### Opção 1: Via Interface Principal (Recomendado)

1. Abra **main_gui.py** ou execute **run.bat**
2. Clique no botão **🧹 Limpeza do Sistema**
3. Selecione os itens a limpar
4. Clique em **▶️ Iniciar Limpeza**
5. Aguarde a conclusão

### Opção 2: Atalho Direto

1. Execute **cleanup_system.bat** na pasta do projeto
2. O diálogo de limpeza se abrirá
3. Proceda com a limpeza

### Opção 3: Linha de Comando

```bash
python gui_cleanup_dialog.py
```

### Opção 4: Programaticamente (Python)

```python
from cleanup_manager import cleanup_all_safe

def progress_callback(message, progress):
    print(f"[{progress}%] {message}")

results = cleanup_all_safe(callback=progress_callback)

print(f"Arquivos deletados: {results['summary']['total_files']}")
print(f"Espaço liberado: {results['summary']['total_bytes']} bytes")
```

---

## 📦 O que é Limpado

### 🗂️ Cache (Pasta de Cache)

Localização: `C:\Users\[USERNAME]\AppData\Local\Cache` e variações

**Incluem:**
- Cache de navegadores:
  - Google Chrome
  - Mozilla Firefox
  - Microsoft Edge
- Cache de aplicativos Windows
- Cache de Windows Update
- Cache de Windows Error Reporting

**Tamanho típico liberado:** 500 MB - 5 GB

### 📁 Arquivos Temporários

Localização: `%TEMP%` (geralmente `C:\Users\[USERNAME]\AppData\Local\Temp`)

**Incluem:**
- Arquivos temporários de instaladores
- Arquivos temporários de aplicativos
- Arquivos de sessão quebrada
- Logs de erro antigos

**Tamanho típico liberado:** 100 MB - 2 GB

### 🗑️ Lixeira (Recycle Bin)

Localização: Recycle Bin do Windows (todos os drives)

**Incluem:**
- Arquivos deletados pelos usuários
- Arquivos de programa desinstalados

**Tamanho típico liberado:** 0 - 10 GB (depende do usuário)

---

## 🔒 Segurança

### O que NÃO é Afetado

- ❌ Arquivos de Documentos do usuário
- ❌ Pastas do Desktop
- ❌ Pastas de Download
- ❌ Pastas de Projetos
- ❌ Arquivos do sistema críticos
- ❌ Banco de dados de aplicativos

### Mecanismos de Segurança

1. **Seleção de Pasta Restrita**
   - Apenas pastas conhecidas de cache/temp
   - Validação de caminho antes de deletar
   - Recusa de deletar pastas críticas

2. **Deleção Gradual**
   - Arquivo por arquivo
   - Tratamento de erro individual
   - Continuação mesmo com erros

3. **Permissões Preservadas**
   - Pasta não é deletada, apenas conteúdo
   - Estrutura de diretório mantida
   - Permissões do usuário respeitadas

4. **Log de Operações**
   - Cada ação é registrada
   - Erros são documentados
   - Relatório final disponível

### Como Aumentar Segurança

1. **Fazer backup** (opcional mas recomendado)
2. **Executar teste** com uma opção por vez
3. **Verificar resultados** antes de executar tudo

---

## 📊 Exemplos de Uso

### Exemplo 1: Limpeza Rápida (Apenas Cache)

```
1. Abra cleanup_system.bat
2. Desmarque "Arquivos Temporários"
3. Desmarque "Lixeira"
4. Clique "Iniciar Limpeza"
```

**Tempo esperado:** 2-5 minutos
**Espaço liberado:** 500 MB - 2 GB

### Exemplo 2: Limpeza Completa (Tudo)

```
1. Abra a interface principal (run.bat)
2. Clique "Limpeza do Sistema"
3. Mantenha todas as opções marcadas
4. Clique "Iniciar Limpeza"
```

**Tempo esperado:** 5-15 minutos
**Espaço liberado:** 1 GB - 15 GB

### Exemplo 3: Liberar Espaço Urgentemente

```
1. Execute cleanup_system.bat
2. Selecione apenas "Lixeira"
3. Clique "Iniciar Limpeza"
4. Se necessário, repita com "Cache"
```

**Tempo esperado:** 1-3 minutos
**Espaço liberado:** Imediato (da lixeira)

---

## 📋 Arquivos do Sistema

### Módulos Criados

#### `cleanup_manager.py` (450+ linhas)
**Classe principal:** `CleanupManager`

**Métodos principais:**
- `clean_cache()` - Limpa caches
- `clean_temp_files()` - Limpa temporários
- `empty_recycle_bin()` - Esvazia lixeira
- `cleanup_all()` - Limpeza completa
- `get_cleanup_info()` - Informações sobre o que será limpo

**Recursos:**
- Callback de progresso (0-100%)
- Tratamento seguro de erros
- Logging detalhado
- Formatação de tamanhos (B, KB, MB, GB)

#### `gui_cleanup_dialog.py` (500+ linhas)
**Classe principal:** `CleanupDialog`

**Componentes:**
- Seletor de opções (checkboxes)
- Barra de progresso animada
- Log em tempo real
- Botões de controle
- Informações pré-limpeza

**Recursos:**
- Threading para não congelar UI
- Callbacks de progresso
- Previsão de tamanho
- Log colorido com códigos de status

### Scripts

#### `cleanup_system.bat`
Atalho para abrir o diálogo de limpeza diretamente.

**Uso:**
```bash
cleanup_system.bat
```

---

## ⚙️ Configuração Avançada

### Personalizar Pastas de Cache

Editar `cleanup_manager.py`, método `get_cache_folders()`:

```python
cache_paths = [
    # Suas pastas personalizadas aqui
    "C:\\Users\\usuario\\AppData\\Local\\Minha App\\Cache",
]
```

### Desabilitar Limpeza de Lixeira

Se não quer esvaziar a lixeira, remover callback em `gui_cleanup_dialog.py`:

```python
# Comentar ou remover esta seção
if "recycle" in cleanup_options:
    self.add_log_message("Esvaziando lixeira...", "INFO")
    results['recycle'] = self.cleanup_manager.empty_recycle_bin()
```

### Ajustar Tamanho de Log

Editar `gui_cleanup_dialog.py`, método `setup_ui()`:

```python
self.log_text = tk.Text(
    log_frame,
    height=12,  # Aumentado de 8
    font=("Courier", 8),
    yscrollcommand=scrollbar.set
)
```

---

## 🔍 Troubleshooting

### Problema: "Erro ao esvaziar lixeira"

**Causa:** Permissões insuficientes

**Solução:**
1. Execute com privilégios de administrador
2. Feche todos os aplicativos
3. Reinicie o Windows
4. Tente novamente

### Problema: "Nenhum arquivo foi deletado"

**Causa 1:** Cache já limpo recentemente

**Solução:** Espere algumas horas e tente novamente

**Causa 2:** Pastas protegidas ou em uso

**Solução:** Feche aplicativos abertos (navegadores, etc.)

### Problema: "Progresso não avança"

**Causa:** Pasta com muitos arquivos pequenos

**Solução:** Aguarde pacientemente (pode levar alguns minutos)

### Problema: "Erro de permissão ao deletar X"

**Causa:** Arquivo em uso ou protegido

**Solução:** 
- Feche o aplicativo que usa o arquivo
- Execute como administrador
- Reinicie o Windows

### Problema: "Nenhuma pasta encontrada"

**Causa:** Sistema sem cache ou aplicativos

**Solução:** Normal em sistemas novos - continue com as outras opções

---

## 📈 Performance e Impacto

### Impacto no Sistema

| Aspecto | Antes | Depois |
|--------|-------|--------|
| Espaço em Disco | 100% | +5-15% |
| Velocidade Inicialização | Lenta | Normal |
| Cache Navegador | Cheio | Vazio |
| Temp Folder | Completo | Limpo |

### Tempo de Limpeza

| Tipo | Tempo |
|------|-------|
| Cache Apenas | 2-5 min |
| Temp Apenas | 1-3 min |
| Lixeira | < 1 min |
| Completo | 5-15 min |

### Espaço Liberado (Típico)

| Sistema | Liberado |
|---------|----------|
| Novo | 100 MB - 500 MB |
| 6 meses | 1 GB - 3 GB |
| 1 ano | 3 GB - 10 GB |
| Muito usado | 10 GB + |

---

## 🔧 Opções Avançadas

### Executar Limpeza via PowerShell

```powershell
# Abrir interface
python gui_cleanup_dialog.py

# Ou executar via PowerShell diretamente
python cleanup_manager.py
```

### Integração em Script

```python
from cleanup_manager import CleanupManager

manager = CleanupManager()

# Obter informações antes de limpar
info = manager.get_cleanup_info()
print(f"Cache: {info['cache_size']} bytes")
print(f"Temp: {info['temp_size']} bytes")

# Executar limpeza
results = manager.cleanup_all()
```

---

## 📚 Referência Rápida

| Ação | Comando |
|------|---------|
| Abrir limpeza | `cleanup_system.bat` |
| Abrir GUI | `python gui_cleanup_dialog.py` |
| Executar direto | `python cleanup_manager.py` |
| Informações | `python -c "from cleanup_manager import get_cleanup_info; print(get_cleanup_info())"` |

---

## ❓ FAQ

**P: É seguro usar?**
R: Sim, apenas arquivos de cache são deletados. Nenhum arquivo de usuário é afetado.

**P: Preciso de administrador?**
R: Para lixeira, sim. Para cache/temp, não obrigatório mas recomendado.

**P: Quanto espaço vou liberar?**
R: Depende do uso. Típicamente 1-5 GB, mas pode variar.

**P: Meus aplicativos vão funcionar?**
R: Sim. Apenas cache é deletado; aplicativos funcionam normalmente.

**P: Posso cancelar durante a limpeza?**
R: Sim, clique "Fechar". Arquivos já deletados permanecerão deletados.

**P: Com que frequência devo limpar?**
R: Mensalmente é recomendado. Semanalmente se espaço for crítico.

**P: Vai melhorar meu PC?**
R: Vai liberar espaço. Performance depende de outros fatores.

**P: E se algo der errado?**
R: Os erros são registrados e você pode tentar novamente depois.

---

## 📞 Suporte

Se encontrar problemas:

1. Verifique [Troubleshooting](#troubleshooting)
2. Leia [FAQ](#faq)
3. Execute como administrador
4. Reinicie e tente novamente
5. Verifique permissões de pasta

---

## 📝 Notas de Versão

### v1.0 (19/01/2026)
- ✅ Limpeza de cache
- ✅ Limpeza de temporários
- ✅ Esvaziamento de lixeira
- ✅ Interface gráfica completa
- ✅ Logging detalhado
- ✅ Tratamento seguro de erros

---

## 📄 Licença

Este componente faz parte do Menino da TI e segue a mesma licença.

---

**Versão:** 1.0  
**Última Atualização:** 19 de janeiro de 2026  
**Status:** ✅ COMPLETO E DOCUMENTADO
