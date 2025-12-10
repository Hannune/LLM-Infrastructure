# Easy Setup Guide - Simplified Workflow

## What's New? ✨

The dashboard now **automatically generates and exports SSH keys** for you!

After running `docker compose up -d`, you'll find the public key in:
```
./ssh-keys/id_rsa.pub
```

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Configure Your Servers (2 minutes)

```bash
cd /home/tetae/Projects/claude-code/multi-server-monitoring-dashboard

# Create config
cp servers.example.yml servers.yml
nano servers.yml
```

**Edit with your server details:**
```yaml
servers:
  - name: "GPU Server 1"
    host: "192.168.1.100"          # ← Your server IP
    username: "myuser"              # ← Your SSH username
    port: 22
    key_file: "/root/.ssh/id_rsa"  # ← Keep as-is
```

Save and exit (Ctrl+X, Y, Enter)

---

### Step 2: Start Dashboard (30 seconds)

```bash
docker compose up -d
```

**What happens automatically:**
1. ✅ Container starts
2. ✅ SSH key pair is generated
3. ✅ Public key is exported to `./ssh-keys/id_rsa.pub`
4. ✅ Dashboard starts at http://localhost:8501

**Check the logs to see your public key:**
```bash
docker compose logs dashboard
```

You'll see:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 YOUR SSH PUBLIC KEY (also saved to ./ssh-keys/id_rsa.pub):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQ... root@abc123
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Step 3: Add Public Key to Your Servers (2 minutes per server)

**Option A: Automatic (Easiest)**

From your host machine (NOT inside container):

```bash
# Copy the public key to each server
ssh-copy-id -i ./ssh-keys/id_rsa.pub myuser@192.168.1.100
```

Enter your password when prompted (only once).

**Option B: Manual**

1. View your public key:
   ```bash
   cat ./ssh-keys/id_rsa.pub
   ```

2. Copy the output (entire line starting with `ssh-rsa`)

3. On each server, run:
   ```bash
   ssh myuser@192.168.1.100
   mkdir -p ~/.ssh
   echo "PASTE_YOUR_PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
   chmod 600 ~/.ssh/authorized_keys
   exit
   ```

**Option C: Inside Container (Original Method)**

```bash
docker compose exec dashboard bash
ssh-copy-id -i /root/.ssh/id_rsa.pub myuser@192.168.1.100
exit
```

---

### Step 4: Access Dashboard ✅

Open browser: **http://localhost:8501**

You should see:
- 🟢 **Online** status for all servers
- Live metrics in tabs

---

## 📁 What Gets Created

After running `docker compose up -d`:

```
multi-server-monitoring-dashboard/
├── ssh-keys/              ← NEW! Auto-created
│   └── id_rsa.pub        ← Your public key (safe to share)
├── servers.yml           ← Your config
├── docker-compose.yml
└── ...
```

---

## 🔄 Workflow Comparison

### Before (Old Way):
```
1. docker compose up -d
2. docker compose exec dashboard bash
3. ssh-keygen ...
4. ssh-copy-id ...
5. exit
6. Access dashboard
```

### Now (New Way):
```
1. docker compose up -d
2. cat ./ssh-keys/id_rsa.pub  ← Public key is RIGHT HERE!
3. ssh-copy-id -i ./ssh-keys/id_rsa.pub user@server
4. Access dashboard
```

**Saved steps: No need to enter container for key generation!**

---

## 📋 Copy-Paste Public Key

Need to copy your public key?

```bash
# Display public key
cat ./ssh-keys/id_rsa.pub

# Copy to clipboard (Linux with xclip)
cat ./ssh-keys/id_rsa.pub | xclip -selection clipboard

# Copy to clipboard (Mac)
cat ./ssh-keys/id_rsa.pub | pbcopy
```

Then paste it into your server's `~/.ssh/authorized_keys`

---

## 🔒 Security Note

**Public key (`id_rsa.pub`):**
- ✅ Safe to share
- ✅ Safe to store in `./ssh-keys/` directory
- ✅ Exported automatically

**Private key (`id_rsa`):**
- ❌ NEVER exposed outside container
- ❌ Stays in Docker volume
- ✅ Secure and isolated

---

## 🐛 Troubleshooting

### Can't find `./ssh-keys/id_rsa.pub`?

```bash
# Check if container is running
docker compose ps

# View logs
docker compose logs dashboard

# Manually export the key
docker compose exec dashboard cp /root/.ssh/id_rsa.pub /ssh-keys-export/id_rsa.pub
```

### Need to regenerate keys?

```bash
# Stop container
docker compose down

# Remove volume (WARNING: This deletes the old key!)
docker volume rm multi-server-monitoring-dashboard_ssh-keys

# Start again (will create new key)
docker compose up -d
```

### Want to use existing SSH keys?

Edit `docker-compose.yml`:
```yaml
volumes:
  # Comment this line:
  # - ssh-keys:/root/.ssh

  # Uncomment this line:
  - ~/.ssh:/root/.ssh:ro
```

---

## 💡 Pro Tips

### 1. View Public Key Anytime

```bash
# From host
cat ./ssh-keys/id_rsa.pub

# From container
docker compose exec dashboard cat /root/.ssh/id_rsa.pub
```

### 2. Add Key to Multiple Servers

```bash
# Create a list of servers
SERVERS="user1@192.168.1.100 user2@192.168.1.101 user3@192.168.1.102"

# Copy key to all servers
for server in $SERVERS; do
    ssh-copy-id -i ./ssh-keys/id_rsa.pub $server
done
```

### 3. Backup Public Key

```bash
cp ./ssh-keys/id_rsa.pub ~/my-monitoring-key-backup.pub
```

---

## ✅ Quick Checklist

After setup:

- [ ] `docker compose ps` shows "Up"
- [ ] `./ssh-keys/id_rsa.pub` exists
- [ ] Public key added to all servers in `servers.yml`
- [ ] Can SSH to servers without password
- [ ] Dashboard shows 🟢 Online status
- [ ] Can see metrics in all tabs

**All checked? You're done!** 🎉

---

## 📞 Need Help?

- **Detailed setup:** [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)
- **Quick start:** [QUICKSTART.md](QUICKSTART.md)
- **SSH issues:** [SSH_SETUP.md](SSH_SETUP.md)
