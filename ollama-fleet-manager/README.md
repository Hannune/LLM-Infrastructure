# Ollama Fleet Manager

**Manage 70+ local LLM models across multiple Ollama servers with a unified Python interface.**

## What It Does

Provides a clean API to work with models distributed across multiple Ollama servers, each optimized for different model sizes and hardware configurations.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure servers
cp .env.example .env
# Edit .env with your Ollama server URLs

# Run example
python fleet_manager.py
```

## Usage

### Basic Usage

```python
from fleet_manager import get_model

# Get a model
llm = get_model("qwen2.5:7b", server="server_medium")

# Use with LangChain
response = llm.invoke("Explain quantum computing in one sentence")
print(response.content)
```

### Get Recommendations

```python
from fleet_manager import get_recommended_model, get_model

# Get recommended model for your use case
model_name, server = get_recommended_model(
    use_case="code",        # or "general", "reasoning", "fast"
    size_preference="medium" # or "small", "large"
)

llm = get_model(model_name, server=server)
```

### List Available Models

```python
from fleet_manager import MODELS

# View all available models by family
for family, models in MODELS.items():
    print(f"{family}: {models}")

# Output:
# qwen: ["qwen2.5:0.5b", "qwen2.5:7b", ...]
# llama: ["llama3.2:1b", "llama3.1:8b", ...]
# granite: ["granite3.1:2b", "granite-code:20b", ...]
```

## Configuration

Edit `.env` to configure your Ollama servers:

```env
# Single Server Setup (default)
OLLAMA_SERVER_SMALL=http://localhost:11434
OLLAMA_SERVER_MEDIUM=http://localhost:11434
OLLAMA_SERVER_LARGE=http://localhost:11434

# Multi-Server Setup
OLLAMA_SERVER_SMALL=http://192.168.1.10:11434   # Small models (<7B)
OLLAMA_SERVER_MEDIUM=http://192.168.1.11:11434  # Medium models (7-14B)
OLLAMA_SERVER_LARGE=http://192.168.1.12:11434   # Large models (>14B)
```

## Model Categories

- **Qwen** - Alibaba's models, excellent quality
- **Llama** - Meta's popular open models
- **Granite** - IBM's enterprise models, strong for code
- **DeepSeek** - Reasoning-optimized models
- **Mistral** - High-quality European models
- **Gemma** - Google's efficient models
- **Phi** - Microsoft's small but capable models

## Why This Approach?

- **Cost Efficient**: Run 70+ models on affordable hardware
- **Optimal Performance**: Match model size to available VRAM
- **Easy Switching**: Test different models without code changes
- **LangChain Compatible**: Drop-in replacement for any LangChain workflow

## Hardware Recommendations

### Single Server (24GB VRAM)
- Run all small/medium models on one GPU
- Set all URLs to `localhost:11434`

### Multi-Server (Optimal)
- **Server 1** (16GB): Small models (0.5B-3B)
- **Server 2** (24GB): Medium models (7B-14B)  
- **Server 3** (48GB+): Large models (20B-70B)

## Example: Multi-Server LLM App

```python
from fleet_manager import get_model

# Fast response for simple queries
fast_llm = get_model("qwen2.5:3b", server="server_small")

# Quality response for complex queries
quality_llm = get_model("qwen2.5:32b", server="server_large")

# Code generation
code_llm = get_model("granite-code:20b", server="server_medium")

# Route based on query complexity
def get_response(query, complexity="medium"):
    llm_map = {
        "fast": fast_llm,
        "medium": quality_llm,
        "complex": quality_llm,
    }
    return llm_map[complexity].invoke(query)
```

## Integration with LangChain

Works seamlessly with any LangChain feature:

```python
from fleet_manager import get_model
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

llm = get_model("qwen2.5:7b", server="server_medium")

# Create chain
prompt = ChatPromptTemplate.from_template("Summarize: {text}")
chain = prompt | llm | StrOutputParser()

# Use it
result = chain.invoke({"text": "Your long text here..."})
```

## Troubleshooting

### "Could not connect to Ollama server"
```bash
# Make sure Ollama is running
ollama serve

# Test connection
curl http://localhost:11434/api/tags
```

### "Model not found"
```bash
# Pull the model first
ollama pull qwen2.5:7b

# Verify it's available
ollama list
```

### Performance Issues
- Use smaller models on servers with less VRAM
- Enable GPU acceleration: `ollama run --gpu`
- Reduce context length for faster responses

## License

MIT License - Use freely in your projects!

---

**Part of the [Local LLM Infrastructure](../) toolkit**  
Works with 100% local models - no API costs, full privacy.
