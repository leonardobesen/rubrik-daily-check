import os
import connection.connect as connect
import view.write_to_csv as write_to_csv
from wrapper import request

# Global variables
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(ROOT_DIR, 'reports')
CONFIG_FILE = os.path.join(ROOT_DIR, 'configuration', 'credencials.json')


if __name__ == '__main__':
    
    # Establish connection with Rubrik CDM and Cluster name
    rsc_access_token = connect.open_session(CONFIG_FILE)

    report = {}
    report["sortBy"] = "ProtectedOn",
    report["sortOrder"] = "desc",
    report["limit"] = 1000

    object_report = request('GET', rsc_access_token, data=report)

    # Send data somewhere
    print("Writing to file")
    write_to_csv.create_file(REPORT_PATH)

    connect.close_session(rsc_access_token)