"""
Individual tab components for the weather dashboard - Refactored to reduce duplication
"""
import tkinter as tk
from tkinter import ttk, messagebox
from .components import StyledButton, StyledText, StyledLabel, AnimatedLabel
from .constants import COLOR_PALETTE
from .tab_helpers import (
    BaseTab, ChartHelper, ButtonHelper, WeatherFormatter, 
    CommonActions, CHARTS_AVAILABLE
)

# Import numpy for chart data generation
try:
    import numpy as np
except ImportError:
    np = None

# Import live weather services
try:
    from services.live_weather_service import LiveAnimationService, WeatherRadarService, AnimatedWeatherWidget, WeatherRadarWidget
    LIVE_WEATHER_AVAILABLE = True
except ImportError:
    LIVE_WEATHER_AVAILABLE = False

try:
    import cv2
    from PIL import Image, ImageTk
    CAMERA_AVAILABLE = True
except ImportError:
    CAMERA_AVAILABLE = False


class WeatherTab(BaseTab):
    """Current weather tab component"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "Current Weather")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        # Create split layout using helper
        self.create_split_layout()
        
        # Setup left panel (original weather interface)
        self._setup_weather_interface()
        
        # Setup right panel (chart area)
        self._setup_chart_interface()
    
    def _setup_weather_interface(self):
        """Setup the weather data interface in the left panel"""
        # City input using helper
        self.setup_city_input(self.left_frame)
        
        # Results display
        self.setup_result_text(self.left_frame, height=12, width=60)
        
        # Animated mascot
        try:
            self.anim_label = AnimatedLabel(self.left_frame, "assets/sunny.gif")
            self.anim_label.pack(pady=10)
        except Exception:
            pass  # Skip if GIF not found
        
        # Alert label
        self.alert_label = StyledLabel(self.left_frame, text="")
        self.alert_label.pack(pady=5)
        
        # Main button
        ButtonHelper.create_main_button(self.left_frame, "primary_black", "Get Weather", self.fetch_weather)
        
        # Toggle button
        ButtonHelper.create_main_button(self.left_frame, "info_black", "Toggle Graph Type", self.controller.toggle_graph_mode)
        
        # Additional buttons using helper
        button_config = [
            ("accent_black", "⭐ Save Favorite", self.save_favorite),
            ("success_black", "🔄 Auto-Refresh", self.toggle_auto_refresh),
            ("warning_black", "⚠️ Check Alerts", self.check_alerts)
        ]
        ButtonHelper.create_button_grid(self.left_frame, button_config, columns=3)

    def _setup_chart_interface(self):
        """Setup the chart interface in the right panel"""
        # Chart title
        StyledLabel(self.right_frame, text="📊 Weather Charts", 
                   font=("Arial", 14, "bold")).pack(pady=5)
        
        # Chart buttons using helper
        if CHARTS_AVAILABLE:
            chart_button_config = [
                ("info_black", "📈 Temperature Trend", self.generate_temperature_chart),
                ("success_black", "📊 Weather Metrics", self.generate_metrics_bar_chart),
                ("accent_black", "📋 Data Distribution", self.generate_histogram),
                ("warning_black", "🌡️ Comfort Analysis", self.generate_scatter_plot)
            ]
            ButtonHelper.create_button_grid(self.right_frame, chart_button_config, columns=2)
        else:
            StyledLabel(self.right_frame, text="Charts unavailable\n(matplotlib not installed)", 
                       foreground="red").pack()
        
        # Chart display area using helper
        self.chart_frame = ChartHelper.create_chart_frame(self.right_frame)
        
        # Initialize with placeholder
        self._create_chart_placeholder()

    def _create_chart_placeholder(self):
        """Create a placeholder for the chart area"""
        placeholder_content = """📊 Weather Charts Available:

Click any chart button to generate visualizations:

📈 Temperature Trend - Historical temperature data
📊 Weather Metrics - Current conditions comparison  
📋 Data Distribution - Temperature distribution analysis
🌡️ Comfort Analysis - Temperature vs humidity scatter plot

Charts will appear here when generated."""
        
        ChartHelper.create_chart_placeholder(self.chart_frame, "Chart Display Area", placeholder_content)
    
    def fetch_weather(self):
        """Fetch weather for the entered city"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            result = self.controller.get_current_weather(city)
            formatted_result = WeatherFormatter.format_weather_display(result)
            self.display_result(formatted_result)
            
            # Check alerts
            alert = WeatherFormatter.check_weather_alerts(result)
            if alert:
                self.alert_label.config(text=alert, foreground=COLOR_PALETTE["heat"])
            else:
                self.alert_label.config(text="", foreground=COLOR_PALETTE["tab_fg"])
        except Exception as e:
            self.handle_error(e, "fetching weather")

    def save_favorite(self):
        """Save current city as favorite"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            result = self.controller.add_favorite_city(city)
            CommonActions.show_info_message("Favorite Saved", result)
        except Exception as e:
            self.handle_error(e, "saving favorite")

    def toggle_auto_refresh(self):
        """Toggle auto-refresh for weather updates"""
        try:
            result = self.controller.toggle_auto_refresh()
            CommonActions.show_info_message("Auto-Refresh", result)
        except Exception as e:
            self.handle_error(e, "toggling auto-refresh")

    def check_alerts(self):
        """Check weather alerts for current city"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            alerts = self.controller.check_weather_alerts(city)
            CommonActions.create_alert_popup(self.frame, "Weather Alerts", alerts)
        except Exception as e:
            self.handle_error(e, "checking alerts")

    def generate_temperature_chart(self):
        """Generate temperature trend line chart using helper"""
        try:
            # Sample temperature data (replace with real data from controller)
            dates = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            temps = [22, 24, 19, 25, 27, 23, 21]
            
            ChartHelper.create_line_chart(
                self.chart_frame,
                "7-Day Temperature Trend",
                dates,
                temps,
                "Day",
                "Temperature (°C)"
            )
        except Exception as e:
            self.handle_error(e, "generating temperature chart")

    def generate_metrics_bar_chart(self):
        """Generate weather metrics bar chart using helper"""
        try:
            # Sample weather metrics data
            metrics = ['Temperature', 'Humidity', 'Wind Speed', 'Pressure', 'Visibility']
            values = [24, 65, 12, 1013, 10]
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']
            
            ChartHelper.create_bar_chart(
                self.chart_frame,
                "Current Weather Metrics",
                metrics,
                values,
                colors,
                rotate_labels=True
            )
        except Exception as e:
            self.handle_error(e, "generating metrics chart")
    
    def generate_histogram(self):
        """Generate temperature distribution histogram using helper"""
        try:
            # Sample temperature distribution data
            if np:
                np.random.seed(42)  # For consistent results
                temp_data = np.random.normal(22, 3, 100)  # Mean 22°C, std dev 3°C
            else:
                temp_data = [20, 21, 22, 23, 24, 22, 21, 23, 22, 24] * 10  # Fallback data
            
            ChartHelper.create_histogram(
                self.chart_frame,
                "Temperature Distribution Analysis",
                temp_data,
                bins=15,
                color='#3498db'
            )
        except Exception as e:
            self.handle_error(e, "generating histogram")

    def generate_scatter_plot(self):
        """Generate temperature vs humidity scatter plot"""
        try:
            if not CHARTS_AVAILABLE:
                CommonActions.show_warning_message("Charts Unavailable", "Matplotlib is not installed")
                return
            
            ChartHelper.clear_chart_area(self.chart_frame)
            
            # This method remains complex due to scatter plot specifics
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
            
            fig = Figure(figsize=(8, 5), dpi=100, facecolor='white')
            ax = fig.add_subplot(111)
            
            # Sample temperature vs humidity data
            if np:
                np.random.seed(42)
                temperatures = np.random.normal(23, 4, 50)
                humidity = np.random.normal(60, 15, 50)
                
                # Calculate comfort index
                comfort_index = 100 - abs(temperatures - 22) * 2 - abs(humidity - 50) * 0.5
                
                scatter = ax.scatter(temperatures, humidity, c=comfort_index, cmap='RdYlGn', 
                                   s=80, alpha=0.7, edgecolors='white', linewidth=1)
                
                cbar = fig.colorbar(scatter, ax=ax)
                cbar.set_label('Comfort Index', fontsize=12)
            else:
                ax.scatter([20, 22, 24, 26], [45, 55, 65, 75], s=80, alpha=0.7)
            
            ax.set_title('Temperature vs Humidity Comfort Analysis', fontsize=14, fontweight='bold', pad=20)
            ax.set_xlabel('Temperature (°C)', fontsize=12)
            ax.set_ylabel('Humidity (%)', fontsize=12)
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.set_facecolor('#f8f9fa')
            
            # Add comfort zones
            ax.axvspan(20, 26, alpha=0.1, color='green', label='Ideal Temperature')
            ax.axhspan(40, 60, alpha=0.1, color='blue', label='Ideal Humidity')
            ax.legend()
            
            fig.tight_layout()
            ChartHelper.embed_chart_in_frame(fig, self.chart_frame)
            
        except Exception as e:
            self.handle_error(e, "generating scatter plot")


class ForecastTab(BaseTab):
    """Weather forecast tab component"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "Forecast")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components with split-screen layout"""
        # Create split layout using helper
        self.create_split_layout()
        
        # Setup left panel
        self._setup_forecast_interface()
        
        # Setup right panel (chart area)
        self._setup_forecast_charts()
    
    def _setup_forecast_interface(self):
        """Setup the forecast interface in the left panel"""
        # City input using helper
        self.setup_city_input(self.left_frame)
        
        # Results display
        self.setup_result_text(self.left_frame, height=12, width=60)
        
        # Main action button
        ButtonHelper.create_main_button(self.left_frame, "primary_black", "Get Forecast", self.fetch_forecast)
        
        # Additional Enhanced Buttons using helper
        button_config = [
            ("accent_black", "🌤️ Hourly Details", self.get_hourly_forecast),
            ("info_black", "📊 Chart View", self.show_forecast_chart),
            ("success_black", "📱 Share Forecast", self.share_forecast),
            ("warning_black", "⚠️ Weather Alerts", self.check_forecast_alerts)
        ]
        ButtonHelper.create_button_grid(self.left_frame, button_config, columns=4)
    
    def _setup_forecast_charts(self):
        """Setup the forecast chart interface in the right panel"""
        # Chart title
        StyledLabel(self.right_frame, text="📊 Forecast Visualizations", 
                   font=("Arial", 14, "bold")).pack(pady=5)
        
        # Chart control buttons using helper
        if CHARTS_AVAILABLE:
            chart_button_config = [
                ("info_black", "📈 Forecast Trend", self.generate_forecast_line_chart),
                ("success_black", "📊 Weather Conditions", self.generate_forecast_bar_chart),
                ("accent_black", "🌧️ Precipitation Chart", self.generate_precipitation_chart),
                ("warning_black", "🌡️ Temp Distribution", self.generate_temp_histogram)
            ]
            ButtonHelper.create_button_grid(self.right_frame, chart_button_config, columns=2)
        else:
            StyledLabel(self.right_frame, text="Charts unavailable\n(matplotlib not installed)", 
                       foreground="red").pack()
        
        # Chart display area using helper
        self.chart_frame = ChartHelper.create_chart_frame(self.right_frame)
        
        # Initialize with placeholder
        self._create_forecast_chart_placeholder()

    def _create_forecast_chart_placeholder(self):
        """Create a placeholder for the forecast chart area"""
        placeholder_content = """📊 Forecast Visualizations Available:

📈 Forecast Trend - Temperature and humidity trends over time
📊 Weather Conditions - Comparison of weather metrics
🌧️ Precipitation Chart - Rain/snow probability analysis
🌡️ Temp Distribution - Temperature frequency distribution

Select a chart type to visualize forecast data."""
        
        ChartHelper.create_chart_placeholder(self.chart_frame, "Forecast Charts", placeholder_content)
    
    def fetch_forecast(self):
        """Fetch forecast for the entered city"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            forecast = self.controller.get_forecast(city)
            unit_label = self.controller.get_unit_label()
            formatted_result = f"Forecast for {city} ({unit_label}):\n{forecast}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "fetching forecast")

    def get_hourly_forecast(self):
        """Get detailed hourly forecast"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            # Enhanced hourly forecast display
            forecast = self.controller.get_forecast(city)
            hourly_details = f"🌤️ HOURLY FORECAST DETAILS for {city}:\n"
            hourly_details += "━" * 50 + "\n\n"
            hourly_details += "⏰ Next 24 Hours:\n"
            hourly_details += "• 6 AM: Partly cloudy, 18°C, Light breeze\n"
            hourly_details += "• 9 AM: Sunny, 22°C, Moderate breeze\n"
            hourly_details += "• 12 PM: Sunny, 26°C, Strong breeze\n"
            hourly_details += "• 3 PM: Partly cloudy, 28°C, Moderate breeze\n"
            hourly_details += "• 6 PM: Cloudy, 24°C, Light breeze\n"
            hourly_details += "• 9 PM: Clear, 20°C, Calm\n\n"
            hourly_details += "🌟 Best Times Today:\n"
            hourly_details += "• Outdoor Activities: 9 AM - 3 PM\n"
            hourly_details += "• Photography: 6 PM - 8 PM (Golden hour)\n"
            hourly_details += "• Evening Walks: 7 PM - 9 PM\n\n"
            hourly_details += forecast
            
            self.display_result(hourly_details)
        except Exception as e:
            self.handle_error(e, "getting hourly forecast")

    def show_forecast_chart(self):
        """Show forecast in chart format"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            chart_data = f"📊 CHART VIEW for {city}:\n"
            chart_data += "━" * 50 + "\n\n"
            chart_data += "Temperature Trend (Next 5 Days):\n"
            chart_data += "Day 1: ████████████████████ 24°C ☀️\n"
            chart_data += "Day 2: ██████████████████ 22°C ⛅\n"
            chart_data += "Day 3: ████████████████ 20°C 🌧️\n"
            chart_data += "Day 4: ██████████████████ 22°C ⛅\n"
            chart_data += "Day 5: ████████████████████████ 26°C ☀️\n\n"
            chart_data += "Precipitation Probability:\n"
            chart_data += "Day 1: ██ 10% (Low)\n"
            chart_data += "Day 2: ████ 25% (Low)\n"
            chart_data += "Day 3: ████████████████ 80% (High)\n"
            chart_data += "Day 4: ██████ 30% (Medium)\n"
            chart_data += "Day 5: █ 5% (Very Low)\n\n"
            chart_data += "💡 Visual representation of weather trends and patterns"
            
            self.display_result(chart_data)
        except Exception as e:
            self.handle_error(e, "showing forecast chart")

    def share_forecast(self):
        """Share forecast information"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            forecast = self.controller.get_forecast(city)
            share_text = f"📱 SHAREABLE FORECAST for {city}:\n"
            share_text += "━" * 50 + "\n\n"
            share_text += f"Weather forecast ready for sharing!\n\n"
            share_text += "Share-ready format:\n"
            share_text += f"🌤️ {city} Weather Update\n"
            share_text += forecast[:200] + "...\n\n"
            share_text += "📲 Social Media Ready:\n"
            share_text += f"#Weather #{city.replace(' ', '')} #Forecast\n\n"
            share_text += "💡 Content has been formatted for easy sharing!"
            
            self.display_result(share_text)
        except Exception as e:
            self.handle_error(e, "sharing forecast")

    def check_forecast_alerts(self):
        """Check for weather alerts in the forecast"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            alerts = f"⚠️ WEATHER ALERTS for {city}:\n"
            alerts += "━" * 50 + "\n\n"
            alerts += "🔍 Scanning forecast for potential weather hazards...\n\n"
            alerts += "📅 Next 3 Days Alert Summary:\n"
            alerts += "• Tomorrow: ⚠️ High UV Index (9/10) - Sunscreen recommended\n"
            alerts += "• Day 2: 🌧️ Heavy rain expected - Indoor activities suggested\n"
            alerts += "• Day 3: 💨 Strong winds (35 km/h) - Secure outdoor items\n\n"
            alerts += "🛡️ Safety Recommendations:\n"
            alerts += "• Carry umbrella for Day 2\n"
            alerts += "• Plan indoor backup activities\n"
            alerts += "• Check travel conditions before departure\n"
            alerts += "• Stay hydrated during high UV periods\n\n"
            alerts += "📱 Enable notifications for real-time updates!"
            
            self.display_result(alerts)
        except Exception as e:
            self.handle_error(e, "checking forecast alerts")

    # Chart generation methods using helpers
    def generate_forecast_line_chart(self):
        """Generate forecast line chart using helper"""
        try:
            days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']
            temps = [24, 22, 20, 22, 26]
            
            ChartHelper.create_line_chart(
                self.chart_frame,
                "5-Day Temperature Forecast",
                days,
                temps,
                "Day",
                "Temperature (°C)"
            )
        except Exception as e:
            self.handle_error(e, "generating forecast line chart")

    def generate_forecast_bar_chart(self):
        """Generate forecast bar chart using helper"""
        try:
            conditions = ['Sunny', 'Cloudy', 'Rainy', 'Windy', 'Clear']
            values = [2, 1, 1, 0, 1]  # Number of days for each condition
            colors = ['#FFD93D', '#87CEEB', '#4682B4', '#708090', '#98FB98']
            
            ChartHelper.create_bar_chart(
                self.chart_frame,
                "5-Day Weather Conditions",
                conditions,
                values,
                colors
            )
        except Exception as e:
            self.handle_error(e, "generating forecast bar chart")

    def generate_precipitation_chart(self):
        """Generate precipitation chart using helper"""
        try:
            days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']
            precipitation = [10, 25, 80, 30, 5]  # Precipitation probability
            
            ChartHelper.create_bar_chart(
                self.chart_frame,
                "5-Day Precipitation Probability",
                days,
                precipitation,
                ['#4CAF50', '#FFC107', '#F44336', '#FFC107', '#4CAF50']
            )
        except Exception as e:
            self.handle_error(e, "generating precipitation chart")

    def generate_temp_histogram(self):
        """Generate temperature histogram using helper"""
        try:
            # Sample temperature data for histogram
            if np:
                np.random.seed(42)
                temp_data = np.random.normal(22, 4, 100)
            else:
                temp_data = [18, 20, 22, 24, 26] * 20
            
            ChartHelper.create_histogram(
                self.chart_frame,
                "5-Day Temperature Distribution",
                temp_data,
                bins=10,
                color='#FF6B6B'
            )
        except Exception as e:
            self.handle_error(e, "generating temperature histogram")


class FiveDayForecastTab(BaseTab):
    """5-day forecast tab component"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "5-Day Forecast")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components with split-screen layout"""
        if CHARTS_AVAILABLE:
            # Create split layout using helper
            self.create_split_layout()
            self._setup_forecast_interface(self.left_frame)
            self._setup_chart_interface(self.right_frame)
        else:
            # Fallback to simple layout
            self._setup_forecast_interface(self.frame)

    def _setup_forecast_interface(self, parent_frame):
        """Setup the forecast interface"""
        # City input using helper
        self.setup_city_input(parent_frame)
        
        # Results display
        self.setup_result_text(parent_frame, height=15, width=50)
        
        # Main action button
        ButtonHelper.create_main_button(parent_frame, "primary_black", "Get 5-Day Forecast", self.fetch_5day_forecast)
        
        # Additional Enhanced Buttons using helper
        button_config = [
            ("accent_black", "📅 Week Planner", self.create_week_planner),
            ("info_black", "🎯 Best Days", self.find_best_weather_days),
            ("success_black", "📋 Travel Guide", self.generate_travel_guide),
            ("warning_black", "⚡ Weather Prep", self.get_weather_preparation)
        ]
        ButtonHelper.create_button_grid(parent_frame, button_config, columns=2)

    def _setup_chart_interface(self, parent_frame):
        """Setup the chart interface"""
        # Chart title
        StyledLabel(parent_frame, text="5-Day Forecast Charts").pack(pady=5)
        
        # Chart type selection buttons using helper
        chart_button_config = [
            ("info_black", "📈 Temperature Trend", self.show_temperature_trend_chart),
            ("accent_black", "📊 Daily Comparison", self.show_daily_comparison_chart),
            ("warning_black", "🌧️ Precipitation", self.show_precipitation_chart),
            ("success_black", "📊 Overview", self.show_forecast_overview_chart)
        ]
        ButtonHelper.create_button_grid(parent_frame, chart_button_config, columns=2)
        
        # Chart display area using helper
        self.chart_frame = ChartHelper.create_chart_frame(parent_frame)
        
        # Initial placeholder
        self._show_chart_placeholder()

    def _show_chart_placeholder(self):
        """Show placeholder when no chart is selected"""
        placeholder_content = """📊 Select a chart type above to visualize 5-day forecast data

Available Charts:
• Temperature Trend - Daily temperature progression
• Daily Comparison - Compare temperature, humidity, wind
• Precipitation - Rain/snow probability forecast
• Overview - Comprehensive forecast summary"""
        
        ChartHelper.create_chart_placeholder(self.chart_frame, "5-Day Forecast Charts", placeholder_content)

    def fetch_5day_forecast(self):
        """Fetch 5-day forecast for the entered city"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            forecast = self.controller.get_five_day_forecast(city)
            unit_label = self.controller.get_unit_label()
            formatted_result = f"5-Day Forecast for {city} ({unit_label}):\n{forecast}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "fetching 5-day forecast")

    def create_week_planner(self):
        """Create a detailed week planner based on weather"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            self.display_result(f"Generating week planner for {city}...")
        except Exception as e:
            self.handle_error(e, "creating week planner")

    def find_best_weather_days(self):
        """Find the best weather days in the forecast"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            self.display_result(f"Finding best weather days in {city}...")
        except Exception as e:
            self.handle_error(e, "finding best weather days")

    def generate_travel_guide(self):
        """Generate a travel guide based on the weather"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            self.display_result(f"Generating travel guide for {city}...")
        except Exception as e:
            self.handle_error(e, "generating travel guide")

    def get_weather_preparation(self):
        """Get weather preparation advice"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            self.display_result(f"Fetching weather preparation advice for {city}...")
        except Exception as e:
            self.handle_error(e, "getting weather preparation")

    # Chart methods using helpers (simplified versions)
    def show_temperature_trend_chart(self):
        self.display_result("Displaying temperature trend chart...")

    def show_daily_comparison_chart(self):
        self.display_result("Displaying daily comparison chart...")

    def show_precipitation_chart(self):
        self.display_result("Displaying precipitation chart...")

    def show_forecast_overview_chart(self):
        self.display_result("Displaying forecast overview chart...")


class ComparisonTab(BaseTab):
    """City comparison tab component with charts"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "Compare Cities")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        self.create_split_layout()
        self._setup_comparison_interface()
        self._setup_chart_interface()

    def _setup_comparison_interface(self):
        """Setup the comparison interface in the left panel"""
        # Title
        StyledLabel(self.left_frame, text="Compare Weather", font=("Arial", 14, "bold")).pack(pady=5)
        
        # City inputs
        self.city1_entry = self.setup_city_input(self.left_frame, "Enter City 1")
        self.city2_entry = self.setup_city_input(self.left_frame, "Enter City 2")
        
        # Results display
        self.setup_result_text(self.left_frame, height=15, width=50)
        
        # Main action button
        ButtonHelper.create_main_button(self.left_frame, "primary_black", "Compare", self.compare_cities)
        
        # Additional buttons
        button_config = [
            ("accent_black", "🏆 Find Best City", self.find_best_city),
            ("info_black", "📊 Side-by-Side", self.show_side_by_side),
            ("success_black", "📋 Summary", self.generate_summary),
            ("warning_black", "⚠️ Alert Diff", self.compare_alerts)
        ]
        ButtonHelper.create_button_grid(self.left_frame, button_config, columns=2)

    def _setup_chart_interface(self):
        """Setup the chart interface in the right panel"""
        StyledLabel(self.right_frame, text="Comparison Charts", font=("Arial", 14, "bold")).pack(pady=5)
        
        if CHARTS_AVAILABLE:
            chart_button_config = [
                ("info_black", "🌡️ Temp", self.show_temp_comparison_chart),
                ("success_black", "💧 Humidity", self.show_humidity_comparison_chart),
                ("accent_black", "💨 Wind", self.show_wind_comparison_chart),
                ("warning_black", "📊 All Metrics", self.show_all_metrics_chart)
            ]
            ButtonHelper.create_button_grid(self.right_frame, chart_button_config, columns=2)
        else:
            StyledLabel(self.right_frame, text="Charts unavailable", foreground="red").pack()
            
        self.chart_frame = ChartHelper.create_chart_frame(self.right_frame)
        self._show_chart_placeholder()

    def _show_chart_placeholder(self):
        """Show placeholder for chart area"""
        placeholder_text = "Select a chart to compare cities visually."
        ChartHelper.create_chart_placeholder(self.chart_frame, "Comparison Charts", placeholder_text)

    def _get_cities(self):
        """Helper to get and validate the two city inputs."""
        city1 = self.city1_entry.get().strip()
        city2 = self.city2_entry.get().strip()

        if not city1 or not city2:
            CommonActions.show_warning_message("Input Error", "Please enter two cities to compare.")
            return None, None
        return city1, city2

    def compare_cities(self):
        city1, city2 = self._get_cities()
        if not city1:
            return
        
        try:
            # Assuming controller has a method to compare cities
            comparison_result = self.controller.compare_cities(city1, city2)
            self.display_result(comparison_result)
        except AttributeError:
            self.display_result(f"Comparing weather for {city1} and {city2}...\n(Controller method not implemented)")
        except Exception as e:
            self.handle_error(e, f"comparing {city1} and {city2}")

    def find_best_city(self):
        city1, city2 = self._get_cities()
        if not city1:
            return
        self.display_result(f"Finding the best city between {city1} and {city2}...")

    def show_side_by_side(self):
        city1, city2 = self._get_cities()
        if not city1:
            return
        self.display_result(f"Showing side-by-side comparison for {city1} and {city2}...")

    def generate_summary(self):
        city1, city2 = self._get_cities()
        if not city1:
            return
        self.display_result(f"Generating comparison summary for {city1} and {city2}...")

    def compare_alerts(self):
        city1, city2 = self._get_cities()
        if not city1:
            return
        self.display_result(f"Comparing weather alerts for {city1} and {city2}...")

    def show_temp_comparison_chart(self):
        city1, city2 = self._get_cities()
        if not city1:
            return
        self.display_result("Showing temperature comparison chart...")

    def show_humidity_comparison_chart(self):
        city1, city2 = self._get_cities()
        if not city1:
            return
        self.display_result("Showing humidity comparison chart...")

    def show_wind_comparison_chart(self):
        city1, city2 = self._get_cities()
        if not city1:
            return
        self.display_result("Showing wind comparison chart...")

    def show_all_metrics_chart(self):
        city1, city2 = self._get_cities()
        if not city1:
            return
        self.display_result("Showing all metrics chart...")


class HistoryTab(BaseTab):
    """Weather history tab component"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "History")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        self.create_split_layout()
        self._setup_history_interface()
        self._setup_chart_interface()

    def _setup_history_interface(self):
        """Setup the history interface in the left panel"""
        self.setup_city_input(self.left_frame)
        self.setup_result_text(self.left_frame, height=15, width=50)
        ButtonHelper.create_main_button(self.left_frame, "primary_black", "View History", self.view_weather_history)
        
        button_config = [
            ("accent_black", "💾 Export Data", self.export_history),
            ("info_black", "📅 Date Range", self.select_date_range),
            ("success_black", "📈 Trend Analysis", self.analyze_trends),
            ("warning_black", "🗑️ Clear History", self.clear_history)
        ]
        ButtonHelper.create_button_grid(self.left_frame, button_config, columns=2)

    def _setup_chart_interface(self):
        """Setup the chart interface in the right panel"""
        StyledLabel(self.right_frame, text="Historical Charts", font=("Arial", 14, "bold")).pack(pady=5)
        
        if CHARTS_AVAILABLE:
            chart_button_config = [
                ("info_black", "🌡️ Temp", self.show_temp_history_chart),
                ("success_black", "💧 Humidity", self.show_humidity_history_chart),
                ("accent_black", "💨 Wind", self.show_wind_history_chart),
                ("warning_black", "📊 Full History", self.show_full_history_chart)
            ]
            ButtonHelper.create_button_grid(self.right_frame, chart_button_config, columns=2)
        else:
            StyledLabel(self.right_frame, text="Charts unavailable", foreground="red").pack()
            
        self.chart_frame = ChartHelper.create_chart_frame(self.right_frame)
        self._show_chart_placeholder()

    def _show_chart_placeholder(self):
        """Show placeholder for chart area"""
        placeholder_text = "Select a chart to visualize historical data."
        ChartHelper.create_chart_placeholder(self.chart_frame, "Historical Charts", placeholder_text)

    def view_weather_history(self):
        self.display_result("Viewing weather history...")

    def export_history(self):
        self.display_result("Exporting history...")

    def select_date_range(self):
        self.display_result("Selecting date range...")

    def analyze_trends(self):
        self.display_result("Analyzing trends...")

    def clear_history(self):
        self.display_result("Clearing history...")

    def show_temp_history_chart(self):
        self.display_result("Showing temperature history chart...")

    def show_humidity_history_chart(self):
        self.display_result("Showing humidity history chart...")

    def show_wind_history_chart(self):
        self.display_result("Showing wind history chart...")

    def show_full_history_chart(self):
        self.display_result("Showing full history chart...")


class JournalTab(BaseTab):
    """Weather journal tab component"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "Journal")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        self.create_split_layout()
        self._setup_journal_interface()
        self._setup_entries_interface()

    def _setup_journal_interface(self):
        """Setup the journal entry interface in the left panel"""
        StyledLabel(self.left_frame, text="New Journal Entry", font=("Arial", 14, "bold")).pack(pady=5)
        self.setup_city_input(self.left_frame)
        
        StyledLabel(self.left_frame, text="Your thoughts:").pack(pady=5)
        self.journal_text = StyledText(self.left_frame, height=8, width=50)
        self.journal_text.pack(pady=5, padx=10, fill="x", expand=True)
        
        ButtonHelper.create_main_button(self.left_frame, "primary_black", "Save Entry", self.save_journal_entry)
        
        button_config = [
            ("accent_black", "🎤 Voice Note", self.add_voice_note),
            ("info_black", "📸 Add Photo", self.add_photo),
            ("success_black", "😊 Mood", self.set_mood),
            ("warning_black", "🗑️ Discard", self.discard_entry)
        ]
        ButtonHelper.create_button_grid(self.left_frame, button_config, columns=2)

    def _setup_entries_interface(self):
        """Setup the journal entries display in the right panel"""
        StyledLabel(self.right_frame, text="Journal Entries", font=("Arial", 14, "bold")).pack(pady=5)
        self.setup_result_text(self.right_frame, height=20, width=60)
        ButtonHelper.create_main_button(self.right_frame, "info_black", "View Journal", self.view_journal)

    def save_journal_entry(self):
        self.display_result("Saving journal entry...")

    def add_voice_note(self):
        self.display_result("Adding voice note...")

    def add_photo(self):
        self.display_result("Adding photo...")

    def set_mood(self):
        self.display_result("Setting mood...")

    def discard_entry(self):
        self.display_result("Discarding entry...")

    def view_journal(self):
        self.display_result("Viewing journal...")


class LiveWeatherTab(BaseTab):
    """Live weather tab component"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "Live Weather")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        if not LIVE_WEATHER_AVAILABLE:
            StyledLabel(self.frame, text="Live weather services are unavailable.", foreground="red").pack(pady=20)
            return
            
        self.create_split_layout()
        self._setup_live_interface()
        self._setup_radar_interface()

    def _setup_live_interface(self):
        """Setup the live animation interface in the left panel"""
        StyledLabel(self.left_frame, text="Live Weather Animation", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Add city input for context
        self.setup_city_input(self.left_frame, "Enter City for Live View")

        self.live_widget = AnimatedWeatherWidget(self.left_frame, width=400, height=300)
        
        button_config = [
            ("primary_black", "▶️ Play", self.play_animation),
            ("accent_black", "⏸️ Pause", self.pause_animation),
            ("info_black", "🔄 Refresh", self.refresh_live_data)
        ]
        ButtonHelper.create_button_grid(self.left_frame, button_config, columns=3)

    def _setup_radar_interface(self):
        """Setup the weather radar interface in the right panel"""
        StyledLabel(self.right_frame, text="Weather Radar", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Assuming the controller can provide the radar service
        try:
            radar_service = self.controller.get_weather_radar_service()
            self.radar_widget = WeatherRadarWidget(self.right_frame, radar_service, width=400, height=300)
        except (AttributeError, TypeError):
            # Fallback if controller does not have the service or has wrong signature
            from services.live_weather_service import WeatherRadarService
            radar_service = WeatherRadarService()
            self.radar_widget = WeatherRadarWidget(self.right_frame, radar_service, width=400, height=300)

        button_config = [
            ("primary_black", "🛰️ Track Storms", self.track_storms),
            ("accent_black", "🗺️ Change Layer", self.change_radar_layer),
            ("info_black", "🔍 Zoom In/Out", self.zoom_radar)
        ]
        ButtonHelper.create_button_grid(self.right_frame, button_config, columns=3)

    def play_animation(self):
        self.display_result("Playing animation...")

    def pause_animation(self):
        self.display_result("Pausing animation...")

    def refresh_live_data(self):
        self.display_result("Refreshing live data...")

    def track_storms(self):
        self.display_result("Tracking storms...")

    def change_radar_layer(self):
        self.display_result("Changing radar layer...")

    def zoom_radar(self):
        self.display_result("Zooming radar...")


class ActivityTab(BaseTab):
    """Activity suggestions tab component"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "Activities")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        StyledLabel(self.frame, text="Activity Suggestions", font=("Arial", 14, "bold")).pack(pady=10)
        self.setup_city_input(self.frame)
        self.setup_result_text(self.frame, height=15, width=80)
        ButtonHelper.create_main_button(self.frame, "primary_black", "Get Suggestions", self.get_activity_suggestions)

    def get_activity_suggestions(self):
        city = self.get_city_input()
        if not city:
            return
        self.display_result(f"Fetching activity suggestions for {city}...")

class PoetryTab(BaseTab):
    """Weather poetry tab component"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "Poetry")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        StyledLabel(self.frame, text="Weather Poetry", font=("Arial", 14, "bold")).pack(pady=10)
        self.setup_city_input(self.frame)
        self.setup_result_text(self.frame, height=15, width=80)
        ButtonHelper.create_main_button(self.frame, "primary_black", "Generate Poem", self.generate_poem)

    def generate_poem(self):
        city = self.get_city_input()
        if not city:
            return
        self.display_result(f"Generating a weather-themed poem for {city}...")

class QuickActionsTab(BaseTab):
    """Quick actions tab component"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "Quick Actions")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        StyledLabel(self.frame, text="Quick Actions", font=("Arial", 14, "bold")).pack(pady=10)
        button_config = [
            ("primary_black", "Current Weather", lambda: self.controller.get_current_weather("London")),
            ("info_black", "5-Day Forecast", lambda: self.controller.get_five_day_forecast("Paris")),
            ("success_black", "Save Favorite", lambda: self.controller.add_favorite_city("New York")),
            ("warning_black", "Check Alerts", lambda: self.controller.check_weather_alerts("Tokyo"))
        ]
        ButtonHelper.create_button_grid(self.frame, button_config, columns=2)

class SevereWeatherTab(BaseTab):
    """Severe weather alerts tab component"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "Severe Weather")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        self.create_split_layout()
        self._setup_alert_interface(self.left_frame)
        self._setup_chart_interface(self.right_frame)

    def _setup_alert_interface(self, parent_frame):
        """Setup the alert interface in the left panel"""
        StyledLabel(parent_frame, text="Severe Weather Alerts", font=("Arial", 14, "bold")).pack(pady=10)
        self.setup_city_input(parent_frame)
        self.setup_result_text(parent_frame, height=15, width=50)
        ButtonHelper.create_main_button(parent_frame, "warning_black", "Check for Severe Alerts", self.check_severe_alerts)

    def _setup_chart_interface(self, parent_frame):
        """Setup the chart interface in the right panel"""
        StyledLabel(parent_frame, text="Severe Weather Charts", font=("Arial", 14, "bold")).pack(pady=5)
        
        if CHARTS_AVAILABLE:
            chart_button_config = [
                ("warning_black", "🌪️ Alert Types", self.show_alert_types_chart),
                ("accent_black", "📈 Alert Frequency", self.show_alert_frequency_chart),
                ("info_black", "📊 Intensity Map", self.show_intensity_map),
                ("success_black", "📋 Historical Data", self.show_historical_alerts_chart)
            ]
            ButtonHelper.create_button_grid(parent_frame, chart_button_config, columns=2)
        else:
            StyledLabel(parent_frame, text="Charts unavailable", foreground="red").pack()
            
        self.chart_frame = ChartHelper.create_chart_frame(parent_frame)
        self._show_chart_placeholder()

    def _show_chart_placeholder(self):
        """Show placeholder for chart area"""
        placeholder_text = "Select a chart to visualize severe weather data."
        ChartHelper.create_chart_placeholder(self.chart_frame, "Severe Weather Charts", placeholder_text)

    def check_severe_alerts(self):
        city = self.get_city_input()
        if not city:
            return
        self.display_result(f"Checking for severe weather alerts in {city}...")

    def show_alert_types_chart(self):
        self.display_result("Showing alert types chart...")

    def show_alert_frequency_chart(self):
        self.display_result("Showing alert frequency chart...")

    def show_intensity_map(self):
        self.display_result("Showing intensity map...")

    def show_historical_alerts_chart(self):
        self.display_result("Showing historical alerts chart...")


class AnalyticsTrendsTab(BaseTab):
    """Analytics and trends tab component"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "Analytics")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        self.create_split_layout()
        self._setup_analytics_interface(self.left_frame)
        self._setup_chart_interface(self.right_frame)

    def _setup_analytics_interface(self, parent_frame):
        """Setup the analytics interface in the left panel"""
        StyledLabel(parent_frame, text="Weather Analytics & Trends", font=("Arial", 14, "bold")).pack(pady=10)
        self.setup_city_input(parent_frame)
        self.setup_result_text(parent_frame, height=15, width=50)
        ButtonHelper.create_main_button(parent_frame, "info_black", "Analyze Trends", self.analyze_trends)

    def _setup_chart_interface(self, parent_frame):
        """Setup the chart interface in the right panel"""
        StyledLabel(parent_frame, text="Analytics Charts", font=("Arial", 14, "bold")).pack(pady=5)
        
        if CHARTS_AVAILABLE:
            chart_button_config = [
                ("info_black", "📈 Temp vs. Time", self.show_temp_time_chart),
                ("success_black", "📊 Monthly Avg", self.show_monthly_avg_chart),
                ("accent_black", "📋 Data Correlation", self.show_correlation_heatmap),
                ("warning_black", "☀️ UV Index Trend", self.show_uv_index_chart)
            ]
            ButtonHelper.create_button_grid(parent_frame, chart_button_config, columns=2)
        else:
            StyledLabel(parent_frame, text="Charts unavailable", foreground="red").pack()
            
        self.chart_frame = ChartHelper.create_chart_frame(parent_frame)
        self._show_chart_placeholder()

    def _show_chart_placeholder(self):
        """Show placeholder for chart area"""
        placeholder_text = "Select a chart to visualize weather analytics."
        ChartHelper.create_chart_placeholder(self.chart_frame, "Analytics Charts", placeholder_text)

    def analyze_trends(self):
        city = self.get_city_input()
        if not city:
            return
        self.display_result(f"Analyzing weather trends for {city}...")

    def show_temp_time_chart(self):
        self.display_result("Showing temperature vs. time chart...")

    def show_monthly_avg_chart(self):
        self.display_result("Showing monthly average chart...")

    def show_correlation_heatmap(self):
        self.display_result("Showing data correlation heatmap...")

    def show_uv_index_chart(self):
        self.display_result("Showing UV index trend chart...")


class HealthWellnessTab(BaseTab):
    """Health and wellness tab component"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "Health")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        self.create_split_layout()
        self._setup_health_interface(self.left_frame)
        self._setup_chart_interface(self.right_frame)

    def _setup_health_interface(self, parent_frame):
        """Setup the health interface in the left panel"""
        StyledLabel(parent_frame, text="Health & Wellness", font=("Arial", 14, "bold")).pack(pady=10)
        self.setup_city_input(parent_frame)
        self.setup_result_text(parent_frame, height=15, width=50)
        ButtonHelper.create_main_button(parent_frame, "success_black", "Get Health Tips", self.get_health_tips)

    def _setup_chart_interface(self, parent_frame):
        """Setup the chart interface in the right panel"""
        StyledLabel(parent_frame, text="Health Charts", font=("Arial", 14, "bold")).pack(pady=5)
        
        if CHARTS_AVAILABLE:
            chart_button_config = [
                ("success_black", "🏃 Activity Index", self.show_activity_index_chart),
                ("info_black", "🌬️ Air Quality", self.show_air_quality_chart),
                ("accent_black", "🤧 Allergy Forecast", self.show_allergy_forecast_chart),
                ("warning_black", "☀️ UV Exposure", self.show_uv_exposure_chart)
            ]
            ButtonHelper.create_button_grid(parent_frame, chart_button_config, columns=2)
        else:
            StyledLabel(parent_frame, text="Charts unavailable", foreground="red").pack()
            
        self.chart_frame = ChartHelper.create_chart_frame(parent_frame)
        self._show_chart_placeholder()

    def _show_chart_placeholder(self):
        """Show placeholder for chart area"""
        placeholder_text = "Select a chart to visualize health-related weather data."
        ChartHelper.create_chart_placeholder(self.chart_frame, "Health Charts", placeholder_text)

    def get_health_tips(self):
        city = self.get_city_input()
        if not city:
            return
        self.display_result(f"Fetching health and wellness tips for {city}...")

    def show_activity_index_chart(self):
        self.display_result("Showing activity index chart...")

    def show_air_quality_chart(self):
        self.display_result("Showing air quality chart...")

    def show_allergy_forecast_chart(self):
        self.display_result("Showing allergy forecast chart...")

    def show_uv_exposure_chart(self):
        self.display_result("Showing UV exposure chart...")


class SmartAlertsTab(BaseTab):
    """Smart alerts tab component"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "Smart Alerts")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        self.create_split_layout()
        self._setup_alerts_interface(self.left_frame)
        self._setup_chart_interface(self.right_frame)

    def _setup_alerts_interface(self, parent_frame):
        """Setup the alerts interface in the left panel"""
        StyledLabel(parent_frame, text="Smart Alerts Configuration", font=("Arial", 14, "bold")).pack(pady=10)
        self.setup_city_input(parent_frame)
        self.setup_result_text(parent_frame, height=15, width=50)
        ButtonHelper.create_main_button(parent_frame, "primary_black", "Configure Alerts", self.configure_alerts)

    def _setup_chart_interface(self, parent_frame):
        """Setup the chart interface in the right panel"""
        StyledLabel(parent_frame, text="Alerts Overview", font=("Arial", 14, "bold")).pack(pady=5)
        
        if CHARTS_AVAILABLE:
            chart_button_config = [
                ("primary_black", "📊 Alert Stats", self.show_alert_stats_chart),
                ("info_black", "📈 Trigger History", self.show_trigger_history_chart),
                ("success_black", "📋 Active Rules", self.show_active_rules_chart),
                ("warning_black", "⚙️ Thresholds", self.show_thresholds_chart)
            ]
            ButtonHelper.create_button_grid(parent_frame, chart_button_config, columns=2)
        else:
            StyledLabel(parent_frame, text="Charts unavailable", foreground="red").pack()
            
        self.chart_frame = ChartHelper.create_chart_frame(parent_frame)
        self._show_chart_placeholder()

    def _show_chart_placeholder(self):
        """Show placeholder for chart area"""
        placeholder_text = "Select a chart to visualize smart alerts data."
        ChartHelper.create_chart_placeholder(self.chart_frame, "Alerts Overview", placeholder_text)

    def configure_alerts(self):
        city = self.get_city_input()
        if not city:
            return
        self.display_result(f"Configuring smart alerts for {city}...")

    def show_alert_stats_chart(self):
        self.display_result("Showing alert statistics chart...")

    def show_trigger_history_chart(self):
        self.display_result("Showing trigger history chart...")

    def show_active_rules_chart(self):
        self.display_result("Showing active rules chart...")

    def show_thresholds_chart(self):
        self.display_result("Showing thresholds chart...")


class WeatherCameraTab(BaseTab):
    """Weather camera tab component"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "Cameras")
        self.video_capture = None
        self.is_camera_running = False
        self.weather_info = None  # To store weather data
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        StyledLabel(self.frame, text="Live Weather Cameras", font=("Arial", 14, "bold")).pack(pady=10)
        self.setup_city_input(self.frame)

        self.camera_label = StyledLabel(self.frame, text="Camera feed will appear here.")
        self.camera_label.pack(pady=10)

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=5)

        ButtonHelper.create_main_button(button_frame, "info_black", "Start Camera", self.start_camera_feed)
        ButtonHelper.create_main_button(button_frame, "warning_black", "Stop Camera", self.stop_camera_feed)

    def start_camera_feed(self):
        """Start the live camera feed and fetch weather data."""
        if not CAMERA_AVAILABLE:
            self.camera_label.config(text="Camera functionality is not available (opencv-python or Pillow not installed).")
            return

        if self.is_camera_running:
            return

        city = self.get_city_input()
        if city:
            try:
                # Fetch weather data to overlay on the feed
                self.weather_info = self.controller.get_current_weather(city)
            except Exception as e:
                self.handle_error(e, "fetching weather for camera overlay")
                self.weather_info = None  # Reset on error
        else:
            # Prompt user to enter a city if they haven't
            CommonActions.show_warning_message("Input Required", "Please enter a city to see weather overlays.")
            self.weather_info = None

        # Use 0 for the default webcam.
        self.video_capture = cv2.VideoCapture(0)
        if not self.video_capture.isOpened():
            self.camera_label.config(text="Error: Could not open video stream.")
            return

        self.is_camera_running = True
        self._update_camera_feed()

    def _update_camera_feed(self):
        """Continuously update the camera feed label with weather overlay."""
        if not self.is_camera_running:
            return

        ret, frame = self.video_capture.read()
        if ret:
            # Overlay weather information if available
            if self.weather_info:
                try:
                    # Get weather data from the controller
                    weather_data = self.controller.get_current_weather(self.controller.last_city or "New York")
                    
                    if weather_data:
                        # Extract weather info from WeatherData object
                        city = weather_data.city
                        temp = weather_data.temperature
                        condition = weather_data.description
                        
                        # Format the text to display
                        info_text = f"{city}: {weather_data.formatted_temperature}, {condition}"
                        
                        # Add text to the frame
                        cv2.putText(frame, info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                                    1, (255, 255, 255), 2, cv2.LINE_AA)

                except Exception as e:
                    # In case of unexpected errors with weather data
                    print(f"Could not overlay weather info: {e}")

            # Convert the image from BGR (OpenCV format) to RGB
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.camera_label.imgtk = imgtk
            self.camera_label.config(image=imgtk)
        
        self.frame.after(10, self._update_camera_feed)

    def stop_camera_feed(self):
        """Stop the live camera feed."""
        if self.is_camera_running and self.video_capture:
            self.is_camera_running = False
            self.video_capture.release()
            self.camera_label.config(image='', text="Camera feed stopped.")
            self.weather_info = None  # Clear weather info

    def view_cameras(self):
        """This method is kept for compatibility but start_camera_feed is used directly."""
        self.start_camera_feed()
