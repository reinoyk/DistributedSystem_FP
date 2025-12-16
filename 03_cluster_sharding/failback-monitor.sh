#!/bin/bash

# Configuration for GNS3 Environment
# Define Masters as IP:PORT
MASTERS=(
  "192.168.122.250:5900" 
  "192.168.122.58:5901" 
  "192.168.122.170:5902"
)

echo "Starting Failback Monitor for nodes: ${MASTERS[*]}"

while true; do
  for NODE in "${MASTERS[@]}"; do
    IP=${NODE%%:*}
    PORT=${NODE##*:}
    
    # 1. Check if node is alive
    if redis-cli -h $IP -p $PORT ping > /dev/null 2>&1; then
      
      # 2. Check current role
      ROLE_INFO=$(redis-cli -h $IP -p $PORT role 2>/dev/null)
      ROLE=$(echo "$ROLE_INFO" | head -n 1)

      # 3. If Slave, attempt Failover
      if [ "$ROLE" == "slave" ]; then
        echo "[$(date)] Node $NODE is SLAVE. Attempting failover to restore MASTER status..."
        
        OUT=$(redis-cli -h $IP -p $PORT CLUSTER FAILOVER 2>&1)
        if [ $? -eq 0 ]; then
             echo "[$(date)] Failover command sent to $NODE. Result: $OUT"
        else
             echo "[$(date)] Failover failed for $NODE. Result: $OUT"
        fi
      fi
    else
       # Node unreachable
       :
    fi
  done
  
  # Check every 5 seconds
  sleep 5
done
