import os
import shutil

# Configuration Mapping
# Node 1: 5900
# Node 2: 5901
# Node 3: 5902
# Node 4: 5903
# Node 5: 5904
# Node 6: 5905

NODES = {
    5900: "192.168.122.250",
    5901: "192.168.122.58",
    5902: "192.168.122.170",
    5903: "192.168.122.11",
    5904: "192.168.122.9",
    5905: "192.168.122.210"
}

BASE_CONF = """port {port}
bind 0.0.0.0
protected-mode no
daemonize no
appendonly yes
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
cluster-announce-ip {ip}
cluster-announce-port {port}
cluster-announce-bus-port 1{port}
dir .
logfile "redis-{port}.log"
"""

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    for i, (port, ip) in enumerate(NODES.items()):
        # Mapping port to node index (1-6)
        node_index = i + 1
        dir_name = f"node-{node_index}"
        dir_path = os.path.join(base_dir, dir_name)
        
        # Create directory
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Created directory: {dir_name}")
        else:
            print(f"Directory exists: {dir_name}")

        # Write redis.conf
        conf_content = BASE_CONF.format(port=port, ip=ip)
        conf_path = os.path.join(dir_path, "redis.conf")
        
        with open(conf_path, "w") as f:
            f.write(conf_content)
        
        print(f"Written config for {dir_name} (IP: {ip})")

if __name__ == "__main__":
    main()
