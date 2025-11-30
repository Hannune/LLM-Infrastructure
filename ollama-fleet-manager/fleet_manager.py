"""Ollama Fleet Manager - Manage 70+ Local LLM Models Across Multiple Servers

This module provides a unified interface to access multiple Ollama servers,
each hosting different model families (Qwen, Llama, Granite, Mistral, etc.)
optimized for different hardware configurations.
"""

import os
from typing import Dict, List, Tuple
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

# Load environment variables
load_dotenv()

# Server configuration
SERVERS = {
    "server_small": os.getenv("OLLAMA_SERVER_SMALL", "http://localhost:11434"),
    "server_medium": os.getenv("OLLAMA_SERVER_MEDIUM", "http://localhost:11435"),
    "server_large": os.getenv("OLLAMA_SERVER_LARGE", "http://localhost:11436"),
}

# Available models by family
MODELS = {
    "qwen": [
        "qwen2.5:0.5b", "qwen2.5:1.5b", "qwen2.5:3b", "qwen2.5:7b",
        "qwen2.5:14b", "qwen2.5:32b", "qwen2.5-coder:7b",
    ],
    "llama": [
        "llama3.2:1b", "llama3.2:3b", "llama3.1:8b", "llama3.1:70b",
    ],
    "granite": [
        "granite3-moe:1b", "granite3.1:2b", "granite3.1:8b",
        "granite-code:20b", "granite-code:34b",
    ],
    "deepseek": [
        "deepseek-r1:1.5b", "deepseek-r1:7b", "deepseek-r1:14b", "deepseek-r1:32b",
    ],
    "mistral": [
        "mistral:7b", "mistral-nemo:12b", "mistral-small:22b",
    ],
    "gemma": [
        "gemma2:2b", "gemma2:9b", "gemma2:27b",
    ],
    "phi": [
        "phi3:3b", "phi3.5:3.8b", "phi4:14b",
    ],
}

# Model recommendations
RECOMMENDATIONS = {
    ("general", "small"): ("qwen2.5:3b", "server_small"),
    ("general", "medium"): ("qwen2.5:7b", "server_medium"),
    ("general", "large"): ("qwen2.5:32b", "server_large"),
    ("code", "small"): ("qwen2.5-coder:7b", "server_small"),
    ("code", "medium"): ("granite-code:20b", "server_medium"),
    ("code", "large"): ("granite-code:34b", "server_large"),
    ("reasoning", "small"): ("deepseek-r1:7b", "server_small"),
    ("reasoning", "medium"): ("deepseek-r1:14b", "server_medium"),
    ("reasoning", "large"): ("deepseek-r1:32b", "server_large"),
    ("fast", "small"): ("qwen2.5:0.5b", "server_small"),
    ("fast", "medium"): ("llama3.2:3b", "server_small"),
    ("fast", "large"): ("qwen2.5:7b", "server_medium"),
}


def get_model(
    model_name: str,
    server: str = "server_small",
    temperature: float = 0.0,
    format: str = ""
) -> ChatOllama:
    """
    Get a configured LangChain ChatOllama instance.

    Args:
        model_name: Name of the Ollama model (e.g., "llama3.1:8b")
        server: Server key from config (server_small, server_medium, server_large)
        temperature: Sampling temperature (0.0 = deterministic)
        format: Output format (e.g., "json")

    Returns:
        Configured ChatOllama instance
    """
    base_url = SERVERS.get(server, SERVERS["server_small"])
    return ChatOllama(
        model=model_name,
        temperature=temperature,
        format=format,
        base_url=base_url
    )


def get_recommended_model(
    use_case: str = "general",
    size_preference: str = "medium"
) -> Tuple[str, str]:
    """
    Get recommended model based on use case and size preference.

    Args:
        use_case: "general", "code", "reasoning", "fast"
        size_preference: "small", "medium", "large"

    Returns:
        Tuple of (model_name, server_key)
    """
    return RECOMMENDATIONS.get(
        (use_case, size_preference),
        ("qwen2.5:7b", "server_medium")
    )


def main():
    """Example usage."""
    # Get a specific model
    llm = get_model("qwen2.5:7b", server="server_medium")
    print(f"Loaded model: qwen2.5:7b")
    
    # Get recommendation
    model_name, server = get_recommended_model(use_case="code", size_preference="medium")
    print(f"Recommended for coding: {model_name} on {server}")
    
    # Test inference
    try:
        response = llm.invoke("Hello! Respond with just 'Hi'")
        print(f"Response: {response.content}")
    except Exception as e:
        print(f"Could not connect to Ollama server: {e}")


if __name__ == "__main__":
    main()
