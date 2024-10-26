import json
import urllib
from pprint import pprint
from unittest.mock import MagicMock, patch

import pytest
import requests

from src.api import fetch_weather_api
from src.config import VISUAL_CROSSING_API_URL


@patch("requests.get")
def test_fetch_weather_api_success(mock_urlopen, weather_api_data):
    # Arrange: mock a successful response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = weather_api_data
    mock_urlopen.return_value = mock_response

    endpoint = "forecast"
    location = "Santa Monica"
    unit = "us"
    api_key = "secret"

    # Act
    data = fetch_weather_api(endpoint, location, unit, api_key)

    # Assert
    assert isinstance(data, dict)
    assert location in data["locations"]
    assert len(data["locations"][location]["values"]) == 3

    assert data["locations"][location]["currentConditions"]["temp"] == 61.8
    assert data["locations"][location]["values"][0]["conditions"] == "Overcast"


@patch("requests.get")
def test_fetch_weather_api_connection_error(mock_get):
    # Arrange: mock a failed response
    mock_get.side_effect = ConnectionError(
        "Failed to connect to the API. Check your network connection."
    )

    endpoint = "forecast"
    location = "Buenos Aires"
    unit = "metric"
    api_key = "secret"

    # Action & Assert
    with pytest.raises(ConnectionError):
        fetch_weather_api(endpoint, location, unit, api_key)


@patch("requests.get")
def test_fetch_weather_api_timeout_error(mock_get):
    # Arrange
    mock_get.side_effect = TimeoutError("The request timed out. Try again later.")
    endpoint = "forecast"
    location = "Buenos Aires"
    unit = "metric"
    api_key = "secret"

    # Action & Assert
    with pytest.raises(TimeoutError):
        fetch_weather_api(endpoint, location, unit, api_key)


@patch("requests.get")
def test_fetch_weather_api_400_error(mock_get):
    # Arrange
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.raise_for_status.side_effect = requests.HTTPError(
        "400 Client Error: Bad Request for url"
    )
    mock_get.return_value = mock_response

    endpoint = "forecast"
    location = "Invalid Location"
    unit = "metric"
    api_key = "secret"

    # Action & Assert
    with pytest.raises(
        ValueError, match="Invalid parameters were provided to the API."
    ):
        fetch_weather_api(endpoint, location, unit, api_key)


@patch("requests.get")
def test_fetch_weather_api_401_error(mock_get):
    # Arrange
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.raise_for_status.side_effect = requests.HTTPError(
        "401 Client Error: Invalid API key."
    )
    mock_get.return_value = mock_response

    endpoint = "forecast"
    location = "Capetown"
    unit = "metric"
    api_key = "invalid_key"

    # Action & Assert
    with pytest.raises(PermissionError, match="Invalid API key."):
        fetch_weather_api(endpoint, location, unit, api_key)


@patch("requests.get")
def test_fetch_weather_api_runtime_error(mock_get):
    # Arrange
    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.raise_for_status.side_effect = requests.HTTPError(
        "403 Client Error: Forbidden for url"
    )
    mock_get.return_value = mock_response

    endpoint = "forecast"
    location = "Capetown"
    unit = "metric"
    api_key = "secret"

    # Act & Assert
    with pytest.raises(RuntimeError, match="HTTP error occured: 403"):
        fetch_weather_api(endpoint, location, unit, api_key)


@patch("requests.get")
def test_fetch_weather_api_unexpected_request_error(mock_get):
    # Arrange
    mock_get.side_effect = requests.RequestException("A general request error occured.")

    endpoint = "forecast"
    location = "Capetown"
    unit = "metric"
    api_key = "secret"

    # Act & Assert
    with pytest.raises(
        RuntimeError, match="An unexpected error occurred with the request."
    ):
        fetch_weather_api(endpoint, location, unit, api_key)
