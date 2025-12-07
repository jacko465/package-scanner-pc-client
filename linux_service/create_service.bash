mkdir -p ~/.config/systemd/user
cp -f package_scanner_client.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable package_scanner_client.service
systemctl --user start package_scanner_client.service