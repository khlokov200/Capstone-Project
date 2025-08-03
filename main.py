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
    
    # Get API key
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise ValueError("Missing WEATHER_API_KEY in environment variables")
    
    # Create controller
    controller = WeatherController(api_key)
    
    # Create and run main window
    app = MainWindow(controller)
    app.mainloop()


if __name__ == "__main__":
    main()
