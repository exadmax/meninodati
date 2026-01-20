# MENINO DA TI - Construtor de Executável - Quick Start

## 🚀 Começar em 30 Segundos

### 1. Clique Duplo (Windows)
```
build_launcher.bat
```
ou
```
build_exe_gui.bat
```

### 2. Selecione Opções
```
[GUI] ou [Console]
```

### 3. Clique "Iniciar Build"
```
Aguarde 2-5 minutos...
```

### 4. Pronto!
```
✅ Arquivo gerado em dist/
```

---

## 📋 Três Formas de Usar

### Modo 1️⃣: Interface Gráfica (+ Fácil)
```bash
python gui_exe_builder.py
```
- Barra de progresso visual
- Log em tempo real
- Botão para abrir pasta

### Modo 2️⃣: Seletor (Recomendado)
```bash
python build_launcher.py
# ou
build_launcher.bat
```
- Escolhe entre GUI ou CLI
- Mais flexível

### Modo 3️⃣: Linha de Comando
```bash
python build_exe.py
```
- Mais direto
- Sem interface

---

## ⚙️ Opções de Build

### Ponto de Entrada
- `auto_launcher.py` ← **Padrão** (com seletor)
- `launcher.py` (seletor visual)
- `main_gui.py` (direto ao GUI)

### Tipo
- `Um arquivo` ← **Recomendado** (fácil distribuir)
- `Diretório` (inicializa mais rápido)

### Extra
- ✅ `Criar ZIP` (para distribuição)

---

## 📊 Resultado

```
dist/
├── MeninoDeTIHelper.exe          (150-200 MB)
├── LEIA-ME.txt                   (instruções)
├── manifest.json                 (info build)
└── MeninoDaTI_v1.0_*.zip         (80-100 MB)
```

---

## 🔥 Recursos

✅ Converte Python → .exe  
✅ Um arquivo ou diretório  
✅ Interface gráfica  
✅ Progresso em tempo real  
✅ Pacote ZIP automático  
✅ Documentação incluída  
✅ Solicita Admin  
✅ Sem dependências externas  

---

## ⏱️ Quanto Tempo Leva?

| Etapa | Tempo |
|-------|-------|
| Limpeza | 10 seg |
| Instalação (1ª vez) | 2 min |
| Build | 1-3 min |
| Documentação | 10 seg |
| **Total** | **3-5 min** |

---

## ❓ FAQ Rápido

**P: O .exe funciona sem Python?**  
✅ Sim, é completamente independente

**P: Precisa de admin?**  
✅ Sim, para executar (build não)

**P: Qual o tamanho?**  
📦 150-200 MB por arquivo

**P: Posso distribuir?**  
✅ Sim, é permitido

**P: Como usar?**  
👉 Execute como Admin

---

## 🐛 Erros Comuns

| Erro | Solução |
|------|---------|
| PyInstaller não encontrado | `pip install pyinstaller` |
| Sem espaço em disco | Libere 500 MB |
| Build muito lento | Feche outros programas |
| .exe não inicia | Execute como Admin |

---

## 📞 Precisa de Ajuda?

```
1. Leia: GUIA_BUILD.md
2. Veja: CONSTRUTOR.md  
3. Abra: VERIFICACAO_SISTEMA.md
```

---

## 🎯 Próximos Passos

```
1. ✅ Executar Build
   python gui_exe_builder.py
   
2. 📁 Abrir dist/
   duplo clique na pasta
   
3. 🚀 Testar .exe
   Clique direito → Executar como admin
   
4. 📦 Distribuir
   Envie arquivo .exe ou .zip
```

---

## 💡 Dicas

- ✅ Use `build_launcher.bat` para mais controle
- ✅ Crie ZIP se for distribuir
- ✅ Teste o .exe antes de enviar
- ✅ Sempre execute como Admin

---

**Status:** ✅ Pronto para Usar  
**Versão:** 1.0  
**Data:** 19 de janeiro de 2026
