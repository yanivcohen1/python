import asyncio
from datetime import datetime
import websockets

async def send_messages():
    uri = "ws://localhost:8766"  # Server 2's address
    async with websockets.connect(uri) as websocket:
        while True:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            await websocket.send(f"Server 1 time: {current_time}")
            msg = await websocket.recv()
            print(f"Server 2 says: {msg}")
            await asyncio.sleep(5)  # Wait for 5 seconds before sending the next message

async def main():
    await send_messages()

if __name__ == "__main__":
    asyncio.run(main())
