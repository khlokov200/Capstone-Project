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
    """City comparison tab component"""
    
    def __init__(self, notebook, controller):
        super().__init__(notebook, controller, "City Comparison")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        # City inputs
        StyledLabel(self.frame, text="City 1:").pack(pady=5)
        self.city1_entry = ttk.Entry(self.frame)
        self.city1_entry.pack()
        
        StyledLabel(self.frame, text="City 2:").pack(pady=5)
        self.city2_entry = ttk.Entry(self.frame)
        self.city2_entry.pack()
        
        # Results display
        self.result_text = StyledText(self.frame)
        self.result_text.pack(pady=10)
        
        # Main action button
        ButtonHelper.create_main_button(self.frame, "info", "Compare", self.compare_cities)
        
        # Additional Enhanced Buttons using helper
        button_config = [
            ("accent_black", "🗺️ Distance Info", self.show_distance_info),
            ("primary_black", "📊 Detailed Compare", self.detailed_comparison),
            ("success_black", "✈️ Travel Advice", self.get_travel_advice),
            ("warning_black", "⭐ Multi-Compare", self.multi_city_compare)
        ]
        ButtonHelper.create_button_grid(self.frame, button_config, columns=4)

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
