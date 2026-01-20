"""
cleanup_manager.py - Gerenciador de limpeza segura de cache, lixeira e arquivos temporários
"""
import os
import shutil
import sys
import logging
import tempfile
from pathlib import Path
from typing import Callable, Tuple, Dict

logger = logging.getLogger(__name__)


class CleanupManager:
    """Gerencia limpeza segura de cache, lixeira e arquivos temporários"""
    
    def __init__(self, callback: Callable = None):
        """
        Inicializa o gerenciador de limpeza.
        
        Args:
            callback: Função para reportar progresso (mensagem, percentual)
        """
        self.callback = callback
        self.total_files_deleted = 0
        self.total_size_freed = 0
        self.errors = []
        
    def _report_progress(self, message: str, progress: int = None):
        """Reporta progresso via callback"""
        if self.callback:
            self.callback(message, progress)
        else:
            logger.info(f"[{progress}%] {message}" if progress else message)
    
    def get_cache_folders(self) -> list:
        """
        Retorna lista de pastas de cache conhecidas.
        
        Returns:
            Lista de caminhos de cache
        """
        cache_folders = []
        username = os.getenv('USERNAME')
        
        if not username:
            return cache_folders
        
        # Caches comuns
        cache_paths = [
            # Windows
            f"C:\\Users\\{username}\\AppData\\Local\\Temp",
            f"C:\\Users\\{username}\\AppData\\Local\\Cache",
            
            # Navegadores
            f"C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache",
            f"C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Code Cache",
            f"C:\\Users\\{username}\\AppData\\Local\\Mozilla\\Firefox\\Profiles",
            f"C:\\Users\\{username}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cache",
            f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Recent",
            
            # Windows Update
            f"C:\\Windows\\SoftwareDistribution\\Download",
            f"C:\\Windows\\Logs\\CBS",
            
            # Aplicativos
            f"C:\\Users\\{username}\\AppData\\Local\\Microsoft\\Windows\\INetCache",
            f"C:\\ProgramData\\Microsoft\\Windows\\WER\\ReportArchive",
            f"C:\\ProgramData\\Microsoft\\Windows\\WER\\ReportQueue",
            
            # Pip/Python
            f"C:\\Users\\{username}\\AppData\\Local\\pip\\Cache",
            
            # npm
            f"C:\\Users\\{username}\\AppData\\Roaming\\npm-cache",
        ]
        
        for path in cache_paths:
            if os.path.exists(path):
                cache_folders.append(path)
        
        return cache_folders
    
    def get_temp_folders(self) -> list:
        """
        Retorna lista de pastas de temporários.
        
        Returns:
            Lista de caminhos temporários
        """
        temp_folders = []
        username = os.getenv('USERNAME')
        
        if not username:
            return temp_folders
        
        temp_paths = [
            # Temp padrão
            tempfile.gettempdir(),
            f"C:\\Users\\{username}\\AppData\\Local\\Temp",
            
            # Downloads (opcional - comentado por segurança)
            # f"C:\\Users\\{username}\\Downloads",
            
            # Recycle Bin metadados (tratado separadamente)
        ]
        
        for path in temp_paths:
            if os.path.exists(path):
                temp_folders.append(path)
        
        return temp_folders
    
    def get_recyclable_size(self) -> int:
        """
        Calcula tamanho da lixeira (Recycle Bin).
        
        Returns:
            Tamanho em bytes
        """
        try:
            import ctypes
            from ctypes import wintypes
            
            # Função Windows para obter tamanho da lixeira
            # SHQueryRecycleBin retorna tamanho em bytes
            SHQueryRecycleBin = ctypes.windll.shell32.SHQueryRecycleBinW
            
            # Reservar espaço para o resultado
            size = wintypes.ULONGLONG()
            count = wintypes.DWORD()
            
            # Chamar a função
            result = SHQueryRecycleBin(None, ctypes.byref(size), ctypes.byref(count))
            
            if result == 0:  # S_OK
                return size.value
            else:
                logger.warning(f"Erro ao calcular tamanho da lixeira: {result}")
                return 0
        except Exception as e:
            logger.error(f"Erro ao calcular tamanho da lixeira: {e}")
            return 0
    
    def _get_folder_size(self, path: str) -> Tuple[int, int]:
        """
        Calcula tamanho de uma pasta.
        
        Args:
            path: Caminho da pasta
            
        Returns:
            Tupla (tamanho_bytes, num_arquivos)
        """
        total_size = 0
        file_count = 0
        
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        if os.path.isfile(filepath):
                            total_size += os.path.getsize(filepath)
                            file_count += 1
                    except (OSError, PermissionError) as e:
                        logger.debug(f"Erro ao obter tamanho de {filepath}: {e}")
        except (OSError, PermissionError) as e:
            logger.debug(f"Erro ao processar pasta {path}: {e}")
        
        return total_size, file_count
    
    def _safe_delete_folder_contents(self, path: str) -> Tuple[int, int]:
        """
        Deleta conteúdo de uma pasta com segurança.
        
        Args:
            path: Caminho da pasta
            
        Returns:
            Tupla (arquivos_deletados, bytes_liberados)
        """
        deleted_count = 0
        freed_bytes = 0
        
        try:
            if not os.path.exists(path):
                return deleted_count, freed_bytes
            
            if not os.path.isdir(path):
                return deleted_count, freed_bytes
            
            # Não deletar a pasta em si, apenas o conteúdo
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                
                try:
                    # Obter tamanho antes de deletar
                    if os.path.isfile(item_path):
                        size = os.path.getsize(item_path)
                        os.remove(item_path)
                        deleted_count += 1
                        freed_bytes += size
                    elif os.path.isdir(item_path):
                        # Deletar recursivamente
                        for subdir, _, files in os.walk(item_path, topdown=False):
                            for file in files:
                                try:
                                    file_path = os.path.join(subdir, file)
                                    size = os.path.getsize(file_path)
                                    os.remove(file_path)
                                    deleted_count += 1
                                    freed_bytes += size
                                except (OSError, PermissionError):
                                    pass
                        
                        try:
                            shutil.rmtree(item_path, ignore_errors=True)
                        except (OSError, PermissionError):
                            pass
                except (OSError, PermissionError) as e:
                    error_msg = f"Erro ao deletar {item_path}: {e}"
                    logger.warning(error_msg)
                    self.errors.append(error_msg)
                    
        except Exception as e:
            error_msg = f"Erro geral ao limpar {path}: {e}"
            logger.error(error_msg)
            self.errors.append(error_msg)
        
        return deleted_count, freed_bytes
    
    def _format_size(self, bytes_size: int) -> str:
        """
        Formata tamanho em bytes para formato legível.
        
        Args:
            bytes_size: Tamanho em bytes
            
        Returns:
            String formatada
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} PB"
    
    def clean_cache(self) -> Dict:
        """
        Limpa caches do sistema.
        
        Returns:
            Dicionário com resultados da limpeza
        """
        self._report_progress("Iniciando limpeza de cache...", 5)
        
        results = {
            'files_deleted': 0,
            'bytes_freed': 0,
            'errors': [],
            'details': []
        }
        
        cache_folders = self.get_cache_folders()
        total_folders = len(cache_folders)
        
        for i, cache_path in enumerate(cache_folders):
            progress = 5 + (i / total_folders) * 30  # 5% a 35%
            
            folder_name = os.path.basename(cache_path)
            self._report_progress(f"Limpando cache: {folder_name}...", int(progress))
            
            try:
                size_before, files_before = self._get_folder_size(cache_path)
                deleted, freed = self._safe_delete_folder_contents(cache_path)
                
                if deleted > 0 or freed > 0:
                    results['files_deleted'] += deleted
                    results['bytes_freed'] += freed
                    results['details'].append({
                        'path': cache_path,
                        'files': deleted,
                        'size': freed
                    })
                    
                    logger.info(f"Cache limpo: {folder_name} - {deleted} arquivos, {self._format_size(freed)}")
                    
            except Exception as e:
                error_msg = f"Erro ao limpar {cache_path}: {e}"
                logger.error(error_msg)
                results['errors'].append(error_msg)
        
        return results
    
    def clean_temp_files(self) -> Dict:
        """
        Limpa arquivos temporários.
        
        Returns:
            Dicionário com resultados da limpeza
        """
        self._report_progress("Iniciando limpeza de arquivos temporários...", 35)
        
        results = {
            'files_deleted': 0,
            'bytes_freed': 0,
            'errors': [],
            'details': []
        }
        
        temp_folders = self.get_temp_folders()
        total_folders = len(temp_folders)
        
        for i, temp_path in enumerate(temp_folders):
            progress = 35 + (i / total_folders) * 30  # 35% a 65%
            
            folder_name = os.path.basename(temp_path) or temp_path
            self._report_progress(f"Limpando temporários: {folder_name}...", int(progress))
            
            try:
                deleted, freed = self._safe_delete_folder_contents(temp_path)
                
                if deleted > 0 or freed > 0:
                    results['files_deleted'] += deleted
                    results['bytes_freed'] += freed
                    results['details'].append({
                        'path': temp_path,
                        'files': deleted,
                        'size': freed
                    })
                    
                    logger.info(f"Temporários limpos: {folder_name} - {deleted} arquivos, {self._format_size(freed)}")
                    
            except Exception as e:
                error_msg = f"Erro ao limpar {temp_path}: {e}"
                logger.error(error_msg)
                results['errors'].append(error_msg)
        
        return results
    
    def empty_recycle_bin(self) -> Dict:
        """
        Esvazia a lixeira do Windows.
        
        Returns:
            Dicionário com resultados
        """
        self._report_progress("Iniciando esvaziamento da lixeira...", 65)
        
        results = {
            'size_freed': 0,
            'success': False,
            'message': ''
        }
        
        try:
            import ctypes
            from ctypes import wintypes
            
            # Função Windows para esvaziar recycle bin
            # SHERB_NOCONFIRMATION = 0x00000001 (sem diálogo de confirmação)
            # SHERB_NOPROGRESSUI = 0x00000002 (sem barra de progresso)
            # SHERB_NOSOUND = 0x00000004 (sem som)
            SHEmptyRecycleBin = ctypes.windll.shell32.SHEmptyRecycleBinW
            
            # Obter tamanho antes
            size_before = self.get_recyclable_size()
            
            self._report_progress("Esvaziando lixeira...", 75)
            
            # Esvaziar recycle bin
            # hwnd=None, pszRootPath=None (todos os drives), dwFlags (sem confirmação + sem progressão)
            result = SHEmptyRecycleBin(None, None, 0x00000001 | 0x00000002 | 0x00000004)
            
            if result == 0:  # S_OK
                results['success'] = True
                results['size_freed'] = size_before
                results['message'] = f"Lixeira esvaziada com sucesso ({self._format_size(size_before)} liberados)"
                logger.info(results['message'])
            else:
                results['message'] = f"Erro ao esvaziar lixeira (código: {result})"
                logger.warning(results['message'])
                
        except Exception as e:
            results['message'] = f"Erro ao esvaziar lixeira: {e}"
            logger.error(results['message'])
        
        return results
    
    def cleanup_all(self) -> Dict:
        """
        Executa limpeza completa (cache + temp + lixeira).
        
        Returns:
            Dicionário com resultados consolidados
        """
        self._report_progress("Iniciando limpeza completa do sistema...", 0)
        
        complete_results = {
            'cache': self.clean_cache(),
            'temp': self.clean_temp_files(),
            'recycle': self.empty_recycle_bin(),
            'summary': {
                'total_files': 0,
                'total_bytes': 0,
                'total_errors': len(self.errors)
            }
        }
        
        # Consolidar resultados
        complete_results['summary']['total_files'] = (
            complete_results['cache']['files_deleted'] +
            complete_results['temp']['files_deleted']
        )
        
        complete_results['summary']['total_bytes'] = (
            complete_results['cache']['bytes_freed'] +
            complete_results['temp']['bytes_freed'] +
            complete_results['recycle']['size_freed']
        )
        
        self._report_progress(
            f"Limpeza completa! {complete_results['summary']['total_files']} arquivos deletados, "
            f"{self._format_size(complete_results['summary']['total_bytes'])} liberados",
            100
        )
        
        return complete_results


def cleanup_all_safe(callback: Callable = None) -> Dict:
    """
    Função de conveniência para limpeza completa.
    
    Args:
        callback: Função para reportar progresso
        
    Returns:
        Resultados da limpeza
    """
    manager = CleanupManager(callback)
    return manager.cleanup_all()


def get_cleanup_info() -> Dict:
    """
    Obtém informações sobre limpeza possível.
    
    Returns:
        Dicionário com informações
    """
    manager = CleanupManager()
    
    info = {
        'cache_folders': manager.get_cache_folders(),
        'temp_folders': manager.get_temp_folders(),
        'recycle_size': manager.get_recyclable_size(),
        'cache_size': 0,
        'temp_size': 0
    }
    
    # Calcular tamanhos
    for path in info['cache_folders']:
        size, _ = manager._get_folder_size(path)
        info['cache_size'] += size
    
    for path in info['temp_folders']:
        size, _ = manager._get_folder_size(path)
        info['temp_size'] += size
    
    return info


if __name__ == "__main__":
    # Teste de limpeza
    def test_callback(msg, progress):
        print(f"[{progress}%] {msg}")
    
    print("=== TESTE DE LIMPEZA SEGURA ===\n")
    
    manager = CleanupManager(test_callback)
    results = manager.cleanup_all()
    
    print("\n=== RESULTADOS ===")
    print(f"Arquivos deletados: {results['summary']['total_files']}")
    print(f"Espaço liberado: {manager._format_size(results['summary']['total_bytes'])}")
    print(f"Erros: {results['summary']['total_errors']}")
    
    if manager.errors:
        print("\nErros encontrados:")
        for error in manager.errors:
            print(f"  - {error}")
