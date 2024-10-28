import os
from pprint import pprint

from dotenv import load_dotenv
import redis

from src.api import fetch_weather_api
from src.config import VISUAL_CROSSING_API_URL
from src.weather_cache import get_weather

load_dotenv()

api_key = os.getenv("VISUAL_CROSSING_API_KEY")




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
    
    pprint(get_weather("forecast", "Santa Monica", "us", api_key))

    # pprint(fetch_weather_api("forecast", "Baltimore", "us", api_key))


if __name__ == "__main__":
    main()
