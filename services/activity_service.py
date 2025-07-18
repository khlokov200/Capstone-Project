"""
Activity Service - Handles activity suggestions
"""
from .weather_service import WeatherService


class ActivityService:
    """Service for weather-based activity suggestions"""
    
    def __init__(self, weather_service: WeatherService):
        self.weather_service = weather_service

    def suggest(self, city, unit="metric"):
        """Get activity suggestion for a city based on weather"""
        weather = self.weather_service.get_current_weather(city, unit)
        return self.weather_service.suggest_activity(weather['description'])
