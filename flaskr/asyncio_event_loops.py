import asyncio
import threading
from asyncio import AbstractEventLoop

# Shared queue between the loops (only main loop should interact with it directly)
shared_queue = asyncio.Queue()

# Producer function running in its own event loop/thread
async def loop2(n, main_loop: AbstractEventLoop):
    loop2_loop = asyncio.get_running_loop()
    print(f"loop2 is using loop: {id(loop2_loop)}")

    for i in range(n):
        await asyncio.sleep(0.5)
        print(f"loop2: yielding {i}")
        main_loop.call_soon_threadsafe(shared_queue.put_nowait, i)

    main_loop.call_soon_threadsafe(shared_queue.put_nowait, None)

def run_loop2_in_thread(n, main_loop):
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    new_loop.run_until_complete(loop2(n, main_loop))
    new_loop.close()

# Consumer function (main loop)
async def loop1():
    loop1_loop = asyncio.get_running_loop()
    print(f"loop1 is using loop: {id(loop1_loop)}")

    # Start producer in a separate thread with its own loop
    t = threading.Thread(target=run_loop2_in_thread, args=(3, loop1_loop))
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
    for _ in range(2):
        async for chank in loop1():
            print(f"main: received {chank}")

if __name__ == "__main__":
    asyncio.run(main())

# run async function in a different thread run in fastapi main loop (app.state.loop)
# future = asyncio.run_coroutine_threadsafe(send_message(user_id, msg), app.state.loop)
# result = future.result()  # This blocks until result is ready
