import os

import redis
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, url_for

from src.api import fetch_weather_api
from src.config import VISUAL_CROSSING_API_URL
from src.forms import LocationForm
from src.weather_cache import (
    check_if_cache_key_exists,
    extract_relevant_data,
    get_from_cache,
    save_data_in_cache,
)

app = Flask(__name__, static_folder="../static", template_folder="../templates")
app.config["SECRET_KEY"] = "super_secret_key"


load_dotenv()

api_key = os.getenv("VISUAL_CROSSING_API_KEY")

redis_client = redis.Redis(host="localhost", port=6379, db=0)


@app.route("/", methods=["GET", "POST"])
def index():
    form = LocationForm()

    if form.validate_on_submit():
        location = form.location.data
        print(f"Form submitted with city: {location}")
        return redirect(url_for("get_weather", location=location))
    return render_template("index.html", form=form)


@app.route("/weather/<location>", methods=["GET"])
def get_weather(location):
    cache_key = location.lower()

    # Decide whether to fetch data from Redis or API
    location_is_cached: bool = check_if_cache_key_exists(cache_key)

    if location_is_cached is True:
        print(f"Found data for {cache_key} in cache.")
        weather_data = get_from_cache(cache_key)

    else:
        print(f"No data found in cache for {cache_key}")
        print("Fetching data from weather API...")

        all_data = fetch_weather_api("forecast", location, "us", api_key)
        weather_data = extract_relevant_data(all_data, location)
        save_data_in_cache(cache_key, weather_data.to_dict())

        # Check if weather_data is None or incomplete
        if not weather_data:
            print("Error: No weather data found.")
            return "Error: No weather data found.", 500

    return render_template("results.html", weather_data=weather_data)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
