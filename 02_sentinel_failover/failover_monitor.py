import redis
import time
from datetime import datetime
import sys

# Konfigurasi IP Sentinel (Docker Environment - Localhost Mapped)
# Jika kembali ke GNS3, ubah IP ini kembali ke IP VM Anda (192.168.122.x)
sentinels = [
    ('localhost', 26379),
    ('localhost', 26380),
    ('localhost', 26381)
]

service_name = 'mymaster'

def get_timestr():
    return datetime.now().strftime("%H:%M:%S")

print(f"[{get_timestr()}] Menghubungkan ke Sentinel...")

try:
    # Inisialisasi koneksi ke Sentinel
    sentinel = redis.Sentinel(sentinels, socket_timeout=0.1)
    
    # Cek Master Awal
    try:
        master = sentinel.discover_master(service_name)
        print(f"[INFO] Master Awal: {master[0]} (Port {master[1]})")
        
        last_master = master[0]
        last_seen_time = time.time() # Catat waktu terakhir lihat master hidup
        
        print("\n=== MONITORING AKTIF: Silakan Matikan Master di Docker ===")
        print("(Gunakan: docker stop redis-node1)")

        while True:
            try:
                # Cek siapa master sekarang
                cur_master = sentinel.discover_master(service_name)
                cur_master_ip = cur_master[0]
                
                if cur_master_ip != last_master:
                    # === MOMEN FAILOVER TERJADI ===
                    failover_time = time.time()
                    downtime_duration = failover_time - last_seen_time
                    
                    print(f"\n[FAILOVER TERDETEKSI]")
                    print(f"==========================================")
                    print(f"1. Waktu Master Lama Hilang : {datetime.fromtimestamp(last_seen_time).strftime('%H:%M:%S')}")
                    print(f"2. Waktu Master Baru Muncul : {get_timestr()}")
                    print(f"3. IP Master Baru           : {cur_master_ip}")
                    print(f"4. ESTIMASI DOWNTIME        : {downtime_duration:.2f} Detik")
                    print(f"==========================================")
                    
                    # Update state
                    last_master = cur_master_ip
                    last_seen_time = failover_time # Reset timer
                else:
                    # Jika master masih sama, update "last seen"
                    last_seen_time = time.time()
                    # print(".", end="", flush=True) # Optional: reduce clutter
                    sys.stdout.write(".")
                    sys.stdout.flush()
                    
                time.sleep(1) # Cek setiap 1 detik
                
            except (redis.exceptions.ConnectionError, redis.sentinel.MasterNotFoundError):
                # Jika koneksi putus (karena master mati), jangan update last_seen_time
                # Ini penting supaya durasi downtime terhitung akurat
                sys.stdout.write("x")
                sys.stdout.flush()
                time.sleep(1)
    except redis.sentinel.MasterNotFoundError:
        print("[ERROR] Master tidak ditemukan saat inisialisasi. Pastikan cluster berjalan.")
            
except KeyboardInterrupt:
    print("\nStop.")
except Exception as e:
    print(f"\n[ERROR] Terjadi kesalahan: {e}")
