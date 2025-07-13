import asyncio
import time

def blocking_function():
    time.sleep(3)
    return time.time()

async def unblock_function():
    return await asyncio.to_thread(blocking_function)

async def main():
    print("Starting blocking function")
    start1 = time.time()
    end1 = await unblock_function()
    results = await asyncio.gather(unblock_function(), unblock_function())
    end2 = time.time()
    print(f'run 1 fun took {end1-start1:.2f} seconds')
    print(f'run 2 funs took {end2-end1:.2f} seconds')

asyncio.run(main())
