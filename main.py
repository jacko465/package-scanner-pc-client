from api_server import APIServer
from package_scanner_api_client import PackageScannerAPIClient
from shipstation_api_client import ShipStationAPIClient

import os
from time import sleep
import threading
import signal
import sys

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
file_handler.setLevel(logging.DEBUG)
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

# Global stop flag for service shutdown
stop_requested = threading.Event()

def request_stop(reason: str):
    if not stop_requested.is_set():
        logger.info(f"Stop requested ({reason})")
        stop_requested.set()

def _handle_signal(signum, frame):
    # Called on service stop / Ctrl+C / Ctrl+Break (depending on platform)
    try:
        signame = signal.Signals(signum).name
    except Exception:
        signame = str(signum)
    request_stop(signame)

# Register handlers (Windows services commonly trigger terminate/ctrl-break paths)
for sig_name in ("SIGTERM", "SIGINT", "SIGBREAK"):
    if hasattr(signal, sig_name):
        try:
            signal.signal(getattr(signal, sig_name), _handle_signal)
        except Exception:
            pass

def main():
    api_server_thread = None
    shutdown_event = None

    try:
        while True:
            # shipstation_api_client = ShipStationAPIClient()
            shutdown_event = threading.Event()
            api_server = APIServer(shutdown_event)
            api_server_thread = threading.Thread(target=api_server.run_api_server, daemon=True)
            package_scanner_api_client = PackageScannerAPIClient()

            logger.info("Registering PC client with package scanner API...")
            while True:
                if package_scanner_api_client.register_pc_client_with_scanner(
                    port=api_server.api_port,
                    api_key=api_server.api_key,
                    local_ip=api_server.local_ip
                ):
                    logger.info("PC client successfully registered with package scanner API.")
                    break
                logger.info("Retrying registration in 5 seconds...")
                # interruptible sleep
                if stop_requested.wait(5):
                    break

            if stop_requested.is_set():
                break

            logger.info("Starting API server...")
            api_server_thread.start()
            try:
                while not stop_requested.is_set():
                    connected = package_scanner_api_client.check_connection_is_active()
                    if not connected:
                        logger.info("Connection to package scanner API lost.")
                        break
                    if stop_requested.wait(10):
                        break
            finally:
                logger.info("Shutting down API server...")
                shutdown_event.set()
                api_server_thread.join()
                logger.info("API server shut down.")
    finally:
        logger.info("Shutting down...")
        if shutdown_event:
            shutdown_event.set()
        if api_server_thread:
            api_server_thread.join()
        logger.info("Companion client shut down gracefully.")


if __name__ == "__main__":
    main()