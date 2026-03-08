# IMPPP:  Unlike the synchronous "requests" library, which blocks the entire program while waiting for an I/O response,
# aiohttp's ClientSession allows the asyncio event loop to switch to other tasks during waiting periods, significantly improving efficiency in I/O-bound applications like making many API calls. 


import asyncio
import aiohttp

async def fetch_url(session, url):
    #async with :  jab tak response aaye tab tak event loop dusre tasks run kar sakta hai So program block nahi hota.
    async with session.get(url) as response:
        print(f"Fetched {url} with status {response.status}")

async def main():
    urls = ["https://httpbin.org/delay/2"] * 3 # Ye endpoint 2 second delay karta hai intentionally.
    # HTTP session open -> requests bhejo -> session automatically closes
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        await asyncio.gather(*tasks) # ...spread jaisa smjlo isko similar to await asyncio.gather(t1, t2, t3)

asyncio.run(main())





# Notes :
# ClientSession ek HTTP client object hai jo server ko request bhejta hai.
# isko asa smjo ki maina ak browser tab open kiya or mutiple request(web search) kr skta hai , but 2nd way hota ki hum har request ka bad browser band krda or phir sa khola new request ka lia 
# to yha clientSession yhi krta hai har request ka lia new session ni bntata , ak hi session ko reuse krta hai 


# 5️⃣ MERN stack analogy

# Node.js example
# const axios = require("axios")

# async function fetchData(){
#    const res = await axios.get("https://api.com")
# }

# Har request me axios new connection create karta hai.
# request1 → connection open
# request2 → connection open
# request3 → connection open

# Better approach (Node me)
# const axios = axios.create({
#    baseURL: "https://api.com"
# })

# Ye client instance(connection) create karta hai jise multiple requests use kar sakti hain.

# Exactly wahi kaam Python me: ClientSession() karta hai.

# ClientSession
#    |
#    ├ request1
#    ├ request2
#    └ request3

# Connection reuse ✅ -> Faster