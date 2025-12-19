import redis
import time
import sys

# --- KONFIGURASI DOCKER ---
# Di Docker, hostname adalah nama service di docker-compose.yml
MASTER_HOST = 'master'      
MASTER_PORT = 6379          # Port internal container selalu 6379

REPLICA_HOST = 'replica-1'
REPLICA_PORT = 6379         # Port internal container selalu 6379

NUM_WRITES = 1000

def run_scenario_1():
    print(f"## 🐳 Docker Scenario 1: Replication Lag Test")
    print(f"   Master  : {MASTER_HOST}:{MASTER_PORT}")
    print(f"   Replica : {REPLICA_HOST}:{REPLICA_PORT}")
    print("-" * 50)

    try:
        # 1. Koneksi
        master = redis.Redis(host=MASTER_HOST, port=MASTER_PORT)
        replica = redis.Redis(host=REPLICA_HOST, port=REPLICA_PORT)
        
        print("⏳ Mengecek koneksi...")
        master.ping()
        replica.ping()
        print("✅ Koneksi ke Container Master & Replica berhasil.")

        master.flushall()

        # 2. Write Phase
        print(f"🔄 Mengirim {NUM_WRITES} data ke Master...")
        pipeline = master.pipeline()
        for i in range(NUM_WRITES):
            pipeline.set(f"key_{i}", f"value_{i}")
        
        start_w = time.time()
        pipeline.execute()
        end_w = time.time()
        print(f"   Write selesai dalam {end_w - start_w:.4f} detik.")

        # 3. Read/Measure Phase
        start_measure = time.time()
        
        initial_count = replica.dbsize()
        unsynced = NUM_WRITES - initial_count
        
        print(f"📊 Key Belum Sinkron: {unsynced}")
        
        while True:
            if replica.dbsize() >= NUM_WRITES:
                break
        
        real_lag = time.time() - start_measure
        print("-" * 50)
        print(f"⏱️  REPLICATION LAG: {real_lag:.6f} detik")
        print("-" * 50)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_scenario_1()
