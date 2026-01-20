
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
    
    Write-Host "`r✓ $Message" -ForegroundColor Green
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
    $form.Width = 600
    $form.Height = 550
    $form.StartPosition = "CenterScreen"
    $form.BackColor = [System.Drawing.Color]::WhiteSmoke
    $form.TopMost = $true
    $form.FormBorderStyle = "FixedSingle"
    $form.MaximizeBox = $false
    
    # ===== TÍTULO =====
    $titleLabel = New-Object System.Windows.Forms.Label
    $titleLabel.Text = "🔧 $APP_NAME"
    $titleLabel.Font = New-Object System.Drawing.Font("Arial", 20, [System.Drawing.FontStyle]::Bold)
    $titleLabel.Location = New-Object System.Drawing.Point(20, 20)
    $titleLabel.Size = New-Object System.Drawing.Size(560, 40)
    $titleLabel.ForeColor = [System.Drawing.Color]::DarkBlue
    $form.Controls.Add($titleLabel)
    
    # ===== SUBTÍTULO =====
    $subtitleLabel = New-Object System.Windows.Forms.Label
    $subtitleLabel.Text = "Assistente de Instalação"
    $subtitleLabel.Font = New-Object System.Drawing.Font("Arial", 10)
    $subtitleLabel.Location = New-Object System.Drawing.Point(20, 60)
    $subtitleLabel.Size = New-Object System.Drawing.Size(560, 20)
    $subtitleLabel.ForeColor = [System.Drawing.Color]::Gray
    $form.Controls.Add($subtitleLabel)
    
    # ===== SEPARADOR =====
    $separator = New-Object System.Windows.Forms.Label
    $separator.BorderStyle = [System.Windows.Forms.BorderStyle]::Fixed3D
    $separator.Location = New-Object System.Drawing.Point(20, 85)
    $separator.Size = New-Object System.Drawing.Size(560, 2)
    $form.Controls.Add($separator)
    
    # ===== STATUS =====
    $statusLabel = New-Object System.Windows.Forms.Label
    $statusLabel.Text = "Inicializando..."
    $statusLabel.Font = New-Object System.Drawing.Font("Arial", 10)
    $statusLabel.Location = New-Object System.Drawing.Point(20, 100)
    $statusLabel.Size = New-Object System.Drawing.Size(560, 20)
    $statusLabel.ForeColor = [System.Drawing.Color]::Blue
    $form.Controls.Add($statusLabel)
    
    # ===== CAIXA DE LOG =====
    $logBox = New-Object System.Windows.Forms.TextBox
    $logBox.Multiline = $true
    $logBox.ReadOnly = $true
    $logBox.ScrollBars = "Vertical"
    $logBox.Location = New-Object System.Drawing.Point(20, 130)
    $logBox.Size = New-Object System.Drawing.Size(560, 280)
    $logBox.Font = New-Object System.Drawing.Font("Courier New", 8)
    $logBox.BackColor = [System.Drawing.Color]::White
    $form.Controls.Add($logBox)
    
    # ===== BARRA DE PROGRESSO =====
    $progressBar = New-Object System.Windows.Forms.ProgressBar
    $progressBar.Location = New-Object System.Drawing.Point(20, 420)
    $progressBar.Size = New-Object System.Drawing.Size(560, 30)
    $progressBar.Value = 0
    $form.Controls.Add($progressBar)
    
    # ===== LABEL DE PROGRESSO =====
    $progressLabel = New-Object System.Windows.Forms.Label
    $progressLabel.Text = "0%"
    $progressLabel.Font = New-Object System.Drawing.Font("Arial", 9)
    $progressLabel.Location = New-Object System.Drawing.Point(20, 455)
    $progressLabel.Size = New-Object System.Drawing.Size(560, 20)
    $progressLabel.ForegroundColor = [System.Drawing.Color]::Gray
    $form.Controls.Add($progressLabel)
    
    # ===== BOTÕES =====
    $buttonPanel = New-Object System.Windows.Forms.Panel
    $buttonPanel.Location = New-Object System.Drawing.Point(20, 480)
    $buttonPanel.Size = New-Object System.Drawing.Size(560, 40)
    $form.Controls.Add($buttonPanel)
    
    # Botão Iniciar
    $startButton = New-Object System.Windows.Forms.Button
    $startButton.Text = "▶ Iniciar Instalação"
    $startButton.Location = New-Object System.Drawing.Point(0, 0)
    $startButton.Size = New-Object System.Drawing.Size(200, 40)
    $startButton.BackColor = [System.Drawing.Color]::LimeGreen
    $startButton.ForeColor = [System.Drawing.Color]::White
    $startButton.Font = New-Object System.Drawing.Font("Arial", 10, [System.Drawing.FontStyle]::Bold)
    $startButton.Cursor = "Hand"
    $buttonPanel.Controls.Add($startButton)
    
    # Botão Cancelar
    $cancelButton = New-Object System.Windows.Forms.Button
    $cancelButton.Text = "✖ Cancelar"
    $cancelButton.Location = New-Object System.Drawing.Point(360, 0)
    $cancelButton.Size = New-Object System.Drawing.Size(200, 40)
    $cancelButton.BackColor = [System.Drawing.Color]::Red
    $cancelButton.ForeColor = [System.Drawing.Color]::White
    $cancelButton.Font = New-Object System.Drawing.Font("Arial", 10, [System.Drawing.FontStyle]::Bold)
    $cancelButton.Cursor = "Hand"
    $buttonPanel.Controls.Add($cancelButton)
    
    # ===== EVENT HANDLERS =====
    
    # Função para adicionar log
    $global:AddLog = {
        param([string]$Message)
        $logBox.AppendText("$Message`r`n")
        $logBox.ScrollToCaret()
        [System.Windows.Forms.Application]::DoEvents()
    }
    
    # Função para atualizar status
    $global:UpdateStatus = {
        param([string]$Status)
        $statusLabel.Text = $Status
        [System.Windows.Forms.Application]::DoEvents()
    }
    
    # Função para atualizar progresso
    $global:UpdateProgress = {
        param([int]$Value)
        $progressBar.Value = [Math]::Min($Value, 100)
        $progressLabel.Text = "$($progressBar.Value)%"
        [System.Windows.Forms.Application]::DoEvents()
    }
    
    # Click no botão Iniciar
    $startButton.Add_Click({
        $startButton.Enabled = $false
        $cancelButton.Enabled = $false
        
        # Executar instalação em background job
        $installationJob = {
            param($AddLog, $UpdateStatus, $UpdateProgress)
            
            & $UpdateStatus "Verificando sistema..."
            & $UpdateProgress 5
            & $AddLog "═══════════════════════════════════════════════════════"
            & $AddLog "INSTALADOR - $APP_NAME"
            & $AddLog "═══════════════════════════════════════════════════════"
            & $AddLog ""
            & $AddLog "[1/5] Verificando Python..."
            & $UpdateProgress 15
            
            # Verificar Python
            $isPythonInstalled, $versionOutput = Test-PythonInstalled
            
            if ($isPythonInstalled) {
                $version = Get-PythonVersion
                & $AddLog "✓ Python já está instalado (versão: $version)"
                & $UpdateProgress 30
            }
            else {
                & $AddLog "✗ Python não encontrado"
                & $AddLog ""
                & $AddLog "[2/5] Instalando Python via winget..."
                & $UpdateProgress 40
                
                $installSuccess = Install-PythonViaWinget
                
                if ($installSuccess) {
                    & $AddLog "✓ Python instalado com sucesso"
                    & $UpdateProgress 50
                }
                else {
                    & $AddLog "✗ Falha na instalação do Python"
                    & $AddLog ""
                    & $AddLog "Por favor, instale Python manualmente de:"
                    & $AddLog "https://www.python.org/downloads/"
                    & $UpdateStatus "Erro: Falha na instalação"
                    & $UpdateProgress 100
                    return $false
                }
            }
            
            & $AddLog ""
            & $AddLog "[3/5] Atualizando pip..."
            & $UpdateProgress 60
            
            python -m pip install --upgrade pip -q
            & $AddLog "✓ Pip atualizado"
            
            & $AddLog ""
            & $AddLog "[4/5] Instalando pacotes necessários..."
            & $UpdateProgress 70
            
            Install-RequiredPackages
            & $UpdateProgress 80
            
            & $AddLog ""
            & $AddLog "[5/5] Finalizando instalação..."
            & $UpdateProgress 90
            
            & $AddLog ""
            & $AddLog "═══════════════════════════════════════════════════════"
            & $AddLog "✓ Instalação concluída com sucesso!"
            & $AddLog "═══════════════════════════════════════════════════════"
            & $UpdateStatus "Instalação concluída!"
            & $UpdateProgress 100
            
            return $true
        }
        
        # Invocar instalação
        $result = & $installationJob -AddLog $global:AddLog -UpdateStatus $global:UpdateStatus -UpdateProgress $global:UpdateProgress
        
        # Atualizar estado dos botões
        $startButton.Text = "✓ Concluído"
        $startButton.BackColor = [System.Drawing.Color]::LimeGreen
        $startButton.Enabled = $false
        
        if ($result) {
            # Adicionar opção para executar app
            $runAppLabel = New-Object System.Windows.Forms.Label
            $runAppLabel.Text = "Deseja executar a aplicação agora?"
            $runAppLabel.Font = New-Object System.Drawing.Font("Arial", 10)
            $runAppLabel.Location = New-Object System.Drawing.Point(20, 450)
            $runAppLabel.Size = New-Object System.Drawing.Size(560, 20)
            $runAppLabel.ForegroundColor = [System.Drawing.Color]::Green
            $form.Controls.Add($runAppLabel)
            
            $runAppButton = New-Object System.Windows.Forms.Button
            $runAppButton.Text = "▶ Executar Aplicação"
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
        
        $cancelButton.Enabled = $true
        $cancelButton.Text = "✖ Fechar"
    })
    
    # Click no botão Cancelar
    $cancelButton.Add_Click({
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
        Write-InstallLog "Executando aplicação: $foundApp" "Green"
        Start-Process python -ArgumentList $foundApp
    }
    else {
        Write-InstallLog "Erro: Arquivo de aplicação não encontrado" "Red"
        Write-InstallLog "Procurando em: $scriptPath" "Yellow"
    }
}

# ============================================================================
# MAIN
# ============================================================================

function Main {
    Write-InstallLog "═══════════════════════════════════════════════════════" "Cyan"
    Write-InstallLog "$APP_NAME - Instalador" "Cyan"
    Write-InstallLog "═══════════════════════════════════════════════════════" "Cyan"
    Write-InstallLog ""
    
    # Verificação inicial
    Write-InstallLog "Verificando privilégios..." "Yellow"
    if (-not (Test-AdminRights)) {
        Write-InstallLog "⚠ Aviso: Recomenda-se executar como administrador" "Yellow"
        Write-InstallLog "Para melhor experiência, execute este script como admin" "Yellow"
        Write-InstallLog ""
    }
    else {
        Write-InstallLog "✓ Executando com privilégios de administrador" "Green"
    }
    
    # Mostrar formulário
    $form = New-InstallerForm
    $result = $form.ShowDialog()
    $form.Dispose()
}

# Executar
Main

