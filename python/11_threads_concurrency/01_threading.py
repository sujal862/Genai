# gyan: Concurrency(threading) is managing multiple tasks by switching between them, while parallelism (parallelism) is executing multiple tasks simultaneously using multiple CPU cores.


# Multithreading : 1 core but many workers(thread)

import threading   # threading module use hota hai multiple threads banane ke liye
import time        # time.sleep() delay dene ke liye use hota hai

def take_orders():
    for i in range(1, 4):
        print(f"Taking order for #{i}")
        time.sleep(2) # wait 2 sec after taking each order

def brew_chai():
    for i in range(1, 4):
        print(f"Brewing chai for #{i}")
        time.sleep(3) # wait 3 sec

# Threading bolta hai: Orders bhi start karo & Chai bhi start karo
# Ab CPU dono kaam switch switch karke karta hai saves time by overlapping.
order_thread  = threading.Thread(target=take_orders)
brew_thread = threading.Thread(target=brew_chai)

order_thread.start()
brew_thread.start()

# join : main program wait karega jab tak dono thread finish nahi hota
order_thread.join()
brew_thread.join()

# jab dono threads ka kaam complete ho jaye tab ye line run hogi
print(f"All orders taken and chai brewed")



# Notes: 
# Main program (full file)-> isika andr dono thread hai 
#       |
#       |---- order_thread → take_orders()
#       |
#       |---- brew_thread  → brew_chai()

# using join let : Main thread wait karega jab tak dono thread finish nahi ho jata uska bad hi main thread ka "join" ka aga wala code execute hoga i.e print(ALL orders taken ....)