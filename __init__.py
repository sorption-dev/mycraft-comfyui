# Node mappings
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

import os

from .install import extract_mycraft_ui
build_path = os.path.join(os.path.dirname(__file__), "mycraft", "build")
if not os.path.exists(build_path):
    extract_mycraft_ui()

from .src.routes import setup_routes
setup_routes()

print("\n\033[92m[Mycraft UI] Ready!\033[0m\n")
