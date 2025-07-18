"""
Comparison Service - Handles city weather comparisons
"""
from .weather_service import WeatherService


class ComparisonService:
    """Service for comparing weather between cities"""
    
    def __init__(self, weather_service: WeatherService):
        self.weather_service = weather_service

    def compare_cities(self, city1, city2, unit="metric"):
        """Compare weather between two cities"""
        weather1 = self.weather_service.get_current_weather(city1, unit)
        weather2 = self.weather_service.get_current_weather(city2, unit)
        
        temp1, desc1 = weather1['temperature'], weather1['description']
        temp2, desc2 = weather2['temperature'], weather2['description']
        
        return f"{city1}: {temp1}°, {desc1}\n{city2}: {temp2}°, {desc2}"
