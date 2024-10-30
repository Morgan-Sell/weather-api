import json
from unittest.mock import MagicMock, patch

import pytest

from src.weather_cache import (
    WeatherData,
    check_if_cache_key_exists,
    extract_relevant_data,
    get_from_cache,
)


@patch("src.weather_cache.redis_client")
def test_check_if_cache_key_exists_key_exists(mock_redis_client):
    # Arrange
    mock_redis_client.exists.return_value = 1

    # Action
    result = check_if_cache_key_exists("existing_key")

    # Assert
    assert result is True
    mock_redis_client.exists.assert_called_once_with("existing_key")


@patch("src.weather_cache.redis_client")
def test_check_if_cache_key_exists_key_does_not_exists(mock_redis_client):
    # Arrange
    mock_redis_client.exists.return_value = 0

    # Act
    result = check_if_cache_key_exists("non_existing_key")

    # Action
    assert result is False
    mock_redis_client.exists.assert_called_once_with("non_existing_key")


@patch("src.weather_cache.redis_client")
def test_check_if_cache_key_exists_redis_error(mock_redis_client):
    # Arrange
    mock_redis_client.exists.side_effect = Exception("Redis error")

    # Action
    result = check_if_cache_key_exists("error_key")

    # Assert
    assert result is False
    mock_redis_client.exists.assert_called_once_with("error_key")


def test_weather_data_to_json():
    # Arrange: Create a WeatherData instance
    weather_data = WeatherData(
        location="Santa Monica",
        address="Santa Monica, CA, United States",
        date_str="2024-10-28",
        temperature=65.7,
        icon="sunny-rain",
        sunrise="2024-10-28T07:10:33-07:00",
        sunset="2024-10-28T18:04:26-07:00",
        humidity=73.3,
        visibility=9.9,
        precipitation=0.0,
    )

    # Act: Convert to JSON
    json_data = weather_data.to_json()

    # Assert: Check if the JSON data matches the expected dictionary
    expected_dict = {
        "location": "Santa Monica",
        "address": "Santa Monica, CA, United States",
        "date_str": "2024-10-28",
        "temperature": 65.7,
        "icon": "Sunny Rain",
        "sunrise": "2024-10-28T07:10:33-07:00",
        "sunset": "2024-10-28T18:04:26-07:00",
        "humidity": 73.3,
        "visibility": 9.9,
        "precipitation": 0.0,
    }
    assert json.loads(json_data) == expected_dict


def test_extract_relevant_data(weather_api_data):
    # Arrange
    sample_data = weather_api_data

    # Action
    result = extract_relevant_data(sample_data, "Santa Monica")

    # Assert: Check if the returned result is an instance of WeatherData
    assert isinstance(result, WeatherData)

    # Assert: Verify each attribute of the returned WeatherData object
    assert result.location == "Santa Monica"
    assert result.address == "Santa Monica, CA, United States"
    assert result.date_str == "2024-10-28"
    assert result.temperature == 65.7
    assert result.icon == "Sunny Rain"
    assert result.sunrise == "07:10:33"
    assert result.sunset == "18:04:26"
    assert result.humidity == 73.3
    assert result.visibility == 9.9
    assert result.precipitation == 0.0


@patch("src.weather_cache.redis_client")
def test_get_from_cach_existing_key(mock_redis_client):
    # Arrange: Set up mock to return JSON data
    mock_data = {"city": "Santa Monica", "temperature": 65.7}
    mock_redis_client.get.return_value = json.dumps(mock_data).encode('utf-8')

    # Act
    result = get_from_cache("existing_key")

    # Assert
    assert result == mock_data
    mock_redis_client.get.assert_called_once_with("existing_key")


@patch("src.weather_cache.redis_client")
def test_get_from_cache_non_existing_key(mock_redis_client):
    # Arrange: Set up the mock to return None for a non-existing key
    mock_redis_client.get.return_value = None

    # Act
    result = get_from_cache("non_existing_key")

    # Assert
    assert result is None
    mock_redis_client.get.assert_called_once_with("non_existing_key")


@patch("src.weather_cache.redis_client")
def test_get_from_cache_invalid_json(mock_redis_client):
    # Arrange
    mock_redis_client.get.return_value = b"invalid json"

    # Act
    result = get_from_cache("invalid_json_key")

    # Assert: Check if the function hands the JSON decoding error
    assert result is None
    mock_redis_client.get.assert_called_once_with("invalid_json_key")


@patch("src.weather_cache.redis_client")
def test_get_from_cache_redis_error(mock_redis_client):
    # Arrange
    mock_redis_client.get.side_effect = Exception("Redis error")

    # Act
    result = get_from_cache("error_key")

    # Assert
    assert result is None
    mock_redis_client.get.assert_called_once_with("error_key")