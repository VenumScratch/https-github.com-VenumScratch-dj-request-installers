import asyncio
import json
import random
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

clients = set()

async def generate_fake_stats():
    while True:
        data = {
            "users": random.randint(10, 100),
            "requests": random.randint(100, 1000),
            "views": random.randint(500, 5000),
            "likes": random.randint(0, 500),
        }
        message = json.dumps(data)
        for client in clients:
            await client.send_text(message)
        await asyncio.sleep(2)

@app.websocket("/ws/stats/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        clients.remove(websocket)

@app.on_event("startup")
async def start_fake_data():
    asyncio.create_task(generate_fake_stats())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
