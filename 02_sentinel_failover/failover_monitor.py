import time
import sys
from redis.sentinel import Sentinel, MasterNotFoundError

def main():
    # Konfigurasi Sentinel (IP GNS3)
    sentinels = [
        ('192.168.122.235', 26379),
        ('192.168.122.92', 26379),
        ('192.168.122.160', 26379)
    ]

    service_name = 'mymaster'
    
    print(f"Monitoring Sentinel setup for master: {service_name}...")
    
    last_master_ip = None
    
    # Inisialisasi koneksi ke Sentinel
    try:
        sentinel_connection = Sentinel(sentinels, socket_timeout=0.1)
    except Exception as e:
        print(f"Error initializing Sentinel connection: {e}")
        return

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
