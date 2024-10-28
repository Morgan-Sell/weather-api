import pytest


@pytest.fixture(scope="function")
def weather_api_data():
    """Fixture that returns simplified mock data for weather API response."""
    return {
        "locations": {
            "Santa Monica": {
                "id": "Santa Monica",
                "address": "Santa Monica, CA, United States",
                "name": "Santa Monica",
                "index": 0,
                "latitude": 34.0116,
                "longitude": -118.492,
                "distance": 0.0,
                "time": 0.0,
                "tz": "America/Los_Angeles",
                "currentConditions": {
                    "wdir": 191.0,
                    "temp": 65.7,
                    "sunrise": "2024-10-28T07:10:33-07:00",
                    "visibility": 9.9,
                    "wspd": 6.6,
                    "icon": "cloudy",
                    "stations": "",
                    "heatindex": "null",
                    "cloudcover": 100.0,
                    "datetime": "2024-10-28T13:42:00-07:00",
                    "precip": 0.0,
                    "moonphase": 0.88,
                    "snowdepth": "null",
                    "sealevelpressure": 1012.0,
                    "dew": 56.9,
                    "sunset": "2024-10-28T18:04:26-07:00",
                    "humidity": 73.3,
                    "wgust": 8.9,
                    "windchill": "null"
                    }
                }
            }
        }