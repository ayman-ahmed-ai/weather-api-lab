"""Lab Assignment 1: Working with a Public REST API using Python.

Fetches current weather from WeatherAPI.com, parses the JSON response,
stores it in a class, and prints a formatted summary.
"""
import os
import sys
from dataclasses import dataclass

import requests
from dotenv import load_dotenv

API_URL = "https://api.weatherapi.com/v1/current.json"
CITY = "Cairo"


@dataclass
class WeatherReport:
    """Stores and organizes the weather data retrieved from the API."""
    city: str
    country: str
    local_time: str
    condition: str
    temp_c: float
    feels_like_c: float
    humidity: int
    wind_kph: float

    @classmethod
    def from_json(cls, data: dict) -> "WeatherReport":
        """Build a WeatherReport from the parsed JSON response."""
        location = data["location"]
        current = data["current"]
        return cls(
            city=location["name"],
            country=location["country"],
            local_time=location["localtime"],
            condition=current["condition"]["text"],
            temp_c=current["temp_c"],
            feels_like_c=current["feelslike_c"],
            humidity=current["humidity"],
            wind_kph=current["wind_kph"],
        )

    def summary(self) -> str:
        """Return a clear, well-organized summary."""
        line = "=" * 40
        return (
            f"{line}\n"
            f"  Current Weather Report\n"
            f"{line}\n"
            f"Location    : {self.city}, {self.country}\n"
            f"Local time  : {self.local_time}\n"
            f"Condition   : {self.condition}\n"
            f"Temperature : {self.temp_c} °C\n"
            f"Feels like  : {self.feels_like_c} °C\n"
            f"Humidity    : {self.humidity} %\n"
            f"Wind speed  : {self.wind_kph} km/h\n"
            f"{line}"
        )


def fetch_weather(api_key: str, city: str) -> dict:
    """Call the REST API and return the parsed JSON response."""
    response = requests.get(
        API_URL,
        params={"key": api_key, "q": city, "aqi": "no"},
        timeout=10,
    )
    response.raise_for_status()  # raises an error for 4xx / 5xx
    return response.json()


def main() -> None:
    load_dotenv()  # loads variables from the .env file
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        sys.exit("Error: WEATHER_API_KEY is missing. Add it to your .env file.")

    try:
        data = fetch_weather(api_key, CITY)
    except requests.exceptions.HTTPError as err:
        sys.exit(f"HTTP error: {err}")
    except requests.exceptions.RequestException as err:
        sys.exit(f"Network error: {err}")

    report = WeatherReport.from_json(data)
    print(report.summary())


if __name__ == "__main__":
    main()
