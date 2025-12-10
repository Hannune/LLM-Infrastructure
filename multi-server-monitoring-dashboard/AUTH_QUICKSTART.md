# Authentication Quick Start

## 🔐 Add Password Protection in 3 Steps

### Step 1: Generate Hash (30 seconds)

```bash
python3 generate_password_hash.py
```

Enter your password when prompted. Copy the output line.

### Step 2: Configure (30 seconds)

```bash
# Create .env file
cp .env.example .env

# Edit and paste the hash
nano .env
```

Paste: `DASHBOARD_PASSWORD_HASH=$2b$12$...`

### Step 3: Apply (10 seconds)

```bash
docker compose restart
```

**Done!** Your dashboard now requires a password.

---

## Testing

1. Open http://localhost:8501
2. Should see login page
3. Enter your password
4. Access dashboard

---

## Disable Authentication

To remove password protection:

```bash
# Remove or comment out in .env
nano .env
# Delete: DASHBOARD_PASSWORD_HASH=...

# Restart
docker compose restart
```

---

## Full Documentation

See [AUTHENTICATION.md](AUTHENTICATION.md) for:
- Detailed setup instructions
- Security best practices
- Troubleshooting guide
- Production deployment checklist

---

## Example Hashes (For Testing Only - DO NOT USE IN PRODUCTION)

```env
# Password: "demo123"
DASHBOARD_PASSWORD_HASH=$2b$12$KIXxLJGopLm4Ne3TZ4vxMuqPZN9QfVWGhBwHkYqz8IFUm7XH/yQdO

# Password: "test456"
DASHBOARD_PASSWORD_HASH=$2b$12$fVYNP3kG1qL9xJm8N5CvReSdKjH6wP2tYqM9ZlBvXcA4RnTgWuHfa
```

**⚠️ WARNING:** These are example hashes. Generate your own for production!

---

## Security Notes

✅ **Safe:**
- Hash stored in .env (never plain password)
- bcrypt with 12 rounds (industry standard)
- Session-based (logout on browser close)

❌ **Important:**
- Use strong passwords (12+ characters)
- Never commit .env to git
- Enable HTTPS for production
- Restrict network access

---

## Quick Commands

```bash
# Generate new hash
python3 generate_password_hash.py

# View current hash
cat .env | grep DASHBOARD_PASSWORD_HASH

# Test authentication is working
curl -I http://localhost:8501  # Should redirect to login

# Disable auth temporarily
docker compose restart -e DASHBOARD_PASSWORD_HASH=

# Re-enable auth
docker compose restart  # Loads from .env
```

---

**Need help?** See [AUTHENTICATION.md](AUTHENTICATION.md)
