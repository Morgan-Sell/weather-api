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

    pprint(get_weather("forecast", "Santa Monica", "us", api_key))

    # pprint(fetch_weather_api("forecast", "Baltimore", "us", api_key))


if __name__ == "__main__":
    main()
