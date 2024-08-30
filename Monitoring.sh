#!/bin/bash
    # Install Prometheus
    cd ~
    wget https://github.com/prometheus/prometheus/releases/download/v2.41.0/prometheus-2.41.0.linux-amd64.tar.gz
    tar xvfz prometheus-2.41.0.linux-amd64.tar.gz
    cd prometheus-2.41.0.linux-amd64/

    # Install Grafana
    cd ~
    wget https://dl.grafana.com/oss/release/grafana-9.5.0.linux-amd64.tar.gz
    tar -zxvf grafana-9.5.0.linux-amd64.tar.gz
    cd grafana-9.5.0/
    sudo ./bin/grafana-server web &