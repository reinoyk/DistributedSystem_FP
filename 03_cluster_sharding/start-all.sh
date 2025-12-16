#!/bin/bash
# Note: In GNS3, you must start redis-server on each VM manually.
# This script is for LOCAL simulation only.

for i in {1..6}; do
  if [ -d "node-$i" ]; then
      # Need to determine port. Mapping: 1->5900, 2->5901, ...
      # Actually, since we are just starting redis-server in the dir, the port is in redis.conf
      # But we printed "Started node-$port" before. Let's stick to simple "Started node-$i".
      (cd node-$i && redis-server redis.conf) &
      echo "Started node-$i"
  else
      echo "Directory node-$i not found. Run update_configs.py first."
  fi
done
