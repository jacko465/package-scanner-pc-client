# package-scanner-pc-client

PC companion client for the package scanner project. Runs a local API server on the PC, polls the package scanner device for scan events, and looks up shipment details via the ShipStation API.

## Configuration

### `config/api_server.cfg`
Set `local_ip` to the IP address of **this machine** on your local network. The `api_key` defined here is used to authenticate incoming requests to this PC's API server.

```json
{
    "api_key": "<your-chosen-api-key>",
    "local_ip": "192.168.1.x"
}
```

### `config/package_scanner_api.cfg`
Set `host` to the IP address of the **package scanner device**. The `api_key` here must match the API key configured on the package scanner itself.

```json
{
    "host": "192.168.1.x",
    "port": 8000,
    "api_key": "<api-key-from-package-scanner>"
}
```

## Running

Install dependencies:
```
pip install -r requirements.txt
```

Start the client:
```
python main.py
```

Logs are written to `log/companion_client.log`.

## Linux Service

Scripts to install/manage a systemd service are in the `linux_service/` directory.

## Virtual Environment Setup

### Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

To deactivate the venv when done, run `deactivate`.

## Compiling to Executable (PyInstaller)

Install PyInstaller:
```
pip install pyinstaller
```

Compile to a single executable:
```
pyinstaller --onefile main.py
```

Without visible console:
```
pyinstaller --onefile --noconsole main.py
```

The compiled executable will be output to the `dist/` directory.
