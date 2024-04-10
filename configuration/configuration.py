import os
from pathlib import Path
import json

# Global variables
ROOT_DIR = str(Path(__file__).resolve().parent.parent)
REPORT_PATH = os.path.join(ROOT_DIR, 'reports')
CONFIG_FILE = os.path.join(ROOT_DIR, 'configuration', 'config.json')

def load_config():
    with open(CONFIG_FILE, 'r') as json_file:
        CONFIG = json.load(json_file)

    return CONFIG