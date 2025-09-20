from google_connector.folder_helper import folder_helper
from google_connector.bucket_connector import gmanager
import utils.decision_aggregator as utils

class DataSender:
    @staticmethod

    def send_zipped_folders():
        folders_to_send = folder_helper.get_unzipped_subfolders()

        for item in folders_to_send:
            res = utils.get_session_majority(item)
            if res is None:
                print("No decision found")
            else:  
                label = res
                print(f"Majority decision: {label}")
                # Update Scaninfo.json with detected aisle and timestamps
                ok = utils.update_scaninfo(item, label)
                print(f"Scaninfo updated: {ok}")

                zip_file_name = folder_helper.zip_subfolder(item)          
                gmanager.upload_file(zip_file_name)
                folder_helper.remove_folder(item)


