#!/bin/bash

# vLLM GPTQ-Marlin Optimization Patch Installer
# This script patches vLLM v0.8.5 to improve GPTQ-Marlin quantization support

set -e

VLLM_VERSION="0.8.5"
PATCH_FILE="gptq_marlin.py"
TARGET_PATH="vllm/model_executor/layers/quantization/gptq_marlin.py"

echo "Checking vLLM installation..."

# Check if vLLM is installed
if ! python -c "import vllm" 2>/dev/null; then
    echo "Error: vLLM is not installed"
    echo "Install vLLM first: pip install vllm==${VLLM_VERSION}"
    exit 1
fi

# Get vLLM version
INSTALLED_VERSION=$(python -c "import vllm; print(vllm.__version__)")
echo "Installed vLLM version: ${INSTALLED_VERSION}"

if [ "${INSTALLED_VERSION}" != "${VLLM_VERSION}" ]; then
    echo "Warning: Patch is designed for vLLM ${VLLM_VERSION}, you have ${INSTALLED_VERSION}"
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Find vLLM installation path
VLLM_PATH=$(python -c "import vllm, os; print(os.path.dirname(vllm.__file__))")
FULL_TARGET_PATH="${VLLM_PATH}/model_executor/layers/quantization/gptq_marlin.py"

echo "vLLM path: ${VLLM_PATH}"
echo "Target file: ${FULL_TARGET_PATH}"

# Backup original file
if [ -f "${FULL_TARGET_PATH}" ]; then
    BACKUP_PATH="${FULL_TARGET_PATH}.backup"
    echo "Backing up original file to ${BACKUP_PATH}"
    cp "${FULL_TARGET_PATH}" "${BACKUP_PATH}"
else
    echo "Warning: Target file does not exist"
fi

# Apply patch
echo "Applying patch..."
cp "${PATCH_FILE}" "${FULL_TARGET_PATH}"

echo "Patch applied successfully!"
echo ""
echo "To restore original file:"
echo "  cp ${BACKUP_PATH} ${FULL_TARGET_PATH}"
