# his program downloads 3 images from the internet.

import threading
import requests
import time

def download(url):
    print(f"Start download from {url}")
    # requests.get() spends most of the time WAITING for the internet (this is called I/O bound task)
    resp = requests.get(url) 
    print(f"Finished downloading from {url}, size: {len(resp.content)} bytes")

urls = [
    "https://httpbin.org/image/png",
    "https://httpbin.org/image/jpeg",
    "https://httpbin.org/image/svg",
]

start = time.time()
threads = []

for url in urls:
    t = threading.Thread(target=download, args=(url, ))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

end = time.time()

print(f"All downloads done in {end-start:.2f} seconds")


# Note :
# Threading is useful for I/O-bound tasks such as network requests, file downloads, and database queries. In this example, each thread downloads an image using requests.get().
#  When a thread waits for the internet response, it releases the GIL, allowing another thread to run. Because of this, multiple downloads can happen at the same time, reducing the total execution time.

# Rule:
# CPU-bound tasks → use multiprocessing
# I/O-bound tasks → use threading