# start this first and then run ws_server1
# pip install websockets
import asyncio
from datetime import datetime
import websockets

async def echo(websocket, path):
    while True:
        message = await websocket.recv()
        print(f"Server 1 says: {message}")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        await websocket.send(f"Server 2 time: {current_time}")

async def main():
    server = await websockets.serve(echo, "localhost", 8766)
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
