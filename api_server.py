from fastapi import FastAPI, HTTPException, Header
import uvicorn
from pydantic import BaseModel
from configloader import ConfigLoader
import webbrowser
import uuid
import threading

import logging
logger = logging.getLogger(__name__)

class APIServer:
    def __init__(self, shutdown_event: threading.Event):
        self.shutdown_event = shutdown_event
        self.app = FastAPI()
        self.api_host = "0.0.0.0"
        self.api_port = 8000
        self.api_key = None

        self.load_config()

        #Routes
        @self.app.post("/open_order_webpage")
        def open_order_webpage(req: OpenOrderRequest, authorisation: str = Header(None)):
            if authorisation != self.api_key:
                raise HTTPException(status_code=401, detail="Unauthorized")
            
            self.open_order_search_webpage(req.order_number)

    def load_config(self):
        try:
            config_data = ConfigLoader("api_server").load_config()
            self.api_key = config_data["api_key"]

        except Exception as e:
            logger.error(f"Error loading API server config: {e}")

    def open_order_search_webpage(self, order_number: str):
        url = f"https://ship14.shipstation.com/orders/all-orders-search-result?quickSearch={order_number}"
        logger.debug(f"Opening order webpage: {url}")
        webbrowser.open(url)

    def run_api_server(self):
        config = uvicorn.Config(
            app=self.app,
            host=self.api_host,
            port=self.api_port,
            log_level="info",
            reload=False
        )

        server = uvicorn.Server(config)
        def watch_for_shutdown():
            self.shutdown_event.wait()
            server.should_exit = True
        
        watcher = threading.Thread(target=watch_for_shutdown, daemon=True)
        watcher.start()
        server.run()
        logger.info("API server shut down.")

class OpenOrderRequest(BaseModel):
    order_number: int

if __name__ == "__main__":
    # Run this to generate an api key config file
    new_api_key = str(uuid.uuid4())
    ConfigLoader("api_server").save_config({"api_key": new_api_key})
    print("API server config file created with new API key.")