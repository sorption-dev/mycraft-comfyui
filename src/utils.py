"""
Utility functions for Mycraft ComfyUI
"""
import hashlib
# import zlib


def calculate_file_hash(filepath):
    """Calculate SHA256 hash of a file"""
    hash_sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

# def calculate_file_crc32(filepath):
#     """Calculate CRC32 hash of a file"""
#     crc32_hash = 0
#     with open(filepath, 'rb') as f:
#         for chunk in iter(lambda: f.read(4096), b""):
#             crc32_hash = zlib.crc32(chunk, crc32_hash)
#     return format(crc32_hash & 0xFFFFFFFF, '08x')

if __name__ == "__main__":
    # Example usage
    test_file = "Little_Tinies.safetensors"
    print(f"SHA256: {calculate_file_hash(test_file)}")
    # print(f"CRC32: {calculate_file_crc32(test_file)}")
