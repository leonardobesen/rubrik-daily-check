import os
import json
from pathlib import Path
from typing import Optional

# Global variables
ROOT_DIR = str(Path(__file__).resolve().parent.parent)
REPORT_PATH = os.path.join(ROOT_DIR, 'reports')
CONFIG_FILE = os.path.join(ROOT_DIR, 'configuration', 'config.json')
TZ_INFO = "America/Sao_Paulo"

def load_config():
    with open(CONFIG_FILE, 'r') as json_file:
        CONFIG = json.load(json_file)

    return CONFIG


def get_root_dir() -> str:
    return ROOT_DIR


def get_timezone_info() -> str:
    return TZ_INFO
