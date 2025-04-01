import zipfile
import os

def extract_zip(file_path, extract_to):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        print(f"Extracted {file_path} to {extract_to}")

zip_file = "mycraft.zip"
output_dir = "mycraft"
extract_zip(zip_file, output_dir)
print("Mycraft UI installed successfully!")

# os.remove(zip_file)
# print(f"Deleted {zip_file} after extraction.")
