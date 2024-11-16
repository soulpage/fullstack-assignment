#!/bin/bash
# For Ubuntu 22.04

# Setup Environment For Nextjs Application
sudo apt update -y
sudo apt install npm -y
sudo npm install -g n
sudo n 18.20.5

# Setup Enviroment For Django Application
sudo apt update -y
sudo apt install python3-venv -y
sudo python3 -m venv .venv
source /.venv/bin/activate
