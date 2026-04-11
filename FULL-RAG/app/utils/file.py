import os
import aiofiles

# aiofiles is a Python library used to handle local file I/O asynchronously within asyncio applications

# Why use it?
# In standard Python, file operations like open().read() are blocking.
# If you use them inside an async function, they will stop the entire event loop until the file operation finishes, defeating the purpose of asynchronous programming.
# aiofiles solves this by offloading these operations to a separate thread pool, allowing your main event loop to keep running.


async def save_to_disk(file: bytes, path: str) -> bool:
    # File save hone se pehle folder (directory) create kar raha hai agar wo exist nahi karta
    os.makedirs(os.path.dirname(path), exist_ok=True)

    async with aiofiles.open(path, 'wb') as out_file:
        await out_file.write(file)

    return True
