# Ollama Production Docker

**Production-ready Docker deployment for Ollama with GPU support and automatic recovery**

Run Ollama in Docker with optimized configuration, persistent storage, and automatic GPU error recovery monitoring.

## Features

- **GPU Support** - Full NVIDIA GPU acceleration
- **Persistent Storage** - Models and data survive container restarts
- **Auto-Recovery** - Monitors and restarts on NVML errors
- **High Context** - Supports up to 65K context length
- **Keep-Alive** - Models stay in VRAM indefinitely
- **100% Local** - No API costs, complete control

## Quick Start

1. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your paths
```

2. **Start Ollama server:**
```bash
./docker-run.sh
```

3. **Verify it's running:**
```bash
docker logs ollama-server
curl http://localhost:11434/api/tags
```

4. **Start monitoring (optional):**
```bash
./monitor.sh
```

## Configuration

Edit `.env` file:

```bash
# Container settings
CONTAINER_NAME=ollama-server
HOST_PORT=11434

# Ollama version
OLLAMA_VERSION=0.11.6

# Data persistence (absolute path)
OLLAMA_DATA_PATH=/path/to/ollama/data

# Performance
OLLAMA_NUM_PARALLEL=1          # Number of parallel requests
OLLAMA_CONTEXT_LENGTH=65536    # Maximum context window
OLLAMA_KEEP_ALIVE=-1h          # Keep models loaded forever

# Auto-restart model (optional)
RESTART_MODEL=qwen2.5:7b
```

## Usage

### Pull and Run Models

```bash
# Pull a model
docker exec ollama-server ollama pull qwen2.5:7b

# Run with keep-alive
docker exec ollama-server ollama run qwen2.5:7b --keepalive -1h

# List installed models
docker exec ollama-server ollama list
```

### API Access

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen2.5:7b",
    base_url="http://localhost:11434"
)

response = llm.invoke("Hello!")
print(response.content)
```

### Multiple Instances

Run multiple Ollama servers on different ports:

```bash
# Server 1 (small models)
CONTAINER_NAME=ollama-small HOST_PORT=11434 ./docker-run.sh

# Server 2 (large models)
CONTAINER_NAME=ollama-large HOST_PORT=11435 ./docker-run.sh
```

## Monitoring

The `monitor.sh` script watches for NVML errors and automatically restarts the container.

### Start Monitoring
```bash
./monitor.sh
```

### Check Logs
```bash
tail -f monitor.log
```

### Stop Monitoring
```bash
# Find the monitor PID
ps aux | grep monitor

# Kill the process
kill <PID>
```

## Performance Tuning

### Context Length
Larger context = more VRAM usage:
```bash
OLLAMA_CONTEXT_LENGTH=8192    # 8K context (less VRAM)
OLLAMA_CONTEXT_LENGTH=65536   # 65K context (more VRAM)
```

### Parallel Requests
```bash
OLLAMA_NUM_PARALLEL=1   # Sequential (better for large models)
OLLAMA_NUM_PARALLEL=4   # Parallel (better for small models)
```

### Keep-Alive
```bash
OLLAMA_KEEP_ALIVE=5m    # Unload after 5 minutes
OLLAMA_KEEP_ALIVE=-1h   # Never unload (recommended)
```

## Management

### View Logs
```bash
docker logs -f ollama-server
```

### Restart Container
```bash
docker restart ollama-server
```

### Stop Container
```bash
docker stop ollama-server
```

### Remove Container
```bash
docker stop ollama-server
docker rm ollama-server
```

### Update Ollama
```bash
# Stop and remove old container
docker stop ollama-server
docker rm ollama-server

# Update version in .env
OLLAMA_VERSION=0.12.0

# Start new container
./docker-run.sh
```

## Troubleshooting

### Container won't start
```bash
# Check if port is in use
sudo lsof -i :11434

# Check Docker logs
docker logs ollama-server
```

### NVML errors
- Monitor script will auto-restart
- Check GPU drivers: `nvidia-smi`
- Ensure nvidia-docker is installed

### Models not persisting
- Verify `OLLAMA_DATA_PATH` exists
- Check permissions: `ls -la $OLLAMA_DATA_PATH`
- Models are stored in `/root/.ollama` inside container

### Out of memory
- Reduce `OLLAMA_CONTEXT_LENGTH`
- Set `OLLAMA_NUM_PARALLEL=1`
- Use smaller models (3B instead of 7B)

## Requirements

- Docker
- NVIDIA GPU
- nvidia-docker2 (nvidia-container-toolkit)
- NVIDIA drivers installed

## Architecture

```
┌─────────────────┐
│   Host System   │
│                 │
│  ┌───────────┐  │
│  │  Docker   │  │
│  │ Container │  │
│  │           │  │
│  │  Ollama   │  │:11434
│  │  Server   │  │
│  └─────┬─────┘  │
│        │        │
│    ┌───▼────┐   │
│    │ Models │   │ (Persistent Volume)
│    │  Data  │   │
│    └────────┘   │
└─────────────────┘
       │
       ▼
  NVIDIA GPU (Local)
```

## License

MIT
