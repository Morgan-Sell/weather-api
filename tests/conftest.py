import pytest


@pytest.fixture(scope="function")
def weather_api_data():
    """Fixture that returns simplified mock data for weather API response."""
    return {
        "columns": {
            "address": {"id": "address", "name": "Address", "type": 1, "unit": None},
            "temp": {"id": "temp", "name": "Temperature", "type": 2, "unit": "degf"},
            "humidity": {
                "id": "humidity",
                "name": "Relative Humidity",
                "type": 2,
                "unit": None,
            },
            "conditions": {
                "id": "conditions",
                "name": "Conditions",
                "type": 1,
                "unit": None,
            },
            "datetime": {
                "id": "datetime",
                "name": "Date time",
                "type": 3,
                "unit": None,
            },
        },
        "locations": {
            "Santa Monica": {
                "address": "Santa Monica, CA, United States",
                "currentConditions": {
                    "temp": 61.8,
                    "humidity": 82.3,
                    "conditions": "Clear",
                    "datetime": "2024-10-26T10:35:00-07:00",
                },
                "values": [
                    {
                        "temp": 64.2,
                        "humidity": 89.5,
                        "conditions": "Overcast",
                        "datetimeStr": "2024-10-26T00:00:00-07:00",
                    },
                    {
                        "temp": 73.2,
                        "humidity": 67.3,
                        "conditions": "Sunny",
                        "datetimeStr": "2024-10-27T00:00:00-07:00",
                    },
                    {
                        "temp": 69.5,
                        "humidity": 78.8,
                        "conditions": "Windy",
                        "datetimeStr": "2024-10-28T00:00:00-07:00",
                    },
                ],
            }
        },
        "messages": None,
        "queryCost": 1,
        "remainingCost": 0,
    }
