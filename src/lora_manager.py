"""
LoRA file management and hashing functionality
"""
import os
from .config import LORAS_DIR, HASH_FILE_PATH
from .utils import calculate_file_hash
from .hash_cache import HashCache
from .file_scanner import scan_lora_files, count_lora_files, load_file_config
from .civitai_api import fetch_model_metadata
import asyncio

_hash_cache = HashCache()

async def generate_lora_hashes():
    """Generate hash map for all .safetensors files in loras_dir"""
    # Count files
    total_files = count_lora_files(LORAS_DIR)
    print(f"\033[92m[Mycraft UI] Found {total_files} LoRA files to hash\033[0m")
    
    # Scan files
    files = scan_lora_files(LORAS_DIR)
    processed = 0
    errors = {}
    
    for file_path, relative_path in files:
        processed += 1
        
        try:
            # Check if hash already exists in cache
            cached_hash = _hash_cache.get_hash(relative_path)
            if cached_hash:
                file_hash = cached_hash
                print(f"\033[92m[Mycraft UI] Using cached hash ({processed}/{total_files}): {relative_path}\033[0m")
            else:
                print(f"\033[92m[Mycraft UI] Hashing ({processed}/{total_files}): {relative_path}\033[0m")
                file_hash = calculate_file_hash(file_path)
            
            # Check for cached CivitAI data
            cached_civitai = _hash_cache.get_civitai_data(relative_path)
            if cached_civitai:
                print(f"\033[92m[Mycraft UI] Using cached CivitAI data ({processed}/{total_files}): {relative_path}\033[0m")
                civitai_data = cached_civitai
            else:
                print(f"\033[92m[Mycraft UI] Fetching from CivitAI ({processed}/{total_files}): {relative_path}\033[0m")
                civitai_data = await fetch_model_metadata(file_hash)
                if civitai_data is None:
                    errors[relative_path] = "Failed to fetch CivitAI data"
            
            # Update cache
            _hash_cache.set_file_data(relative_path, file_hash, civitai_data)
            
        except Exception as e:
            print(f"\033[91m[Mycraft UI] Error processing {relative_path}: {e}\033[0m")
            errors[relative_path] = str(e)
    
    # Save cache to file
    _hash_cache.save()
    
    print(f"\033[92m[Mycraft UI] Generated hashes and caches for {processed} LoRA files\033[0m")
    
    if errors:
        print(f"\033[91m[Mycraft UI] Errors occurred while processing files:\033[0m")
        for file, error in errors.items():
            print(f" - {file}: {error}")


def get_lora_files():
    """Get list of all LoRA files with their metadata"""
    files = []
    
    for file_path, relative_path in scan_lora_files(LORAS_DIR):
        # Generate ID from path
        file_id = relative_path.replace("\\", "_").replace(".safetensors", "")
        
        # Load config if exists
        config = load_file_config(file_path)
        
        # Get cached hash data
        hash_data = _hash_cache.get_file_data(relative_path)
        
        # Build file entry
        if config:
            file_entry = {
                **config,
                "id": file_id,
                "title": config.get("title", os.path.splitext(os.path.basename(file_path))[0]),
                "file": relative_path,
                "hash": hash_data["hash"] if hash_data else None,
                "civitai": hash_data["civitai"] if hash_data else None,
            }
        else:
            file_entry = {
                "id": file_id,
                "title": os.path.splitext(os.path.basename(file_path))[0],
                "file": relative_path,
                "hash": hash_data["hash"] if hash_data else None,
                "civitai": hash_data["civitai"] if hash_data else None,
            }
        
        files.append(file_entry)
    
    return files

async def check_hash_cache():
    if not os.path.exists(HASH_FILE_PATH):
        print(f"\033[93m[Mycraft UI] Hash cache file not found at {HASH_FILE_PATH}, generating new cache.\033[0m")
        await generate_lora_hashes()
        _hash_cache._load_cache()

# Run check_hash_cache on module import
asyncio.create_task(check_hash_cache())
