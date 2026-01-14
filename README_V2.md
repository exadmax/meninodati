# 🔧 Menino de TI Helper v2.0

> Sistema Gráfico de Atualização Automática para Windows

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Windows](https://img.shields.io/badge/Windows-10%2F11-blue.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Índice

- [Sobre](#-sobre)
- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Execução como Administrador](#-execução-como-administrador)
- [Solução de Problemas](#-solução-de-problemas)
- [Build do Executável](#-build-do-executável)
- [Contribuindo](#-contribuindo)

---

## 📖 Sobre

O **Menino de TI Helper** é uma ferramenta completa e amigável que automatiza o processo de atualização do seu sistema Windows. Com uma interface gráfica intuitiva e barra de progresso detalhada, você pode:

- ✅ Atualizar **todos os aplicativos** instalados automaticamente
- ✅ Executar **Windows Update** sem complicações
- ✅ Acompanhar o progresso em tempo real (**0-100%**)
- ✅ Atualizações **100% silenciosas** (sem interação do usuário)
- ✅ Aceitação automática de licenças

---

## ✨ Características

### 🎯 Interface Gráfica Moderna
- Design limpo e intuitivo
- Feedback visual em tempo real
- Janela de progresso detalhada
- Logs com timestamps

### 📦 Atualização de Aplicativos
- Usa o **Windows Package Manager (winget)**
- Atualiza todos os apps de uma vez
- **Modo silencioso**: sem popups ou confirmações
- Aceitação automática de licenças
- Progresso individual por aplicativo

### 🪟 Windows Update Automático
- Instala automaticamente o módulo **PSWindowsUpdate**
- Baixa e instala atualizações do Windows
- Progresso traduzido do processo do Windows
- Sem reinicialização automática

### 🔐 Gestão de Privilégios
- Verifica automaticamente se está rodando como admin
- Tela de orientação sobre como executar como administrador
- Suporte a UAC (User Account Control)

### 📊 Barra de Progresso Inteligente
- Progresso de **0 a 100%**
- Dividido em 2 passos:
  - **Passo 1 (0-50%)**: Atualização de aplicativos
  - **Passo 2 (50-100%)**: Windows Update
- Informações detalhadas sobre a operação atual
- Histórico de todas as ações executadas

---

## 💻 Requisitos

### Sistema Operacional
- Windows 10 (versão 1809 ou superior)
- Windows 11

### Pré-requisitos
- **Windows Package Manager (winget)** - geralmente já vem instalado
- **PowerShell 5.1** ou superior
- **Conexão com a Internet**
- **Privilégios de Administrador** (recomendado)

### Para Desenvolvimento
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

---

## 📥 Instalação

### Opção 1: Usar o Executável (Recomendado para Usuários)

1. Baixe o arquivo **MeninoDeTIHelper.exe**
2. Não é necessário instalar nada!
3. Execute o arquivo (veja [Como Usar](#-como-usar))

### Opção 2: Executar com Python (Para Desenvolvedores)

```bash
# Clone o repositório
git clone https://github.com/exadmax/meninodati.git

# Entre na pasta
cd meninodati

# Instale as dependências
pip install -r requirements.txt

# Execute o programa
python main_gui.py
```

---

## 🚀 Como Usar

### 1. Executar o Programa

**IMPORTANTE:** O programa deve ser executado como **Administrador**.

#### Método Rápido
1. Localize o arquivo `MeninoDeTIHelper.exe`
2. Clique com o **botão direito** sobre o arquivo
3. Selecione **"Executar como administrador"**
4. Clique em **"Sim"** no UAC (Controle de Conta de Usuário)

#### Método Permanente
1. Clique com o **botão direito** em `MeninoDeTIHelper.exe`
2. Selecione **"Propriedades"**
3. Vá para a aba **"Compatibilidade"**
4. Marque **"Executar este programa como administrador"**
5. Clique em **"OK"**
6. Agora você pode executar com duplo clique normalmente

### 2. Interface Principal

Ao abrir o programa, você verá 3 opções principais:

#### 🚀 Atualização Completa
- Atualiza **aplicativos** + **Windows**
- Processo completo automatizado
- Tempo estimado: 30-60 minutos

#### 📦 Apenas Aplicativos
- Atualiza somente os **aplicativos instalados**
- Mais rápido que a atualização completa
- Tempo estimado: 10-30 minutos

#### 🪟 Apenas Windows Update
- Executa somente o **Windows Update**
- Ideal para atualizações de segurança
- Tempo estimado: 15-45 minutos

### 3. Acompanhar o Progresso

Durante a execução, você verá:
- **Barra de progresso visual** (0-100%)
- **Porcentagem em destaque**
- **Descrição da operação atual**
- **Logs detalhados** com timestamps
- **Status em tempo real**

### 4. Conclusão

Ao final, você receberá uma mensagem de confirmação informando que todas as atualizações foram aplicadas.

---

## 🔐 Execução como Administrador

### Por que preciso de privilégios de administrador?

O programa precisa de permissões elevadas para:
- Instalar e atualizar aplicativos do sistema
- Executar Windows Update
- Modificar configurações do sistema
- Instalar módulos PowerShell

### O que acontece se eu não executar como admin?

O programa mostrará uma tela de orientação explicando como executar corretamente. Você pode optar por:
- **Fechar o programa** e executar como admin (recomendado)
- **Continuar mesmo assim** (não recomendado - algumas funcionalidades podem falhar)

### Como saber se estou executando como admin?

Na tela principal, você verá um indicador no topo:
- ✅ **Verde**: "Executando como Administrador" → Tudo OK!
- ⚠️ **Vermelho**: "NÃO está executando como Administrador" → Execute como admin

---

## 🔧 Solução de Problemas

### O programa não inicia

**Problema:** Nada acontece ao duplo clique no executável

**Soluções:**
1. Execute como **Administrador** (botão direito → Executar como administrador)
2. Verifique se o **Windows Defender** ou antivírus não está bloqueando
3. Desabilite temporariamente o antivírus e tente novamente
4. Verifique os logs na pasta do programa

---

### Winget não encontrado

**Problema:** Mensagem "Winget não está instalado"

**Soluções:**
1. Instale o **"App Installer"** da Microsoft Store
2. Ou baixe diretamente de: https://github.com/microsoft/winget-cli/releases
3. Reinicie o computador após a instalação
4. Execute o programa novamente

---

### Atualizações falham

**Problema:** Algumas atualizações não são aplicadas

**Causas Comuns:**
- Falta de privilégios administrativos
- Conexão com Internet instável
- Servidores de atualização sobrecarregados
- Aplicativo em uso durante a atualização

**Soluções:**
1. **Execute como Administrador**
2. Feche todos os programas antes de atualizar
3. Verifique sua conexão com a Internet
4. Aguarde alguns minutos e tente novamente
5. Execute cada atualização separadamente (Apps ou Windows)

---

### Windows Update trava

**Problema:** Windows Update não progride

**Soluções:**
1. Seja **paciente** - Windows Update pode demorar bastante
2. Verifique os logs para ver se há progresso
3. Se travar por mais de 1 hora, feche o programa e tente novamente
4. Execute apenas "Windows Update" isoladamente

---

### Erro de módulo PSWindowsUpdate

**Problema:** "Falha ao instalar módulo PSWindowsUpdate"

**Soluções:**
1. Execute como **Administrador**
2. Abra PowerShell como admin e execute manualmente:
   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
   Install-Module -Name PSWindowsUpdate -Force
   ```
3. Execute o programa novamente

---

## 🛠️ Build do Executável

### Para Desenvolvedores

Se você quiser compilar o executável você mesmo:

```bash
# 1. Instale as dependências
pip install -r requirements.txt

# 2. Execute o script de build
python build_exe.py

# 3. O executável estará em: dist/MeninoDeTIHelper.exe
```

O script de build:
- Limpa builds anteriores automaticamente
- Verifica e instala PyInstaller se necessário
- Compila com todas as configurações corretas
- Gera README para o executável
- Cria manifesto UAC para solicitar admin

---

## 📚 Documentação Adicional

- **[PASSO_A_PASSO.md](PASSO_A_PASSO.md)**: Guia completo de desenvolvimento
- **[GUIA_DE_USO.md](GUIA_DE_USO.md)**: Manual original do usuário
- **Logs**: Arquivos `.log` gerados automaticamente

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o repositório
2. Crie uma branch para sua feature:
   ```bash
   git checkout -b feature/minha-feature
   ```
3. Commit suas mudanças:
   ```bash
   git commit -am 'Adiciona nova funcionalidade'
   ```
4. Push para a branch:
   ```bash
   git push origin feature/minha-feature
   ```
5. Abra um Pull Request

### Áreas para Contribuição

- 🎨 Melhorias na interface
- 🐛 Correção de bugs
- 📝 Documentação
- 🌐 Internacionalização
- ✨ Novas funcionalidades

---

## 📋 Roadmap

### Versão 2.1 (Planejada)
- [ ] Temas claro/escuro
- [ ] Suporte a ícones personalizados
- [ ] Seleção de aplicativos específicos
- [ ] Agendamento de atualizações

### Versão 3.0 (Futuro)
- [ ] Backup antes de atualizar
- [ ] Rollback de atualizações
- [ ] Visualizador de logs integrado
- [ ] Suporte a múltiplos idiomas

---

## 📝 Changelog

### v2.0 (2026-01-14)
- ✨ Nova interface gráfica moderna
- ✨ Barra de progresso inteligente (0-100%)
- ✨ Atualizações silenciosas com aceitação automática de licenças
- ✨ Tela de orientação para execução como administrador
- ✨ Sistema de logs melhorado
- ✨ Script de build automatizado
- 🐛 Correções de estabilidade

### v1.0 (Versão Anterior)
- ✅ Atualização básica de aplicativos
- ✅ Windows Update
- ✅ Interface com Tkinter

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👨‍💻 Autor

**exadmax**
- GitHub: [@exadmax](https://github.com/exadmax)

---

## 🙏 Agradecimentos

- Comunidade Python
- Microsoft (winget e PSWindowsUpdate)
- Todos os contribuidores

---

## 📞 Suporte

- 🐛 **Bug Reports**: Abra uma [issue](../../issues)
- 💡 **Feature Requests**: Abra uma [issue](../../issues)
- 📧 **Email**: Entre em contato através do GitHub

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela! ⭐**

Desenvolvido com ❤️ por exadmax

</div>
