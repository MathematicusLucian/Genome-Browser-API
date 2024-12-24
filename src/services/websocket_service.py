from fastapi.websockets import WebSocket, WebSocketDisconnect

class WebSocketService:
    async def websocket_endpoint(self, websocket: WebSocket): 
        await websocket.accept()
        try:
            while True:
                data = await websocket.receive_text()
                await websocket.send_text(f"Message received: {data}")
        except WebSocketDisconnect:
            print("WebSocket connection closed")
        except Exception as e:
            print(f"WebSocket connection closed: {e}")
