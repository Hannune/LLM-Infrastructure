# Multi-Server Monitoring Dashboard

**Real-time Streamlit dashboard for monitoring multiple Linux servers running local LLMs**

Monitor CPU, memory, disk, GPU (NVIDIA), and Docker containers across your fleet of LLM servers from a single web interface.

## Features

- **Real-Time Monitoring** - Live stats from multiple servers
- **GPU Monitoring** - NVIDIA GPU usage and temperature
- **Docker Container Status** - Track running LLM containers
- **SSH-Based** - Secure key-based authentication
- **Auto SSH Key Generation** - Keys generated and exported automatically
- **Smart Auto-Refresh** - Non-blocking UI with configurable intervals
- **Concurrent Collection** - Fast parallel data gathering
- **Docker Support** - Easy deployment with Docker Compose
- **100% Local** - No cloud dependencies

## Quick Start (Docker - Recommended)

1. **Configure servers:**
```bash
cp servers.example.yml servers.yml
nano servers.yml  # Edit with your server details
```

2. **Start with Docker:**
```bash
docker compose up -d
```

3. **Access dashboard:**
```
http://localhost:8501
```

**Note:** The dashboard uses your host SSH keys from `~/.ssh/`. Make sure you have SSH key access configured to all your servers.

📖 **Guides:**
- **Simplified setup:** [EASY_SETUP.md](EASY_SETUP.md) ⭐ Start here!
- **Detailed walkthrough:** [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)
- **Complete guide:** [DEPLOYMENT.md](DEPLOYMENT.md)

## Alternative: Native Python Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure servers:**
```bash
cp servers.example.yml servers.yml
nano servers.yml
```

3. **Setup SSH keys:**
```bash
ssh-keygen -t rsa -b 4096
ssh-copy-id user@server-ip
```

4. **Run:**
```bash
streamlit run app.py
```

## Configuration

### servers.yml

```yaml
servers:
  - name: "GPU Server 1"
    host: "192.168.1.100"
    username: "your_username"
    port: 22
    key_file: "~/.ssh/id_rsa"
    
  - name: "GPU Server 2"
    host: "192.168.1.101"
    username: "your_username"
    port: 22
    key_file: "~/.ssh/id_rsa"
```

### SSH Key Setup

Ensure passwordless SSH access to all servers:

```bash
# Test connection
ssh -i ~/.ssh/id_rsa user@server-ip

# Should connect without password prompt
```

## Monitored Metrics

### System
- **Uptime** - Server uptime
- **CPU Usage** - Current CPU utilization
- **Memory** - RAM usage and available memory
- **Disk** - Disk space usage for all mounts

### GPU (NVIDIA)
- GPU utilization percentage
- Memory usage
- Temperature
- Running processes

### Docker
- Running containers
- Container status
- Resource usage

## Usage

### Auto-Refresh (Improved)
Smart auto-refresh with non-blocking UI:
- **Enable:** Check "Auto Refresh" in sidebar
- **Configure:** Set interval (30-300 seconds)
- **Monitor:** Shows countdown timer and last refresh time
- **Efficient:** Only connects to servers at intervals (not continuously)
- **Secure:** Connections closed immediately after data collection
- **Non-blocking:** UI remains responsive during refresh cycle

**Benefits over simple refresh:**
- ✅ No UI freezing
- ✅ Resource-efficient (SSH connections only when needed)
- ✅ Secure (no persistent connections)
- ✅ Visual feedback (countdown timer)

### Manual Refresh
Click "Refresh Now" button in sidebar

### Dashboard Layout
- **Status Overview** - Quick status cards for all servers
- **Detailed Tabs** - Per-server detailed metrics
  - Disk Usage
  - Memory
  - GPU (NVIDIA)
  - Docker Containers
  - System Info

## Use Cases

### LLM Fleet Monitoring
Monitor multiple servers running Ollama, vLLM, or other local LLM deployments:
- Track GPU utilization across servers
- Monitor Docker containers (ollama, vllm, etc.)
- Check available disk space for models

### Multi-GPU Setup
Monitor servers with multiple GPUs:
- See which GPUs are in use
- Track VRAM usage per GPU
- Identify idle GPUs

### Development Environment
Monitor development servers:
- Track resource usage during model training
- Monitor Docker container health
- Check system availability

## Docker Deployment

### Management Commands

```bash
# Start
docker compose up -d

# Stop
docker compose down

# View logs
docker compose logs -f

# Restart
docker compose restart

# Rebuild after updates
docker compose up -d --build
```

### Volume Persistence

SSH keys are stored in a Docker volume for persistence:
```bash
# Backup SSH keys
docker compose exec dashboard tar czf - /root/.ssh > ssh-backup.tar.gz

# View volume
docker volume inspect multi-server-monitoring-dashboard_ssh-keys
```

## Architecture

```
┌──────────────────────────┐
│   Docker Container       │
│  ┌──────────────────┐    │
│  │   Streamlit      │    │
│  │   Dashboard      │:8501├─── Port 8501 → localhost:8501
│  └────────┬─────────┘    │
│           │ SSH Keys     │
│      /root/.ssh/         │
└───────────┼──────────────┘
            │ SSH (Paramiko)
       ┌────┴────┬──────────┬──────────┐
       │         │          │          │
   ┌───▼───┐ ┌──▼──┐  ┌────▼────┐ ┌───▼────┐
   │Server1│ │Srv2 │  │Server 3 │ │Server 4│
   │+ GPU  │ │+GPU │  │  + GPU  │ │  +GPU  │
   │+Docker│ │+Dock│  │ +Docker │ │ +Docker│
   └───────┘ └─────┘  └─────────┘ └────────┘
     LOCAL    LOCAL      LOCAL      LOCAL
```

## Troubleshooting

### SSH Connection Failed
```bash
# Test SSH connection manually
ssh -i ~/.ssh/id_rsa user@server-ip

# Check key permissions
chmod 600 ~/.ssh/id_rsa
```

### NVIDIA-SMI Not Found
- Install NVIDIA drivers on target server
- Verify: `ssh user@server nvidia-smi`

### Docker Not Accessible
```bash
# Add user to docker group on remote server
sudo usermod -aG docker your_username

# Logout and login again
```

### Dashboard Not Loading
```bash
# Check if Streamlit is running
ps aux | grep streamlit

# Restart dashboard
streamlit run app.py
```

## Security Considerations

1. **Password Protection** - Enable authentication for production (see [AUTHENTICATION.md](AUTHENTICATION.md))
2. **SSH Keys** - Use strong SSH keys (4096-bit RSA)
3. **Key Permissions** - Ensure keys are chmod 600
4. **Firewall** - Restrict SSH access to known IPs
5. **HTTPS** - Use reverse proxy with SSL for production
6. **Local Network** - Best used within private network
7. **No Root Access** - Don't use root user for monitoring

### Setting Up Password Protection

```bash
# Generate password hash
python3 generate_password_hash.py

# Add to .env file
cp .env.example .env
nano .env  # Add DASHBOARD_PASSWORD_HASH=...

# Restart
docker compose restart
```

See [AUTHENTICATION.md](AUTHENTICATION.md) for detailed instructions.

## Requirements

- Python 3.8+
- SSH access to monitored servers
- Servers running Linux (Ubuntu/Debian/CentOS)
- NVIDIA drivers (for GPU monitoring)
- Docker (for container monitoring)

## Performance

- Concurrent data collection using ThreadPoolExecutor
- Fast updates even with 10+ servers
- Minimal resource usage (~50MB RAM)

## Documentation

- **[AUTHENTICATION.md](AUTHENTICATION.md)** - Password protection setup
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete deployment walkthrough
- **[SSH_SETUP.md](SSH_SETUP.md)** - Detailed SSH key setup guide
- **[DOCKER_SETUP.md](DOCKER_SETUP.md)** - Docker-specific instructions

## What's New

### v2.3 Updates (Latest)
- ✅ **Optimized SSH connection stability** - Fixed random connection failures
- ✅ **Improved performance** - Faster data collection with optimized timeouts
- ✅ **Host SSH key support** - Uses existing host SSH keys
- ✅ **Simplified deployment** - Cleaner entrypoint with less verbose output
- ✅ **Grid layout** - Better UI for 10+ servers (4 per row)

### v2.2 Updates
- ✅ **Password authentication** with bcrypt hashing
- ✅ Secure login page
- ✅ Optional authentication (can be disabled)

### v2.0 Updates
- ✅ Docker Compose support for easy deployment
- ✅ Fixed auto-refresh (non-blocking UI)
- ✅ SSH key path expansion (supports `~/.ssh/`)
- ✅ Comprehensive documentation

## License

MIT
