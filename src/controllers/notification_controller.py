from fastapi import WebSocket
from services.notification_service import NotificationService

class NotificationController:
    def __init__(self):
        self.notification_service = NotificationService()

    async def notify_patient_file_load_complete(self, websocket: WebSocket): 
        """
            WebSocket endpoint for real-time communication.

            - **Websocket**: The WebSocket connection instance.
        """
        await self.notification_service.notify_patient_file_load_complete(websocket)
