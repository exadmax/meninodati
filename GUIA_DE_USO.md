# 📖 Guia de Uso - Menino de TI Helper

## 🎯 Objetivo

Este guia fornece instruções detalhadas sobre como usar o **Menino de TI Helper** para manter seu Windows 11 sempre atualizado.

## 🚀 Iniciando o Aplicativo

### Método 1: Script Batch (Recomendado para Iniciantes)

1. **Execução Normal**:
   - Dê duplo clique no arquivo `run.bat`
   - O aplicativo será iniciado

2. **Execução como Administrador** (Recomendado):
   - Clique com o botão direito em `run_admin.bat`
   - Selecione "Executar como administrador"
   - Confirme na janela de UAC (Controle de Conta de Usuário)

### Método 2: Script PowerShell

1. Abra o PowerShell como Administrador
2. Navegue até a pasta do projeto:
   ```powershell
   cd C:\caminho\para\meninodati
   ```
3. Execute o script:
   ```powershell
   .\run.ps1
   ```

### Método 3: Python Direto

1. Abra o PowerShell ou CMD como Administrador
2. Navegue até a pasta do projeto
3. Execute:
   ```bash
   python main.py
   ```

## 🖥️ Interface do Usuário

### Tela de Abertura
Ao iniciar, você verá uma tela de splash com:
- Logo "🔧 Menino de TI Helper 🔧"
- Mensagem de carregamento
- Barra de progresso

### Tela Principal

A interface principal contém:

1. **Título**: Nome do aplicativo
2. **Três Botões de Ação**:
   - ▶ **Atualizar Tudo**: Atualiza aplicativos E Windows
   - 📦 **Atualizar Apenas Aplicativos**: Usa winget para atualizar apps
   - 🪟 **Atualizar Apenas Windows**: Executa Windows Update
3. **Área de Progresso**: Mostra logs em tempo real
4. **Barra de Status**: Estado atual da operação

## 📋 Como Usar Cada Função

### 1. Atualizar Tudo (Recomendado)

**Quando usar**: Para manutenção completa do sistema

**Passos**:
1. Clique em "▶ Atualizar Tudo"
2. Leia a confirmação e clique em "Sim"
3. Aguarde o processo (pode levar 30-60 minutos)
4. Acompanhe o progresso na área de log

**O que acontece**:
- Primeiro: Atualiza todos os aplicativos com winget
- Depois: Executa Windows Update completo
- Ao final: Mostra mensagem de conclusão

### 2. Atualizar Apenas Aplicativos

**Quando usar**: Para atualizar rapidamente seus programas instalados

**Passos**:
1. Clique em "📦 Atualizar Apenas Aplicativos"
2. Confirme a operação
3. Aguarde (normalmente 5-15 minutos)

**O que acontece**:
- Verifica aplicativos instalados via winget
- Baixa e instala atualizações disponíveis
- Mostra lista de aplicativos atualizados

### 3. Atualizar Apenas Windows

**Quando usar**: Para instalar atualizações do sistema operacional

**Passos**:
1. Clique em "🪟 Atualizar Apenas Windows"
2. Confirme a operação
3. Aguarde (pode levar 20-40 minutos)

**O que acontece**:
- Instala módulo PSWindowsUpdate (se necessário)
- Busca atualizações do Windows
- Baixa e instala atualizações
- Lista atualizações instaladas

## ⚠️ Avisos Importantes

### Privilégios de Administrador

O aplicativo funciona melhor quando executado como Administrador:
- ✅ **Com Admin**: Todas as funcionalidades disponíveis
- ⚠️ **Sem Admin**: Algumas atualizações podem falhar

### Durante a Atualização

**FAÇA**:
- ✅ Mantenha o computador conectado à energia
- ✅ Mantenha uma conexão estável com a internet
- ✅ Aguarde o processo completar
- ✅ Leia os logs para acompanhar o progresso

**NÃO FAÇA**:
- ❌ Não feche o aplicativo durante a atualização
- ❌ Não desligue o computador
- ❌ Não suspenda o sistema
- ❌ Não desconecte da internet

## 📊 Entendendo os Logs

### Tipos de Mensagens

- **INFO**: Informações normais do processo
  ```
  [14:30:25] INFO: Iniciando atualização de aplicativos...
  ```

- **WARNING**: Avisos que não impedem a execução
  ```
  [14:30:30] WARNING: Não está executando como Administrador!
  ```

- **ERROR**: Erros que impedem alguma operação
  ```
  [14:30:35] ERROR: Winget não está instalado
  ```

### Símbolos

- ✓ : Operação bem-sucedida
- ✗ : Operação falhou
- ⚠ : Aviso importante

## 🔧 Resolução de Problemas

### Problema: "Winget não está instalado"

**Solução**:
1. Abra a Microsoft Store
2. Procure por "App Installer"
3. Instale ou atualize o aplicativo
4. Reinicie o Menino de TI Helper

### Problema: "Erro ao instalar PSWindowsUpdate"

**Solução**:
1. Abra PowerShell como Administrador
2. Execute:
   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   Install-Module PSWindowsUpdate -Force
   ```
3. Reinicie o aplicativo

### Problema: "Aplicativo não inicia"

**Solução**:
1. Verifique se o Python está instalado:
   ```bash
   python --version
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Tente executar novamente

### Problema: "Algumas atualizações falharam"

**Solução**:
- Verifique os logs para identificar qual aplicativo falhou
- Alguns aplicativos podem precisar de atualização manual
- Tente executar o processo novamente
- Verifique se há espaço em disco suficiente

## 📁 Arquivos de Log

Os logs são salvos automaticamente com o formato:
```
menino_ti_helper_YYYYMMDD_HHMMSS.log
```

Exemplo: `menino_ti_helper_20260114_143025.log`

**Localização**: Mesma pasta do aplicativo

**Use os logs para**:
- Diagnosticar problemas
- Verificar quais aplicativos foram atualizados
- Compartilhar informações ao reportar bugs

## 💡 Dicas e Melhores Práticas

### Frequência de Uso

**Recomendado**:
- **Semanal**: Executar "Atualizar Tudo"
- **Após instalar novos programas**: Executar "Atualizar Aplicativos"
- **Quando o Windows notificar**: Executar "Atualizar Windows"

### Manutenção Preventiva

1. Execute o aplicativo regularmente
2. Mantenha backups importantes
3. Verifique os logs periodicamente
4. Mantenha espaço livre em disco (mínimo 20GB)

### Otimização

- Execute durante horários de baixo uso do PC
- Feche aplicativos desnecessários antes
- Desative temporariamente antivírus se houver conflitos (com cautela)

## 🎓 Perguntas Frequentes

**P: Preciso executar como Administrador?**
R: Recomendado, mas não obrigatório. Algumas atualizações podem falhar sem privilégios admin.

**P: Quanto tempo demora?**
R: Varia de 10 a 60 minutos, dependendo da quantidade de atualizações.

**P: Precisa de internet?**
R: Sim, conexão estável é essencial.

**P: O computador vai reiniciar?**
R: O aplicativo está configurado para NÃO reiniciar automaticamente. Você decide quando reiniciar.

**P: Posso usar outros programas enquanto atualiza?**
R: Sim, mas o desempenho pode ser afetado. Recomenda-se deixar o processo executar sem interrupções.

**P: É seguro?**
R: Sim, o código é open-source e usa apenas ferramentas oficiais da Microsoft (winget e Windows Update).

## 📞 Suporte

Se tiver problemas:

1. Consulte a seção "Resolução de Problemas"
2. Verifique os arquivos de log
3. Abra uma issue no GitHub: https://github.com/exadmax/meninodati/issues
4. Inclua:
   - Descrição do problema
   - Mensagem de erro
   - Arquivo de log relevante

## 🎯 Checklist de Primeira Execução

Antes de usar pela primeira vez:

- [ ] Python 3.7+ instalado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Executando como Administrador (recomendado)
- [ ] Conexão com internet estável
- [ ] Pelo menos 20GB de espaço livre
- [ ] Backups importantes realizados
- [ ] App Installer (winget) instalado

---

**Desenvolvido para facilitar a vida de técnicos de TI e usuários do Windows 11** 🔧
