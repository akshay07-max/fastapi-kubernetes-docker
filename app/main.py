from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from app.dummy_data import dummy_data

app = FastAPI()

@app.get("/")
def root():
    return {
            "message": "app started successfully"
            }


@app.get("/data")
def get_dummy_data():
    return dummy_data

@app.get("/data/{id}")
def get_user(id: int):
    try:
        for data in dummy_data:
            if data["id"] == id:
                return data
            
        raise HTTPException(status_code=404, detail="User Not Found")
            
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=str(e))
    


                


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
    await manager.connect(websocket)

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

