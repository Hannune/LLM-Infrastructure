#!/bin/bash

# Helper script to add a new WireGuard client
# Usage: docker exec -it wireguard /bin/bash -c "/etc/wireguard/add-client.sh client_name"

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
ORANGE='\033[0;33m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo -e "${RED}Error: Client name is required${NC}"
    echo "Usage: docker exec -it wireguard /bin/bash -c '/etc/wireguard/add-client.sh client_name'"
    exit 1
fi

CLIENT_NAME=$1

# Load server parameters
if [ ! -f /etc/wireguard/params ]; then
    echo -e "${RED}Error: WireGuard server not configured. Run the container first.${NC}"
    exit 1
fi

source /etc/wireguard/params

# Check if client already exists
if grep -q "### Client ${CLIENT_NAME}" "/etc/wireguard/${SERVER_WG_NIC}.conf"; then
    echo -e "${RED}Error: Client ${CLIENT_NAME} already exists${NC}"
    exit 1
fi

echo -e "${GREEN}Creating new client: ${CLIENT_NAME}${NC}"

# Generate client keys
CLIENT_PRIV_KEY=$(wg genkey)
CLIENT_PUB_KEY=$(echo "${CLIENT_PRIV_KEY}" | wg pubkey)
CLIENT_PRE_SHARED_KEY=$(wg genpsk)

# Find next available IP
# Get the last client number from the config
LAST_CLIENT_NUM=$(grep -oP "### Client \K\w+" "/etc/wireguard/${SERVER_WG_NIC}.conf" | wc -l)
NEXT_NUM=$((LAST_CLIENT_NUM + 2)) # Start from .2, .3, etc.

# Calculate client IP
BASE_IPV4=$(echo "${SERVER_WG_IPV4}" | sed 's/\.[0-9]*$//')
CLIENT_WG_IPV4="${BASE_IPV4}.${NEXT_NUM}"

BASE_IPV6=$(echo "${SERVER_WG_IPV6}" | sed 's/::[0-9]*$//')
CLIENT_WG_IPV6="${BASE_IPV6}::${NEXT_NUM}"

echo -e "${ORANGE}Assigning IP addresses:${NC}"
echo -e "  IPv4: ${CLIENT_WG_IPV4}/32"
echo -e "  IPv6: ${CLIENT_WG_IPV6}/128"

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

# Reload WireGuard configuration
wg syncconf "${SERVER_WG_NIC}" <(wg-quick strip "${SERVER_WG_NIC}")

echo ""
echo -e "${GREEN}Client ${CLIENT_NAME} created successfully!${NC}"
echo ""
echo -e "${GREEN}QR Code for mobile devices:${NC}"
qrencode -t ansiutf8 < "/etc/wireguard/${CLIENT_NAME}.conf"
echo ""
echo -e "${ORANGE}Configuration file saved to: /etc/wireguard/${CLIENT_NAME}.conf${NC}"
echo ""
echo -e "${ORANGE}Client configuration:${NC}"
cat "/etc/wireguard/${CLIENT_NAME}.conf"
echo ""
echo -e "${GREEN}To download the config file from the container:${NC}"
echo -e "docker cp wireguard:/etc/wireguard/${CLIENT_NAME}.conf ./${CLIENT_NAME}.conf"
echo ""
