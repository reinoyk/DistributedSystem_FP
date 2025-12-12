import time
import sys
from redis.sentinel import Sentinel, MasterNotFoundError

def main():
    sentinels = [
        ('192.168.1.10', 26379),
        ('192.168.1.11', 26379),
        ('192.168.1.12', 26379)
    ]

    service_name = 'mymaster'
    
    print(f"Monitoring Sentinel setup for master: {service_name}...")
    
    last_master_ip = None
    
    sentinel_connection = Sentinel(sentinels, socket_timeout=0.1)

    while True:
        try:
            # Discover current master
            master_ip, master_port = sentinel_connection.discover_master(service_name)
            
            if last_master_ip is None:
                print(f"[{time.strftime('%H:%M:%S')}] Current Master is: {master_ip}")
                last_master_ip = master_ip
            elif master_ip != last_master_ip:
                print(f"[{time.strftime('%H:%M:%S')}] FAILOVER DETECTED! New Master: {master_ip}")
                last_master_ip = master_ip
                
            time.sleep(0.5)

        except MasterNotFoundError:
            print(f"[{time.strftime('%H:%M:%S')}] Master not found! (Voting in progress?)")
            time.sleep(0.5)
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Connection Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
        sys.exit(0)
