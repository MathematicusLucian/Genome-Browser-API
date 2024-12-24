from dotenv import load_dotenv 
from fastapi import APIRouter, Depends, WebSocketDisconnect 
from fastapi.websockets import WebSocket
from fastapi.openapi.utils import get_openapi 
from controllers.notification_controller import NotificationController

load_dotenv()

notification_router = APIRouter()
notification_controller = NotificationController()

def custom_openapi():
    if notification_router.openapi_schema:
        return notification_router.openapi_schema
    openapi_schema = get_openapi(
        title="WebSocket API",
        version="1.0.0",
        description="This is the Genome Browser API for real-time notifications (employs WebSockets)",
        routes=notification_router.routes,
    )
    openapi_schema["paths"]["/ws"] = {
        "get": {
            "summary": "WebSocket connection",
            "description": "Connect to the WebSocket server. Send a message and receive a response.",
            "responses": {
                "101": {
                    "description": "Switching Protocols - The client is switching protocols as requested by the server.",
                }
            }
        }
    }
    notification_router.openapi_schema = openapi_schema
    return notification_router.openapi_schema

notification_router.openapi = custom_openapi
 
# Notify UI or log the completion of data loading activity

@notification_router.websocket("/notify_patient_file_load_complete")
async def notify_patient_file_load_complete(websocket: WebSocket): 
    """
        WebSocket endpoint for real-time communication.

        - **Websocket**: The WebSocket connection instance.
    """
    await notification_controller.notify_patient_file_load_complete(websocket)