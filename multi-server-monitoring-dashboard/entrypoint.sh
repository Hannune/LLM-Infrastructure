#!/bin/bash
set -e

echo "🚀 Starting Multi-Server Monitoring Dashboard..."
echo "🌐 Dashboard will be available at: http://localhost:8501"
echo ""

# Start Streamlit
exec streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true
