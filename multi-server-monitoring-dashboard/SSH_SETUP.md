# SSH Key Setup Guide for Multi-Server Monitoring

## Quick Setup (Inside Docker Container)

### Step 1: Generate SSH Key in Container

```bash
# After starting the container, exec into it
docker compose exec dashboard bash

# Generate SSH key (press Enter for all prompts to use defaults)
ssh-keygen -t rsa -b 4096 -f /root/.ssh/id_rsa -N ""

# This creates:
# - /root/.ssh/id_rsa (private key)
# - /root/.ssh/id_rsa.pub (public key)
```

### Step 2: Copy Public Key to Target Servers

**Option A: Using ssh-copy-id (recommended)**
```bash
# From inside the container
ssh-copy-id -i /root/.ssh/id_rsa.pub user@192.168.1.100
ssh-copy-id -i /root/.ssh/id_rsa.pub user@192.168.1.101
```

**Option B: Manual Copy**
```bash
# From inside the container, display your public key
cat /root/.ssh/id_rsa.pub

# Then on each target server, add it to authorized_keys
# SSH into each server and run:
echo "YOUR_PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

### Step 3: Test Connection

```bash
# From inside the container
ssh -i /root/.ssh/id_rsa user@192.168.1.100

# Should connect without password prompt
```

### Step 4: Update servers.yml

```yaml
servers:
  - name: "GPU Server 1"
    host: "192.168.1.100"
    username: "your_username"
    port: 22
    key_file: "/root/.ssh/id_rsa"  # Use absolute path
```

## Alternative: Using Existing SSH Keys (Volume Mount)

If you already have SSH keys on your host machine:

### Step 1: Update docker-compose.yml

```yaml
volumes:
  - ./servers.yml:/app/servers.yml
  - ~/.ssh:/root/.ssh:ro  # Mount your existing SSH keys (read-only)
```

### Step 2: Update servers.yml

```yaml
servers:
  - name: "GPU Server 1"
    host: "192.168.1.100"
    username: "your_username"
    port: 22
    key_file: "/root/.ssh/id_rsa"  # Points to mounted key
```

## Troubleshooting

### Permission Denied

```bash
# Inside container
chmod 600 /root/.ssh/id_rsa
chmod 644 /root/.ssh/id_rsa.pub
chmod 700 /root/.ssh
```

### Host Key Verification Failed

```bash
# First connection needs to accept host key
ssh -o StrictHostKeyChecking=no user@192.168.1.100

# Or add to ~/.ssh/config inside container
cat >> /root/.ssh/config <<EOF
Host *
    StrictHostKeyChecking accept-new
EOF
```

### Connection Timeout

- Check if target server's firewall allows SSH (port 22)
- Verify network connectivity: `ping 192.168.1.100`
- Check if SSH service is running on target server

## Security Best Practices

1. **Use read-only volume mounts** for SSH keys when possible
2. **Never commit** SSH keys to git
3. **Use different keys** for different purposes
4. **Set proper permissions** (600 for private keys)
5. **Consider using SSH agent** forwarding for better security
