# GIL = GIL (Global Interpreter Lock) is a lock in CPython that allows only one thread to execute Python code at a time, even if multiple threads exist. Because of this, CPU-bound programs do not run faster with threading. to run fast use MultiProcessing
import threading
import time

def brew_chai():
    # threading.current_thread() → returns the thread currently running.
    print(f"{threading.current_thread().name}started brewing...")  
    # CPU Bound programs
    count = 0 # beach thread will have own count var but both will share same memory
    for _ in range(100_000_000):
        count += 1
    print(f"{threading.current_thread().name} finished brewing...")

# dono execution turn-by-turn ho raha hai because of GIL.
thread1 =threading.Thread(target=brew_chai, name="Barista-1")
thread2 = threading.Thread(target=brew_chai, name="Barista-2")

start = time.time() # stores the current time so we can measure execution time.
thread1.start()
thread2.start()
thread1.join()
thread2.join()
end = time.time() # Get the time after execution finishes.

print(f"total time taken: {end - start:.2f} seconds")