# Quick Start Guide - 5 Minutes to Dashboard

Follow these steps to get your monitoring dashboard running in 5 minutes.

## Prerequisites Check

- [ ] Docker and Docker Compose installed
- [ ] Network access to your servers
- [ ] Know your server IP addresses and SSH usernames

## Step-by-Step Setup

### 1. Configure Servers (1 minute)

```bash
cd /home/tetae/Projects/claude-code/multi-server-monitoring-dashboard

# Copy example config
cp servers.example.yml servers.yml

# Edit with your details
nano servers.yml
```

**Replace these values:**
```yaml
servers:
  - name: "My Server"           # ← Change this
    host: "192.168.1.100"       # ← Your server IP
    username: "myuser"          # ← Your SSH username
    port: 22                    # ← Usually 22
    key_file: "/root/.ssh/id_rsa"  # ← Keep as is
```

Save and exit (Ctrl+X, Y, Enter)

### 2. Start Dashboard (30 seconds)

```bash
docker compose up -d
```

Wait for:
```
✔ Container server-monitor-dashboard  Started
```

### 3. Setup SSH Keys (2 minutes)

```bash
# Enter container
docker compose exec dashboard bash

# Generate key (press Enter 3 times)
ssh-keygen -t rsa -b 4096 -f /root/.ssh/id_rsa -N ""

# Copy to your server (replace with your details)
ssh-copy-id -i /root/.ssh/id_rsa.pub myuser@192.168.1.100
```

**You'll be asked for password ONCE**

Test it works:
```bash
ssh myuser@192.168.1.100
# Should connect without password!
exit
```

Exit container:
```bash
exit
```

### 4. Access Dashboard (10 seconds)

Open browser: **http://localhost:8501**

You should see:
- 🟢 Green status for your server
- Live metrics in tabs

## Troubleshooting

### "Connection Error" in dashboard

**Test SSH manually:**
```bash
docker compose exec dashboard bash
ssh myuser@192.168.1.100
```

If it asks for password, SSH keys aren't set up correctly. Repeat Step 3.

### Can't access http://localhost:8501

**Check container:**
```bash
docker compose ps
```

Should show "Up". If not:
```bash
docker compose logs dashboard
```

### Port 8501 already in use

**Change port in docker-compose.yml:**
```yaml
ports:
  - "8502:8501"  # Changed from 8501:8501
```

Then access: http://localhost:8502

## Next Steps

### Add More Servers

```bash
# Edit config
nano servers.yml

# Add another server (copy the block)
# Restart dashboard
docker compose restart

# Setup SSH for new server
docker compose exec dashboard bash
ssh-copy-id -i /root/.ssh/id_rsa.pub user@new-server-ip
exit
```

### Enable Auto-Refresh

1. Open dashboard: http://localhost:8501
2. Check "Auto Refresh" in sidebar
3. Set interval (60 seconds recommended)
4. Watch the countdown timer

### Backup SSH Keys

```bash
docker compose exec dashboard tar czf - /root/.ssh > ssh-keys-backup.tar.gz
```

Store this file safely!

## Common Commands

```bash
# View logs
docker compose logs -f

# Restart
docker compose restart

# Stop
docker compose down

# Start again
docker compose up -d

# Update after code changes
docker compose up -d --build
```

## Need More Help?

- Detailed setup: [DEPLOYMENT.md](DEPLOYMENT.md)
- SSH issues: [SSH_SETUP.md](SSH_SETUP.md)
- Docker issues: [DOCKER_SETUP.md](DOCKER_SETUP.md)

## Success Checklist

- [ ] Docker container running (`docker compose ps`)
- [ ] servers.yml configured with your IPs
- [ ] SSH keys generated
- [ ] SSH keys copied to all servers
- [ ] Can SSH without password from container
- [ ] Dashboard accessible at http://localhost:8501
- [ ] Servers show 🟢 Online status
- [ ] Can see GPU/Docker/Memory stats

If all checked, you're done! 🎉
