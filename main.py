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
    
    # Toggle data source: "api" for live, "json" for local JSON
    data_source = os.getenv("DATA_SOURCE_MODE", "api")  # or set manually: "json" or "api"
    json_data_dir = os.getenv("JSON_DATA_DIR", "data/json_exports")
    
    # Create controller
    controller = WeatherController(api_key, data_source=data_source, json_data_dir=json_data_dir)
    
    # Create and run main window
    app = MainWindow(controller)
    app.mainloop()


if __name__ == "__main__":
    main()
