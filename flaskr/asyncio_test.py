import asyncio
import random

async def rnd_sleep(t):
    # sleep for T seconds on average
    await asyncio.sleep(t * random.random() * 2)


async def producer(queue: asyncio.Queue):
    while True:
        # produce a token and send it to a consumer
        token = random.random()
        if token < 0.4:
            print(f"produced-break {token}")
            break
        print(f"produced {token}")
        await queue.put(token)
        await rnd_sleep(0.1)


async def consumer(queue: asyncio.Queue):
    while True:
        token = await queue.get()
        # process the token received from a producer
        await rnd_sleep(0.3)
        print(f"consumed {token}")
        queue.task_done()  # for queue.join() wait for queue.empty() and queue.task_done()


async def main():
    queue = asyncio.Queue()

    # fire up the both producers and consumers in 3 instances
    producers = [asyncio.create_task(producer(queue)) for _ in range(3)]
    consumers = [asyncio.create_task(consumer(queue)) for _ in range(4)]

    # with both producers and consumers running, wait for
    # the producers to finish
    await asyncio.gather(*producers)
    print("---- done producing")

    # wait for the remaining tasks to be processed
    await queue.join()

    # cancel the consumers, which are now idle
    for c in consumers:
        c.cancel()


asyncio.run(main())
