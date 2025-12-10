# Docker Setup Guide

## Quick Start

### 1. Create Server Configuration

```bash
cp servers.example.yml servers.yml
nano servers.yml  # Edit with your server details
```

### 2. Build and Start

```bash
docker compose up -d
```

### 3. Setup SSH Keys (First Time Only)

```bash
# Enter the container
docker compose exec dashboard bash

# Generate SSH key
ssh-keygen -t rsa -b 4096 -f /root/.ssh/id_rsa -N ""

# Copy to your servers
ssh-copy-id -i /root/.ssh/id_rsa.pub user@192.168.1.100
ssh-copy-id -i /root/.ssh/id_rsa.pub user@192.168.1.101

# Test connection
ssh user@192.168.1.100

# Exit container
exit
```

### 4. Access Dashboard

Open your browser: **http://localhost:8501**

## Management Commands

```bash
# Start dashboard
docker compose up -d

# Stop dashboard
docker compose down

# View logs
docker compose logs -f

# Restart dashboard
docker compose restart

# Rebuild after code changes
docker compose up -d --build

# View container status
docker compose ps
```

## Using Existing SSH Keys

If you already have SSH keys on your host machine:

### Edit docker-compose.yml

```yaml
volumes:
  - ./servers.yml:/app/servers.yml:ro
  # Comment this line:
  # - ssh-keys:/root/.ssh

  # Uncomment this line:
  - ~/.ssh:/root/.ssh:ro
```

Then update `servers.yml` to use `/root/.ssh/id_rsa`

## Updating Configuration

### Update servers.yml

```bash
nano servers.yml  # Make changes
docker compose restart  # Restart to apply
```

### Update app.py

```bash
nano app.py  # Make changes
docker compose up -d --build  # Rebuild and restart
```

## Troubleshooting

### Container won't start

```bash
# Check logs
docker compose logs dashboard

# Check if port 8501 is already in use
sudo lsof -i :8501
```

### SSH connection issues

```bash
# Exec into container
docker compose exec dashboard bash

# Test SSH manually
ssh -v user@192.168.1.100

# Check SSH key permissions
ls -la /root/.ssh/
```

### Dashboard not loading

```bash
# Check container health
docker compose ps

# Check logs for errors
docker compose logs -f dashboard

# Restart container
docker compose restart
```

## Network Configuration

The dashboard needs to reach your servers. Ensure:

1. **Host network mode** (if servers are on same host):
   ```yaml
   network_mode: "host"
   ```

2. **Bridge network** (default - works for most cases)
   - Container can reach external IPs
   - Use server IPs directly in servers.yml

3. **Custom network** (for advanced setups)
   - Define your network in docker-compose.yml

## Security Notes

1. **SSH Keys**: Stored in Docker volume, isolated from host
2. **servers.yml**: Mounted read-only (`:ro`)
3. **Port exposure**: Only 8501 exposed
4. **Resource limits**: Prevents resource exhaustion

## Production Deployment

### Add authentication (Recommended)

Create `.streamlit/config.toml`:

```toml
[server]
headless = true
port = 8501

[browser]
gatherUsageStats = false

# Basic authentication
[auth]
enabled = true
cookieMaxAgeDays = 1
```

### Use environment variables for secrets

```bash
# Create .env file (don't commit to git)
echo "SSH_KEY_PASSWORD=your_password" > .env
```

Update docker-compose.yml:
```yaml
env_file:
  - .env
```

### Setup reverse proxy (nginx/traefik)

Example nginx config:
```nginx
server {
    listen 80;
    server_name monitor.yourdomain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

## Backup SSH Keys

```bash
# Backup SSH keys from Docker volume
docker compose exec dashboard cat /root/.ssh/id_rsa > backup_id_rsa
docker compose exec dashboard cat /root/.ssh/id_rsa.pub > backup_id_rsa.pub

# Restore
docker compose exec -T dashboard sh -c 'cat > /root/.ssh/id_rsa' < backup_id_rsa
docker compose exec dashboard chmod 600 /root/.ssh/id_rsa
```
