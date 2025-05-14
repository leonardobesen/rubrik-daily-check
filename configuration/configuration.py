import os
import json
from services.validations import clear_empty_strings
from pathlib import Path
from typing import Optional

# Global variables
ROOT_DIR = str(Path(__file__).resolve().parent.parent)
REPORT_PATH = os.path.join(ROOT_DIR, 'reports')
CONFIG_FILE = os.path.join(ROOT_DIR, 'configuration', 'config.json')

# Global variable to store configuration data
CONFIG = None


def load_config():
    global CONFIG
    if CONFIG is None:
        with open(CONFIG_FILE, 'r') as json_file:
            CONFIG = json.load(json_file)
    return CONFIG


def get_root_dir() -> str:
    return ROOT_DIR


def get_timezone_info() -> str:
    config = load_config()

    TZ_INFO_DEFAULT = "UTC"

    try:
        TZ_INFO = config["tz_info"]

        if TZ_INFO == "":
            return TZ_INFO_DEFAULT

        return TZ_INFO
    except KeyError:
        return TZ_INFO_DEFAULT


def get_google_config_path() -> Optional[str]:
    try:
        GOOGLE_FILE = os.path.join(
            ROOT_DIR, 'configuration', 'google_drive.json')
        return GOOGLE_FILE
    except:
        raise ValueError(
            "Unable to find Google Drive OAuth Crendential file 'google_drive.json' on configuration folder")


def get_drive_folder_id() -> Optional[list[str]]:
    config = load_config()

    try:
        FOLDER_IDS = config["google_drive_upload_folder_ids"]
    except KeyError:
        return None

    FOLDER_IDS = clear_empty_strings(FOLDER_IDS)

    if not len(FOLDER_IDS) > 0:
        return None

    return FOLDER_IDS


def get_excluded_clusters_uuids() -> Optional[list[str]]:
    config = load_config()

    try:
        EXCLUDED_CLUSTERS = config["excluded_clusters_uuids"]
    except KeyError:
        return None

    EXCLUDED_CLUSTERS = clear_empty_strings(EXCLUDED_CLUSTERS)

    if len(EXCLUDED_CLUSTERS) == 0:
        return None

    return EXCLUDED_CLUSTERS
