
import os
from pprint import pprint
from dotenv import load_dotenv

from src.api import fetch_weather_api
from src.config import VISUAL_CROSSING_API_URL



load_dotenv()

api_key = os.getenv("VISUAL_CROSSING_API_KEY")


def main():

    pprint(fetch_weather_api("forecast", "Santa Monica", "us", api_key))







if __name__ == "__main__":
    main()