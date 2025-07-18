"""
Forecast Service - Handles weather forecast functionality
"""
import requests
from features.five_day_forecast import FiveDayForecaster


class ForecastService:
    """Service for weather forecasts"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.five_day_forecaster = FiveDayForecaster(api_key)

    def get_forecast(self, city, unit="metric", limit=5):
        """Get basic weather forecast"""
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": unit
        }
        
        resp = requests.get(url, params=params)
        if resp.status_code != 200:
            try:
                message = resp.json().get("message", "Failed to fetch forecast")
            except Exception:
                message = "Failed to fetch forecast"
            raise Exception(message)
        
        data = resp.json()
        forecasts = []
        for item in data.get("list", [])[:limit]:
            dt_txt = item["dt_txt"]
            desc = item["weather"][0]["description"].capitalize()
            temp = item["main"]["temp"]
            forecasts.append(f"{dt_txt}: {desc}, {temp}°")
        
        return "\n".join(forecasts)

    def get_five_day_forecast(self, city, unit="metric"):
        """Get detailed 5-day forecast"""
        return self.five_day_forecaster.fetch_5day_forecast(city, unit)
