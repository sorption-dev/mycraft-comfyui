"""
Configuration constants for Mycraft ComfyUI
"""
import os

# Directory paths
WEBROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "mycraft", "build")
TEMP_UPLOAD = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "temp_upload")
LORAS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "../../models/loras")
WORKFLOWS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "workflows")
HASH_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "lorashashes.json")

# URL slug
SLUG = "/mycraft"


