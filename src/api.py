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

    try:
        response = requests.get(base_url, params)
        response.raise_for_status() # raises an error  for 4xx/5xx responses
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Failed to connect to the API. Check your network connection.")
    except requests.exceptions.Timeout:
        raise TimeoutError("The request timed out. Try again later.")
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 400:
            raise ValueError("Invalid parameters were provided to the API.") from http_err
        elif response.status_code == 401:
            raise PermissionError("Invalid API key.") from http_err
        else:
            raise RuntimeError(f"HTTP error occured: {response.status_code}") from http_err
    except requests.exceptions.RequestException as e:
        raise RuntimeError("An unexpected error occurred with the request.") from e
    
    return response.json()
