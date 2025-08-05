"""
Comparison Service - Handles city weather comparisons
"""
from .weather_service import WeatherService


class ComparisonService:
    """Service for comparing weather between cities"""
    
    def __init__(self, weather_service: WeatherService):
        self.weather_service = weather_service

    def compare_cities(self, city1, city2, unit="metric"):
        """Compare weather between two cities with detailed metrics"""
        try:
            weather1 = self.weather_service.get_current_weather(city1, unit)
            weather2 = self.weather_service.get_current_weather(city2, unit)
            
            # Build comparison text
            comparison = f"Weather Comparison: {city1} vs {city2}\n"
            comparison += "=" * 40 + "\n\n"
            
            # Add conditions
            comparison += f"{city1}: {weather1.description}\n"
            comparison += f"{city2}: {weather2.description}\n\n"
            
            # Compare temperature
            comparison += f"Temperature:\n"
            comparison += f"{city1}: {weather1.formatted_temperature}\n"
            comparison += f"{city2}: {weather2.formatted_temperature}\n"
            temp_diff = weather1.temperature - weather2.temperature
            comparison += f"Difference: {abs(temp_diff):.1f}° "
            comparison += f"({'higher' if temp_diff > 0 else 'lower'} in {city1})\n\n"
            
            # Compare humidity
            comparison += f"Humidity:\n"
            comparison += f"{city1}: {weather1.humidity}%\n"
            comparison += f"{city2}: {weather2.humidity}%\n"
            hum_diff = weather1.humidity - weather2.humidity
            comparison += f"Difference: {abs(hum_diff)}% "
            comparison += f"({'higher' if hum_diff > 0 else 'lower'} in {city1})\n\n"
            
            # Compare wind
            comparison += f"Wind:\n"
            comparison += f"{city1}: {weather1.formatted_wind}\n"
            comparison += f"{city2}: {weather2.formatted_wind}\n"
            wind_diff = weather1.wind_speed - weather2.wind_speed
            comparison += f"Difference: {abs(wind_diff):.1f} m/s "
            comparison += f"({'stronger' if wind_diff > 0 else 'weaker'} in {city1})\n\n"
            
            # Compare pressure if available
            if hasattr(weather1, 'pressure') and hasattr(weather2, 'pressure'):
                comparison += f"Pressure:\n"
                comparison += f"{city1}: {weather1.pressure} hPa\n"
                comparison += f"{city2}: {weather2.pressure} hPa\n"
                pressure_diff = weather1.pressure - weather2.pressure
                comparison += f"Difference: {abs(pressure_diff)} hPa "
                comparison += f"({'higher' if pressure_diff > 0 else 'lower'} in {city1})\n\n"
            
            return comparison
            
        except Exception as e:
            raise Exception(f"Failed to compare cities: {str(e)}")
