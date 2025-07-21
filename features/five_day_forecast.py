import requests
import urllib3

# Disable SSL warnings for development
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class FiveDayForecaster:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_5day_forecast(self, city, unit="metric"):
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
                    # Show one forecast per day (at 12:00)
                    for item in data.get("list", []):
                        if "12:00:00" in item["dt_txt"]:
                            dt_txt = item["dt_txt"]
                            desc = item["weather"][0]["description"].capitalize()
                            temp = item["main"]["temp"]
                            unit_symbol = "°C" if unit == "metric" else "°F"
                            forecasts.append(f"{dt_txt}: {desc}, {temp}{unit_symbol}")
                    return "\n".join(forecasts)
                else:
                    try:
                        message = resp.json().get("message", "Failed to fetch 5-day forecast")
                    except Exception:
                        message = f"HTTP {resp.status_code}: Failed to fetch 5-day forecast"
                    raise Exception(message)
            except Exception as e:
                if i == len(methods) - 1:  # Last method
                    raise e
                else:
                    print(f"5-day forecast method {i+1} failed: {e}, trying next method...")
                    continue