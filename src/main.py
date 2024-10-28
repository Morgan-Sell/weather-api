import json
import os
from pprint import pprint

import redis
from dotenv import load_dotenv

from src.api import fetch_weather_api
from src.config import VISUAL_CROSSING_API_URL
from src.weather_cache import (
    check_if_cache_key_exists,
    extract_relevant_data,
    get_from_cache,
    save_data_in_cache,
)

load_dotenv()

api_key = os.getenv("VISUAL_CROSSING_API_KEY")

redis_client = redis.Redis(host="localhost", port=6379, db=0)


def main():
    """
    STEPS:
        1. User inputs location
        2. Check if location is in Redis
        3.

            a. If location is in Redis:
                i. Retrieve data from Redis.

            b. If location is NOT in Redis:
                i. Fetch data from API.
                ii. Extract the necessary data from JSON into a WeatherData
                iii. Save WeatherData to Redis. The city will be lower case.
            d.

    """

    # User input
    location = "Buenos Aires"
    cache_key = location.lower()

    # Decide whether to fetch data from Redis or API
    location_is_cached: bool = check_if_cache_key_exists(cache_key)

    if location_is_cached is True:
        print(f"Found data for {cache_key} in cache.")
        weather_results = get_from_cache(cache_key)

    else:
        print(f"No data found in cache for {cache_key}")
        print("Fetching data from weather API...")

        data = fetch_weather_api("forecast", location, "us", api_key)
        weather_results = extract_relevant_data(data, location)
        save_data_in_cache(cache_key, weather_results.to_dict())

        with open("weather.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

    # pprint(fetch_weather_api("forecast", "Baltimore", "us", api_key))


if __name__ == "__main__":
    main()
