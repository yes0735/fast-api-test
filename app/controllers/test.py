# -*- coding: utf-8 -*-


from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from app.common.route import BaseRoute


router = APIRouter(route_class=BaseRoute)
configurations = {
    "swagger": {
        "tags": ["web socket chat API"],
        "tags_metadata": {
            "name": "web socket chat API",
            "description": "web socket chat",
        },
    },
}


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <label>client ID: <input type="text" id="clientId" autocomplete="off" value=""/></label>
        <label>room name: <input type="text" id="room_name" autocomplete="off" value="some-key-token"/></label>
        <button onclick="connect(event)">Connect</button>
        <button onclick="disconnect(event)">Disconnect</button>
        <hr>
        <form action="" onsubmit="sendMessage(event)">
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = null;
            function connect(event) {
                var clientId = document.getElementById("clientId")
                var room_name = document.getElementById("room_name")

                ws = new WebSocket("ws://localhost:8000/ws/" + room_name.value + "/"  + clientId.value);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
            function disconnect(event) {
                ws.close();
                window.location = '/chat'
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[WebSocket] = {}

    async def connect(self, message: str, room_name: str, websocket: WebSocket):
        await websocket.accept()
        await websocket.send_text(message)

        if room_name not in self.active_connections:
            self.active_connections[room_name] = []

        self.active_connections[room_name].append(websocket)

    def disconnect(self, room_name: int, websocket: WebSocket):
        self.active_connections[room_name].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, room_name: int, message: str):
        for connection in self.active_connections[room_name]:
            await connection.send_text(message)


manager = ConnectionManager()


@router.get("/chat")
async def get():
    return HTMLResponse(html)


@router.websocket("/ws/{room_name}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, room_name: str, client_id: str):
    await manager.connect(f"connect...room_name: {room_name}", room_name, websocket)
    await manager.broadcast(room_name, f"Client : #{client_id} / Room : #{room_name} 입장")

    try:
        while True:
            data = await websocket.receive_text()

            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(room_name, f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(room_name, websocket)
        await manager.broadcast(room_name, f"Client #{client_id} left the chat")
