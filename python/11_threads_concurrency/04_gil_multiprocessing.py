# multiprocessing allows true parallel execution using multiple CPU cores (Speed up the Process)
from multiprocessing import Process
import time
def crunch_number():
    print(f"Started the count process...")
    count = 0
    for _ in range(100_000_000):
        count += 1
    print(f"Ended the count process...")


if __name__ == "__main__":
    start = time.time()

    p1 = Process(target=crunch_number)
    p2 = Process(target=crunch_number)

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    end = time.time()
    print(f"Total time : {end - start:.2f} sec")



# Notes :
# multiprocessing creates separate processes instead of threads.
# Each process has its own Python interpreter and memory.
# Because of this, GIL does not block them, so they can run on multiple CPU cores simultaneously.