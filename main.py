import connection.connect as connect
import view.write_to_excel as write_to_excel
from controller import cluster_controller, live_mount_controller, vcenter_controller, security_controller


if __name__ == '__main__':
   # Establish connection with Rubrik RSC
   rsc_access_token = connect.open_session()

   print("Collecting Data...")
   cluster_info = cluster_controller.get_all_cluster_info(access_token=rsc_access_token)
   live_mount_info = live_mount_controller.get_all_live_mounts_info(access_token=rsc_access_token)
   vcenter_info = vcenter_controller.get_all_vcenter_info(access_token=rsc_access_token)
   certificate_info = security_controller.get_all_certificate_info(access_token=rsc_access_token)
   account_info = security_controller.get_all_service_account_info(access_token=rsc_access_token)

   print("Writing to file...")
   file_path = write_to_excel.generate_report(
      cluster_info=cluster_info,
      live_mount_info=live_mount_info,
      vcenter_info=vcenter_info,
      certificate_info=certificate_info,
      account_info=account_info
   )

   print(f"Saved to {file_path}")

   # Close session
   connect.close_session(rsc_access_token)