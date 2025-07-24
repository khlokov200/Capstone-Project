#!/usr/bin/env python3
"""
Comprehensive test to verify all Poetry tab buttons work correctly
"""
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.weather_controller import WeatherController

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

def test_all_poetry_methods():
    """Test all Poetry tab methods that are called from the UI"""
    print("🧪 COMPREHENSIVE POETRY TAB TEST")
    print("=" * 60)
    
    # Create a mock weather controller
    controller = WeatherController("demo_key")
    
    # Replace the weather service with a mock
    controller.poetry_service.weather_service = MockWeatherService()
    
    city = "London"
    
    # Test all Poetry tab methods
    poetry_methods = [
        ("generate_weather_poetry", "General Weather Poetry"),
        ("generate_weather_haiku", "Weather Haiku"),
        ("generate_weather_sonnet", "Weather Sonnet"),
        ("generate_weather_limerick", "Weather Limerick"),
        ("generate_weather_free_verse", "Free Verse Poetry")
    ]
    
    all_passed = True
    
    for method_name, description in poetry_methods:
        try:
            print(f"\n🔍 Testing {description}:")
            print("-" * 40)
            
            # Call the method
            method = getattr(controller, method_name)
            result = method(city)
            
            # Check if result is valid
            if result and isinstance(result, str) and len(result) > 10:
                print(f"✅ {description} - SUCCESS")
                # Show first few lines of the result
                preview = result.split('\n')[:3]
                for line in preview:
                    if line.strip():
                        print(f"   📝 {line[:60]}{'...' if len(line) > 60 else ''}")
            else:
                print(f"❌ {description} - FAILED (Invalid result)")
                all_passed = False
                
        except Exception as e:
            print(f"❌ {description} - ERROR: {e}")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL POETRY TAB METHODS WORKING CORRECTLY!")
        print("✅ Poetry tab is fully functional")
    else:
        print("❌ Some Poetry tab methods failed")
    
    print("=" * 60)
    
    return all_passed

def test_additional_methods():
    """Test additional methods that might be called from other tabs"""
    print("\n🔧 TESTING ADDITIONAL CONTROLLER METHODS")
    print("=" * 60)
    
    controller = WeatherController("demo_key")
    controller.weather_service = MockWeatherService()
    
    # Test some common methods that tabs might call
    additional_methods = [
        ("get_unit_label", "Get Unit Label"),
        ("toggle_unit", "Toggle Temperature Unit"),
        ("add_favorite_city", "Add Favorite City"),
        ("get_favorite_cities", "Get Favorite Cities"),
        ("toggle_auto_refresh", "Toggle Auto Refresh")
    ]
    
    for method_name, description in additional_methods:
        try:
            print(f"\n🔍 Testing {description}:")
            method = getattr(controller, method_name)
            
            if method_name == "add_favorite_city":
                result = method("London")
            elif method_name in ["toggle_unit", "toggle_auto_refresh"]:
                result = method()
            else:
                result = method()
            
            print(f"✅ {description} - SUCCESS")
            print(f"   📄 Result: {str(result)[:100]}...")
            
        except Exception as e:
            print(f"❌ {description} - ERROR: {e}")

if __name__ == "__main__":
    poetry_success = test_all_poetry_methods()
    test_additional_methods()
    
    print("\n🏁 FINAL SUMMARY:")
    print("=" * 60)
    if poetry_success:
        print("🎯 POETRY TAB: ✅ FULLY FUNCTIONAL")
        print("📝 All poetry generation methods working correctly")
        print("🌟 Users can generate haikus, sonnets, limericks, and free verse")
        print("✨ Poetry tab error has been successfully resolved!")
    else:
        print("🎯 POETRY TAB: ❌ NEEDS ATTENTION")
    
    print("\n💡 NEXT STEPS:")
    print("• Test the Poetry tab in the actual application")
    print("• Try generating different types of poetry")
    print("• Verify all buttons in all tabs work correctly")
    print("• Application is ready for full functionality testing!")
