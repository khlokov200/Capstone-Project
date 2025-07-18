"""
Weather Service - Handles all weather-related business logic
"""
import os
import csv
from datetime import datetime
from core.api import WeatherAPI
from features.activity_suggester import ActivitySuggester


class WeatherService:
    """Main weather service handling current weather and data persistence"""
    
    def __init__(self, api_key, log_file="data/weather_log.csv"):
        if not api_key:
            raise ValueError("Missing WEATHER_API_KEY")
        
        self.api = WeatherAPI(api_key)
        self.activity_suggester = ActivitySuggester()
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    def get_current_weather(self, city, unit="metric"):
        """Get current weather for a city"""
        data = self.api.fetch_weather(city, unit)
        if not data:
            raise Exception("Failed to fetch weather")
        
        desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        
        self.save_weather(city, temp, desc, unit, humidity, wind_speed)
        return {
            'temperature': temp,
            'description': desc,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'unit': unit
        }

    def save_weather(self, city, temp, desc, unit=None, humidity=None, wind_speed=None):
        """Save weather data to CSV log"""
        file_exists = os.path.isfile(self.log_file)
        with open(self.log_file, "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["DateTime", "City", "Temperature", "Description", "Unit", "Humidity", "WindSpeed"])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                city, temp, desc, unit, humidity, wind_speed
            ])

    def load_weather_history(self, limit=7):
        """Load recent weather history from CSV"""
        if not os.path.exists(self.log_file):
            return [], []
        
        with open(self.log_file, "r") as file:
            reader = list(csv.DictReader(file))
            if not reader:
                return [], []
            
            recent = reader[-limit:]
            
            # Handle different CSV formats (old vs new)
            dates = []
            temps = []
            
            for row in recent:
                # Try different possible column names
                date_value = None
                temp_value = None
                
                # Date column variants
                for date_col in ["DateTime", "DateTime           "]:  # Handle spaces
                    if date_col in row and row[date_col]:
                        date_value = row[date_col].strip()
                        break
                
                # Temperature column variants  
                for temp_col in ["Temperature", " Temperature"]:  # Handle spaces
                    if temp_col in row and row[temp_col]:
                        try:
                            temp_value = float(row[temp_col].strip())
                            break
                        except (ValueError, TypeError):
                            continue
                
                if date_value and temp_value is not None:
                    dates.append(date_value)
                    temps.append(temp_value)
            
            return dates, temps

    def suggest_activity(self, description):
        """Get activity suggestion based on weather description"""
        if not description:
            return None
        return self.activity_suggester.suggest(description)
