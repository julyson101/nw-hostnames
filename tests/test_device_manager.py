from unittest.mock import patch, MagicMock
from src.dev_hostname.device_manager import get_hostname


fake_device = {
    "device_type": "cisco_ios",
    "host": "1.1.1.1",
    "username": "admin",
    "password": "password"
}


@patch("src.dev_hostname.device_manager.ConnectHandler")
def test_get_hostname_success(mock_connect):
    mock_conn = MagicMock()
    mock_conn.send_command.return_value = "hostname TEST-RTR"

    mock_connect.return_value.__enter__.return_value = mock_conn

    result = get_hostname(fake_device)

    assert result == "TEST-RTR"


@patch("src.dev_hostname.device_manager.ConnectHandler")
def test_get_hostname_failure(mock_connect):
    mock_connect.side_effect = Exception("SSH failure")

    try:
        get_hostname(fake_device)
    except Exception as e:
        assert "connection failed" in str(e)

