# Panduan Implementasi di GNS3

Dokumen ini menjelaskan cara mensimulasikan Redis Cluster Sharding menggunakan GNS3 dengan topologi 6 node terdistribusi.

## 1. Topologi Jaringan

Buatlah topologi di GNS3 dengan spesifikasi berikut:
- **Jumlah Node**: 6 Client (bisa menggunakan Ubuntu Docker, Alpine, atau VM Linux ringan).
- **Switch**: 1 Ethernet Switch untuk menghubungkan semua node.
- **Subnet/Network**: `192.168.122.0/24`.

### Konfigurasi IP Konfigurasi

Pastikan setiap node dikonfigurasi dengan IP statis berikut agar sesuai dengan konfigurasi Redis yang sudah disiapkan:

| Node Name | IP Address       | Redis Port | Role Configured |
|-----------|------------------|------------|-----------------|
| Node 1    | 192.168.122.250  | 5900       | Master 1        |
| Node 2    | 192.168.122.58   | 5901       | Master 2        |
| Node 3    | 192.168.122.170  | 5902       | Master 3        |
| Node 4    | 192.168.122.11   | 5903       | Replica 1       |
| Node 5    | 192.168.122.9    | 5904       | Replica 2       |
| Node 6    | 192.168.122.210  | 5905       | Replica 3       |

## 2. Persiapan File

Copy folder proyek ini ke direktori kerja di GNS3 (atau clone repository ini di setiap node).

Struktur folder yang penting untuk setiap node adalah direktori konfigurasinya masing-masing.
> **Note**: Di repository ini folder bernama `node-5900`, `node-5901`, dst. Untuk kemudahan di GNS3, Anda bisa merename-nya menjadi `node-1`, `node-2`, dst sesuai tabel di atas.

## 3. Menjalankan Redis (Per-Node)

Lakukan langkah ini di **masing-masing terminal node** di GNS3:

**Di Node 1 (192.168.122.250):**
```bash
cd node-1 (atau node-5900)
redis-server redis.conf
```

**Di Node 2 (192.168.122.58):**
```bash
cd node-2 (atau node-5901)
redis-server redis.conf
```

... Lakukan hal yang sama untuk Node 3 s/d 6 (folder `node-3` s/d `node-6`).

> **Catatan:** Jangan gunakan `start-all.sh` di GNS3 karena script tersebut didesain untuk menjalankan semua process di satu mesin lokal (localhost). Di GNS3, Anda harus menyalakan manual agar terdistribusi di masing-masing VM.

## 4. Membuat Cluster

Setelah semua 6 node Redis berjalan ("Ready to accept connections"), gunakan salah satu node (misal Node 1) untuk menginisiasi cluster.

Jalankan perintah ini dari folder root project (luar folder node):

```bash
bash create-cluster.sh
```

Script ini akan menghubungi ke-6 IP tersebut dan membentuk cluster. Ketik `yes` saat diminta konfirmasi.

## 5. Verifikasi

Jalankan script verifikasi Python dari salah satu node (pastikan `python3` dan `redis-py` terinstall):

```bash
python3 cluster_verification.py
```

Jika sukses, Anda akan melihat laporan distribusi key yang tersebar di berbagai IP address.

## 6. Failover & Failback Monitor

Untuk menjalankan sistem **Failback Monitor** otomatis:
1. Pilih satu node sebagai "Monitor Node" (bisa Node 1 atau node tambahan).
2. Jalankan script monitor:
   ```bash
   bash failback-monitor.sh
   ```
   Script ini akan terus berjalan dan memantau status cluster. Jika Node Master (misal Node 1) mati dan hidup kembali, script ini akan otomatis mengembalikan perannya menjadi Master.
