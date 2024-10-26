import requests

import json

from src.config import VISUAL_CROSSING_API_URL


#  Location is the address, partial address or latitude,longitude location for which to retrieve weather data. You can also use US ZIP Codes


def fetch_weather_api(endpoint: str, location: str, unit: str, api_key: str) -> dict:

    base_url = f"{VISUAL_CROSSING_API_URL}/{endpoint}"
    
    params = {
        "location": location,
        "aggregateHours": 24,
        "unitGroup": unit,
        "contentType": "json",
        "key": api_key
    }
    response = requests.get(base_url, params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to fetch data: ", response.status_code, response.text)