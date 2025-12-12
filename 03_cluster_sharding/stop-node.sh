#!/bin/bash

PORT=$1

if [ -z "$PORT" ]; then
  echo "Usage: ./stop-node.sh <port>"
  exit 1
fi

PID=$(ps aux | grep "redis-server .*:${PORT}" | grep -v grep | awk '{print $2}')

if [ -z "$PID" ]; then
  echo "No redis-server found running on port $PORT"
  exit 1
fi

echo "Stopping redis-server on port $PORT with PID $PID"
kill $PID

sleep 1

if ps -p $PID > /dev/null; then
  echo "Force killing PID $PID"
  kill -9 $PID
else
  echo "Node on port $PORT stopped successfully."
fi
