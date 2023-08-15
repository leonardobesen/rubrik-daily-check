import pandas as pd
import os
from enum import Enum
from datetime import datetime

class Sheets(Enum):
    CAPACITY    = 'Capacity'
    CLUSTER     = 'Cluster_Health_Check'
    MOUNT       = 'Live_Mounts'
    OBJECTS     = 'Num_Objects'
    VCENTER     = 'vCenter_Status'
    API         = 'API_Token_Status'
    CERTIFICATE = 'AD_Certificate_Status'
    NAS         = 'NAS_Disconnected'
    JOBS        = 'Long_Running_Jobs'
    SQL         = 'SQL_DBs_Removed_from_Backups'

def create_file(ROOT_DIR: str):
    # Get now datetime info formatted
    now = datetime.now().strftime("%d-%m-%Y_%H_%M_%S")

    # Set path and file information
    file_name = 'Rubrik_Enviroment_Health_Check_{date}.xlsx'.format(date=now)
    report_path = os.path.join(ROOT_DIR, 'report_repo', file_name)

    return report_path

def update_report(REPORT_FILE, **data_dict):
    # Get a set of all sheets expected from Enum
    expected_sheets = set(str(sheet.value) for sheet in Sheets)

    # Compare the set of expected sheets with the dict keys received from function call
    if set(data_dict.keys()) != expected_sheets:
        raise ValueError("Data keys must match the sheet names.")

    writer = pd.ExcelWriter(REPORT_FILE, engine='openpyxl')

    # Iterate over the received dict
    for sheet_name, sheet_data in data_dict.items():
        # Get Enum that correspond to the sheet_name from dict
        sheet_enum = next((sheet for sheet in Sheets if sheet.value == sheet_name), None)
        if sheet_enum:
            # Append data to excel sheet
            df = pd.DataFrame(sheet_data)
            start_row = writer.sheets[str(sheet_enum.value)].max_row if str(sheet_enum.value) in writer.sheets else 0
            df.to_excel(writer, sheet_name=str(sheet_enum.value), startrow=start_row, index=False, header=True)

    writer.close()
