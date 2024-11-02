import os
import time

from googleapiclient import discovery
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from typing import Optional

from commons import create_or_run_instance, get_instance_status, get_startup_script

load_dotenv()

PROJECT_ID: str = os.getenv('PROJECT_ID')
ZONE: str = os.getenv('ZONE')

credentials: Credentials = Credentials.from_service_account_file(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
compute = discovery.build('compute', 'v1', credentials=credentials)

def openmp() -> None:
    instance01: str = 'instance-openmp-01-e2-highcpu-8'
    
    create_or_run_instance(instance01, family_type="e2-highcpu-8", startup_script=get_startup_script("openmp/startup-openmp.sh"))
    
    status: Optional[str] = get_instance_status(instance01)

    print(f"{instance01} is {status}")



   