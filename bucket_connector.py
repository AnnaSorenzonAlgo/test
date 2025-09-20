from google.cloud import storage
from google.oauth2 import service_account
from pathlib import Path
from google_connector import credentials_config
import os
from utils.conf_init import cfg

class GoogleStorageManager:    

    def __init__(self):

        credentials_info = credentials_config.credentials_info
        credentials = service_account.Credentials.from_service_account_info(credentials_info)
        self.client = storage.Client(credentials=credentials, project=credentials.project_id)       
        self.bucket = self.client.bucket(credentials_info['bucket_name'])
        self.root_folder = cfg.get('google_connector', None).get('root_folder')

    def _get_content_type(self, file_path: str):
        ext = Path(file_path).suffix.lower()
        content_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.json': 'application/json',
            '.zip': 'application/zip'
        }
        return content_types.get(ext, 'application/octet-stream')
    
    def upload_file_bytes(self, file_bytes: bytes, destination_blob_name: str):
        blob = self.bucket.blob(destination_blob_name)        
        content_type = self._get_content_type(destination_blob_name) 

        blob.upload_from_string(file_bytes, content_type)
        print(f"Uploaded {destination_blob_name}")

    def upload_file(self, file_name:str):     
        file_path = os.path.join(self.root_folder, file_name)   
        blob = self.bucket.blob(file_name)        
        content_type = self._get_content_type(file_path)
         
        blob.upload_from_filename(file_path, content_type)
        print(f"Uploaded {file_path}")
    
    def list_all_blobs(self):
        return list(self.client.list_blobs(self.bucket))

    def download_blob(self, blob_name: str, destination_file_path: str):
        blob = self.bucket.blob(blob_name)
        blob.download_to_filename(destination_file_path)
        print(f"Downloaded {blob_name} → {destination_file_path}")

gmanager = GoogleStorageManager()

