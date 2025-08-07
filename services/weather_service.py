"""
Weather Service - Handles all weather-related business logic
"""
import os
import csv
from datetime import datetime
from core.api import WeatherAPI
from features.activity_suggester import ActivitySuggester
from models.weather_models import WeatherData


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
        if not city:
            raise ValueError("City name cannot be empty")
            
        try:
            data = self.api.fetch_weather(city, unit)
            if not data:
                raise Exception(f"No weather data received for '{city}'")

            # Extract basic weather data
            desc = data["weather"][0]["description"].capitalize()
            temp = float(data["main"]["temp"])
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            
            # Extract additional fields with safe defaults
            visibility = data.get("visibility", 10000)
            cloudiness = data.get("clouds", {}).get("all", 0)
            pressure = data.get("main", {}).get("pressure", 1013)
            feels_like = data.get("main", {}).get("feels_like", temp)
            wind_direction = data.get("wind", {}).get("deg", 0)
            sunrise = data.get("sys", {}).get("sunrise", 0)
            sunset = data.get("sys", {}).get("sunset", 0)
            rain_1h = data.get("rain", {}).get("1h", 0)
            rain_3h = data.get("rain", {}).get("3h", 0)
            snow_1h = data.get("snow", {}).get("1h", 0)
            snow_3h = data.get("snow", {}).get("3h", 0)
            
            return WeatherData(
                temperature=temp,
                description=desc,
                humidity=humidity,
                wind_speed=wind_speed,
                unit=unit,
                city=city,
                visibility=visibility,
                cloudiness=cloudiness,
                pressure=pressure,
                feels_like=feels_like,
                wind_direction=wind_direction,
                sunrise=sunrise,
                sunset=sunset,
                rain_1h=rain_1h,
                rain_3h=rain_3h,
                snow_1h=snow_1h,
                snow_3h=snow_3h
            )
        except Exception as e:
            raise Exception(f"Failed to get weather data for '{city}': {str(e)}")
            
    def get_historical_data(self, city, time_range):
        """Get historical weather data for analytics
        
        Args:
            city (str): City name
            time_range (str): Time range ("7 days", "30 days", "90 days", "1 year")
            
        Returns:
            dict: Historical weather data with timestamps and various metrics
        """
        try:
            # For demo/development, generate sample data
            # In production, this would fetch from API or database
            import numpy as np
            from datetime import datetime, timedelta
            
            # Convert time range to number of days
            days_map = {
                "7 days": 7,
                "30 days": 30,
                "90 days": 90,
                "1 year": 365
            }
            days = days_map.get(time_range, 7)
            
            # Generate timestamps
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            timestamps = [start_date + timedelta(hours=i) for i in range(days * 24)]
            
            # Generate sample data with realistic patterns
            base_temp = 20  # Base temperature
            temp_range = 10  # Temperature variation range
            
            # Temperature with daily and seasonal patterns
            hours = np.arange(len(timestamps))
            daily_pattern = 5 * np.sin(2 * np.pi * hours / 24)  # Daily temperature cycle
            seasonal_pattern = 10 * np.sin(2 * np.pi * hours / (365 * 24))  # Seasonal pattern
            random_variation = np.random.normal(0, 2, len(timestamps))  # Random variations
            
            temperatures = base_temp + daily_pattern + seasonal_pattern + random_variation
            
            # Generate other weather metrics
            humidity = 60 + 20 * np.sin(2 * np.pi * hours / 24) + np.random.normal(0, 5, len(timestamps))
            humidity = np.clip(humidity, 0, 100)  # Keep between 0-100%
            
            wind_speeds = 5 + 5 * np.random.random(len(timestamps))
            wind_directions = np.random.randint(0, 360, len(timestamps))
            
            precipitation = np.random.exponential(1, len(timestamps)) * (np.random.random(len(timestamps)) > 0.7)
            
            # Calculate daily aggregates
            dates = [ts.date() for ts in timestamps]
            unique_dates = sorted(list(set(dates)))
            daily_precip = []
            daylight_hours = []
            
            for date in unique_dates:
                # Daily precipitation sum
                daily_precip.append(sum(precipitation[i] for i, ts in enumerate(timestamps) if ts.date() == date))
                
                # Simulate daylight hours with seasonal variation
                day_of_year = date.timetuple().tm_yday
                daylight = 12 + 4 * np.sin(2 * np.pi * (day_of_year - 172) / 365)  # Peak at summer solstice
                daylight_hours.append(daylight)
            
            return {
                'timestamps': timestamps,
                'dates': unique_dates,
                'temperatures': temperatures,
                'humidity': humidity,
                'wind_speeds': wind_speeds,
                'wind_directions': wind_directions,
                'precipitation': daily_precip,
                'daylight_hours': daylight_hours
            }
            
        except Exception as e:
            print(f"Error generating historical data: {str(e)}")
            return None
        
        # Save basic weather data (keeping existing format for CSV compatibility)
        self.save_weather(city, temp, desc, unit, humidity, wind_speed)
        
        # Create a result object that supports attribute access
        class WeatherResult:
            pass
        
        result = WeatherResult()
        result.temperature = temp
        result.description = desc
        result.humidity = humidity
        result.wind_speed = wind_speed
        result.unit = unit
        result.visibility = visibility
        result.cloudiness = cloudiness
        result.pressure = pressure
        result.feels_like = feels_like
        result.wind_direction = wind_direction
        result.sunrise = sunrise
        result.sunset = sunset
        result.rain_1h = rain_1h
        result.rain_3h = rain_3h
        result.snow_1h = snow_1h
        result.snow_3h = snow_3h
        
        return result

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
