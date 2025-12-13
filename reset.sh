#!/bin/bash
for port in 7000 7001 7002 7003 7004 7005; do
  kill -9 $(lsof -t -i:$port) 2>/dev/null
  rm -rf node-$port/nodes.conf node-$port/appendonly.aof node-$port/appendonlydir node-$port/dump.rdb node-$port/redis-$port.log
done
echo "Cluster reset!"
