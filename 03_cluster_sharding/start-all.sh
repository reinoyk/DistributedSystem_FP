#!/bin/bash
for port in 7000 7001 7002 7003 7004 7005; do
  (cd node-$port && redis-server redis.conf) &
done

echo "Nodes started."

# Start background monitor for auto-failback
if ! pgrep -f "failback-monitor.sh" > /dev/null; then
  echo "Starting Failback Monitor..."
  nohup bash failback-monitor.sh > failback-monitor.log 2>&1 &
else
  echo "Failback Monitor is already running."
fi

