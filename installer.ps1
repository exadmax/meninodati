
# installer.ps1 - Instalador Gráfico para MENINO DA TI
# Verifica Python, instala se necessário via winget, e executa a aplicação

# Requer PowerShell 5.0+
#Requires -Version 5.0

# Policy de execução para este script
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

$APP_NAME = "MENINO DA TI"
$PYTHON_MIN_VERSION = "3.8"
$REQUIRED_PACKAGES = @("requests", "pillow")

# ============================================================================
# FUNÇÕES DE UTILIDADE
# ============================================================================

function Write-InstallLog {
    param([string]$Message, [string]$Color = "White")
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] $Message" -ForegroundColor $Color
}

function Test-AdminRights {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Test-PythonInstalled {
    try {
        $output = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            return $true, $output
        }
        return $false, $null
    }
    catch {
        return $false, $null
    }
}

function Get-PythonVersion {
    try {
        $versionOutput = python --version 2>&1
        if ($versionOutput -match 'Python (\d+\.\d+)') {
            return $matches[1]
        }
    }
    catch { }
    return $null
}

function Test-Winget {
    try {
        $output = winget --version 2>&1
        return ($LASTEXITCODE -eq 0)
    }
    catch {
        return $false
    }
}

function Install-PythonViaWinget {
    Write-InstallLog "Instalando Python via winget..." "Yellow"
    
    try {
        # Verificar se winget está disponível
        if (-not (Test-Winget)) {
            Write-InstallLog "ERRO: winget não está disponível no sistema" "Red"
            return $false
        }
        
        Write-InstallLog "Executando: winget install -e --id Python.Python.3.12" "Cyan"
        
        # Instalar Python 3.12
        winget install -e --id Python.Python.3.12 -h --accept-source-agreements --accept-package-agreements
        
        if ($LASTEXITCODE -eq 0) {
            Write-InstallLog "Python instalado com sucesso!" "Green"
            return $true
        }
        else {
            Write-InstallLog "Falha ao instalar Python via winget" "Red"
            return $false
        }
    }
    catch {
        Write-InstallLog "Erro durante instalação: $_" "Red"
        return $false
    }
}

function Install-RequiredPackages {
    Write-InstallLog "Verificando pacotes Python necessários..." "Yellow"
    
    foreach ($package in $REQUIRED_PACKAGES) {
        Write-InstallLog "Instalando: $package" "Cyan"
        pip install $package -q
        
        if ($LASTEXITCODE -ne 0) {
            Write-InstallLog "Aviso: Falha ao instalar $package" "Yellow"
        }
        else {
            Write-InstallLog "$package instalado com sucesso" "Green"
        }
    }
}

function Show-LoadingAnimation {
    param([string]$Message, [int]$Duration = 3)
    
    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    $spinner = @('|', '/', '-', '\')
    $index = 0
    
    while ($stopwatch.Elapsed.TotalSeconds -lt $Duration) {
        $char = $spinner[$index % 4]
        Write-Host -NoNewline "`r$char $Message" -ForegroundColor Cyan
        $index++
        Start-Sleep -Milliseconds 100
    }
    
    Write-Host "`r Message" -ForegroundColor Green
    Write-Host ""
}

# ============================================================================
# INTERFACE GRÁFICA (Windows Forms)
# ============================================================================

function New-InstallerForm {
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
    
    # Criar formulário
    $form = New-Object System.Windows.Forms.Form
    $form.Text = "$APP_NAME - Instalador"
    $form.Width = 650
    $form.Height = 700
    $form.StartPosition = "CenterScreen"
    $form.BackColor = [System.Drawing.Color]::WhiteSmoke
    $form.TopMost = $true
    $form.FormBorderStyle = "FixedSingle"
    $form.MaximizeBox = $false
    
    # ===== TÍTULO =====
    $titleLabel = New-Object System.Windows.Forms.Label
    $titleLabel.Text = "MENINO DA TI"
    $titleLabel.Font = New-Object System.Drawing.Font("Arial", 20, [System.Drawing.FontStyle]::Bold)
    $titleLabel.Location = New-Object System.Drawing.Point(20, 20)
    $titleLabel.Size = New-Object System.Drawing.Size(610, 40)
    $titleLabel.ForeColor = [System.Drawing.Color]::DarkBlue
    $form.Controls.Add($titleLabel)
    
    # ===== SUBTÍTULO =====
    $subtitleLabel = New-Object System.Windows.Forms.Label
    $subtitleLabel.Text = "Assistente de Instalacao"
    $subtitleLabel.Font = New-Object System.Drawing.Font("Arial", 10)
    $subtitleLabel.Location = New-Object System.Drawing.Point(20, 60)
    $subtitleLabel.Size = New-Object System.Drawing.Size(610, 20)
    $subtitleLabel.ForeColor = [System.Drawing.Color]::Gray
    $form.Controls.Add($subtitleLabel)
    
    # ===== SEPARADOR =====
    $separator = New-Object System.Windows.Forms.Label
    $separator.BorderStyle = [System.Windows.Forms.BorderStyle]::Fixed3D
    $separator.Location = New-Object System.Drawing.Point(20, 85)
    $separator.Size = New-Object System.Drawing.Size(610, 2)
    $form.Controls.Add($separator)
    
    # ===== STATUS =====
    $script:statusLabel = New-Object System.Windows.Forms.Label
    $script:statusLabel.Text = "Inicializando..."
    $script:statusLabel.Font = New-Object System.Drawing.Font("Arial", 10)
    $script:statusLabel.Location = New-Object System.Drawing.Point(20, 100)
    $script:statusLabel.Size = New-Object System.Drawing.Size(610, 20)
    $script:statusLabel.ForeColor = [System.Drawing.Color]::Blue
    $form.Controls.Add($script:statusLabel)
    
    # ===== CAIXA DE LOG =====
    $script:logBox = New-Object System.Windows.Forms.TextBox
    $script:logBox.Multiline = $true
    $script:logBox.ReadOnly = $true
    $script:logBox.ScrollBars = "Vertical"
    $script:logBox.Location = New-Object System.Drawing.Point(20, 130)
    $script:logBox.Size = New-Object System.Drawing.Size(610, 400)
    $script:logBox.Font = New-Object System.Drawing.Font("Courier New", 8)
    $script:logBox.BackColor = [System.Drawing.Color]::White
    $form.Controls.Add($script:logBox)
    
    # ===== BARRA DE PROGRESSO =====
    $script:progressBar = New-Object System.Windows.Forms.ProgressBar
    $script:progressBar.Location = New-Object System.Drawing.Point(20, 540)
    $script:progressBar.Size = New-Object System.Drawing.Size(610, 30)
    $script:progressBar.Value = 0
    $form.Controls.Add($script:progressBar)
    
    # ===== LABEL DE PROGRESSO =====
    $script:progressLabel = New-Object System.Windows.Forms.Label
    $script:progressLabel.Text = "0%"
    $script:progressLabel.Font = New-Object System.Drawing.Font("Arial", 9)
    $script:progressLabel.Location = New-Object System.Drawing.Point(20, 575)
    $script:progressLabel.Size = New-Object System.Drawing.Size(610, 20)
    $script:progressLabel.ForeColor = [System.Drawing.Color]::Gray
    $form.Controls.Add($script:progressLabel)
    
    # ===== BOTÕES =====
    $buttonPanel = New-Object System.Windows.Forms.Panel
    $buttonPanel.Location = New-Object System.Drawing.Point(20, 600)
    $buttonPanel.Size = New-Object System.Drawing.Size(610, 50)
    $form.Controls.Add($buttonPanel)
    
    # Botão Iniciar
    $script:startButton = New-Object System.Windows.Forms.Button
    $script:startButton.Text = "Iniciar Instalacao"
    $script:startButton.Location = New-Object System.Drawing.Point(0, 5)
    $script:startButton.Size = New-Object System.Drawing.Size(280, 40)
    $script:startButton.BackColor = [System.Drawing.Color]::LimeGreen
    $script:startButton.ForeColor = [System.Drawing.Color]::White
    $script:startButton.Font = New-Object System.Drawing.Font("Arial", 10, [System.Drawing.FontStyle]::Bold)
    $script:startButton.Cursor = "Hand"
    $buttonPanel.Controls.Add($script:startButton)
    
    # Botão Cancelar
    $script:cancelButton = New-Object System.Windows.Forms.Button
    $script:cancelButton.Text = "Cancelar"
    $script:cancelButton.Location = New-Object System.Drawing.Point(330, 5)
    $script:cancelButton.Size = New-Object System.Drawing.Size(280, 40)
    $script:cancelButton.BackColor = [System.Drawing.Color]::Red
    $script:cancelButton.ForeColor = [System.Drawing.Color]::White
    $script:cancelButton.Font = New-Object System.Drawing.Font("Arial", 10, [System.Drawing.FontStyle]::Bold)
    $script:cancelButton.Cursor = "Hand"
    $buttonPanel.Controls.Add($script:cancelButton)
    
    # ===== EVENT HANDLERS =====
    
    # Função para adicionar log
    $global:AddLog = {
        param([string]$Message)
        $script:logBox.AppendText("$Message`r`n")
        $script:logBox.ScrollToCaret()
        [System.Windows.Forms.Application]::DoEvents()
    }
    
    # Função para atualizar status
    $global:UpdateStatus = {
        param([string]$Status)
        $script:statusLabel.Text = $Status
        [System.Windows.Forms.Application]::DoEvents()
    }
    
    # Função para atualizar progresso
    $global:UpdateProgress = {
        param([int]$Value)
        $script:progressBar.Value = [Math]::Min($Value, 100)
        $script:progressLabel.Text = "$($script:progressBar.Value)%"
        [System.Windows.Forms.Application]::DoEvents()
    }
    
    # Click no botão Iniciar
    $script:startButton.Add_Click({
        $script:startButton.Enabled = $false
        $script:cancelButton.Enabled = $false
        
        # Executar instalação em background job
        $installationJob = {
            param($AddLog, $UpdateStatus, $UpdateProgress)
            
            & $UpdateStatus "Verificando sistema..."
            & $UpdateProgress 5
            & $AddLog "===================================================="
            & $AddLog "INSTALADOR - $APP_NAME"
            & $AddLog "===================================================="
            & $AddLog ""
            & $AddLog "[1/5] Verificando Python..."
            & $UpdateProgress 15
            
            # Verificar Python
            $isPythonInstalled, $versionOutput = Test-PythonInstalled
            
            if ($isPythonInstalled) {
                $version = Get-PythonVersion
                & $AddLog "Python ja esta instalado (versao: $version)"
                & $UpdateProgress 30
            }
            else {
                & $AddLog "Python nao encontrado"
                & $AddLog ""
                & $AddLog "[2/5] Instalando Python via winget..."
                & $UpdateProgress 40
                
                $installSuccess = Install-PythonViaWinget
                
                if ($installSuccess) {
                    & $AddLog "Python instalado com sucesso"
                    & $UpdateProgress 50
                }
                else {
                    & $AddLog "Falha na instalacao do Python"
                    & $AddLog ""
                    & $AddLog "Por favor, instale Python manualmente de:"
                    & $AddLog "https://www.python.org/downloads/"
                    & $UpdateStatus "Erro: Falha na instalacao"
                    & $UpdateProgress 100
                    return $false
                }
            }
            
            & $AddLog ""
            & $AddLog "[3/5] Atualizando pip..."
            & $UpdateProgress 60
            
            python -m pip install --upgrade pip -q
            & $AddLog "Pip atualizado"
            
            & $AddLog ""
            & $AddLog "[4/5] Instalando pacotes necessarios..."
            & $UpdateProgress 70
            
            Install-RequiredPackages
            & $UpdateProgress 80
            
            & $AddLog ""
            & $AddLog "[5/5] Finalizando instalacao..."
            & $UpdateProgress 90
            
            & $AddLog ""
            & $AddLog "===================================================="
            & $AddLog "Instalacao concluida com sucesso!"
            & $AddLog "===================================================="
            & $UpdateStatus "Instalacao concluida!"
            & $UpdateProgress 100
            
            return $true
        }
        
        # Invocar instalação
        $result = & $installationJob $global:AddLog $global:UpdateStatus $global:UpdateProgress
        
        # Atualizar estado dos botões
        $script:startButton.Text = "Concluido"
        $script:startButton.BackColor = [System.Drawing.Color]::LimeGreen
        $script:startButton.Enabled = $false
        
        if ($result) {
            # Adicionar opção para executar app
            $runAppLabel = New-Object System.Windows.Forms.Label
            $runAppLabel.Text = "Deseja executar a aplicacao agora?"
            $runAppLabel.Font = New-Object System.Drawing.Font("Arial", 10)
            $runAppLabel.Location = New-Object System.Drawing.Point(20, 450)
            $runAppLabel.Size = New-Object System.Drawing.Size(560, 20)
            $runAppLabel.ForeColor = [System.Drawing.Color]::Green
            $form.Controls.Add($runAppLabel)
            
            $runAppButton = New-Object System.Windows.Forms.Button
            $runAppButton.Text = "Executar Aplicacao"
            $runAppButton.Location = New-Object System.Drawing.Point(180, 475)
            $runAppButton.Size = New-Object System.Drawing.Size(240, 35)
            $runAppButton.BackColor = [System.Drawing.Color]::LimeGreen
            $runAppButton.ForeColor = [System.Drawing.Color]::White
            $runAppButton.Font = New-Object System.Drawing.Font("Arial", 10, [System.Drawing.FontStyle]::Bold)
            $runAppButton.Cursor = "Hand"
            $form.Controls.Add($runAppButton)
            
            $runAppButton.Add_Click({
                $form.Close()
                Start-Application
            })
        }
        
        $script:cancelButton.Enabled = $true
        $script:cancelButton.Text = "Fechar"
    })
    

    
    # Click no botão Cancelar
    $script:cancelButton.Add_Click({
        $form.Close()
    })
    
    return $form
}

function Start-Application {
    # Procurar por main_gui.py ou main.py
    $scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
    
    # Tentar encontrar os arquivos de entrada
    $appFiles = @("main_gui.py", "auto_launcher.py", "main.py")
    $foundApp = $null
    
    foreach ($file in $appFiles) {
        $fullPath = Join-Path $scriptPath $file
        if (Test-Path $fullPath) {
            $foundApp = $fullPath
            break
        }
    }
    
    if ($foundApp) {
        Write-InstallLog "Executando aplicacao: $foundApp" "Green"
        Start-Process python -ArgumentList $foundApp
    }
    else {
        Write-InstallLog "Erro: Arquivo de aplicacao nao encontrado" "Red"
        Write-InstallLog "Procurando em: $scriptPath" "Yellow"
    }
}

# ============================================================================
# MAIN
# ============================================================================

function Main {
    Write-InstallLog "====================================================" "Cyan"
    Write-InstallLog "$APP_NAME - Instalador" "Cyan"
    Write-InstallLog "====================================================" "Cyan"
    Write-InstallLog ""
    
    # Verificação inicial
    Write-InstallLog "Verificando privilegios..." "Yellow"
    if (-not (Test-AdminRights)) {
        Write-InstallLog "Aviso: Recomenda-se executar como administrador" "Yellow"
        Write-InstallLog "Para melhor experiencia, execute este script como admin" "Yellow"
        Write-InstallLog ""
    }
    else {
        Write-InstallLog "Executando com privilegios de administrador" "Green"
    }
    
    # Mostrar formulário
    $form = New-InstallerForm
    $result = $form.ShowDialog()
    $form.Dispose()
}

# Executar
Main

