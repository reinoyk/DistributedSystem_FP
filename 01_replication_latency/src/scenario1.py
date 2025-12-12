import redis
import time

# --- Konfigurasi Eksperimen ---
MASTER_HOST = '127.0.0.1'
MASTER_PORT = 6379
REPLICA_PORT = 6380  # Kita akan uji baca dari Replica 1
NUM_WRITES = 1000
KEY_PREFIX = "test_key_"

def run_scenario_1():
    print("## 🧪 Skenario 1: Observasi Replication Lag & Eventual Consistency")
    print(f"Menggunakan Master: {MASTER_HOST}:{MASTER_PORT}, Replica: {MASTER_HOST}:{REPLICA_PORT}")
    print("-" * 50)

    try:
        # 1. Koneksi ke Master dan Replica
        master = redis.Redis(host=MASTER_HOST, port=MASTER_PORT, decode_responses=True)
        replica = redis.Redis(host=MASTER_HOST, port=REPLICA_PORT, decode_responses=True)
        
        # Cek koneksi
        master.ping()
        replica.ping()
        print("✅ Koneksi Master dan Replica berhasil.")

        # --- Langkah Eksperimen ---

        # 2. Kirim 1000 write (SET) ke master
        print(f"🔄 Langkah 2: Mengirim {NUM_WRITES} write (SET) ke Master...")
        start_write_time = time.time()
        
        pipeline = master.pipeline()
        for i in range(NUM_WRITES):
            key = f"{KEY_PREFIX}{i}"
            value = f"value_{i}_{start_write_time}"
            pipeline.set(key, value)
        pipeline.execute()
        
        end_write_time = time.time()
        print(f"   Selesai menulis dalam {end_write_time - start_write_time:.4f} detik.")

        # 3. Segera baca dari replica
        # Ini adalah momen penting: membaca TEPAT SETELAH penulisan selesai.
        print("🔍 Langkah 3: Segera membaca dari Replica...")
        
        unsynced_keys = 0
        
        # Hitung berapa banyak key yang tidak tersedia/belum terupdate di replica
        for i in range(NUM_WRITES):
            key = f"{KEY_PREFIX}{i}"
            # Kita hanya perlu mengecek keberadaan key, atau jika nilainya berbeda
            
            # Catatan: Pada Redis, SET akan tereplikasi dengan cepat. 
            # Kita bisa mengukur 'unsynced' sebagai key yang *belum ada*.
            if not replica.exists(key):
                unsynced_keys += 1
        
        # 4. Catat berapa banyak key yang belum tersinkron
        print("-" * 50)
        print("### Hasil Observasi Konsistensi Eventual ###")
        print(f"Total Key Ditulis: {NUM_WRITES}")
        print(f"Key yang Belum Tersinkron di Replica (Port {REPLICA_PORT}): **{unsynced_keys}**")
        
        if unsynced_keys > 0:
            print("❌ Terdapat Replication Lag. Replica belum memiliki semua data Master.")
        else:
            print("✅ Data tersinkron dengan cepat. Lanjut observasi lag.")

        # Observasi Replication Lag (waktu yang dibutuhkan untuk konsisten)
        
        if unsynced_keys == 0:
            print("\n⏳ Menunggu 50 ms untuk memastikan data tereplikasi sepenuhnya...")
            # Jika unsynced_keys 0, coba cek lagi setelah jeda kecil
            time.sleep(0.05) 
        
        # Verifikasi akhir (Loop hingga semua tersinkron)
        max_wait_time = 5 # detik
        synced_count = 0
        start_sync_wait = time.time()
        
        while synced_count < NUM_WRITES and (time.time() - start_sync_wait) < max_wait_time:
            synced_count = 0
            for i in range(NUM_WRITES):
                key = f"{KEY_PREFIX}{i}"
                if replica.exists(key):
                    synced_count += 1
            
            if synced_count < NUM_WRITES:
                # Print status setiap 100ms
                if int((time.time() - start_sync_wait) * 1000) % 100 == 0:
                    print(f"   > Status: {synced_count}/{NUM_WRITES} tersinkron...")
                time.sleep(0.001) # Jeda mikro
                
        sync_time = time.time() - start_sync_wait

        if synced_count == NUM_WRITES:
            print(f"**Replikasi selesai sepenuhnya dalam {sync_time:.4f} detik (Replication Lag).**")
            print(f"✅ STATUS: SUKSES. Semua {NUM_WRITES} data berhasil direplikasi ke Replica.")
        else:
            print(f"❌ STATUS: GAGAL. Waktu habis ({max_wait_time}s). Hanya {synced_count}/{NUM_WRITES} data yang tersinkron.")
        print("-" * 50)

    except redis.exceptions.ConnectionError as e:
        print(f"❌ GAGAL KONEKSI. Pastikan Redis Master ({MASTER_PORT}) dan Replica ({REPLICA_PORT}) berjalan!")
        print(f"Error: {e}")
    finally:
        # Opsional: Membersihkan kunci yang dibuat
        try:
            master.delete(*[f"{KEY_PREFIX}{i}" for i in range(NUM_WRITES)])
            print("\n🧹 Data eksperimen telah dibersihkan.")
        except:
            pass
            
if __name__ == "__main__":
    run_scenario_1()
