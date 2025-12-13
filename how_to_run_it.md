# Panduan Menjalankan Proyek Cluster Sharding

Dokumen ini menjelaskan langkah-langkah untuk menjalankan simulasi Redis Cluster Sharding yang ada di direktori `03_cluster_sharding`.

## Prasyarat

Pastikan Anda telah menginstal `redis-server`, `redis-cli` dan `python3`.
Jika belum, Anda dapat menginstalnya di Ubuntu/WSL/Debian dengan perintah:
```bash
sudo apt update
sudo apt install redis-server redis-tools python3-pip
pip install redis
```

## Langkah-langkah Menjalankan

### 1. Memulai Node Redis
Jalankan skrip `start-all.sh` untuk menyalakan 6 instance Redis (port 7000-7005).

```bash
cd /home/delix/DistributedSystem_FP/03_cluster_sharding
bash start-all.sh
```

### 2. Membuat Cluster
Setelah node menyala, jalankan skrip `create-cluster.sh` untuk membentuk cluster Redis dari node-node tersebut.

```bash
bash create-cluster.sh
```
Akan muncul dialog konfirmasi dari redis-cli, ketik `yes` jika diminta.

### 3. Verifikasi Cluster
Untuk memastikan cluster berjalan dan sharding berfungsi (distribusi key merata), jalankan script Python verifikasi.

```bash
python3 cluster_verification.py
```
Output yang diharapkan akan menampilkan distribusi key di berbagai node:
```
SHARDING DISTRIBUTION SUMMARY
========================================
Node 127.0.0.1:7000 holds XX keys
Node 127.0.0.1:7001 holds XX keys
...
========================================
If multiple IPs are listed above, sharding is WORKING.
```

## Menghentikan dan Mereset
Jika ingin menghentikan semua process dan menghapus data cluster (reset bersih), jalankan:

```bash
bash reset.sh
```
Ini akan mematikan proses redis di port 7000-7005 dan menghapus file data (`dump.rdb`, `nodes.conf`, dll).

## Struktur File
- **start-all.sh**: Menjalankan 6 server Redis di background dan mengaktifkan monitor failback.
- **create-cluster.sh**: Perintah `redis-cli` untuk menggabungkan node menjadi cluster.
- **cluster_verification.py**: Script Python untuk insert data dan cek sharding.
- **reset.sh**: Script pembersihan (kill process & delete data).
- **stop-node.sh**: Helper untuk stop 1 node spesifik (jarang dipakai manual).
- **failback-monitor.sh**: Program background yang otomatis mengembalikan status Master ke node 7000-7002 jika restart.

## Cara Menguji Failover (Master Mati diganti Slave)

Untuk membuktikan bahwa Replica menggantikan Master yang mati:

1. **Cek Status Awal**
   Cek node mana yang menjadi Master dan mana Slave-nya.
   ```bash
   redis-cli -p 7000 cluster nodes
   ```
   Misal: 7000 adalah Master, dan 7003/7004/7005 mungkin adalah Slave-nya (lihat ID yang ada di kolom `myself` atau `slave`).

2. **Matikan Salah Satu Master**
   Misalnya node 7000 adalah Master. Matikan node tersebut:
   ```bash
   bash stop-node.sh 7000
   ```

3. **Cek Status Lagi**
   Cek status cluster dari node lain yang masih hidup (misal 7001).
   ```bash
   redis-cli -p 7001 cluster nodes
   ```
   Perhatikan node 7000 akan berstatus `fail`, dan Slave-nya (yang tadinya replica) akan berubah status menjadi `master`.

4. **Hidupkan Kembali Node Lama**
   Nyalakan kembali node 7000.
   ```bash
   cd node-7000 && redis-server redis.conf &
   ```
   Saat dicek lagi (`redis-cli -p 7001 cluster nodes`), node 7000 akan bergabung kembali, tetapi sekarang dia akan menjadi **slave** dari master yang baru.

5. **Mengembalikan Master Asli (Failback)**
   
   Sistem kini dilengkapi dengan **Failback Monitor Otomatis**.
   Script `failback-monitor.sh` (yang dijalankan otomatis oleh `start-all.sh`) akan berjalan di background dan memantau Node 7000, 7001, dan 7002.
   
   Jika salah satu node Master tersebut mati dan kemudian dinyalakan kembali (menjadi Slave), monitor akan otomatis mendeteksinya dan melakukan failover dalam waktu ±5 detik.
   
5. **Mengembalikan Master Asli (Failback)**
   
   Sistem kini dilengkapi dengan **Failback Monitor Otomatis**.
   Script `failback-monitor.sh` (yang dijalankan otomatis oleh `start-all.sh`) akan berjalan di background dan memantau Node 7000, 7001, dan 7002 ("Preferred Masters").
   
   Jika salah satu node Master tersebut mati dan kemudian dinyalakan kembali (menjadi Slave), monitor akan otomatis mendeteksinya dan melakukan failover dalam waktu ±5 detik.
   
   **Anda tidak perlu menjalankan perintah manual apapun.**
   
   Jika monitor belum berjalan (misal karena Anda merestart komputer tanpa `start-all.sh`), jalankan saja:
   ```bash
   nohup bash failback-monitor.sh > failback-monitor.log 2>&1 &
   ```
