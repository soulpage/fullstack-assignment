#!/bin/bash
    # Update package lists
    sudo apt update -y

    # Install required dependencies
    sudo apt install -y curl tar

    # Create a directory for the GitHub Actions runner
    mkdir -p /home/ubuntu/actions-runner
    cd /home/ubuntu/actions-runner

    # Download the latest GitHub Actions runner package
    curl -o actions-runner-linux-x64-2.319.1.tar.gz -L https://github.com/actions/runner/releases/download/v2.319.1/actions-runner-linux-x64-2.319.1.tar.gz

    # Extract the package
    tar xzf ./actions-runner-linux-x64-2.319.1.tar.gz

    # Configure the runner
    ./config.sh --url https://github.com/KANDUKURIsaikrishna/fullstack-assignment --token AMBLTQBV5ZG7ARBEJ3X3KSLG2CX5Q --unattended --replace

    # Install and start the runner as a service
    #sudo ./svc.sh install
    #sudo ./svc.sh start
    ./run.sh

    