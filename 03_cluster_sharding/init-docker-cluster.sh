#!/bin/bash

echo "Starting Redis Cluster creation..."

# Wait a bit for nodes to be ready
echo "Waiting 5s for containers to start..."
sleep 5

# Create the cluster using the internal container network, but pointing to the announced IPs?
# Actually, since we want the cluster to be usable from HOST, we should tell them to meet as 127.0.0.1.
# BUT, from INSIDE the container (where redis-cli runs), 127.0.0.1 is the container itself.
# This is tricky.
# If we run this command from the HOST (Windows), we use 127.0.0.1:7000.
# If we run from inside, we must be careful.
#
# Strategy: Since the user is on Windows, they might NOT have redis-cli installed on the host.
# We must use 'docker exec' to run redis-cli.
# But 'docker exec' runs inside the container network.
# If we tell node-0 to "meet" 127.0.0.1:7001, it will try to connect to ITSELF on port 7001 (which fails, because it listens on 7000).
#
# Solution for Docker Desktop (Mac/Windows):
# We use `host.docker.internal` to refer to the host, OR we use the service names if we were staying internal.
# BUT, we forced `cluster-announce-ip 127.0.0.1`.
# So the nodes believes they are at 127.0.0.1.
# The internal `meet` messages must reach the other nodes.
#
# If I use `docker exec -it redis-node-7000 redis-cli --cluster create 127.0.0.1:7000 127.0.0.1:7001 ...`
# The node-7000 will try to talk to 127.0.0.1:7001. Inside its container, nothing is on 7001. Fail.
#
# ALTERNATIVE:
# Use `network_mode: host` (Linux only). Windows: No.
#
# HYBRID APPROACH:
# We need the nodes to communicate internally via Docker names (node-0, node-1...) or shared network,
# BUT announce 127.0.0.1 to external clients.
# Redis allows separate `announce-ip` (what clients see) vs what it binds to.
#
# However, the Bus/Gossip protocol uses the *same* IP usually unless configured otherwise.
#
# Let's try the simple "Host Networking" simulation for Windows:
# We set `cluster-announce-ip 127.0.0.1`.
# We NEED the init command to run from the HOST if possible.
#
# Valid approach for Windows User without local redis-cli:
# Use a separate container that has host networking or uses `host.docker.internal`? No, complex.
#
# EASIEST FIX:
# Instruct the user to run the init command *if* they have redis-cli.
# IF NOT, we try to use `docker exec` but use the private IPs for the initial meet?
# No, if we init with private IPs, `cluster_verification.py` will receive private IPs (172.18.x.x) and fail to connect from Windows.
#
# WAIT.
# If I run `docker exec ... redis-cli --cluster create host.docker.internal:7000 host.docker.internal:7001 ...`
# Then the nodes will meet at `host.docker.internal`.
# And we set `cluster-announce-ip 127.0.0.1`?
#
# Let's try a proven pattern:
# We use the `host.docker.internal` for the create command if running from inside Docker.
#
# docker exec redis-node-7000 redis-cli --cluster create \
#   host.docker.internal:7000 \
#   host.docker.internal:7001 \
#   ...
#
# Note: `host.docker.internal` resolves to the host IP from inside the container.
# The host (Windows) is listening on 7000, 7001 (mapped from containers).
# So `host.docker.internal:7000` -> Windows:7000 -> container:7000.
# This works!
#
# Requirement: User updates hosts file? No, Docker Desktop handles `host.docker.internal` automatically.
#
# Let's write the script.

echo "Creating cluster using host.docker.internal to route via Host Ports..."

docker exec redis-node-7000 redis-cli --cluster create \
  host.docker.internal:7000 \
  host.docker.internal:7001 \
  host.docker.internal:7002 \
  host.docker.internal:7003 \
  host.docker.internal:7004 \
  host.docker.internal:7005 \
  --cluster-replicas 1 --cluster-yes

echo "Cluster created."
