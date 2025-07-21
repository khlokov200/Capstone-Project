"""
Forecast Service - Handles weather forecast functionality
"""
import requests
import ssl
import urllib3
from features.five_day_forecast import FiveDayForecaster

# Disable SSL warnings for development
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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
        
        # Try multiple methods to handle SSL issues
        methods = [
            lambda: requests.get(url, params=params, timeout=30),
            lambda: requests.get(url, params=params, timeout=30, verify=False),
            lambda: requests.get(url.replace("https://", "http://"), params=params, timeout=30)
        ]
        
        for i, method in enumerate(methods):
            try:
                resp = method()
                if resp.status_code == 200:
                    data = resp.json()
                    forecasts = []
                    for item in data.get("list", [])[:limit]:
                        dt_txt = item["dt_txt"]
                        desc = item["weather"][0]["description"].capitalize()
                        temp = item["main"]["temp"]
                        forecasts.append(f"{dt_txt}: {desc}, {temp}°")
                    return "\n".join(forecasts)
                else:
                    try:
                        message = resp.json().get("message", "Failed to fetch forecast")
                    except Exception:
                        message = f"HTTP {resp.status_code}: Failed to fetch forecast"
                    raise Exception(message)
            except Exception as e:
                if i == len(methods) - 1:  # Last method
                    raise e
                else:
                    print(f"Forecast method {i+1} failed: {e}, trying next method...")
                    continue

    def get_five_day_forecast(self, city, unit="metric"):
        """Get detailed 5-day forecast"""
        return self.five_day_forecaster.fetch_5day_forecast(city, unit)
