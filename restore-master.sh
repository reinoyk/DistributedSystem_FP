#!/bin/bash

# Port node yang ingin dikembalikan menjadi Master
NODE_PORT=7000

# Cek apakah node 7000 hidup
if ! redis-cli -p $NODE_PORT ping > /dev/null 2>&1; then
    echo "Error: Node $NODE_PORT tidak aktif. Silakan jalankan node terlebih dahulu."
    exit 1
fi

# Cek role saat ini
ROLE=$(redis-cli -p $NODE_PORT role | head -n 1)

if [ "$ROLE" == "master" ]; then
    echo "Node $NODE_PORT sudah menjadi Master."
    exit 0
fi

echo "Node $NODE_PORT saat ini adalah Slave. Melakukan Failover agar menjadi Master..."

# Lakukan Manual Failover
redis-cli -p $NODE_PORT CLUSTER FAILOVER

# Tunggu sebentar dan verifikasi
sleep 2
NEW_ROLE=$(redis-cli -p $NODE_PORT role | head -n 1)

if [ "$NEW_ROLE" == "master" ]; then
    echo "Berhasil! Node $NODE_PORT sekarang kembali menjadi Master."
else
    echo "Gagal mengembalikan Node $NODE_PORT menjadi Master."
fi
