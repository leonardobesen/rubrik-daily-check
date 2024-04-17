import pandas as pd
import os
from enum import Enum
from datetime import datetime
from configuration.configuration import get_root_dir


class Sheets(Enum):
    CAPACITY = 'Capacity'
    CLUSTER = 'Cluster_Health_Check'
    MOUNT = 'Live_Mounts'
    OBJECTS = 'Num_Objects'
    JOBS = 'Long_Running_Jobs'
    VCENTER = 'vCenter_Status'
    API = 'API_Token_Status'
    CERTIFICATE = 'AD_Certificate_Status'
    NAS = 'NAS_Disconnected'
    


def create_file():
    # Get now datetime info formatted
    now = datetime.now().strftime("%d-%m-%Y_%H_%M_%S")

    # Set path and file information
    file_name = 'Rubrik_Enviroment_Health_Check_{date}.xlsx'.format(date=now)
    report_path = os.path.join(get_root_dir(), 'reports', file_name)

    return report_path


def update_report(cluster_info: dict):
    REPORT_FILE = create_file()

    writer = pd.ExcelWriter(REPORT_FILE, engine='openpyxl')

    writer.close()
