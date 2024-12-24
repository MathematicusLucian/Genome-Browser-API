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

    async def notify_ui(self, genome_file_name_with_path: str, patient_genome_df_size: str):
        websocket_url = "ws://localhost:8000/ws"
        async with WebSocket(websocket_url, headers=None, subprotocols=None) as websocket:
            await websocket.send_json({"event": "genome_loaded", "genome_file_name_with_path": genome_file_name_with_path, "Number of Rows": patient_genome_df_size})