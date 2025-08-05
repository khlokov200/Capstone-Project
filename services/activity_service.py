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
        
        # Get weather conditions and temperature for better suggestions
        conditions = weather.description.lower()
        temp = weather.temperature
        
        # Generate appropriate activity suggestions based on weather
        suggestions = []
        
        # Temperature-based suggestions
        if temp > 25:  # Hot weather
            suggestions.extend([
                "🏊 Visit a pool or beach",
                "🍦 Get ice cream",
                "🌳 Find a shaded park"
            ])
        elif temp > 15:  # Mild weather
            suggestions.extend([
                "🚴 Go cycling",
                "🏃 Go for a run",
                "🎾 Play outdoor sports"
            ])
        else:  # Cool weather
            suggestions.extend([
                "🏃 Indoor fitness activities",
                "🎨 Visit museums",
                "☕ Visit cozy cafes"
            ])
            
        # Weather condition based suggestions
        if "rain" in conditions or "snow" in conditions:
            suggestions.extend([
                "🎬 Watch a movie",
                "📚 Visit the library",
                "🎨 Try indoor activities"
            ])
        elif "clear" in conditions:
            suggestions.extend([
                "🌅 Go sightseeing",
                "🏞️ Visit parks",
                "📸 Photography tour"
            ])
        elif "cloud" in conditions:
            suggestions.extend([
                "🚶 Take a walking tour",
                "🎨 Visit art galleries",
                "🛍️ Go shopping"
            ])
            
        # Format the suggestions nicely
        suggestion_text = f"Weather in {city}: {weather.description}, {weather.formatted_temperature}\n\n"
        suggestion_text += "Recommended Activities:\n"
        suggestion_text += "\n".join(f"• {suggestion}" for suggestion in suggestions[:5])
        suggestion_text += "\n\n💡 Suggestions are based on current weather conditions"
        
        return suggestion_text
