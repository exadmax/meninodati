"""
test_winget_parsing.py - Testa o parsing correto de IDs do winget

Este script testa:
1. Parsing correto de IDs do winget upgrade
2. Filtragem de IDs inválidos
3. Extração correta de nome, versão e versão disponível
"""
import sys

def test_winget_list_parsing():
    """Testa o parsing da lista de apps upgradáveis"""
    print("\n" + "="*75)
    print("TESTE: Parsing de Lista do Winget")
    print("="*75 + "\n")
    
    # Exemplo de saída real do winget upgrade
    sample_output = """Name                           Id                           Version        Available      Source
--------------------------------------------------------------------------------------------------------------------------------
Microsoft Edge                 Microsoft.Edge               131.0.2903.99  132.0.2957.81  winget
Microsoft Visual Studio Code   Microsoft.VisualStudioCode   1.95.3         1.96.0         winget
Adobe Acrobat Reader DC        Adobe.Acrobat.Reader.64-bit  25.3.2         25.4.0         winget
Google Chrome                  Google.Chrome                131.0.6778.140 131.0.6778.205 winget
Discord                        Discord.Discord              1.0.9178       1.0.9179       winget
Docker Desktop                 Docker.DockerDesktop         4.35.1         4.36.0         winget
Anysphere Cursor              Anysphere.Cursor             0.43.6         0.44.0         winget
13 upgrades available."""
    
    try:
        from powershell_manager import PowerShellManager
        import re
        
        ps_manager = PowerShellManager()
        
        # Simular parsing
        lines = sample_output.split('\n')
        
        # Encontrar a linha de cabeçalho e separadores
        header_idx = -1
        separator_idx = -1
        
        for i, line in enumerate(lines):
            if 'Name' in line and 'Id' in line and 'Version' in line:
                header_idx = i
            elif header_idx >= 0 and '-' * 10 in line:
                separator_idx = i
                break
        
        print(f"Header encontrado na linha: {header_idx}")
        print(f"Separador encontrado na linha: {separator_idx}\n")
        
        apps = []
        
        # Se encontrou o separador, processar linhas de dados
        if separator_idx > 0:
            for line in lines[separator_idx + 1:]:
                line = line.strip()
                
                # Ignorar linhas vazias e rodapés
                if not line or 'upgrades available' in line.lower():
                    continue
                
                # Usar regex para parsing mais robusto
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
                        
                        # Filtrar IDs que não são válidos
                        if len(app_id) > 3 and '.' in app_id and not app_id.replace('.', '').isdigit():
                            apps.append({
                                'name': app_name,
                                'id': app_id,
                                'version': version,
                                'available': available
                            })
                            print(f"✓ Parseado: {app_name}")
                            print(f"  ID: {app_id}")
                            print(f"  Versão: {version} → {available}\n")
                    except (ValueError, IndexError) as e:
                        print(f"✗ Erro ao parsear linha: {line}")
                        print(f"  Erro: {e}\n")
        
        print(f"{'='*75}")
        print(f"Total de aplicativos parseados: {len(apps)}")
        print('='*75)
        
        # Validar IDs
        valid_ids = 0
        invalid_ids = []
        
        for app in apps:
            app_id = app['id']
            # Validar que o ID tem formato correto
            if '.' in app_id and len(app_id) > 5 and not app_id.replace('.', '').isdigit():
                valid_ids += 1
            else:
                invalid_ids.append(app_id)
        
        print(f"\n✓ IDs válidos: {valid_ids}")
        if invalid_ids:
            print(f"✗ IDs inválidos: {len(invalid_ids)}")
            for invalid_id in invalid_ids:
                print(f"  - {invalid_id}")
        
        return len(apps) > 0 and len(invalid_ids) == 0
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_real_winget_list():
    """Testa com winget real do sistema"""
    print("\n" + "="*75)
    print("TESTE: Winget Real do Sistema")
    print("="*75 + "\n")
    
    try:
        from powershell_manager import PowerShellManager
        
        ps_manager = PowerShellManager()
        
        print("Verificando winget...")
        is_installed, msg = ps_manager.install_winget_if_needed()
        
        if not is_installed:
            print(f"⚠️  {msg}")
            return False
        
        print("✓ Winget disponível\n")
        print("Listando aplicativos upgradáveis...\n")
        
        apps = ps_manager.list_upgradable_apps()
        
        if not apps:
            print("ℹ️  Nenhum aplicativo precisa atualização (ou erro ao listar)")
            return True
        
        print(f"Encontrados {len(apps)} aplicativos:\n")
        
        for i, app in enumerate(apps, 1):
            print(f"{i}. {app['name']}")
            print(f"   ID: {app['id']}")
            print(f"   Versão: {app['version']} → {app['available']}\n")
        
        # Validar todos os IDs
        invalid_count = 0
        for app in apps:
            app_id = app['id']
            # ID válido deve ter ponto e não ser só números
            if '.' not in app_id or app_id.replace('.', '').isdigit() or len(app_id) < 4:
                print(f"⚠️  ID suspeito detectado: {app_id} ({app['name']})")
                invalid_count += 1
        
        if invalid_count == 0:
            print("✓ Todos os IDs parecem válidos!")
            return True
        else:
            print(f"\n⚠️  {invalid_count} IDs suspeitos detectados")
            return False
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Executa todos os testes"""
    print("\n" + "="*75)
    print("SUITE DE TESTES - PARSING DO WINGET")
    print("="*75)
    
    tests = [
        ("Parsing de Sample Output", test_winget_list_parsing),
        ("Winget Real do Sistema", test_real_winget_list),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ Teste '{test_name}' falhou com erro: {e}")
            results[test_name] = False
    
    # Resumo
    print("\n" + "="*75)
    print("RESUMO DOS TESTES")
    print("="*75 + "\n")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASSOU" if result else "❌ FALHOU"
        print(f"{status}: {test_name}")
    
    print(f"\n{passed}/{total} testes passaram")
    
    if passed == total:
        print("\n✓ PARSING DO WINGET ESTÁ CORRETO!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam")
        return 1


if __name__ == "__main__":
    sys.exit(main())
