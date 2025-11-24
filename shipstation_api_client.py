import requests
from requests.auth import HTTPBasicAuth
from configloader import ConfigLoader

import logging
logger = logging.getLogger(__name__)

class ShipStationAPIClient:
    def __init__(self):
        # V1 params
        self.url_v1 = "https://ssapi.shipstation.com"
        self.api_key_v1 = ""
        self.api_key_secret_v1 = ""
        self.auth_v1 = None

        self.load_keys()

    def load_keys(self):
        try:
            config_data = ConfigLoader("shipstation_api").load_config()
            self.api_key_v1 = config_data["api_key_v1"]
            self.api_key_secret_v1 = config_data["api_key_secret_v1"]
            self.auth_v1 = HTTPBasicAuth(self.api_key_v1, self.api_key_secret_v1)
            logger.info("ShipStation API keys loaded")
        except Exception as e:
            logger.error(f"Error loading ShipStation API keys: {e}")

    # V1 API
    def get_order_by_order_number(self, order_number):
        order_id = self.get_order_id_by_order_number(order_number)
        url = f"{self.url_v1}/orders/{order_id}"
        response = requests.get(url, auth=self.auth_v1)
        response.raise_for_status()
        return response.json()

    def get_order_id_by_order_number(self, order_number):
        url = f"{self.url_v1}/orders"
        params = {
            'orderNumber': order_number
        }
        response = requests.get(url, auth=self.auth_v1, params=params)
        response.raise_for_status()
        orders = response.json().get('orders', [])
        if orders:
            return orders[0]['orderId']
        else:
            raise ValueError(f"Order number {order_number} not found")
        
if __name__ == "__main__":
    api_client = ShipStationAPIClient()
    response = api_client.get_order_by_order_number("104474")
    print(response)