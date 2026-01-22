"""
Hash cache management
"""
import os
import json
from .config import HASH_FILE_PATH


class HashCache:
    """Manages loading, saving and accessing hash cache"""
    
    def __init__(self):
        self._cache = self._load_cache()
    
    def _load_cache(self):
        """Load existing hashes from file"""
        if os.path.exists(HASH_FILE_PATH):
            try:
                with open(HASH_FILE_PATH, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"\033[91m[Mycraft UI] Error loading hash cache: {e}\033[0m")
                return {}
        else:
            print(f"\033[93m[Mycraft UI] Hash cache file not found, starting with empty cache.\033[0m")
        return {}
    
    def save(self):
        """Save cache to file"""
        try:
            with open(HASH_FILE_PATH, 'w') as f:
                json.dump(self._cache, f, indent=2)
            return True
        except IOError as e:
            print(f"\033[91m[Mycraft UI] Error saving hash cache: {e}\033[0m")
            return False
    
    def get_hash(self, file_path):
        """Get cached hash for a file"""
        if file_path in self._cache and "hash" in self._cache[file_path]:
            return self._cache[file_path]["hash"]
        return None
    
    def get_civitai_data(self, file_path):
        """Get cached CivitAI data for a file"""
        if file_path in self._cache and "civitai" in self._cache[file_path]:
            return self._cache[file_path]["civitai"]
        return None
    
    def set_file_data(self, file_path, file_hash, civitai_data=None):
        """Set hash and CivitAI data for a file"""
        self._cache[file_path] = {
            "hash": file_hash,
            "civitai": civitai_data
        }
    
    def get_file_data(self, file_path):
        """Get all cached data for a file"""
        return self._cache.get(file_path)
    
    def get_all(self):
        """Get entire cache"""
        return self._cache
    
    def update_all(self, new_cache):
        """Replace entire cache"""
        self._cache = new_cache
