import connection.connect as connect
import view.write_to_csv as write_to_csv
from controller import manager


if __name__ == '__main__':
    # Establish connection with Rubrik RSC
    rsc_access_token = connect.open_session()

    print(manager.get_all_unmanaged_objects(access_token=rsc_access_token, 
                                            cluster_id="String"))

    # Send data somewhere
    print("Writing to file")
    # write_to_csv.create_file(REPORT_PATH)

    # Close connection
    connect.close_session(rsc_access_token)