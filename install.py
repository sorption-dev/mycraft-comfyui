import zipfile
import os

def extract_zip(file_path, extract_to):
    if not os.path.exists(file_path):
        print(f"\033[91m[Mycraft UI] File {file_path} does not exist.\033[0m")
        return

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        print(f"\033[92m[Mycraft UI] Extracted {file_path} to {extract_to}\033[0m")

def extract_mycraft_ui():
    zip_file = os.path.join(os.path.dirname(__file__), "mycraft.zip")
    output_dir = os.path.join(os.path.dirname(__file__), "mycraft")
    print(f"\033[92m[Mycraft UI] Installing Mycraft UI...\033[0m\nfrom {zip_file}")
    extract_zip(zip_file, output_dir)
    print(f"\033[92m[Mycraft UI] Mycraft UI installed successfully!\033[0m")

# os.remove(zip_file)
# print(f"Deleted {zip_file} after extraction.")

if __name__ == "__main__":
    extract_mycraft_ui()
