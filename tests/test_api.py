import json
from unittest.mock import MagicMock, patch


from src.api import fetch_weather_api
import urllib



@patch("urllib.request.urlopen")
def test_fetch_weather_api_success(mock_urlopen, weather_api_data):
    # Arrange: mock a successful response
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps(weather_api_data).encode("utf-8")
    mock_urlopen.return_value = mock_response

    endpoint = "forecast"
    location = "Santa Monica"
    unit = "us"
    api_key = "secret"

    # Act
    data = fetch_weather_api(endpoint, location, unit, api_key)


    # Assert
    assert isinstance(data, dict)
    assert data["location"] == location
    assert len(data["location"]["values"]) == 3
