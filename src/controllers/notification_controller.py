from fastapi import APIRouter, WebSocket
from services.notification_service import NotificationService

router = APIRouter()
websocket_service = NotificationService()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket): 
    """
        WebSocket endpoint for real-time communication.

        - **Websocket**: The WebSocket connection instance.
    """
    await websocket_service.websocket_endpoint(websocket)
