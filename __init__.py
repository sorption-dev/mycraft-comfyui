# DEPS
## ComfyUI_JPS-Nodes
## ComfyUI-TeaCache
## was-node-suite-comfyui
## rgthree-comfy

import os
import server
from aiohttp import web
import json
import hashlib
import aiohttp

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

WEBROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), "mycraft", "build")

TEMP_UPLOAD = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temp_upload")

slug = "/mycraft"
loras_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../models/loras")

# Load existing hashes or initialize as None
hash_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "lorashashes.json")
hashes_file = None
if os.path.exists(hash_file_path):
    with open(hash_file_path, 'r') as f:
        hashes_file = json.load(f)

def calculate_file_hash(filepath):
    """Calculate SHA256 hash of a file"""
    hash_sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

async def generate_lora_hashes():
    """Generate hash map for all .safetensors files in loras_dir"""
    hashes = {}
    
    if os.path.exists(loras_dir):
        # First, count total files
        total_files = 0
        for root, _, filenames in os.walk(loras_dir):
            for filename in filenames:
                if filename.endswith(".safetensors"):
                    total_files += 1
        
        print(f"\033[92m[Mycraft UI] Found {total_files} LoRA files to hash\033[0m")
        
        # Process files with progress
        processed = 0
        errors = {}
        for root, _, filenames in os.walk(loras_dir):
            for filename in filenames:
                if filename.endswith(".safetensors"):
                    file_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(file_path, loras_dir)
                    processed += 1
                    
                    
                    try:
                        print(f"\033[92m[Mycraft UI] Hashing ({processed}/{total_files}): {relative_path}\033[0m")
                        # Check if hash already exists
                        if hashes_file and relative_path in hashes_file and "hash" in hashes_file[relative_path]:
                            file_hash = hashes_file[relative_path]["hash"]
                            print(f"\033[92m[Mycraft UI] Using cached hash for {relative_path}\033[0m")
                        else:
                            file_hash = calculate_file_hash(file_path)
                        
                        print(f"\033[92m[Mycraft UI] Caching from Civitai ({processed}/{total_files}): {relative_path}\033[0m")
                        
                        civitai_data = hashes_file[relative_path].get("civitai", None)
                        if civitai_data:
                            # civitai_data = hashes_file[relative_path].get("civitai", None)
                            print(f"\033[92m[Mycraft UI] Using cached CivitAI data for {relative_path}\033[0m")
                        else:
                            civitai_data = None
                            # Fetch metadata from CivitAI API
                            async with aiohttp.ClientSession() as session:
                                async with session.get(f"https://civitai.com/api/v1/model-versions/by-hash/{file_hash}") as response:
                                    if response.status == 200:
                                        civitai_data = await response.json()
                                        print(f"\033[92m[Mycraft UI] CivitAI data: {len(civitai_data)} bytes\033[0m")
                                    else:
                                        print(f"\033[91m[Mycraft UI] CivitAI API returned status {response.status}\033[0m")
                                        errors[relative_path] = f"API error: {response.status}"
                        
                        hashes[relative_path] = {
                            "hash": file_hash,
                            "civitai": civitai_data
                        }
                        
                    except Exception as e:
                        print(f"\033[91m[Mycraft UI] Error hashing {relative_path}: {e}\033[0m")
    
    # Save to lorashashes.json
    # hash_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "lorashashes.json")
    with open(hash_file_path, 'w') as f:
        json.dump(hashes, f, indent=2)
    
    print(f"\033[92m[Mycraft UI] Generated hashes and caches for {len(hashes)} LoRA files\033[0m")

    if errors:
        print(f"\033[91m[Mycraft UI] Errors occurred while processing files:\033[0m")
        for file, error in errors.items():
            print(f" - {file}: {error}")

@server.PromptServer.instance.routes.get(slug + "/recalculate_hashes")
async def recalculate_hashes(request):
    await generate_lora_hashes()
    return web.json_response({"status": "done"})



@server.PromptServer.instance.routes.get(slug + "/list-loras")
async def list_loras(request):
    files = []
    
    for root, _, filenames in os.walk(loras_dir):
        for filename in filenames:
            if filename.endswith(".safetensors"):
                relative_path = os.path.relpath(os.path.join(root, filename), loras_dir)
                config_path = os.path.splitext(os.path.join(root, filename))[0] + ".json"
                
                id = relative_path.replace("\\", "_")
                id = id.replace(".safetensors", "")
                hash_value = hashes_file.get(relative_path) if hashes_file else None

                if os.path.exists(config_path):
                    with open(config_path, 'r') as config_file:
                        config = json.load(config_file)
                        files.append({
                            **config,
                            "id": id,
                            "title": config.get("title", os.path.splitext(filename)[0]),
                            "file": relative_path,
                            "hash": hash_value["hash"] if hash_value else None,
                            "civitai": hash_value["civitai"] if hash_value else None,
                        })
                else:
                    files.append({
                        "id": id,
                        "title": os.path.splitext(filename)[0],
                        "file": relative_path,
                        "hash": hash_value["hash"] if hash_value else None,
                        "civitai": hash_value["civitai"] if hash_value else None,
                    })
    return web.json_response(files)


@server.PromptServer.instance.routes.get(slug + "/api/list-workflows")
async def list_workflows(request):
    workflows_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "workflows")
    combined_workflows = {}

    for root, _, filenames in os.walk(workflows_dir):
        for filename in filenames:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r') as json_file:
                    try:
                        combined_workflows[os.path.splitext(filename)[0]] = json.load(json_file)
                    except json.JSONDecodeError:
                        combined_workflows[os.path.splitext(filename)[0]] = None

    return web.json_response(combined_workflows)

@server.PromptServer.instance.routes.post(slug + "/api/upload-image")
async def handle_upload(request):
    reader = await request.multipart()
    field = await reader.next()
    filename =  field.filename
    temp_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temp_upload")
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, filename)
    file_path_for_web = f"{slug}/temp_upload/{filename}"

    with open(file_path, 'wb') as f:
        while True:
            chunk = await field.read_chunk()
            if not chunk:
                break
            f.write(chunk)
    
    return web.json_response({"message": "File uploaded successfully", "file_path": file_path_for_web})

# Отдаем index.html на /mycraft
# @server.PromptServer.instance.routes.get(slug)
# async def react_root(request):
#     return web.FileResponse(os.path.join(WEBROOT, 'index.html'))

@server.PromptServer.instance.routes.get(slug)
async def react_catch_all(request):
    file = os.path.join(WEBROOT, 'index.html')
    return web.FileResponse(file)

@server.PromptServer.instance.routes.get(slug + "/p/{tail:.*}")
async def react_catch_all(request):
    file = os.path.join(WEBROOT, 'index.html')
    return web.FileResponse(file)



# Отдаем статику
server.PromptServer.instance.routes.static(slug, path=WEBROOT)
server.PromptServer.instance.routes.static(slug+"/temp_upload", path=TEMP_UPLOAD)



print("\n\033[92m[Mycraft UI] Ready!\033[0m\n")

# handle file uploads


