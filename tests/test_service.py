#!/usr/bin/env python3
"""
Test script to check the WeatherService
"""
import os
from services.weather_service import WeatherService

print("🧪 Testing WeatherService")
print("=" * 40)

# Set test API key
os.environ['WEATHER_API_KEY'] = 'test_key_for_validation'

try:
    # Initialize weather service
    service = WeatherService(os.environ['WEATHER_API_KEY'])
    
    # Test getting weather data
    city = "London"
    print(f"Getting weather for {city}...")
    weather_data = service.get_current_weather(city)
    
    # Access attributes to verify fix
    print(f"Temperature: {weather_data.temperature}")
    print(f"Description: {weather_data.description}")
    print(f"Humidity: {weather_data.humidity}")
    
    print("\n✅ Test successful! WeatherService is working correctly.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
