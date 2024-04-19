import connection.connect as connect
import view.write_to_excel as write_to_excel
from controller import cluster_controller


if __name__ == '__main__':
    # Establish connection with Rubrik RSC
    rsc_access_token = connect.open_session()

    cluster_info = cluster_controller.get_all_cluster_info(access_token=rsc_access_token)

    # Send data somewhere
    print("Writing to file")
    write_to_excel.generate_report(
        cluster_info=cluster_info
    )

    # Close connection
    connect.close_session(rsc_access_token)