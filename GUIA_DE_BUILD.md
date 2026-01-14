# 🛠️ Guia Visual de Build - Menino de TI Helper

## 📋 Pré-requisitos

Antes de começar, você precisa ter:
- ✅ Python 3.8+ instalado
- ✅ pip funcionando
- ✅ Git instalado (para clonar o repositório)

---

## 🚀 Passo 1: Obter o Código

### Via Git (Recomendado)
```bash
git clone https://github.com/exadmax/meninodati.git
cd meninodati
```

### Ou Download ZIP
1. Vá para https://github.com/exadmax/meninodati
2. Clique em "Code" → "Download ZIP"
3. Extraia o ZIP
4. Abra o terminal na pasta extraída

---

## 📦 Passo 2: Instalar Dependências

Abra o terminal/CMD na pasta do projeto e execute:

```bash
pip install -r requirements.txt
```

**O que será instalado:**
```
✓ tkinter-tooltip==2.1.0  (Tooltips para GUI)
✓ Pillow==10.4.0          (Manipulação de imagens)
✓ pyinstaller==6.3.0      (Gerador de executável)
```

**Tempo estimado:** 1-2 minutos

---

## 🧪 Passo 3: Testar em Modo Desenvolvimento (Opcional mas Recomendado)

Antes de gerar o executável, teste se tudo funciona:

```bash
python main_gui.py
```

**Deve aparecer:**
- Janela com título "Menino de TI Helper"
- Interface gráfica completa
- Botões funcionais

**Se funcionar:** ✅ Prossiga para o build  
**Se não funcionar:** ⚠️ Verifique as dependências

---

## 🏗️ Passo 4: Gerar o Executável

Execute o script de build:

```bash
python build_exe.py
```

### O que o script faz automaticamente:

```
🧹 Limpando builds anteriores...
  ✓ Removido: build
  ✓ Removido: dist
  ✓ Removido: __pycache__

🔍 Verificando PyInstaller...
  ✓ PyInstaller encontrado

🔨 Construindo executável...
  → Analisando dependências...
  → Coletando arquivos...
  → Compilando código Python...
  → Empacotando recursos...
  → Criando executável único...
  → Adicionando manifesto UAC...

✅ Build concluído com sucesso!

📦 Executável criado:
   Localização: C:\...\meninodati\dist\MeninoDeTIHelper.exe
   Tamanho: 65.43 MB

📝 README criado: dist\README_EXECUTAVEL.txt

🎉 PROCESSO CONCLUÍDO COM SUCESSO!

📁 Seus arquivos estão em: dist/
   - MeninoDeTIHelper.exe (executável)
   - README_EXECUTAVEL.txt (instruções)

⚠️  IMPORTANTE: Execute o .exe como Administrador!
```

**Tempo estimado:** 2-5 minutos

---

## 📂 Passo 5: Localizar o Executável

Após o build bem-sucedido:

```
meninodati/
└── dist/
    ├── MeninoDeTIHelper.exe         ← SEU EXECUTÁVEL
    └── README_EXECUTAVEL.txt        ← INSTRUÇÕES DE USO
```

**Tamanho esperado do .exe:** 50-70 MB (normal para apps Python empacotados)

---

## ✅ Passo 6: Testar o Executável

1. **Navegue até a pasta `dist/`**

2. **Clique com o botão DIREITO em `MeninoDeTIHelper.exe`**

3. **Selecione "Executar como administrador"**

4. **Clique "Sim" no UAC (Controle de Conta de Usuário)**

5. **Verifique se:**
   - Janela abre corretamente
   - Interface está completa
   - Indicador mostra "✅ Executando como Administrador"
   - Botões são clicáveis

**Se tudo funcionar:** 🎉 Build bem-sucedido!

---

## 📤 Passo 7: Distribuir

### Opção A: Compartilhar a Pasta `dist/`

1. Compacte a pasta `dist/` em um arquivo ZIP:
   ```bash
   # Windows PowerShell
   Compress-Archive -Path dist\* -DestinationPath MeninoDeTIHelper_v2.0.zip
   ```

2. Compartilhe o arquivo `MeninoDeTIHelper_v2.0.zip`

3. Instrua os usuários:
   ```
   1. Extrair o ZIP
   2. Executar MeninoDeTIHelper.exe como Administrador
   ```

### Opção B: Compartilhar Apenas o .exe

1. Copie `dist/MeninoDeTIHelper.exe` para onde desejar

2. O executável é **standalone** (não precisa de Python instalado)

3. Instrua os usuários:
   ```
   Botão direito → Executar como administrador
   ```

---

## 🐛 Solução de Problemas do Build

### ❌ Erro: "PyInstaller not found"

**Solução:**
```bash
pip install --upgrade pyinstaller
```

---

### ❌ Erro: "Module not found: tkinter"

**Problema:** tkinter não está instalado

**Solução (Windows):**
- tkinter vem com Python, reinstale o Python e marque "tcl/tk and IDLE"

**Solução (Linux):**
```bash
sudo apt-get install python3-tk
```

---

### ❌ Erro: "Access denied" ao limpar pastas

**Problema:** Arquivos em uso

**Solução:**
1. Feche todas as instâncias do programa
2. Feche o terminal/CMD
3. Reabra e tente novamente

---

### ❌ Executável não abre (sem mensagem de erro)

**Possíveis causas:**
1. Antivírus bloqueando
2. Windows Defender bloqueando
3. Falta de privilégios

**Soluções:**
1. Adicione exceção no antivírus para a pasta `dist/`
2. Execute como Administrador
3. Desabilite temporariamente o antivírus e teste

---

### ❌ Executável abre mas fecha imediatamente

**Solução:** Execute via CMD para ver erros:
```bash
cd dist
.\MeninoDeTIHelper.exe
```

Isso mostrará mensagens de erro no console.

---

## 📊 Estrutura de Build Detalhada

### Antes do Build
```
meninodati/
├── main_gui.py
├── powershell_manager.py
├── build_exe.py
├── requirements.txt
└── [outros arquivos]
```

### Durante o Build
```
meninodati/
├── [arquivos originais]
├── build/              ← Pasta temporária (PyInstaller)
│   └── [arquivos temp]
├── dist/               ← Pasta de output (criada)
│   └── [em construção]
└── MeninoDeTIHelper.spec  ← Arquivo de configuração (gerado)
```

### Após o Build
```
meninodati/
├── [arquivos originais]
├── build/              ← Pode ser deletado
├── dist/               ← PASTA IMPORTANTE
│   ├── MeninoDeTIHelper.exe      ← EXECUTÁVEL
│   └── README_EXECUTAVEL.txt
└── MeninoDeTIHelper.spec  ← Pode ser deletado
```

---

## 🧹 Limpeza Pós-Build (Opcional)

Se quiser economizar espaço, pode deletar:

```bash
# Deletar pastas temporárias
rm -rf build/
rm -rf __pycache__/
rm MeninoDeTIHelper.spec

# Manter apenas:
# - dist/ (com o executável)
# - Arquivos de código-fonte (para futuras modificações)
```

---

## 🔄 Rebuild (Atualizar o Executável)

Se você modificar o código e quiser gerar um novo executável:

```bash
# O script de build já limpa automaticamente
python build_exe.py
```

Não precisa limpar manualmente, o script cuida de tudo!

---

## 📝 Customizações Avançadas

### Adicionar Ícone Customizado

1. Tenha um arquivo `.ico` pronto (ex: `icon.ico`)

2. Edite `build_exe.py`, linha com `--icon=`:
   ```python
   '--icon=icon.ico',  # Em vez de '--icon=NONE',
   ```

3. Execute o build novamente

### Alterar Nome do Executável

Em `build_exe.py`, modifique:
```python
'--name=MeninoDeTIHelper',  # Altere para o nome desejado
```

### Incluir Arquivos Adicionais

Em `build_exe.py`, adicione:
```python
'--add-data=meu_arquivo.txt;.',
'--add-data=pasta_config;config',
```

---

## 🎯 Checklist de Build

Antes de distribuir, verifique:

- [ ] Build executou sem erros
- [ ] Executável foi criado em `dist/`
- [ ] Tamanho do executável é razoável (50-100 MB)
- [ ] Executável abre corretamente
- [ ] UAC solicita permissões de admin
- [ ] Interface está completa e funcional
- [ ] Botões respondem corretamente
- [ ] Todas as funcionalidades testadas
- [ ] README_EXECUTAVEL.txt foi criado
- [ ] Logs são gerados corretamente

---

## 📚 Recursos Adicionais

### Documentação PyInstaller
- https://pyinstaller.org/en/stable/

### Solução de Problemas
- https://pyinstaller.org/en/stable/common-problems.html

### Python Packaging
- https://packaging.python.org/

---

## 💡 Dicas Finais

### ✅ Boas Práticas

1. **Sempre teste o executável antes de distribuir**
   - Execute em máquina limpa (sem Python instalado)
   - Teste com e sem privilégios de admin

2. **Mantenha o código-fonte**
   - Não delete os arquivos `.py`
   - Use controle de versão (Git)

3. **Documente suas modificações**
   - Atualize o README se mudar funcionalidades
   - Mantenha changelog atualizado

4. **Versione seus builds**
   - `MeninoDeTIHelper_v2.0.exe`
   - `MeninoDeTIHelper_v2.1.exe`
   - etc.

### ⚠️ Avisos Importantes

1. **Antivírus podem dar falso positivo**
   - Normal para executáveis PyInstaller
   - Adicione exceção se necessário

2. **Executável é maior que o código fonte**
   - Normal, inclui interpretador Python inteiro
   - ~50-70 MB é esperado

3. **UAC é obrigatório**
   - Programa precisa de admin para funcionar
   - Não tente contornar o UAC

---

**🎉 Parabéns! Você agora sabe como fazer o build do Menino de TI Helper!**

---

**Autor:** exadmax  
**Versão:** 2.0  
**Data:** Janeiro 2026

