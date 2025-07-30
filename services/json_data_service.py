import os
import json
from typing import Any, Dict, Optional

class JSONDataService:
    """
    Service for loading weather and related data from local JSON files.
    """
    def __init__(self, data_dir: str = "data/json_exports"):
        self.data_dir = data_dir

    def _load_json(self, filename: str) -> Optional[Dict[str, Any]]:
        path = os.path.join(self.data_dir, filename)
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_weather_data(self, city: str) -> Optional[Dict[str, Any]]:
        filename = f"{city.lower().replace(' ', '_')}_weather.json"
        return self._load_json(filename)

    def get_forecast_data(self, city: str) -> Optional[Dict[str, Any]]:
        filename = f"{city.lower().replace(' ', '_')}_forecast.json"
        return self._load_json(filename)

    # Add more methods as needed for other data types
