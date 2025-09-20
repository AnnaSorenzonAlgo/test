import os
import zipfile
import subprocess
import utils.conf_init as global_config

class FolderHelper:  

    @staticmethod
    def _get_root_folder():
        return global_config.cfg.get('google_connector', None).get('root_folder')

    @staticmethod
    def zip_subfolder(folder_name):
        root_folder = FolderHelper._get_root_folder()

        item_path = os.path.join(root_folder, folder_name)
        zip_path = ''
        if os.path.isdir(item_path):
            zip_path = os.path.join(root_folder, f"{folder_name}.zip")
            FolderHelper._zip_directory(item_path, zip_path)
            print(f"Zipped {item_path} -> {zip_path}")     

        return os.path.basename(zip_path)   
           
    @staticmethod
    def _zip_directory(dir_path, zip_path):

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=dir_path)
                    zipf.write(file_path, arcname) 

    @staticmethod
    def remove_folder(folder_name):
        root_folder = FolderHelper._get_root_folder()
        folder_path = os.path.join(root_folder, folder_name)
        zip_path = os.path.join(root_folder, f"{folder_name}.zip")

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

    @staticmethod
    def get_all_folders():
        folders = []
        root_folder = FolderHelper._get_root_folder()
        for item in os.listdir(root_folder):
            folders.append(item)
        return folders
    
    @staticmethod
    def get_unzipped_subfolders():
        folders = []
        root_folder = FolderHelper._get_root_folder()
        for item in os.listdir(root_folder):
            item_path = os.path.join(root_folder, item)
            # Check if it's a directory
            if os.path.isdir(item_path):
                zip_filename = f"{item}.zip"
                zip_path = os.path.join(root_folder, zip_filename)
                # Check if ZIP exists
                if not os.path.isfile(zip_path):
                    # No ZIP found for this subfolder
                    folders.append(item_path)

        return folders

        
