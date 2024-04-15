import connection.connect as connect
import view.write_to_csv as write_to_csv
from controller import querier


if __name__ == '__main__':
    # Establish connection with Rubrik RSC
    rsc_access_token = connect.open_session()

    # print(querier.get_all_cluster_info(access_token=rsc_access_token))

    # Send data somewhere
    print("Writing to file")
    # write_to_csv.create_file(REPORT_PATH)

    # Close connection
    connect.close_session(rsc_access_token)