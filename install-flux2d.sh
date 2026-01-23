#!/bin/bash

echo "[Mycraft UI] Installing FLUX.2-dev model files..."

curl -L -o "../../models/vae/flux2-vae.safetensors" "https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/vae/flux2-vae.safetensors"

curl -L -o "../../models/clip/qwen_3_8b_fp8mixed.safetensors" "https://huggingface.co/Comfy-Org/flux2-klein-9B/resolve/main/split_files/text_encoders/qwen_3_8b_fp8mixed.safetensors"

curl -L -o "../../models/diffusion_models/flux-2-klein-base-9b-fp8.safetensors" "https://huggingface.co/black-forest-labs/FLUX.2-klein-base-9b-fp8/resolve/main/flux-2-klein-base-9b-fp8.safetensors"

curl -L -o "../../models/diffusion_models/flux-2-klein-9b-fp8.safetensors" "https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-fp8/resolve/main/flux-2-klein-9b-fp8.safetensors"

echo "[Mycraft UI] FLUX.2-dev model files downloaded."