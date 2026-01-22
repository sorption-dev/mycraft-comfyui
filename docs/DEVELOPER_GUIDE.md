# Developer Guide - Mycraft ComfyUI

## Quick Start for Developers

### Project Structure

```
mycraft-comfyui/
├── __init__.py              # Entry point (initialization)
├── config.py                # Configuration (constants, paths)
├── routes.py                # HTTP routes and handlers
├── lora_manager.py          # LoRA business logic
├── civitai_api.py           # CivitAI API integration
├── hash_cache.py            # Hash cache management
├── file_scanner.py          # File system scanning
├── utils.py                 # Helper functions
├── ARCHITECTURE.md          # Detailed architecture
└── REFACTORING.md           # Refactoring history
```

## Where to Find What

### 🔧 Need to add a new HTTP endpoint?
➡️ **`routes.py`** - add new `@server.PromptServer.instance.routes` decorator

### 📂 Need to work with files?
➡️ **`file_scanner.py`** - add scanning function

### 🌐 Need to integrate external API?
➡️ Create a new file similar to **`civitai_api.py`**

### 💾 Need to cache data?
➡️ **`hash_cache.py`** - extend `HashCache` class or create similar

### 🎯 Need to add business logic?
➡️ **`lora_manager.py`** - add function using services

### ⚙️ Need to add a constant or path?
➡️ **`config.py`** - add constant

## Development Rules

### 1. Separation of Concerns

❌ **Bad:**
```python
# In routes.py - direct external API call
@server.PromptServer.instance.routes.get("/data")
async def get_data(request):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.example.com") as response:
            data = await response.json()
    return web.json_response(data)
```

✅ **Good:**
```python
# In api_service.py
async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.example.com") as response:
            return await response.json()

# In routes.py - HTTP handling only
@server.PromptServer.instance.routes.get("/data")
async def get_data(request):
    data = await fetch_data()
    return web.json_response(data)
```

### 2. Avoid Circular Dependencies

✅ **Correct hierarchy:**
```
config.py (no dependencies)
  ↑
utils.py (depends on config)
  ↑
file_scanner.py (depends on config)
  ↑
lora_manager.py (depends on utils, file_scanner)
  ↑
routes.py (depends on lora_manager)
```

### 3. Use Type Hints

✅ **Good:**
```python
def calculate_file_hash(filepath: str) -> str:
    """Calculate SHA256 hash of a file"""
    # ...
```

### 4. Document Functions

✅ **Good:**
```python
async def fetch_model_metadata(file_hash: str) -> dict | None:
    """
    Fetch metadata from CivitAI API by file hash
    
    Args:
        file_hash: SHA256 hash of the model file
        
    Returns:
        dict: Model metadata from CivitAI or None if not found
    """
```

### 5. Handle Errors

✅ **Good:**
```python
try:
    data = await fetch_model_metadata(file_hash)
except Exception as e:
    print(f"\033[91m[Mycraft UI] Error: {e}\033[0m")
    return None
```

## Adding New Features

### Example: Adding Checkpoint Support

1. **In `file_scanner.py`** - add scanning function:
```python
def scan_checkpoint_files(checkpoints_dir: str):
    """Scan directory for checkpoint files"""
    # ...
```

2. **In `config.py`** - add path:
```python
CHECKPOINTS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../models/checkpoints")
```

3. **Create `checkpoint_manager.py`**:
```python
from .config import CHECKPOINTS_DIR
from .file_scanner import scan_checkpoint_files

def get_checkpoint_files():
    """Get list of all checkpoint files"""
    # ...
```

4. **In `routes.py`** - add endpoint:
```python
from .checkpoint_manager import get_checkpoint_files

@server.PromptServer.instance.routes.get(SLUG + "/list-checkpoints")
async def list_checkpoints(request):
    files = get_checkpoint_files()
    return web.json_response(files)
```

## Testing

### Unit Tests (recommended to add)

```python
# tests/test_file_scanner.py
import pytest
from file_scanner import scan_lora_files

def test_scan_lora_files():
    files = scan_lora_files("./test_data")
    assert len(files) > 0
```

### Manual Testing

1. Start ComfyUI
2. Open http://localhost:8188/mycraft
3. Check console for errors

## Debugging

### Enable Detailed Logs

Add at the beginning of the module:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

Use:
```python
logger.debug(f"Processing file: {filename}")
logger.info(f"Found {count} files")
logger.error(f"Error: {e}")
```

## Useful Commands

### Syntax Check
```bash
python -m py_compile *.py
```

### Code Formatting (if black is installed)
```bash
black *.py
```

### Import Check (if pylint is installed)
```bash
pylint *.py
```

## Pre-Commit Checklist

- [ ] Code follows project structure
- [ ] No circular dependencies
- [ ] Docstrings added to functions
- [ ] Possible errors handled
- [ ] Manually tested in ComfyUI
- [ ] Documentation updated (if needed)

