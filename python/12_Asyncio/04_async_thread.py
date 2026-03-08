# Learning : Async code ke andar blocking function kaise run karein without blocking the event loop.
# await asyncio.sleep(2) :  Non blocking ops  |   time.sleep(2) : blocking ops

# run_in_executor() allows blocking functions to run in a separate thread or process without blocking the asyncio event loop. This helps integrate synchronous code with asynchronous programs.
# ThreadPoolExecutor → threads ka pool create karta hai jisme blocking functions run kar sakte hain


import asyncio                      
import time                         
from concurrent.futures import ThreadPoolExecutor  # thread pool create karne ke liye


# Ye ek normal (blocking) function hai
# Ye async function nahi hai
def check_stock(item):
    print(f"Checking {item} in store...")

    # Ye blocking operation hai
    # Agar ye event loop me directly chale to pura async program ruk jayega
    time.sleep(3)
    return f"{item} stock: 42"


# Ye async function hai jo event loop me run hoga
async def main():

    # Current asyncio event loop ko le rahe hain / aquire kr rha hai 
    # Event loop async tasks ko manage karta hai
    loop = asyncio.get_running_loop()

    # ThreadPoolExecutor create kar rahe hain
    # Ye threads ka pool hai jisme blocking tasks run kar sakte hain
    with ThreadPoolExecutor() as pool:

        # Important line
        # run_in_executor blocking function ko alg thread me run karta hai
        # taaki event loop block na ho or dusre async tasks run kar sake

        result = await loop.run_in_executor(
            pool,              # kis thread pool me run karna hai
            check_stock,       # kaunsa function run karna hai
            "Masala chai"      # function ka argument
        )

        # Jab thread ka kaam complete ho jata hai
        # result yaha return hota hai
        print(result)


# asyncio event loop start karta hai
# aur main() coroutine ko run karta hai
asyncio.run(main())








# # Extra for just seeing proof in real:-

# #mix async tasks + blocking task and see that blocking task does NOT block async tasks when we use run_in_executor().
# # demonstration code.


# import asyncio
# import time
# from concurrent.futures import ThreadPoolExecutor


# # -------------------------------
# # Blocking function (normal function)
# # -------------------------------
# def check_stock(item):
#     print(f"Checking stock for {item} (blocking task)...")
    
#     # simulate slow blocking work
#     time.sleep(3)

#     return f"{item} stock: 42"


# # -------------------------------
# # Async task
# # -------------------------------
# async def make_chai(name):
#     print(f"{name}: Boiling water...")

#     # async sleep (does NOT block event loop)
#     await asyncio.sleep(2)

#     print(f"{name}: Chai ready!")


# # -------------------------------
# # Main async program
# # -------------------------------
# async def main():

#     # get currently running event loop
#     loop = asyncio.get_running_loop()

#     # create thread pool for blocking tasks
#     with ThreadPoolExecutor() as pool:

#         # send blocking function to thread pool
#         blocking_task = loop.run_in_executor(
#             pool,
#             check_stock,
#             "Masala chai"
#         )

#         # create async tasks
#         chai1 = asyncio.create_task(make_chai("Worker-1"))
#         chai2 = asyncio.create_task(make_chai("Worker-2"))

#         # wait for all tasks together
#         results = await asyncio.gather(
#             blocking_task,
#             chai1,
#             chai2
#         )

#         print("Blocking result:", results[0])


# # start event loop
# asyncio.run(main())