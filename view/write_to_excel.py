import pandas as pd
import os
from enum import Enum
from datetime import datetime
from configuration.configuration import get_root_dir
from model.cluster import Cluster


class Sheets(Enum):
    CAPACITY = 'Capacity'
    CLUSTER = 'Cluster_Health_Check'
    COMPLIANCE = 'Cluster_Compliance'
    #MOUNT = 'Live_Mounts'
    #JOBS = 'Long_Running_Jobs'
    #VCENTER = 'vCenter_Status'
    #API = 'API_Token_Status'
    #CERTIFICATE = 'AD_Certificate_Status'
    #NAS = 'NAS_Disconnected'
    

def create_file() -> str:
    # Get current datetime formatted
    now = datetime.now().strftime("%d-%m-%Y_%H_%M_%S")
    file_name = f'Rubrik_Environment_Health_Check_{now}.xlsx'
    report_path = os.path.join(get_root_dir(), 'reports', file_name)
    return report_path


def generate_report(cluster_info: list[Cluster]) -> str:
    REPORT_FILE = create_file()

    writer = pd.ExcelWriter(REPORT_FILE, engine='openpyxl')
    
    writer = write_cluster_data(writer, cluster_info)

    writer.close()  # Save the Excel file

    return REPORT_FILE


def write_cluster_data(writer: pd.ExcelWriter, cluster_info: list[Cluster]) -> pd.ExcelWriter:
        # Add empty sheets to the workbook
    writer.book.create_sheet(title=Sheets.CLUSTER.value)
    writer.book.create_sheet(title=Sheets.CAPACITY.value)
    writer.book.create_sheet(title=Sheets.COMPLIANCE.value)

    # Write cluster status to sheet
    df_cluster = pd.DataFrame([{
        'Name': cluster.name,
        'Cluster System Status': cluster.system_status,
        'Protection Paused Status': cluster.pause_status,
        'Cluster Connection Status': cluster.status,
        'RSC Connection with Cluster': cluster.connected_state,
        'Passed RSC Connection Test': cluster.passed_connection_test,
        'Last RSC Connection Time': cluster.last_connection_time
    }  for cluster in cluster_info])
    df_cluster.to_excel(writer, sheet_name=Sheets.CLUSTER.value, index=False)

    # Write cluster capacity to sheet
    df_capacity = pd.DataFrame([{
        'Name': cluster.name,
        'Total Capacity (TB)': cluster.total_capacity,
        'Used Capacity (TB)': cluster.used_capacity,
        'Snapshot Capacity (TB)': cluster.snapshot_capacity,
        'System Capacity (TB)': cluster.system_capacity,
        'Available Capacity (TB)': cluster.available_capacity
    } for cluster in cluster_info])
    df_capacity.to_excel(writer, sheet_name=Sheets.CAPACITY.value, index=False)

    # Write cluster compliance to sheet
    compliance_data = []
    for cluster in cluster_info:
        if cluster.in_compliance_count > 0 or cluster.out_of_compliance_count > 0:
            total_object_count = cluster.in_compliance_count + cluster.out_of_compliance_count
            percent_in_compliance = round((cluster.in_compliance_count / total_object_count) * 100, 1)
            percent_out_of_compliance = round((cluster.out_of_compliance_count / total_object_count) * 100, 1)
        else:
            total_object_count = None
            percent_in_compliance = None
            percent_out_of_compliance = None

        compliance_data.append({
            'Name': cluster.name,
            'Total Object Count': total_object_count,
            'In Compliance Count': cluster.in_compliance_count,
            'Out of Compliance Count': cluster.out_of_compliance_count,
            'Percentage In Compliance': percent_in_compliance,
            'Percentage Out of Compliance': percent_out_of_compliance,
            'Compliance Pull Time': cluster.compliance_pull_time
        })

    df_compliance = pd.DataFrame(compliance_data)    
    df_compliance.to_excel(writer, sheet_name=Sheets.COMPLIANCE.value, index=False)

    return writer