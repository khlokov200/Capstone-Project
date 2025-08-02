"""
Individual tab components for the weather dashboard - Refactored to reduce duplication
"""
import tkinter as tk
from tkinter import ttk, messagebox
import random
import matplotlib.pyplot as plt
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
                x_label="Metric",
                y_label="Value",
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
                colors,
                x_label="Condition",
                y_label="Number of Days"
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
                ['#4CAF50', '#FFC107', '#F44336', '#FFC107', '#4CAF50'],
                x_label="Day",
                y_label="Probability (%)"
            )
        except Exception as e:
            self.handle_error(e, "generating precipitation chart")

    def generate_temp_histogram(self):
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
                colors,
                x_label="Condition",
                y_label="Number of Days"
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
                ['#4CAF50', '#FFC107', '#F44336', '#FFC107', '#4CAF50'],
                x_label="Day",
                y_label="Probability (%)"
            )
        except Exception as e:
            self.handle_error(e, "generating precipitation chart")

    def generate_temp_histogram(self):
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
                colors,
                x_label="Condition",
                y_label="Number of Days"
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
                ['#4CAF50', '#FFC107', '#F44336', '#FFC107', '#4CAF50'],
                x_label="Day",
                y_label="Probability (%)"
            )
        except Exception as e:
            self.handle_error(e, "generating precipitation chart")

    def generate_temp_histogram(self):
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
            result = self.controller.get_week_planner(city)
            self.display_result(result)
        except Exception as e:
            self.handle_error(e, "creating week planner")

    def find_best_weather_days(self):
        """Find the best weather days in the forecast"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            result = self.controller.find_best_times(city)
            self.display_result(result)
        except Exception as e:
            self.handle_error(e, "finding best weather days")

    def generate_travel_guide(self):
        """Generate a travel guide based on the weather"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            result = self.controller.get_weather_summary(city)
            self.display_result(result)
        except Exception as e:
            self.handle_error(e, "generating travel guide")

    def get_weather_preparation(self):
        """Get weather preparation advice"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            result = self.controller.get_emergency_preparedness(city)
            self.display_result(result)
        except Exception as e:
            self.handle_error(e, "getting weather preparation")

    # Chart methods using helpers (simplified versions)
    def show_temperature_trend_chart(self):
        """Generate and display a 5-day temperature trend chart."""
        city = self.get_city_input()
        if not city:
            return
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available (matplotlib not installed).")
            return
        try:
            # In a real app, you'd fetch this data from the controller
            days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']
            temps = [random.randint(15, 25) for _ in range(5)] # Dummy data
            ChartHelper.create_line_chart(
                self.chart_frame,
                f"5-Day Temperature Trend for {city}",
                days,
                temps,
                "Day",
                f"Temperature ({self.controller.get_unit_label()})"
            )
        except Exception as e:
            self.handle_error(e, "generating temperature trend chart")

    def show_daily_comparison_chart(self):
        """Generate and display a daily comparison bar chart."""
        city = self.get_city_input()
        if not city:
            return
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available (matplotlib not installed).")
            return
        try:
            # Dummy data for comparison
            days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']
            temps = [random.randint(15, 25) for _ in range(5)]
            humidity = [random.randint(40, 80) for _ in range(5)]
            
            ChartHelper.create_grouped_bar_chart(
                self.chart_frame,
                f"Daily Comparison for {city}",
                days,
                {'Temperature (°C)': temps, 'Humidity (%)': humidity},
                "Day",
                "Value"
            )
        except Exception as e:
            self.handle_error(e, "generating daily comparison chart")


    def show_precipitation_chart(self):
        """Generate and display a 5-day precipitation probability chart."""
        city = self.get_city_input()
        if not city:
            return
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available (matplotlib not installed).")
            return
        try:
            days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']
            precipitation = [random.randint(0, 100) for _ in range(5)]
            ChartHelper.create_bar_chart(
                self.chart_frame,
                f"5-Day Precipitation Probability for {city}",
                days,
                precipitation,
                colors=['#3498db'],
                x_label="Day",
                y_label="Probability (%)"
            )
        except Exception as e:
            self.handle_error(e, "generating precipitation chart")

    def show_forecast_overview_chart(self):
        """Generate and display a forecast overview pie chart."""
        city = self.get_city_input()
        if not city:
            return
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available (matplotlib not installed).")
            return
        try:
            # Dummy data for overview
            conditions = ['Sunny', 'Cloudy', 'Rainy', 'Partly Cloudy']
            counts = [random.randint(1, 5) for _ in range(4)]
            
            ChartHelper.create_pie_chart(
                self.chart_frame,
                f"5-Day Weather Overview for {city}",
                labels=conditions,
                sizes=counts
            )
        except Exception as e:
            self.handle_error(e, "generating forecast overview chart")


class ComparisonTab(BaseTab):
    """City comparison tab component with charts"""
    
    def __init__(self, notebook, controller):
        BaseTab.setup_whitespace_style()
        super().__init__(notebook, controller, "Compare Cities")
        self.frame.configure(style="Whitespace.TFrame")
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
            # Fallback for when the method doesn't exist on the controller
            weather1 = self.controller.get_current_weather(city1)
            weather2 = self.controller.get_current_weather(city2)
            
            result = f"Comparison for {city1} vs {city2}:\n"
            result += f"Temp: {weather1.formatted_temperature} vs {weather2.formatted_temperature}\n"
            result += f"Humidity: {weather1.humidity}% vs {weather2.humidity}%\n"
            result += f"Wind: {weather1.formatted_wind} vs {weather2.formatted_wind}"
            self.display_result(result)
        except Exception as e:
            self.handle_error(e, f"comparing {city1} and {city2}")

    def find_best_city(self):
        city1, city2 = self._get_cities()
        if not city1:
            return
        try:
            result = self.controller.find_best_city(city1, city2)
            self.display_result(result)
        except Exception as e:
            self.handle_error(e, "finding best city")

    def show_side_by_side(self):
        city1, city2 = self._get_cities()
        if not city1:
            return
        try:
            result = self.controller.compare_cities(city1, city2)
            self.display_result(result)
        except Exception as e:
            self.handle_error(e, "showing side-by-side comparison")

    def generate_summary(self):
        city1, city2 = self._get_cities()
        if not city1:
            return
        try:
            summary1 = self.controller.get_weather_summary(city1)
            summary2 = self.controller.get_weather_summary(city2)
            self.display_result(f"--- Summary for {city1} ---\n{summary1}\n\n--- Summary for {city2} ---\n{summary2}")
        except Exception as e:
            self.handle_error(e, "generating comparison summary")

    def compare_alerts(self):
        city1, city2 = self._get_cities()
        if not city1:
            return
        try:
            alerts1 = self.controller.check_weather_alerts(city1)
            alerts2 = self.controller.check_weather_alerts(city2)
            self.display_result(f"--- Alerts for {city1} ---\n{alerts1}\n\n--- Alerts for {city2} ---\n{alerts2}")
        except Exception as e:
            self.handle_error(e, "comparing weather alerts")

    def show_temp_comparison_chart(self):
        """Shows a bar chart comparing temperatures of two cities."""
        city1, city2 = self._get_cities()
        if not city1 or not city2:
            return
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            temps = [random.randint(10, 30) for _ in range(2)]
            cities = [city1, city2]
            ChartHelper.create_bar_chart(
                self.chart_frame,
                f"Temperature Comparison: {city1} vs {city2}",
                cities,
                temps,
                ['#FF6B6B', '#4ECDC4'],
                "City",
                f"Temperature ({self.controller.get_unit_label()})"
            )
        except Exception as e:
            self.handle_error(e, "generating temperature comparison chart")

    def show_humidity_comparison_chart(self):
        """Shows a bar chart comparing humidity of two cities."""
        city1, city2 = self._get_cities()
        if not city1 or not city2:
            return
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            humidity = [random.randint(30, 90) for _ in range(2)]
            cities = [city1, city2]
            ChartHelper.create_bar_chart(
                self.chart_frame,
                f"Humidity Comparison: {city1} vs {city2}",
                cities,
                humidity,
                ['#45B7D1', '#96CEB4'],
                "City",
                "Humidity (%)"
            )
        except Exception as e:
            self.handle_error(e, "generating humidity comparison chart")

    def show_wind_comparison_chart(self):
        """Shows a bar chart comparing wind speed of two cities."""
        city1, city2 = self._get_cities()
        if not city1 or not city2:
            return
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            wind_speeds = [random.randint(0, 20) for _ in range(2)]
            cities = [city1, city2]
            ChartHelper.create_bar_chart(
                self.chart_frame,
                f"Wind Speed Comparison: {city1} vs {city2}",
                cities,
                wind_speeds,
                ['#FECA57', '#F3A683'],
                "City",
                "Wind Speed (m/s)"
            )
        except Exception as e:
            self.handle_error(e, "generating wind comparison chart")

    def show_all_metrics_chart(self):
        """Shows a grouped bar chart for all metrics."""
        city1, city2 = self._get_cities()
        if not city1 or not city2:
            return
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            metrics = {
                'Temperature': [random.randint(10, 30) for _ in range(2)],
                'Humidity': [random.randint(30, 90) for _ in range(2)],
                'Wind Speed': [random.randint(0, 20) for _ in range(2)]
            }
            ChartHelper.create_grouped_bar_chart(
                self.chart_frame,
                f"All Metrics: {city1} vs {city2}",
                [city1, city2],
                metrics,
                "City",
                "Value"
            )
        except Exception as e:
            self.handle_error(e, "generating all metrics chart")


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
        city = self.get_city_input()
        if not city:
            return
        try:
            history = self.controller.get_weather_history(city)
            self.display_result(history)
        except Exception as e:
            self.handle_error(e, "viewing weather history")

    def export_history(self):
        city = self.get_city_input()
        if not city:
            return
        try:
            result = self.controller.export_weather_data(city)
            self.display_result(result)
        except Exception as e:
            self.handle_error(e, "exporting history")

    def select_date_range(self):
        # This would require a date picker, for now, it's a placeholder
        CommonActions.show_info_message("Feature Not Implemented", "Date range selection is not yet implemented.")

    def analyze_trends(self):
        city = self.get_city_input()
        if not city:
            return
        try:
            trends = self.controller.get_weather_trends(city)
            self.display_result(trends)
        except Exception as e:
            self.handle_error(e, "analyzing trends")

    def clear_history(self):
        try:
            result = self.controller.clear_weather_history()
            self.display_result(result)
        except Exception as e:
            self.handle_error(e, "clearing history")

    def show_temp_history_chart(self):
        """Shows a line chart for temperature history."""
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            dates = [f"Day {i}" for i in range(1, 8)]
            temps = [random.randint(10, 25) for _ in range(7)]
            ChartHelper.create_line_chart(
                self.chart_frame,
                "Temperature History (Last 7 Days)",
                dates,
                temps,
                "Date",
                f"Temperature ({self.controller.get_unit_label()})"
            )
        except Exception as e:
            self.handle_error(e, "generating temperature history chart")

    def show_humidity_history_chart(self):
        """Shows a line chart for humidity history."""
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            dates = [f"Day {i}" for i in range(1, 8)]
            humidity = [random.randint(40, 80) for _ in range(7)]
            ChartHelper.create_line_chart(
                self.chart_frame,
                "Humidity History (Last 7 Days)",
                dates,
                humidity,
                "Date",
                "Humidity (%)"
            )
        except Exception as e:
            self.handle_error(e, "generating humidity history chart")

    def show_wind_history_chart(self):
        """Shows a line chart for wind speed history."""
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            dates = [f"Day {i}" for i in range(1, 8)]
            wind = [random.randint(0, 15) for _ in range(7)]
            ChartHelper.create_line_chart(
                self.chart_frame,
                "Wind Speed History (Last 7 Days)",
                dates,
                wind,
                "Date",
                "Wind Speed (m/s)"
            )
        except Exception as e:
            self.handle_error(e, "generating wind history chart")

    def show_full_history_chart(self):
        """Shows a complex chart with multiple historical metrics."""
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            dates = [f"Day {i}" for i in range(1, 8)]
            temps = [random.randint(10, 25) for _ in range(7)]
            humidity = [random.randint(40, 80) for _ in range(7)]
            
            fig, ax1 = plt.subplots(figsize=(8, 4))

            color = 'tab:red'
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Temperature', color=color)
            ax1.plot(dates, temps, color=color, marker='o')
            ax1.tick_params(axis='y', labelcolor=color)

            ax2 = ax1.twinx()
            color = 'tab:blue'
            ax2.set_ylabel('Humidity (%)', color=color)
            ax2.plot(dates, humidity, color=color, marker='x')
            ax2.tick_params(axis='y', labelcolor=color)

            fig.tight_layout()
            ChartHelper.embed_chart_in_frame(fig, self.chart_frame)
        except Exception as e:
            self.handle_error(e, "generating full history chart")


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
        entry_text = self.journal_text.get("1.0", tk.END).strip()
        if not entry_text:
            CommonActions.show_warning_message("Input Error", "Journal entry cannot be empty.")
            return
        try:
            # Assuming a simple mood for now, can be expanded
            self.controller.save_journal_entry(entry_text, "neutral")
            self.display_result("Journal entry saved successfully.")
            self.journal_text.delete("1.0", tk.END) # Clear the text box
        except Exception as e:
            self.handle_error(e, "saving journal entry")

    def add_voice_note(self):
        CommonActions.show_info_message("Feature Not Implemented", "Voice note functionality is not yet implemented.")

    def add_photo(self):
        CommonActions.show_info_message("Feature Not Implemented", "Adding photos is not yet implemented.")

    def set_mood(self):
        CommonActions.show_info_message("Feature Not Implemented", "Mood setting is not yet implemented.")

    def discard_entry(self):
        self.journal_text.delete("1.0", tk.END)
        self.display_result("Journal entry discarded.")

    def view_journal(self):
        try:
            entries = self.controller.journal_service.load_entries()
            if not entries:
                self.display_result("No journal entries found.")
                return
            
            formatted_entries = "\n\n".join([f"[{entry['timestamp']}] - Mood: {entry['mood']}\n{entry['text']}" for entry in entries])
            self.display_result(formatted_entries)
        except Exception as e:
            self.handle_error(e, "viewing journal")


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
        

        # Add city input for context with Enter button
        city_input_frame = ttk.Frame(self.left_frame)
        city_input_frame.pack(pady=(10, 0))
        StyledLabel(city_input_frame, text="Enter City for Live View").pack(side="left", padx=(0, 5))
        self.city_entry = ttk.Entry(city_input_frame)
        self.city_entry.pack(side="left")
        enter_btn = ttk.Button(city_input_frame, text="Enter", command=self._on_enter_city)
        enter_btn.pack(side="left", padx=(5, 0))

    def _on_enter_city(self):
        city = self.get_city_input()
        if city:
            # Fetch weather type for the city
            try:
                weather = self.controller.get_current_weather(city)
                # Try to get a weather type string for animation
                weather_type = None
                desc = (weather.description or '').lower() if hasattr(weather, 'description') else ''
                if 'rain' in desc:
                    weather_type = 'rain'
                elif 'storm' in desc or 'thunder' in desc:
                    weather_type = 'storm'
                elif 'snow' in desc or 'blizzard' in desc:
                    weather_type = 'snow'
                elif 'cloud' in desc:
                    weather_type = 'cloudy'
                elif 'clear' in desc or 'sun' in desc:
                    weather_type = 'clear'
                else:
                    weather_type = 'clear'
                if hasattr(self, 'live_widget'):
                    self.live_widget.update_weather(weather_type)
                    self.live_widget.start_animation(weather_type)
                self.display_result(f"City set for live view: {city}\nWeather: {weather.description}")
            except Exception as e:
                self.display_result(f"❌ Could not fetch weather for {city}: {e}")


        self.live_widget = AnimatedWeatherWidget(self.left_frame, width=400, height=300)

        # Add legend below the animation
        legend_frame = ttk.LabelFrame(self.left_frame, text="Legend")
        legend_frame.pack(pady=(5, 10), fill="x")
        legend_items = [
            ("blue", "Walker"),
            ("green", "Jogger"),
            ("purple", "Elderly"),
            ("red", "Cyclist"),
            ("blue", "Rain Drop"),
            ("white", "Snowflake"),
            ("yellow", "Lightning"),
            ("darkblue", "Heavy Rain")
        ]
        for color, label in legend_items:
            item_frame = ttk.Frame(legend_frame)
            item_frame.pack(anchor="w", padx=8, pady=1)
            color_box = tk.Canvas(item_frame, width=16, height=16, highlightthickness=0)
            color_box.pack(side="left")
            if color == "white":
                color_box.create_oval(2, 2, 14, 14, fill=color, outline="lightgray")
            elif color == "yellow":
                color_box.create_line(2, 14, 14, 2, fill=color, width=3)
            elif color == "darkblue":
                color_box.create_line(2, 2, 14, 14, fill=color, width=3)
            else:
                color_box.create_oval(2, 2, 14, 14, fill=color, outline="black")
            ttk.Label(item_frame, text=label, font=("Arial", 9)).pack(side="left", padx=6)

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

        # Add radar legend below the radar widget
        radar_legend_frame = ttk.LabelFrame(self.right_frame, text="Legend")
        radar_legend_frame.pack(pady=(5, 10), fill="x")
        radar_legend_items = [
            ("red", "Severe (🔴)"),
            ("orange", "Heavy (🟠)"),
            ("yellow", "Moderate (🟡)"),
            ("green", "Light (🟢)"),
            ("white", "Clear (⚪)"),
            ("blue", "Rain"),
            ("purple", "Snow"),
            ("gray", "Cloudy"),
            ("*", "Severe Weather Event (Red Star)")
        ]
        for color, label in radar_legend_items:
            item_frame = ttk.Frame(radar_legend_frame)
            item_frame.pack(anchor="w", padx=8, pady=1)
            color_box = tk.Canvas(item_frame, width=16, height=16, highlightthickness=0)
            color_box.pack(side="left")
            if color == "white":
                color_box.create_oval(2, 2, 14, 14, fill=color, outline="lightgray")
            elif color == "*":
                # Draw a red star for severe event
                color_box.create_text(8, 8, text="*", fill="red", font=("Arial", 12, "bold"))
            else:
                color_box.create_oval(2, 2, 14, 14, fill=color, outline="black")
            ttk.Label(item_frame, text=label, font=("Arial", 9)).pack(side="left", padx=6)

        button_config = [
            ("primary_black", "🛰️ Track Storms", self.track_storms),
            ("accent_black", "🗺️ Change Layer", self.change_radar_layer),
            ("info_black", "🔍 Zoom In/Out", self.zoom_radar)
        ]
        ButtonHelper.create_button_grid(self.right_frame, button_config, columns=3)

    def play_animation(self):
        if hasattr(self, 'live_widget'):
            self.live_widget.start_animation()
            self.display_result("▶️ Live animation started.")
        else:
            self.display_result("Live animation widget not available.")

    def pause_animation(self):
        if hasattr(self, 'live_widget'):
            self.live_widget.stop_animation()
            self.display_result("⏸️ Live animation paused.")
        else:
            self.display_result("Live animation widget not available.")

    def refresh_live_data(self):
        result = self.controller.refresh_live_data()
        self.display_result(result)

    def track_storms(self):
        city = self.get_city_input()
        if not city:
            return
        result = self.controller.track_severe_weather(city)
        self.display_result(result)

    def change_radar_layer(self):
        result = self.controller.switch_live_view()
        self.display_result(result)

    def zoom_radar(self):
        result = self.controller.zoom_radar()
        self.display_result(result)


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
        try:
            suggestions = self.controller.suggest_activity(city)
            self.display_result(suggestions)
        except Exception as e:
            self.handle_error(e, "fetching activity suggestions")

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
        ButtonHelper.create_main_button(self.frame, "primary_black", "Generate Haiku", self.generate_haiku)
        ButtonHelper.create_main_button(self.frame, "primary_black", "Generate Sonnet", self.generate_sonnet)
        ButtonHelper.create_main_button(self.frame, "primary_black", "Generate Limerick", self.generate_limerick)
        ButtonHelper.create_main_button(self.frame, "primary_black", "Generate Free Verse", self.generate_free_verse)
        ButtonHelper.create_main_button(self.frame, "primary_black", "Generate Acrostic", self.generate_acrostic)
        ButtonHelper.create_main_button(self.frame, "primary_black", "Weather Riddle", self.generate_riddle)
        ButtonHelper.create_main_button(self.frame, "primary_black", "Interactive Prompt", self.generate_interactive_prompt)

    def generate_haiku(self):
        city = self.get_city_input()
        if not city:
            return
        try:
            poem = self.controller.generate_weather_haiku(city)
            self.display_result(poem)
        except Exception as e:
            self.handle_error(e, "generating a haiku")

    def generate_sonnet(self):
        city = self.get_city_input()
        if not city:
            return
        try:
            poem = self.controller.generate_weather_sonnet(city)
            self.display_result(poem)
        except Exception as e:
            self.handle_error(e, "generating a sonnet")

    def generate_limerick(self):
        city = self.get_city_input()
        if not city:
            return
        try:
            poem = self.controller.generate_weather_limerick(city)
            self.display_result(poem)
        except Exception as e:
            self.handle_error(e, "generating a limerick")

    def generate_free_verse(self):
        city = self.get_city_input()
        if not city:
            return
        try:
            poem = self.controller.generate_weather_free_verse(city)
            self.display_result(poem)
        except Exception as e:
            self.handle_error(e, "generating free verse")

    def generate_acrostic(self):
        city = self.get_city_input()
        if not city:
            return
        try:
            poem = self.controller.generate_acrostic(city)
            self.display_result(poem)
        except Exception as e:
            self.handle_error(e, "generating acrostic poem")

    def generate_riddle(self):
        city = self.get_city_input()
        if not city:
            return
        try:
            riddle = self.controller.generate_weather_riddle(city)
            self.display_result(riddle)
        except Exception as e:
            self.handle_error(e, "generating weather riddle")

    def generate_interactive_prompt(self):
        city = self.get_city_input()
        if not city:
            return
        try:
            prompt = self.controller.generate_interactive_prompt(city)
            self.display_result(prompt)
        except Exception as e:
            self.handle_error(e, "generating interactive prompt")
    def generate_poem(self):
        city = self.get_city_input()
        if not city:
            return
        try:
            poem = self.controller.generate_poem(city)
            self.display_result(poem)
        except Exception as e:
            self.handle_error(e, "generating a weather-themed poem")

class QuickActionsTab(BaseTab):
    def _cycle_bg_color(self):
        """Cycle the background color of the entire Quick Actions tab using ttk style."""
        self._bg_color_index = (self._bg_color_index + 1) % len(self._bg_colors)
        new_color = self._bg_colors[self._bg_color_index]
        style = ttk.Style()
        style_name = "QuickActionsTab.TFrame"
        style.configure(style_name, background=new_color)
        self.frame.configure(style=style_name)
    """Quick actions tab component for instant access to all major features"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "🚀 Quick Actions")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the quick actions UI components"""
        # Title
        title_label = StyledLabel(self.frame, text="🚀 Quick Actions Dashboard")
        title_label.configure(font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Description
        desc_label = StyledLabel(self.frame, 
                                text="Instant access to all major weather dashboard features")
        desc_label.pack(pady=5)
        
        # Main actions container
        self.main_container = tk.Frame(self.frame)
        self.main_container.pack(pady=20, padx=20, fill="both", expand=True)
        # Background color changer button (add after all other UI setup)
        self._bg_colors = ["#f0f4f8", "#e0e7ef", "#ffe4e1", "#e6ffe6", "#e6f7ff", "#fffbe6", "#f5e6ff", "#262a32", "#23272e"]
        self._bg_color_index = 0
        StyledButton(self.frame, "accent_black", text="🎨 Change Background Color", command=self._cycle_bg_color).pack(pady=5)
    def _setup_ui(self):
        """Setup the quick actions UI components"""
        # Title
        title_label = StyledLabel(self.frame, text="🚀 Quick Actions Dashboard")
        title_label.configure(font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Description
        desc_label = StyledLabel(self.frame, 
                                text="Instant access to all major weather dashboard features")
        desc_label.pack(pady=5)
        
        # Main actions container
        main_container = ttk.Frame(self.frame)
        main_container.pack(pady=20, padx=20, fill="both", expand=True)

        # Weather Actions Section
        weather_frame = ttk.LabelFrame(main_container, text="🌤️ Weather Actions", padding=15)
        weather_frame.pack(fill="x", pady=10)
        weather_row1 = ttk.Frame(weather_frame)
        weather_row1.pack(pady=5)
        StyledButton(weather_row1, "primary_black", text="🌡️ Quick Weather", command=self._quick_weather, width=15).grid(row=0, column=0, padx=5)
        StyledButton(weather_row1, "info_black", text="📅 Today's Plan", command=self._todays_plan, width=15).grid(row=0, column=1, padx=5)
        StyledButton(weather_row1, "cool_black", text="🎯 Best Times", command=self._best_times, width=15).grid(row=0, column=2, padx=5)

        # Utility Actions Section
        utility_frame = ttk.LabelFrame(main_container, text="🔧 Utility Actions", padding=15)
        utility_frame.pack(fill="x", pady=10)
        utility_row1 = ttk.Frame(utility_frame)
        utility_row1.pack(pady=5)
        StyledButton(utility_row1, "accent_black", text="📱 Share Weather", command=self._share_weather, width=15).grid(row=0, column=0, padx=5)
        StyledButton(utility_row1, "success_black", text="⭐ Save Favorite", command=self._save_favorite, width=15).grid(row=0, column=1, padx=5)
        StyledButton(utility_row1, "warning_black", text="⚠️ Weather Alerts", command=self._check_alerts, width=15).grid(row=0, column=2, padx=5)

        # Smart Features Section
        smart_frame = ttk.LabelFrame(main_container, text="🧠 Smart Features", padding=15)
        smart_frame.pack(fill="x", pady=10)
        smart_row1 = ttk.Frame(smart_frame)
        smart_row1.pack(pady=5)
        StyledButton(smart_row1, "accent_black", text="🔄 Refresh All", command=self._refresh_all, width=15).grid(row=0, column=0, padx=5)
        StyledButton(smart_row1, "info_black", text="📊 Quick Stats", command=self._quick_stats, width=15).grid(row=0, column=1, padx=5)
        StyledButton(smart_row1, "success_black", text="🌍 Multi-City", command=self._multi_city, width=15).grid(row=0, column=2, padx=5)

        # Background color changer button
        self._bg_colors = ["#f0f4f8", "#e0e7ef", "#ffe4e1", "#e6ffe6", "#e6f7ff", "#fffbe6", "#f5e6ff", "#262a32", "#23272e"]
        self._bg_color_index = 0
        StyledButton(self.frame, "accent_black", text="🎨 Change Background Color", command=self._cycle_bg_color).pack(pady=5)

        # Results display area
        self.result_frame = ttk.LabelFrame(main_container, text="📄 Results", padding=10)
        self.result_frame.pack(fill="both", expand=True, pady=10)
        self.result_text = StyledText(self.result_frame, height=12, width=80)
        self.result_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Initial welcome message
        welcome_msg = (
            "Welcome to Quick Actions Dashboard!\n\n"
            "Select any action above to get started:\n\n"
            "Weather Actions:\n"
            "- Quick Weather: Get current conditions instantly\n"
            "- Today's Plan: Comprehensive daily weather planning\n"
            "- Best Times: Optimal timing for activities\n\n"
            "Utility Actions:\n"
            "- Share Weather: Social media ready content\n"
            "- Save Favorite: Bookmark your cities\n"
            "- Weather Alerts: Check for weather warnings\n\n"
            "Smart Features:\n"
            "- Refresh All: System optimization and refresh\n"
            "- Quick Stats: Usage and performance statistics\n"
            "- Multi-City: Global weather overview\n\n"
            "Results will appear in this area when you use the quick actions above."
        )
        self.result_text.insert("1.0", welcome_msg)

    # Quick Action Methods (delegated to controller with result display)
    def _quick_weather(self):
        """Get weather for last used city or prompt for new city"""
        city = self.controller.last_city
        if not city:
            city = self._prompt_for_city("Enter city for quick weather:")
        
        if city:
            try:
                weather_data = self.controller.get_quick_weather(city)
                result = f"🌡️ QUICK WEATHER for {weather_data.city}:\n"
                result += "=" * 50 + "\n"
                result += f"Temperature: {weather_data.formatted_temperature}\n"
                result += f"Description: {weather_data.description}\n"
                result += f"Humidity: {weather_data.humidity}%\n"
                result += f"Wind: {weather_data.formatted_wind}\n"
                result += f"Visibility: {weather_data.formatted_visibility}\n"
                result += f"Pressure: {weather_data.pressure} hPa\n"
                self._display_result(result)
            except Exception as e:
                self._display_error(f"Failed to get weather: {str(e)}")

    def _todays_plan(self):
        """Get comprehensive today's weather plan"""
        city = self.controller.last_city
        if not city:
            city = self._prompt_for_city("Enter city for today's plan:")
        
        if city:
            try:
                plan = self.controller.get_todays_plan(city)
                self._display_result(plan)
            except Exception as e:
                self._display_error(f"Failed to get today's plan: {str(e)}")

    def _best_times(self):
        """Get best times for activities"""
        city = self.controller.last_city
        if not city:
            city = self._prompt_for_city("Enter city for best times:")
        
        if city:
            try:
                times = self.controller.find_best_times(city)
                self._display_result(times)
            except Exception as e:
                self._display_error(f"Failed to get best times: {str(e)}")

    def _share_weather(self):
        """Get shareable weather content"""
        city = self.controller.last_city
        if not city:
            city = self._prompt_for_city("Enter city for shareable weather:")
        
        if city:
            try:
                content = self.controller.get_shareable_weather(city)
                self._display_result(content)
            except Exception as e:
                self._display_error(f"Failed to generate shareable content: {str(e)}")

    def _save_favorite(self):
        """Save current or entered city as favorite"""
        city = self.controller.last_city
        if not city:
            city = self._prompt_for_city("Enter city to save as favorite:")
        
        if city:
            result = self.controller.add_favorite_city(city)
            fav_cities = self.controller.get_favorite_cities()
            
            display_result = f"⭐ FAVORITE CITIES MANAGER:\n{'=' * 50}\n"
            display_result += f"Status: {result}\n\n"
            display_result += "Your Favorite Cities:\n"
            if fav_cities:
                for i, fav_city in enumerate(fav_cities, 1):
                    display_result += f"• {fav_city}\n"
            else:
                display_result += "No favorite cities saved yet.\n"
            
            self._display_result(display_result)

    def _check_alerts(self):
        """Check comprehensive weather alerts"""
        city = self.controller.last_city
        if not city:
            city = self._prompt_for_city("Enter city to check alerts:")
        
        if city:
            try:
                alerts = self.controller.get_quick_alerts(city)
                self._display_result(alerts)
            except Exception as e:
                self._display_error(f"Failed to check alerts: {str(e)}")

    def _refresh_all(self):
        """Refresh all system data"""
        try:
            refresh_report = self.controller.refresh_all_data()
            self._display_result(refresh_report)
        except Exception as e:
            self._display_error(f"Failed to refresh data: {str(e)}")

    def _quick_stats(self):
        """Get quick statistics"""
        try:
            stats = self.controller.get_quick_statistics()
            self._display_result(stats)
        except Exception as e:
            self._display_error(f"Failed to get statistics: {str(e)}")

    def _multi_city(self):
        """Get multi-city weather overview"""
        try:
            overview = self.controller.get_multi_city_quick_check()
            self._display_result(overview)
        except Exception as e:
            self._display_error(f"Failed to get multi-city overview: {str(e)}")

    def _prompt_for_city(self, prompt_text):
        """Prompt user for city name"""
        import tkinter.simpledialog as simpledialog
        return simpledialog.askstring("City Input", prompt_text)

    def _display_result(self, content):
        """Display result in the text area"""
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", content)

    def _display_error(self, error_msg):
        """Display error message in the text area"""
        self.result_text.delete("1.0", "end")
        error_content = f"❌ ERROR:\n{'=' * 50}\n{error_msg}\n\n"
        error_content += "💡 Tips:\n"
        error_content += "• Check your internet connection\n"
        error_content += "• Verify the city name spelling\n"
        error_content += "• Try a different city\n"
        self.result_text.insert("1.0", error_content)

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
        try:
            alerts = self.controller.track_severe_weather(city)
            self.display_result(alerts)
        except Exception as e:
            self.handle_error(e, "checking for severe weather alerts")

    def show_alert_types_chart(self):
        """Shows a pie chart of severe alert types."""
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            labels = ['Thunderstorm', 'Tornado', 'Flood', 'Wind']
            sizes = [random.randint(1, 10) for _ in range(4)]
            ChartHelper.create_pie_chart(
                self.chart_frame,
                "Severe Alert Types Distribution",
                labels,
                sizes
            )
        except Exception as e:
            self.handle_error(e, "generating alert types chart")

    def show_alert_frequency_chart(self):
        """Shows a bar chart of severe alert frequency."""
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
            counts = [random.randint(0, 5) for _ in range(5)]
            ChartHelper.create_bar_chart(
                self.chart_frame,
                "Severe Alert Frequency by Month",
                months,
                counts,
                colors=['#F44336'],
                x_label="Month",
                y_label="Number of Alerts"
            )
        except Exception as e:
            self.handle_error(e, "generating alert frequency chart")

    def show_intensity_map(self):
        """Shows a heatmap of severe weather intensity."""
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            data = np.random.rand(10, 10)
            ChartHelper.create_heatmap(
                self.chart_frame,
                "Severe Weather Intensity Map",
                data,
                "Longitude",
                "Latitude"
            )
        except Exception as e:
            self.handle_error(e, "generating intensity map")

    def show_historical_alerts_chart(self):
        """Shows a line chart of historical severe alerts."""
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            years = ['2020', '2021', '2022', '2023', '2024']
            counts = [random.randint(10, 30) for _ in range(5)]
            ChartHelper.create_line_chart(
                self.chart_frame,
                "Historical Severe Alerts (Last 5 Years)",
                years,
                counts,
                "Year",
                "Number of Alerts"
            )
        except Exception as e:
            self.handle_error(e, "generating historical alerts chart")


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
        try:
            trends = self.controller.get_weather_trends(city)
            self.display_result(trends)
        except Exception as e:
            self.handle_error(e, "analyzing trends")

    def show_temp_time_chart(self):
        """Shows a line chart for temperature over time."""
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            time_of_day = [f"{h}:00" for h in range(0, 24, 3)]
            temps = [random.randint(10, 25) for _ in range(8)]
            ChartHelper.create_line_chart(
                self.chart_frame,
                "Temperature vs. Time of Day",
                time_of_day,
                temps,
                "Time",
                f"Temperature ({self.controller.get_unit_label()})"
            )
        except Exception as e:
            self.handle_error(e, "generating temp vs. time chart")

    def show_monthly_avg_chart(self):
        """Shows a bar chart for monthly average temperatures."""
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            avg_temps = [random.randint(-5, 30) for _ in range(6)]
            ChartHelper.create_bar_chart(
                self.chart_frame,
                "Monthly Average Temperature",
                months,
                avg_temps,
                colors=['#8e44ad'],
                x_label="Month",
                y_label=f"Average Temperature ({self.controller.get_unit_label()})"
            )
        except Exception as e:
            self.handle_error(e, "generating monthly average chart")

    def show_correlation_heatmap(self):
        """Shows a heatmap for weather data correlation."""
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            data = np.random.rand(5, 5)
            labels = ['Temp', 'Humidity', 'Wind', 'Pressure', 'UV Index']
            ChartHelper.create_heatmap(
                self.chart_frame,
                "Weather Data Correlation Matrix",
                data,
                labels,
                labels,
                cmap='viridis'
            )
        except Exception as e:
            self.handle_error(e, "generating correlation heatmap")

    def show_uv_index_chart(self):
        """Shows a line chart for UV index trend."""
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            days = [f"Day {i}" for i in range(1, 8)]
            uv_index = [random.randint(1, 11) for _ in range(7)]
            ChartHelper.create_line_chart(
                self.chart_frame,
                "UV Index Trend (Last 7 Days)",
                days,
                uv_index,
                "Day",
                "UV Index"
            )
        except Exception as e:
            self.handle_error(e, "generating UV index chart")


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
        try:
            tips = self.controller.get_health_recommendations(city)
            self.display_result(tips)
        except Exception as e:
            self.handle_error(e, "fetching health and wellness tips")

    def show_activity_index_chart(self):
        """Shows a bar chart for the outdoor activity index."""
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            activities = ['Running', 'Cycling', 'Hiking', 'Picnic']
            scores = [random.randint(1, 10) for _ in range(4)]
            ChartHelper.create_bar_chart(
                self.chart_frame,
                "Outdoor Activity Index",
                activities,
                scores,
                colors=['#27ae60'],
                x_label="Activity",
                y_label="Suitability Score (1-10)"
            )
        except Exception as e:
            self.handle_error(e, "generating activity index chart")

    def show_air_quality_chart(self):
        """Shows a gauge chart for air quality."""
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            aqi = random.randint(0, 200)
            ChartHelper.create_gauge_chart(
                self.chart_frame,
                "Air Quality Index (AQI)",
                aqi,
                0,
                300,
                ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']
            )
        except Exception as e:
            self.handle_error(e, "generating air quality chart")

    def show_allergy_forecast_chart(self):
        """Shows a bar chart for allergy forecast."""
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            allergens = ['Tree Pollen', 'Grass Pollen', 'Weed Pollen']
            levels = [random.randint(1, 10) for _ in range(3)]
            ChartHelper.create_bar_chart(
                self.chart_frame,
                "Allergy Forecast",
                allergens,
                levels,
                colors=['#d35400'],
                x_label="Allergen",
                y_label="Pollen Level (1-10)"
            )
        except Exception as e:
            self.handle_error(e, "generating allergy forecast chart")

    def show_uv_exposure_chart(self):
        """Shows a line chart for UV exposure throughout the day."""
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            hours = [f"{h}:00" for h in range(6, 20, 2)]
            uv_levels = [random.randint(0, 11) for _ in range(7)]
            ChartHelper.create_line_chart(
                self.chart_frame,
                "UV Exposure by Hour",
                hours,
                uv_levels,
                "Time of Day",
                "UV Index"
            )
        except Exception as e:
            self.handle_error(e, "generating UV exposure chart")


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
        try:
            config_info = self.controller.configure_alert_settings()
            self.display_result(config_info)
        except Exception as e:
            self.handle_error(e, "configuring alerts")

    def show_alert_stats_chart(self):
        """Shows a pie chart of alert statistics."""
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            labels = ['Triggered', 'Snoozed', 'Dismissed', 'Inactive']
            sizes = [random.randint(1, 20) for _ in range(4)]
            ChartHelper.create_pie_chart(
                self.chart_frame,
                "Alert Statistics",
                labels,
                sizes
            )
        except Exception as e:
            self.handle_error(e, "generating alert stats chart")

    def show_trigger_history_chart(self):
        """Shows a line chart of alert trigger history."""
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            dates = [f"Day {i}" for i in range(1, 11)]
            triggers = [random.randint(0, 5) for _ in range(10)]
            ChartHelper.create_line_chart(
                self.chart_frame,
                "Alert Trigger History (Last 10 Days)",
                dates,
                triggers,
                "Date",
                "Number of Triggers"
            )
        except Exception as e:
            self.handle_error(e, "generating trigger history chart")

    def show_active_rules_chart(self):
        """Shows a bar chart of active alert rules."""
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data
            rules = ['High Temp', 'Low Temp', 'High Wind', 'Heavy Rain']
            active_status = [random.choice([0, 1]) for _ in range(4)]
            ChartHelper.create_bar_chart(
                self.chart_frame,
                "Active Alert Rules",
                rules,
                active_status,
                ['#e74c3c', '#3498db'],
                "Rule",
                "Status (1=Active, 0=Inactive)"
            )
        except Exception as e:
            self.handle_error(e, "generating active rules chart")

    def show_thresholds_chart(self):
        """Shows a chart for alert thresholds."""
        if not CHARTS_AVAILABLE:
            self.display_result("Charts are not available.")
            return
        try:
            # Dummy data for thresholds
            labels = ['Temp >', 'Temp <', 'Wind >']
            values = [30, 0, 20]
            
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.barh(labels, values, color=['#e74c3c', '#3498db', '#95a5a6'])
            ax.set_xlabel('Threshold Value')
            ax.set_title('Configured Alert Thresholds')
            
            for index, value in enumerate(values):
                ax.text(value, index, str(value))

            fig.tight_layout()
            ChartHelper.embed_chart_in_frame(fig, self.chart_frame)
        except Exception as e:
            self.handle_error(e, "generating thresholds chart")


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
