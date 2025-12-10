#!/usr/bin/env python3
"""
Password Hash Generator for Streamlit Dashboard
Generates bcrypt hashes for secure password storage
"""

import bcrypt
import getpass
import sys

def generate_hash(password):
    """Generate bcrypt hash from password"""
    # Generate salt and hash
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_hash(password, hashed):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def main():
    print("=" * 70)
    print("  Streamlit Dashboard - Password Hash Generator")
    print("=" * 70)
    print()

    # Get password securely (won't show on screen)
    password1 = getpass.getpass("Enter password: ")

    if not password1:
        print("❌ Error: Password cannot be empty!")
        sys.exit(1)

    if len(password1) < 8:
        print("⚠️  Warning: Password is less than 8 characters. Consider using a stronger password.")

    password2 = getpass.getpass("Confirm password: ")

    if password1 != password2:
        print("❌ Error: Passwords do not match!")
        sys.exit(1)

    print()
    print("🔐 Generating secure hash...")
    hashed = generate_hash(password1)

    # Escape $ for .env file (Docker Compose requires $$)
    escaped_hash = hashed.replace('$', '$$')

    print()
    print("=" * 70)
    print("✅ Password hash generated successfully!")
    print("=" * 70)
    print()
    print("📋 Copy this line to your .env file:")
    print()
    print(f"DASHBOARD_PASSWORD_HASH={escaped_hash}")
    print()
    print("=" * 70)
    print()
    print("📝 Instructions:")
    print("1. Copy the line above (with $$ - this is correct!)")
    print("2. Add it to your .env file")
    print("3. Restart the dashboard: docker compose restart")
    print()
    print("💡 Note: The $$ is intentional - Docker Compose requires it")
    print()

    # Verify the hash works
    print("🔍 Verifying hash...")
    if verify_hash(password1, hashed):
        print("✅ Hash verification successful!")
    else:
        print("❌ Hash verification failed!")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
