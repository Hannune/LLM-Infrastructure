#!/bin/bash
set -e

echo "🚀 Starting Multi-Server Monitoring Dashboard..."
echo ""

# Generate SSH key if it doesn't exist
if [ ! -f "/root/.ssh/id_rsa" ]; then
    echo "🔑 Generating SSH key pair..."
    ssh-keygen -t rsa -b 4096 -f /root/.ssh/id_rsa -N "" -q
    echo "✅ SSH key generated"
else
    echo "✅ SSH key already exists"
fi

# Export public key to shared directory
echo "📤 Exporting public key to ./ssh-keys/ directory..."
mkdir -p /ssh-keys-export
cp /root/.ssh/id_rsa.pub /ssh-keys-export/id_rsa.pub 2>/dev/null || true
chmod 644 /ssh-keys-export/id_rsa.pub 2>/dev/null || true

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 YOUR SSH PUBLIC KEY (also saved to ./ssh-keys/id_rsa.pub):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat /root/.ssh/id_rsa.pub
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 TO ADD THIS KEY TO YOUR SERVERS:"
echo ""
echo "   Method 1 (Automatic):"
echo "   ssh-copy-id -i ./ssh-keys/id_rsa.pub user@192.168.1.100"
echo ""
echo "   Method 2 (Manual - on each server):"
echo "   echo \"$(cat /root/.ssh/id_rsa.pub)\" >> ~/.ssh/authorized_keys"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Dashboard will be available at: http://localhost:8501"
echo ""

# Start Streamlit
exec streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true
