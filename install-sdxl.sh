#!/bin/bash

echo "[Mycraft UI] Installing SDXL model files..."

curl -L -o "../../models/checkpoints/sd_xl_base_1.0.safetensors" "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors"

echo "[Mycraft UI] SDXL model files downloaded."
