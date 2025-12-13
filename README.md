<div id="top">

<div align="center">
 
# DISTRIBUTED-SYSTEM-REDIS-LAB

*Practical Analysis of Replication, Sentinel, and Clustering in Distributed Systems*

<p align="center">
<img src="https://img.shields.io/github/last-commit/reinoyk/DistributedSystem_FP?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/reinoyk/DistributedSystem_FP?style=flat&color=0080ff" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/reinoyk/DistributedSystem_FP?style=flat&color=0080ff" alt="repo-language-count">
<img src="https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white" alt="redis">
<img src="https://img.shields.io/badge/GNS3-Network%20Simulation-success" alt="gns3">
</p>

<em>Built with Python, Redis, and GNS3</em>

</div>
---

## Table of Contents

* [Overview](#overview)
* [Key Concepts](#key-concepts)
* [System Architecture](#system-architecture)
* [Experiment Scenarios](#experiment-scenarios)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Configuration](#configuration)
* [Usage](#usage)
* [Results & CAP Theorem](#results--cap-theorem)
* [How to Contribute](#how-to-contribute)
* [License](#license)

---

## Overview

**DistributedSystem-Redis-Lab** is a practical implementation for analyzing three fundamental mechanisms in distributed systems using **Redis**:

* **Replication**
* **Sentinel (High Availability)**
* **Cluster (Sharding)**

Through network simulations using **GNS3** and **Localhost**, this project goes beyond theory by validating **Eventual Consistency**, measuring replication lag, testing **Automatic Failover** during server crashes, and demonstrating **Load Balancing** across distributed nodes.

The repository includes modular **Python scripts** for automated testing, logging, and visualization to empirically validate the **CAP Theorem** in real-world scenarios.

---

## Key Concepts

This project focuses on three core pillars of Redis distributed capabilities:

### 🔄 Replication (Master–Replica)

* Asynchronous data replication from a master node to one or more replicas
* Emphasis on **Eventual Consistency**
* Measurement of replication lag using Python-based monitoring scripts

### 🛡️ Sentinel (High Availability)

* Continuous monitoring of Redis nodes
* Automatic failure detection and **master promotion**
* Ensures high availability with minimal downtime

### 🧩 Cluster (Sharding)

* Horizontal scaling through automatic data partitioning
* Uses hash slots to distribute keys across multiple nodes
* Handles request routing transparently

---

## System Architecture

Experiments are conducted in two environments:

1. **GNS3 Network Simulation**
   Simulates real-world network conditions such as latency, packet loss, and partitions.

2. **Localhost Environment**
   Used for rapid prototyping and functional validation of automation scripts.

### Typical Topology

* **1 Master Node** (Read/Write)
* **2+ Replica Nodes** (Read-only / Backup)
* **3 Sentinel Instances** (Quorum-based decision making)
* **Python Clients** (Load generation, monitoring, and metrics collection)

---

## Experiment Scenarios

The codebase is organized into modular experiment scenarios:

1. **Consistency Check**
   Measures the time difference between a write on the master and its visibility on replicas.

2. **Failover Test**
   Simulates a Redis master crash (e.g., `SIGTERM`) and records the time taken by Sentinel to elect a new master.

3. **Sharding Analysis**
   Inserts bulk data into a Redis Cluster and verifies key distribution across hash slots and nodes.

---

## Getting Started

### Prerequisites

* **Python 3.8+**
* **Redis Server** (local or VM-based)
* **GNS3** (optional, for advanced network simulation)
* **pip** (Python package manager)

---

### Installation

1. Clone the repository:

```bash
git clone https://github.com/reinoyk/DistributedSystem_FP.git
```

2. Navigate to the project directory:

```bash
cd DistributedSystem_FP
```

3. Install Python dependencies:

```bash
pip install redis pandas matplotlib
```

---

### Configuration

* **Redis Configuration Files**
  Located in the `configs/` directory (e.g., `redis_master.conf`, `redis_replica.conf`, `redis_sentinel.conf`).

* **Python Script Configuration**
  Update IP addresses and ports in `config.py` or at the top of each script to match your GNS3 or localhost setup.

---

## Usage

### 1. Replication & Consistency Test

Start all Redis instances, then run:

```bash
python test_replication.py
```

**Output:**

* Average replication lag (milliseconds)
* Timestamped logs for each write/read operation

---

### 2. Sentinel Failover Test

Start Redis Sentinel processes, then execute:

```bash
python test_failover.py
```

While the script is running, manually stop the master Redis service.

**Output:**

* Failure detection timestamp
* New master election time
* Total failover duration

---

### 3. Cluster Sharding Demo

Ensure the Redis Cluster is properly initialized, then run:

```bash
python test_cluster.py
```

**Output:**

* Distribution of keys across cluster nodes
* Mapping of keys to hash slots

---

## Results & CAP Theorem

The experimental results provide empirical insights into the **CAP Theorem**:

* **Consistency vs Availability**
  During network partitions or master failures, Redis Sentinel prioritizes **Availability** by promoting a new master. This may temporarily sacrifice **strong consistency**, potentially causing minor data loss if the old master accepted writes before demotion.

* **Partition Tolerance & Sharding**
  Redis Cluster demonstrates effective horizontal scalability and fault isolation, with the limitation that multi-key operations must reside in the same hash slot.

Detailed logs, metrics, and visualizations are available in the `results/` directory.

---

## How to Contribute

Contributions are welcome and encouraged.

1. Fork the project
2. Create a new feature branch:

```bash
git checkout -b feature/NewScenario
```

3. Commit your changes
4. Push to your branch
5. Open a Pull Request

Possible extensions include:

* Redlock (Distributed Locking)
* AOF vs RDB persistence benchmarking
* Network partition tolerance experiments

---

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

<p align="center"><a href="#top">⬆ Back to Top</a></p>
