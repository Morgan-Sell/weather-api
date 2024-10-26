import json
from unittest.mock import MagicMock, patch

import requests
from src.api import fetch_weather_api
import urllib

from src.config import VISUAL_CROSSING_API_URL

import pytest

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


@patch("urllib.request.urlopen")
def test_fetch_weather_api_connection_error(mock_urlopen):
    # Arrange: mock a failed response
    mock_urlopen.side_effect = ConnectionError("Failed to connect to the API. Check your network connection.")

    endpoint = "forecast"
    location = "Buenos Aires"
    unit = "metric"
    api_key = "secret"

    # Action & Assert
    with pytest.raises(ConnectionError):
        fetch_weather_api(endpoint, location, unit, api_key)