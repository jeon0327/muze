#!/bin/bash
echo "Stopping httpd"
sudo systemctl stop httpd || true
