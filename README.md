# LLM Infrastructure

> **Production-grade infrastructure for running 70+ local LLM models with zero API costs**

A collection of battle-tested tools for deploying, managing, and monitoring local Large Language Models at scale. Built for developers who want the power of GPT-4 class models without the API bills or privacy concerns.

## 🎯 Why This Repository?

**Zero API Costs** - Run unlimited inference locally  
**Complete Privacy** - Your data never leaves your infrastructure  
**Production Ready** - Battle-tested in real deployments  
**Hardware Optimized** - Get maximum performance from your GPUs  
**Easy to Deploy** - Docker-first with simple configuration

## 📦 Components

### 🚀 [ollama-fleet-manager](./ollama-fleet-manager/)
**Manage 70+ models across multiple Ollama servers**

Unified Python interface for accessing Qwen, Llama, Granite, Mistral, and more. Automatically route requests to the right server based on model size and hardware.

```python
from fleet_manager import get_model

# Automatically routes to optimal server
llm = get_model("qwen2.5:32b", server="server_large")
response = llm.invoke("Explain quantum computing")
```

**Use Case**: Multi-server LLM deployments, hardware optimization

---

### 🌐 [litellm-local-gateway](./litellm-local-gateway/)
**Production API gateway for local LLMs**

OpenAI-compatible proxy that unifies Ollama, vLLM, and other local endpoints. Features load balancing, fallbacks, rate limiting, and Prometheus metrics.

```bash
# Single endpoint for all your local models
curl http://localhost:4000/v1/chat/completions \
  -d '{"model": "qwen2.5:7b", "messages": [...]}'
```

**Use Case**: Unified API for multiple LLM backends, production deployments

---

### 🐳 [ollama-production-docker](./ollama-production-docker/)
**Production-hardened Ollama Docker deployment**

Secure, monitored Docker setup with automatic restarts, health checks, and permission management. Includes monitoring scripts and best-practice configurations.

```bash
# Production-ready in one command
docker run --gpus all -v ollama:/root/.ollama \
  -p 11434:11434 --restart unless-stopped ollama/ollama
```

**Use Case**: Deploying Ollama in production environments

---

### 📊 [multi-server-monitoring-dashboard](./multi-server-monitoring-dashboard/)
**Real-time monitoring for distributed LLM infrastructure**

Streamlit dashboard showing GPU usage, model status, and system health across multiple servers. Monitor your entire LLM fleet from one interface.

**Monitors:**
- GPU utilization & memory
- Active models per server
- System resources (CPU, RAM, disk)
- Model response times

**Use Case**: Infrastructure monitoring, capacity planning

---

### ⚡ [vllm-gptq-marlin-optimization](./vllm-gptq-marlin-optimization/)
**2-3x faster inference with GPTQ-Marlin kernel**

Patch for vLLM enabling Marlin kernels for GPTQ-quantized models. Dramatically improves throughput for 4-bit quantized models on modern GPUs.

**Performance gains:**
- 2-3x faster token generation
- Same accuracy as standard GPTQ
- Works with Ampere/Ada GPUs (3090, 4090, A100)

**Use Case**: Maximizing inference speed for quantized models

---

### 🔒 [vpn-wireguard](./vpn-wireguard/)
**Secure VPN server for remote LLM infrastructure access**

Dockerized WireGuard VPN server with automatic client configuration, QR code generation, and easy client management. Connect securely to your LLM infrastructure from anywhere.

**Features:**
- Auto-detection of public IP
- One-command client creation
- QR codes for mobile devices
- Persistent configuration storage

**Use Case**: Secure remote access to LLM servers, multi-location deployments

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Your Application                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     │  🔒 Optional: WireGuard VPN
                     │     (Secure remote access)
                     │
            ┌────────▼─────────┐
            │  LiteLLM Gateway │  ← Unified API, load balancing
            │  (localhost:4000)│
            └────────┬─────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   ┌────▼───┐  ┌────▼───┐  ┌────▼───┐
   │Ollama  │  │Ollama  │  │ vLLM   │
   │Server 1│  │Server 2│  │Server 3│
   │Small   │  │Medium  │  │Large   │
   │Models  │  │Models  │  │Models  │
   └────────┘  └────────┘  └────────┘
        │            │            │
   ┌────▼────────────▼────────────▼────┐
   │  Multi-Server Monitoring Dashboard│
   │      (Real-time fleet view)       │
   └───────────────────────────────────┘
```

## 🚀 Quick Start

### Single Server Setup (Most Common)

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Pull some models
ollama pull qwen2.5:7b
ollama pull llama3.1:8b
ollama pull granite-code:20b

# 3. Use fleet manager
cd ollama-fleet-manager
pip install -r requirements.txt
python fleet_manager.py
```

### Production Multi-Server Setup

```bash
# Server 1 (Small models - 16GB VRAM)
cd ollama-production-docker
./docker-run.sh

# Server 2 (Medium models - 24GB VRAM)
cd ollama-production-docker
./docker-run.sh

# API Gateway (Any server)
cd litellm-local-gateway
docker-compose up -d

# Monitoring Dashboard (Any server)
cd multi-server-monitoring-dashboard
streamlit run app.py
```

## 💡 Use Cases

### 1. Development Environment
**Components**: ollama-fleet-manager  
**Setup Time**: 5 minutes  
**Hardware**: Single GPU (12GB+)

Perfect for local development and testing with multiple models.

### 2. Small Team Production
**Components**: ollama-production-docker + litellm-local-gateway  
**Setup Time**: 30 minutes  
**Hardware**: 1-2 GPUs (24GB+)

Reliable API endpoint for a small team with basic monitoring.

### 3. Enterprise Deployment
**Components**: All components  
**Setup Time**: 2-3 hours  
**Hardware**: 3+ GPUs across multiple servers

Full-scale deployment with load balancing, monitoring, and optimized inference.

## 🔧 Configuration

All components use environment variables for configuration:

```env
# Ollama servers
OLLAMA_SERVER_SMALL=http://192.168.1.10:11434
OLLAMA_SERVER_MEDIUM=http://192.168.1.11:11434
OLLAMA_SERVER_LARGE=http://192.168.1.12:11434

# LiteLLM gateway
LITELLM_PORT=4000
LITELLM_LOG_LEVEL=INFO

# Monitoring
MONITOR_REFRESH_INTERVAL=5
```

See individual component READMEs for detailed configuration options.

## 📊 Performance Benchmarks

**Single Server (RTX 4090 24GB)**
- Small models (3B-7B): 80-120 tokens/sec
- Medium models (14B-20B): 30-50 tokens/sec
- Large models (32B+): 15-25 tokens/sec (with quantization)

**Multi-Server Fleet (3x RTX 4090)**
- Concurrent requests: 50+ simultaneous users
- Total throughput: 200+ tokens/sec aggregate
- Uptime: 99.9% with gateway failover

## 🛠️ Troubleshooting

### Ollama not connecting
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
systemctl restart ollama  # Linux
brew services restart ollama  # macOS
```

### GPU not detected
```bash
# Check NVIDIA drivers
nvidia-smi

# For Docker
docker run --gpus all nvidia/cuda:12.0-base nvidia-smi
```

### Models running slow
1. Check quantization level (Q4_K_M recommended)
2. Verify GPU memory not full (`nvidia-smi`)
3. Consider vLLM with Marlin kernels for 4-bit models

## 🤝 Contributing

This is a personal portfolio showcasing production LLM infrastructure. However, suggestions and feedback are welcome:

1. Open an issue describing your use case
2. Share your deployment experience
3. Suggest optimizations or improvements

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

Built with:
- [Ollama](https://ollama.ai/) - The easiest way to run LLMs locally
- [LiteLLM](https://github.com/BerriAI/litellm) - Unified LLM API gateway
- [vLLM](https://github.com/vllm-project/vllm) - High-performance inference engine
- [FastChat](https://github.com/lm-sys/FastChat) - LLM serving infrastructure

## 🔗 Related Repositories

**LLM Components**: [llm-components](https://github.com/Hannune/LLM-Components) - Building blocks for LLM applications  
**LLM Applications**: [llm-applications](https://github.com/Hannune/LLM-Applications) - Full applications built with local LLMs

---

**Built for developers who want production-grade LLM infrastructure without the cloud bills** 🚀

Questions? Open an issue or check individual component READMEs for detailed documentation.
