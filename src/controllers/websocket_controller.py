from fastapi import APIRouter, WebSocket
from services.websocket_service import WebSocketService

router = APIRouter()
websocket_service = WebSocketService()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket): 
    """
        WebSocket endpoint for real-time communication.

        - **Websocket**: The WebSocket connection instance.
    """
    await websocket_service.websocket_endpoint(websocket)
