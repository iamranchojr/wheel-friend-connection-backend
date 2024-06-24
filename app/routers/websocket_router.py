from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect


router = APIRouter()


class WebsocketConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, path_params: dict):
        for connection in self.active_connections:
            if connection.path_params == path_params:
                await connection.send_text(message)


manager = WebsocketConnectionManager()


@router.websocket('/ws/{client_id}')
async def websocket_endpoint(
        websocket: WebSocket,
        client_id: int,
):
   await manager.connect(websocket)
   try:
       while True:
           data = await websocket.receive_text()
           await manager.send_personal_message(data, websocket)
           await manager.broadcast(data, websocket.path_params)
   except WebSocketDisconnect:
       manager.disconnect(websocket)
