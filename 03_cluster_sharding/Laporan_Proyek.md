# Laporan Proyek: Implementasi Redis Cluster Sharding

## 1. Penjelasan Teori

**Redis Cluster** adalah implementasi terdistribusi dari Redis yang menyediakan kemampuan _sharding_ (partisi data) secara otomatis ke berbagai node. Sistem ini memungkinkan penyimpanan data yang lebih besar daripada kapasitas RAM satu server (horizontal scaling).

Konsep kunci dalam proyek ini meliputi:

- **Sharding**: Pemecahan data menjadi bagian-bagian kecil (shards). Redis menggunakan konsep _Hash Slots_ (total 16.384 slot) untuk memetakan key ke node tertentu.
- **Replication**: Setiap node master memiliki satu atau lebih replica. Jika master mati, replica akan mengambil alih (Failover) untuk menjamin _High Availability_.
- **Gossip Protocol**: Node saling berkomunikasi menggunakan port bus (port dasar + 10000) untuk memantau kesehatan node lain.

## 2. Topologi Cluster

Sistem ini menggunakan 6 container Redis yang berjalan di atas Docker, membentuk satu cluster utuh.

- **Arsitektur**: Master-Slave Replication
- **Jumlah Node**: 6 (3 Master, 3 Replica)
- **Mapping Port**:
  - Master 1: Port 7000 (Slot 0-5460)
  - Master 2: Port 7001 (Slot 5461-10922)
  - Master 3: Port 7002 (Slot 10923-16383)
  - Replica 1: Port 7003 (Replikasi Master 1)
  - Replica 2: Port 7004 (Replikasi Master 2)
  - Replica 3: Port 7005 (Replikasi Master 3)

## 3. Skenario Eksperimen

Berikut adalah tabel skenario eksperimen yang dilakukan untuk menguji kemampuan cluster:

| Tujuan Eksperimen                              | Langkah-Langkah                                                                                                                                                             | Hasil yang Diharapkan                                                                                                 | Analisis Singkat                                                                                                                                                                        |
| :--------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Verifikasi Sharding (Distribusi Data)**   | 1. Jalankan `python cluster_verification.py`.<br>2. Script akan menulis 100 key acak.<br>3. Amati output terminal.                                                          | Key tersebar ke Node 7000, 7001, dan 7002. Tidak menumpuk di satu node.                                               | Algoritma _CRC16(key) mod 16384_ berhasil membagi beban penyimpanan secara merata ke seluruh master node.                                                                               |
| **2. High Availability (Failover Simulation)** | 1. Matikan Node Master (misal port 7000) dengan `./stop-node.sh 7000`.<br>2. Cek status cluster dengan `redis-cli cluster nodes`.<br>3. Jalankan kembali script verifikasi. | Status node 7000 menjadi `fail`. Node replica (7003) otomatis promosi jadi Master. Script tetap bisa tulis/baca data. | Cluster mendeteksi kegagalan melalui _heartbeat_. Konsensus quorum tercapai untuk mempromosikan slave, sehingga sistem tetap _available_ meski ada node mati (AP/CP depend on context). |
| **3. Recovery Node**                           | 1. Hidupkan kembali node yang mati (7000).<br>2. Cek log replikasi.                                                                                                         | Node 7000 bergabung kembali ke cluster, namun kali ini sebagai _Replica_ dari node 7003.                              | Sistem bersifat _self-healing_. Node yang kembali online akan melakukan sinkronisasi data dari master saat ini.                                                                         |

## 4. Hasil Log & Screenshot

> **Instruksi:** Silakan tempel screenshot bukti eksekusi di bagian ini.

### A. Screenshot Docker Containers

_(Tempel screenshot output perintah `docker compose ps` di sini)_

### B. Screenshot Inisialisasi Cluster

_(Tempel screenshot output saat menjalankan `./init-docker-cluster.sh` di sini)_

### C. Screenshot Verifikasi Sharding (Output Python)

_(Tempel screenshot output script `cluster_verification.py` yang menunjukkan "Node x holds y keys" di sini)_

### D. Screenshot Simulasi Failover

_(Tempel screenshot saat node dimatikan dan output `cluster nodes` yang menunjukkan status FAIL/SLAVE di sini)_

## 5. Analisis Berdasarkan Konsep Distributed Systems

### A. Scalability (Skalabilitas)

Sistem menunjukkan **Horizontal Scalability**. Dengan sharding, kapasitas tulis (_write throughput_) dan penyimpanan meningkat seiring penambahan node master. Jika container ditambah, Redis Cluster mendukung _resharding_ tanpa downtime.

### B. Availability & Fault Tolerance

Sistem mengadopsi prinsip **Eventual Consistency** dan **High Availability**.

- **Fault Tolerance**: Terbukti pada Skenario 2, di mana hilangnya satu komponen (Node 7000) tidak melumpuhkan sistem total.
- **Vulnerability**: Jika Master dan Replicanya mati bersamaan, sebagian hash slot akan hilang (Cluster Down).

### C. Transparency

- **Location Transparency**: Klien (script Python) tidak perlu tahu di node mana data `user:1` disimpan. Library `redis-py` secara otomatis mengatur _redirection_ (MOVED error) ke node yang tepat.

## 6. Kontribusi Masing-Masing Anggota

| Nama Anggota   | NRP   | Kontribusi dalam Proyek                             |
| :------------- | :---- | :-------------------------------------------------- |
| [Nama Anda]    | [NRP] | Setup Docker, Scripting Python, Konfigurasi Cluster |
| [Nama Teman 1] | [NRP] | Perancangan Skenario Uji Coba, Analisis Teori       |
| [Nama Teman 2] | [NRP] | Pengujian Failover, Penyusunan Laporan              |

_(Sesuaikan isi tabel ini dengan pembagian tugas tim yang sebenarnya)_
