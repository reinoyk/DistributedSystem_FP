#!/bin/bash

echo "=== Setup Scenario 2 (Sentinel Failover) ==="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker Desktop."
    exit 1
fi

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed."
    exit 1
fi

echo "Installing Python dependencies (redis)..."
pip install redis

echo "Setup complete. You can now run:"
echo "  docker-compose up -d"
echo "  bash run_test.sh"
