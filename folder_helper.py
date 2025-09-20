import os
import zipfile
from google_connector import credentials_config
import subprocess
from utils.conf_init import cfg
class FolderHelper:   
    
    def __init__(self):
        credentials_info = credentials_config.credentials_info
        self.root_folder = cfg.get('google_connector', None).get('root_folder')


    def zip_subfolder(self, folder_name):
        item_path = os.path.join(self.root_folder, folder_name)
        zip_path = ''
        if os.path.isdir(item_path):
            zip_path = os.path.join(self.root_folder, f"{folder_name}.zip")
            self._zip_directory(item_path, zip_path)
            print(f"Zipped {item_path} -> {zip_path}")     

        return os.path.basename(zip_path)          

    def _zip_directory(self, dir_path, zip_path):

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=dir_path)
                    zipf.write(file_path, arcname) 

    def remove_folder(self, folder_name):
        folder_path = os.path.join(self.root_folder, folder_name)
        zip_path = os.path.join(self.root_folder, f"{folder_name}.zip")

        folder_removed = False
        if os.path.isdir(folder_path):
            try:
                subprocess.check_call(['rmdir', '/s', '/q', folder_path], shell=True)
                folder_removed = True             
                print(f"Removed folder: {folder_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}; {folder_path}")
        else:
            print(f"Folder not found: {folder_path}")
        
        if folder_removed:
            # Remove ZIP file if it exists
            if os.path.isfile(zip_path):
                try:
                    os.remove(zip_path)
                    print(f"Removed ZIP: {zip_path}")
                except PermissionError:
                    print(f"Permission denied when trying to remove: {zip_path}")
                except Exception as e:
                    print(f"Error removing ZIP file: {zip_path}. Error: {e}")
            else:
                print(f"ZIP file not found: {zip_path}")

    def get_all_folders(self):
        folders = []
        for item in os.listdir(self.root_folder):
            folders.append(item)
        return folders
    
    def get_unzipped_subfolders(self):
        folders = []

        for item in os.listdir(self.root_folder):
            item_path = os.path.join(self.root_folder, item)
            # Check if it's a directory
            if os.path.isdir(item_path):
                zip_filename = f"{item}.zip"
                zip_path = os.path.join(self.root_folder, zip_filename)
                # Check if ZIP exists
                if not os.path.isfile(zip_path):
                    # No ZIP found for this subfolder
                    folders.append(item_path)

        return folders

folder_helper = FolderHelper()
        
