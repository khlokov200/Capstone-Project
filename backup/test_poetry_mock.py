#!/usr/bin/env python3
"""
Mock test script to verify Poetry tab functionality without API calls
"""
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.poetry_service import PoetryService

class MockWeatherService:
    """Mock weather service for testing"""
    
    def get_current_weather(self, city, unit="metric"):
        """Return mock weather data"""
        return {
            'temperature': 22,
            'description': 'partly cloudy',
            'humidity': 65,
            'wind_speed': 5.2,
            'pressure': 1013,
            'unit': unit
        }

def test_poetry_service():
    """Test all poetry methods with mock data"""
    mock_weather_service = MockWeatherService()
    poetry_service = PoetryService(mock_weather_service)
    city = "London"
    
    print(f"Testing Poetry Service for {city}...")
    print("=" * 60)
    
    # Test basic poem generation
    try:
        print("\n1. Testing generate_poem:")
        poem = poetry_service.generate_poem(city)
        print(poem)
        print("✅ generate_poem - SUCCESS")
    except Exception as e:
        print(f"❌ generate_poem - ERROR: {e}")
    
    # Test haiku generation
    try:
        print("\n2. Testing generate_haiku:")
        haiku = poetry_service.generate_haiku(city)
        print(haiku)
        print("✅ generate_haiku - SUCCESS")
    except Exception as e:
        print(f"❌ generate_haiku - ERROR: {e}")
    
    # Test sonnet generation
    try:
        print("\n3. Testing generate_sonnet:")
        sonnet = poetry_service.generate_sonnet(city)
        print(sonnet)
        print("✅ generate_sonnet - SUCCESS")
    except Exception as e:
        print(f"❌ generate_sonnet - ERROR: {e}")
    
    # Test limerick generation
    try:
        print("\n4. Testing generate_limerick:")
        limerick = poetry_service.generate_limerick(city)
        print(limerick)
        print("✅ generate_limerick - SUCCESS")
    except Exception as e:
        print(f"❌ generate_limerick - ERROR: {e}")
    
    # Test free verse generation
    try:
        print("\n5. Testing generate_free_verse:")
        free_verse = poetry_service.generate_free_verse(city)
        print(free_verse)
        print("✅ generate_free_verse - SUCCESS")
    except Exception as e:
        print(f"❌ generate_free_verse - ERROR: {e}")

if __name__ == "__main__":
    test_poetry_service()
