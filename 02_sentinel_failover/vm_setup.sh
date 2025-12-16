#!/bin/bash

# Initial setup installation script

echo "Updating package lists..."
apt-get update

echo "Installing Redis Tools..."
apt-get install -y redis-tools

echo "Installing Redis Server..."
apt-get install -y redis-server

echo "Installing Redis Sentinel..."
# separate package usually named redis-sentinel, or included in redis-server
# trying redis-sentinel as requested (if it exists separate, or it will be picked up)
apt-get install -y redis-sentinel

echo "Installation complete."
