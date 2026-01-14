# 🔧 Menino de TI Helper

Aplicativo voltado para Windows 11 que visa atualizar todos os aplicativos e executar o Windows Update automaticamente, facilitando a vida do usuário final.

## 📋 Descrição

O **Menino de TI Helper** é uma ferramenta automatizada que:
- 📦 Atualiza todos os aplicativos instalados via winget
- 🪟 Executa Windows Update completo
- 🔄 Integra-se automaticamente com PowerShell
- 🎨 Interface gráfica intuitiva e amigável
- 📊 Exibe logs em tempo real do progresso das atualizações

## ✨ Características

- **Interface Gráfica (GUI)**: Tela de abertura "Menino de TI Helper" e interface principal intuitiva
- **Integração PowerShell**: Executa automaticamente comandos PowerShell quando necessário
- **Autonomia Máxima**: Instala dependências necessárias automaticamente (como PSWindowsUpdate)
- **Três Modos de Operação**:
  - Atualização completa (Apps + Windows)
  - Apenas aplicativos
  - Apenas Windows Update
- **Logs Detalhados**: Acompanhe todo o processo em tempo real
- **Verificação de Privilégios**: Alerta se não estiver executando como administrador

## 🔧 Requisitos

- **Sistema Operacional**: Windows 11 (ou Windows 10 com winget)
- **Python**: 3.7 ou superior
- **Privilégios**: Recomendado executar como Administrador
- **Winget**: App Installer da Microsoft Store (geralmente já instalado no Windows 11)

## 📥 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/exadmax/meninodati.git
cd meninodati
```

2. Instale as dependências Python:
```bash
pip install -r requirements.txt
```

## 🚀 Como Usar

### Execução Normal
```bash
python main.py
```

### Execução como Administrador (Recomendado)
1. Abra o PowerShell como Administrador
2. Navegue até a pasta do projeto
3. Execute:
```powershell
python main.py
```

Ou clique com o botão direito no arquivo `main.py` e selecione "Executar como administrador" (se tiver Python associado).

## 🎮 Interface

A aplicação possui uma interface gráfica com:

- **Tela de Abertura**: Splash screen "Menino de TI Helper"
- **Três Botões Principais**:
  - ▶ Atualizar Tudo (Apps + Windows)
  - 📦 Atualizar Apenas Aplicativos
  - 🪟 Atualizar Apenas Windows
- **Área de Log**: Mostra o progresso em tempo real
- **Barra de Status**: Indica o estado atual da operação

## 📁 Estrutura do Projeto

```
meninodati/
├── main.py                 # Aplicação principal com GUI
├── powershell_manager.py   # Módulo de integração PowerShell
├── requirements.txt        # Dependências Python
├── README.md              # Este arquivo
├── LICENSE                # Licença do projeto
└── .gitignore            # Arquivos ignorados pelo git
```

## 🔐 Segurança

- O aplicativo requer privilégios de administrador para algumas operações
- Todos os comandos PowerShell são registrados em log
- Não armazena credenciais ou dados sensíveis
- Código-fonte aberto para auditoria

## 📝 Logs

Os logs são salvos automaticamente em arquivos com timestamp:
- `menino_ti_helper_YYYYMMDD_HHMMSS.log`

## ⚠️ Observações Importantes

1. **Tempo de Execução**: As atualizações podem levar muito tempo (30+ minutos) dependendo da quantidade de atualizações disponíveis
2. **Conexão com Internet**: Requer conexão estável com a internet
3. **Espaço em Disco**: Certifique-se de ter espaço suficiente para as atualizações
4. **Não Interrompa**: Evite fechar o aplicativo durante as atualizações

## 🛠️ Tecnologias Utilizadas

- **Python 3**: Linguagem principal
- **tkinter**: Interface gráfica
- **PowerShell**: Execução de comandos Windows
- **winget**: Gerenciador de pacotes Windows
- **PSWindowsUpdate**: Módulo PowerShell para Windows Update

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

Desenvolvido para facilitar a vida de técnicos de TI e usuários finais do Windows 11.

## 🐛 Problemas Conhecidos

- Em alguns casos, o PSWindowsUpdate pode precisar de configurações adicionais no Windows
- Algumas atualizações podem requerer reinicialização do sistema
- O winget pode não estar disponível em versões mais antigas do Windows 10

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs gerados
2. Execute como Administrador
3. Certifique-se de que o winget está instalado
4. Abra uma issue no GitHub com detalhes do problema
