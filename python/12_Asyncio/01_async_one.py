# asyncio allows one program to handle multiple waiting tasks efficiently using a single thread.

import asyncio

async def brew_chai():
    print("brewing chai...")
    await asyncio.sleep(2) # jab tak ye task wait kare tab tak doosra task run ho sakta hai
    print("Chai is ready")


asyncio.run(brew_chai())

# Asyncio internally uses Even loop:
# Event loop ka kaam:
# check karo konsa task wait kar raha
# aur konsa ready hai run karne ke liye



# Key Functions and Features
# asyncio.run(main()): The main entry point to run the top-level async function.
# await: Suspends the execution of a coroutine until the awaited task is complete.
# asyncio.gather(*aws): run multiple async tasks concurrently and wait for all of them to finish
# asyncio.create_task(coro): Schedules a coroutine to run, returning a Task object.
# asyncio.sleep(delay): Pauses for a specified time without blocking the event loop.


# IMP : Coroutines vs Blocking func 
# Coroutines are lightweight, non-blocking asynchronous tasks that suspend execution, allowing the underlying thread to do other work,
# while blocking functions pause the entire thread until the task completes