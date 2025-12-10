# Changelog

All notable changes to this project will be documented in this file.

## [2.3.0] - 2025-12-10

### Added
- Grid layout for server status cards (4 servers per row) for better UI with 10+ servers
- Optimized parallel worker count (6 concurrent connections)
- Staggered SSH connection timing to prevent race conditions

### Changed
- **Major SSH connection stability improvements** - Fixed random connection failures with Paramiko
- Reduced connection timeouts (10s → 8s) for faster data collection
- Reduced random delay (0.05-0.15s → 0.01-0.05s) for better performance
- Simplified entrypoint.sh - removed verbose SSH key messages
- Docker Compose now uses host SSH keys (`~/.ssh`) instead of generating new ones
- Made .env file optional in docker-compose.yml

### Fixed
- Random SSH connection failures due to Paramiko race conditions
- Inconsistent server connection status across refreshes
- Channel management issues causing "No existing session" errors

### Performance
- Data collection time improved from 14-15s to 6-8s for 11 servers
- All servers now connect reliably instead of random failures

## [2.2.0] - 2025-12-09

### Added
- Password authentication with bcrypt hashing
- Secure login page with password protection
- `generate_password_hash.py` utility for creating password hashes
- Optional authentication (can be disabled by not setting DASHBOARD_PASSWORD_HASH)
- Documentation for authentication setup (AUTHENTICATION.md, AUTH_QUICKSTART.md)

### Changed
- Updated requirements.txt to include bcrypt>=4.0.0
- Added .env file support for password hash storage
- Docker Compose env_file configuration for environment variables

## [2.1.0] - 2025-12-08

### Added
- Automatic SSH key generation in Docker container
- SSH public key export to host `./ssh-keys/` directory
- Detailed setup instructions displayed on container startup

### Changed
- entrypoint.sh now generates SSH keys automatically if not present
- Improved first-time setup experience

## [2.0.0] - 2025-12-07

### Added
- Docker Compose support for easy deployment
- Dockerfile for containerized deployment
- Docker volume for SSH key persistence
- Comprehensive documentation suite:
  - DEPLOYMENT.md - Complete deployment guide
  - DOCKER_SETUP.md - Docker-specific instructions
  - SETUP_CHECKLIST.md - Step-by-step checklist
  - EASY_SETUP.md - Quick start guide
  - SSH_SETUP.md - SSH key setup guide
- Non-blocking auto-refresh with JavaScript timer
- SSH key path expansion support (`~/.ssh/`)
- Grid layout for server cards
- Resource limits in docker-compose.yml

### Changed
- Auto-refresh now uses JavaScript setTimeout instead of blocking time.sleep()
- Fixed UI responsiveness during auto-refresh
- Improved error handling for SSH connections
- Better status indicators (🟢/🔴)

### Fixed
- Auto-refresh blocking UI issue
- SSH key path not expanding ~ to home directory
- Performance issues with concurrent SSH connections

### Performance
- Single SSH connection per server (instead of 6)
- Parallel data collection using ThreadPoolExecutor
- Optimized connection timeouts

## [1.0.0] - Initial Release

### Added
- Basic multi-server monitoring dashboard
- SSH-based data collection
- System metrics (CPU, memory, disk, uptime)
- NVIDIA GPU monitoring
- Docker container monitoring
- Streamlit web interface
- Manual refresh functionality
- servers.yml configuration file
