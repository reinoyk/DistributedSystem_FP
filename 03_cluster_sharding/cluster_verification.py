import redis
from redis.cluster import RedisCluster, ClusterNode

def main():
    # Cluster Configuration for GNS3
    startup_nodes = [
        ClusterNode("192.168.122.250", 5900), # Node 1
        ClusterNode("192.168.122.58", 5901),  # Node 2
        ClusterNode("192.168.122.170", 5902), # Node 3
        ClusterNode("192.168.122.11", 5903),  # Node 4
        ClusterNode("192.168.122.9", 5904),   # Node 5
        ClusterNode("192.168.122.210", 5905)  # Node 6
    ]

    print("Connecting to Redis Cluster...")
    try:
        # Note: We can connect to any node. 
        # Ensure your client machine (Node Client) can reach these IPs.
        rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
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
        try:
            rc.set(key, value)
            
            # Identify which node holds the key
            node_conn = rc.get_node_from_key(key)
            node_name = f"{node_conn.host}:{node_conn.port}"
            
            if node_name not in node_distribution:
                node_distribution[node_name] = 0
            node_distribution[node_name] += 1
        except Exception as e:
            print(f"Error checking key {key}: {e}")

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
