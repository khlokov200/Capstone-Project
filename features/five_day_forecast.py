import requests

class FiveDayForecaster:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_5day_forecast(self, city):
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        resp = requests.get(url, params=params)
        if resp.status_code != 200:
            try:
                message = resp.json().get("message", "Failed to fetch 5-day forecast")
            except Exception:
                message = "Failed to fetch 5-day forecast"
            raise Exception(message)
        data = resp.json()
        forecasts = []
        # Show one forecast per day (at 12:00)
        for item in data.get("list", []):
            if "12:00:00" in item["dt_txt"]:
                dt_txt = item["dt_txt"]
                desc = item["weather"][0]["description"].capitalize()
                temp = item["main"]["temp"]
                forecasts.append(f"{dt_txt}: {desc}, {temp}°C")
        return "\n".join(forecasts)