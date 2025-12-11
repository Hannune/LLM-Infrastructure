#!/bin/bash

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
NC='\033[0m'

echo -e "${GREEN}Starting WireGuard Docker Setup${NC}"

# Set defaults
SERVER_PUB_IP=${SERVER_PUB_IP:-auto}
SERVER_PUB_NIC=${SERVER_PUB_NIC:-eth0}
SERVER_WG_NIC=${SERVER_WG_NIC:-wg0}
SERVER_WG_IPV4=${SERVER_WG_IPV4:-10.66.66.1}
SERVER_WG_IPV6=${SERVER_WG_IPV6:-fd42:42:42::1}
SERVER_PORT=${SERVER_PORT:-51820}
CLIENT_DNS_1=${CLIENT_DNS_1:-1.1.1.1}
CLIENT_DNS_2=${CLIENT_DNS_2:-1.0.0.1}
ALLOWED_IPS=${ALLOWED_IPS:-0.0.0.0/0,::/0}
CLIENT_NAME=${CLIENT_NAME:-client1}

# Auto-detect public IP if set to auto
if [ "$SERVER_PUB_IP" = "auto" ]; then
    echo -e "${ORANGE}Auto-detecting public IP address...${NC}"
    # Try multiple methods to get public IP
    SERVER_PUB_IP=$(curl -s ifconfig.me || curl -s icanhazip.com || curl -s ipinfo.io/ip || echo "")

    if [ -z "$SERVER_PUB_IP" ]; then
        echo -e "${RED}Failed to auto-detect public IP. Please set SERVER_PUB_IP environment variable.${NC}"
        exit 1
    fi
    echo -e "${GREEN}Detected public IP: ${SERVER_PUB_IP}${NC}"
fi

# Check if WireGuard config already exists
if [ -f "/etc/wireguard/${SERVER_WG_NIC}.conf" ]; then
    echo -e "${GREEN}WireGuard configuration already exists. Using existing configuration.${NC}"
else
    echo -e "${ORANGE}Creating new WireGuard configuration...${NC}"

    # Create config directory if it doesn't exist
    mkdir -p /etc/wireguard
    chmod 700 /etc/wireguard

    # Generate server keys if they don't exist
    if [ ! -f "/etc/wireguard/server_private.key" ]; then
        wg genkey | tee /etc/wireguard/server_private.key | wg pubkey > /etc/wireguard/server_public.key
        chmod 600 /etc/wireguard/server_private.key
        chmod 600 /etc/wireguard/server_public.key
    fi

    SERVER_PRIV_KEY=$(cat /etc/wireguard/server_private.key)
    SERVER_PUB_KEY=$(cat /etc/wireguard/server_public.key)

    # Save parameters
    cat > /etc/wireguard/params <<EOF
SERVER_PUB_IP=${SERVER_PUB_IP}
SERVER_PUB_NIC=${SERVER_PUB_NIC}
SERVER_WG_NIC=${SERVER_WG_NIC}
SERVER_WG_IPV4=${SERVER_WG_IPV4}
SERVER_WG_IPV6=${SERVER_WG_IPV6}
SERVER_PORT=${SERVER_PORT}
SERVER_PRIV_KEY=${SERVER_PRIV_KEY}
SERVER_PUB_KEY=${SERVER_PUB_KEY}
CLIENT_DNS_1=${CLIENT_DNS_1}
CLIENT_DNS_2=${CLIENT_DNS_2}
ALLOWED_IPS=${ALLOWED_IPS}
EOF
    chmod 600 /etc/wireguard/params

    # Create server configuration
    cat > "/etc/wireguard/${SERVER_WG_NIC}.conf" <<EOF
[Interface]
Address = ${SERVER_WG_IPV4}/24,${SERVER_WG_IPV6}/64
ListenPort = ${SERVER_PORT}
PrivateKey = ${SERVER_PRIV_KEY}
PostUp = iptables -I INPUT -p udp --dport ${SERVER_PORT} -j ACCEPT
PostUp = iptables -I FORWARD -i ${SERVER_PUB_NIC} -o ${SERVER_WG_NIC} -j ACCEPT
PostUp = iptables -I FORWARD -i ${SERVER_WG_NIC} -j ACCEPT
PostUp = iptables -t nat -A POSTROUTING -o ${SERVER_PUB_NIC} -j MASQUERADE
PostUp = ip6tables -I FORWARD -i ${SERVER_WG_NIC} -j ACCEPT
PostUp = ip6tables -t nat -A POSTROUTING -o ${SERVER_PUB_NIC} -j MASQUERADE
PostDown = iptables -D INPUT -p udp --dport ${SERVER_PORT} -j ACCEPT
PostDown = iptables -D FORWARD -i ${SERVER_PUB_NIC} -o ${SERVER_WG_NIC} -j ACCEPT
PostDown = iptables -D FORWARD -i ${SERVER_WG_NIC} -j ACCEPT
PostDown = iptables -t nat -D POSTROUTING -o ${SERVER_PUB_NIC} -j MASQUERADE
PostDown = ip6tables -D FORWARD -i ${SERVER_WG_NIC} -j ACCEPT
PostDown = ip6tables -t nat -D POSTROUTING -o ${SERVER_PUB_NIC} -j MASQUERADE

EOF

    chmod 600 "/etc/wireguard/${SERVER_WG_NIC}.conf"

    echo -e "${GREEN}Server configuration created successfully${NC}"

    # Create initial client if specified
    if [ -n "$CLIENT_NAME" ]; then
        echo -e "${ORANGE}Creating client configuration for: ${CLIENT_NAME}${NC}"

        # Generate client keys
        CLIENT_PRIV_KEY=$(wg genkey)
        CLIENT_PUB_KEY=$(echo "${CLIENT_PRIV_KEY}" | wg pubkey)
        CLIENT_PRE_SHARED_KEY=$(wg genpsk)

        # Calculate client IP (increment last octet)
        CLIENT_WG_IPV4=$(echo "${SERVER_WG_IPV4}" | sed 's/\.[0-9]*$/.2/')
        CLIENT_WG_IPV6=$(echo "${SERVER_WG_IPV6}" | sed 's/::[0-9]*$/::2/')

        # Add client to server config
        cat >> "/etc/wireguard/${SERVER_WG_NIC}.conf" <<EOF
### Client ${CLIENT_NAME}
[Peer]
PublicKey = ${CLIENT_PUB_KEY}
PresharedKey = ${CLIENT_PRE_SHARED_KEY}
AllowedIPs = ${CLIENT_WG_IPV4}/32,${CLIENT_WG_IPV6}/128

EOF

        # Create client config file
        cat > "/etc/wireguard/${CLIENT_NAME}.conf" <<EOF
[Interface]
PrivateKey = ${CLIENT_PRIV_KEY}
Address = ${CLIENT_WG_IPV4}/24,${CLIENT_WG_IPV6}/64
DNS = ${CLIENT_DNS_1},${CLIENT_DNS_2}

[Peer]
PublicKey = ${SERVER_PUB_KEY}
PresharedKey = ${CLIENT_PRE_SHARED_KEY}
Endpoint = ${SERVER_PUB_IP}:${SERVER_PORT}
AllowedIPs = ${ALLOWED_IPS}
PersistentKeepalive = 25
EOF

        chmod 600 "/etc/wireguard/${CLIENT_NAME}.conf"

        echo -e "${GREEN}Client configuration created: /etc/wireguard/${CLIENT_NAME}.conf${NC}"
        echo ""
        echo -e "${GREEN}QR Code for mobile devices:${NC}"
        qrencode -t ansiutf8 < "/etc/wireguard/${CLIENT_NAME}.conf"
        echo ""
        echo -e "${ORANGE}Client configuration file content:${NC}"
        cat "/etc/wireguard/${CLIENT_NAME}.conf"
        echo ""
    fi
fi

# Load WireGuard kernel module
if ! lsmod | grep -q wireguard; then
    echo -e "${ORANGE}Loading WireGuard kernel module...${NC}"
    modprobe wireguard || echo -e "${ORANGE}Could not load wireguard module, it may already be built-in${NC}"
fi

# Start WireGuard
echo -e "${GREEN}Starting WireGuard interface: ${SERVER_WG_NIC}${NC}"
wg-quick up "${SERVER_WG_NIC}" || echo -e "${ORANGE}Interface may already be up${NC}"

# Show status
echo ""
echo -e "${GREEN}WireGuard Status:${NC}"
wg show

echo ""
echo -e "${GREEN}==================================${NC}"
echo -e "${GREEN}WireGuard is now running!${NC}"
echo -e "${GREEN}==================================${NC}"
echo ""
echo -e "Server public key: ${SERVER_PUB_KEY}"
echo -e "Listening on port: ${SERVER_PORT}/udp"
echo -e "Server endpoint: ${SERVER_PUB_IP}:${SERVER_PORT}"
echo ""
echo -e "${ORANGE}Client configuration files are located in: /etc/wireguard/${NC}"
echo -e "${ORANGE}To add more clients, use the add-client.sh script${NC}"
echo ""

# Keep container running and monitor WireGuard
while true; do
    sleep 300
    if ! wg show "${SERVER_WG_NIC}" > /dev/null 2>&1; then
        echo -e "${RED}WireGuard interface is down, attempting to restart...${NC}"
        wg-quick up "${SERVER_WG_NIC}"
    fi
done
