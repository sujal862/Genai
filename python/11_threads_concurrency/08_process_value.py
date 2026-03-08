# since each process has its own memory so sharing variable is not possible so we use Value , Queue , Array from multiprocessing
# how to safely share data between multiple processes using multiprocessing.Value and a lock.

from multiprocessing import Process, Value

def increment(counter):
    for _ in range(100000):
        # Since multiple processes may update the value simultaneously, a lock is used
        with counter.get_lock():
            counter.value += 1


if __name__ == "__main__":
    # This creates a shared integer: 'i' → integer type , 0 → initial value
    counter = Value('i', 0) 
    processes = [Process(target=increment, args=(counter, )) for _ in range(4)]
    [p.start() for p in processes]
    [p.join() for p in processes]

    print("Final counter value: ",counter.value )