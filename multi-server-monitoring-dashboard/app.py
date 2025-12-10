import streamlit as st
import paramiko
import json
import pandas as pd
from datetime import datetime
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import yaml
import os
import bcrypt

class ServerMonitor:
    def __init__(self, config_file='servers.yml'):
        self.config_file = config_file
        self.servers = self.load_servers()

    def load_servers(self):
        try:
            with open(self.config_file, 'r') as file:
                config = yaml.safe_load(file)
                return config.get('servers', [])
        except FileNotFoundError:
            st.error(f"Configuration file {self.config_file} not found!")
            return []
        except Exception as e:
            st.error(f"Error loading configuration: {str(e)}")
            return []

    def ssh_execute(self, server, command):
        """Execute command on remote server via SSH"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Expand user path for SSH key
            key_file = server.get('key_file')
            if key_file:
                key_file = os.path.expanduser(key_file)

            # Connect with key-based authentication
            ssh.connect(
                hostname=server['host'],
                port=server.get('port', 22),
                username=server['username'],
                key_filename=key_file,
                timeout=10
            )
            
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            
            ssh.close()
            
            if error and 'command not found' not in error.lower():
                return f"Error: {error}"
            
            return output
            
        except Exception as e:
            return f"Connection Error: {str(e)}"

    def get_disk_usage(self, server):
        """Get disk usage information"""
        output = self.ssh_execute(server, "df -h")
        return output

    def get_memory_usage(self, server):
        """Get memory usage information"""
        output = self.ssh_execute(server, "free -h")
        return output

    def get_nvidia_info(self, server):
        """Get NVIDIA GPU information"""
        output = self.ssh_execute(server, "nvidia-smi")
        return output

    def get_docker_containers(self, server):
        """Get Docker container information"""
        output = self.ssh_execute(server, "docker ps")
        return output

    def get_system_uptime(self, server):
        """Get system uptime"""
        output = self.ssh_execute(server, "uptime")
        return output

    def get_cpu_info(self, server):
        """Get CPU usage information"""
        output = self.ssh_execute(server, "top -bn1 | grep 'Cpu(s)' | head -1")
        return output

    def collect_all_data(self, server):
        """Collect all monitoring data for a server"""
        data = {
            'server': server['name'],
            'host': server['host'],
            'status': 'Unknown',
            'uptime': '',
            'cpu': '',
            'disk': '',
            'memory': '',
            'nvidia': '',
            'docker': '',
            'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            # Test connection first
            uptime = self.get_system_uptime(server)
            if "Connection Error" in uptime:
                data['status'] = '🔴 Offline'
                data['uptime'] = uptime
                return data
            else:
                data['status'] = '🟢 Online'
                data['uptime'] = uptime.strip()

            # Collect other data
            data['cpu'] = self.get_cpu_info(server)
            data['disk'] = self.get_disk_usage(server)
            data['memory'] = self.get_memory_usage(server)
            data['nvidia'] = self.get_nvidia_info(server)
            data['docker'] = self.get_docker_containers(server)
            
        except Exception as e:
            data['status'] = f'🔴 Error: {str(e)}'
        
        return data

def check_password():
    """Check if password authentication is required and validate"""
    # Get password hash from environment variable
    password_hash = os.environ.get('DASHBOARD_PASSWORD_HASH', '')

    # If no password hash is set, authentication is disabled
    if not password_hash:
        return True

    # Initialize session state for authentication
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    # If already authenticated, return True
    if st.session_state.authenticated:
        return True

    # Show login form
    st.title("🔐 Dashboard Login")
    st.markdown("---")

    with st.form("login_form"):
        password = st.text_input("Password", type="password", key="password_input")
        submit = st.form_submit_button("Login")

        if submit:
            if password:
                # Verify password
                try:
                    if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
                        st.session_state.authenticated = True
                        # Rerun immediately - loading will happen on dashboard page
                        st.rerun()
                    else:
                        st.error("❌ Invalid password")
                except Exception as e:
                    st.error(f"❌ Authentication error: {str(e)}")
            else:
                st.warning("⚠️ Please enter a password")

    st.markdown("---")
    st.info("💡 To disable authentication, remove DASHBOARD_PASSWORD_HASH from environment")

    return False

def main():
    st.set_page_config(
        page_title="Server Monitoring Dashboard",
        page_icon="🖥️",
        layout="wide"
    )

    # Check authentication first
    if not check_password():
        return

    st.title("🖥️ Multi-Server Monitoring Dashboard")
    st.markdown("---")

    # Initialize monitor
    monitor = ServerMonitor()

    if not monitor.servers:
        st.warning("No servers configured. Please check your servers.yml file.")
        return

    # Initialize session state for timing
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time.time()

    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Controls")
        auto_refresh = st.checkbox("Auto Refresh", value=False)
        refresh_interval = st.slider("Refresh Interval (seconds)", 30, 300, 60)

        if st.button("🔄 Refresh Now"):
            st.session_state.last_refresh = time.time()
            st.rerun()

        # Show last refresh time
        time_since_refresh = int(time.time() - st.session_state.last_refresh)
        st.info(f"⏱️ Last refresh: {time_since_refresh}s ago")

        if auto_refresh:
            st.success(f"✅ Auto-refresh enabled ({refresh_interval}s)")

    # Smart auto-refresh using st.empty() and time-based trigger
    # This avoids blocking the UI with time.sleep()
    if auto_refresh:
        time_since_refresh = time.time() - st.session_state.last_refresh
        if time_since_refresh >= refresh_interval:
            st.session_state.last_refresh = time.time()
            st.rerun()
        else:
            # Use st.empty() with JavaScript to trigger refresh
            # This creates a non-blocking timer
            time_to_next_refresh = int(refresh_interval - time_since_refresh)
            st.sidebar.markdown(f"⏳ Next refresh in: **{time_to_next_refresh}s**")

            # JavaScript-based auto-refresh (non-blocking)
            refresh_script = f"""
                <script>
                    setTimeout(function() {{
                        window.parent.location.reload();
                    }}, {time_to_next_refresh * 1000});
                </script>
            """
            st.components.v1.html(refresh_script, height=0)
    
    # Collect data from all servers concurrently
    with st.spinner("Collecting data from servers..."):
        all_data = []
        
        with ThreadPoolExecutor(max_workers=len(monitor.servers)) as executor:
            future_to_server = {
                executor.submit(monitor.collect_all_data, server): server 
                for server in monitor.servers
            }
            
            for future in as_completed(future_to_server):
                data = future.result()
                all_data.append(data)
    
    # Server status overview
    st.header("📊 Server Status Overview")

    # Use grid layout - max 4 columns per row for better readability
    servers_per_row = min(4, len(all_data))

    # Create rows of server cards
    for row_start in range(0, len(all_data), servers_per_row):
        row_data = all_data[row_start:row_start + servers_per_row]
        cols = st.columns(len(row_data))

        for i, data in enumerate(row_data):
            with cols[i]:
                status_color = "green" if "🟢" in data['status'] else "red"
                st.markdown(
                    f"""
                    <div style="border: 2px solid {status_color}; border-radius: 10px; padding: 10px; margin: 5px;">
                        <h4>{data['server']}</h4>
                        <p><strong>Status:</strong> {data['status']}</p>
                        <p><strong>Host:</strong> {data['host']}</p>
                        <p><strong>Updated:</strong> {data['last_updated']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    # Detailed information for each server
    for data in all_data:
        st.header(f"🖥️ {data['server']} ({data['host']})")
        
        if "🔴" in data['status']:
            st.error(f"Server is offline or unreachable: {data['status']}")
            continue
        
        # Create tabs for different metrics
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "💽 Disk Usage", 
            "🧠 Memory", 
            "🎮 GPU (NVIDIA)", 
            "🐳 Docker", 
            "📈 System Info"
        ])
        
        with tab1:
            st.subheader("Disk Usage")
            if data['disk']:
                st.code(data['disk'], language='bash')
            else:
                st.info("No disk information available")
        
        with tab2:
            st.subheader("Memory Usage")
            if data['memory']:
                st.code(data['memory'], language='bash')
            else:
                st.info("No memory information available")
        
        with tab3:
            st.subheader("NVIDIA GPU Information")
            if data['nvidia'] and "command not found" not in data['nvidia']:
                st.code(data['nvidia'], language='bash')
            else:
                st.info("NVIDIA drivers not installed or nvidia-smi not available")
        
        with tab4:
            st.subheader("Docker Containers")
            if data['docker'] and "Cannot connect" not in data['docker']:
                st.code(data['docker'], language='bash')
            else:
                st.info("Docker not running or not accessible")
        
        with tab5:
            st.subheader("System Information")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Uptime:**")
                st.code(data['uptime'])
            with col2:
                st.write("**CPU Usage:**")
                st.code(data['cpu'])
        
        st.markdown("---")

if __name__ == "__main__":
    main()
