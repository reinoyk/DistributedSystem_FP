#!/bin/bash

# Port yang seharusnya menjadi Master
PREFERRED_MASTERS=(7000 7001 7002)

echo "Starting Failback Monitor for nodes: ${PREFERRED_MASTERS[*]}"

while true; do
  for PORT in "${PREFERRED_MASTERS[@]}"; do
    # 1. Cek apakah node hidup
    if redis-cli -p $PORT ping > /dev/null 2>&1; then
      
      # 2. Cek role saat ini
      ROLE_INFO=$(redis-cli -p $PORT role 2>/dev/null)
      ROLE=$(echo "$ROLE_INFO" | head -n 1)

      # 3. Jika Slave, lakukan Failover
      if [ "$ROLE" == "slave" ]; then
        echo "[$(date)] Node $PORT is SLAVE. Attempting failover to restore MASTER status..."
        
        # Cek status sync dulu, jika master_link_status down, failover mungkin gagal atau unsafe
        # Tapi CLUSTER FAILOVER memhandle safety check.
        
        OUT=$(redis-cli -p $PORT CLUSTER FAILOVER 2>&1)
        if [ $? -eq 0 ]; then
             echo "[$(date)] Failover command sent to $PORT. Result: $OUT"
        else
             echo "[$(date)] Failover failed for $PORT. Result: $OUT"
        fi
      fi
    # else
       # Node mati, skip
    fi
  done
  
  # Cek setiap 5 detik
  sleep 5
done
