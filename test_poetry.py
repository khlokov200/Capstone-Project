#!/usr/bin/env python3
"""
Test script to verify Poetry tab functionality
"""
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.weather_controller import WeatherController

def test_poetry_methods():
    """Test all poetry methods in WeatherController"""
    # Get API key from environment variable
    api_key = os.getenv("WEATHER_API_KEY", "demo_key")
    
    controller = WeatherController(api_key)
    city = "London"
    
    print(f"Testing Poetry methods for {city}...")
    print("=" * 60)
    
    # Test basic poem generation
    try:
        print("\n1. Testing generate_poem:")
        poem = controller.generate_poem(city)
        print(poem)
        print("✅ generate_poem - SUCCESS")
    except Exception as e:
        print(f"❌ generate_poem - ERROR: {e}")
    
    # Test general weather poetry
    try:
        print("\n2. Testing generate_weather_poetry:")
        poetry = controller.generate_weather_poetry(city)
        print(poetry)
        print("✅ generate_weather_poetry - SUCCESS")
    except Exception as e:
        print(f"❌ generate_weather_poetry - ERROR: {e}")
    
    # Test haiku generation
    try:
        print("\n3. Testing generate_weather_haiku:")
        haiku = controller.generate_weather_haiku(city)
        print(haiku)
        print("✅ generate_weather_haiku - SUCCESS")
    except Exception as e:
        print(f"❌ generate_weather_haiku - ERROR: {e}")
    
    # Test sonnet generation
    try:
        print("\n4. Testing generate_weather_sonnet:")
        sonnet = controller.generate_weather_sonnet(city)
        print(sonnet)
        print("✅ generate_weather_sonnet - SUCCESS")
    except Exception as e:
        print(f"❌ generate_weather_sonnet - ERROR: {e}")
    
    # Test limerick generation
    try:
        print("\n5. Testing generate_weather_limerick:")
        limerick = controller.generate_weather_limerick(city)
        print(limerick)
        print("✅ generate_weather_limerick - SUCCESS")
    except Exception as e:
        print(f"❌ generate_weather_limerick - ERROR: {e}")
    
    # Test free verse generation
    try:
        print("\n6. Testing generate_weather_free_verse:")
        free_verse = controller.generate_weather_free_verse(city)
        print(free_verse)
        print("✅ generate_weather_free_verse - SUCCESS")
    except Exception as e:
        print(f"❌ generate_weather_free_verse - ERROR: {e}")

if __name__ == "__main__":
    test_poetry_methods()
