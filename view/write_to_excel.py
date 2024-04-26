import pandas as pd
import os
from enum import Enum
from datetime import datetime
from configuration.configuration import get_root_dir
from model.cluster import Cluster
from model.live_mount import LiveMount
from model.data_source import VCenter, Nas
from model.job import Job
from model.security import ServicesAccount, SSOCertificate
from services.formatter import format_timedelta


class Sheets(Enum):
    CAPACITY = 'Capacity'
    CLUSTER = 'Cluster_Health_Check'
    COMPLIANCE = 'Cluster_Compliance'
    MOUNT = 'Live_Mounts'
    JOB = 'Long_Running_Jobs'
    VCENTER = 'vCenter_Status'
    ACCOUNT = 'Service_Accounts_Status'
    CERTIFICATE = 'SSO_Certificate_Status'
    NAS = 'NAS_Disconnected'


def create_empty_file() -> str:
    # Get current datetime formatted
    now = datetime.now().strftime("%d-%m-%Y_%H_%M_%S")
    file_name = f'Rubrik_Environment_Health_Check_{now}.xlsx'
    report_path = os.path.join(get_root_dir(), 'reports', file_name)
    return report_path


def generate_report(cluster_info: list[Cluster],
                    live_mount_info: list[LiveMount],
                    vcenter_info: list[VCenter],
                    certificate_info: list[SSOCertificate],
                    account_info: list[ServicesAccount],
                    nas_info: list[Nas],
                    job_info: list[Job]) -> str:
    REPORT_FILE = create_empty_file()

    writer = pd.ExcelWriter(REPORT_FILE, engine='openpyxl')

    writer = write_cluster_data(writer, cluster_info)
    writer = write_live_mount_data(writer, live_mount_info)
    writer = write_vcenter_data(writer, vcenter_info)
    writer = write_job_data(writer, job_info)
    writer = write_nas_data(writer, nas_info)
    writer = write_certificate_data(writer, certificate_info)
    writer = write_account_data(writer, account_info)

    writer.close()  # Save the Excel file

    return REPORT_FILE


def write_job_data(writer: pd.ExcelWriter, job_info: list[Job]) -> pd.ExcelWriter:
    # Add empty sheets to the workbook
    writer.book.create_sheet(title=Sheets.JOB.value)

    # Write cluster status to sheet
    df_cluster = pd.DataFrame([{
        'Cluster': job.cluster_name,
        'Event Series Id': job.id,
        'Object Name': job.object_name,
        'Object Type': job.object_type,
        'Start Time': job.start_time,
        'Duration': format_timedelta(job.duration),
        'Job Status': job.job_status,
        'Job Type': job.job_type,
        'SLA Domain': job.sla_name
    } for job in job_info])
    df_cluster.to_excel(writer, sheet_name=Sheets.JOB.value, index=False)

    return writer


def write_nas_data(writer: pd.ExcelWriter, nas_info: list[Nas]) -> pd.ExcelWriter:
    # Add empty sheets to the workbook
    writer.book.create_sheet(title=Sheets.NAS.value)

    # Write cluster status to sheet
    df_cluster = pd.DataFrame([{
        'Cluster': nas.cluster_name,
        'Object Id': nas.id,
        'Name': nas.name,
        'Connection Status': nas.connection_status
    } for nas in nas_info])
    df_cluster.to_excel(writer, sheet_name=Sheets.NAS.value, index=False)

    return writer


def write_account_data(writer: pd.ExcelWriter, account_info: list[ServicesAccount]) -> pd.ExcelWriter:
    # Add empty sheets to the workbook
    writer.book.create_sheet(title=Sheets.ACCOUNT.value)

    # Write cluster status to sheet
    df = pd.DataFrame([{
        'Name': account.name,
        'Description': account.description,
        'Last Login': account.last_login
    } for account in account_info])
    df.to_excel(writer, sheet_name=Sheets.ACCOUNT.value, index=False)

    return writer


def write_certificate_data(writer: pd.ExcelWriter, certificate_info: list[SSOCertificate]) -> pd.ExcelWriter:
    # Add empty sheets to the workbook
    writer.book.create_sheet(title=Sheets.CERTIFICATE.value)

    # Write cluster status to sheet
    df = pd.DataFrame([{
        'Name': certificate.name,
        'Expiration Date': certificate.expiration_date
    } for certificate in certificate_info])
    df.to_excel(
        writer, sheet_name=Sheets.CERTIFICATE.value, index=False)

    return writer


def write_vcenter_data(writer: pd.ExcelWriter, vcenter_info: list[VCenter]) -> pd.ExcelWriter:
    # Add empty sheets to the workbook
    writer.book.create_sheet(title=Sheets.VCENTER.value)

    # Write cluster status to sheet
    df = pd.DataFrame([{
        'Cluster Name': vcenter.cluster_name,
        'Name': vcenter.name,
        'Status': vcenter.status,
        'Status Message': vcenter.status_message,
        'Last Refresh Time': vcenter.last_refresh_time
    } for vcenter in vcenter_info])
    df.to_excel(writer, sheet_name=Sheets.VCENTER.value, index=False)

    return writer


def write_live_mount_data(writer: pd.ExcelWriter, live_mount_info: list[LiveMount]) -> pd.ExcelWriter:
    # Add empty sheets to the workbook
    writer.book.create_sheet(title=Sheets.MOUNT.value)

    # Write cluster status to sheet
    df = pd.DataFrame([{
        'Cluster Name': live_mount.cluster_name,
        'Live Mount Type': live_mount.type,
        'Name': live_mount.name,
        'Mounted Date': live_mount.date
    } for live_mount in live_mount_info])
    df.to_excel(writer, sheet_name=Sheets.MOUNT.value, index=False)

    return writer


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
    } for cluster in cluster_info])
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
            percent_in_compliance = round(
                (cluster.in_compliance_count / total_object_count) * 100, 1)
            percent_out_of_compliance = round(
                (cluster.out_of_compliance_count / total_object_count) * 100, 1)
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
    df_compliance.to_excel(
        writer, sheet_name=Sheets.COMPLIANCE.value, index=False)

    return writer
