#!/bin/bash

# Port node yang ingin dikembalikan menjadi Master
# Default ke 5900 jika tidak diberikan argumen
NODE_PORT=${1:-5900}
NODE_IP=${2:-"127.0.0.1"}

echo "Checking Node $NODE_IP:$NODE_PORT..."

# Cek apakah node hidup
if ! redis-cli -h $NODE_IP -p $NODE_PORT ping > /dev/null 2>&1; then
    echo "Error: Node $NODE_IP:$NODE_PORT tidak aktif atau tidak dapat dijangkau."
    exit 1
fi

# Cek role saat ini
ROLE=$(redis-cli -h $NODE_IP -p $NODE_PORT role | head -n 1)

if [ "$ROLE" == "master" ]; then
    echo "Node $NODE_PORT sudah menjadi Master."
    exit 0
fi

echo "Node $NODE_PORT saat ini adalah Slave. Melakukan Failover agar menjadi Master..."

# Lakukan Manual Failover
redis-cli -h $NODE_IP -p $NODE_PORT CLUSTER FAILOVER

# Tunggu sebentar dan verifikasi
sleep 2
NEW_ROLE=$(redis-cli -h $NODE_IP -p $NODE_PORT role | head -n 1)

if [ "$NEW_ROLE" == "master" ]; then
    echo "Berhasil! Node $NODE_PORT sekarang kembali menjadi Master."
else
    echo "Gagal mengembalikan Node $NODE_PORT menjadi Master."
fi
