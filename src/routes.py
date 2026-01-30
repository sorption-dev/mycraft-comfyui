"""
Web routes and handlers for Mycraft ComfyUI
"""
import os
from aiohttp import web
import server
from .config import SLUG, WEBROOT, TEMP_UPLOAD
from .lora_manager import generate_lora_hashes, get_lora_files, check_hash_cache
from .file_scanner import scan_workflow_files


def setup_routes():
    """Setup all web routes for the application"""
    
    @server.PromptServer.instance.routes.get(SLUG + "/api/recalculate_hashes")
    async def recalculate_hashes(request):
        """Recalculate all LoRA hashes"""
        await generate_lora_hashes()
        return web.json_response({"status": "done"})

    @server.PromptServer.instance.routes.get(SLUG + "/api/list-loras")
    async def list_loras(request):
        """Get list of all LoRA files"""
        files = get_lora_files()
        return web.json_response(files)

    @server.PromptServer.instance.routes.get(SLUG + "/api/list-workflows")
    async def list_workflows(request):
        """Get list of all workflow files"""
        from .config import WORKFLOWS_DIR
        workflows = scan_workflow_files(WORKFLOWS_DIR)
        return web.json_response(workflows)

    @server.PromptServer.instance.routes.post(SLUG + "/api/upload-image")
    async def handle_upload(request):
        """Handle image file upload"""
        reader = await request.multipart()
        field = await reader.next()
        filename = field.filename
        temp_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "temp_upload")
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, filename)
        file_path_for_web = f"{SLUG}/temp_upload/{filename}"

        with open(file_path, 'wb') as f:
            while True:
                chunk = await field.read_chunk()
                if not chunk:
                    break
                f.write(chunk)
        
        return web.json_response({"message": "File uploaded successfully", "file_path": file_path_for_web})

    @server.PromptServer.instance.routes.get(SLUG)
    async def react_root(request):
        """Serve React app root"""
        file = os.path.join(WEBROOT, 'index.html')
        return web.FileResponse(file)

    @server.PromptServer.instance.routes.get(SLUG + "/p/{tail:.*}")
    async def react_catch_all(request):
        """Serve React app for all routes"""
        file = os.path.join(WEBROOT, 'index.html')
        return web.FileResponse(file)

    # Setup static routes
    server.PromptServer.instance.routes.static(SLUG, path=WEBROOT)
    server.PromptServer.instance.routes.static(SLUG + "/temp_upload", path=TEMP_UPLOAD)
