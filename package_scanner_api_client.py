import requests
import socket
from configloader import ConfigLoader

import logging
logger = logging.getLogger(__name__)

class PackageScannerAPIClient:
    def __init__(self):
        self.config_name = "package_scanner_api"
        
        self.host = None
        self.port = None
        self.api_key = None
        self.base_url = None

        self.load_config()

    def load_config(self):
        config_data = ConfigLoader(self.config_name).load_config()
        self.host = config_data["host"]
        self.port = config_data["port"]
        self.api_key = config_data["api_key"]
        self.base_url = f"http://{self.host}:{self.port}"

    def register_pc_client_with_scanner(self, port: int, api_key: str):
        local_ip = self.get_local_ip()
        url = f"{self.base_url}/register_companion_client"
        
        data = {
            "host": local_ip,
            "port": port,
            "api_key": api_key
        }

        headers = {
            "authorisation": self.api_key
        }

        try:
            logger.debug(f"Registering PC client at {local_ip}:{port} with package scanner API...")
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            logger.info("Successfully registered PC client with package scanner.")
            return True
        except requests.RequestException as e:
            logger.error(f"Failed to register PC client with package scanner: {e}")
            return False

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip