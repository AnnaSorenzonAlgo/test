import json
from utils.conf_init import cfg

class CredentialsConfig:
    __CREDENTIALS_FILE = cfg.get('google_connector', None).get('config_file')

    def __init__(self):
        with open(self.__CREDENTIALS_FILE, 'r') as f:
            self.credentials_info = json.load(f)

    def get_credentials_info(self):
        return self.credentials_info
    
credentials_config = CredentialsConfig()
