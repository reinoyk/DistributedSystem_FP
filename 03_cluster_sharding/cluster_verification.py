import redis
from redis.cluster import RedisCluster

def main():
    # Cluster Configuration
    startup_nodes = [
        {"host": "127.0.0.1", "port": "7000"},
        {"host": "127.0.0.1", "port": "7001"},
        {"host": "127.0.0.1", "port": "7002"}
    ]

    print("Connecting to Redis Cluster...")
    # By default, redis-py handles cluster discovery if we point to one node, 
    # but providing multiple helps with robustness.
    # Note: 'redis-py' 4.x+ supports cluster via RedisCluster class (formerly redis-py-cluster)
    try:
        rc = RedisCluster(host='127.0.0.1', port=7000, decode_responses=True)
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
        node_name = f"{node_conn.host}:{node_conn.port}"
        
        if node_name not in node_distribution:
            node_distribution[node_name] = 0
        node_distribution[node_name] += 1

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
