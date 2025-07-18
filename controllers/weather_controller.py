"""
Main Weather Dashboard Controller
Coordinates between UI components and services
"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from models.weather_models import WeatherData
from services.weather_service import WeatherService
from services.forecast_service import ForecastService
from services.comparison_service import ComparisonService
from services.journal_service import JournalService
from services.activity_service import ActivityService
from services.poetry_service import PoetryService
from ui.constants import COLOR_PALETTE, TEMPERATURE_UNITS


class WeatherController:
    """Main controller for weather dashboard functionality"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.temp_unit_value = "metric"
        self.graph_mode_value = "line"
        
        # Initialize services
        self.weather_service = WeatherService(api_key)
        self.forecast_service = ForecastService(api_key)
        self.comparison_service = ComparisonService(self.weather_service)
        self.journal_service = JournalService()
        self.activity_service = ActivityService(self.weather_service)
        self.poetry_service = PoetryService(self.weather_service)
        
        # Graph components (will be set by main window)
        self.fig = None
        self.ax = None
        self.canvas = None

    def set_graph_components(self, fig, ax, canvas):
        """Set the matplotlib components for graph updates"""
        self.fig = fig
        self.ax = ax
        self.canvas = canvas

    def get_current_weather(self, city):
        """Get current weather and return WeatherData model"""
        unit = self.temp_unit_value
        weather_data = self.weather_service.get_current_weather(city, unit)
        
        # Update graph after getting weather
        self.update_graph()
        
        return WeatherData(
            temperature=weather_data['temperature'],
            description=weather_data['description'],
            humidity=weather_data['humidity'],
            wind_speed=weather_data['wind_speed'],
            unit=weather_data['unit'],
            city=city
        )

    def get_forecast(self, city):
        """Get weather forecast"""
        unit = self.temp_unit_value
        return self.forecast_service.get_forecast(city, unit)

    def get_five_day_forecast(self, city):
        """Get 5-day weather forecast"""
        unit = self.temp_unit_value
        return self.forecast_service.get_five_day_forecast(city, unit)

    def compare_cities(self, city1, city2):
        """Compare weather between two cities"""
        unit = self.temp_unit_value
        return self.comparison_service.compare_cities(city1, city2, unit)

    def save_journal_entry(self, text, mood):
        """Save journal entry"""
        self.journal_service.save_entry(text, mood)

    def suggest_activity(self, city):
        """Get activity suggestion for a city"""
        unit = self.temp_unit_value
        return self.activity_service.suggest(city, unit)

    def generate_poem(self, city):
        """Generate weather poem for a city"""
        unit = self.temp_unit_value
        return self.poetry_service.generate_poem(city, unit)

    def get_weather_history(self, limit=7):
        """Get weather history"""
        return self.weather_service.load_weather_history(limit)

    def toggle_unit(self):
        """Toggle between Celsius and Fahrenheit"""
        if self.temp_unit_value == "metric":
            self.temp_unit_value = "imperial"
        else:
            self.temp_unit_value = "metric"

    def toggle_graph_mode(self):
        """Toggle between line graph and heatmap"""
        if self.graph_mode_value == "line":
            self.graph_mode_value = "heatmap"
        else:
            self.graph_mode_value = "line"
        self.update_graph()

    def get_unit_label(self):
        """Get current temperature unit label"""
        unit = self.temp_unit_value
        return TEMPERATURE_UNITS[unit]["label"]

    def get_unit_name(self):
        """Get current temperature unit name"""
        unit = self.temp_unit_value
        return TEMPERATURE_UNITS[unit]["name"]

    def update_graph(self):
        """Update the graph display"""
        if not all([self.fig, self.ax, self.canvas]):
            return
        
        if self.graph_mode_value == "line":
            self._draw_line_graph()
        else:
            self._draw_heat_cool_map()

    def _draw_line_graph(self):
        """Draw line graph of temperature history"""
        dates, temps = self.weather_service.load_weather_history()
        self.ax.clear()
        
        if dates and temps:
            self.ax.plot(dates, temps, marker='o', color=COLOR_PALETTE["accent"])
            self.ax.set_title("Temperature History")
            self.ax.set_ylabel(self.get_unit_label())
            self.ax.tick_params(axis='x', labelrotation=45)
        else:
            self.ax.set_title("No Temperature History Available")
        
        self.fig.tight_layout()
        self.canvas.draw()

    def _draw_heat_cool_map(self):
        """Draw heat/cool map of temperature history"""
        dates, temps = self.weather_service.load_weather_history()
        self.ax.clear()
        
        if not dates or not temps:
            self.ax.set_title("No Data")
        else:
            temps_array = np.array(temps).reshape(1, -1)
            cmap = plt.get_cmap('coolwarm')
            self.ax.imshow(temps_array, cmap=cmap, aspect='auto')
            self.ax.set_xticks(range(len(dates)))
            self.ax.set_xticklabels(dates, rotation=45)
            self.ax.set_yticks([])
            self.ax.set_title("Heat/Cool Map of Temperatures")
        
        self.fig.tight_layout()
        self.canvas.draw()
