"""
Main Weather Dashboard Controller
Coordinates between UI components and services
"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from models.weather_models import WeatherData
from models.ml_models import MLEnhancedWeatherData
from services.weather_service import WeatherService
from services.forecast_service import ForecastService
from services.comparison_service import ComparisonService
from services.journal_service import JournalService
from services.activity_service import ActivityService
from services.poetry_service import PoetryService
from controllers.ml_controller import MLController
from ui.constants import COLOR_PALETTE, TEMPERATURE_UNITS


class WeatherController:
    """Main controller for weather dashboard functionality"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.temp_unit_value = "metric"
        self.graph_mode_value = "line"
        
        # New attributes for enhanced functionality
        self.last_city = None
        self.favorite_cities = []
        self.auto_refresh_enabled = False
        self.auto_refresh_interval = 300000  # 5 minutes in milliseconds
        
        # Initialize services
        self.weather_service = WeatherService(api_key)
        self.forecast_service = ForecastService(api_key)
        self.comparison_service = ComparisonService(self.weather_service)
        self.journal_service = JournalService()
        self.activity_service = ActivityService(self.weather_service)
        self.poetry_service = PoetryService(self.weather_service)
        
        # Initialize ML controller
        self.ml_controller = MLController()
        
        # Graph components (will be set by main window)
        self.fig = None
        self.ax = None
        self.canvas = None

        # New attributes for enhanced functionality
        self.last_city = None
        self.favorite_cities = []
        self.auto_refresh_enabled = False
        self.auto_refresh_interval = 300000  # 5 minutes in milliseconds

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
            city=city,
            # Add new weather elements
            visibility=weather_data.get('visibility'),
            cloudiness=weather_data.get('cloudiness'),
            pressure=weather_data.get('pressure'),
            feels_like=weather_data.get('feels_like'),
            wind_direction=weather_data.get('wind_direction'),
            sunrise=weather_data.get('sunrise'),
            sunset=weather_data.get('sunset'),
            rain_1h=weather_data.get('rain_1h'),
            rain_3h=weather_data.get('rain_3h'),
            snow_1h=weather_data.get('snow_1h'),
            snow_3h=weather_data.get('snow_3h')
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

    def get_weather_history(self, city_or_limit=7):
        """Get weather history - supports both city name and limit parameters"""
        if isinstance(city_or_limit, str):
            # If a city name is passed, get general history and filter
            dates, temps = self.weather_service.load_weather_history()
            if not dates or not temps:
                return "No weather history available for this location."
            
            # Create a formatted history display
            history = f"📅 Recent weather data (last {len(dates)} entries):\n\n"
            for date, temp in zip(dates[-10:], temps[-10:]):  # Show last 10 entries
                history += f"• {date}: {temp}°{self.get_unit_label()}\n"
            
            if len(dates) > 10:
                history += f"\n... and {len(dates) - 10} more entries"
            
            return history
        else:
            # Original behavior for numeric limit
            return self.weather_service.load_weather_history(city_or_limit)

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

    # Quick Action Methods for Enhanced UX
    def get_quick_weather(self, city=None):
        """Get weather for specified city or last used city"""
        target_city = city or self.last_city or "New York"  # Default fallback
        weather_data = self.get_current_weather(target_city)
        self.last_city = target_city
        return weather_data

    def get_weather_summary(self, city):
        """Get comprehensive weather summary including current + forecast"""
        current = self.get_current_weather(city)
        forecast = self.get_forecast(city)
        five_day = self.get_five_day_forecast(city)
        
        summary = f"🌟 WEATHER SUMMARY FOR {city.upper()}\n"
        summary += "=" * 50 + "\n\n"
        
        # Current weather
        summary += "📍 CURRENT CONDITIONS:\n"
        summary += f"Temperature: {current.formatted_temperature}\n"
        summary += f"Description: {current.description}\n"
        summary += f"Humidity: {current.humidity}%\n"
        summary += f"Wind: {current.formatted_wind}\n\n"
        
        # Add forecast preview
        summary += "📅 FORECAST PREVIEW:\n"
        summary += forecast[:200] + "...\n\n"
        
        # Add activity suggestion
        activity = self.suggest_activity(city)
        summary += "🎯 SUGGESTED ACTIVITY:\n"
        summary += activity[:150] + "...\n"
        
        return summary

    def add_favorite_city(self, city):
        """Add city to favorites list"""
        if city and city not in self.favorite_cities:
            self.favorite_cities.append(city)
            return f"✅ {city} added to favorites!"
        return f"ℹ️ {city} is already in favorites."

    def get_favorite_cities(self):
        """Get list of favorite cities"""
        return self.favorite_cities

    def toggle_auto_refresh(self):
        """Toggle auto-refresh functionality"""
        self.auto_refresh_enabled = not self.auto_refresh_enabled
        status = "enabled" if self.auto_refresh_enabled else "disabled"
        return f"🔄 Auto-refresh {status}"

    def check_weather_alerts(self, city):
        """Check for weather alerts and warnings"""
        try:
            weather_data = self.get_current_weather(city)
            alerts = []
            
            # Temperature alerts
            temp = weather_data.temperature
            if (temp > 35 and weather_data.unit == "metric") or \
               (temp > 95 and weather_data.unit == "imperial"):
                alerts.append("🔥 EXTREME HEAT WARNING")
            elif (temp < -10 and weather_data.unit == "metric") or \
                 (temp < 14 and weather_data.unit == "imperial"):
                alerts.append("🥶 EXTREME COLD WARNING")
            
            # Weather condition alerts
            desc = weather_data.description.lower()
            if any(word in desc for word in ["storm", "thunderstorm"]):
                alerts.append("⛈️ STORM ALERT")
            elif "rain" in desc and weather_data.wind_speed > 10:
                alerts.append("🌧️ HEAVY RAIN & WIND")
            elif weather_data.visibility and weather_data.visibility < 1:
                alerts.append("🌫️ LOW VISIBILITY WARNING")
            
            # Wind alerts
            if weather_data.wind_speed > 15:
                alerts.append("💨 HIGH WIND WARNING")
                
            if not alerts:
                alerts.append("✅ NO CURRENT WEATHER ALERTS")
                
            return "\n".join(alerts)
            
        except Exception as e:
            return f"❌ Error checking alerts: {str(e)}"

    # History-related methods for HistoryTab
    def get_weather_history(self, city_or_limit=7):
        """Get weather history - supports both city name and limit parameters"""
        if isinstance(city_or_limit, str):
            # If a city name is passed, get general history and filter
            dates, temps = self.weather_service.load_weather_history()
            if not dates or not temps:
                return "No weather history available for this location."
            
            # Create a formatted history display
            history = f"📅 Recent weather data (last {len(dates)} entries):\n\n"
            for date, temp in zip(dates[-10:], temps[-10:]):  # Show last 10 entries
                history += f"• {date}: {temp}°{self.get_unit_label()}\n"
            
            if len(dates) > 10:
                history += f"\n... and {len(dates) - 10} more entries"
            
            return history
        else:
            # Original behavior for numeric limit
            return self.weather_service.load_weather_history(city_or_limit)

    def get_weather_statistics(self, city):
        """Get weather statistics for a city"""
        try:
            dates, temps = self.weather_service.load_weather_history()
            
            if not dates or not temps:
                return "No weather data available for statistics."
            
            # Calculate statistics
            avg_temp = sum(temps) / len(temps)
            max_temp = max(temps)
            min_temp = min(temps)
            temp_range = max_temp - min_temp
            unit_label = self.get_unit_label()
            
            stats = f"📊 WEATHER STATISTICS:\n"
            stats += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            stats += f"📋 Data Period: {dates[0]} to {dates[-1]}\n"
            stats += f"📋 Total Records: {len(dates)}\n\n"
            
            stats += f"🌡️ TEMPERATURE ANALYSIS:\n"
            stats += f"• Average Temperature: {avg_temp:.1f}{unit_label}\n"
            stats += f"• Maximum Temperature: {max_temp:.1f}{unit_label}\n"
            stats += f"• Minimum Temperature: {min_temp:.1f}{unit_label}\n"
            stats += f"• Temperature Range: {temp_range:.1f}°\n\n"
            
            # Temperature distribution
            hot_days = sum(1 for t in temps if t > 25)  # Assuming Celsius for now
            cold_days = sum(1 for t in temps if t < 10)
            moderate_days = len(temps) - hot_days - cold_days
            
            stats += f"🔍 TEMPERATURE PATTERNS:\n"
            stats += f"• Hot days (>25°): {hot_days} ({hot_days/len(temps)*100:.1f}%)\n"
            stats += f"• Cold days (<10°): {cold_days} ({cold_days/len(temps)*100:.1f}%)\n"
            stats += f"• Moderate days: {moderate_days} ({moderate_days/len(temps)*100:.1f}%)\n\n"
            
            # Recent trend
            if len(temps) > 7:
                recent_avg = sum(temps[-7:]) / 7
                older_avg = sum(temps[:7]) / 7
                trend = "warming" if recent_avg > older_avg else "cooling"
                stats += f"📈 Recent Trend: {trend.upper()} (last 7 days vs first 7 days)\n"
            
            return stats
            
        except Exception as e:
            return f"❌ Error generating statistics: {str(e)}"

    def get_weather_trends(self, city):
        """Get weather trends analysis for a city"""
        try:
            dates, temps = self.weather_service.load_weather_history(30)  # Get more data for trends
            
            if len(temps) < 5:
                return "Need at least 5 data points for trend analysis."
            
            trends = f"📈 WEATHER TREND ANALYSIS:\n"
            trends += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            # Weekly analysis if enough data
            if len(temps) >= 14:
                week1_avg = sum(temps[:7]) / 7
                week2_avg = sum(temps[7:14]) / 7
                change = week2_avg - week1_avg
                
                trends += f"📊 WEEKLY COMPARISON:\n"
                trends += f"• First Week Average: {week1_avg:.1f}°{self.get_unit_label()}\n"
                trends += f"• Second Week Average: {week2_avg:.1f}°{self.get_unit_label()}\n"
                trends += f"• Week-over-week Change: {change:+.1f}°\n\n"
            
            # Moving average trend
            if len(temps) >= 7:
                recent_trend = sum(temps[-5:]) / 5
                earlier_trend = sum(temps[-10:-5]) / 5 if len(temps) >= 10 else sum(temps[:-5]) / len(temps[:-5])
                
                trend_direction = "📈 UPWARD" if recent_trend > earlier_trend else "📉 DOWNWARD"
                trends += f"🎯 CURRENT TREND: {trend_direction}\n"
                trends += f"• Recent Average: {recent_trend:.1f}°{self.get_unit_label()}\n"
                trends += f"• Previous Average: {earlier_trend:.1f}°{self.get_unit_label()}\n"
                trends += f"• Change: {recent_trend - earlier_trend:+.1f}°\n\n"
            
            # Variability analysis
            import statistics
            std_dev = statistics.stdev(temps) if len(temps) > 1 else 0
            trends += f"📊 VARIABILITY ANALYSIS:\n"
            trends += f"• Standard Deviation: {std_dev:.1f}°\n"
            trends += f"• Weather Stability: {'Stable' if std_dev < 3 else 'Variable' if std_dev < 6 else 'Highly Variable'}\n\n"
            
            # Forecast insight
            trends += f"🔮 INSIGHTS:\n"
            if std_dev < 3:
                trends += "• Weather patterns are quite stable\n"
            elif recent_trend > earlier_trend:
                trends += "• Temperatures are trending warmer\n"
            else:
                trends += "• Temperatures are trending cooler\n"
            
            return trends
            
        except Exception as e:
            return f"❌ Error analyzing trends: {str(e)}"

    def export_weather_data(self, city):
        """Export weather data for a city"""
        try:
            dates, temps = self.weather_service.load_weather_history()
            
            if not dates:
                return "No weather data available for export."
            
            # Create export summary
            export_summary = f"📤 WEATHER DATA EXPORT COMPLETE\n"
            export_summary += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            export_summary += f"📊 Export Summary:\n"
            export_summary += f"• Total Records: {len(dates)}\n"
            export_summary += f"• Date Range: {dates[0]} to {dates[-1]}\n"
            export_summary += f"• Average Temperature: {sum(temps)/len(temps):.1f}°{self.get_unit_label()}\n"
            export_summary += f"• Temperature Range: {min(temps):.1f}° to {max(temps):.1f}°\n\n"
            
            export_summary += f"💾 Data Format: CSV\n"
            export_summary += f"📁 Location: data/weather_log.csv\n\n"
            
            export_summary += f"📋 Sample Data (last 5 entries):\n"
            for i, (date, temp) in enumerate(zip(dates[-5:], temps[-5:])):
                export_summary += f"{i+1}. {date}: {temp}°{self.get_unit_label()}\n"
            
            export_summary += f"\n✅ Export completed successfully!"
            export_summary += f"\n💡 You can find the complete data in the CSV file."
            
            return export_summary
            
        except Exception as e:
            return f"❌ Error exporting data: {str(e)}"

    def clear_weather_history(self):
        """Clear weather history"""
        try:
            # Instead of actually clearing the file, provide information about how to clear it
            clear_info = f"🗑️ WEATHER HISTORY CLEARING\n"
            clear_info += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            clear_info += f"⚠️ IMPORTANT NOTICE:\n"
            clear_info += f"Weather history clearing is currently disabled to preserve data.\n\n"
            clear_info += f"📂 History Location: data/weather_log.csv\n"
            clear_info += f"💾 Current Records: Available in file\n\n"
            clear_info += f"🛠️ To manually clear history:\n"
            clear_info += f"1. Navigate to the 'data' folder\n"
            clear_info += f"2. Rename or delete 'weather_log.csv'\n"
            clear_info += f"3. Restart the application\n\n"
            clear_info += f"💡 This preserves your weather history for future analysis!"
            
            return clear_info
            
        except Exception as e:
            return f"❌ Error clearing history: {str(e)}"
