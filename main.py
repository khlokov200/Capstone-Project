"""
Weather Dashboard Application Entry Point
Clean separation of concerns implementation
"""
import os
from dotenv import load_dotenv
from controllers.weather_controller import WeatherController
# from ui.main_window import MainWindow
try:
    from ui.main_window import MainWindow
except ModuleNotFoundError:
    # Fallback: try importing from current directory if 'ui' package is missing
    from ui.main_window import MainWindow


def main():
    """Main application entry point"""
    # Load environment variables
    load_dotenv()
    
    # Get API key with fallback
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        # Provide a demo key for testing
        api_key = "demo_key_for_testing_12345"
        print("⚠️  Using demo API key. For real weather data, set WEATHER_API_KEY environment variable.")
        print("   You can still use all features with simulated data!")
    
    try:
        # Create controller
        controller = WeatherController(api_key)
        
        # Create and run main window
        print("🚀 Starting Weather Dashboard with Live Radar...")
        print("🌦️ All features available including:")
        print("   🎬 Live Weather Animations")
        print("   🌩️ Doppler Weather Radar")
        print("   🌪️ Severe Weather Tracking")
        print("   📊 Comprehensive Charts & Analytics")
        
        app = MainWindow(controller)
        app.mainloop()
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("\n🔧 Try these steps:")
        print("1. Check if all dependencies are installed")
        print("2. Run: pip install -r requirements.txt")
        print("3. Make sure you're in the correct directory")
        raise


if __name__ == "__main__":
    main()
