from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from dummy_data import dummy_data

app = FastAPI()

@app.get("/")
def root():
    return {
            "message": "app started successfully"
            }


@app.get("/data")
def get_dummy_data():
    return dummy_data

# websocket 

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# websocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket:WebSocket):
    await manager.connect()

    try:
        #send initial summy data
        for message in dummy_data:
            await websocket.send_json(message)

        while True:
            data = await websocket.receive_text()
            response = f"Client says: {data}"
            
            # Broadcast to all clients
            await manager.broadcast(response)

    except WebSocketDisconnect:
        manager.disconnect(websocket)

