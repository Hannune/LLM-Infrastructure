#!/usr/bin/env python3
"""
Performance Debugging Script
Tests SSH connection speed to each server
"""

import paramiko
import time
import yaml
import os
from datetime import datetime

def load_servers():
    """Load servers from config"""
    try:
        with open('servers.yml', 'r') as file:
            config = yaml.safe_load(file)
            return config.get('servers', [])
    except Exception as e:
        print(f"Error loading servers.yml: {e}")
        return []

def test_server_connection(server):
    """Test connection speed to a single server"""
    print(f"\n{'='*70}")
    print(f"Testing: {server['name']} ({server['host']})")
    print(f"{'='*70}")

    results = {}

    # Test 1: Connection time
    start = time.time()
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        key_file = server.get('key_file')
        if key_file:
            key_file = os.path.expanduser(key_file)

        ssh.connect(
            hostname=server['host'],
            port=server.get('port', 22),
            username=server['username'],
            key_filename=key_file,
            timeout=10
        )

        connect_time = time.time() - start
        results['connect_time'] = connect_time
        print(f"✅ Connection established: {connect_time:.2f}s")

        # Test 2: Command execution time
        commands = {
            'uptime': 'uptime',
            'cpu': "top -bn1 | grep 'Cpu(s)' | head -1",
            'disk': 'df -h',
            'memory': 'free -h',
            'nvidia': 'nvidia-smi',
            'docker': 'docker ps'
        }

        total_cmd_time = 0
        for cmd_name, command in commands.items():
            cmd_start = time.time()
            try:
                stdin, stdout, stderr = ssh.exec_command(command, timeout=5)
                output = stdout.read().decode('utf-8')
                cmd_time = time.time() - cmd_start
                total_cmd_time += cmd_time
                print(f"  ├─ {cmd_name:10s}: {cmd_time:.2f}s")
            except Exception as e:
                cmd_time = time.time() - cmd_start
                print(f"  ├─ {cmd_name:10s}: {cmd_time:.2f}s (Error: {e})")

        results['cmd_time'] = total_cmd_time

        ssh.close()
        close_time = time.time() - start
        results['total_time'] = close_time

        print(f"\n📊 Summary:")
        print(f"  Connect: {connect_time:.2f}s")
        print(f"  Commands: {total_cmd_time:.2f}s")
        print(f"  Total: {close_time:.2f}s")

        return results

    except Exception as e:
        error_time = time.time() - start
        print(f"❌ Connection failed: {error_time:.2f}s")
        print(f"   Error: {e}")
        return {'error': str(e), 'total_time': error_time}

def main():
    print(f"\n{'#'*70}")
    print(f"# Performance Debugging Tool")
    print(f"# Testing SSH connection speed to all servers")
    print(f"{'#'*70}")

    servers = load_servers()

    if not servers:
        print("\n❌ No servers found in servers.yml")
        return

    print(f"\n📋 Found {len(servers)} servers")

    total_start = time.time()
    all_results = []

    for server in servers:
        results = test_server_connection(server)
        results['server'] = server['name']
        results['host'] = server['host']
        all_results.append(results)

    total_time = time.time() - total_start

    # Summary
    print(f"\n{'#'*70}")
    print(f"# OVERALL SUMMARY")
    print(f"{'#'*70}")
    print(f"\nTotal servers: {len(servers)}")
    print(f"Total time (sequential): {total_time:.2f}s")
    print(f"Average per server: {total_time/len(servers):.2f}s")

    # Slowest servers
    print(f"\n🐌 Slowest servers:")
    sorted_results = sorted(
        [r for r in all_results if 'total_time' in r],
        key=lambda x: x['total_time'],
        reverse=True
    )[:5]

    for i, result in enumerate(sorted_results, 1):
        print(f"  {i}. {result['server']:20s} ({result['host']:15s}): {result['total_time']:.2f}s")

    # Failed connections
    failed = [r for r in all_results if 'error' in r]
    if failed:
        print(f"\n❌ Failed connections: {len(failed)}")
        for result in failed:
            print(f"  - {result['server']} ({result['host']}): {result['error']}")

    # Expected parallel time
    if sorted_results:
        expected_parallel = sorted_results[0]['total_time']
        print(f"\n⚡ Expected time with parallel execution: {expected_parallel:.2f}s")
        print(f"   (Time taken by slowest server)")

    # Diagnosis
    print(f"\n🔍 DIAGNOSIS:")
    avg_time = sum(r['total_time'] for r in all_results if 'total_time' in r) / len([r for r in all_results if 'total_time' in r])

    if avg_time > 10:
        print(f"  ⚠️  VERY SLOW: Average {avg_time:.1f}s per server")
        print(f"     Possible causes:")
        print(f"     - Network latency (slow network)")
        print(f"     - SSH key issues (password prompt timeout)")
        print(f"     - Slow servers (high CPU/load)")
        print(f"     - Firewall delays")
    elif avg_time > 5:
        print(f"  ⚠️  SLOW: Average {avg_time:.1f}s per server")
        print(f"     Possible causes:")
        print(f"     - Network latency")
        print(f"     - Some slow commands (nvidia-smi, docker)")
    elif avg_time > 2:
        print(f"  ✅ NORMAL: Average {avg_time:.1f}s per server")
        print(f"     Performance is acceptable")
    else:
        print(f"  ✅ FAST: Average {avg_time:.1f}s per server")
        print(f"     Performance is excellent!")

    print(f"\n{'#'*70}\n")

if __name__ == "__main__":
    main()
