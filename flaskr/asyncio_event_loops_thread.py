import asyncio
import threading
from asyncio import AbstractEventLoop

# Shared queue between the loops (only main loop should interact with it directly)
shared_queue = asyncio.Queue()

def call_async_send_message_from_none_async_in_concurncy_way(n: int, main_loop: AbstractEventLoop):
    # run event fun (coroutine fun) that run in main_loop from thread
    future = asyncio.run_coroutine_threadsafe(loop2(n), main_loop)
    try: result = future.result(timeout=10)
    except: result = None
    return result

def run_stream_loop2_in_thread(n: int, main_loop: AbstractEventLoop):
    msg = call_async_send_message_from_none_async_in_concurncy_way(n, main_loop)
    # thread safe put in queue for main_loop
    main_loop.call_soon_threadsafe(shared_queue.put_nowait, msg)
    main_loop.call_soon_threadsafe(shared_queue.put_nowait, None)

# Producer function running in its own event loop/thread
async def loop2(n):
    # get current event loop (coroutine loop)
    loop2_loop = asyncio.get_running_loop()
    print(f"loop2 is using loop: {id(loop2_loop)}")

    for i in range(n):
        await asyncio.sleep(0.5)
        print(f"loop2: yielding {i}")
    return "Done"

# Consumer function (main loop)
async def loop1():
    # get current event loop (coroutine loop)
    main_loop = asyncio.get_running_loop()
    print(f"loop1 is using loop: {id(main_loop)}")

    # Start producer in a separate thread with its own loop
    t = threading.Thread(target=run_stream_loop2_in_thread, args=(3, main_loop))
    t.start()

    while True:
        item = await shared_queue.get()
        if item is None:
            break
        print(f"loop1: received {item}")
        yield item

    t.join()
    print("loop1: done")

async def main():
    for i in range(2):
        print(f"\nmain: starting itteration {i+1}")
        async for chank in loop1():
            print(f"main: received {chank}")

if __name__ == "__main__":
    asyncio.run(main())
