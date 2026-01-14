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
            
            # Execute PowerShell command
            process = subprocess.Popen(
                ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding=self.encoding
            )
            
            stdout, stderr = process.communicate(timeout=timeout)
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
        return success and stdout.strip().lower() == "true"
    
    def install_winget_if_needed(self) -> Tuple[bool, str]:
        """
        Check if winget is installed, and provide instructions if not
        
        Returns:
            Tuple of (is_installed: bool, message: str)
        """
        command = "Get-Command winget -ErrorAction SilentlyContinue"
        success, stdout, _ = self.execute_command(command)
        
        if success and stdout.strip():
            logger.info("Winget is installed")
            return True, "Winget is available"
        else:
            logger.warning("Winget is not installed")
            return False, "Winget não está instalado. Por favor, instale o App Installer da Microsoft Store."
    
    def update_all_apps_with_winget(self) -> Tuple[bool, str]:
        """
        Update all applications using winget
        
        Returns:
            Tuple of (success: bool, output: str)
        """
        logger.info("Starting application updates with winget")
        command = "winget upgrade --all --accept-source-agreements --accept-package-agreements"
        success, stdout, stderr = self.execute_command(command, timeout=1800)  # 30 minutes timeout
        
        output = stdout if stdout else stderr
        return success, output
    
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
        
        if stdout.strip():
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
