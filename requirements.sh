#!/bin/bash
    apt-get update -y
    apt-get install -y docker.io
    apt-get install -y python3-pip
    apt-get install -y nodejs npm
    systemctl start docker
    systemctl enable docker
    usermod -aG docker ubuntu
    curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
    apt-get install -y nodejs
    pip3 install virtualenv