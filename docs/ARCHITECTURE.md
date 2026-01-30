# Mycraft ComfyUI Architecture

## Module Structure

The project is divided into several specialized modules for better code organization and maintainability.

### 📋 `__init__.py` - Entry Point
Main ComfyUI plugin initialization file.
- Imports configuration
- Registers web routes
- Minimal logic, initialization only

### ⚙️ `config.py` - Configuration
All application constants and settings in one place.
- Directory paths (WEBROOT, TEMP_UPLOAD, LORAS_DIR, etc.)
- URL slug
- Node mappings for ComfyUI

### 🛣️ `routes.py` - Web Routes (HTTP only)
HTTP endpoint registration and request/response handling only.
- `/mycraft/api/recalculate_hashes` - trigger hash recalculation
- `/mycraft/api/list-loras` - get LoRA list
- `/mycraft/api/list-workflows` - get workflows list
- `/mycraft/api/upload-image` - image upload
- React routes for SPA

**Dependencies:** `aiohttp.web`, `server` (ComfyUI)

### 🗂️ `lora_manager.py` - LoRA Management (Business Logic)
High-level LoRA file operations logic, without direct HTTP or API calls.
- `generate_lora_hashes()` - orchestrates hash generation process
- `get_lora_files()` - collects LoRA file data

**Dependencies:** `hash_cache`, `file_scanner`, `civitai_api`, `utils`

### 🌐 `civitai_api.py` - CivitAI API (External API)
External CivitAI API integration.
- `fetch_model_metadata()` - fetch model metadata by hash

**Dependencies:** `aiohttp`

### 📂 `file_scanner.py` - File System Scanning
Pure file system operations, no business logic.
- `scan_lora_files()` - find .safetensors files
- `count_lora_files()` - count files
- `load_file_config()` - load JSON configs
- `scan_workflow_files()` - scan workflow files

**Dependencies:** standard library only (`os`, `json`)

### 💾 `hash_cache.py` - Hash Cache
Hash and metadata caching management.
- `HashCache` class - works with lorashashes.json
- Load/save cache
- Get/set data

**Dependencies:** standard library only (`os`, `json`)

### 🔧 `utils.py` - Utilities
General purpose helper functions.
- `calculate_file_hash()` - calculate SHA256 hash

**Dependencies:** standard library only (`hashlib`)

## Dependency Diagram

```
__init__.py
├── config.py
└── routes.py
    ├── server (ComfyUI)
    ├── aiohttp.web
    ├── file_scanner.py
    └── lora_manager.py
        ├── hash_cache.py
        ├── file_scanner.py
        ├── civitai_api.py
        │   └── aiohttp
        └── utils.py
```

## Separation Principles

1. **Separation of Concerns** - each module is responsible for one area
2. **Minimal Dependencies** - low-level modules don't depend on external APIs
3. **Testability** - logic is separated from HTTP and external APIs
4. **Reusability** - modules can be used independently

## Architecture Layers

1. **HTTP Layer** (`routes.py`) - web request handling
2. **Business Logic** (`lora_manager.py`) - operation orchestration
3. **Services** (`civitai_api.py`, `hash_cache.py`) - specialized operations
4. **Utilities** (`file_scanner.py`, `utils.py`) - low-level operations
5. **Configuration** (`config.py`) - settings

