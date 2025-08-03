import os
import json
from typing import Any, Dict, Optional

class JSONDataService:
    """
    Service for loading weather and related data from local JSON files.
    """
    def __init__(self, data_dir: str = "data/json_exports"):
        self.data_dir = data_dir
        # Always load team_cities.json if it exists
        self._team_cities_path = os.path.join(self.data_dir, "team_cities.json")
        self._team_cities_data = None
        if os.path.exists(self._team_cities_path):
            with open(self._team_cities_path, "r", encoding="utf-8") as f:
                self._team_cities_data = json.load(f)

    def _load_json(self, filename: str) -> Optional[Dict[str, Any]]:
        path = os.path.join(self.data_dir, filename)
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_weather_data(self, city: str) -> Optional[Dict[str, Any]]:
        # Use team_cities.json if loaded
        if self._team_cities_data and "cities_analysis" in self._team_cities_data:
            city_data = self._team_cities_data["cities_analysis"]["city_data"].get(city)
            if city_data:
                # Flatten city_data to match expected weather_data structure
                return {
                    "temperature": city_data.get("temperature", {}).get("avg"),
                    "description": ", ".join(city_data.get("weather_conditions", [])),
                    "humidity": city_data.get("humidity", {}).get("avg"),
                    "wind_speed": city_data.get("wind", {}).get("avg"),
                    "unit": "metric",
                    "city": city,
                    "visibility": None,
                    "cloudiness": None,
                    "pressure": None,
                    "feels_like": city_data.get("temperature", {}).get("avg"),
                    "wind_direction": None,
                    "sunrise": None,
                    "sunset": None,
                    "rain_1h": None,
                    "rain_3h": None,
                    "snow_1h": None,
                    "snow_3h": None
                }
        # Fallback to old per-city file
        filename = f"{city.lower().replace(' ', '_')}_weather.json"
        return self._load_json(filename)

    def get_forecast_data(self, city: str) -> Optional[Dict[str, Any]]:
        filename = f"{city.lower().replace(' ', '_')}_forecast.json"
        return self._load_json(filename)

    # Add more methods as needed for other data types
