# Setup Checklist - Complete Guide

Follow this checklist to get your monitoring dashboard running.

---

## ✅ BEFORE Running Docker Compose

### Step 1: Verify Prerequisites (2 minutes)

```bash
# Check if Docker is installed
docker --version
# Should show: Docker version 20.x or higher

# Check if Docker Compose is installed
docker compose version
# Should show: Docker Compose version v2.x or higher

# Check if Docker is running
docker ps
# Should NOT show error
```

**If Docker is not installed:** Install Docker first
- Ubuntu: `sudo apt install docker.io docker-compose-plugin`
- Other: https://docs.docker.com/engine/install/

---

### Step 2: Navigate to Project Directory (10 seconds)

```bash
cd /home/tetae/Projects/claude-code/multi-server-monitoring-dashboard
```

---

### Step 3: Create servers.yml Configuration (2 minutes)

```bash
# Copy example file
cp servers.example.yml servers.yml

# Edit with your server details
nano servers.yml
```

**What to fill in:**

```yaml
servers:
  - name: "My GPU Server 1"        # ← Give it a friendly name
    host: "192.168.1.100"          # ← YOUR server's IP address
    username: "myusername"         # ← YOUR SSH username on that server
    port: 22                       # ← Usually 22 (default SSH port)
    key_file: "/root/.ssh/id_rsa"  # ← Keep this as-is (path inside container)

  - name: "My GPU Server 2"        # ← Add more servers if needed
    host: "192.168.1.101"          # ← Second server IP
    username: "myusername"         # ← Your username
    port: 22
    key_file: "/root/.ssh/id_rsa"
```

**Important:**
- Replace `192.168.1.100` with your actual server IP
- Replace `myusername` with your actual SSH username
- Keep `key_file: "/root/.ssh/id_rsa"` unchanged (this is the path INSIDE the Docker container)

Save and exit (Ctrl+X, then Y, then Enter)

---

### Step 4: Verify servers.yml is Valid (30 seconds)

```bash
# Check the file exists
ls -lh servers.yml

# View the content to make sure it looks correct
cat servers.yml
```

**Should look like:**
```
servers:
  - name: "..."
    host: "..."
    username: "..."
```

---

### Step 5: Test Network Connectivity (1 minute)

```bash
# Make sure you can reach your servers from this machine
ping -c 3 192.168.1.100  # Replace with your server IP

# Should show:
# 64 bytes from 192.168.1.100: icmp_seq=1 ttl=64 time=0.5 ms
```

**If ping fails:**
- Check the IP address is correct
- Check firewall isn't blocking
- Make sure server is powered on

---

### Step 6: Pre-flight Check Summary

Before proceeding, confirm:

- [ ] Docker is installed and running
- [ ] You're in the project directory
- [ ] `servers.yml` exists and has your server IPs
- [ ] You can ping your servers
- [ ] You know your SSH username for each server
- [ ] You have SSH access credentials (password for first-time setup)

**All checked?** → Ready to run docker compose!

---

## 🚀 RUNNING Docker Compose

### Start the Dashboard

```bash
docker compose up -d
```

**Expected output:**
```
[+] Running 2/2
 ✔ Network multi-server-monitoring-dashboard_monitoring    Created
 ✔ Container server-monitor-dashboard                      Started
```

### Verify Container is Running

```bash
docker compose ps
```

**Should show:**
```
NAME                          STATUS    PORTS
server-monitor-dashboard      Up        0.0.0.0:8501->8501/tcp
```

**Status should be "Up"** (not "Restarting" or "Exited")

### Check Logs (if needed)

```bash
docker compose logs -f
```

**Should see:**
```
dashboard  | You can now view your Streamlit app in your browser.
dashboard  | Network URL: http://0.0.0.0:8501
```

Press Ctrl+C to exit logs.

---

## ✅ AFTER Docker Compose is Running

### Step 7: Setup SSH Keys (5 minutes - FIRST TIME ONLY)

This is the most important step! Without SSH keys, the dashboard can't connect to your servers.

#### 7.1: Enter the Container

```bash
docker compose exec dashboard bash
```

**You should see:**
```
root@abc123:/app#
```

You're now INSIDE the Docker container.

#### 7.2: Generate SSH Key Pair

```bash
ssh-keygen -t rsa -b 4096 -f /root/.ssh/id_rsa -N ""
```

**What this does:**
- Creates a new SSH key pair
- `-N ""` means no passphrase (for automation)

**You should see:**
```
Generating public/private rsa key pair.
Your identification has been saved in /root/.ssh/id_rsa
Your public key has been saved in /root/.ssh/id_rsa.pub
```

#### 7.3: Copy SSH Key to Each Server

For EACH server in your servers.yml, run:

```bash
ssh-copy-id -i /root/.ssh/id_rsa.pub myusername@192.168.1.100
```

**Replace:**
- `myusername` with your SSH username
- `192.168.1.100` with your server IP

**First time, you'll see:**
```
The authenticity of host '192.168.1.100' can't be established.
ECDSA key fingerprint is SHA256:...
Are you sure you want to continue connecting (yes/no)?
```

Type: **yes** and press Enter

**Then you'll be asked for password:**
```
myusername@192.168.1.100's password:
```

Enter your SSH password (ONE TIME ONLY)

**Success looks like:**
```
Number of key(s) added: 1

Now try logging into the machine with:
  ssh 'myusername@192.168.1.100'
```

**Repeat for all servers in your servers.yml**

#### 7.4: Test SSH Connection (IMPORTANT!)

For each server, test that you can connect WITHOUT password:

```bash
ssh myusername@192.168.1.100
```

**If successful:**
- You'll connect immediately (NO password prompt)
- You'll see your server's command prompt

Type `exit` to return to the container.

**If it asks for password:**
- ❌ SSH key setup failed
- Go back to step 7.3 and try again

#### 7.5: Exit Container

```bash
exit
```

You're back on your host machine.

---

### Step 8: Access the Dashboard (30 seconds)

Open your web browser and go to:

```
http://localhost:8501
```

**What you should see:**

1. **Title:** "🖥️ Multi-Server Monitoring Dashboard"
2. **Status cards** at the top showing each server
3. **Green status (🟢 Online)** if everything is working
4. **Red status (🔴 Offline)** if there's a problem

---

### Step 9: Verify It's Working

#### Check Server Status
Look at the status cards at the top:
- 🟢 **Online** = Good! SSH connection working
- 🔴 **Offline** = Problem with SSH connection

#### Click Through the Tabs
For each server, check the tabs:
- **💽 Disk Usage** - Should show disk partitions
- **🧠 Memory** - Should show RAM usage
- **🎮 GPU (NVIDIA)** - Should show GPU info (if nvidia-smi installed)
- **🐳 Docker** - Should show containers (if Docker accessible)
- **📈 System Info** - Should show uptime and CPU

#### Test Auto-Refresh
1. In the sidebar, check "Auto Refresh"
2. Set interval to 60 seconds
3. You should see:
   - "⏱️ Last refresh: 0s ago"
   - "⏳ Next refresh in: 60s"
   - Countdown timer

---

## 🐛 Troubleshooting After Setup

### Problem: Dashboard shows "🔴 Offline" or "Connection Error"

**Solution:**
```bash
# Enter container
docker compose exec dashboard bash

# Try SSH manually
ssh -v myusername@192.168.1.100

# If it asks for password, SSH keys aren't set up correctly
# Go back to Step 7.3
```

---

### Problem: Can't access http://localhost:8501

**Check 1: Is container running?**
```bash
docker compose ps
# Should show "Up", not "Exited"
```

**Check 2: Are logs showing errors?**
```bash
docker compose logs dashboard
# Look for error messages
```

**Check 3: Is port 8501 already used?**
```bash
sudo lsof -i :8501
# If something else is using port 8501, stop it or change port
```

---

### Problem: "Configuration file servers.yml not found"

**Solution:**
```bash
# Make sure servers.yml exists
ls -lh servers.yml

# Make sure it's in the right directory
pwd
# Should show: /home/tetae/Projects/claude-code/multi-server-monitoring-dashboard

# Restart container
docker compose restart
```

---

### Problem: GPU metrics not showing

**On your target server (not in Docker):**
```bash
# Check if nvidia-smi is installed
nvidia-smi

# If not found, install NVIDIA drivers first
```

---

### Problem: Docker containers not showing

**On your target server:**
```bash
# Check if your user can access Docker
docker ps

# If permission denied, add user to docker group:
sudo usermod -aG docker myusername
# Then logout and login again
```

---

## 🎉 Success Checklist

After setup, you should have:

- [ ] Container running (`docker compose ps` shows "Up")
- [ ] Dashboard accessible at http://localhost:8501
- [ ] All servers showing 🟢 Online status
- [ ] Can see disk usage in "Disk Usage" tab
- [ ] Can see memory in "Memory" tab
- [ ] SSH keys work (no password prompts)
- [ ] Auto-refresh works (timer counts down)

**All checked? You're done!** 🎉

---

## 📝 Daily Usage

### Start Dashboard
```bash
cd /home/tetae/Projects/claude-code/multi-server-monitoring-dashboard
docker compose up -d
```

### Stop Dashboard
```bash
docker compose down
```

### View Logs
```bash
docker compose logs -f
```

### Restart Dashboard
```bash
docker compose restart
```

### Update Dashboard (after code changes)
```bash
docker compose up -d --build
```

---

## 🔐 Security Notes

### SSH Keys Location

Your SSH keys are stored in a Docker volume:
```bash
# Backup SSH keys (RECOMMENDED!)
docker compose exec dashboard tar czf - /root/.ssh > ssh-keys-backup-$(date +%Y%m%d).tar.gz

# Store this file safely!
```

### Adding New Servers Later

1. Edit servers.yml:
   ```bash
   nano servers.yml
   # Add new server block
   ```

2. Restart dashboard:
   ```bash
   docker compose restart
   ```

3. Setup SSH for new server:
   ```bash
   docker compose exec dashboard bash
   ssh-copy-id -i /root/.ssh/id_rsa.pub user@new-server-ip
   exit
   ```

---

## 📞 Need Help?

- **Setup issues:** See [DEPLOYMENT.md](DEPLOYMENT.md)
- **SSH problems:** See [SSH_SETUP.md](SSH_SETUP.md)
- **Docker issues:** See [DOCKER_SETUP.md](DOCKER_SETUP.md)
- **Quick reference:** See [QUICKSTART.md](QUICKSTART.md)
