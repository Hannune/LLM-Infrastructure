#!/bin/bash
# Script to export SSH public key to host directory

echo "📤 Exporting SSH public key..."

# Check if SSH key exists
if [ ! -f "/root/.ssh/id_rsa.pub" ]; then
    echo "❌ SSH key not found. Generating new key..."
    ssh-keygen -t rsa -b 4096 -f /root/.ssh/id_rsa -N ""
fi

# Create export directory if it doesn't exist
mkdir -p /ssh-keys-export

# Copy public key
cp /root/.ssh/id_rsa.pub /ssh-keys-export/id_rsa.pub
chmod 644 /ssh-keys-export/id_rsa.pub

echo "✅ Public key exported to: ./ssh-keys/id_rsa.pub"
echo ""
echo "📋 Your public key:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat /root/.ssh/id_rsa.pub
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 To add this key to your servers, run on each server:"
echo "   echo \"$(cat /root/.ssh/id_rsa.pub)\" >> ~/.ssh/authorized_keys"
