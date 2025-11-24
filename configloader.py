import os
import json

class ConfigLoader:
    def __init__(self, config_name):
        self.config_name = config_name
        self.config_path = os.path.join("config", f"{self.config_name}.cfg")

        os.makedirs("config", exist_ok=True)

    def load_config(self):
        with open(self.config_path, 'r') as file:
            config_data = json.load(file)
        return config_data
    
    def save_config(self, config_data):
        with open(self.config_path, 'w') as file:
            json.dump(config_data, file, indent=4)

# if __name__ == "__main__":
#     data = {
#         "host": "",
#         "port": 0,
#         "api_key": ""
#     }
#     # ConfigLoader("package_scanner_api").save_config(data)