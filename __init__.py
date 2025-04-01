# DEPS
## ComfyUI_JPS-Nodes
## ComfyUI-TeaCache
## was-node-suite-comfyui

import os
import server
from aiohttp import web
import uuid
import json

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

WEBROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), "mycraft", "build")

TEMP_UPLOAD = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temp_upload")

slug = "/mycraft"

@server.PromptServer.instance.routes.get(slug + "/list-loras")
async def list_loras(request):
    loras_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../models/loras")
    files = []
    
    for root, _, filenames in os.walk(loras_dir):
        for filename in filenames:
            if filename.endswith(".safetensors"):
                relative_path = os.path.relpath(os.path.join(root, filename), loras_dir)
                config_path = os.path.splitext(os.path.join(root, filename))[0] + ".json"
                
                id = relative_path.replace("\\", "_")
                id = id.replace(".safetensors", "")

                if os.path.exists(config_path):
                    with open(config_path, 'r') as config_file:
                        config = json.load(config_file)
                        files.append({
                            **config,
                            "id": id,
                            "title": config.get("title", os.path.splitext(filename)[0]),
                            "file": relative_path,
                        })
                else:
                    files.append({
                        "id": id,
                        "title": os.path.splitext(filename)[0],
                        "file": relative_path
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



print("\n\033[92m[Valera UI] Ready!\033[0m\n")

# handle file uploads


