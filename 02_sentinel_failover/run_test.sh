#!/bin/bash

echo "=== Running Failover Monitor Test ==="
echo "Ensure your docker containers are running (docker-compose up -d)"
echo "Press Ctrl+C to stop."

python failover_monitor_docker.py
