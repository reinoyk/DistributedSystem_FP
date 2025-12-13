import time
import sys
from redis.sentinel import Sentinel, MasterNotFoundError

def main():
    # Configuration for Docker environment (Localhost Mapped Ports)
    # Mapping based on docker-compose.yml:
    # Sentinel 1: localhost:26379
    # Sentinel 2: localhost:26380
    # Sentinel 3: localhost:26381
    sentinels = [
        ('localhost', 26379),
        ('localhost', 26380),
        ('localhost', 26381)
    ]

    service_name = 'mymaster'
    
    print(f"Monitoring Sentinel setup for master: {service_name}...")
    print("Note: The IPs returned below will be internal Docker IPs/Hostnames.")
    
    last_master_ip = None
    
    # Initialize connection to Sentinel
    try:
        sentinel_connection = Sentinel(sentinels, socket_timeout=0.1)
    except Exception as e:
        print(f"Error initializing Sentinel connection: {e}")
        print("Ensure docker-compose is running!")
        return

    while True:
        try:
            # Discover current master
            master_ip, master_port = sentinel_connection.discover_master(service_name)
            
            if last_master_ip is None:
                print(f"[{time.strftime('%H:%M:%S')}] Current Master is: {master_ip}:{master_port}")
                last_master_ip = master_ip
            elif master_ip != last_master_ip:
                print(f"[{time.strftime('%H:%M:%S')}] 🚨 FAILOVER DETECTED! New Master: {master_ip}:{master_port}")
                last_master_ip = master_ip
                
            time.sleep(0.5)

        except MasterNotFoundError:
            print(f"[{time.strftime('%H:%M:%S')}] Master not found! (Voting in progress?)")
            time.sleep(0.5)
        except Exception as e:
            # print(f"[{time.strftime('%H:%M:%S')}] Connection Error: {e}")
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
        sys.exit(0)
