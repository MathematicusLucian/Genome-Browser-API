from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from controllers.notification_controller import router
from services.notification_service import NotificationService

client = TestClient(router)

@pytest.fixture
def mock_websocket_service():
    with patch('src.controllers.websocket_controller.NotificationService') as MockNotificationService:
        yield MockNotificationService.return_value

def test_connect_websocket_positive(mock_websocket_service):
    mock_websocket_service.connect.return_value = True
    response = client.post("/connect_websocket", json={"url": "ws://example.com"})
    assert response.status_code == 200
    assert response.json() == {"message": "Connected"}

def test_connect_websocket_negative(mock_websocket_service):
    mock_websocket_service.connect.return_value = False
    response = client.post("/connect_websocket", json={"url": "ws://example.com"})
    assert response.status_code == 500
    assert response.json() == {"message": "Connection failed"}

def test_send_message_positive(mock_websocket_service):
    mock_websocket_service.send_message.return_value = True
    response = client.post("/send_message", json={"message": "Hello"})
    assert response.status_code == 200
    assert response.json() == {"message": "Message sent"}

def test_send_message_negative(mock_websocket_service):
    mock_websocket_service.send_message.return_value = False
    response = client.post("/send_message", json={"message": "Hello"})
    assert response.status_code == 500
    assert response.json() == {"message": "Send failed"}