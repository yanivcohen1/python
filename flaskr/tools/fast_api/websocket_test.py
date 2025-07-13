import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    app.state.loop = asyncio.get_event_loop()
    yield
    # Shutdown code (if needed)

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="./flaskr/tools/fast_api/templates")
websockets = {}  # Maps user_id to websocket
user_queues = {}  # Maps user_id to asyncio.Queue

# def compute_max_workers(multiplier: float = 1.0) -> int:
#     cpu_count = os.cpu_count() or 1
#     return max(1, int(cpu_count * multiplier))

# # e.g. 5 threads per core for background I/O tasks
# executor = ThreadPoolExecutor(max_workers=compute_max_workers(5.0))

@app.get("/send_message_sync")
def call_async_send_message_from_none_async_in_concurncy_way(user_id: str, msg: str):
    # Use the main loop to run the coroutine thread-safely
    future = asyncio.run_coroutine_threadsafe(send_message(user_id, msg), app.state.loop)
    result = future.result()  # This blocks until result is ready
    return result

@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    websockets[user_id] = websocket
    user_queues[user_id] = asyncio.Queue()
    try:
        while True:
            data = await websocket.receive_text()
            # Put the received data into the user's queue
            await user_queues[user_id].put(data)
            # await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print(f"Client {user_id} disconnected")
        websockets.pop(user_id, None)
        user_queues.pop(user_id, None)

@app.get("/send_message")
async def send_message(user_id: str, msg: str = "Hello from FastAPI!"):
    websocket: WebSocket = websockets.get(user_id)
    queue: asyncio.Queue = user_queues.get(user_id)
    if websocket and queue:
        await websocket.send_text(msg)
        try:
            # Wait for the next message from the client (with a timeout)
            response = await asyncio.wait_for(queue.get(), timeout=10)
            # print(f"Received response from {user_id}: {response}")
            return {"message": f"Sent '{msg}' to {user_id}, received: {response}"}
        except asyncio.TimeoutError:
            return {"error": f"No response from client {user_id} within timeout"}
    else:
        return {"error": f"No WebSocket client connected for user_id {user_id}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=7000) # host="0.0.0.0"
