#!/bin/bash

echo "[Mycraft UI Preview] Installing Flux 1 Dev lora models..."

curl -L -o "../../models/loras/flux/details/Flux_Ultimator.safetensors" "https://civitai.com/api/download/models/885950"

curl -L -o "../../models/loras/flux/details/UltraRealPhoto.safetensors" "https://civitai.com/api/download/models/1026423"

curl -L -o "../../models/loras/flux/style/araminta_k_softpasty_diffusion_flux.safetensors" "https://civitai.com/api/download/models/767186"

curl -L -o "../../models/loras/flux/style/Comic book V2.safetensors" "https://civitai.com/api/download/models/954701"

curl -L -o "../../models/loras/flux/style/v3ctora.safetensors" "https://civitai.com/api/download/models/768020"

echo "[Mycraft UI Preview] Flux 1 Dev lora models downloaded."
