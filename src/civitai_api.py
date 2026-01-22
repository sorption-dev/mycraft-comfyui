"""
CivitAI API integration
"""
import aiohttp


async def fetch_model_metadata(file_hash):
    """
    Fetch metadata from CivitAI API by file hash
    
    Args:
        file_hash: SHA256 hash of the model file
        
    Returns:
        dict: Model metadata from CivitAI or None if not found
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://civitai.com/api/v1/model-versions/by-hash/{file_hash}") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"\033[92m[Mycraft UI] CivitAI data: {len(str(data))} bytes\033[0m")
                    return data
                else:
                    print(f"\033[91m[Mycraft UI] CivitAI API returned status {response.status}\033[0m")
                    return None
    except Exception as e:
        print(f"\033[91m[Mycraft UI] Error fetching CivitAI metadata: {e}\033[0m")
        return None
