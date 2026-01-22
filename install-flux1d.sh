#!/bin/bash

echo "[Mycraft UI] Installing FLUX.1-dev model files..."

curl -L -o "../../models/vae/ae.safetensors" "https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/ae.safetensors"

curl -L -o "../../models/clip/clip_l.safetensors" "https://huggingface.co/camenduru/FLUX.1-dev/resolve/main/clip_l.safetensors"

curl -L -o "../../models/text_encoders/t5xxl_fp16.safetensors" "https://huggingface.co/camenduru/FLUX.1-dev/resolve/main/t5xxl_fp16.safetensors"

curl -L -o "../../models/text_encoders/t5xxl_fp8_e4m3fn.safetensors" "https://huggingface.co/camenduru/FLUX.1-dev/resolve/main/t5xxl_fp8_e4m3fn.safetensors"

curl -L -o "../../models/diffusion_models/flux1-dev.safetensors" "https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/flux1-dev.safetensors"

echo "[Mycraft UI] FLUX.1-dev model files downloaded."