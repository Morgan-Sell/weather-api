import json
from dataclasses import dataclass

import redis

from src.api import fetch_weather_api
from src.config import REDIS_STORAGE_DURATION
from src.operations import extract_date, extract_time

# Connect to Redis
try:
    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    print("Connected to Redis successfully.")
except Exception as e:
    print(f"Error connecting to Redis: {e}")


def check_if_cache_key_exists(cache_key: str) -> bool:
    try:
        return redis_client.exists(cache_key) == 1
    except Exception as e:
        print(f"Error checking if cach key exists in Redis: {e}")
        return False


def get_from_cache(cache_key: str) -> dict:
    try:
        cached_data = redis_client.get(cache_key)
        return json.loads(cached_data)
    except Exception as e:
        print(f"Error retrieving data from cache: {e}")
        return None


@dataclass
class WeatherData:
    city: str
    address: str
    date_str: str
    temperature: float
    icon: str
    sunrise: str
    sunset: str
    humidity: float
    visibility: float
    precipitation: float

    def to_json(self) -> str:
        """Convert data class to JSON string for Redis storage."""
        return json.dumps(self.__dict__)

    def to_dict(self) -> dict:
        """Convert data class to a dictionary."""
        return self.__dict__


def extract_relevant_data(data: dict, location: str) -> WeatherData:
    current_conditions = data["locations"][location]["currentConditions"]

    weather_data = WeatherData(
        city=location,
        address=data["locations"][location]["address"],
        date_str=extract_date(current_conditions.get("datetime")),
        temperature=current_conditions.get("temp"),
        icon=current_conditions.get("icon"),
        sunrise=extract_time(current_conditions.get("sunrise")),
        sunset=extract_time(current_conditions.get("sunset")),
        humidity=current_conditions.get("humidity"),
        visibility=current_conditions.get("visibility"),
        precipitation=current_conditions.get("precip"),
    )

    return weather_data


def save_data_in_cache(cache_key: str, data: dict) -> None:
    redis_client.setex(cache_key, REDIS_STORAGE_DURATION, json.dumps(data))
