from fastapi.websockets import WebSocket, WebSocketDisconnect

class NotificationService:
    async def notify_patient_file_load_complete(self, websocket: WebSocket): 
        await websocket.accept()
        try:
            while True:
                data = await websocket.receive_text()
                await websocket.send_text(f"Message received: {data}")
        except WebSocketDisconnect:
            print("WebSocket connection closed")
        except Exception as e:
            print(f"WebSocket connection closed: {e}")
