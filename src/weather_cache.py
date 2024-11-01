import json
from dataclasses import dataclass

import redis

from src.config import REDIS_STORAGE_DURATION
from src.operations import extract_date, extract_time

# Connect to Redis
try:
    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    print("Connected to Redis successfully.")
except Exception as e:
    print(f"Error connecting to Redis: {e}")


def check_if_cache_key_exists(cache_key: str) -> bool:
    """
    Checks if a specified cache key exists in Redis.

    Args:
        cache_key (str): The key to check in the cache.

    Returns:
        bool: True if the cache key exists, False otherwise.
    """
    try:
        print(f"Looking for {cache_key} in cache")
        return redis_client.exists(cache_key) == 1
    except Exception as e:
        print(f"Error checking if cach key exists in Redis: {e}")
        return False


def get_from_cache(cache_key: str) -> dict:
    """
    Retrieves data from the cache for a given key.

    Args:
        cache_key (str): The cache key to retrieve data for.

    Returns:
        dict: The cached data if found, or None if an error occurs.
    """
    try:
        cached_data = redis_client.get(cache_key)
        return json.loads(cached_data)
    except Exception as e:
        print(f"Error retrieving data from cache: {e}")
        return None


@dataclass
class WeatherData:
    """
    Represents weather data for a specific location and date.

    Attributes:
        location (str): The name of the location.
        address (str): The full address of the location.
        date_str (str): Date of the weather data.
        temperature (float): Temperature in the specified unit.
        icon (str): Weather icon description.
        sunrise (str): Sunrise time.
        sunset (str): Sunset time.
        humidity (float): Humidity percentage.
        visibility (float): Visibility distance.
        precipitation (float): Precipitation amount.

    Methods:
        to_json() -> str: Converts the instance to a JSON string.
        to_dict() -> dict: Converts the instance to a dictionary.
    """

    location: str
    address: str
    date_str: str
    temperature: float
    icon: str
    sunrise: str
    sunset: str
    humidity: float
    visibility: float
    precipitation: float

    def __post_init__(self):
        self.icon = self.icon.replace("-", " ").title()

    def to_json(self) -> str:
        """Convert data class to JSON string for Redis storage."""
        return json.dumps(self.__dict__)

    def to_dict(self) -> dict:
        """Convert data class to a dictionary."""
        return self.__dict__


def extract_relevant_data(data: dict, location: str) -> WeatherData:
    """
    Extracts and maps relevant weather information for a given location.

    Args:
        data (dict): Raw weather data.
        location (str): The location for which to extract weather data.

    Returns:
        WeatherData: An instance containing structured weather data.
    """
    current_conditions = data["locations"][location]["currentConditions"]

    weather_data = WeatherData(
        location=location,
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
    """
    Saves data in the cache with an expiration time.

    Args:
        cache_key (str): The key under which to store the data.
        data (dict): The data to cache.
    """
    redis_client.setex(cache_key, REDIS_STORAGE_DURATION, json.dumps(data))
