"""
Poetry Service - Handles weather poetry generation
"""
from .weather_service import WeatherService


class PoetryService:
    """Service for generating weather-based poetry"""
    
    def __init__(self, weather_service: WeatherService):
        self.weather_service = weather_service

    def generate_poem(self, city, unit="metric"):
        """Generate a poem based on current weather"""
        weather = self.weather_service.get_current_weather(city, unit)
        temp, desc = weather['temperature'], weather['description']
        return f"{city} weather inspires:\n{desc}, {temp}°\nNature sings in every degree."
