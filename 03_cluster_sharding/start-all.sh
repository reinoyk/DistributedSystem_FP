#!/bin/bash
for port in 7000 7001 7002 7003 7004 7005; do
  (cd node-$port && redis-server redis.conf) &
done

echo "All Redis nodes started!"
