#!/usr/bin/env python3
"""
Test script to check the weather data access
"""
import os
import sys
from unittest.mock import patch, MagicMock

# Mock the API response
mock_weather_data = {
    "weather": [{"description": "clear sky"}],
    "main": {
        "temp": 22.5,
        "humidity": 65,
        "feels_like": 23.2,
        "pressure": 1012
    },
    "wind": {
        "speed": 3.6,
        "deg": 180
    },
    "clouds": {"all": 20},
    "visibility": 10000,
    "sys": {
        "sunrise": 1596290400,
        "sunset": 1596344400
    }
}

print("🧪 Testing Weather Service with Mock Data")
print("=" * 50)

# Path to add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import after setting path
from services.weather_service import WeatherService
from core.api import WeatherAPI

# Create mock for the API fetch method
def mock_fetch(*args, **kwargs):
    return mock_weather_data

# Patch the API fetch method
WeatherAPI.fetch_weather = MagicMock(side_effect=mock_fetch)

try:
    # Initialize weather service with dummy key
    service = WeatherService("dummy_key")
    
    # Test getting weather data
    city = "Beijing"
    print(f"Getting mock weather for {city}...")
    
    # Get weather data
    weather_data = service.get_current_weather(city)
    
    # Test attribute access
    print(f"\nWeather Data Attributes:")
    print(f"Temperature: {weather_data.temperature}")
    print(f"Description: {weather_data.description}")
    print(f"Humidity: {weather_data.humidity}%")
    print(f"Wind Speed: {weather_data.wind_speed}")
    print(f"Feels Like: {weather_data.feels_like}")
    
    print("\n✅ Test successful! Attribute access is working correctly.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
