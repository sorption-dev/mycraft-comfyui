#!/bin/bash

echo "[Mycraft UI Preview] Installing SDXL lora models..."

mkdir -p "../../models/loras/sdxl/style"
mkdir -p "../../models/loras/sdxl/details"

curl -L -o "../../models/loras/sdxl/style/Araminta_Soft_Focus_3D-000013.safetensors" "https://civitai.com/api/download/models/574502?type=Model&format=SafeTensor"

curl -L -o "../../models/loras/sdxl/style/Little_Tinies.safetensors" "https://civitai.com/api/download/models/556905"

curl -L -o "../../models/loras/sdxl/details/add-detail-xl.safetensors" "https://civitai.com/api/download/models/135867"

curl -L -o "../../models/loras/sdxl/style/SDXL_MSPaint_Portrait.safetensors" "https://civitai.com/api/download/models/205793"

echo "[Mycraft UI Preview] SDXL lora models downloaded."