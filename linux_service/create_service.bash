sudo cp -f package_scanner_client.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable package_scanner_client.service
sudo systemctl start package_scanner_client.service