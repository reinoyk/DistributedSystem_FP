# 📘 Blueprint Skenario 2: Redis Sentinel di GNS3

**Status**: Transisi dari AWS/Localhost ke GNS3.
**Tujuan**: Membangun Cluster High Availability dengan 3 Node terpisah dengan IP Custom.

## 1. Topologi GNS3 (Konfigurasi Anda)

| Node Name | Peran | IP Address | Redis Port | Sentinel Port | Keterangan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Node 1** | Master + Sentinel A | `192.168.122.235` | `5900` | `26379` | Initial Master |
| **Node 2** | Replica + Sentinel B | `192.168.122.92` | `5901` | `26379` | Calon Master |
| **Node 3** | Replica + Sentinel C | `192.168.122.160` | `5902` | `26379` | Calon Master |
| **Client-PC** | Tester / Benchmarker | `192.168.122.129` | `5914` | - | Tempat run script |

> **⚠️ Penting**: Pastikan semua node bisa saling PING sebelum lanjut.

---

## 2. Langkah Konfigurasi (Di Terminal Node GNS3)

Lakukan ini satu per satu di dalam console VNC/Terminal GNS3 Anda.

### Tahap A: Setup Replikasi Dasar (Pondasi Sentinel)
Sentinel tidak bisa jalan tanpa replikasi master-replica yang sehat.

**1. Di Node Master (192.168.122.235)**
- Edit config redis (biasanya `/etc/redis/redis.conf`).
- Pastikan: `port 5900`
- Pastikan: `bind 0.0.0.0`
- Pastikan: `protected-mode no`
- Restart: `sudo service redis-server restart`

**2. Di Node Replica 1 (192.168.122.92)**
- Edit config.
- Pastikan: `port 5901`
- Pastikan: `bind 0.0.0.0`
- Tambahkan baris di paling bawah:
  ```conf
  replicaof 192.168.122.235 5900
  ```
- Restart Redis.

**3. Di Node Replica 2 (192.168.122.160)**
- Edit config.
- Pastikan: `port 5902`
- Pastikan: `bind 0.0.0.0`
- Tambahkan baris di paling bawah:
  ```conf
  replicaof 192.168.122.235 5900
  ```
- Restart Redis.

**Verifikasi (Wajib):**
Di Master (Node 1), ketik:
```bash
redis-cli -p 5900 info replication
```
Pastikan tertulis: **`connected_slaves:2`**.

---

### Tahap B: Setup Sentinel

Sekarang kita pasang "CCTV" (Sentinel) di ketiga node.

**1. Buat/Edit File Sentinel (Di SEMUA 3 Node)**
File: `/etc/redis/sentinel.conf` (atau lokasi konfigurasi sentinel Anda).

Isi dengan konfigurasi berikut (Sama untuk semua node, karena monitor target yang sama):

```conf
port 26379
daemonize yes
dir "/tmp"

# Monitor Master (IP Master Awal: Node 1)
sentinel monitor mymaster 192.168.122.235 5900 2

sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000
sentinel parallel-syncs mymaster 1
```

**2. Jalankan Sentinel (Di SEMUA 3 Node)**
```bash
redis-sentinel /etc/redis/sentinel.conf
```

**3. Cek Status Sentinel**
Di salah satu node:
```bash
redis-cli -p 26379 info sentinel
```
Harus muncul: **`status=ok, slaves=2, sentinels=3`**.

---

## 3. Script Pengujian (Di Client-PC)

Script [failover_monitor.py](file:///d:/Kuliah/Distributed%20System/DistributedSystem_FP/02_sentinel_failover/failover_monitor.py) di folder `02_sentinel_failover` sudah saya update dengan IP Anda.

### Cara Menjalankan:
1. Pindahkan [failover_monitor.py](file:///d:/Kuliah/Distributed%20System/DistributedSystem_FP/02_sentinel_failover/failover_monitor.py) ke Client-PC (`192.168.122.129`).
2. Jalankan script:
   ```bash
   python failover_monitor.py
   ```
3. Biarkan script berjalan (akan mencetak titik `.` per detik).

---

## 4. Cara Eksperimen (Failover Demo)

1. Pastikan script python sedang berjalan dan mencetak `.`
2. Buka GNS3, **Matikan/Suspend** Node 1 (Master).
3. Tunggu 5-10 detik.
4. Lihat terminal Client-PC.
5. Anda akan melihat pesan **🚨 FAILOVER DETECTED**.
6. Ambil Screenshot! Itu bukti Sentinel bekerja.
