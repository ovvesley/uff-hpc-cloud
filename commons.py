from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient import discovery
import time

load_dotenv()

PROJECT_ID: str = os.getenv('PROJECT_ID')
ZONE: str = os.getenv('ZONE')

credentials: Credentials = Credentials.from_service_account_file(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
compute = discovery.build('compute', 'v1', credentials=credentials)

def get_instance_status(instance_name: str) -> Optional[str]:
    """Verifica o status da instância."""
    try:
        result: Dict[str, Any] = compute.instances().get(project=PROJECT_ID, zone=ZONE, instance=instance_name).execute()
        return result['status']
    except Exception as e:
        return None 

def create_instance(instance_name: str, family_type="e2-medium", startup_script="") -> Dict[str, Any]:
    """Cria uma nova máquina virtual com Ubuntu."""
    config: Dict[str, Any] = {
        "name": instance_name,
        "machineType": f"zones/{ZONE}/machineTypes/{family_type}",
        "disks": [
            {
                "boot": True,
                "autoDelete": True,
                "initializeParams": {
                    "sourceImage": "projects/ubuntu-os-cloud/global/images/family/ubuntu-2004-lts"
                }
            }
        ],
        "networkInterfaces": [
            {
                "network": "global/networks/default",
                "accessConfigs": [
                    {"type": "ONE_TO_ONE_NAT", "name": "External NAT"}
                ]
            }
        ],
        "metadata": {
            "items": [
                {
                    "key": "startup-script",
                    "value": startup_script
                }
            ]
        }
    }
    return compute.instances().insert(project=PROJECT_ID, zone=ZONE, body=config).execute()

def start_instance(instance_name: str) -> Dict[str, Any]:
    """Inicia a instância se ela já existir."""
    return compute.instances().start(project=PROJECT_ID, zone=ZONE, instance=instance_name).execute()

def stop_instance(instance_name: str) -> Dict[str, Any]:
    """Para a instância."""
    return compute.instances().stop(project=PROJECT_ID, zone=ZONE, instance=instance_name).execute()

def wait_for_operation(operation: Dict[str, Any]) -> None:
    """Aguarda uma operação do Google Cloud ser concluída."""
    print('Waiting for operation to finish...')
    while True:
        result: Dict[str, Any] = compute.zoneOperations().get(project=PROJECT_ID, zone=ZONE, operation=operation['name']).execute()
        if result['status'] == 'DONE':
            print("Operation complete.")
            break
        time.sleep(5)

def create_or_run_instance(instance_name: str, family_type="e2-medium", startup_script="") -> None:
    """Verifica, inicia ou cria a instância."""
    status: Optional[str] = get_instance_status(instance_name)
    
    if status is None:
        print(f"Instance {instance_name} does not exist. Creating...")
        operation: Dict[str, Any] = create_instance(instance_name, family_type, startup_script)
        wait_for_operation(operation)
    elif status == 'TERMINATED':
        print(f"Instance {instance_name} is terminated. Starting...")
        set_startup_script(instance_name, get_startup_script())
        operation: Dict[str, Any] = start_instance(instance_name)
        wait_for_operation(operation)
    else:
        print(f"Instance {instance_name} is already running.")

def set_startup_script(instance_name: str, startup_script: str) -> Dict[str, Any]:
    """Define um script de inicialização para a instância."""
    try:
        instance = compute.instances().get(project=PROJECT_ID, zone=ZONE, instance=instance_name).execute()
        fingerprint = instance['metadata']['fingerprint']
        
        config: Dict[str, Any] = {
            "fingerprint": fingerprint,
            "items": [
                {
                    "key": "startup-script",
                    "value": startup_script
                }
            ]
        }
        
        return compute.instances().setMetadata(project=PROJECT_ID, zone=ZONE, instance=instance_name, body=config).execute()
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

def get_startup_script(script_name: str) -> str:
    """Retorna o script de inicialização."""
    with open(script_name, 'r') as file:
        return file.read()
