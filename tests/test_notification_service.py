import pytest
from unittest.mock import patch, MagicMock
from services.notification_service import NotificationService

@pytest.fixture
def websocket_service():
    return NotificationService()

def test_connect_positive(websocket_service):
    with patch('src.services.websocket_service.WebSocketClient') as MockWebSocketClient:
        mock_client = MockWebSocketClient.return_value
        mock_client.connect.return_value = True
        result = websocket_service.connect("ws://example.com")
        assert result is True

def test_connect_negative(websocket_service):
    with patch('src.services.websocket_service.WebSocketClient') as MockWebSocketClient:
        mock_client = MockWebSocketClient.return_value
        mock_client.connect.side_effect = Exception("Connection failed")
        result = websocket_service.connect("ws://example.com")
        assert result is False

def test_send_message_positive(websocket_service):
    with patch('src.services.websocket_service.WebSocketClient') as MockWebSocketClient:
        mock_client = MockWebSocketClient.return_value
        mock_client.send.return_value = True
        result = websocket_service.send_message("Hello")
        assert result is True

def test_send_message_negative(websocket_service):
    with patch('src.services.websocket_service.WebSocketClient') as MockWebSocketClient:
        mock_client = MockWebSocketClient.return_value
        mock_client.send.side_effect = Exception("Send failed")
        result = websocket_service.send_message("Hello")
        assert result is False