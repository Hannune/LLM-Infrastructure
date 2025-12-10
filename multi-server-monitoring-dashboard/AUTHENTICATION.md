# Authentication Setup Guide

## 🔐 Password Protection for Your Dashboard

The dashboard now supports password authentication using secure bcrypt hashing.

---

## Quick Setup (3 Steps)

### Step 1: Generate Password Hash (2 minutes)

```bash
# Run the hash generator
python3 generate_password_hash.py
```

**You'll be prompted:**
```
Enter password: [type your password - won't show on screen]
Confirm password: [type again]
```

**Output:**
```
✅ Password hash generated successfully!

📋 Copy this hash to your .env file:

DASHBOARD_PASSWORD_HASH=$2b$12$abcd1234...

📝 Instructions:
1. Copy the line above
2. Add it to your .env file
3. Restart the dashboard: docker compose restart
```

### Step 2: Create .env File

```bash
# Copy example file
cp .env.example .env

# Edit and add your password hash
nano .env
```

**Paste the hash from Step 1:**
```env
DASHBOARD_PASSWORD_HASH=$2b$12$YOUR_GENERATED_HASH_HERE
```

Save and exit (Ctrl+X, Y, Enter)

### Step 3: Restart Dashboard

```bash
docker compose restart
```

**Done!** The dashboard now requires a password to access.

---

## How It Works

### 🔒 Security Features

1. **Bcrypt Hashing**
   - Industry-standard password hashing
   - Salted and slow (12 rounds)
   - Protects against brute-force attacks

2. **No Plain-Text Storage**
   - Password is NEVER stored
   - Only the hash is stored in .env
   - Even with .env access, password cannot be recovered

3. **Session-Based**
   - Login once per browser session
   - No cookies or persistent storage
   - Automatic logout when closing browser

### 🔓 Login Flow

```
User opens dashboard
     ↓
Shows login page
     ↓
User enters password
     ↓
Password hashed and compared
     ↓
If match: Show dashboard
If no match: Show error
```

---

## Usage

### Normal Operation

1. Open http://localhost:8501
2. Enter password
3. Click "Login"
4. Dashboard appears

### Disabling Authentication

To disable password protection (NOT recommended for production):

**Method 1: Remove from .env**
```bash
# Edit .env
nano .env

# Delete or comment out the line:
# DASHBOARD_PASSWORD_HASH=...
```

**Method 2: Don't create .env file**
```bash
# If .env doesn't exist, auth is disabled
rm .env
```

Restart: `docker compose restart`

---

## Advanced Configuration

### Multiple Users

Currently supports single password. For multiple users:

**Option 1: Shared Password**
- Give all users the same password
- Simple but less secure

**Option 2: Multiple Hashes (Future)**
- Not implemented yet
- Would require code changes

### Changing Password

1. Generate new hash:
   ```bash
   python3 generate_password_hash.py
   ```

2. Update .env with new hash

3. Restart:
   ```bash
   docker compose restart
   ```

All users will need the new password.

### Forgot Password?

Since you have access to the server:

1. Generate new hash:
   ```bash
   python3 generate_password_hash.py
   ```

2. Replace hash in .env

3. Restart dashboard

---

## Troubleshooting

### Can't Login - "Authentication error"

**Cause:** Hash format is incorrect

**Solution:**
```bash
# Regenerate hash properly
python3 generate_password_hash.py

# Copy the ENTIRE line including $2b$12$...
# Paste into .env

# Restart
docker compose restart
```

### Password Prompt Not Showing

**Cause:** No password hash in environment

**Check:**
```bash
# View .env file
cat .env | grep DASHBOARD_PASSWORD_HASH

# Should show:
# DASHBOARD_PASSWORD_HASH=$2b$12$...
```

**If empty:**
```bash
python3 generate_password_hash.py
# Add hash to .env
docker compose restart
```

### "Module 'bcrypt' not found"

**Cause:** bcrypt not installed

**Solution:**
```bash
# Stop container
docker compose down

# Rebuild (bcrypt is in requirements.txt)
docker compose up -d --build
```

### Logged Out Unexpectedly

**Cause:** Session state cleared (browser refresh, Streamlit rerun)

**Solution:** Log in again. This is normal behavior for security.

---

## Security Best Practices

### ✅ DO:

1. **Use strong passwords**
   - At least 12 characters
   - Mix of letters, numbers, symbols
   - Example: `MyD@shb0ard#2024`

2. **Keep .env file secure**
   - Never commit to git (.gitignore includes it)
   - Restrict file permissions: `chmod 600 .env`
   - Store backups securely

3. **Use HTTPS in production**
   - Password transmitted over HTTPS only
   - Use reverse proxy (nginx, traefik)
   - Get SSL certificate (Let's Encrypt)

4. **Change default passwords**
   - Never use example passwords
   - Regenerate hash for production

5. **Limit network access**
   - Use firewall rules
   - VPN for remote access
   - Don't expose to internet directly

### ❌ DON'T:

1. **Don't use weak passwords**
   - "password", "123456", "admin"
   - Dictionary words
   - Personal information

2. **Don't share passwords insecurely**
   - Email, Slack, SMS
   - Use password manager instead

3. **Don't disable auth in production**
   - Always use passwords for production
   - Even on private networks

4. **Don't commit .env to git**
   - Already in .gitignore
   - Double-check before pushing

---

## Testing Authentication

### Test 1: Verify Hash Generation

```bash
python3 generate_password_hash.py
# Should generate hash successfully
```

### Test 2: Verify Login Works

1. Start dashboard: `docker compose up -d`
2. Open http://localhost:8501
3. Should see login page
4. Enter password
5. Should access dashboard

### Test 3: Verify Wrong Password Fails

1. Open dashboard
2. Enter wrong password
3. Should see "Invalid password" error

### Test 4: Verify No Auth When Disabled

1. Remove password from .env
2. Restart: `docker compose restart`
3. Open dashboard
4. Should go directly to dashboard (no login)

---

## Production Deployment Checklist

Before deploying to production:

- [ ] Strong password set (12+ characters)
- [ ] Password hash in .env file
- [ ] .env file not in git
- [ ] HTTPS/SSL configured
- [ ] Firewall rules configured
- [ ] Dashboard not exposed to public internet
- [ ] Backup of .env file created
- [ ] Password shared securely with team
- [ ] Tested login works
- [ ] Tested wrong password fails

---

## Example: Full Setup from Scratch

```bash
# 1. Navigate to project
cd /home/tetae/Projects/claude-code/multi-server-monitoring-dashboard

# 2. Generate password hash
python3 generate_password_hash.py
# Enter password: MySecureP@ss123
# Confirm password: MySecureP@ss123
# Copy the output hash

# 3. Create .env file
cp .env.example .env
nano .env

# 4. Add hash to .env
# DASHBOARD_PASSWORD_HASH=$2b$12$abcd1234...
# Save and exit

# 5. Start dashboard
docker compose up -d

# 6. Test it
# Open http://localhost:8501
# Enter: MySecureP@ss123
# Should work!
```

---

## Password Manager Integration

Recommended password managers:
- **1Password** - Team sharing
- **Bitwarden** - Open source, self-hosted option
- **LastPass** - Popular choice
- **KeePass** - Offline, encrypted

Store:
- Password (the actual password)
- Dashboard URL (http://localhost:8501)
- .env file location (if team needs it)

---

## FAQ

**Q: Can I use the same password for all my team?**
A: Yes, but use a strong password and share via password manager.

**Q: How do I add multiple passwords?**
A: Not supported yet. Everyone uses the same password currently.

**Q: Is the password stored in the Docker container?**
A: No. Only the hash is passed via environment variable.

**Q: What if someone gets my .env file?**
A: They have the hash, but cannot reverse it to get your password. They could replace it with their own hash though, so keep .env secure.

**Q: Can I integrate with LDAP/Active Directory/OAuth?**
A: Not built-in. Would require custom development.

**Q: Is this secure enough for production?**
A: Yes, with these conditions:
   - HTTPS enabled
   - Strong password
   - Network access restricted
   - Behind VPN or firewall

**Q: Do I need to enter password every time?**
A: Only once per browser session. Closing browser = need to login again.

---

## Additional Security Layers

For maximum security, combine password auth with:

1. **VPN Access** - Only accessible via VPN
2. **IP Whitelist** - Firewall rules limiting IPs
3. **HTTPS** - SSL/TLS encryption
4. **Reverse Proxy Auth** - nginx basic auth on top
5. **Network Segmentation** - Separate management network

---

## Support

- Authentication issues: Check this guide's Troubleshooting section
- Generate hash: `python3 generate_password_hash.py`
- Verify bcrypt installed: `docker compose logs | grep bcrypt`
