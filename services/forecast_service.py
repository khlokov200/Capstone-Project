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
                    
                    # Group forecasts by day
                    day_forecasts = {}
                    for item in data.get("list", []):
                        date = item["dt_txt"].split()[0]
                        if date not in day_forecasts:
                            day_forecasts[date] = {
                                'temps': [],
                                'humidity': [],
                                'conditions': []
                            }
                        day_forecasts[date]['temps'].append(item["main"]["temp"])
                        day_forecasts[date]['humidity'].append(item["main"]["humidity"])
                        day_forecasts[date]['conditions'].append(item["weather"][0]["description"])
                    
                    # Process daily data
                    for date, day_data in list(day_forecasts.items())[:5]:  # Limit to 5 days
                        avg_temp = sum(day_data['temps']) / len(day_data['temps'])
                        avg_humidity = sum(day_data['humidity']) / len(day_data['humidity'])
                        # Get most common condition
                        common_condition = max(set(day_data['conditions']), key=day_data['conditions'].count)
                        
                        forecasts.append({
                            'date': date,
                            'temp': round(avg_temp, 1),
                            'humidity': round(avg_humidity),
                            'conditions': common_condition.capitalize()
                        })
                    
                    return forecasts
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
