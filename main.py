import os
from api_server import APIServer
from package_scanner_api_client import PackageScannerAPIClient
from shipstation_api_client import ShipStationAPIClient
from time import sleep

import logging
# init logging
from logging.handlers import RotatingFileHandler
os.makedirs("log", exist_ok=True)

# log file handler
file_handler = RotatingFileHandler(
    "log/companion_client.log",
    maxBytes=10*1024*1024,  # 10 MB
    backupCount=2
)
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))

# console log handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))

# configure root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)

logger = logging.getLogger(__name__)
logger.info("Logger initialised")

def main():
    # shipstation_api_client = ShipStationAPIClient()
    api_server = APIServer()
    package_scanner_api_client = PackageScannerAPIClient()

    logger.info("Registering PC client with package scanner API...")
    while True:
        if package_scanner_api_client.register_pc_client_with_scanner(
            port=api_server.api_port,
            api_key=api_server.api_key
        ):
            logger.info("PC client successfully registered with package scanner API.")
            break
        logger.info("Retrying registration in 5 seconds...")
        sleep(5)

    logger.info("Starting API server...")
    api_server.run_api_server()


if __name__ == "__main__":
    main()