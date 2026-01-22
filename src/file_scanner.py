"""
File system scanning utilities
"""
import os
import json


def scan_lora_files(loras_dir):
    """
    Scan directory for .safetensors files
    
    Args:
        loras_dir: Directory to scan
        
    Returns:
        list: List of tuples (file_path, relative_path)
    """
    files = []
    
    if os.path.exists(loras_dir):
        for root, _, filenames in os.walk(loras_dir):
            for filename in filenames:
                if filename.endswith(".safetensors"):
                    file_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(file_path, loras_dir)
                    files.append((file_path, relative_path))
    
    return files


def count_lora_files(loras_dir):
    """Count total number of .safetensors files"""
    total = 0
    if os.path.exists(loras_dir):
        for root, _, filenames in os.walk(loras_dir):
            for filename in filenames:
                if filename.endswith(".safetensors"):
                    total += 1
    return total


def load_file_config(file_path):
    """
    Load JSON config for a file if it exists
    
    Args:
        file_path: Path to .safetensors file
        
    Returns:
        dict: Config data or None
    """
    config_path = os.path.splitext(file_path)[0] + ".json"
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"\033[91m[Mycraft UI] Error loading config {config_path}: {e}\033[0m")
            return None
    
    return None


def scan_workflow_files(workflows_dir):
    """
    Scan directory for workflow JSON files
    
    Args:
        workflows_dir: Directory to scan
        
    Returns:
        dict: Dictionary of workflow name -> workflow data
    """
    workflows = {}
    
    if os.path.exists(workflows_dir):
        for root, _, filenames in os.walk(workflows_dir):
            for filename in filenames:
                if filename.endswith(".json"):
                    file_path = os.path.join(root, filename)
                    workflow_name = os.path.splitext(filename)[0]
                    
                    try:
                        with open(file_path, 'r') as f:
                            workflows[workflow_name] = json.load(f)
                    except json.JSONDecodeError:
                        workflows[workflow_name] = None
    
    return workflows
