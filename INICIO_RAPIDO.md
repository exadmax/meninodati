# 🚀 Início Rápido - Menino de TI Helper v2.0

## Para Usuários Finais

### 1️⃣ Baixar
- Baixe o arquivo `MeninoDeTIHelper.exe`

### 2️⃣ Executar como Administrador
```
Botão direito no arquivo → "Executar como administrador" → Clique em "Sim"
```

### 3️⃣ Usar
- **Atualização Completa**: Atualiza tudo (apps + Windows)
- **Apenas Aplicativos**: Só apps
- **Apenas Windows**: Só Windows Update

### 4️⃣ Aguardar
- Acompanhe a barra de progresso (0-100%)
- Veja os logs detalhados
- Aguarde a mensagem de conclusão

## Para Desenvolvedores

### Setup
```bash
git clone https://github.com/exadmax/meninodati.git
cd meninodati
pip install -r requirements.txt
```

### Executar em Desenvolvimento
```bash
python main_gui.py
```

### Gerar Executável
```bash
python build_exe.py
```

O executável estará em `dist/MeninoDeTIHelper.exe`

## Estrutura de Arquivos

```
meninodati/
├── main_gui.py              # Aplicação principal (USE ESTE)
├── main.py                  # Versão antiga (manter para referência)
├── powershell_manager.py    # Gerenciador PowerShell
├── build_exe.py             # Script de build
├── requirements.txt         # Dependências
│
├── PASSO_A_PASSO.md        # Guia de desenvolvimento detalhado
├── README_V2.md            # README completo v2.0
├── README.md               # README original
└── INICIO_RAPIDO.md        # Este arquivo
```

## Problemas Comuns

### ❌ Programa não abre
**Solução:** Execute como Administrador

### ❌ Winget não encontrado
**Solução:** Instale "App Installer" da Microsoft Store

### ❌ Atualizações falham
**Solução:** 
1. Execute como Administrador
2. Feche todos os programas
3. Verifique Internet

## Logs

Arquivos de log são gerados automaticamente:
```
menino_ti_helper_YYYYMMDD_HHMMSS.log
```

Abra com Bloco de Notas para ver detalhes.

## Requisitos

- ✅ Windows 10/11
- ✅ Conexão Internet
- ✅ Executar como Administrador
- ✅ Winget instalado (geralmente já vem com Windows)

## Tempo Estimado

- 📦 **Apenas Apps**: 10-30 minutos
- 🪟 **Apenas Windows**: 15-45 minutos  
- 🚀 **Completo**: 30-60 minutos

## Suporte

🐛 Problemas? Abra uma issue no GitHub

---

**Versão:** 2.0  
**Data:** Janeiro 2026  
**Autor:** exadmax
