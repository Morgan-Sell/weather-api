import redis
import json

from src.api import fetch_weather_api
from src.config import REDIS_STORAGE_DURATION


# Connect to Redis
try:
    r = redis.Redis(host="localhost", port=6379, db=0)
    print("Connected to Redis successfully.")
except Exception as e:
    print(f"Error connecting to Redis: {e}")


def get_weather(endpoint: str, location: str, unit: str, api_key: str) -> dict:
    try:
        # Check if weather data is already in Redis
        cache_key = f"weather:{location.lower()}"
        cached_data = r.get(cache_key)

        if cached_data:
            # Data found in cache, return data after decoding
            weather_data = json.loads(cached_data)
            print("Retrieved from cache:", weather_data)
        
        else:
            # Data not in cache, fet it from the API
            print(f"No cached data found for {location}. Fetching from API...")
            weather_data = fetch_weather_api(endpoint, location, unit, api_key)
            if weather_data:
                # Store the fetched data in Redis for future requests
                print("Fetched from API and cached:", weather_data)
                r.setex(cache_key, REDIS_STORAGE_DURATION, json.dumps(weather_data))
            else:
                print(f"Could not fetch data for {location}.")
                return None

        return weather_data
    
    except Exception as e:
        print(f"An error occurred in get_weather: {e}")
        return None