import redis
from redis.cluster import RedisCluster

def main():
    # Cluster Configuration
    startup_nodes = [
        {"host": "192.168.1.31", "port": "6379"},
        {"host": "192.168.1.32", "port": "6379"},
        {"host": "192.168.1.33", "port": "6379"}
    ]

    print("Connecting to Redis Cluster...")
    # By default, redis-py handles cluster discovery if we point to one node, 
    # but providing multiple helps with robustness.
    # Note: 'redis-py' 4.x+ supports cluster via RedisCluster class (formerly redis-py-cluster)
    try:
        rc = RedisCluster(host='192.168.1.31', port=6379, decode_responses=True)
        # Alternatively check connection
        rc.ping()
        print("Connected successfully.")
    except Exception as e:
        print(f"Error connecting to cluster: {e}")
        return

    num_keys = 100
    print(f"Inserting {num_keys} random keys...")

    # Insert keys and track their distribution
    node_distribution = {}

    for i in range(1, num_keys + 1):
        key = f"user:{i}"
        value = f"data_{i}"
        
        # Write
        rc.set(key, value)
        
        # Identify which node holds the key
        # In redis-py, we can get the connection for a specific key
        node_conn = rc.get_node_from_key(key)
        node_ip = node_conn.host
        
        if node_ip not in node_distribution:
            node_distribution[node_ip] = 0
        node_distribution[node_ip] += 1

    print("\n" + "=" * 40)
    print("SHARDING DISTRIBUTION SUMMARY")
    print("=" * 40)
    
    sorted_nodes = sorted(node_distribution.items())
    for node, count in sorted_nodes:
        print(f"Node {node} holds {count} keys")

    print("=" * 40)
    print("If multiple IPs are listed above, sharding is WORKING.")

if __name__ == "__main__":
    main()
