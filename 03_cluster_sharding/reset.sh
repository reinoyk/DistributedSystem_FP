#!/bin/bash
# Note: This generally runs locally to clean up. 
# For GNS3, you might need to run this on each node or manually delete files.

for port in 5900 5901 5902 5903 5904 5905; do
  kill -9 $(lsof -t -i:$port) 2>/dev/null
done

for i in {1..6}; do
  DIR="node-$i"
  if [ -d "$DIR" ]; then
      rm -rf $DIR/nodes.conf $DIR/appendonly.aof $DIR/appendonlydir $DIR/dump.rdb $DIR/*.log
      echo "Cleaned $DIR"
  fi
done
  fi
done
echo "Cluster reset (local artifacts cleaned)."
