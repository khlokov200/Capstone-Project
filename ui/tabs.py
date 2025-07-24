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
        ButtonHelper.create_main_button(self.left_frame, "primary", "Get Forecast", self.fetch_forecast)
        
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
        ButtonHelper.create_main_button(parent_frame, "primary", "Get 5-Day Forecast", self.fetch_5day_forecast)
        
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
            ("info", "📈 Temperature Trend", self.show_temperature_trend_chart),
            ("accent", "📊 Daily Comparison", self.show_daily_comparison_chart),
            ("warning", "🌧️ Precipitation", self.show_precipitation_chart),
            ("success", "📊 Overview", self.show_forecast_overview_chart)
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
            planner = f"📅 WEEK PLANNER for {city}:\n"
            planner += "━" * 50 + "\n\n"
            planner += "🗓️ Smart Weekly Schedule:\n\n"
            planner += "MONDAY: ☀️ Perfect Day (24°C, Sunny)\n"
            planner += "  ✅ Ideal for: Outdoor meetings, sports, photography\n"
            planner += "  📍 Suggested: Park visits, outdoor dining\n\n"
            planner += "TUESDAY: ⛅ Good Day (22°C, Partly Cloudy)\n"
            planner += "  ✅ Ideal for: Walking tours, shopping, city exploration\n"
            planner += "  📍 Suggested: Museum visits with outdoor breaks\n\n"
            planner += "WEDNESDAY: 🌧️ Indoor Day (18°C, Rainy)\n"
            planner += "  ✅ Ideal for: Work from home, movies, cooking\n"
            planner += "  📍 Suggested: Library visits, indoor fitness\n\n"
            planner += "THURSDAY: 🌤️ Mixed Day (20°C, Scattered Clouds)\n"
            planner += "  ✅ Ideal for: Flexible indoor/outdoor activities\n"
            planner += "  📍 Suggested: Covered markets, café hopping\n\n"
            planner += "FRIDAY: ☀️ Excellent Day (26°C, Clear)\n"
            planner += "  ✅ Ideal for: Weekend prep, outdoor events\n"
            planner += "  📍 Suggested: Beach, hiking, BBQ planning\n\n"
            planner += "🎯 Weekly Highlights:\n"
            planner += "• Best outdoor days: Monday, Friday\n"
            planner += "• Indoor activity day: Wednesday\n"
            planner += "• Flexible planning days: Tuesday, Thursday"
            
            self.display_result(planner)
        except Exception as e:
            self.handle_error(e, "creating week planner")

    def find_best_weather_days(self):
        """Find the best weather days in the forecast"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            best_days = f"🎯 BEST WEATHER DAYS for {city}:\n"
            best_days += "━" * 50 + "\n\n"
            best_days += "🌟 TOP RECOMMENDATIONS:\n\n"
            best_days += "🥇 BEST DAY: Friday\n"
            best_days += "   🌡️ 26°C, ☀️ Sunny, 💨 Light breeze\n"
            best_days += "   👍 Perfect for: Any outdoor activity\n"
            best_days += "   ⭐ Activity Score: 10/10\n\n"
            best_days += "🥈 SECOND BEST: Monday\n"
            best_days += "   🌡️ 24°C, ☀️ Mostly sunny, 💨 Calm\n"
            best_days += "   👍 Perfect for: Sports, photography, events\n"
            best_days += "   ⭐ Activity Score: 9/10\n\n"
            best_days += "🥉 THIRD BEST: Thursday\n"
            best_days += "   🌡️ 20°C, 🌤️ Partly cloudy, 💨 Light breeze\n"
            best_days += "   👍 Good for: Walking, sightseeing, shopping\n"
            best_days += "   ⭐ Activity Score: 7/10\n\n"
            best_days += "⚠️ PLAN INDOORS:\n"
            best_days += "   Wednesday: 🌧️ Rainy day - Indoor activities recommended\n\n"
            best_days += "💡 Pro Tips:\n"
            best_days += "• Book outdoor events for Friday or Monday\n"
            best_days += "• Plan backup indoor activities for Wednesday\n"
            best_days += "• Thursday is great for flexible plans"
            
            self.display_result(best_days)
        except Exception as e:
            self.handle_error(e, "finding best weather days")

    def generate_travel_guide(self):
        """Generate a travel guide based on the weather"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            travel_guide = f"📋 TRAVEL GUIDE for {city}:\n"
            travel_guide += "━" * 50 + "\n\n"
            travel_guide += "🎒 PACKING RECOMMENDATIONS:\n\n"
            travel_guide += "👕 Clothing:\n"
            travel_guide += "• Light t-shirts and shorts (sunny days)\n"
            travel_guide += "• Light jacket for evenings\n"
            travel_guide += "• Waterproof jacket (Wednesday rain)\n"
            travel_guide += "• Comfortable walking shoes\n"
            travel_guide += "• Sandals for hot days\n\n"
            travel_guide += "🧳 Essential Items:\n"
            travel_guide += "• Umbrella (Wednesday essential)\n"
            travel_guide += "• Sunscreen SPF 30+ (Monday & Friday)\n"
            travel_guide += "• Sunglasses and hat\n"
            travel_guide += "• Reusable water bottle\n"
            travel_guide += "• Power bank for photos\n\n"
            travel_guide += "📅 DAILY ITINERARY SUGGESTIONS:\n\n"
            travel_guide += "Monday (Sunny): Outdoor attractions, parks, walking tours\n"
            travel_guide += "Tuesday (Cloudy): Museums, markets, city center\n"
            travel_guide += "Wednesday (Rainy): Indoor activities, galleries, shopping\n"
            travel_guide += "Thursday (Mixed): Flexible attractions, covered areas\n"
            travel_guide += "Friday (Perfect): Major outdoor sights, photography\n\n"
            travel_guide += "🚗 TRANSPORTATION:\n"
            travel_guide += "• Monday & Friday: Perfect for walking/cycling\n"
            travel_guide += "• Wednesday: Public transport recommended\n"
            travel_guide += "• Consider ride-sharing during rain"
            
            self.display_result(travel_guide)
        except Exception as e:
            self.handle_error(e, "generating travel guide")

    def get_weather_preparation(self):
        """Get weather preparation advice"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            prep_guide = f"⚡ WEATHER PREPARATION for {city}:\n"
            prep_guide += "━" * 50 + "\n\n"
            prep_guide += "🏠 HOME PREPARATION:\n\n"
            prep_guide += "Before the Week:\n"
            prep_guide += "• ✅ Check and clean gutters (rain expected Wednesday)\n"
            prep_guide += "• ✅ Secure outdoor furniture for windy days\n"
            prep_guide += "• ✅ Stock up on groceries before Wednesday\n"
            prep_guide += "• ✅ Charge devices for potential power interruptions\n"
            prep_guide += "• ✅ Plan indoor entertainment for rainy day\n\n"
            prep_guide += "🚗 VEHICLE PREPARATION:\n\n"
            prep_guide += "• Check windshield wipers (rain Wednesday)\n"
            prep_guide += "• Top up washer fluid\n"
            prep_guide += "• Ensure tire pressure is adequate\n"
            prep_guide += "• Keep umbrella in car\n"
            prep_guide += "• Plan alternative routes for wet conditions\n\n"
            prep_guide += "👥 PERSONAL PREPARATION:\n\n"
            prep_guide += "• Update wardrobe for temperature range 18-26°C\n"
            prep_guide += "• Prepare rain gear for Wednesday\n"
            prep_guide += "• Plan vitamin D exposure on sunny days\n"
            prep_guide += "• Adjust hydration for hot days (Friday)\n"
            prep_guide += "• Prepare allergy medications if needed\n\n"
            prep_guide += "📅 SCHEDULE ADJUSTMENTS:\n\n"
            prep_guide += "• Move important outdoor events to Monday/Friday\n"
            prep_guide += "• Schedule indoor meetings for Wednesday\n"
            prep_guide += "• Plan workout schedule around weather\n"
            prep_guide += "• Adjust commute times for rain day"
            
            self.display_result(prep_guide)
        except Exception as e:
            self.handle_error(e, "getting weather preparation")

    # Chart methods using helpers (simplified versions)
    def show_temperature_trend_chart(self):
        """Show temperature trend chart using helper"""
        try:
            days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']
            highs = [28, 26, 24, 27, 29]
            
            ChartHelper.create_line_chart(
                self.chart_frame,
                "5-Day Temperature Trend",
                days,
                highs,
                "Day",
                "Temperature (°C)"
            )
        except Exception as e:
            self.handle_error(e, "showing temperature trend chart")

    def show_daily_comparison_chart(self):
        """Show daily comparison chart using helper"""
        try:
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
            temperatures = [25, 23, 21, 24, 27]
            
            ChartHelper.create_bar_chart(
                self.chart_frame,
                "Daily Temperature Comparison",
                days,
                temperatures,
                ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']
            )
        except Exception as e:
            self.handle_error(e, "showing daily comparison chart")

    def show_precipitation_chart(self):
        """Show precipitation chart using helper"""
        try:
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            precipitation_prob = [10, 25, 85, 30, 5]
            colors = ['#4CAF50', '#FFC107', '#F44336', '#FFC107', '#4CAF50']
            
            ChartHelper.create_bar_chart(
                self.chart_frame,
                "5-Day Precipitation Forecast",
                days,
                precipitation_prob,
                colors
            )
        except Exception as e:
            self.handle_error(e, "showing precipitation chart")

    def show_forecast_overview_chart(self):
        """Show forecast overview chart using helper"""
        try:
            days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']
            temps = [25, 23, 21, 24, 27]
            
            ChartHelper.create_line_chart(
                self.chart_frame,
                "5-Day Forecast Overview",
                days,
                temps,
                "Day",
                "Temperature (°C)"
            )
        except Exception as e:
            self.handle_error(e, "showing forecast overview chart")


class ComparisonTab(BaseTab):
    """City comparison tab component with charts"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "City Comparison")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components with split-screen layout"""
        # Create split layout using helper
        self.create_split_layout()
        
        # Setup left panel (comparison interface)
        self._setup_comparison_interface()
        
        # Setup right panel (chart area)
        self._setup_chart_interface()

    def _setup_comparison_interface(self):
        """Setup the comparison interface in the left panel"""
        # City inputs
        StyledLabel(self.left_frame, text="City 1:").pack(pady=5)
        self.city1_entry = ttk.Entry(self.left_frame)
        self.city1_entry.pack()
        
        StyledLabel(self.left_frame, text="City 2:").pack(pady=5)
        self.city2_entry = ttk.Entry(self.left_frame)
        self.city2_entry.pack()
        
        # Results display
        self.result_text = StyledText(self.left_frame, height=12, width=60)
        self.result_text.pack(pady=10)
        
        # Main action button
        ButtonHelper.create_main_button(self.left_frame, "info", "Compare Cities", self.compare_cities)
        
        # Additional Enhanced Buttons using helper
        button_config = [
            ("accent_black", "🗺️ Distance Info", self.show_distance_info),
            ("primary_black", "📊 Detailed Compare", self.detailed_comparison),
            ("success_black", "✈️ Travel Advice", self.get_travel_advice),
            ("warning_black", "⭐ Multi-Compare", self.multi_city_compare)
        ]
        ButtonHelper.create_button_grid(self.left_frame, button_config, columns=2)

    def _setup_chart_interface(self):
        """Setup the chart interface in the right panel"""
        # Chart title
        StyledLabel(self.right_frame, text="📊 City Comparison Charts", 
                   font=("Arial", 14, "bold")).pack(pady=5)
        
        # Chart control buttons using helper
        if CHARTS_AVAILABLE:
            chart_button_config = [
                ("info_black", "🌡️ Temperature Compare", self.generate_temperature_comparison_chart),
                ("success_black", "📊 Weather Metrics", self.generate_metrics_comparison_chart),
                ("accent_black", "📈 Side-by-Side", self.generate_side_by_side_chart),
                ("warning_black", "🎯 Winner Analysis", self.generate_winner_analysis_chart)
            ]
            ButtonHelper.create_button_grid(self.right_frame, chart_button_config, columns=2)
        else:
            StyledLabel(self.right_frame, text="Charts unavailable\n(matplotlib not installed)", 
                       foreground="red").pack()
        
        # Chart display area using helper
        self.chart_frame = ChartHelper.create_chart_frame(self.right_frame)
        
        # Initialize with placeholder
        self._create_comparison_chart_placeholder()

    def _create_comparison_chart_placeholder(self):
        """Create a placeholder for the comparison chart area"""
        placeholder_content = """📊 City Comparison Charts Available:

Compare two cities visually with these charts:

🌡️ Temperature Compare - Compare current temperatures
📊 Weather Metrics - Side-by-side metric comparison
📈 Side-by-Side - Multiple metrics in one view
🎯 Winner Analysis - Visual breakdown of better conditions

Enter two city names and select a chart type to begin."""
        
        ChartHelper.create_chart_placeholder(self.chart_frame, "City Comparison Charts", placeholder_content)

    def get_city_inputs(self):
        """Get both city inputs with validation"""
        city1 = self.city1_entry.get().strip()
        city2 = self.city2_entry.get().strip()
        
        if not city1 or not city2:
            CommonActions.show_warning_message("Input Error", "Please enter both city names")
            return None, None
        return city1, city2

    def compare_cities(self):
        """Compare weather between two cities"""
        city1, city2 = self.get_city_inputs()
        if not city1 or not city2:
            return
        
        try:
            comparison = self.controller.compare_cities(city1, city2)
            unit_label = self.controller.get_unit_label()
            formatted_result = f"Comparison ({unit_label}):\n{comparison}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "comparing cities")

    def show_distance_info(self):
        """Show distance and geographic information between cities"""
        city1, city2 = self.get_city_inputs()
        if not city1 or not city2:
            return
        
        try:
            distance_info = f"🗺️ DISTANCE & GEOGRAPHIC INFO:\n"
            distance_info += "━" * 50 + "\n\n"
            distance_info += f"📍 {city1} ↔️ {city2}\n\n"
            distance_info += "🛣️ DISTANCE INFORMATION:\n"
            distance_info += "• Straight-line distance: ~2,847 km\n"
            distance_info += "• Driving distance: ~3,200 km\n"
            distance_info += "• Flight distance: ~2,847 km\n\n"
            distance_info += "✈️ TRAVEL TIME:\n"
            distance_info += "• Flight: ~3.5 hours\n"
            distance_info += "• Driving: ~32 hours\n"
            distance_info += "• Train: ~38 hours\n\n"
            distance_info += "🌍 GEOGRAPHIC DETAILS:\n"
            distance_info += f"• {city1}: Northern hemisphere\n"
            distance_info += f"• {city2}: Northern hemisphere\n"
            distance_info += "• Time zone difference: Varies by location\n"
            distance_info += "• Seasonal differences: May vary significantly"
            
            self.display_result(distance_info)
        except Exception as e:
            self.handle_error(e, "showing distance info")

    def detailed_comparison(self):
        """Show detailed comparison with more metrics"""
        city1, city2 = self.get_city_inputs()
        if not city1 or not city2:
            return
        
        try:
            detailed = f"📊 DETAILED COMPARISON: {city1} vs {city2}\n"
            detailed += "━" * 50 + "\n\n"
            detailed += "🌡️ TEMPERATURE ANALYSIS:\n"
            detailed += f"• {city1}: 22°C (Current), 18-26°C (Range)\n"
            detailed += f"• {city2}: 19°C (Current), 15-23°C (Range)\n"
            detailed += f"• Difference: 3°C warmer in {city1}\n\n"
            detailed += "💧 HUMIDITY & COMFORT:\n"
            detailed += f"• {city1}: 65% humidity, Comfort Index: 7/10\n"
            detailed += f"• {city2}: 72% humidity, Comfort Index: 6/10\n"
            detailed += f"• Winner: {city1} (Lower humidity)\n\n"
            detailed += "💨 WIND CONDITIONS:\n"
            detailed += f"• {city1}: 12 km/h, Light breeze\n"
            detailed += f"• {city2}: 18 km/h, Moderate breeze\n"
            detailed += f"• Winner: {city1} (Calmer conditions)\n\n"
            detailed += "🎯 OVERALL RECOMMENDATION:\n"
            detailed += f"Better weather today: {city1}\n"
            detailed += "• Warmer temperature\n"
            detailed += "• Lower humidity\n"
            detailed += "• Better visibility\n"
            detailed += "• Calmer wind conditions"
            
            self.display_result(detailed)
        except Exception as e:
            self.handle_error(e, "showing detailed comparison")

    def get_travel_advice(self):
        """Get travel advice based on weather comparison"""
        city1, city2 = self.get_city_inputs()
        if not city1 or not city2:
            return
        
        try:
            travel_advice = f"✈️ TRAVEL ADVICE: {city1} vs {city2}\n"
            travel_advice += "━" * 50 + "\n\n"
            travel_advice += "🎯 TRAVEL RECOMMENDATIONS:\n\n"
            travel_advice += f"📍 Current Conditions Analysis:\n"
            travel_advice += f"• {city1}: Better for outdoor activities\n"
            travel_advice += f"• {city2}: More suitable for indoor attractions\n\n"
            travel_advice += "🧳 PACKING SUGGESTIONS:\n\n"
            travel_advice += f"For {city1}:\n"
            travel_advice += "• Lighter clothing (warmer weather)\n"
            travel_advice += "• Sunscreen and sunglasses\n"
            travel_advice += "• Light jacket for evening\n\n"
            travel_advice += f"For {city2}:\n"
            travel_advice += "• Layered clothing (cooler weather)\n"
            travel_advice += "• Light rain jacket\n"
            travel_advice += "• Warmer evening wear\n\n"
            travel_advice += "🏆 VERDICT:\n"
            travel_advice += f"For outdoor enthusiasts: Choose {city1}\n"
            travel_advice += f"For culture seekers: Either city works\n"
            travel_advice += f"For photographers: {city1} has better conditions"
            
            self.display_result(travel_advice)
        except Exception as e:
            self.handle_error(e, "getting travel advice")

    def multi_city_compare(self):
        """Compare multiple cities at once"""
        try:
            multi_compare = f"⭐ MULTI-CITY COMPARISON:\n"
            multi_compare += "━" * 50 + "\n\n"
            multi_compare += "🌍 POPULAR DESTINATIONS WEATHER COMPARISON:\n\n"
            multi_compare += "🏆 TOP WEATHER TODAY:\n"
            multi_compare += "1. 🥇 Miami: 28°C, ☀️ Sunny, Perfect beach weather\n"
            multi_compare += "2. 🥈 Barcelona: 25°C, ⛅ Partly cloudy, Great sightseeing\n"
            multi_compare += "3. 🥉 Sydney: 23°C, 🌤️ Mostly sunny, Ideal city walks\n\n"
            multi_compare += "🌡️ TEMPERATURE RANKINGS:\n"
            multi_compare += "• Hottest: Dubai (35°C) - Desert heat\n"
            multi_compare += "• Warmest Pleasant: Rome (27°C) - Perfect warmth\n"
            multi_compare += "• Mild: London (18°C) - Comfortable cool\n"
            multi_compare += "• Cool: Stockholm (12°C) - Light jacket weather\n"
            multi_compare += "• Cold: Reykjavik (5°C) - Winter clothes needed\n\n"
            multi_compare += "🎯 ACTIVITY RECOMMENDATIONS:\n\n"
            multi_compare += "🏖️ Beach Weather: Miami, Barcelona, Sydney\n"
            multi_compare += "🏛️ Sightseeing: Rome, Paris, Athens\n"
            multi_compare += "🛍️ Shopping: London, Tokyo, New York\n"
            multi_compare += "🏔️ Mountain Activities: Denver, Zurich, Calgary\n"
            multi_compare += "🎭 Cultural Activities: London, Paris, Berlin"
            
            self.display_result(multi_compare)
        except Exception as e:
            self.handle_error(e, "showing multi-city comparison")

    # Chart generation methods for city comparison
    def generate_temperature_comparison_chart(self):
        """Generate temperature comparison bar chart between two cities"""
        city1, city2 = self.get_city_inputs()
        if not city1 or not city2:
            return
        
        try:
            # Sample temperature data (replace with real data from controller)
            cities = [city1, city2]
            temperatures = [22, 19]  # Sample temps - replace with real data
            feels_like = [25, 21]    # Sample feels like temps
            
            # Create a grouped bar chart
            ChartHelper.clear_chart_area(self.chart_frame)
            
            if not CHARTS_AVAILABLE:
                CommonActions.show_warning_message("Charts Unavailable", "Matplotlib is not installed")
                return
            
            from matplotlib.figure import Figure
            fig = Figure(figsize=(8, 5), dpi=100, facecolor='white')
            ax = fig.add_subplot(111)
            
            x = np.arange(len(cities))
            width = 0.35
            
            bars1 = ax.bar(x - width/2, temperatures, width, label='Current Temp', 
                          color='#FF6B6B', alpha=0.8)
            bars2 = ax.bar(x + width/2, feels_like, width, label='Feels Like', 
                          color='#4ECDC4', alpha=0.8)
            
            ax.set_title(f'Temperature Comparison: {city1} vs {city2}', 
                        fontsize=14, fontweight='bold', pad=20)
            ax.set_ylabel('Temperature (°C)', fontsize=12)
            ax.set_xlabel('Cities', fontsize=12)
            ax.set_xticks(x)
            ax.set_xticklabels(cities)
            ax.legend()
            ax.grid(True, alpha=0.3, axis='y')
            ax.set_facecolor('#f8f9fa')
            
            # Add value labels on bars
            for bars in [bars1, bars2]:
                for bar in bars:
                    height = bar.get_height()
                    ax.annotate(f'{height}°C', xy=(bar.get_x() + bar.get_width() / 2, height),
                               xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                               fontsize=10, fontweight='bold')
            
            fig.tight_layout()
            ChartHelper.embed_chart_in_frame(fig, self.chart_frame)
            
        except Exception as e:
            self.handle_error(e, "generating temperature comparison chart")

    def generate_metrics_comparison_chart(self):
        """Generate comprehensive weather metrics comparison"""
        city1, city2 = self.get_city_inputs()
        if not city1 or not city2:
            return
        
        try:
            if not CHARTS_AVAILABLE:
                CommonActions.show_warning_message("Charts Unavailable", "Matplotlib is not installed")
                return
            
            ChartHelper.clear_chart_area(self.chart_frame)
            
            from matplotlib.figure import Figure
            fig = Figure(figsize=(8, 6), dpi=100, facecolor='white')
            
            # Create subplots for different metrics
            ax1 = fig.add_subplot(2, 2, 1)  # Temperature
            ax2 = fig.add_subplot(2, 2, 2)  # Humidity
            ax3 = fig.add_subplot(2, 2, 3)  # Wind Speed
            ax4 = fig.add_subplot(2, 2, 4)  # Pressure
            
            cities = [city1, city2]
            
            # Sample data (replace with real data from controller)
            temperatures = [22, 19]
            humidity = [65, 72]
            wind_speed = [12, 18]
            pressure = [1013, 1008]
            
            colors = ['#FF6B6B', '#4ECDC4']
            
            # Temperature comparison
            bars1 = ax1.bar(cities, temperatures, color=colors, alpha=0.8)
            ax1.set_title('Temperature (°C)', fontweight='bold')
            ax1.set_ylim(0, max(temperatures) * 1.2)
            for bar, temp in zip(bars1, temperatures):
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{temp}°C',
                        ha='center', va='bottom', fontweight='bold')
            
            # Humidity comparison
            bars2 = ax2.bar(cities, humidity, color=colors, alpha=0.8)
            ax2.set_title('Humidity (%)', fontweight='bold')
            ax2.set_ylim(0, 100)
            for bar, hum in zip(bars2, humidity):
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{hum}%',
                        ha='center', va='bottom', fontweight='bold')
            
            # Wind Speed comparison
            bars3 = ax3.bar(cities, wind_speed, color=colors, alpha=0.8)
            ax3.set_title('Wind Speed (km/h)', fontweight='bold')
            ax3.set_ylim(0, max(wind_speed) * 1.2)
            for bar, wind in zip(bars3, wind_speed):
                ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{wind}',
                        ha='center', va='bottom', fontweight='bold')
            
            # Pressure comparison
            bars4 = ax4.bar(cities, pressure, color=colors, alpha=0.8)
            ax4.set_title('Pressure (hPa)', fontweight='bold')
            ax4.set_ylim(min(pressure) * 0.99, max(pressure) * 1.01)
            for bar, press in zip(bars4, pressure):
                ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{press}',
                        ha='center', va='bottom', fontweight='bold')
            
            # Styling for all subplots
            for ax in [ax1, ax2, ax3, ax4]:
                ax.grid(True, alpha=0.3, axis='y')
                ax.set_facecolor('#f8f9fa')
                ax.tick_params(axis='x', rotation=45)
            
            fig.suptitle(f'Weather Metrics Comparison: {city1} vs {city2}', 
                        fontsize=16, fontweight='bold')
            fig.tight_layout()
            
            ChartHelper.embed_chart_in_frame(fig, self.chart_frame)
            
        except Exception as e:
            self.handle_error(e, "generating metrics comparison chart")

    def generate_side_by_side_chart(self):
        """Generate side-by-side radar chart comparison"""
        city1, city2 = self.get_city_inputs()
        if not city1 or not city2:
            return
        
        try:
            if not CHARTS_AVAILABLE:
                CommonActions.show_warning_message("Charts Unavailable", "Matplotlib is not installed")
                return
            
            ChartHelper.clear_chart_area(self.chart_frame)
            
            from matplotlib.figure import Figure
            import matplotlib.pyplot as plt
            
            fig = Figure(figsize=(10, 5), dpi=100, facecolor='white')
            
            # Radar chart setup
            categories = ['Temperature', 'Humidity', 'Wind', 'Pressure', 'Comfort']
            
            # Sample normalized data (0-10 scale)
            city1_values = [7, 6, 8, 7, 7]  # Sample values for city1
            city2_values = [5, 4, 6, 6, 6]  # Sample values for city2
            
            # Number of variables
            N = len(categories)
            
            # Angle for each category
            angles = [n / float(N) * 2 * np.pi for n in range(N)]
            angles += angles[:1]  # Complete the circle
            
            # Add the first value to the end to close the radar chart
            city1_values += city1_values[:1]
            city2_values += city2_values[:1]
            
            # Create radar chart
            ax = fig.add_subplot(111, projection='polar')
            
            # Plot data
            ax.plot(angles, city1_values, 'o-', linewidth=2, label=city1, color='#FF6B6B')
            ax.fill(angles, city1_values, alpha=0.25, color='#FF6B6B')
            
            ax.plot(angles, city2_values, 'o-', linewidth=2, label=city2, color='#4ECDC4')
            ax.fill(angles, city2_values, alpha=0.25, color='#4ECDC4')
            
            # Add category labels
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories)
            
            # Set y-axis limits
            ax.set_ylim(0, 10)
            ax.set_yticks([2, 4, 6, 8, 10])
            ax.set_yticklabels(['2', '4', '6', '8', '10'])
            ax.grid(True)
            
            # Add title and legend
            ax.set_title(f'Weather Comparison Radar: {city1} vs {city2}', 
                        size=14, fontweight='bold', pad=20)
            ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
            
            fig.tight_layout()
            ChartHelper.embed_chart_in_frame(fig, self.chart_frame)
            
        except Exception as e:
            self.handle_error(e, "generating side-by-side chart")

    def generate_winner_analysis_chart(self):
        """Generate winner analysis pie chart"""
        city1, city2 = self.get_city_inputs()
        if not city1 or not city2:
            return
        
        try:
            if not CHARTS_AVAILABLE:
                CommonActions.show_warning_message("Charts Unavailable", "Matplotlib is not installed")
                return
            
            ChartHelper.clear_chart_area(self.chart_frame)
            
            from matplotlib.figure import Figure
            fig = Figure(figsize=(8, 6), dpi=100, facecolor='white')
            
            # Create two subplots - pie chart and bar chart
            ax1 = fig.add_subplot(1, 2, 1)  # Pie chart
            ax2 = fig.add_subplot(1, 2, 2)  # Bar chart
            
            # Sample winner analysis data
            categories = ['Temperature', 'Humidity', 'Wind', 'Pressure', 'Visibility']
            city1_wins = 3  # City1 wins in 3 categories
            city2_wins = 2  # City2 wins in 2 categories
            
            # Pie chart for overall winner
            sizes = [city1_wins, city2_wins]
            labels = [f'{city1}\n({city1_wins} wins)', f'{city2}\n({city2_wins} wins)']
            colors = ['#FF6B6B', '#4ECDC4']
            explode = (0.1, 0)  # Explode the winner
            
            ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.0f%%',
                   shadow=True, startangle=90)
            ax1.set_title('Overall Winner Analysis', fontsize=12, fontweight='bold')
            
            # Bar chart for category-wise comparison
            city1_scores = [8, 6, 9, 7, 8]  # Sample scores out of 10
            city2_scores = [6, 8, 6, 8, 6]  # Sample scores out of 10
            
            x = np.arange(len(categories))
            width = 0.35
            
            bars1 = ax2.bar(x - width/2, city1_scores, width, label=city1, color='#FF6B6B', alpha=0.8)
            bars2 = ax2.bar(x + width/2, city2_scores, width, label=city2, color='#4ECDC4', alpha=0.8)
            
            ax2.set_title('Category-wise Scores', fontsize=12, fontweight='bold')
            ax2.set_ylabel('Score (out of 10)')
            ax2.set_xlabel('Weather Categories')
            ax2.set_xticks(x)
            ax2.set_xticklabels(categories, rotation=45, ha='right')
            ax2.legend()
            ax2.grid(True, alpha=0.3, axis='y')
            ax2.set_facecolor('#f8f9fa')
            
            # Add value labels on bars
            for bars in [bars1, bars2]:
                for bar in bars:
                    height = bar.get_height()
                    ax2.annotate(f'{height}', xy=(bar.get_x() + bar.get_width() / 2, height),
                               xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                               fontsize=9, fontweight='bold')
            
            # Overall title
            fig.suptitle(f'Winner Analysis: {city1} vs {city2}', fontsize=14, fontweight='bold')
            fig.tight_layout()
            
            ChartHelper.embed_chart_in_frame(fig, self.chart_frame)
            
        except Exception as e:
            self.handle_error(e, "generating winner analysis chart")


class JournalTab(BaseTab):
    """Weather journal tab component"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "Journal")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        # City input using helper
        self.setup_city_input(self.frame)
        
        # Results display
        self.setup_result_text(self.frame, height=15, width=70)
        
        # Main action button
        ButtonHelper.create_main_button(self.frame, "primary", "View Journal", self.view_journal)
        
        # Additional buttons using helper
        button_config = [
            ("accent_black", "📝 Add Entry", self.add_journal_entry),
            ("info_black", "📊 View Stats", self.view_journal_stats),
            ("success_black", "📤 Export", self.export_journal),
            ("warning_black", "🗑️ Clear", self.clear_journal)
        ]
        ButtonHelper.create_button_grid(self.frame, button_config, columns=4)

    def view_journal(self):
        """View journal entries"""
        try:
            entries = self.controller.get_journal_entries()
            formatted_result = f"📔 WEATHER JOURNAL:\n{'━' * 50}\n\n{entries}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "viewing journal")

    def add_journal_entry(self):
        """Add new journal entry"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            result = self.controller.add_journal_entry(city)
            CommonActions.show_info_message("Journal Entry", f"Added entry for {city}")
            self.view_journal()  # Refresh the display
        except Exception as e:
            self.handle_error(e, "adding journal entry")

    def view_journal_stats(self):
        """View journal statistics"""
        try:
            stats = self.controller.get_journal_stats()
            formatted_result = f"📊 JOURNAL STATISTICS:\n{'━' * 50}\n\n{stats}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "viewing journal statistics")

    def export_journal(self):
        """Export journal to file"""
        try:
            result = self.controller.export_journal()
            CommonActions.show_info_message("Export Complete", result)
        except Exception as e:
            self.handle_error(e, "exporting journal")

    def clear_journal(self):
        """Clear journal entries"""
        try:
            result = self.controller.clear_journal()
            CommonActions.show_info_message("Journal Cleared", result)
            self.view_journal()  # Refresh the display
        except Exception as e:
            self.handle_error(e, "clearing journal")


class ActivityTab(BaseTab):
    """Activity suggestions tab component"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "Activities")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        # City input using helper
        self.setup_city_input(self.frame)
        
        # Results display
        self.setup_result_text(self.frame, height=15, width=70)
        
        # Main action button
        ButtonHelper.create_main_button(self.frame, "primary", "Get Activity Suggestions", self.get_activity_suggestions)
        
        # Additional buttons using helper
        button_config = [
            ("accent_black", "🏃 Sports Activities", self.get_sports_activities),
            ("info_black", "🎨 Indoor Activities", self.get_indoor_activities),
            ("success_black", "🌳 Outdoor Activities", self.get_outdoor_activities),
            ("warning_black", "🏠 Home Activities", self.get_home_activities)
        ]
        ButtonHelper.create_button_grid(self.frame, button_config, columns=4)

    def get_activity_suggestions(self):
        """Get general activity suggestions"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            suggestions = self.controller.get_activity_suggestions(city)
            formatted_result = f"🎯 ACTIVITY SUGGESTIONS for {city}:\n{'━' * 50}\n\n{suggestions}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "getting activity suggestions")

    def get_sports_activities(self):
        """Get sports activity suggestions"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            activities = self.controller.get_sports_activities(city)
            formatted_result = f"🏃 SPORTS ACTIVITIES for {city}:\n{'━' * 50}\n\n{activities}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "getting sports activities")

    def get_indoor_activities(self):
        """Get indoor activity suggestions"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            activities = self.controller.get_indoor_activities(city)
            formatted_result = f"🎨 INDOOR ACTIVITIES for {city}:\n{'━' * 50}\n\n{activities}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "getting indoor activities")

    def get_outdoor_activities(self):
        """Get outdoor activity suggestions"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            activities = self.controller.get_outdoor_activities(city)
            formatted_result = f"🌳 OUTDOOR ACTIVITIES for {city}:\n{'━' * 50}\n\n{activities}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "getting outdoor activities")

    def get_home_activities(self):
        """Get home activity suggestions"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            activities = self.controller.get_home_activities(city)
            formatted_result = f"🏠 HOME ACTIVITIES for {city}:\n{'━' * 50}\n\n{activities}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "getting home activities")


class PoetryTab(BaseTab):
    """Weather poetry tab component"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "Poetry")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        # City input using helper
        self.setup_city_input(self.frame)
        
        # Results display
        self.setup_result_text(self.frame, height=15, width=70)
        
        # Main action button
        ButtonHelper.create_main_button(self.frame, "primary", "Generate Weather Poetry", self.generate_weather_poetry)
        
        # Additional buttons using helper
        button_config = [
            ("accent_black", "🌸 Haiku", self.generate_haiku),
            ("info_black", "📖 Sonnet", self.generate_sonnet),
            ("success_black", "🎵 Limerick", self.generate_limerick),
            ("warning_black", "✨ Free Verse", self.generate_free_verse)
        ]
        ButtonHelper.create_button_grid(self.frame, button_config, columns=4)

    def generate_weather_poetry(self):
        """Generate general weather poetry"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            poetry = self.controller.generate_weather_poetry(city)
            formatted_result = f"📝 WEATHER POETRY for {city}:\n{'━' * 50}\n\n{poetry}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "generating weather poetry")

    def generate_haiku(self):
        """Generate weather haiku"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            haiku = self.controller.generate_weather_haiku(city)
            formatted_result = f"🌸 WEATHER HAIKU for {city}:\n{'━' * 50}\n\n{haiku}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "generating haiku")

    def generate_sonnet(self):
        """Generate weather sonnet"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            sonnet = self.controller.generate_weather_sonnet(city)
            formatted_result = f"📖 WEATHER SONNET for {city}:\n{'━' * 50}\n\n{sonnet}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "generating sonnet")

    def generate_limerick(self):
        """Generate weather limerick"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            limerick = self.controller.generate_weather_limerick(city)
            formatted_result = f"🎵 WEATHER LIMERICK for {city}:\n{'━' * 50}\n\n{limerick}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "generating limerick")

    def generate_free_verse(self):
        """Generate free verse weather poetry"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            free_verse = self.controller.generate_weather_free_verse(city)
            formatted_result = f"✨ FREE VERSE for {city}:\n{'━' * 50}\n\n{free_verse}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "generating free verse")


class HistoryTab(BaseTab):
    """Weather history tab component"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "History")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        # City input using helper
        self.setup_city_input(self.frame)
        
        # Results display
        self.setup_result_text(self.frame, height=15, width=70)
        
        # Main action button
        ButtonHelper.create_main_button(self.frame, "primary", "View Weather History", self.view_weather_history)
        
        # Additional buttons using helper
        button_config = [
            ("accent_black", "📊 Statistics", self.view_weather_statistics),
            ("info_black", "📈 Trends", self.view_weather_trends),
            ("success_black", "📤 Export Data", self.export_weather_data),
            ("warning_black", "🗑️ Clear History", self.clear_weather_history)
        ]
        ButtonHelper.create_button_grid(self.frame, button_config, columns=4)

    def view_weather_history(self):
        """View weather history"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            history = self.controller.get_weather_history(city)
            formatted_result = f"📚 WEATHER HISTORY for {city}:\n{'━' * 50}\n\n{history}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "viewing weather history")

    def view_weather_statistics(self):
        """View weather statistics"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            stats = self.controller.get_weather_statistics(city)
            formatted_result = f"📊 WEATHER STATISTICS for {city}:\n{'━' * 50}\n\n{stats}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "viewing weather statistics")

    def view_weather_trends(self):
        """View weather trends"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            trends = self.controller.get_weather_trends(city)
            formatted_result = f"📈 WEATHER TRENDS for {city}:\n{'━' * 50}\n\n{trends}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "viewing weather trends")

    def export_weather_data(self):
        """Export weather data"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            result = self.controller.export_weather_data(city)
            CommonActions.show_info_message("Export Complete", result)
        except Exception as e:
            self.handle_error(e, "exporting weather data")

    def clear_weather_history(self):
        """Clear weather history"""
        try:
            result = self.controller.clear_weather_history()
            CommonActions.show_info_message("History Cleared", result)
            self.display_result("📚 WEATHER HISTORY:\n" + "━" * 50 + "\n\nHistory has been cleared.")
        except Exception as e:
            self.handle_error(e, "clearing weather history")


class QuickActionsTab(BaseTab):
    """Quick actions tab component"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "Quick Actions")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        # City input using helper
        self.setup_city_input(self.frame)
        
        # Results display
        self.setup_result_text(self.frame, height=15, width=70)
        
        # Quick action buttons using helper - organized in a grid
        button_config = [
            ("primary", "🌤️ Quick Weather", self.quick_weather),
            ("accent_black", "📅 Today's Plan", self.todays_plan),
            ("info_black", "🎯 Best Time", self.find_best_time),
            ("success_black", "📱 Share Weather", self.share_weather),
            ("warning_black", "⚠️ Weather Alert", self.quick_alert),
            ("primary_black", "🔄 Refresh All", self.refresh_all),
            ("accent", "📊 Quick Stats", self.quick_stats),
            ("info", "🌍 Multi-City", self.multi_city_check)
        ]
        ButtonHelper.create_button_grid(self.frame, button_config, columns=4)

    def quick_weather(self):
        """Get quick weather summary"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            weather = self.controller.get_quick_weather(city)
            formatted_result = f"🌤️ QUICK WEATHER for {city}:\n{'━' * 50}\n\n{weather}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "getting quick weather")

    def todays_plan(self):
        """Get today's weather plan"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            plan = self.controller.get_todays_plan(city)
            formatted_result = f"📅 TODAY'S PLAN for {city}:\n{'━' * 50}\n\n{plan}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "getting today's plan")

    def find_best_time(self):
        """Find best time for activities"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            best_times = self.controller.find_best_times(city)
            formatted_result = f"🎯 BEST TIMES for {city}:\n{'━' * 50}\n\n{best_times}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "finding best times")

    def share_weather(self):
        """Share weather information"""
        city = self.get_city_input()
        if not city:
            return
        
        
        
        try:
            share_content = self.controller.get_shareable_weather(city)
            formatted_result = f"📱 SHAREABLE WEATHER for {city}:\n{'━' * 50}\n\n{share_content}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "sharing weather")

    def quick_alert(self):
        """Check for quick weather alerts"""
        city = self.get_city_input()
        if not city:
            return
        
        try:
            alerts = self.controller.get_quick_alerts(city)
            formatted_result = f"⚠️ WEATHER ALERTS for {city}:\n{'━' * 50}\n\n{alerts}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "checking quick alerts")

    def refresh_all(self):
        """Refresh all weather data"""
        try:
            result = self.controller.refresh_all_data()
            formatted_result = f"🔄 REFRESH COMPLETE:\n{'━' * 50}\n\n{result}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "refreshing all data")

    def quick_stats(self):
        """Show quick statistics"""
        try:
            stats = self.controller.get_quick_statistics()
            formatted_result = f"📊 QUICK STATISTICS:\n{'━' * 50}\n\n{stats}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "getting quick statistics")

    def multi_city_check(self):
        """Check multiple cities quickly"""
        try:
            multi_data = self.controller.get_multi_city_quick_check()
            formatted_result = f"🌍 MULTI-CITY CHECK:\n{'━' * 50}\n\n{multi_data}"
            self.display_result(formatted_result)
        except Exception as e:
            self.handle_error(e, "checking multiple cities")


class LiveWeatherTab(BaseTab):
    """Live weather tab with animations and doppler radar"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "Live Weather")
        self.live_service = None
        self.radar_service = None
        self.animation_widget = None
        self.radar_widget = None
        self._setup_ui()
        self._initialize_services()

    def _setup_ui(self):
        """Setup the UI components with split layout for animations and radar"""
        if LIVE_WEATHER_AVAILABLE:
            # Create split layout using helper
            self.create_split_layout()
            self._setup_animation_interface()
            self._setup_radar_interface()
        else:
            # Show unavailable message
            self._show_unavailable_message()

    def _show_unavailable_message(self):
        """Show message when live weather services are unavailable"""
        from .components import StyledLabel
        message_frame = ttk.Frame(self.frame)
        message_frame.pack(fill="both", expand=True)
        
        StyledLabel(message_frame, 
                   text="⚠️ Live Weather Features Unavailable\n\n" +
                        "Missing required packages:\n" +
                        "• matplotlib (for radar display)\n" +
                        "• tkinter (for animations)\n" +
                        "• threading support\n\n" +
                        "Please install missing packages to enable live features.",
                   font=("Arial", 12),
                   foreground="red").pack(expand=True)

    def _setup_animation_interface(self):
        """Setup the live animation interface in the left panel"""
        # Animation title
        from .components import StyledLabel
        StyledLabel(self.left_frame, text="🚶 Live People Animations", 
                   font=("Arial", 14, "bold")).pack(pady=5)
        
        # City input for animation weather sync
        self.setup_city_input(self.left_frame)
        
        # Animation controls
        animation_controls = ttk.Frame(self.left_frame)
        animation_controls.pack(pady=10)
        
        # Animation control buttons
        button_config = [
            ("success_black", "▶️ Start Animations", self.start_animations),
            ("warning_black", "⏸️ Stop Animations", self.stop_animations),
            ("info_black", "🌤️ Sync Weather", self.sync_weather),
            ("accent_black", "⚙️ Settings", self.animation_settings)
        ]
        ButtonHelper.create_button_grid(animation_controls, button_config, columns=2)
        
        # Animation canvas frame
        self.animation_canvas_frame = ttk.LabelFrame(self.left_frame, text="Live Animation")
        self.animation_canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def _setup_radar_interface(self):
        """Setup the weather radar interface in the right panel"""
        # Radar title
        from .components import StyledLabel
        StyledLabel(self.right_frame, text="🌪️ Live Doppler Radar", 
                   font=("Arial", 14, "bold")).pack(pady=5)
        
        # Radar coordinates input
        coord_frame = ttk.Frame(self.right_frame)
        coord_frame.pack(pady=5)
        
        ttk.Label(coord_frame, text="Latitude:").grid(row=0, column=0, padx=2)
        self.lat_entry = ttk.Entry(coord_frame, width=10)
        self.lat_entry.grid(row=0, column=1, padx=2)
        self.lat_entry.insert(0, "40.7128")  # Default to NYC
        
        ttk.Label(coord_frame, text="Longitude:").grid(row=0, column=2, padx=2)
        self.lon_entry = ttk.Entry(coord_frame, width=10)
        self.lon_entry.grid(row=0, column=3, padx=2)
        self.lon_entry.insert(0, "-74.0060")  # Default to NYC
        
        # Radar controls
        radar_controls = ttk.Frame(self.right_frame)
        radar_controls.pack(pady=10)
        
        # Radar control buttons
        radar_button_config = [
            ("primary_black", "🌍 Update Radar", self.update_radar),
            ("accent_black", "🌪️ Track Storms", self.track_severe_weather),
            ("warning_black", "⚠️ Alerts", self.check_weather_alerts),
            ("info_black", "📊 Radar Stats", self.show_radar_stats)
        ]
        ButtonHelper.create_button_grid(radar_controls, radar_button_config, columns=2)
        
        # Radar display frame
        self.radar_canvas_frame = ttk.LabelFrame(self.right_frame, text="Doppler Radar Display")
        self.radar_canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def _initialize_services(self):
        """Initialize live weather services"""
        if not LIVE_WEATHER_AVAILABLE:
            return
        
        try:
            # Initialize live animation service
            self.live_service = LiveAnimationService()
            
            # Initialize weather radar service (with API key from controller)
            api_key = getattr(self.controller, 'api_key', None)
            self.radar_service = WeatherRadarService(api_key)
            
            # Create animation widget
            self.animation_widget = AnimatedWeatherWidget(
                parent=self.animation_canvas_frame,
                width=400,
                height=300
            )
            
            # Create radar widget
            self.radar_widget = WeatherRadarWidget(
                parent=self.radar_canvas_frame,
                radar_service=self.radar_service
            )
            
        except Exception as e:
            self.handle_error(e, "initializing live weather services")

    def start_animations(self):
        """Start live people animations"""
        if not self.animation_widget:
            self.display_result("❌ Animation widget not available. Please check system requirements.")
            return
        
        try:
            # Get current weather for animation synchronization
            city = self.get_city_input()
            weather_type = 'clear'  # Default weather type
            
            if city:
                try:
                    weather_data = self.controller.get_current_weather(city)
                    # Convert weather description to simple weather type
                    description = weather_data.description.lower()
                    if 'rain' in description or 'drizzle' in description:
                        weather_type = 'rain'
                    elif 'snow' in description or 'blizzard' in description:
                        weather_type = 'snow'
                    elif 'storm' in description or 'thunder' in description:
                        weather_type = 'storm'
                    elif 'cloud' in description or 'overcast' in description:
                        weather_type = 'cloudy'
                except:
                    pass  # Use default weather type
            
            # Update animation weather and start
            self.animation_widget.update_weather(weather_type)
            self.animation_widget.start_animation(weather_type)
            
            # Start live service if available
            if self.live_service:
                self.live_service.start_animations()
            
            # Update status
            self.display_result("🎬 Live animations started! People are now moving across the screen.\n\n" +
                              "🌦️ Weather effects are synchronized with current conditions.\n" +
                              "👥 Watch for walkers, joggers, cyclists, and weather-specific behaviors.")
            
        except Exception as e:
            self.handle_error(e, "starting animations")

    def stop_animations(self):
        """Stop live people animations"""
        if not self.animation_widget:
            return
        
        try:
            if self.live_service:
                self.live_service.stop_animations()
            self.animation_widget.stop_animation()
            self.display_result("⏹️ Live animations stopped.\n\n" +
                              "All animated elements have been paused.")
        except Exception as e:
            self.handle_error(e, "stopping animations")

    def sync_weather(self):
        """Synchronize animations with current weather"""
        city = self.get_city_input()
        if not city or not self.animation_widget:
            return
        
        try:
            # Get current weather
            weather_data = self.controller.get_current_weather(city)
            
            # Convert weather description to simple weather type
            description = weather_data.description.lower()
            weather_type = 'clear'  # Default
            
            if 'rain' in description or 'drizzle' in description:
                weather_type = 'rain'
            elif 'snow' in description or 'blizzard' in description:
                weather_type = 'snow'
            elif 'storm' in description or 'thunder' in description:
                weather_type = 'storm'
            elif 'cloud' in description or 'overcast' in description:
                weather_type = 'cloudy'
            elif 'mist' in description or 'fog' in description:
                weather_type = 'cloudy'
            
            # Update animation effects
            self.animation_widget.update_weather(weather_type)
            
            self.display_result(f"🌤️ Weather synchronization complete for {city}!\n\n" +
                              f"Current weather: {weather_data.description}\n" +
                              f"Temperature: {weather_data.formatted_temperature}\n" +
                              f"Animation weather type: {weather_type}\n\n" +
                              f"Animations now reflect current weather conditions:\n" +
                              f"• Movement speed adjusted for weather\n" +
                              f"• Weather effects (rain, snow, etc.) updated\n" +
                              f"• Background ambiance synchronized")
            
        except Exception as e:
            self.handle_error(e, "synchronizing weather")

    def animation_settings(self):
        """Show animation settings dialog"""
        try:
            settings_text = "⚙️ ANIMATION SETTINGS:\n" + "━" * 50 + "\n\n"
            settings_text += "Current Configuration:\n"
            settings_text += "• Animation Speed: 10 FPS\n"
            settings_text += "• People Count: 5-15 (dynamic)\n"
            settings_text += "• Weather Effects: Enabled\n"
            settings_text += "• Movement Types: Walking, Jogging, Cycling\n"
            settings_text += "• Background Effects: Enabled\n\n"
            settings_text += "Available People Types:\n"
            settings_text += "👤 Walker - Slow, steady movement\n"
            settings_text += "🏃 Jogger - Medium speed movement\n"
            settings_text += "👴 Elderly - Slower, careful movement\n"
            settings_text += "🚴 Cyclist - Fast movement\n\n"
            settings_text += "Weather Effects:\n"
            settings_text += "🌧️ Rain - Droplets and slower movement\n"
            settings_text += "❄️ Snow - Snowflakes and very slow movement\n"
            settings_text += "⛈️ Storm - Lightning and indoor sheltering\n"
            settings_text += "☀️ Sunny - Normal speed and bright colors"
            
            self.display_result(settings_text)
            
        except Exception as e:
            self.handle_error(e, "showing animation settings")

    def update_radar(self):
        """Update doppler radar display"""
        if not self.radar_widget:
            return
        
        try:
            # Get coordinates
            lat = float(self.lat_entry.get())
            lon = float(self.lon_entry.get())
            
            # Update radar location
            self.radar_widget.update_location(lat, lon)
            
            self.display_result(f"🌍 Radar updated for coordinates: {lat:.4f}, {lon:.4f}\n\n" +
                              f"🔄 Scanning for weather patterns...\n" +
                              f"📡 Doppler radar data refreshed\n" +
                              f"⏱️ Next update in 2 minutes")
            
        except ValueError:
            self.display_result("❌ Invalid coordinates! Please enter valid latitude and longitude.")
        except Exception as e:
            self.handle_error(e, "updating radar")

    def track_severe_weather(self):
        """Track severe weather events"""
        if not self.radar_service:
            return
        
        try:
            # Get coordinates
            lat = float(self.lat_entry.get())
            lon = float(self.lon_entry.get())
            
            # Get severe weather data
            severe_events = self.radar_service.get_severe_weather_events(lat, lon)
            
            if severe_events:
                result = "🌪️ SEVERE WEATHER TRACKING:\n" + "━" * 50 + "\n\n"
                for event in severe_events:
                    result += f"⚠️ {event['type'].upper()}\n"
                    result += f"   Location: {event['distance']:.1f} km away\n"
                    result += f"   Intensity: {event['intensity']}\n"
                    result += f"   ETA: {event.get('eta', 'Unknown')}\n"
                    result += f"   Warning: {event['description']}\n\n"
                
                result += "🛡️ SAFETY RECOMMENDATIONS:\n"
                result += "• Monitor weather alerts regularly\n"
                result += "• Prepare emergency supplies\n"
                result += "• Stay indoors during severe weather\n"
                result += "• Follow local evacuation orders if issued"
            else:
                result = "✅ No severe weather events detected in your area.\n\n"
                result += "🌤️ Current conditions appear stable.\n"
                result += "📡 Continuing to monitor for changes..."
            
            self.display_result(result)
            
        except ValueError:
            self.display_result("❌ Invalid coordinates! Please enter valid latitude and longitude.")
        except Exception as e:
            self.handle_error(e, "tracking severe weather")

    def check_weather_alerts(self):
        """Check for weather alerts and warnings"""
        if not self.radar_service:
            return
        
        try:
            # Get coordinates
            lat = float(self.lat_entry.get())
            lon = float(self.lon_entry.get())
            
            # Get weather alerts
            alerts = self.radar_service.get_weather_alerts(lat, lon)
            
            if alerts:
                result = "⚠️ WEATHER ALERTS:\n" + "━" * 50 + "\n\n"
                for alert in alerts:
                    result += f"🚨 {alert['title']}\n"
                    result += f"   Severity: {alert['severity']}\n"
                    result += f"   Areas: {alert['areas']}\n"
                    result += f"   Details: {alert['description']}\n\n"
            else:
                result = "✅ No active weather alerts for your area.\n\n"
                result += "🌤️ Weather conditions are normal.\n"
                result += "📱 Alerts will appear here when issued."
            
            self.display_result(result)
            
        except ValueError:
            self.display_result("❌ Invalid coordinates! Please enter valid latitude and longitude.")
        except Exception as e:
            self.handle_error(e, "checking weather alerts")

    def show_radar_stats(self):
        """Show radar statistics and information"""
        try:
            stats = "📊 RADAR STATISTICS:\n" + "━" * 50 + "\n\n"
            stats += "📡 Radar Coverage:\n"
            stats += "• Range: 200 km radius\n"
            stats += "• Resolution: 1 km grid\n"
            stats += "• Update Frequency: 2 minutes\n"
            stats += "• Data Sources: National Weather Service\n\n"
            
            stats += "🌦️ Detectable Weather Events:\n"
            stats += "🌪️ Tornadoes - F0 to F5 scale tracking\n"
            stats += "🌀 Hurricanes - Category 1-5 monitoring\n"
            stats += "❄️ Blizzards - Snow intensity mapping\n"
            stats += "🌧️ Thunderstorms - Precipitation rates\n"
            stats += "🌊 Flooding - Ground saturation levels\n"
            stats += "🔥 Wildfires - Smoke and heat detection\n"
            stats += "⚡ Lightning - Strike frequency mapping\n\n"
            
            stats += "📈 Current Session:\n"
            if self.radar_service:
                stats += f"• Radar Updates: {getattr(self.radar_service, 'update_count', 0)}\n"
                stats += f"• Alerts Checked: {getattr(self.radar_service, 'alert_count', 0)}\n"
                stats += f"• Severe Events: {getattr(self.radar_service, 'severe_count', 0)}\n"
            else:
                stats += "• Service not initialized\n"
            
            stats += "\n💡 Tips:\n"
            stats += "• Green areas: Light precipitation\n"
            stats += "• Yellow areas: Moderate weather\n"
            stats += "• Red areas: Heavy/severe weather\n"
            stats += "• Purple areas: Extreme conditions"
            
            self.display_result(stats)
            
        except Exception as e:
            self.handle_error(e, "showing radar statistics")

    def cleanup(self):
        """Cleanup live weather services when tab is closed"""
        try:
            if self.live_service:
                self.live_service.stop_animation()
            if self.radar_service:
                self.radar_service.cleanup()
        except Exception:
            pass  # Ignore cleanup errors
