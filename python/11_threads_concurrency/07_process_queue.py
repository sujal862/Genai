from multiprocessing import Process, Queue

def prepare_chai(queue):
    queue.put("Masala chai is ready") # Insert data into the queue (child process sa insert krwa rha hai)



if __name__ == '__main__':
    queue = Queue()

    p = Process(target=prepare_chai, args=(queue,)) # queue is passed as an argument so the process can send data back to the main process.
    p.start()
    p.join()
    print(queue.get()) # get() removes and returns an item from the queue. (child process sa insert kraka main process mai acces kr rha )