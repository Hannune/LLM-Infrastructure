#!/usr/bin/env python3
"""Quick test to measure actual collection time"""

import time
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import from app.py
from app import ServerMonitor

def main():
    print("🔍 Quick Performance Test\n")

    monitor = ServerMonitor()

    if not monitor.servers:
        print("❌ No servers configured in servers.yml")
        return

    print(f"📋 Found {len(monitor.servers)} servers\n")

    # Test with timing
    start = time.time()

    print("⏱️  Starting parallel data collection...")
    all_data = []

    # Limit concurrent connections to avoid Paramiko race conditions
    max_parallel = min(6, len(monitor.servers))
    print(f"  → Using {max_parallel} parallel workers\n")

    with ThreadPoolExecutor(max_workers=max_parallel) as executor:
        future_to_server = {
            executor.submit(monitor.collect_all_data, server): server
            for server in monitor.servers
        }

        completed = 0
        for future in as_completed(future_to_server):
            data = future.result()
            all_data.append(data)
            completed += 1
            elapsed = time.time() - start
            print(f"  ✓ Server {completed}/{len(monitor.servers)} completed ({elapsed:.1f}s elapsed)")

    total_time = time.time() - start

    print(f"\n{'='*70}")
    print(f"⏱️  TOTAL TIME: {total_time:.2f} seconds")
    print(f"{'='*70}\n")

    # Show results
    print("📊 Results:")
    for data in all_data:
        status_icon = "🟢" if "🟢" in data['status'] else "🔴"
        print(f"  {status_icon} {data['server']:20s} ({data['host']:15s}) - {data['status']}")

    print(f"\n🎯 Analysis:")
    if total_time > 30:
        print(f"  ❌ VERY SLOW: {total_time:.1f}s is too long!")
        print(f"     Expected: 3-5 seconds for {len(monitor.servers)} servers")
        print(f"     Something is wrong - run debug_performance.py for details")
    elif total_time > 10:
        print(f"  ⚠️  SLOW: {total_time:.1f}s is slower than expected")
        print(f"     Expected: 3-5 seconds for {len(monitor.servers)} servers")
    elif total_time > 5:
        print(f"  ✅ ACCEPTABLE: {total_time:.1f}s")
        print(f"     Could be faster, but not too bad")
    else:
        print(f"  ✅ FAST: {total_time:.1f}s - excellent!")

if __name__ == "__main__":
    main()
