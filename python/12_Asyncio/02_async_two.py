import asyncio

# async function (coroutine)
# this function can pause and resume execution
async def make_chai():
    print("Boiling water...")

    # 'await' pauses this task for 2 seconds
    # during this waiting time, the event loop can run other tasks
    await asyncio.sleep(2)

    print("Chai ready")


# main async function that schedules tasks
async def main():

    # create first task and register it with the event loop
    task1 = asyncio.create_task(make_chai())
    task2 = asyncio.create_task(make_chai())

    # wait until task1 finishes
    # while task1 is waiting (sleep), the event loop runs other tasks
    await task1
    # wait until task2 finishes
    await task2


# start the asyncio event loop and run the main coroutine
# the event loop manages and switches between async tasks
asyncio.run(main())


#await ka matlab hai:

# main abhi ruk raha hu
# jab tak ye kaam complete ho
# tab tak event loop dusra task chala sakta hai