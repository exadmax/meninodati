# Inicialização do MENINO DA TI - Modo Console e Gráfico

## Arquivos Criados

### 1. **console_splash.py**
Tela de inicialização em modo console com arte ASCII.

**Características:**
- Arte ASCII do "MENINO DA TI"
- Simulação de STATUS DO SISTEMA com itens de verificação
- Animação de barra de progresso em tempo real
- Suporte a callbacks para integração com aplicação principal

**Uso:**
```python
from console_splash import ConsoleSplash

splash = ConsoleSplash()
splash.show()  # Com animação
# ou
splash.show_simple()  # Sem animação
```

---

### 2. **splash_screen.py**
Tela de carregamento gráfica com imagem `img/loading.png`.

**Características:**
- Janela splash com imagem de carregamento
- Barra de progresso animada
- Textos de status dinâmicos
- Callbacks para progresso (0-100%)
- Fechamento automático após duração definida
- Centralizada na tela

**Uso:**
```python
from splash_screen import SplashScreen
import tkinter as tk

root = tk.Tk()
root.withdraw()

splash = SplashScreen(root, image_path='img/loading.png', duration=3.0)
splash.set_complete_callback(lambda: print("Carregamento completo!"))
root.mainloop()
```

---

### 3. **launcher.py**
Janela de seleção de modo (console ou gráfico).

**Características:**
- Interface visual para escolher modo de inicialização
- Botões com descrições detalhadas
- Informações sobre cada modo
- Layout responsivo com textos não-cortados
- Dimensões: 700x500 pixels

**Uso:**
```bash
python launcher.py
```

---

### 4. **auto_launcher.py**
Launcher automático com suporte a argumentos de linha de comando.

**Características:**
- Execução automática em modo console ou gráfico via argumentos
- Fallback para seletor de modo se nenhum argumento for fornecido
- Suporte a argumentos: `console` ou `gui`
- Tratamento de erros com fallback para modo console

**Uso:**
```bash
python auto_launcher.py console  # Modo console direto
python auto_launcher.py gui      # Modo gráfico direto
python auto_launcher.py          # Abre seletor de modo
```

---

### 5. **launcher.bat**
Script batch para iniciar o launcher com verificação de Python.

**Características:**
- Verifica instalação do Python
- Exibe mensagens de erro claras
- Mudança automática para diretório do script
- Pausa antes de sair para visualizar mensagens

**Uso:**
```bash
launcher.bat
```

---

### 6. **run_launcher_admin.bat**
Script batch para executar o launcher como administrador.

**Características:**
- Verifica privilégios de administrador
- Executa auto_launcher em modo console
- Mensagens instruindo como executar com privilégios
- Tratamento de erros

**Uso:**
```bash
# Clique com direito e selecione "Executar como administrador"
run_launcher_admin.bat
```

---

## Fluxo de Execução

### Modo 1: Seletor Gráfico
```
launcher.bat
    ↓
launcher.py (ModeLauncher)
    ↓
┌─────────────────────────────┐
│ Seleciona modo (console/gui)│
└──────┬──────────────────────┘
       ├── console: auto_launcher.py console
       │   ↓
       │   ConsoleSplash + Lógica Console
       │
       └── gui: auto_launcher.py gui
           ↓
           SplashScreen (3s)
           ↓
           MeninoDeTIHelperGUI
```

### Modo 2: Direto pelo Console
```
python auto_launcher.py console
    ↓
ConsoleSplash.show()
    ↓
Arte ASCII + Progresso Animado
    ↓
Aplicação em modo console
```

### Modo 3: Direto pelo Gráfico
```
python auto_launcher.py gui
    ↓
SplashScreen (3 segundos)
    ↓
MeninoDeTIHelperGUI (Aplicação Principal)
```

---

## Tela ASCII do Console

A tela exibida é:

```
+-----------------------------------------------------------------------+
|  MENINO DA TI - DIAGNOSTICO v1.0                                [X]   |
+-----------------------------------------------------------------------+
|                                                                       |
|   __  __            _               ____         _____ ___            |
|  |  \/  | ___ _ __ (_)_ __   ___   |  _ \ __ _  |_   _|_ _|           |
|  | |\/| |/ _ \ '_ \| | '_ \ / _ \  | | | / _` |   | |  | |            |
|  | |  | |  __/ | | | | | | | (_) | | |_| | (_| |   | |  | |            |
|  |_|  |_|\___|_| |_|_|_| |_|\___/  |____/ \__,_|   |_| |___|          |
|                                                                       |
|                                                                       |
|  STATUS DO SISTEMA:                                                   |
|  [OK] Verificando cabos de rede...                                    |
|  [OK] Perguntando se reiniciou o modem...                             |
|  [..] Carregando solucoes magicas...                                  |
|                                                                       |
|  PROGRESSO:                                                           |
|  [||||||||||||||||||||||||||||||||||||.................] 65%          |
|                                                                       |
|-----------------------------------------------------------------------|
|  Criado por Diogo Goes Zanetti                                        |
+-----------------------------------------------------------------------+
```

---

## Splash Screen Gráfico

- Exibe imagem de carregamento de `img/loading.png`
- Barra de progresso animada (0-100%)
- Textos de status dinâmicos:
  - "Carregando componentes..."
  - "Inicializando sistema..."
  - "Preparando interface..."
  - "Quase pronto..."
- Duração: 3 segundos (configurável)
- Centralizada na tela
- Transparência: 95%

---

## Chamadas do Launcher

### Para modo console direto:
```bash
launcher.bat console
```

### Para modo gráfico direto:
```bash
launcher.bat gui
```

### Com seletor visual:
```bash
launcher.bat
```

---

## Compatibilidade

- **Python**: 3.8+
- **Dependências**: tkinter (incluído), Pillow (para imagens)
- **SO**: Windows (scripts .bat), pode ser adaptado para Linux/Mac

---

## Testes

Execute os testes com:

```bash
# Teste modo console
python auto_launcher.py console

# Teste do arquivo de tela ASCII
python console_splash.py

# Teste do arquivo de splash gráfico
python splash_screen.py
```

---

**Criado por:** Sistema de Inicialização do MENINO DA TI
**Versão:** 1.0
**Data:** 19 de janeiro de 2026
