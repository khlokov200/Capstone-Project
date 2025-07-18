#!/usr/bin/env python3
"""
Weather Elements Test Script
Tests all the new weather elements to ensure they're working correctly
"""

import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, '/Users/Tobi_Prod/Documents/JTC/Capstone-Project')

from controllers.weather_controller import WeatherController

def test_weather_elements():
    """Test all weather elements with a sample city"""
    print("🧪 Testing Weather Elements...")
    print("=" * 60)
    
    # Load environment
    load_dotenv()
    api_key = os.getenv("WEATHER_API_KEY")
    
    if not api_key:
        print("❌ Error: WEATHER_API_KEY not found in environment variables")
        return False
    
    try:
        # Create controller
        controller = WeatherController(api_key)
        
        # Test city
        test_city = "Baltimore"
        print(f"📍 Testing weather data for: {test_city}")
        print("-" * 40)
        
        # Get weather data
        weather_data = controller.get_current_weather(test_city)
        
        # Test basic elements
        print("🌡️  TEMPERATURE ELEMENTS:")
        print(f"   • Temperature: {weather_data.formatted_temperature}")
        print(f"   • Feels Like: {weather_data.formatted_feels_like}")
        print(f"   • Description: {weather_data.description}")
        print()
        
        # Test atmospheric elements
        print("🌬️  ATMOSPHERIC ELEMENTS:")
        print(f"   • Humidity: {weather_data.humidity}%")
        print(f"   • Pressure: {weather_data.pressure} hPa" if weather_data.pressure else "   • Pressure: N/A")
        print(f"   • Visibility: {weather_data.formatted_visibility}")
        print(f"   • Cloudiness: {weather_data.formatted_cloudiness}")
        print()
        
        # Test wind elements
        print("💨 WIND ELEMENTS:")
        print(f"   • Wind: {weather_data.formatted_wind}")
        print()
        
        # Test solar elements
        print("☀️  SOLAR ELEMENTS:")
        print(f"   • Sunrise: {weather_data.formatted_sunrise}")
        print(f"   • Sunset: {weather_data.formatted_sunset}")
        print()
        
        # Test special conditions
        print("🌧️  SPECIAL CONDITIONS:")
        print(f"   • Fog: {weather_data.formatted_fog}")
        print(f"   • Precipitation: {weather_data.formatted_precipitation}")
        print()
        
        # Test unit conversion
        print("🔄 UNIT CONVERSION TEST:")
        controller.toggle_unit()
        weather_data_f = controller.get_current_weather(test_city)
        print(f"   • Fahrenheit: {weather_data_f.formatted_temperature}")
        print(f"   • Feels Like (F): {weather_data_f.formatted_feels_like}")
        
        # Switch back
        controller.toggle_unit()
        print()
        
        print("✅ All weather elements tested successfully!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

def test_ui_elements():
    """Test that UI elements are properly configured"""
    print("🎨 Testing UI Elements...")
    print("-" * 40)
    
    try:
        from ui.constants import COLOR_PALETTE
        from ui.components import StyledButton
        
        # Test color palette
        required_colors = [
            "button_primary", "button_secondary", "button_warning", 
            "button_info", "button_dark", "text_on_button"
        ]
        
        for color in required_colors:
            if color in COLOR_PALETTE:
                print(f"   ✅ {color}: {COLOR_PALETTE[color]}")
            else:
                print(f"   ❌ Missing color: {color}")
                return False
        
        print("✅ UI elements configured correctly!")
        print()
        return True
        
    except Exception as e:
        print(f"❌ Error testing UI elements: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Weather Dashboard Elements Test Suite")
    print("=" * 60)
    print()
    
    # Test weather elements
    weather_test = test_weather_elements()
    print()
    
    # Test UI elements
    ui_test = test_ui_elements()
    
    # Summary
    print("📊 TEST SUMMARY:")
    print(f"   • Weather Elements: {'✅ PASS' if weather_test else '❌ FAIL'}")
    print(f"   • UI Elements: {'✅ PASS' if ui_test else '❌ FAIL'}")
    print()
    
    if weather_test and ui_test:
        print("🎉 ALL TESTS PASSED! Your Weather Dashboard is ready!")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
