# Learning : Async code ke andar blocking function kaise run karein without blocking the event loop.
# see 04 file code , instead thread we are using process to run blocking code

import asyncio
from concurrent.futures import ProcessPoolExecutor

# CPU bound task (blocking)
def encrypt(data):
    return f" {data[::-1]}"

async def main():
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool,
            encrypt,
            "credit_card_1234"
        )

        print(result)

if __name__ == "__main__":
    asyncio.run(main())