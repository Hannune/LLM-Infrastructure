# Multi-Server Monitoring Dashboard

**Real-time Streamlit dashboard for monitoring multiple Linux servers running local LLMs**

Monitor CPU, memory, disk, GPU (NVIDIA), and Docker containers across your fleet of LLM servers from a single web interface.

## Features

- **Real-Time Monitoring** - Live stats from multiple servers
- **GPU Monitoring** - NVIDIA GPU usage and temperature
- **Docker Container Status** - Track running LLM containers
- **SSH-Based** - Secure key-based authentication
- **Auto-Refresh** - Configurable polling intervals
- **Concurrent Collection** - Fast parallel data gathering
- **100% Local** - No cloud dependencies

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure servers:**
```bash
cp servers.example.yml servers.yml
# Edit servers.yml with your server details
```

3. **Setup SSH keys:**
```bash
# Generate SSH key if you don't have one
ssh-keygen -t rsa -b 4096

# Copy key to servers
ssh-copy-id user@server-ip
```

4. **Run dashboard:**
```bash
streamlit run app.py
```

5. **Access dashboard:**
```
http://localhost:8501
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

### Auto-Refresh
Enable auto-refresh from the sidebar:
- Check "Auto Refresh"
- Set refresh interval (30-300 seconds)

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

## Architecture

```
┌──────────────────┐
│   Streamlit      │
│   Dashboard      │ :8501
└────────┬─────────┘
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

1. **SSH Keys** - Use strong SSH keys (4096-bit RSA)
2. **Key Permissions** - Ensure keys are chmod 600
3. **Firewall** - Restrict SSH access to known IPs
4. **Local Network** - Best used within private network
5. **No Root Access** - Don't use root user for monitoring

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

## License

MIT
