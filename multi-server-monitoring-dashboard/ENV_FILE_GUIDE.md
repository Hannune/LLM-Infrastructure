# .env File Configuration Guide

## 🔧 Common Issue: Dollar Sign ($) in Password Hash

### The Problem

Bcrypt hashes contain `$` symbols like this:
```
$2b$12$kjJECATFvThvjMOf/dIxpel3n4y3qkbMRakU3bZIIQGG5dVsjHP2u
```

Docker Compose interprets `$` as variable substitution, causing errors:
```
WARN[0000] The "kjJECATFvThvjMOf" variable is not set.
```

### The Solution

**Escape dollar signs by doubling them:**

❌ **Wrong:**
```env
DASHBOARD_PASSWORD_HASH=$2b$12$kjJECATFvThvjMOf...
```

✅ **Correct:**
```env
DASHBOARD_PASSWORD_HASH=$$2b$$12$$kjJECATFvThvjMOf...
```

### Quick Fix

If you already have a hash, use this command:

```bash
# Your original hash
HASH='$2b$12$kjJECATFvThvjMOf/dIxpel3n4y3qkbMRakU3bZIIQGG5dVsjHP2u'

# Escape it for .env
echo "DASHBOARD_PASSWORD_HASH=${HASH//\$/\$\$}"

# Output:
# DASHBOARD_PASSWORD_HASH=$$2b$$12$$kjJECATFvThvjMOf/dIxpel3n4y3qkbMRakU3bZIIQGG5dVsjHP2u
```

Or manually double each `$`:
```
$2b$12$... → $$2b$$12$$...
```

---

## 🎯 Your Specific Hash

Your hash:
```
$2b$12$kjJECATFvThvjMOf/dIxpel3n4y3qkbMRakU3bZIIQGG5dVsjHP2u
```

For `.env` file, use:
```env
DASHBOARD_PASSWORD_HASH=$$2b$$12$$kjJECATFvThvjMOf/dIxpel3n4y3qkbMRakU3bZIIQGG5dVsjHP2u
```

---

## 📝 Complete .env File Example

```env
# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Auto-refresh settings
DEFAULT_AUTO_REFRESH=false
DEFAULT_REFRESH_INTERVAL=60

# Dashboard Authentication
# NOTE: Use $$ instead of $ for Docker Compose
DASHBOARD_PASSWORD_HASH=$$2b$$12$$kjJECATFvThvjMOf/dIxpel3n4y3qkbMRakU3bZIIQGG5dVsjHP2u
```

---

## 🔄 Step-by-Step Fix

### 1. Edit .env File

```bash
nano .env
```

### 2. Update the Hash Line

Change from:
```env
DASHBOARD_PASSWORD_HASH=$2b$12$kjJECATFvThvjMOf/dIxpel3n4y3qkbMRakU3bZIIQGG5dVsjHP2u
```

To:
```env
DASHBOARD_PASSWORD_HASH=$$2b$$12$$kjJECATFvThvjMOf/dIxpel3n4y3qkbMRakU3bZIIQGG5dVsjHP2u
```

### 3. Save and Exit

Ctrl+X, Y, Enter

### 4. Restart Dashboard

```bash
docker compose down
docker compose up -d
```

### 5. Verify - No Warnings

```bash
docker compose up
```

Should NOT show any warnings about undefined variables.

### 6. Test Login

Open http://localhost:8501 and login with your password.

---

## 🔍 Why This Happens

### Docker Compose Variable Substitution

In `.env` files, Docker Compose treats `$` as variable substitution:

```env
# This tries to use variable $2b, $12, $kjJECATFvThvjMOf
VARIABLE=$2b$12$kjJECATFvThvjMOf...

# Docker sees:
# - Variable $2b (not defined)
# - Variable $12 (not defined)
# - Variable $kjJECATFvThvjMOf (not defined)
```

### Escaping with $$

Double `$$` tells Docker Compose: "This is a literal dollar sign, not a variable":

```env
# This is treated as literal string "$$2b$$12$$..."
VARIABLE=$$2b$$12$$kjJECATFvThvjMOf...

# In the container, it becomes: $2b$12$kjJECATFvThvjMOf...
```

### Inside the Container

When your app reads the environment variable, it receives the correctly formatted hash:
```python
os.environ.get('DASHBOARD_PASSWORD_HASH')
# Returns: "$2b$12$kjJECATFvThvjMOf..."
```

---

## 🧪 Testing

### Test 1: Check Environment Variable

```bash
# Check what the container sees
docker compose exec dashboard printenv DASHBOARD_PASSWORD_HASH
```

**Should output:**
```
$2b$12$kjJECATFvThvjMOf/dIxpel3n4y3qkbMRakU3bZIIQGG5dVsjHP2u
```

(Single `$`, not double!)

### Test 2: No Warnings on Startup

```bash
docker compose up
```

**Should NOT show:**
```
WARN[0000] The "kjJECATFvThvjMOf" variable is not set.
```

### Test 3: Login Works

1. Open http://localhost:8501
2. Enter your password
3. Should successfully login

---

## 🔄 Alternative: Use Quotes (Doesn't Work in .env)

**Note:** This does NOT work in `.env` files:

❌ **Does not work:**
```env
DASHBOARD_PASSWORD_HASH='$2b$12$kjJECATFvThvjMOf...'
DASHBOARD_PASSWORD_HASH="$2b$12$kjJECATFvThvjMOf..."
```

Quotes are treated as part of the value in `.env` files.

**Only this works:**
```env
DASHBOARD_PASSWORD_HASH=$$2b$$12$$kjJECATFvThvjMOf...
```

---

## 🛠️ Alternative: Direct Environment Variable

Instead of `.env` file, you can set it directly in `docker-compose.yml`:

```yaml
services:
  dashboard:
    environment:
      # Use single $ here (quotes protect it)
      - DASHBOARD_PASSWORD_HASH=$2b$12$kjJECATFvThvjMOf/dIxpel3n4y3qkbMRakU3bZIIQGG5dVsjHP2u
```

But this is **NOT recommended** because:
- ❌ Hash visible in docker-compose.yml
- ❌ Gets committed to git if not careful
- ✅ Better to keep secrets in .env file

---

## 📚 Summary

| Method | Syntax | Works? | Recommended? |
|--------|--------|--------|--------------|
| Double $$ in .env | `$$2b$$12$$...` | ✅ Yes | ✅ Yes (best) |
| Single $ in .env | `$2b$12$...` | ❌ No (variable substitution) | ❌ No |
| Quotes in .env | `'$2b$12$...'` | ❌ No (quotes included) | ❌ No |
| Direct in compose | `$2b$12$...` | ✅ Yes | ⚠️ Not recommended |

**Use: `$$2b$$12$$...` in your .env file!**

---

## 🆘 Still Not Working?

### Debug Steps:

1. **Check .env file exists:**
   ```bash
   ls -lh .env
   ```

2. **View contents:**
   ```bash
   cat .env | grep DASHBOARD_PASSWORD_HASH
   ```

3. **Verify escaping:**
   ```bash
   # Should show $$2b$$12$$...
   grep DASHBOARD_PASSWORD_HASH .env
   ```

4. **Test in container:**
   ```bash
   docker compose exec dashboard bash
   echo $DASHBOARD_PASSWORD_HASH
   # Should show: $2b$12$... (single $)
   exit
   ```

5. **Check logs:**
   ```bash
   docker compose logs dashboard | grep -i password
   ```

---

## 🎉 Success Checklist

- [ ] .env file exists
- [ ] Hash has `$$` (double dollar signs)
- [ ] No warnings when running `docker compose up`
- [ ] `docker compose exec dashboard printenv DASHBOARD_PASSWORD_HASH` shows single `$`
- [ ] Login page appears
- [ ] Can login with password

All checked? You're good! 🎉

---

## 💡 Pro Tip

The updated `generate_password_hash.py` script now automatically outputs the hash with `$$` escaping. Always use the script's output directly!
