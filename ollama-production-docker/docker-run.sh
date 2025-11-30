#!/bin/bash

# Load environment variables
source .env

docker run -d --gpus all \
-v ${OLLAMA_DATA_PATH}:/root/.ollama \
--name ${CONTAINER_NAME} \
-p ${HOST_PORT}:11434 \
-e OLLAMA_NUM_PARALLEL=${OLLAMA_NUM_PARALLEL} \
-e OLLAMA_CONTEXT_LENGTH=${OLLAMA_CONTEXT_LENGTH} \
-e OLLAMA_KEEP_ALIVE=${OLLAMA_KEEP_ALIVE} \
ollama/ollama:${OLLAMA_VERSION}

echo "Ollama server started as ${CONTAINER_NAME} on port ${HOST_PORT}"
