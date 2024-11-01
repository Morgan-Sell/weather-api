# Weather Application

A Python-based application that checks the weather for a specified location. It first checks a Redis cache for recent data. If the weather data is not cached, the application fetches the data from a third-party weather API and caches the data for future requests. This reduces API calls, speeds up responses, and supports a better user experience.

The application obtains data from [Visiual Crossing's API](https://www.visualcrossing.com/weather-api).

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the Repository**
   
   ```
   git clone https://github.com/Morgan-Sell/weather-api.git
   cd weather-api
   ```

2. **Environment Variables:** Set up a .env file in the root directory of the project with the following variable.
    
    ```
    API_KEY=<your_weather_api_key>

    ```

3. **Run Initial Setup:** Use the provided run.sh script for setting up your environment.

    ```

    ```
