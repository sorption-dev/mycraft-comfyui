#!/bin/bash

cd ..
echo "[Mycraft UI] Installing dependencies..."
git clone https://github.com/rgthree/rgthree-comfy.git 2>&1 | grep -q "already exists" && echo "[Mycraft UI] rgthree-comfy already exists. Skipped." || true
git clone https://github.com/ltdrdata/ComfyUI-Impact-Pack.git 2>&1 | grep -q "already exists" && echo "[Mycraft UI] ComfyUI-Impact-Pack already exists. Skipped." || true
git clone https://github.com/tsogzark/ComfyUI-load-image-from-url.git 2>&1 | grep -q "already exists" && echo "[Mycraft UI] ComfyUI-load-image-from-url already exists. Skipped." || true
git clone https://github.com/JPS-GER/ComfyUI_JPS-Nodes.git 2>&1 | grep -q "already exists" && echo "[Mycraft UI] ComfyUI_JPS-Nodes already exists. Skipped." || true