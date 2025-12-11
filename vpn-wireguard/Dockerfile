FROM debian:bookworm-slim

# Install required packages
RUN apt-get update && \
    apt-get install -y \
    wireguard \
    wireguard-tools \
    iptables \
    iproute2 \
    qrencode \
    net-tools \
    procps \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create wireguard directory
RUN mkdir -p /etc/wireguard

# Copy scripts
COPY entrypoint.sh /entrypoint.sh
COPY add-client.sh /add-client.sh
RUN chmod +x /entrypoint.sh /add-client.sh

# Expose WireGuard port (default 51820, can be changed via env)
EXPOSE 51820/udp

ENTRYPOINT ["/entrypoint.sh"]
