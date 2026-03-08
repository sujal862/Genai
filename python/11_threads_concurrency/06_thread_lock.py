import threading   
count = 0          # shared global variable (both threads will modify this)
lock = threading.Lock()   # create a lock to protect the shared variable


def increase():
    global count   # tells Python to use the global variable 'count'

    # each thread will try to increase the counter 100000 times (at last count = 200000)
    for _ in range(100000):

        # 'with lock:' acquires the lock before entering the block
        # only ONE thread can hold the lock at a time
        # other threads must wait until the lock is released
        with lock:

            # critical section (shared data modification)
            # because of the lock, only one thread updates count at a time
            count += 1

        # after leaving the 'with' block, the lock is automatically released


t1 = threading.Thread(target=increase)
t2 = threading.Thread(target=increase)

t1.start()
t2.start()

t1.join()
t2.join()

print("Final count:", count)



# Note:
# What happens if we do NOT use a Lock in threading?

# When multiple threads modify the same shared variable without synchronization, a race condition can occur.
# A race condition means the final result becomes unpredictable because threads access and update the variable at the same time.

# Actual results (may vary) will not be  200000

# The result changes each run because both threads update the same variable at the same time, causing some increments to be lost.


# Example of the conflict
# Suppose: count = 5

# Two threads run at the same time:

# Thread1 reads count = 5
# Thread2 reads count = 5

# Thread1 writes count = 6
# Thread2 writes count = 6

# Expected value: 7

# Actual value: 6

# One update is lost.