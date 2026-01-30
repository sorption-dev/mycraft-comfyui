#!/bin/bash

echo "[Mycraft UI] Starting installation..."

cd ComfyUI/custom_nodes

git clone https://github.com/sorption-dev/mycraft-comfyui.git

cd mycraft-comfyui

sh install-dependencies.sh

# ---

# Optional:

sh install-sdxl.sh
sh install-loras-sdxl.sh

# sh install-flux1d.sh
# sh install-loras-flux1d.sh

# ---

echo "[Mycraft UI] Installed!"
