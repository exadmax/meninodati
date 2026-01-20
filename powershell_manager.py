"""
PowerShell Integration Module
Handles execution of PowerShell commands from Python
"""
import subprocess
import logging
from typing import Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PowerShellManager:
    """Manages PowerShell command execution"""
    
    def __init__(self):
        self.encoding = 'utf-8'
        
    def execute_command(self, command: str, timeout: int = 300) -> Tuple[bool, str, str]:
        """
        Execute a PowerShell command
        
        Args:
            command: PowerShell command to execute
            timeout: Maximum time to wait for command completion (seconds)
            
        Returns:
            Tuple of (success: bool, stdout: str, stderr: str)
        """
        try:
            logger.info(f"Executing PowerShell command: {command[:100]}...")
            
            # Tentar com UTF-8 primeiro
            try:
                process = subprocess.Popen(
                    ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', command],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8',
                    errors='replace'  # Substituir caracteres inválidos
                )
                
                stdout, stderr = process.communicate(timeout=timeout)
            except UnicodeDecodeError:
                # Fallback para CP1252 (Windows Latin-1)
                logger.warning("UTF-8 decode failed, trying CP1252")
                process = subprocess.Popen(
                    ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', command],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='cp1252',
                    errors='replace'
                )
                
                stdout, stderr = process.communicate(timeout=timeout)
            
            # Garantir que stdout e stderr nunca sejam None
            stdout = stdout if stdout is not None else ""
            stderr = stderr if stderr is not None else ""
            
            success = process.returncode == 0
            
            if success:
                logger.info("Command executed successfully")
            else:
                logger.error(f"Command failed with return code {process.returncode}")
                
            return success, stdout, stderr
            
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out after {timeout} seconds")
            process.kill()
            return False, "", "Command timed out"
            
        except Exception as e:
            logger.error(f"Error executing command: {str(e)}")
            return False, "", str(e)
    
    def check_admin_privileges(self) -> bool:
        """
        Check if the script is running with administrator privileges
        
        Returns:
            True if running as admin, False otherwise
        """
        command = """
        $currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
        $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
        """
        success, stdout, _ = self.execute_command(command)
        return success and stdout and stdout.strip().lower() == "true"
    
    def install_winget_if_needed(self) -> Tuple[bool, str]:
        """
        Check if winget is installed, and provide instructions if not
        
        Returns:
            Tuple of (is_installed: bool, message: str)
        """
        command = "Get-Command winget -ErrorAction SilentlyContinue"
        success, stdout, _ = self.execute_command(command)
        
        if success and stdout and stdout.strip():
            logger.info("Winget is installed")
            return True, "Winget is available"
        else:
            logger.warning("Winget is not installed")
            return False, "Winget não está instalado. Por favor, instale o App Installer da Microsoft Store."
    
    def update_all_apps_with_winget(self) -> Tuple[bool, str]:
        """
        Update all applications using winget (método mais rápido - atualiza tudo de uma vez)
        
        Returns:
            Tuple of (success: bool, output: str)
        """
        logger.info("Starting application updates with winget (bulk update)")
        command = "winget upgrade --all --silent --accept-source-agreements --accept-package-agreements"
        success, stdout, stderr = self.execute_command(command, timeout=1800)  # 30 minutes timeout
        
        output = stdout if stdout else stderr
        
        if success:
            logger.info("Bulk update completed successfully")
        else:
            logger.warning(f"Bulk update had issues: {stderr}")
        
        return success, output
    
    def update_apps_individually(self, progress_callback=None) -> Tuple[int, int, list]:
        """
        Atualiza aplicativos individualmente com progresso detalhado
        
        Args:
            progress_callback: Função callback(current, total, app_name, success) para reportar progresso
            
        Returns:
            Tuple of (successful_count, failed_count, failed_apps_list)
        """
        logger.info("Starting individual application updates")
        
        # Listar apps que precisam atualização
        apps_to_update = self.list_upgradable_apps()
        
        if not apps_to_update:
            logger.info("No applications to update")
            return 0, 0, []
        
        total = len(apps_to_update)
        successful = 0
        failed = 0
        failed_apps = []
        
        logger.info(f"Found {total} applications to update")
        
        for i, app in enumerate(apps_to_update, 1):
            app_id = app['id']
            app_name = app['name']
            
            if progress_callback:
                try:
                    progress_callback(i, total, app_name, None)
                except Exception as e:
                    logger.warning(f"Progress callback error: {e}")
            
            # Atualizar app
            success = self.update_app_silent(app_id)
            
            if success:
                successful += 1
            else:
                failed += 1
                failed_apps.append({'name': app_name, 'id': app_id})
            
            if progress_callback:
                try:
                    progress_callback(i, total, app_name, success)
                except Exception as e:
                    logger.warning(f"Progress callback error: {e}")
        
        logger.info(f"Update complete: {successful} successful, {failed} failed")
        return successful, failed, failed_apps
    
    def list_upgradable_apps(self) -> list:
        """
        Lista aplicativos que precisam ser atualizados usando formato JSON do winget
        
        Returns:
            Lista de dicionários com informações dos apps: [{'id': ..., 'name': ..., 'version': ..., 'available': ...}]
        """
        logger.info("Listing upgradable applications")
        
        # Tentar primeiro com formato JSON (mais confiável)
        import json
        command = "winget upgrade --accept-source-agreements | ConvertTo-Json -Depth 10"
        success, stdout, stderr = self.execute_command(command, timeout=120)
        
        apps = []
        
        # Se JSON falhar, usar parsing de texto tradicional melhorado
        if not success or not stdout or not stdout.strip():
            logger.info("JSON parsing failed, using text parsing")
            command = "winget upgrade --accept-source-agreements"
            success, stdout, stderr = self.execute_command(command, timeout=120)
        
        if success and stdout:
            # Tentar parsear como JSON primeiro
            try:
                data = json.loads(stdout)
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and 'Id' in item:
                            apps.append({
                                'name': item.get('Name', item.get('Id', 'Unknown')),
                                'id': item['Id'],
                                'version': item.get('Version', 'unknown'),
                                'available': item.get('Available', item.get('AvailableVersion', 'unknown'))
                            })
                    logger.info(f"Found {len(apps)} upgradable applications via JSON")
                    return apps
            except (json.JSONDecodeError, ValueError):
                logger.debug("Not JSON format, using text parsing")
            
            # Fallback: Parsing de texto melhorado
            lines = stdout.split('\n')
            
            # Encontrar a linha de cabeçalho e separadores
            header_idx = -1
            separator_idx = -1
            
            for i, line in enumerate(lines):
                if 'Name' in line and 'Id' in line and 'Version' in line:
                    header_idx = i
                elif header_idx >= 0 and '-' * 10 in line:
                    separator_idx = i
                    break
            
            # Se encontrou o separador, processar linhas de dados
            if separator_idx > 0:
                for line in lines[separator_idx + 1:]:
                    line = line.strip()
                    
                    # Ignorar linhas vazias e rodapés
                    if not line or 'upgrades available' in line.lower():
                        continue
                    
                    # Usar regex para parsing mais robusto
                    import re
                    # Padrão: Nome (pode ter espaços) | ID (formato Package.ID) | Versão | Versão Disponível | Source
                    # Procurar por padrão de ID com pontos (ex: Microsoft.PowerShell)
                    match = re.search(r'(\S+\.\S+)', line)
                    
                    if match:
                        app_id = match.group(1)
                        parts = line.split()
                        
                        # Encontrar posição do ID na lista de parts
                        try:
                            id_idx = parts.index(app_id)
                            
                            # Nome está antes do ID
                            app_name = ' '.join(parts[:id_idx]) if id_idx > 0 else app_id
                            
                            # Versão atual e disponível estão depois do ID
                            version = parts[id_idx + 1] if len(parts) > id_idx + 1 else 'unknown'
                            available = parts[id_idx + 2] if len(parts) > id_idx + 2 else 'unknown'
                            
                            # Filtrar IDs que não são válidos (muito curtos, só números, etc)
                            if len(app_id) > 3 and '.' in app_id and not app_id.replace('.', '').isdigit():
                                apps.append({
                                    'name': app_name,
                                    'id': app_id,
                                    'version': version,
                                    'available': available
                                })
                        except (ValueError, IndexError):
                            continue
        
        logger.info(f"Found {len(apps)} upgradable applications")
        return apps
    
    def update_app_silent(self, app_id: str) -> bool:
        """
        Atualiza um aplicativo específico silenciosamente com retry e melhor tratamento de erros
        
        Args:
            app_id: ID do aplicativo para atualizar
            
        Returns:
            True se sucesso, False caso contrário
        """
        logger.info(f"Updating application: {app_id}")
        
        # Validar que o ID parece válido
        if not app_id or len(app_id) < 3:
            logger.error(f"Invalid app ID: {app_id}")
            return False
        
        # Tentar com --id exato primeiro (mais preciso)
        command = f"winget upgrade --id {app_id} --exact --silent --accept-source-agreements --accept-package-agreements"
        success, stdout, stderr = self.execute_command(command, timeout=600)
        
        # Se falhar com --exact, tentar sem (pode encontrar por match parcial)
        if not success:
            logger.info(f"Exact match failed for {app_id}, trying without --exact")
            command = f"winget upgrade --id {app_id} --silent --accept-source-agreements --accept-package-agreements"
            success, stdout, stderr = self.execute_command(command, timeout=600)
        
        if success:
            logger.info(f"Successfully updated: {app_id}")
            return True
        else:
            # Log mais detalhado do erro
            error_msg = stderr if stderr else stdout
            logger.warning(f"Failed to update {app_id}: {error_msg}")
            
            # Verificar se é erro conhecido
            if "No applicable update found" in error_msg:
                logger.info(f"No update needed for {app_id} (already up to date)")
                return True  # Não é erro se já está atualizado
            elif "No package found matching input criteria" in error_msg:
                logger.error(f"Package {app_id} not found in repositories")
                return False
            elif "installer failed" in error_msg.lower():
                logger.error(f"Installer failed for {app_id}")
                return False
            
            return False
    
    def install_pswindowsupdate_module(self) -> Tuple[bool, str]:
        """
        Install PSWindowsUpdate module if not already installed
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        logger.info("Checking for PSWindowsUpdate module")
        
        # Check if module is already installed
        check_command = "Get-Module -ListAvailable -Name PSWindowsUpdate"
        success, stdout, _ = self.execute_command(check_command)
        
        if stdout and stdout.strip():
            logger.info("PSWindowsUpdate module is already installed")
            return True, "Módulo PSWindowsUpdate já está instalado"
        
        # Install the module
        logger.info("Installing PSWindowsUpdate module")
        install_command = """
        Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force -ErrorAction SilentlyContinue
        Set-PSRepository -Name 'PSGallery' -InstallationPolicy Trusted -ErrorAction SilentlyContinue
        Install-Module -Name PSWindowsUpdate -Force -ErrorAction Stop
        """
        success, stdout, stderr = self.execute_command(install_command, timeout=600)
        
        if success:
            logger.info("PSWindowsUpdate module installed successfully")
            return True, "Módulo PSWindowsUpdate instalado com sucesso"
        else:
            logger.error(f"Failed to install PSWindowsUpdate module: {stderr}")
            return False, f"Falha ao instalar módulo: {stderr}"
    
    def run_windows_update(self) -> Tuple[bool, str]:
        """
        Run Windows Update
        
        Returns:
            Tuple of (success: bool, output: str)
        """
        logger.info("Starting Windows Update")
        
        # First, ensure the module is installed
        module_success, module_msg = self.install_pswindowsupdate_module()
        if not module_success:
            return False, module_msg
        
        # Run Windows Update
        command = """
        Import-Module PSWindowsUpdate
        Get-WindowsUpdate -AcceptAll -Install -AutoReboot:$false -Verbose
        """
        success, stdout, stderr = self.execute_command(command, timeout=3600)  # 1 hour timeout
        
        output = stdout if stdout else stderr
        
        if success:
            logger.info("Windows Update completed successfully")
        else:
            logger.error(f"Windows Update failed: {stderr}")
            
        return success, output
    
    def run_windows_update_with_progress(self, progress_callback=None) -> Tuple[bool, str]:
        """
        Run Windows Update with progress callback
        
        Args:
            progress_callback: Função callback(percent, message) chamada durante o progresso
            
        Returns:
            Tuple of (success: bool, output: str)
        """
        logger.info("Starting Windows Update with progress tracking")
        
        # First, ensure the module is installed
        module_success, module_msg = self.install_pswindowsupdate_module()
        if not module_success:
            return False, module_msg
        
        if progress_callback:
            progress_callback(0, "Verificando atualizações disponíveis...")
        
        # Run Windows Update
        command = """
        Import-Module PSWindowsUpdate
        Get-WindowsUpdate -AcceptAll -Install -AutoReboot:$false -Verbose
        """
        
        if progress_callback:
            progress_callback(20, "Baixando atualizações...")
        
        success, stdout, stderr = self.execute_command(command, timeout=3600)  # 1 hour timeout
        
        if progress_callback:
            progress_callback(80, "Instalando atualizações...")
        
        output = stdout if stdout else stderr
        
        if progress_callback:
            progress_callback(100, "Windows Update concluído")
        
        if success or "No updates" in output or "não há atualizações" in output.lower():
            logger.info("Windows Update completed")
            return True, output
        else:
            logger.error(f"Windows Update completed with issues: {stderr}")
            return False, output
