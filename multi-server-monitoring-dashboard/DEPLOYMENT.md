# Deployment Guide - Complete Walkthrough

## 🚀 Quick Start (Recommended - Docker)

### Prerequisites
- Docker and Docker Compose installed
- Network access to your servers
- SSH access to servers you want to monitor

### Step 1: Clone/Navigate to Project

```bash
cd /home/tetae/Projects/claude-code/multi-server-monitoring-dashboard
```

### Step 2: Configure Servers

```bash
cp servers.example.yml servers.yml
nano servers.yml
```

Edit to match your environment:
```yaml
servers:
  - name: "My GPU Server"
    host: "192.168.1.100"      # Your server IP
    username: "myuser"          # Your SSH username
    port: 22
    key_file: "/root/.ssh/id_rsa"  # Path inside container
```

### Step 3: Build and Start

```bash
docker compose up -d
```

### Step 4: Setup SSH Keys (First Time Only)

```bash
# Enter the container
docker compose exec dashboard bash

# Generate SSH key (press Enter for all prompts)
ssh-keygen -t rsa -b 4096 -f /root/.ssh/id_rsa -N ""

# Copy key to each server (you'll be prompted for password once)
ssh-copy-id -i /root/.ssh/id_rsa.pub myuser@192.168.1.100

# Test connection (should work without password)
ssh myuser@192.168.1.100

# Exit container
exit
```

### Step 5: Access Dashboard

Open browser: **http://localhost:8501**

✅ **Done!** Your dashboard should now be monitoring your servers.

---

## 📋 Detailed Setup Options

### Option 1: Docker (Isolated, Production-Ready)

**Pros:**
- Isolated environment
- Easy to deploy/remove
- Persistent SSH keys in Docker volume
- Resource limits
- Easy updates

**Setup:**
```bash
# Build and start
docker compose up -d

# View logs
docker compose logs -f

# Stop
docker compose down
```

### Option 2: Docker with Host SSH Keys

If you already have SSH keys set up on your host:

**Edit docker-compose.yml:**
```yaml
volumes:
  - ./servers.yml:/app/servers.yml:ro
  - ~/.ssh:/root/.ssh:ro  # Mount your existing SSH directory
```

**Update servers.yml:**
```yaml
servers:
  - name: "Server"
    host: "192.168.1.100"
    username: "youruser"
    key_file: "/root/.ssh/id_rsa"  # Points to mounted key
```

### Option 3: Native Python (Development)

**Setup:**
```bash
# Install dependencies
pip install -r requirements.txt

# Configure servers
cp servers.example.yml servers.yml
nano servers.yml

# Update servers.yml to use host paths
# key_file: "~/.ssh/id_rsa"  # Uses your local SSH key

# Run
streamlit run app.py
```

---

## 🔑 SSH Key Setup - Detailed

### Creating New SSH Keys

```bash
# On your host OR inside Docker container
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa

# You'll see:
# Generating public/private rsa key pair.
# Enter passphrase (empty for no passphrase): [Press Enter]
# Enter same passphrase again: [Press Enter]
```

### Copying Keys to Servers

**Method 1: ssh-copy-id (easiest)**
```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub user@192.168.1.100
# Enter password when prompted
```

**Method 2: Manual**
```bash
# Display your public key
cat ~/.ssh/id_rsa.pub

# On each target server:
mkdir -p ~/.ssh
echo "YOUR_PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

### Testing SSH Connection

```bash
# Should connect without password
ssh user@192.168.1.100

# If it asks for password, SSH key setup failed
```

### Troubleshooting SSH

**Permission denied:**
```bash
# Fix permissions
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 700 ~/.ssh
```

**Host key verification failed:**
```bash
# Remove old host key
ssh-keygen -R 192.168.1.100

# Connect again (will ask to accept new key)
ssh user@192.168.1.100
```

---

## ⚙️ Configuration Reference

### servers.yml Format

```yaml
servers:
  - name: "Server Display Name"      # Required: Shows in dashboard
    host: "IP or hostname"            # Required: Server address
    username: "ssh_username"          # Required: SSH login user
    port: 22                          # Optional: Default is 22
    key_file: "/path/to/key"          # Required: SSH private key path

  - name: "Another Server"
    host: "192.168.1.101"
    username: "admin"
    port: 22
    key_file: "/root/.ssh/id_rsa"
```

### Auto-Refresh Settings

The new implementation includes:

1. **Non-blocking refresh** - UI remains responsive
2. **Timer display** - Shows countdown to next refresh
3. **Configurable interval** - 30-300 seconds
4. **Manual override** - Refresh Now button

**Benefits:**
- ✅ No UI freezing
- ✅ SSH connections only made at intervals (resource efficient)
- ✅ Connections closed immediately (security)
- ✅ Shows time since last update

---

## 🔒 Security Best Practices

### 1. SSH Key Security

```bash
# Use strong keys (4096-bit)
ssh-keygen -t rsa -b 4096

# Set proper permissions
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub

# Consider using passphrase-protected keys
ssh-keygen -t rsa -b 4096 -N "your_passphrase"
```

### 2. Network Security

- Run on private network only
- Don't expose port 8501 to the internet
- Use VPN if accessing remotely
- Consider firewall rules on monitored servers

### 3. Docker Volume Security

```bash
# SSH keys stored in isolated Docker volume
docker volume inspect multi-server-monitoring-dashboard_ssh-keys

# Backup keys securely
docker compose exec dashboard tar czf - /root/.ssh > ssh-keys-backup.tar.gz
```

### 4. Read-Only Mounts

The docker-compose.yml mounts servers.yml as read-only:
```yaml
volumes:
  - ./servers.yml:/app/servers.yml:ro  # :ro = read-only
```

---

## 🛠️ Maintenance

### Updating the Application

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker compose up -d --build
```

### Adding New Servers

```bash
# Edit configuration
nano servers.yml

# Add new server:
# - name: "New Server"
#   host: "192.168.1.102"
#   username: "user"
#   port: 22
#   key_file: "/root/.ssh/id_rsa"

# Restart dashboard
docker compose restart

# Setup SSH for new server
docker compose exec dashboard bash
ssh-copy-id user@192.168.1.102
exit
```

### Viewing Logs

```bash
# Follow logs in real-time
docker compose logs -f

# View last 50 lines
docker compose logs --tail=50

# View specific service
docker compose logs dashboard
```

### Backing Up Configuration

```bash
# Backup servers.yml
cp servers.yml servers.yml.backup

# Backup SSH keys from Docker
docker compose exec dashboard tar czf - /root/.ssh | cat > ssh-backup.tar.gz
```

---

## 🐛 Troubleshooting

### Dashboard won't start

```bash
# Check if port is in use
sudo lsof -i :8501

# Check container logs
docker compose logs dashboard

# Try rebuilding
docker compose down
docker compose up -d --build
```

### SSH connection failures

```bash
# Exec into container
docker compose exec dashboard bash

# Test SSH with verbose output
ssh -vvv user@192.168.1.100

# Check if server is reachable
ping 192.168.1.100

# Verify SSH key
ls -la /root/.ssh/
cat /root/.ssh/id_rsa.pub
```

### "Configuration file not found"

```bash
# Check if servers.yml exists
ls -la servers.yml

# Verify it's mounted in container
docker compose exec dashboard ls -la /app/servers.yml

# Check docker-compose.yml volume mount
cat docker-compose.yml | grep servers.yml
```

### GPU monitoring not working

```bash
# Check if nvidia-smi works on target server
ssh user@192.168.1.100 nvidia-smi

# If not found, install NVIDIA drivers on target server
```

### Docker containers not showing

```bash
# Check if user can access Docker on target server
ssh user@192.168.1.100 docker ps

# If permission denied, add user to docker group on target:
# sudo usermod -aG docker user
```

---

## 📊 Resource Usage

### Docker Container
- **CPU**: ~0.5-1% idle, ~5-10% during data collection
- **Memory**: ~200-300 MB
- **Disk**: ~500 MB (including base image)

### Network
- **SSH connections**: Made only at refresh intervals
- **Connection duration**: ~1-2 seconds per server
- **Bandwidth**: Minimal (~1-5 KB per server per refresh)

### Auto-Refresh Recommendations

| Server Count | Recommended Interval | Reasoning |
|--------------|---------------------|-----------|
| 1-5 servers  | 30-60 seconds       | Low overhead |
| 6-10 servers | 60-120 seconds      | Moderate load |
| 10+ servers  | 120-300 seconds     | Avoid SSH throttling |

---

## 🎯 Production Checklist

- [ ] SSH keys generated and copied to all servers
- [ ] servers.yml configured with correct IPs and usernames
- [ ] Test SSH connection to each server works without password
- [ ] Docker container starts successfully
- [ ] Dashboard loads at http://localhost:8501
- [ ] All servers show "🟢 Online" status
- [ ] Auto-refresh works without UI freezing
- [ ] Resource usage is acceptable
- [ ] Backup of SSH keys created
- [ ] Documentation reviewed

---

## 📞 Getting Help

If you encounter issues:

1. Check logs: `docker compose logs -f`
2. Test SSH manually: `docker compose exec dashboard ssh user@server-ip`
3. Verify configuration: `cat servers.yml`
4. Check network: `docker compose exec dashboard ping server-ip`
5. Review this guide's troubleshooting section

For SSH key issues, see [SSH_SETUP.md](SSH_SETUP.md)
For Docker issues, see [DOCKER_SETUP.md](DOCKER_SETUP.md)
