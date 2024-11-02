import os
import time

from googleapiclient import discovery
from google.oauth2.service_account import Credentials

from typing import Optional

from commons import create_or_run_instance, get_instance_status, get_startup_script

PROJECT_ID: str = os.getenv('PROJECT_ID')
ZONE: str = os.getenv('ZONE')

credentials: Credentials = Credentials.from_service_account_file(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
compute = discovery.build('compute', 'v1', credentials=credentials)
def mpi() -> None:
    instance01: str = 'instance-01-medium'
    instance02: str = 'instance-02-medium'
    instance03: str = 'instance-03-medium'
    
    create_or_run_instance(instance01, family_type="e2-medium", startup_script=get_startup_script("mpi/startup01.c"))
    create_or_run_instance(instance02, family_type="e2-medium", startup_script=get_startup_script("mpi/startup01.c"))
    create_or_run_instance(instance03, family_type="e2-medium", startup_script=get_startup_script("mpi/startup01.c"))

    for instance in [instance01, instance02, instance03]:
        status: Optional[str] = get_instance_status(instance)
        print(f"{instance} is {status}")
