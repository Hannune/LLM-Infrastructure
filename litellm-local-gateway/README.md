# LiteLLM Local Gateway

**OpenAI-compatible API gateway for local LLM deployments (Ollama, vLLM, etc.)**

Provides a unified OpenAI-compatible API interface to all your local LLMs, enabling load balancing, fallbacks, and monitoring without vendor lock-in or API costs.

## Features

- **100% Local LLM Support** - Works with Ollama, vLLM, and other local deployments
- **OpenAI-Compatible API** - Drop-in replacement for OpenAI API clients
- **Load Balancing** - Route requests across multiple model servers
- **Prometheus Metrics** - Monitor performance and usage
- **Web Dashboard** - Manage models via UI at `http://localhost:4000`
- **No API Costs** - Everything runs locally

## Quick Start

1. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your keys
```

2. **Edit config.yaml to add your local models:**
```yaml
model_list:
  - model_name: qwen2.5:7b
    litellm_params:
      model: ollama/qwen2.5:7b
      api_base: http://localhost:11434
```

3. **Start the gateway:**
```bash
./run.sh
```

4. **Access the dashboard:**
```
http://localhost:4000
```

## Configuration

### Adding Ollama Models

Edit `config.yaml`:
```yaml
model_list:
  - model_name: llama3.1:8b
    litellm_params:
      model: ollama/llama3.1:8b
      api_base: http://localhost:11434
```

### Adding vLLM Models

```yaml
model_list:
  - model_name: gpt-oss-20b
    litellm_params:
      model: openai/gpt-oss-20b
      api_base: http://localhost:13080/v1
      api_key: EMPTY
```

### Multiple Ollama Servers

Run different models on different ports:
```yaml
model_list:
  - model_name: small-model
    litellm_params:
      model: ollama/qwen2.5:3b
      api_base: http://localhost:11434
  
  - model_name: large-model
    litellm_params:
      model: ollama/llama3.1:70b
      api_base: http://localhost:11435
```

## Usage

### OpenAI Python Client

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-master-key",
    base_url="http://localhost:4000"
)

response = client.chat.completions.create(
    model="qwen2.5:7b",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

### cURL

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer your-master-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5:7b",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Monitoring

### Prometheus Metrics
Access metrics at:
```
http://localhost:9090
```

Available metrics:
- Request latency
- Token usage
- Model availability
- Error rates

### Dashboard
Web UI available at:
```
http://localhost:4000
```

## Deployment

### Production Checklist

1. Set strong `LITELLM_MASTER_KEY` in `.env`
2. Set `LITELLM_SALT_KEY` (cannot change after models are added)
3. Enable master_key in `config.yaml`:
```yaml
litellm_settings:
  master_key: "your-secret-master-key"
```

4. Use reverse proxy (nginx/caddy) for HTTPS
5. Set up Prometheus alerts for monitoring

### Stop Gateway
```bash
docker compose down
```

### Update Gateway
```bash
docker compose pull
docker compose up -d
```

## Architecture

```
┌─────────────────┐
│   LiteLLM       │
│   Gateway       │ :4000
│ (OpenAI API)    │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    │         │          │          │
┌───▼───┐ ┌──▼──┐  ┌────▼────┐ ┌───▼────┐
│Ollama │ │vLLM │  │Ollama   │ │Postgres│
│:11434 │ │:8000│  │:11435   │ │  DB    │
└───────┘ └─────┘  └─────────┘ └────────┘
   LOCAL    LOCAL      LOCAL      LOCAL
```

## Requirements

- Docker & Docker Compose
- Local LLM server (Ollama/vLLM) running
- 2GB RAM (for gateway only)

## Troubleshooting

### Cannot connect to Ollama
- Ensure Ollama is running: `ollama serve`
- Check Ollama port in `config.yaml` matches your setup
- Test: `curl http://localhost:11434/api/tags`

### Models not showing in UI
- Verify `config.yaml` syntax
- Check Docker logs: `docker compose logs litellm`
- Restart: `docker compose restart`

### Database errors
- Remove volumes: `docker compose down -v`
- Restart: `./run.sh`

## License

MIT
