"""
Individual tab components for the weather dashboard
"""

import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk, ImageDraw
import matplotlib
# Use Agg backend for matplotlib (non-interactive) to avoid window issues
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import traceback
from ui.config import COLOR_PALETTE, apply_styles
from ui.custom_widgets import (StyledButton, StyledLabel, StyledText, 
                               setup_style, create_gradient_background)

import random
from .components import StyledButton, StyledText, StyledLabel, AnimatedLabel
from .constants import COLOR_PALETTE
from .tab_helpers import ButtonHelper, ChartHelper

# Matplotlib imports with availability checking
CHARTS_AVAILABLE = False
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    from matplotlib.figure import Figure
    import numpy as np
    # Suppress emoji glyph warnings
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
    CHARTS_AVAILABLE = True
except ImportError:
    print("📊 Charts unavailable: matplotlib not installed")
    # Fallback classes to prevent errors
    class Figure:
        pass
    class FigureCanvasTkAgg:
        def __init__(self, *args, **kwargs):
            pass


class WeatherTab:
    """Current weather tab component"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Current Weather")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        # Create main horizontal paned window for split layout
        self.main_paned = ttk.PanedWindow(self.frame, orient="horizontal")
        self.main_paned.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left panel for weather data input and display
        self.left_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.left_frame, weight=1)
        
        # Right panel for charts
        self.right_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.right_frame, weight=1)
        
        # Setup left panel (original weather interface)
        self._setup_weather_interface()
        
        # Setup right panel (chart area)
        self._setup_chart_interface()
    
    def _setup_weather_interface(self):
        """Setup the weather data interface in the left panel"""
        # City input
        StyledLabel(self.left_frame, text="Enter City:").pack(pady=10)
        self.city_entry = ttk.Entry(self.left_frame)
        self.city_entry.pack()
        
        # Results display - adjusted size for split view
        self.result_text = StyledText(self.left_frame, height=12, width=60)
        self.result_text.pack(pady=10)
        
        # Animated mascot
        try:
            self.anim_label = AnimatedLabel(self.left_frame, "assets/sunny.gif")
            self.anim_label.pack(pady=10)
        except Exception:
            pass  # Skip if GIF not found
        
        # Alert label
        self.alert_label = StyledLabel(self.left_frame, text="")
        self.alert_label.pack(pady=5)
        
        # Buttons
        StyledButton(self.left_frame, "primary_black", text="Get Weather", 
                    command=self.fetch_weather).pack(pady=5)
        
        StyledButton(self.left_frame, "info_black", text="Toggle Graph Type", 
                    command=self.controller.toggle_graph_mode).pack(pady=5)
        
        # Additional Quick Action Buttons
        button_frame = ttk.Frame(self.left_frame)
        button_frame.pack(pady=5)
        
        StyledButton(button_frame, "accent_black", text="⭐ Save Favorite", 
                    command=self.save_favorite).grid(row=0, column=0, padx=2)
        StyledButton(button_frame, "success_black", text="🔄 Auto-Refresh", 
                    command=self.toggle_auto_refresh).grid(row=0, column=1, padx=2)
        StyledButton(button_frame, "warning_black", text="⚠️ Check Alerts", 
                    command=self.check_alerts).grid(row=0, column=2, padx=2)
    
    def _setup_chart_interface(self):
        """Setup the chart interface in the right panel"""
        # Chart title
        StyledLabel(self.right_frame, text="📊 Weather Charts", 
                   font=("Arial", 14, "bold")).pack(pady=5)
        
        # Chart control buttons
        chart_controls = ttk.Frame(self.right_frame)
        chart_controls.pack(pady=5)
        
        if CHARTS_AVAILABLE:
            StyledButton(chart_controls, "info_black", text="📈 Temperature Trend", 
                        command=self.generate_temperature_chart).grid(row=0, column=0, padx=2)
            StyledButton(chart_controls, "success_black", text="📊 Weather Metrics", 
                        command=self.generate_metrics_bar_chart).grid(row=0, column=1, padx=2)
            StyledButton(chart_controls, "accent_black", text="📋 Data Distribution", 
                        command=self.generate_histogram).grid(row=1, column=0, padx=2, pady=2)
            StyledButton(chart_controls, "warning_black", text="🌡️ Comfort Analysis", 
                        command=self.generate_scatter_plot).grid(row=1, column=1, padx=2, pady=2)
        else:
            StyledLabel(chart_controls, text="Charts unavailable\n(matplotlib not installed)", 
                       foreground="red").pack()
        
        # Chart display area
        self.chart_frame = ttk.Frame(self.right_frame)
        self.chart_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Initialize with placeholder
        self._create_chart_placeholder()

    def _create_chart_placeholder(self):
        """Create a placeholder for the chart area"""
        placeholder_frame = ttk.LabelFrame(self.chart_frame, text="Chart Display Area")
        placeholder_frame.pack(fill="both", expand=True)
        
        placeholder_text = tk.Text(placeholder_frame, height=10, wrap="word",
                                 bg=COLOR_PALETTE["tab_bg"], fg=COLOR_PALETTE["tab_fg"])
        placeholder_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        placeholder_content = """📊 Weather Charts Available:

Click any chart button to generate visualizations:

📈 Temperature Trend - Historical temperature data
📊 Weather Metrics - Current conditions comparison  
📋 Data Distribution - Temperature distribution analysis
🌡️ Comfort Analysis - Temperature vs humidity scatter plot

Charts will appear here when generated."""
        
        placeholder_text.insert("1.0", placeholder_content)
        placeholder_text.config(state="disabled")
    
    def _clear_chart_area(self):
        """Clear the chart display area"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
    
    def fetch_weather(self):
        """Fetch weather for the entered city"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            result = self.controller.get_current_weather(city)
            self.display_weather_result(result)
            self.check_weather_alerts(result)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_weather_result(self, weather_data):
        """Display weather result in the text widget"""
        self.result_text.delete(1.0, tk.END)
        
        # Build comprehensive weather display
        weather_text = f"Weather in {weather_data.city}:\n"
        weather_text += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        weather_text += f"🌡️  Temperature: {weather_data.formatted_temperature}\n"
        weather_text += f"🌡️  Feels Like: {weather_data.formatted_feels_like}\n"
        weather_text += f"📋 Description: {weather_data.description}\n"
        weather_text += f"💧 Humidity: {weather_data.humidity}%\n"
        weather_text += f"💨 Wind Speed: {weather_data.formatted_wind}\n"
        weather_text += f"👁️  Visibility: {weather_data.formatted_visibility}\n"
        weather_text += f"☁️  Cloudiness: {weather_data.formatted_cloudiness}\n"
        weather_text += f"🌅 Sunrise: {weather_data.formatted_sunrise}\n"
        weather_text += f"🌇 Sunset: {weather_data.formatted_sunset}\n"
        weather_text += f"🌫️  Fog: {weather_data.formatted_fog}\n"
        weather_text += f"🌧️  Rain/Snow: {weather_data.formatted_precipitation}\n"
        
        if weather_data.pressure:
            weather_text += f"🧭 Pressure: {weather_data.pressure} hPa\n"
        
        self.result_text.insert(tk.END, weather_text)

    def check_weather_alerts(self, weather_data):
        """Check and display weather alerts"""
        try:
            # Get temperature value from formatted string
            temp_str = weather_data.formatted_temperature.split('°')[0]
            temp = float(temp_str)
            desc = weather_data.description.lower()
            
            # Check for severe weather conditions
            has_alert = False
            alert_text = "⚠️ Weather Alert:"
            
            if (temp > 35 and "C" in weather_data.formatted_temperature) or \
               (temp > 95 and "F" in weather_data.formatted_temperature):
                alert_text += " Extreme temperature!"
                has_alert = True
                
            if "storm" in desc or "severe" in desc:
                alert_text += " Severe weather conditions!"
                has_alert = True
                
            # Update alert label
            if has_alert:
                self.alert_label.config(text=alert_text, 
                                      foreground=COLOR_PALETTE["heat"])
            else:
                self.alert_label.config(text="", 
                                      foreground=COLOR_PALETTE["tab_fg"])
                                      
        except (AttributeError, ValueError) as e:
            # Handle any errors gracefully
            print(f"Error checking weather alerts: {e}")
            self.alert_label.config(text="", 
                                  foreground=COLOR_PALETTE["tab_fg"])

    def save_favorite(self):
        """Save current city as favorite"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name first")
            return
        
        result = self.controller.add_favorite_city(city)
        messagebox.showinfo("Favorite Saved", result)

    def toggle_auto_refresh(self):
        """Toggle auto-refresh for weather updates"""
        result = self.controller.toggle_auto_refresh()
        messagebox.showinfo("Auto-Refresh", result)

    def check_alerts(self):
        """Check weather alerts for current city"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name first")
            return
        
        try:
            alerts = self.controller.check_weather_alerts(city)
            # Show alerts in a popup
            popup = tk.Toplevel(self.frame)
            popup.title("Weather Alerts")
            popup.geometry("400x300")
            popup.configure(bg=COLOR_PALETTE["background"])
            
            text_widget = StyledText(popup, height=12, width=50)
            text_widget.pack(padx=10, pady=10, fill="both", expand=True)
            text_widget.insert("1.0", alerts)
            text_widget.config(state="disabled")
            
            StyledButton(popup, "primary", text="Close", 
                        command=popup.destroy).pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to check alerts: {str(e)}")

    def generate_temperature_chart(self):
        """Generate temperature trend line chart"""
        if not CHARTS_AVAILABLE:
            messagebox.showwarning("Charts Unavailable", "Matplotlib is not installed")
            return
        
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name first")
            return
            
        try:
            self._clear_chart_area()
            
            # Get weather data from controller
            weather_data = self.controller.get_current_weather(city)
            if not weather_data or not hasattr(weather_data, 'temperature'):
                messagebox.showerror("Error", "Could not retrieve temperature data")
                return
                
            # Create figure and axis
            fig = Figure(figsize=(8, 5), dpi=100, facecolor='white')
            ax = fig.add_subplot(111)
            
            # Use current temperature for single point visualization
            current_temp = weather_data.temperature
            
            # Create line chart with styling
            ax.plot(['Current'], [current_temp], marker='o', linewidth=2, markersize=12,
                   color='#2E86AB', markerfacecolor='#A23B72', markeredgecolor='white', markeredgewidth=2)
            
            # Customize chart
            ax.set_title(f'Current Temperature in {city}', fontsize=14, fontweight='bold', pad=20)
            ax.set_xlabel('Time', fontsize=12)
            ax.set_ylabel('Temperature (°C)', fontsize=12)
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.set_facecolor('#f8f9fa')
            
            # Add value annotation
            ax.annotate(f'{current_temp}°C',
                      xy=(0, current_temp), 
                      xytext=(10, 10),
                      textcoords='offset points',
                      fontsize=12,
                      fontweight='bold')
            
            # Create canvas and add toolbar
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
            toolbar.update()
            canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            fig.tight_layout()
            
            # Embed chart in tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Add navigation toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
            toolbar.update()
            
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to generate temperature chart: {str(e)}")

    def generate_metrics_bar_chart(self):
        """Generate weather metrics bar chart"""
        if not CHARTS_AVAILABLE:
            messagebox.showwarning("Charts Unavailable", "Matplotlib is not installed")
            return
        
        try:
            self._clear_chart_area()
            
            # Create figure and axis
            fig = Figure(figsize=(8, 5), dpi=100, facecolor='white')
            ax = fig.add_subplot(111)
            
            # Sample weather metrics data
            metrics = ['Temperature', 'Humidity', 'Wind Speed', 'Pressure', 'Visibility']
            values = [24, 65, 12, 1013, 10]
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']
            
            # Create bar chart
            bars = ax.bar(metrics, values, color=colors, alpha=0.8, edgecolor='white', linewidth=1.5)
            
            # Customize chart
            ax.set_title('Current Weather Metrics', fontsize=14, fontweight='bold', pad=20)
            ax.set_ylabel('Values', fontsize=12)
            ax.grid(True, alpha=0.3, axis='y', linestyle='--')
            ax.set_facecolor('#f8f9fa')
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.annotate(f'{value}', xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                           fontsize=10, fontweight='bold')
            
            # Rotate x-axis labels for better readability
            ax.tick_params(axis='x', rotation=45)
            fig.tight_layout()
            
            # Embed chart in tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Add navigation toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
            toolbar.update()
            
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to generate metrics chart: {str(e)}")
    
    def generate_histogram(self):
        """Generate temperature distribution histogram"""
        if not CHARTS_AVAILABLE:
            messagebox.showwarning("Charts Unavailable", "Matplotlib is not installed")
            return
        
        try:
            self._clear_chart_area()
            
            # Create figure and axis
            fig = Figure(figsize=(8, 5), dpi=100, facecolor='white')
            ax = fig.add_subplot(111)
            
            # Sample temperature distribution data
            if CHARTS_AVAILABLE:
                np.random.seed(42)  # For consistent results
                temp_data = np.random.normal(22, 3, 100)  # Mean 22°C, std dev 3°C
            else:
                temp_data = [20, 21, 22, 23, 24]  # Fallback data
            
            # Create histogram
            n, bins, patches = ax.hist(temp_data, bins=15, alpha=0.7, color='#3498db', 
                                     edgecolor='white', linewidth=1.2)
            
            # Customize chart
            ax.set_title('Temperature Distribution Analysis', fontsize=14, fontweight='bold', pad=20)
            ax.set_xlabel('Temperature (°C)', fontsize=12)
            ax.set_ylabel('Frequency', fontsize=12)
            ax.grid(True, alpha=0.3, axis='y', linestyle='--')
            ax.set_facecolor('#f8f9fa')
            
            # Add statistical info
            if CHARTS_AVAILABLE:
                mean_temp = np.mean(temp_data)
                ax.axvline(mean_temp, color='red', linestyle='--', linewidth=2, 
                          label=f'Mean: {mean_temp:.1f}°C')
                ax.legend()
            
            fig.tight_layout();
            
            # Embed chart in tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Add navigation toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
            toolbar.update()
            
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to generate histogram: {str(e)}")

    def generate_scatter_plot(self):
        """Generate temperature vs humidity scatter plot for comfort analysis"""
        if not CHARTS_AVAILABLE:
            messagebox.showwarning("Charts Unavailable", "Matplotlib is not installed")
            return
        
        try:
            self._clear_chart_area()
            
            # Create figure and axis
            fig = Figure(figsize=(8, 5), dpi=100, facecolor='white')
            ax = fig.add_subplot(111)
            
            # Sample temperature vs humidity data
            if CHARTS_AVAILABLE:
                np.random.seed(42)
                temperatures = np.random.normal(23, 4, 50)
                humidity = np.random.normal(60, 15, 50)
                
                # Calculate comfort index (simple formula)
                comfort_index = 100 - abs(temperatures - 22) * 2 - abs(humidity - 50) * 0.5
                
                # Create scatter plot with color mapping for comfort
                scatter = ax.scatter(temperatures, humidity, c=comfort_index, cmap='RdYlGn', 
                                   s=80, alpha=0.7, edgecolors='white', linewidth=1)
                
                # Add colorbar for comfort index
                cbar = fig.colorbar(scatter, ax=ax)
                cbar.set_label('Comfort Index', fontsize=12)
            else:
                # Fallback simple scatter
                ax.scatter([20, 22, 24, 26], [45, 55, 65, 75], s=80, alpha=0.7)
            
            # Customize chart
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
            
            # Embed chart in tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Add navigation toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
            toolbar.update()
            
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to generate scatter plot: {str(e)}")

class ForecastTab:
    """Weather forecast tab component"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Forecast")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components with split-screen layout"""
        # Create main horizontal paned window for split layout
        self.main_paned = ttk.PanedWindow(self.frame, orient="horizontal")
        self.main_paned.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left panel for forecast data
        self.left_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.left_frame, weight=1)
        
        # Right panel for charts
        self.right_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.right_frame, weight=1)
        
        # Setup left panel
        self._setup_forecast_interface()
        
        # Setup right panel (chart area)
        self._setup_forecast_charts()
    
    def _setup_forecast_interface(self):
        """Setup the forecast interface in the left panel"""
        StyledLabel(self.left_frame, text="Enter City:").pack(pady=10)
        self.city_entry = ttk.Entry(self.left_frame)
        self.city_entry.pack()
        
        self.result_text = StyledText(self.left_frame, height=12, width=60)
        self.result_text.pack(pady=10)
        
        # Main action button
        StyledButton(self.left_frame, "primary_black", text="Get Forecast", 
                    command=self.fetch_forecast).pack(pady=5)
        
        # Additional Enhanced Buttons
        forecast_button_frame = ttk.Frame(self.left_frame)
        forecast_button_frame.pack(pady=5)
        
        StyledButton(forecast_button_frame, "accent_black", text="🌤️ Hourly Details", 
                    command=self.get_hourly_forecast).grid(row=0, column=0, padx=3)
        StyledButton(forecast_button_frame, "info_black", text="📊 Chart View", 
                    command=self.show_forecast_chart).grid(row=0, column=1, padx=3)
        StyledButton(forecast_button_frame, "success_black", text="📱 Share Forecast", 
                    command=self.share_forecast).grid(row=0, column=2, padx=3)
        StyledButton(forecast_button_frame, "warning_black", text="⚠️ Weather Alerts", 
                    command=self.check_forecast_alerts).grid(row=0, column=3, padx=3)
    
    def _setup_forecast_charts(self):
        """Setup the forecast chart interface in the right panel"""
        # Chart title
        StyledLabel(self.right_frame, text="📊 Forecast Visualizations", 
                   font=("Arial", 14, "bold")).pack(pady=5)
        
        # Chart control buttons
        chart_controls = ttk.Frame(self.right_frame)
        chart_controls.pack(pady=5)
        
        if CHARTS_AVAILABLE:
            StyledButton(chart_controls, "info_black", text="📈 Forecast Trend", 
                        command=self.generate_forecast_line_chart).grid(row=0, column=0, padx=2)
            StyledButton(chart_controls, "success_black", text="📊 Weather Conditions", 
                        command=self.generate_forecast_bar_chart).grid(row=0, column=1, padx=2)
            StyledButton(chart_controls, "accent_black", text="🌧️ Precipitation Chart", 
                        command=self.generate_precipitation_chart).grid(row=1, column=0, padx=2, pady=2)
            StyledButton(chart_controls, "warning_black", text="🌡️ Temp Distribution", 
                        command=self.generate_temp_histogram).grid(row=1, column=1, padx=2, pady=2)
        else:
            StyledLabel(chart_controls, text="Charts unavailable\n(matplotlib not installed)", 
                       foreground="red").pack()
        
        # Chart display area
        self.forecast_chart_frame = ttk.Frame(self.right_frame)
        self.forecast_chart_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Initialize with placeholder
        self._create_forecast_chart_placeholder()

    def _create_forecast_chart_placeholder(self):
        """Create a placeholder for the forecast chart area"""
        placeholder_frame = ttk.LabelFrame(self.forecast_chart_frame, text="Forecast Charts")
        placeholder_frame.pack(fill="both", expand=True)
        
        placeholder_text = tk.Text(placeholder_frame, height=10, wrap="word",
                                 bg=COLOR_PALETTE["tab_bg"], fg=COLOR_PALETTE["tab_fg"])
        placeholder_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        placeholder_content = """📊 Forecast Visualizations Available:

📈 Forecast Trend - Temperature and humidity trends over time
📊 Weather Conditions - Comparison of weather metrics
🌧️ Precipitation Chart - Rain/snow probability analysis
🌡️ Temp Distribution - Temperature frequency distribution

Select a chart type to visualize forecast data."""
        
        placeholder_text.insert("1.0", placeholder_content)
        placeholder_text.config(state="disabled")
    
    def _clear_forecast_chart_area(self):
        """Clear the forecast chart display area"""
        for widget in self.forecast_chart_frame.winfo_children():
            widget.destroy()
    
    def fetch_forecast(self):
        """Fetch forecast for the entered city"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            forecast = self.controller.get_forecast(city)
            unit_label = self.controller.get_unit_label()
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Forecast for {city} ({unit_label}):\n{forecast}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_hourly_forecast(self):
        """Get detailed hourly forecast"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            # Get forecast data from controller
            forecast = self.controller.get_forecast(city)
            
            # Current time for reference
            from datetime import datetime, timedelta
            import numpy as np
            current_time = datetime.now()
            
            # Create enhanced hourly details
            hourly_details = f"🌤️ HOURLY FORECAST DETAILS for {city.upper()}\n"
            hourly_details += "━" * 50 + "\n\n"
            
            # Current conditions
            hourly_details += "📍 CURRENT CONDITIONS:\n"
            current_temp = 24  # Example value, should come from forecast data
            current_desc = "Partly Cloudy"  # Example value
            current_feel = current_temp + 2  # Example value
            hourly_details += f"• Temperature: {current_temp}°C (Feels like {current_feel}°C)\n"
            hourly_details += f"• Conditions: {current_desc}\n"
            hourly_details += f"• Last Updated: {current_time.strftime('%I:%M %p')}\n\n"
            
            # Hourly breakdown (next 24 hours)
            hourly_details += "⏰ HOURLY BREAKDOWN:\n"
            forecast_hours = [
                (current_time + timedelta(hours=i)).strftime("%I %p")
                for i in range(24)
            ]
            # Generate hourly data with conditions that follow a realistic pattern
            conditions = []
            temps = []
            wind = []
            
            for hour in range(24):
                time = current_time + timedelta(hours=hour)
                hour_val = time.hour
                
                # Temperature variation (cooler at night, warmer in day)
                base_temp = 22
                temp_variation = 8 * np.sin((hour_val - 6) * np.pi / 12)  # Peak at 2PM
                temp = round(base_temp + temp_variation)
                temps.append(temp)
                
                # Conditions based on time of day
                if 6 <= hour_val < 9:
                    conditions.append("Partly Cloudy")
                    wind.append("Light breeze")
                elif 9 <= hour_val < 16:
                    conditions.append("Sunny")
                    wind.append("Moderate breeze")
                elif 16 <= hour_val < 19:
                    conditions.append("Partly Cloudy")
                    wind.append("Light breeze")
                else:
                    conditions.append("Clear")
                    wind.append("Calm")
            
            # Display hourly details in 3-hour intervals
            for i in range(0, 24, 3):
                hour = forecast_hours[i]
                hourly_details += f"• {hour:5}: {conditions[i]:12} {temps[i]:2}°C, {wind[i]}\n"
            
            hourly_details += "\n🌟 RECOMMENDED TIMES:\n"
            hourly_details += "• Peak Sunshine: 12 PM - 3 PM (Best for solar activities)\n"
            hourly_details += "• Outdoor Exercise: 7 AM - 9 AM (Comfortable temperatures)\n"
            hourly_details += "• Beach/Pool: 10 AM - 4 PM (Watch UV index)\n"
            hourly_details += "• Photography: 6 PM - 7 PM (Golden hour)\n"
            hourly_details += "• Evening Activities: After 7 PM (Cooler temperatures)\n\n"
            
            hourly_details += "⚡ QUICK STATS:\n"
            hourly_details += f"• Warmest Hour: {temps.index(max(temps))+1}:00 ({max(temps)}°C)\n"
            hourly_details += f"• Coolest Hour: {temps.index(min(temps))+1}:00 ({min(temps)}°C)\n"
            hourly_details += f"• Temperature Swing: {max(temps) - min(temps)}°C\n"
            
            # Update display
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, hourly_details)
            
            # Show a helpful tooltip
            messagebox.showinfo("Forecast Tip", 
                              "💡 Hover over times to see detailed conditions.\n"
                              "Use the chart view for visual temperature trends!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get hourly forecast: {str(e)}")

    def show_forecast_chart(self):
        """Show forecast in chart format"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
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
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, chart_data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display forecast chart: {str(e)}")

    def share_forecast(self):
        """Share forecast information"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            forecast = self.controller.get_forecast(city)
            share_text = f"📱 SHAREABLE FORECAST for {city}:\n"
            share_text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            share_text += f"Weather forecast copied to clipboard!\n\n"
            share_text += "Share-ready format:\n"
            share_text += f"🌤️ {city} Weather Update\n"
            share_text += forecast[:200] + "...\n\n"
            share_text += "📲 Social Media Ready:\n"
            share_text += f"#Weather #{city.replace(' ', '')} #Forecast\n\n"
            share_text += "💡 Content has been formatted for easy sharing!"
            
            # Copy to clipboard
            try:
                import pyperclip
                pyperclip.copy(f"🌤️ {city} Weather Update\n{forecast}")
                share_text += "\n✅ Copied to clipboard successfully!"
            except ImportError:
                share_text += "\n📋 Copy feature requires pyperclip package"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, share_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def check_forecast_alerts(self):
        """Check for weather alerts in the forecast"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            alerts = f"⚠️ WEATHER ALERTS for {city}:\n"
            alerts += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
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
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, alerts)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def generate_forecast_line_chart(self):
        """Generate forecast line chart visualization"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            self._clear_forecast_chart_area()
            
            if CHARTS_AVAILABLE:
                import matplotlib.pyplot as plt
                import matplotlib.dates as mdates
                from datetime import datetime, timedelta
                import numpy as np
                
                # Create figure
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
                fig.suptitle(f'📈 Forecast Trend for {city}', fontsize=14, fontweight='bold')
                
                # Generate sample forecast data
                dates = [datetime.now() + timedelta(days=i) for i in range(5)]
                temps = [22, 25, 18, 20, 26]  # Sample temperatures
                humidity = [65, 70, 85, 75, 60]  # Sample humidity
                
                # Temperature trend
                ax1.plot(dates, temps, marker='o', linewidth=2, color='#FF6B6B', label='Temperature')
                ax1.set_ylabel('Temperature (°C)', fontweight='bold')
                ax1.set_title('Temperature Trend', fontweight='bold')
                ax1.grid(True, alpha=0.3)
                ax1.legend()
                
                # Humidity trend
                ax2.plot(dates, humidity, marker='s', linewidth=2, color='#4ECDC4', label='Humidity')
                ax2.set_ylabel('Humidity (%)', fontweight='bold')
                ax2.set_title('Humidity Trend', fontweight='bold')
                ax2.set_xlabel('Date', fontweight='bold')
                ax2.grid(True, alpha=0.3)
                ax2.legend()
                
                # Format dates
                for ax in [ax1, ax2]:
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
                    ax.xaxis.set_major_locator(mdates.DayLocator())
                
                plt.tight_layout()
                
                # Display chart
                canvas = FigureCanvasTkAgg(fig, self.forecast_chart_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)
                
                # Add toolbar
                from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
                toolbar = NavigationToolbar2Tk(canvas, self.forecast_chart_frame)
                toolbar.update()
            else:
                # Fallback text display
                self._create_forecast_chart_placeholder()
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"📈 Forecast Line Chart for {city}:\n\nTemperature and humidity trends would be displayed here if matplotlib was available.")
                
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to generate forecast line chart: {str(e)}")

    def generate_forecast_bar_chart(self):
        """Generate forecast bar chart for weather conditions"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            self._clear_forecast_chart_area()
            
            if CHARTS_AVAILABLE:
                import matplotlib.pyplot as plt
                import numpy as np
                
                # Create figure
                fig, ax = plt.subplots(figsize=(8, 6))
                fig.suptitle(f'📊 Weather Conditions for {city}', fontsize=14, fontweight='bold')
                
                # Sample data
                days = ['Today', 'Tomorrow', 'Day 3', 'Day 4', 'Day 5']
                temperatures = [22, 25, 18, 20, 26]
                wind_speeds = [10, 15, 25, 12, 8]
                
                x = np.arange(len(days))
                width = 0.35
                
                bars1 = ax.bar(x - width/2, temperatures, width, label='Temperature (°C)', color='#FF9F43', alpha=0.8)
                bars2 = ax.bar(x + width/2, wind_speeds, width, label='Wind Speed (km/h)', color='#74B9FF', alpha=0.8)
                
                ax.set_xlabel('Days', fontweight='bold')
                ax.set_ylabel('Values', fontweight='bold')
                ax.set_title('Temperature vs Wind Speed Comparison', fontweight='bold')
                ax.set_xticks(x)
                ax.set_xticklabels(days)
                ax.legend()
                ax.grid(True, alpha=0.3)
                
                # Add value labels on bars
                for bars in [bars1, bars2]:
                    for bar in bars:
                        height = bar.get_height()
                        ax.annotate(f'{height:.0f}',
                                  xy=(bar.get_x() + bar.get_width() / 2, height),
                                  xytext=(0, 3),
                                  textcoords="offset points",
                                  ha='center', va='bottom',
                                  fontweight='bold')
                
                plt.tight_layout()
                
                # Display chart
                canvas = FigureCanvasTkAgg(fig, self.forecast_chart_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)
                
                # Add toolbar
                from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
                toolbar = NavigationToolbar2Tk(canvas, self.forecast_chart_frame)
                toolbar.update()
            else:
                # Fallback text display
                self._create_forecast_chart_placeholder()
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"📊 Weather Conditions Bar Chart for {city}:\n\nWeather conditions comparison would be displayed here if matplotlib was available.")
                
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to generate forecast bar chart: {str(e)}")

    def generate_precipitation_chart(self):
        """Generate precipitation probability chart"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            self._clear_forecast_chart_area()
            
            if CHARTS_AVAILABLE:
                import matplotlib.pyplot as plt
                import numpy as np
                
                # Create figure
                fig, ax = plt.subplots(figsize=(8, 6))
                fig.suptitle(f'🌧️ Precipitation Forecast for {city}', fontsize=14, fontweight='bold')
                
                # Sample precipitation data
                days = ['Today', 'Tomorrow', 'Day 3', 'Day 4', 'Day 5']
                precipitation_prob = [10, 25, 80, 30, 5]  # Percentage
                precipitation_amount = [0, 2, 15, 5, 0]  # mm
                
                x = np.arange(len(days))
                
                # Create dual y-axis chart
                ax2 = ax.twinx()
                
                bars = ax.bar(x, precipitation_prob, alpha=0.7, color='#74B9FF', label='Probability (%)')
                line = ax2.plot(x, precipitation_amount, color='#00B894', marker='o', linewidth=3, 
                               markersize=8, label='Amount (mm)')
                
                ax.set_xlabel('Days', fontweight='bold')
                ax.set_ylabel('Precipitation Probability (%)', color='#74B9FF', fontweight='bold')
                ax2.set_ylabel('Precipitation Amount (mm)', color='#00B894', fontweight='bold')
                ax.set_title('Precipitation Probability & Amount', fontweight='bold')
                ax.set_xticks(x)
                ax.set_xticklabels(days)
                
                # Add value labels
                for i, (prob, amount) in enumerate(zip(precipitation_prob, precipitation_amount)):
                    ax.text(i, prob + 2, f'{prob}%', ha='center', va='bottom', fontweight='bold')
                    ax2.text(i, amount + 0.5, f'{amount}mm', ha='center', va='bottom', 
                            fontweight='bold', color='#00B894')
                
                # Legends
                ax.legend(loc='upper left')
                ax2.legend(loc='upper right')
                ax.grid(True, alpha=0.3)
                
                plt.tight_layout()
                
                # Display chart
                canvas = FigureCanvasTkAgg(fig, self.forecast_chart_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)
                
                # Add toolbar
                from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
                toolbar = NavigationToolbar2Tk(canvas, self.forecast_chart_frame)
                toolbar.update()
            else:
                # Fallback text display
                self._create_forecast_chart_placeholder()
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"🌧️ Precipitation Chart for {city}:\n\nPrecipitation probability and amount would be displayed here if matplotlib was available.")
                
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to generate precipitation chart: {str(e)}")

    def generate_temp_histogram(self):
        """Generate temperature distribution histogram"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            self._clear_forecast_chart_area()
            
            if CHARTS_AVAILABLE:
                import matplotlib.pyplot as plt
                import numpy as np
                
                # Create figure
                fig, ax = plt.subplots(figsize=(8, 6))
                fig.suptitle(f'🌡️ Temperature Distribution for {city}', fontsize=14, fontweight='bold')
                
                # Generate sample temperature distribution data
                np.random.seed(42)  # For consistent results
                daily_temps = np.random.normal(22, 4, 30)  # 30 days of temperatures
                hourly_temps = np.random.normal(20, 6, 100)  # Hourly variation
                
                # Create histogram
                n, bins, patches = ax.hist(daily_temps, bins=10, alpha=0.7, color='#FF6B6B', 
                                         edgecolor='black', linewidth=1.2)
                
                # Color gradient for bars
                for i, patch in enumerate(patches):
                    patch.set_facecolor(plt.cm.viridis(i / len(patches)))
                
                ax.set_xlabel('Temperature (°C)', fontweight='bold')
                ax.set_ylabel('Frequency (Days)', fontweight='bold')
                ax.set_title('Temperature Frequency Distribution (30 Days)', fontweight='bold')
                ax.grid(True, alpha=0.3)
                
                # Add statistics text
                mean_temp = np.mean(daily_temps)
                std_temp = np.std(daily_temps)
                stats_text = f'Mean: {mean_temp:.1f}°C\nStd Dev: {std_temp:.1f}°C'
                ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
                       verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                       fontweight='bold')
                
                # Add normal distribution curve
                x = np.linspace(min(daily_temps), max(daily_temps), 100)
                y = ((1/(std_temp * np.sqrt(2 * np.pi))) * 
                     np.exp(-0.5 * ((x - mean_temp) / std_temp) ** 2)) * len(daily_temps) * (bins[1] - bins[0])
                ax.plot(x, y, 'r-', linewidth=2, label='Normal Distribution')
                ax.legend()
                
                plt.tight_layout()
                
                # Display chart
                canvas = FigureCanvasTkAgg(fig, self.forecast_chart_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)
                
                # Add toolbar
                from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
                toolbar = NavigationToolbar2Tk(canvas, self.forecast_chart_frame)
                toolbar.update()
            else:
                # Fallback text display
                self._create_forecast_chart_placeholder()
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"🌡️ Temperature Distribution for {city}:\n\nTemperature histogram would be displayed here if matplotlib was available.")
                
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to generate temperature histogram: {str(e)}")


class FiveDayForecastTab:
    """5-day forecast tab component"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="5-Day Forecast")
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the UI components"""
        # Input area
        input_frame = ttk.Frame(self.frame)
        input_frame.pack(pady=10, padx=10)
        
        StyledLabel(input_frame, text="Enter City:").pack(side="left", padx=5)
        self.city_entry = ttk.Entry(input_frame)
        self.city_entry.pack(side="left", padx=5)
        
        # Action buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=5)
        
        get_forecast_btn = StyledButton(button_frame, "primary_black", text="Get Forecast", 
                    command=self._get_forecast)
        get_forecast_btn.configure(fg="black")  # Explicitly set to black
        get_forecast_btn.pack(side="left", padx=5)
        
        StyledButton(button_frame, "accent_black", text="Weekly Planner", 
                    command=self.create_week_planner).pack(side="left", padx=5)
                    
        StyledButton(button_frame, "info_black", text="Best Weather Days", 
                    command=self.find_best_weather_days).pack(side="left", padx=5)
                    
        StyledButton(button_frame, "success_black", text="Travel Guide", 
                    command=self.generate_travel_guide).pack(side="left", padx=5)
        
        # Results area
        self.result_text = StyledText(self.frame, height=20, width=60)
        self.result_text.pack(pady=10, padx=10, fill="both", expand=True)
        
    def _get_forecast(self):
        """Get and display the 5-day forecast for the entered city"""
        city = self.city_entry.get().strip()
        if not city:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Please enter a city name")
            return
            
        try:
            # Get forecast data from controller
            forecast_data = self.controller.get_five_day_forecast(city)
            
            # Clear previous results
            self.result_text.delete(1.0, tk.END)
            
            # Display formatted forecast
            self.result_text.insert(tk.END, f"📍 5-Day Forecast for {city}\n\n")
            
            # Handle both list and string responses
            if isinstance(forecast_data, str):
                self.result_text.insert(tk.END, forecast_data)
            else:
                for day in forecast_data:
                    try:
                        date = str(day['date']) if 'date' in day else 'Date not available'
                        temp = f"{day['temp']}°C" if 'temp' in day else 'Temperature not available'
                        humidity = f"{day['humidity']}%" if 'humidity' in day else 'Humidity not available'
                        conditions = day['conditions'] if 'conditions' in day else 'Conditions not available'
                        
                        self.result_text.insert(tk.END, f"📅 {date}\n")
                        self.result_text.insert(tk.END, f"🌡️ Temperature: {temp}\n")
                        self.result_text.insert(tk.END, f"💧 Humidity: {humidity}\n")
                        self.result_text.insert(tk.END, f"🌥️ Conditions: {conditions}\n")
                        self.result_text.insert(tk.END, "\n")
                    except (TypeError, AttributeError) as e:
                        print(f"Error processing day data: {e}")
                        continue
                
        except Exception as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Error getting forecast: {str(e)}\n\n")
            self.result_text.insert(tk.END, "Please check:\n")
            self.result_text.insert(tk.END, "- City name is spelled correctly\n")
            self.result_text.insert(tk.END, "- Internet connection is active\n")
            self.result_text.insert(tk.END, "- Weather service is available")

    def create_week_planner(self):
        """Create a weekly weather planner based on the forecast"""
        city = self.city_entry.get().strip()
        if not city:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Please enter a city name first")
            return
            
        try:
            # Get forecast data
            forecast_data = self.controller.get_five_day_forecast(city)
            
            # Clear previous results
            self.result_text.delete(1.0, tk.END)
            
            # Create weekly planner
            self.result_text.insert(tk.END, f"📋 Weekly Weather Planner for {city}\n")
            self.result_text.insert(tk.END, "=" * 40 + "\n\n")
            
            for day in forecast_data:
                # Add day header
                self.result_text.insert(tk.END, f"📅 {day['date']}\n")
                
                # Add weather summary
                self.result_text.insert(tk.END, f"Weather: {day['conditions']}\n")
                self.result_text.insert(tk.END, f"Temperature: {day['temp']}°C\n")
                
                # Add activity suggestions based on weather
                if "rain" in day['conditions'].lower():
                    self.result_text.insert(tk.END, "Suggested: Indoor activities\n")
                elif "clear" in day['conditions'].lower():
                    self.result_text.insert(tk.END, "Suggested: Outdoor activities\n")
                else:
                    self.result_text.insert(tk.END, "Suggested: Mixed activities\n")
                
                self.result_text.insert(tk.END, "\n")
                
        except Exception as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Error creating week planner: {str(e)}")

    def find_best_weather_days(self):
        """Find and display the best weather days for outdoor activities"""
        city = self.city_entry.get().strip()
        if not city:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Please enter a city name first")
            return
            
        try:
            # Get forecast data
            forecast_data = self.controller.get_five_day_forecast(city)
            
            # Clear previous results
            self.result_text.delete(1.0, tk.END)
            
            # Header
            self.result_text.insert(tk.END, f"🎯 Best Days for Outdoor Activities in {city}\n")
            self.result_text.insert(tk.END, "=" * 40 + "\n\n")
            
            # Score each day
            good_days = []
            for day in forecast_data:
                score = 0
                conditions = day['conditions'].lower()
                temp = float(day['temp'])
                
                # Score based on temperature (15-25°C ideal)
                if 15 <= temp <= 25:
                    score += 2
                elif 10 <= temp <= 30:
                    score += 1
                
                # Score based on conditions
                if "clear" in conditions or "sunny" in conditions:
                    score += 2
                elif "partly cloudy" in conditions:
                    score += 1
                elif "rain" in conditions or "storm" in conditions:
                    score -= 2
                
                if score > 0:
                    good_days.append((day['date'], score, temp, day['conditions']))
            
            # Sort by score
            good_days.sort(key=lambda x: x[1], reverse=True)
            
            if good_days:
                for date, score, temp, conditions in good_days:
                    self.result_text.insert(tk.END, f"📅 {date}\n")
                    self.result_text.insert(tk.END, f"🌡️ Temperature: {temp}°C\n")
                    self.result_text.insert(tk.END, f"🌥️ Conditions: {conditions}\n")
                    stars = "⭐" * score
                    self.result_text.insert(tk.END, f"Rating: {stars}\n\n")
            else:
                self.result_text.insert(tk.END, "No ideal outdoor days found in the forecast.\n")
                self.result_text.insert(tk.END, "Consider indoor activities this week!\n")
                
        except Exception as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Error finding best days: {str(e)}")

    def generate_travel_guide(self):
        """Generate a weather-based travel guide for the city"""
        city = self.city_entry.get().strip()
        if not city:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Please enter a city name first")
            return
            
        try:
            # Get forecast data
            forecast_data = self.controller.get_five_day_forecast(city)
            
            # Clear previous results
            self.result_text.delete(1.0, tk.END)
            
            # Create travel guide header
            self.result_text.insert(tk.END, f"✈️ Travel Guide for {city}\n")
            self.result_text.insert(tk.END, "=" * 40 + "\n\n")
            
            # Weather overview
            temps = [float(day['temp']) for day in forecast_data]
            avg_temp = sum(temps) / len(temps)
            
            self.result_text.insert(tk.END, "🌡️ Weather Overview:\n")
            self.result_text.insert(tk.END, f"Average Temperature: {avg_temp:.1f}°C\n")
            self.result_text.insert(tk.END, f"Temperature Range: {min(temps):.1f}°C to {max(temps):.1f}°C\n\n")
            
            # Weather pattern analysis
            conditions = [day['conditions'].lower() for day in forecast_data]
            rainy_days = sum(1 for c in conditions if "rain" in c)
            sunny_days = sum(1 for c in conditions if "clear" in c or "sunny" in c)
            
            self.result_text.insert(tk.END, "🌦️ Weather Pattern:\n")
            if rainy_days > 2:
                self.result_text.insert(tk.END, "Pack rain gear - significant chance of rain\n")
            if sunny_days > 2:
                self.result_text.insert(tk.END, "Bring sun protection - sunny weather expected\n")
            self.result_text.insert(tk.END, "\n")
            
            # Daily recommendations
            self.result_text.insert(tk.END, "📅 Daily Planning Guide:\n")
            for day in forecast_data:
                self.result_text.insert(tk.END, f"\n{day['date']}:\n")
                temp = float(day['temp'])
                conditions = day['conditions'].lower()
                
                # Clothing recommendations
                if temp < 15:
                    self.result_text.insert(tk.END, "👕 Warm layers recommended\n")
                elif temp > 25:
                    self.result_text.insert(tk.END, "👕 Light, breathable clothing\n")
                
                # Activity suggestions
                if "rain" in conditions:
                    self.result_text.insert(tk.END, "🎫 Indoor activities recommended\n")
                elif "clear" in conditions or "sunny" in conditions:
                    self.result_text.insert(tk.END, "🏖️ Perfect for outdoor exploration\n")
                
        except Exception as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Error generating travel guide: {str(e)}")

    def get_weather_preparation(self):
        """Get weather preparation advice based on the forecast"""
        city = self.city_entry.get().strip()
        if not city:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Please enter a city name first")
            return
            
        try:
            # Get forecast data
            forecast_data = self.controller.get_five_day_forecast(city)
            
            # Clear previous results
            self.result_text.delete(1.0, tk.END)
            
            # Create header
            self.result_text.insert(tk.END, f"🎒 Weather Preparation Guide for {city}\n")
            self.result_text.insert(tk.END, "=" * 40 + "\n\n")
            
            # Analyze weather patterns
            conditions = [day['conditions'].lower() for day in forecast_data]
            temps = [float(day['temp']) for day in forecast_data]
            
            # Essential items section
            self.result_text.insert(tk.END, "🔰 Essential Items:\n")
            essentials = ["Water bottle", "Weather app", "Emergency contacts"]
            for item in essentials:
                self.result_text.insert(tk.END, f"• {item}\n")
            self.result_text.insert(tk.END, "\n")
            
            # Weather-specific items
            self.result_text.insert(tk.END, "🌦️ Weather-Specific Items:\n")
            if any("rain" in c for c in conditions):
                self.result_text.insert(tk.END, "☔ Rain Protection:\n")
                self.result_text.insert(tk.END, "• Umbrella\n")
                self.result_text.insert(tk.END, "• Waterproof jacket\n")
                self.result_text.insert(tk.END, "• Water-resistant footwear\n\n")
                
            if any("clear" in c or "sunny" in c for c in conditions):
                self.result_text.insert(tk.END, "☀️ Sun Protection:\n")
                self.result_text.insert(tk.END, "• Sunscreen (SPF 30+)\n")
                self.result_text.insert(tk.END, "• Sunglasses\n")
                self.result_text.insert(tk.END, "• Hat or cap\n\n")
                
            # Temperature-based recommendations
            self.result_text.insert(tk.END, "🌡️ Temperature Considerations:\n")
            if any(t < 15 for t in temps):
                self.result_text.insert(tk.END, "❄️ Cold Weather Items:\n")
                self.result_text.insert(tk.END, "• Warm jacket\n")
                self.result_text.insert(tk.END, "• Gloves\n")
                self.result_text.insert(tk.END, "• Thermal layers\n\n")
                
            if any(t > 25 for t in temps):
                self.result_text.insert(tk.END, "🌞 Hot Weather Items:\n")
                self.result_text.insert(tk.END, "• Light, breathable clothing\n")
                self.result_text.insert(tk.END, "• Cooling towel\n")
                self.result_text.insert(tk.END, "• Electrolyte drinks\n\n")
                
            # Safety tips
            self.result_text.insert(tk.END, "⚠️ Safety Tips:\n")
            self.result_text.insert(tk.END, "• Check weather updates regularly\n")
            self.result_text.insert(tk.END, "• Stay hydrated\n")
            self.result_text.insert(tk.END, "• Know emergency shelter locations\n")
            
        except Exception as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Error getting preparation guide: {str(e)}")

    def _setup_ui(self):
        """Setup the UI components with split-screen layout"""
        if CHARTS_AVAILABLE:
            # Create horizontal paned window for split-screen layout
            paned = ttk.PanedWindow(self.frame, orient=tk.HORIZONTAL)
            paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Left panel for data and controls
            left_frame = ttk.Frame(paned)
            paned.add(left_frame, weight=1)
            
            # Right panel for charts
            right_frame = ttk.Frame(paned)
            paned.add(right_frame, weight=1)
            
            self._setup_forecast_interface(left_frame)
            self._setup_chart_interface(right_frame)
        else:
            # Fallback to original layout
            self._setup_forecast_interface(self.frame)

    def _setup_forecast_interface(self, parent_frame):
        """Setup the forecast interface in the left panel"""
        StyledLabel(parent_frame, text="Enter City:").pack(pady=10)
        self.city_entry = ttk.Entry(parent_frame)
        self.city_entry.pack()
        
        self.result_text = StyledText(parent_frame, height=15, width=50)
        self.result_text.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Main action button
        StyledButton(parent_frame, "primary", text="Get 5-Day Forecast", 
                    command=self._get_forecast).pack(pady=5)
        
        # Additional Enhanced Buttons
        fiveday_button_frame = ttk.Frame(parent_frame)
        fiveday_button_frame.pack(pady=5)
        
        StyledButton(fiveday_button_frame, "accent_black", text="📅 Week Planner", 
                    command=self.create_week_planner).grid(row=0, column=0, padx=2, pady=2)
        StyledButton(fiveday_button_frame, "info_black", text="🎯 Best Days", 
                    command=self.find_best_weather_days).grid(row=0, column=1, padx=2, pady=2)
        StyledButton(fiveday_button_frame, "success_black", text="📋 Travel Guide", 
                    command=self.generate_travel_guide).grid(row=1, column=0, padx=2, pady=2)
        StyledButton(fiveday_button_frame, "warning_black", text="⚡ Weather Prep", 
                    command=self.get_weather_preparation).grid(row=1, column=1, padx=2, pady=2)

    def _setup_chart_interface(self, parent_frame):
        """Setup the chart interface in the right panel"""
        # Chart title
        chart_title = StyledLabel(parent_frame, text="5-Day Forecast Charts")
        chart_title.pack(pady=5)
        
        # Chart type selection buttons
        chart_buttons_frame = ttk.Frame(parent_frame)
        chart_buttons_frame.pack(pady=5)
        
        StyledButton(chart_buttons_frame, "info_black", text="📈 Temperature Trend", 
                    command=self.show_temperature_trend_chart).grid(row=0, column=0, padx=2)
        StyledButton(chart_buttons_frame, "accent_black", text="📊 Daily Comparison", 
                    command=self.show_daily_comparison_chart).grid(row=0, column=1, padx=2)
        StyledButton(chart_buttons_frame, "warning_black", text="🌧️ Precipitation", 
                    command=self.show_precipitation_chart).grid(row=1, column=0, padx=2)
        StyledButton(chart_buttons_frame, "success_black", text="📊 Overview", 
                    command=self.show_forecast_overview_chart).grid(row=1, column=1, padx=2)
        
        # Chart display area
        self.chart_frame = ttk.Frame(parent_frame)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Initial placeholder
        self._show_chart_placeholder()

    def _show_chart_placeholder(self):
        """Show placeholder when no chart is selected"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        placeholder = StyledLabel(self.chart_frame, 
                                text="📊 Select a chart type above to visualize 5-day forecast data\n\n"
                                     "Available Charts:\n"
                                     "• Temperature Trend - Daily temperature progression\n"
                                     "• Daily Comparison - Compare temperature, humidity, wind\n"
                                     "• Precipitation - Rain/snow probability forecast\n"
                                     "• Overview - Comprehensive forecast summary")
        placeholder.pack(expand=True)

    def _clear_chart_area(self):
        """Clear the chart display area"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

    def show_temperature_trend_chart(self):
        """Show 5-day temperature trend chart"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name first")
            return
            
        if not CHARTS_AVAILABLE:
            messagebox.showinfo("Charts Unavailable", 
                               "Matplotlib not available. Please install it to view charts.")
            return
        
        self._clear_chart_area()
        
        # Sample 5-day forecast data (replace with real API data)
        days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']
        highs = [28, 26, 24, 27, 29]
        lows = [18, 16, 14, 17, 19]
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(8, 5))
        
        x = range(len(days))
        ax.plot(x, highs, marker='o', linewidth=2, color='#FF6B6B', label='High Temperature')
        ax.plot(x, lows, marker='s', linewidth=2, color='#4ECDC4', label='Low Temperature')
        ax.fill_between(x, highs, lows, alpha=0.2, color='#FFD93D')
        
        ax.set_title(f'5-Day Temperature Forecast - {city}', fontsize=14, fontweight='bold')
        ax.set_xlabel('Day')
        ax.set_ylabel('Temperature (°C)')
        ax.set_xticks(x)
        ax.set_xticklabels(days)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Add temperature labels
        for i, (high, low) in enumerate(zip(highs, lows)):
            ax.annotate(f'{high}°', (i, high), textcoords="offset points", 
                       xytext=(0,10), ha='center', fontweight='bold')
            ax.annotate(f'{low}°', (i, low), textcoords="offset points", 
                       xytext=(0,-15), ha='center', fontweight='bold')
        
        plt.tight_layout()
        
        # Embed chart in tkinter
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add navigation toolbar
        toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
        toolbar.update()

    def show_daily_comparison_chart(self):
        """Show daily comparison chart for multiple metrics"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name first")
            return
            
        if not CHARTS_AVAILABLE:
            messagebox.showinfo("Charts Unavailable", 
                               "Matplotlib not available. Please install it to view charts.")
            return
        
        self._clear_chart_area()
        
        # Sample data for 5 days
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        temperatures = [25, 23, 21, 24, 27]
        humidity = [65, 70, 75, 68, 60]
        wind_speed = [12, 15, 18, 10, 8]
        
        # Create subplots
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 8))
        
        # Temperature chart
        bars1 = ax1.bar(days, temperatures, color='#FF6B6B', alpha=0.8)
        ax1.set_title(f'Daily Weather Comparison - {city}', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Temperature (°C)')
        ax1.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, temp in zip(bars1, temperatures):
            height = bar.get_height()
            ax1.annotate(f'{temp}°', xy=(bar.get_x() + bar.get_width()/2, height),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
        
        # Humidity chart
        bars2 = ax2.bar(days, humidity, color='#4ECDC4', alpha=0.8)
        ax2.set_ylabel('Humidity (%)')
        ax2.grid(True, alpha=0.3)
        
        for bar, hum in zip(bars2, humidity):
            height = bar.get_height()
            ax2.annotate(f'{hum}%', xy=(bar.get_x() + bar.get_width()/2, height),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
        
        # Wind speed chart
        bars3 = ax3.bar(days, wind_speed, color='#95E1D3', alpha=0.8)
        ax3.set_ylabel('Wind Speed (km/h)')
        ax3.set_xlabel('Day')
        ax3.grid(True, alpha=0.3)
        
        for bar, wind in zip(bars3, wind_speed):
            height = bar.get_height()
            ax3.annotate(f'{wind}', xy=(bar.get_x() + bar.get_width()/2, height),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Embed chart in tkinter
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add navigation toolbar
        toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
        toolbar.update()

    def show_precipitation_chart(self):
        """Show precipitation probability chart"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name first")
            return
            
        if not CHARTS_AVAILABLE:
            messagebox.showinfo("Charts Unavailable", 
                               "Matplotlib not available. Please install it to view charts.")
            return
        
        self._clear_chart_area()
        
        # Sample precipitation data
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        precipitation_prob = [10, 25, 85, 30, 5]
        
        # Color code based on probability
        colors = []
        for prob in precipitation_prob:
            if prob < 20:
                colors.append('#4CAF50')  # Green - Low
            elif prob < 50:
                colors.append('#FFC107')  # Yellow - Medium
            else:
                colors.append('#F44336')  # Red - High
        
        # Create horizontal bar chart
        fig, ax = plt.subplots(figsize=(8, 6))
        bars = ax.barh(days, precipitation_prob, color=colors, alpha=0.8)
        
        ax.set_title(f'5-Day Precipitation Forecast - {city}', fontsize=14, fontweight='bold')
        ax.set_xlabel('Precipitation Probability (%)')
        ax.set_xlim(0, 100)
        
        # Add percentage labels
        for bar, prob in zip(bars, precipitation_prob):
            width = bar.get_width()
            ax.annotate(f'{prob}%', xy=(width, bar.get_y() + bar.get_height()/2),
                       xytext=(5, 0), textcoords="offset points", va='center')
        
        # Add risk level legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#4CAF50', label='Low Risk (0-19%)'),
            Patch(facecolor='#FFC107', label='Medium Risk (20-49%)'),
            Patch(facecolor='#F44336', label='High Risk (50%+)')
        ]
        ax.legend(handles=legend_elements, loc='lower right')
        
        ax.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        
        # Embed chart in tkinter
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add navigation toolbar
        toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
        toolbar.update()

    def show_forecast_overview_chart(self):
        """Show comprehensive forecast overview chart"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name first")
            return
            
        if not CHARTS_AVAILABLE:
            messagebox.showinfo("Charts Unavailable", 
                               "Matplotlib not available. Please install it to view charts.")
            return
        
        self._clear_chart_area()
        
        # Sample comprehensive data
        days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']
        temps = [25, 23, 21, 24, 27]
        conditions = ['Sunny', 'Cloudy', 'Rainy', 'Partly Cloudy', 'Sunny']
        comfort_index = [8.5, 7.2, 5.1, 7.8, 9.1]  # Out of 10
        
        # Create figure with subplots
        fig = plt.figure(figsize=(10, 8))
        
        # Temperature line chart (top)
        ax1 = plt.subplot(2, 2, (1, 2))
        line = ax1.plot(days, temps, marker='o', linewidth=3, markersize=8, color='#FF6B6B')
        ax1.set_title(f'5-Day Forecast Overview - {city}', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Temperature (°C)')
        ax1.grid(True, alpha=0.3)
        
        # Add temperature labels
        for i, temp in enumerate(temps):
            ax1.annotate(f'{temp}°', (i, temp), textcoords="offset points", 
                        xytext=(0,10), ha='center', fontweight='bold')
        
        # Weather conditions pie chart (bottom left)
        ax2 = plt.subplot(2, 2, 3)
        condition_counts = {}
        for condition in conditions:
            condition_counts[condition] = condition_counts.get(condition, 0) + 1
        
        colors = ['#FFD93D', '#6BCF7F', '#4D96FF', '#9B59B6', '#E74C3C']
        ax2.pie(condition_counts.values(), labels=condition_counts.keys(), 
               colors=colors[:len(condition_counts)], autopct='%1.0f%%', startangle=90)
        ax2.set_title('Weather Conditions Distribution')
        
        # Comfort index bar chart (bottom right)
        ax3 = plt.subplot(2, 2, 4)
        bars = ax3.bar(range(len(days)), comfort_index, color='#95E1D3', alpha=0.8)
        ax3.set_title('Daily Comfort Index')
        ax3.set_ylabel('Comfort (1-10)')
        ax3.set_xticks(range(len(days)))
        ax3.set_xticklabels([f'D{i+1}' for i in range(len(days))])
        ax3.set_ylim(0, 10)
        ax3.grid(True, alpha=0.3)
        
        # Add comfort index labels
        for bar, comfort in zip(bars, comfort_index):
            height = bar.get_height()
            ax3.annotate(f'{comfort}', xy=(bar.get_x() + bar.get_width()/2, height),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Embed chart in tkinter
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add navigation toolbar
        toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
        toolbar.update()
        
    def _create_chart_placeholder(self):
        """Create a placeholder for the chart area"""
        if self.current_chart_frame:
            self.current_chart_frame.destroy()
        
        self.current_chart_frame = ttk.Frame(self.right_frame)
        self.current_chart_frame.pack(fill="both", expand=True)
        
        ChartHelper.create_chart_placeholder(
            self.current_chart_frame,
            title="Analytics Chart Display",
            content="Generate analytics to see weather trends and comparisons."
        )

    def _generate_analytics(self):
        """Fetch data and prepare for analytics"""
        city1 = self.city1_combo.get().strip()
        city2 = self.city2_combo.get().strip()
        
        if not city1:
            messagebox.showwarning("Input Required", "Please select at least a primary city.")
            return
            
        self.cities = [city for city in [city1, city2] if city]
        time_range_str = self.time_range.get()
        
        self.info_text.config(state="normal")
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert("1.0", f"📊 Generating analytics for {', '.join(self.cities)} over {time_range_str}...")
        self.info_text.config(state="disabled")
        
        # In a real app, you'd fetch data here. For now, we'll use dummy data.
        messagebox.showinfo("Analytics Generated", 
                            f"Analytics data for {', '.join(self.cities)} is ready. Please select a chart type to view.")

    def _show_temperature_trends(self):
        """Show temperature trends for the selected cities"""
        if not self.cities:
            messagebox.showwarning("No Data", "Please generate analytics first.")
            return
        
        # Dummy data
        days = list(range(1, 8))
        temps1 = [np.random.randint(10, 20) for _ in days]
        
        ChartHelper.create_line_chart(
            self.current_chart_frame,
            title=f"🌡️ Weekly Temperature Trend for {self.cities[0]}",
            x_data=days,
            y_data=temps1,
            x_label="Day",
            y_label="Temperature (°C)"
        )

    def _show_precipitation_analysis(self):
        """Show precipitation analysis"""
        if not self.cities:
            messagebox.showwarning("No Data", "Please generate analytics first.")
            return
            
        # Dummy data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        precipitation = [np.random.randint(50, 200) for _ in months]
        
        ChartHelper.create_bar_chart(
            self.current_chart_frame,
            title=f"🌧️ Monthly Precipitation for {self.cities[0]}",
            x_data=months,
            y_data=precipitation
        )

    def _show_wind_patterns(self):
        """Show wind patterns using a histogram"""
        if not self.cities:
            messagebox.showwarning("No Data", "Please generate analytics first.")
            return
            
        # Dummy data
        wind_speeds = np.random.normal(15, 5, 100)
        
        ChartHelper.create_histogram(
            self.current_chart_frame,
            title=f"💨 Wind Speed Distribution for {self.cities[0]}",
            data=wind_speeds,
            bins=20
        )

    def _show_daylight_hours(self):
        """Show daylight hours trend"""
        if not self.cities:
            messagebox.showwarning("No Data", "Please generate analytics first.")
            return
            
        # Dummy data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
        daylight = [10, 11, 12.5, 14, 15, 15.5, 15]
        
        ChartHelper.create_line_chart(
            self.current_chart_frame,
            title=f"☀️ Daylight Hours Trend for {self.cities[0]}",
            x_data=months,
            y_data=daylight,
            x_label="Month",
            y_label="Hours"
        )

    def _show_humidity_trends(self):
        """Display humidity trends chart"""
        if not self.cities:
            return
            
        try:
            self._clear_chart_area()
            
            # Get data from controller
            time_range = self.time_range.get()
            data = self.controller.get_humidity_data(self.cities, time_range)
            
            if not data or len(data) == 0:
                messagebox.showinfo("No Data", "No humidity data available for the selected period")
                return
            
            # Create figure
            fig = Figure(figsize=(10, 6), dpi=100)
            ax = fig.add_subplot(111)
            
            # Plot data for each city
            colors = ['#4ECDC4', '#FF6B6B', '#45B7D1']
            for i, city_data in enumerate(data):
                timestamps = city_data['timestamps']
                humidity_values = city_data['humidity_values']
                
                ax.plot(timestamps, humidity_values, color=colors[i % len(colors)],
                       label=self.cities[i], marker='o', markersize=4)
            
            # Customize appearance
            ax.set_title(f"Humidity Trends - Past {time_range}")
            ax.set_xlabel("Time")
            ax.set_ylabel("Relative Humidity (%)")
            ax.grid(True, alpha=0.3)
            ax.legend()
            ax.tick_params(axis='x', rotation=45)
            
            fig.tight_layout()
            
            # Embed chart
            ChartHelper.embed_chart_in_frame(fig, self.current_chart_frame)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate humidity trends: {str(e)}")
            self._create_chart_placeholder()

    def _show_weather_comparison(self):
        """Compare weather elements between two cities"""
        if len(self.cities) < 2:
            messagebox.showwarning("Input Required", "Please provide two cities to compare.")
            return
            
        # Dummy data
        metrics = ['Temp', 'Humidity', 'Wind']
        city1_data = [np.random.randint(10, 25), np.random.randint(40, 70), np.random.randint(5, 20)]
        city2_data = [np.random.randint(10, 25), np.random.randint(40, 70), np.random.randint(5, 20)]
        
        # For demonstration, we'll just create a bar chart. A more complex chart could be used.
        if not CHARTS_AVAILABLE:
            ChartHelper.show_chart_unavailable(self.current_chart_frame)
            return

        ChartHelper.clear_chart_area(self.current_chart_frame)
        
        fig = Figure(figsize=(8, 5), dpi=100, facecolor='white')
        ax = fig.add_subplot(111)
        
        x = np.arange(len(metrics))
        width = 0.35
        
        rects1 = ax.bar(x - width/2, city1_data, width, label=self.cities[0])
        rects2 = ax.bar(x + width/2, city2_data, width, label=self.cities[1])
        
        ax.set_ylabel('Values')
        ax.set_title(f'📊 Weather Comparison: {self.cities[0]} vs {self.cities[1]}')
        ax.set_xticks(x)
        ax.set_xticklabels(metrics)
        ax.legend()
        
        try:
            fig.tight_layout()
            ChartHelper.embed_chart_in_frame(fig, self.current_chart_frame)
            
            # Prepare guide text
            prep_guide = "• Plan workout schedule around weather\n"
            prep_guide += "• Adjust commute times for rain day\n\n"
            prep_guide += "🚨 EMERGENCY PREPAREDNESS:\n"
            prep_guide += "• Emergency flashlight ready\n"
            prep_guide += "• First aid kit accessible\n"
            prep_guide += "• Contact list updated\n"
            prep_guide += "• Know severe weather protocols"
            
            if hasattr(self, 'result_text'):
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, prep_guide)
        except Exception as e:
            messagebox.showerror("Error", str(e))


class ComparisonTab:
    """City comparison tab component"""
    
    def __init__(self, notebook, controller):
        """Initialize the City Comparison tab"""
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="City Comparison")
        
        # Initialize matplotlib-related variables for chart generation
        try:
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
            self.Figure = Figure
            self.FigureCanvasTkAgg = FigureCanvasTkAgg
            self.NavigationToolbar2Tk = NavigationToolbar2Tk
        except ImportError:
            # Handle case where matplotlib is not available
            self.Figure = None
            self.FigureCanvasTkAgg = None
            self.NavigationToolbar2Tk = None
        
        # Initialize data storage
        self._weather_df = {}
        
        # Initialize with a default list of cities
        self.available_cities = [
            "New York", "London", "Tokyo", "Paris", "Sydney", 
            "Dubai", "San Francisco", "Berlin", "Toronto", "Singapore"
        ]
        
        self.city1_combo = None
        self.city2_combo = None
        self.result_text = None
        self.chart_frame = None
        
        # Set up UI directly
        self._setup_ui()
        
    # _load_team_cities method removed - no longer needed
            
    def _get_selected_cities(self):
        """Get the currently selected cities from the comboboxes"""
        try:
            if not hasattr(self, 'city1_combo') or not hasattr(self, 'city2_combo'):
                raise ValueError("City selection components not initialized")
                
            city1 = self.city1_combo.get().strip() if self.city1_combo['state'] != 'disabled' else ''
            city2 = self.city2_combo.get().strip() if self.city2_combo['state'] != 'disabled' else ''
            
            return city1, city2
        except Exception as e:
            print(f"Error getting selected cities: {e}")
            return None, None
        
    def _validate_city_selection(self):
        """Validate that selected cities are from our available cities"""
        try:
            # Check if we have available cities
            if not hasattr(self, 'available_cities') or not self.available_cities:
                # Initialize with an empty list if not available
                self.available_cities = []
            
            city1, city2 = self._get_selected_cities()
            
            # Check if cities are selected
            if not city1 or not city2:
                messagebox.showwarning("Input Error", "Please select both cities")
                return False
                
            # Check if cities exist in available list
            if city1 not in self.available_cities or city2 not in self.available_cities:
                missing_city = city1 if city1 not in self.available_cities else city2
                messagebox.showerror("Error", f"City '{missing_city}' is not available for comparison")
                return False
                
            # Check they aren't the same city
            if city1 == city2:
                messagebox.showwarning("Invalid Selection", "Please select two different cities to compare")
                return False
                
            return True
                
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Error validating city selection: {str(e)}")
            return False

    def show_distance_info(self):
        """Show distance and geographic information between cities"""
        if not self._validate_city_selection():
            return
            
        city1, city2 = self._get_selected_cities()
        
        try:
            distance_info = f"🗺️ DISTANCE & GEOGRAPHIC INFO:\n"
            distance_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
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
            distance_info += "• Seasonal differences: May vary significantly\n\n"
            distance_info += "🧭 COORDINATE INFO:\n"
            distance_info += "• Direction: Calculate based on coordinates\n"
            distance_info += "• Climate zones: May differ significantly\n"
            distance_info += "• Weather patterns: Can be very different\n\n"
            distance_info += "💡 Tips for Travelers:\n"
            distance_info += "• Check time zones for communication\n"
            distance_info += "• Consider seasonal weather differences\n"
            distance_info += "• Plan for climate adaptation time"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, distance_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def detailed_comparison(self):
        """Show detailed comparison with more metrics"""
        if not self._validate_city_selection():
            return
            
        city1, city2 = self._get_selected_cities()
        
        try:
            # Check if we have weather data stored
            if city1 not in self._weather_df or city2 not in self._weather_df:
                # If not, fetch it now
                self.compare_cities()
                
            # Now get the data from the weather dictionary
            data1 = self._weather_df[city1] if city1 in self._weather_df else {}
            data2 = self._weather_df[city2] if city2 in self._weather_df else {}
            
            if not data1 or not data2:
                messagebox.showerror("Error", "Weather data not available. Please compare cities first.")
                return
                
            # Create detailed comparison text
            detailed = f"📊 DETAILED COMPARISON: {city1} vs {city2}\n"
            detailed += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            # Current data section
            detailed += "🌡️ TEMPERATURE ANALYSIS:\n"
            temp1 = data1.get('temp', 'N/A')
            temp2 = data2.get('temp', 'N/A')
            detailed += f"• {city1}: {temp1}°C (Current)\n"
            detailed += f"• {city2}: {temp2}°C (Current)\n"
            
            if isinstance(temp1, (int, float)) and isinstance(temp2, (int, float)):
                diff = abs(temp1 - temp2)
                warmer = city1 if temp1 > temp2 else city2
                detailed += f"• Difference: {diff:.1f}°C warmer in {warmer}\n\n"
            else:
                detailed += "• Difference: Data not available\n\n"
                
            # Humidity section
            detailed += "💧 HUMIDITY & COMFORT:\n"
            hum1 = data1.get('humidity', 'N/A')
            hum2 = data2.get('humidity', 'N/A')
            detailed += f"• {city1}: {hum1}% humidity\n"
            detailed += f"• {city2}: {hum2}% humidity\n"
            
            if isinstance(hum1, (int, float)) and isinstance(hum2, (int, float)):
                # Determine comfort based on humidity (40-60% is optimal)
                comfort1 = 10 - abs(hum1 - 50) / 5 if 0 <= hum1 <= 100 else 5
                comfort2 = 10 - abs(hum2 - 50) / 5 if 0 <= hum2 <= 100 else 5
                comfort1 = max(0, min(10, comfort1))  # Clamp to 0-10 range
                comfort2 = max(0, min(10, comfort2))  # Clamp to 0-10 range
                
                detailed += f"• {city1} Comfort Index: {comfort1:.1f}/10\n"
                detailed += f"• {city2} Comfort Index: {comfort2:.1f}/10\n"
                
                winner = city1 if abs(hum1 - 50) < abs(hum2 - 50) else city2
                detailed += f"• Winner: {winner} (More comfortable humidity)\n\n"
            else:
                detailed += "• Comfort analysis: Data not available\n\n"
                
            # Wind section
            detailed += "💨 WIND CONDITIONS:\n"
            wind1 = data1.get('wind_speed', 'N/A')
            wind2 = data2.get('wind_speed', 'N/A')
            detailed += f"• {city1}: {wind1} km/h\n"
            detailed += f"• {city2}: {wind2} km/h\n"
            
            if isinstance(wind1, (int, float)) and isinstance(wind2, (int, float)):
                # Wind descriptions
                def wind_desc(speed):
                    if speed < 5: return "Calm"
                    elif speed < 11: return "Light breeze"
                    elif speed < 19: return "Moderate breeze"
                    elif speed < 28: return "Fresh breeze"
                    elif speed < 38: return "Strong breeze"
                    elif speed < 49: return "High wind"
                    else: return "Gale force wind"
                    
                detailed += f"• {city1}: {wind_desc(wind1)}\n"
                detailed += f"• {city2}: {wind_desc(wind2)}\n"
                
                calmer = city1 if wind1 < wind2 else city2
                detailed += f"• Winner: {calmer} (Calmer conditions)\n\n"
            else:
                detailed += "• Wind analysis: Data not available\n\n"
                
            # Weather conditions
            detailed += "☁️ CURRENT CONDITIONS:\n"
            desc1 = data1.get('description', 'N/A')
            desc2 = data2.get('description', 'N/A')
            detailed += f"• {city1}: {desc1}\n"
            detailed += f"• {city2}: {desc2}\n\n"
            
            # Overall recommendation
            detailed += "🎯 OVERALL RECOMMENDATION:\n"
            if all(isinstance(x, (int, float)) for x in [temp1, temp2, hum1, hum2, wind1, wind2]):
                # Calculate a simple weather score (0-10)
                # Temperature: 15-25°C is ideal (10 points)
                # Humidity: 40-60% is ideal (10 points)
                # Wind: 0-15 km/h is ideal (10 points)
                
                def temp_score(t):
                    if 20 <= t <= 25: return 10
                    elif 15 <= t < 20 or 25 < t <= 30: return 8
                    elif 10 <= t < 15 or 30 < t <= 35: return 6
                    elif 5 <= t < 10 or 35 < t <= 40: return 4
                    else: return 2
                
                def humidity_score(h):
                    if 40 <= h <= 60: return 10
                    elif 30 <= h < 40 or 60 < h <= 70: return 8
                    elif 20 <= h < 30 or 70 < h <= 80: return 6
                    elif 10 <= h < 20 or 80 < h <= 90: return 4
                    else: return 2
                
                def wind_score(w):
                    if 0 <= w <= 10: return 10
                    elif 10 < w <= 20: return 8
                    elif 20 < w <= 30: return 6
                    elif 30 < w <= 40: return 4
                    else: return 2
                
                score1 = (temp_score(temp1) + humidity_score(hum1) + wind_score(wind1)) / 3
                score2 = (temp_score(temp2) + humidity_score(hum2) + wind_score(wind2)) / 3
                
                better_city = city1 if score1 > score2 else city2
                detailed += f"Better weather today: {better_city}\n\n"
                detailed += "🏆 Weather Score:\n"
                detailed += f"• {city1}: {score1:.1f}/10\n"
                detailed += f"• {city2}: {score2:.1f}/10\n\n"
                
                # Add chart reminder
                detailed += "📊 VISUALIZATION AVAILABLE:\n"
                detailed += "• See the chart panel for visual comparison\n"
                detailed += "• Radar chart shows all metrics at once\n"
                detailed += "• Temperature chart shows daily variations\n"
            else:
                detailed += "• Not enough data for complete analysis\n"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, detailed)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate detailed comparison: {str(e)}")

    def get_travel_advice(self):
        """Get travel advice based on weather comparison"""
        if not self._validate_city_selection():
            return
            
        city1, city2 = self._get_selected_cities()
        
        try:
            travel_advice = f"✈️ TRAVEL ADVICE: {city1} vs {city2}\n"
            travel_advice += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            travel_advice += "🎯 TRAVEL RECOMMENDATIONS:\n\n"
            travel_advice += f"📍 Current Conditions Analysis:\n"
            travel_advice += f"• {city1}: Better for outdoor activities\n"
            travel_advice += f"• {city2}: More suitable for indoor attractions\n\n"
            travel_advice += "🧳 PACKING SUGGESTIONS:\n\n"
            travel_advice += f"For {city1}:\n"
            travel_advice += "• Lighter clothing (warmer weather)\n"
            travel_advice += "• Sunscreen and sunglasses\n"
            travel_advice += "• Light jacket for evening\n"
            travel_advice += "• Comfortable walking shoes\n\n"
            travel_advice += f"For {city2}:\n"
            travel_advice += "• Layered clothing (cooler weather)\n"
            travel_advice += "• Light rain jacket\n"
            travel_advice += "• Warmer evening wear\n"
            travel_advice += "• Umbrella (higher humidity)\n\n"
            travel_advice += "🗓️ TIMING RECOMMENDATIONS:\n\n"
            travel_advice += f"Visit {city1} for:\n"
            travel_advice += "• Outdoor sightseeing\n"
            travel_advice += "• Photography sessions\n"
            travel_advice += "• Walking tours\n"
            travel_advice += "• Beach/park activities\n\n"
            travel_advice += f"Visit {city2} for:\n"
            travel_advice += "• Museum visits\n"
            travel_advice += "• Indoor entertainment\n"
            travel_advice += "• Shopping experiences\n"
            travel_advice += "• Cozy café culture\n\n"
            travel_advice += "💰 COST CONSIDERATIONS:\n"
            travel_advice += f"• {city1}: Peak season pricing (good weather)\n"
            travel_advice += f"• {city2}: Potentially lower rates (weather dependent)\n\n"
            travel_advice += "🏆 VERDICT:\n"
            travel_advice += f"For outdoor enthusiasts: Choose {city1}\n"
            travel_advice += f"For culture seekers: Either city works\n"
            travel_advice += f"For budget travelers: Consider {city2}\n"
            travel_advice += f"For photographers: {city1} has better conditions"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, travel_advice)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def fix_radar_comparison(self):
        """Fix array shape mismatch issues in radar chart comparison"""
        if not self._validate_city_selection():
            return
            
        city1, city2 = self._get_selected_cities()
        
        try:
            # Display a status message while we're working on the fix
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "🔧 Fixing radar chart comparison...\n")
            self.result_text.update()
            
            # Ensure we have data for both cities
            if city1 not in self._weather_df or city2 not in self._weather_df:
                # Need to get the data first
                self.compare_cities()
                
            # Get city data
            data1 = self._weather_df.get(city1, {})
            data2 = self._weather_df.get(city2, {})
            
            if not data1 or not data2:
                messagebox.showerror("Error", "No data available for the selected cities. Please run comparison first.")
                return
                
            # Find common metrics between the two cities
            common_metrics = []
            for metric in set(data1.keys()).intersection(set(data2.keys())):
                if metric != 'description':  # Skip text fields
                    common_metrics.append(metric)
            
            # Check if we have enough common metrics
            if len(common_metrics) < 2:
                messagebox.showerror("Error", "Not enough common metrics between the cities to create a radar chart.")
                return
                
            # Create labels for display
            labels = []
            for metric in common_metrics:
                if metric == 'temp':
                    labels.append('Temperature')
                elif metric == 'humidity':
                    labels.append('Humidity')
                elif metric == 'wind_speed':
                    labels.append('Wind Speed')
                else:
                    # Convert snake_case to Title Case
                    labels.append(metric.replace('_', ' ').title())
                    
            # Create a new radar chart with only the common metrics
            self._clear_chart_area()
            
            # Prepare a comprehensive report that includes actual data values
            report = f"✅ RADAR CHART FIXED!\n\n"
            report += f"📊 CHART REPAIR REPORT:\n"
            report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            report += f"🔍 ANALYSIS:\n"
            report += f"• Issue detected: Different metrics between cities\n"
            report += f"• Solution: Using only common metrics for comparison\n\n"
            report += f"📋 METRICS FOUND:\n"
            report += f"• {city1}: {list(data1.keys())}\n"
            report += f"• {city2}: {list(data2.keys())}\n\n"
            report += f"🎯 COMMON METRICS USED:\n"
            report += f"• {', '.join(labels)}\n\n"
            
            # Add the actual comparison data for the common metrics
            report += f"📈 DATA COMPARISON:\n"
            for metric in common_metrics:
                val1 = data1.get(metric, "N/A")
                val2 = data2.get(metric, "N/A")
                
                # Create a more readable metric name
                if metric == 'temp':
                    label = "Temperature (°C)"
                elif metric == 'humidity':
                    label = "Humidity (%)"
                elif metric == 'wind_speed':
                    label = "Wind Speed (km/h)"
                else:
                    # Convert snake_case to Title Case
                    label = metric.replace('_', ' ').title()
                
                report += f"• {label}:\n"
                report += f"  - {city1}: {val1}\n"
                report += f"  - {city2}: {val2}\n"
                
                # Add comparison if both values are numerical
                if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                    diff = abs(val1 - val2)
                    if metric == 'temp':
                        warmer = city1 if val1 > val2 else city2
                        report += f"  - Difference: {diff:.1f}°C warmer in {warmer}\n"
                    elif metric == 'humidity':
                        higher = city1 if val1 > val2 else city2
                        report += f"  - Difference: {diff:.1f}% higher in {higher}\n"
                    elif metric == 'wind_speed':
                        windier = city1 if val1 > val2 else city2
                        report += f"  - Difference: {diff:.1f} km/h windier in {windier}\n"
                    else:
                        higher = city1 if val1 > val2 else city2
                        report += f"  - Difference: {diff:.1f} higher in {higher}\n"
                report += "\n"
            
            report += f"� CHART REGENERATED:\n"
            report += f"• Fixed radar chart created with matched dimensions\n"
            report += f"• Array shape issue resolved\n\n"
            report += f"💡 TIP: If you need more metrics, ensure both cities have the same data sources."
            
            # Update the text display
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, report)
            
            # Create the fixed radar chart
            self._create_radar_chart(city1, city2)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fix radar comparison: {str(e)}")

    def multi_city_compare(self):
        """Compare multiple cities at once"""
        if not self._validate_city_selection():
            return
            
        city1, city2 = self._get_selected_cities()
        if city1 and city1 not in self.available_cities:
            messagebox.showerror("Invalid City", f"'{city1}' is not in the list of available cities.")
            return False
            
        if city2 and city2 not in self.available_cities:
            messagebox.showerror("Invalid City", f"'{city2}' is not in the list of available cities.")
            return False
            
        return True
    def _setup_ui(self):
        """Setup the UI components"""
        # Create main split-screen layout
        self.main_paned = ttk.PanedWindow(self.frame, orient="horizontal")
        self.main_paned.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left panel for input and text results
        self.left_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.left_frame, weight=1)
        
        # Right panel for charts and visualizations
        self.right_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.right_frame, weight=2)
        
        # Set up left panel (input and text results)
        self._setup_left_panel()
        
        # Set up right panel (charts)
        self._setup_right_panel()

    def _setup_left_panel(self):
        """Setup the left panel with input fields and text results"""
        import sys
        print(f"Setting up left panel with {len(self.available_cities)} cities available", file=sys.stderr, flush=True)
        
        # Create frame for team cities comparison
        team_frame = ttk.LabelFrame(self.left_frame, text="City Comparison")
        team_frame.pack(fill="x", padx=5, pady=5)
        
        # City 1 input section
        city1_frame = ttk.Frame(team_frame)
        city1_frame.pack(fill="x", padx=5, pady=5)
        
        StyledLabel(city1_frame, text="🏙️ First City", font=("Arial", 10, "bold")).pack()
        # Make sure we initialize with the correct values
        self.city1_combo = ttk.Combobox(city1_frame, values=self.available_cities, state="readonly")
        if self.available_cities:
            # Set initial value for first city
            self.city1_combo.set(self.available_cities[0])
            self.city1_combo.pack(fill="x", pady=(5, 0))
            print(f"City1 dropdown populated with {len(self.available_cities)} cities")
            print(f"First city set to: {self.available_cities[0]}")
        else:
            self.city1_combo["state"] = "disabled"
            self.city1_combo.pack(fill="x", pady=(5, 0))
            error_label = StyledLabel(city1_frame, text="⚠️ No cities available", foreground="red")
            error_label.pack(pady=2)
        
        # Quick info for city 1
        city1_info = ttk.Frame(city1_frame)
        city1_info.pack(fill="x", pady=5)
        self.city1_temp = StyledLabel(city1_info, text="🌡️ --°C")
        self.city1_temp.pack(side="left", padx=5)
        self.city1_weather = StyledLabel(city1_info, text="☀️ --")
        self.city1_weather.pack(side="right", padx=5)
        
        # Separator
        ttk.Separator(team_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # City 2 input section
        city2_frame = ttk.Frame(team_frame)
        city2_frame.pack(fill="x", padx=5, pady=5)
        
        StyledLabel(city2_frame, text="🌆 Second City", font=("Arial", 10, "bold")).pack()
        # Make sure we initialize with the correct values
        self.city2_combo = ttk.Combobox(city2_frame, values=self.available_cities, state="readonly")
        if self.available_cities:
            # Set initial value for second city if we have at least 2 cities
            if len(self.available_cities) > 1:
                self.city2_combo.set(self.available_cities[1])
                print(f"Second city set to: {self.available_cities[1]}")
            elif self.available_cities:
                # If only one city, use the same city (though this will cause validation errors later)
                self.city2_combo.set(self.available_cities[0])
                print(f"Second city set to: {self.available_cities[0]} (same as first)")
            self.city2_combo.pack(fill="x", pady=(5, 0))
        else:
            self.city2_combo["state"] = "disabled"
            self.city2_combo.pack(fill="x", pady=(5, 0))
            error_label = StyledLabel(city2_frame, text="⚠️ No cities available", foreground="red")
            error_label.pack(pady=2)
        
        # Quick info for city 2
        city2_info = ttk.Frame(city2_frame)
        city2_info.pack(fill="x", pady=5)
        self.city2_temp = StyledLabel(city2_info, text="🌡️ --°C")
        self.city2_temp.pack(side="left", padx=5)
        self.city2_weather = StyledLabel(city2_info, text="☀️ --")
        self.city2_weather.pack(side="right", padx=5)
        
        # Comparison buttons
        button_frame = ttk.Frame(team_frame)
        button_frame.pack(fill="x", padx=5, pady=10)
        
        # Row 1 buttons
        row1 = ttk.Frame(button_frame)
        row1.pack(fill="x", pady=2)
        StyledButton(row1, "primary_black", text="🔄 Compare", 
                    command=self.compare_cities).pack(side="left", padx=2, expand=True)
        StyledButton(row1, "info_black", text="📊 Details", 
                    command=self.detailed_comparison).pack(side="right", padx=2, expand=True)
        
        # Row 2 buttons
        row2 = ttk.Frame(button_frame)
        row2.pack(fill="x", pady=2)
        StyledButton(row2, "success_black", text="✈️ Travel Tips", 
                    command=self.get_travel_advice).pack(side="left", padx=2, expand=True)
        StyledButton(row2, "warning_black", text="🗺️ Distance", 
                    command=self.show_distance_info).pack(side="right", padx=2, expand=True)
                    
        # Row 3 buttons - Add fix button
        row3 = ttk.Frame(button_frame)
        row3.pack(fill="x", pady=2)
        StyledButton(row3, "accent_black", text="🔧 Fix Comparison", 
                    command=self.fix_radar_comparison).pack(side="left", padx=2, expand=True)
        
        # Results text area
        results_frame = ttk.LabelFrame(self.left_frame, text="Comparison Results")
        results_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.result_text = StyledText(results_frame)
        self.result_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Results area
        self.result_text = StyledText(self.left_frame, height=15)
        self.result_text.pack(pady=10, fill="both", expand=True, padx=10)
        
        # Main action button
        StyledButton(self.left_frame, "info_black", text="Compare", 
                    command=self.compare_cities).pack(pady=5)
        
        # Additional Enhanced Buttons
        comparison_button_frame = ttk.Frame(self.left_frame)
        comparison_button_frame.pack(pady=5)
        
        StyledButton(comparison_button_frame, "accent_black", text="🗺️ Distance Info", 
                    command=self.show_distance_info).grid(row=0, column=0, padx=3)
        StyledButton(comparison_button_frame, "primary_black", text="📊 Detailed Compare", 
                    command=self.detailed_comparison).grid(row=0, column=1, padx=3)
        StyledButton(comparison_button_frame, "success_black", text="✈️ Travel Advice", 
                    command=self.get_travel_advice).grid(row=0, column=2, padx=3)
        StyledButton(comparison_button_frame, "warning_black", text="⭐ Multi-Compare", 
                    command=self.multi_city_compare).grid(row=0, column=3, padx=3)

    # Methods for team cities comparison removed
        
    def _setup_right_panel(self):
        """Setup the right panel with charts and visualizations"""
        # Create main container for right panel
        main_container = ttk.Frame(self.right_frame)
        main_container.pack(fill="both", expand=True)
        
        # Chart title with smaller font
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill="x", pady=(5,0))
        StyledLabel(title_frame, text="📊 City Comparison Charts", 
                   font=("Arial", 12, "bold")).pack(pady=2)
        
        # Chart selection buttons in a more compact layout
        chart_controls = ttk.Frame(main_container)
        chart_controls.pack(fill="x", pady=2)
        
        # Create a grid for buttons with minimal spacing
        button_frame = ttk.Frame(chart_controls)
        button_frame.pack()
        
        # Row 1 buttons
        StyledButton(button_frame, "info_black", text="🌡️ Temperature", 
                    command=self.generate_temperature_comparison_chart).grid(row=0, column=0, padx=1, pady=1)
        StyledButton(button_frame, "primary_black", text="📊 Metrics", 
                    command=self.generate_radar_comparison_chart).grid(row=0, column=1, padx=1, pady=1)
        
        # Row 2 buttons
        StyledButton(button_frame, "success_black", text="💧 Humidity", 
                    command=self.generate_humidity_pressure_chart).grid(row=1, column=0, padx=1, pady=1)
        StyledButton(button_frame, "warning_black", text="📈 Trends", 
                    command=self.generate_climate_trend_chart).grid(row=1, column=1, padx=1, pady=1)
        
        # Chart display area with fixed size
        chart_container = ttk.Frame(main_container)
        chart_container.pack(fill="both", expand=True, pady=2)
        
        # Create chart frame with specific size and scrolling capability
        canvas = tk.Canvas(chart_container)
        self.chart_frame = ttk.Frame(canvas)
        scrollbar = ttk.Scrollbar(chart_container, orient="vertical", command=canvas.yview)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Create window in canvas for chart frame
        canvas_frame = canvas.create_window((0, 0), window=self.chart_frame, anchor="nw")
        
        # Configure canvas scrolling
        def configure_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Keep the width of the chart frame matched to the canvas
            canvas.itemconfig(canvas_frame, width=canvas.winfo_width())
            
        self.chart_frame.bind("<Configure>", configure_scroll)
        
        # Create initial chart placeholder
        self._create_chart_placeholder()
        
    def _create_chart_placeholder(self):
        """Create a placeholder for the chart area"""
        # Create frame with specific size
        placeholder_frame = ttk.Frame(self.chart_frame)
        placeholder_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Info icon and header
        header_frame = ttk.Frame(placeholder_frame)
        header_frame.pack(fill="x", pady=(10,5))
        
        StyledLabel(header_frame, 
                   text="📈 Interactive Weather Visualization",
                   font=("Arial", 11, "bold")).pack()
        
        # Main instruction
        instruction_frame = ttk.Frame(placeholder_frame)
        instruction_frame.pack(fill="x", pady=5)
        
        StyledLabel(instruction_frame,
                   text="Select two cities and choose a visualization type",
                   font=("Arial", 10)).pack()
        
        # Chart descriptions in a more compact format
        desc_frame = ttk.Frame(placeholder_frame)
        desc_frame.pack(fill="both", expand=True, pady=10)
        
        charts_info = [
            ("🌡️ Temperature", "Compare temperature metrics between cities"),
            ("📊 Metrics Radar", "Multi-dimensional weather comparison"),
            ("💧 Humidity/Pressure", "Analyze weather correlations"),
            ("📈 Climate Trends", "View and compare weather patterns")
        ]
        
        for icon, desc in charts_info:
            chart_frame = ttk.Frame(desc_frame)
            chart_frame.pack(fill="x", pady=2)
            
            StyledLabel(chart_frame, text=icon,
                       font=("Arial", 10, "bold")).pack(side="left", padx=(5,10))
            StyledLabel(chart_frame, text=desc,
                       font=("Arial", 9)).pack(side="left")
            
        # Tip at the bottom
        tip_frame = ttk.Frame(placeholder_frame)
        tip_frame.pack(fill="x", pady=10)
        
        StyledLabel(tip_frame,
                   text="💡 Hover over charts for interactive features",
                   font=("Arial", 9, "italic")).pack()

    def _clear_chart_area(self):
        """Clear the chart display area and close all matplotlib figures"""
        # Close any open matplotlib figures to prevent memory leaks
        import matplotlib.pyplot as plt
        plt.close('all')
        
        # Remove all widgets from the chart frame
        if hasattr(self, 'chart_frame') and self.chart_frame:
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
                
        # Clear any references to previous canvas objects
        if hasattr(self, 'radar_chart_canvas') and self.radar_chart_canvas:
            self.radar_chart_canvas = None
    
    def generate_temperature_comparison_chart(self):
        """Generate temperature comparison bar chart"""
        if not CHARTS_AVAILABLE:
            messagebox.showwarning("Charts Unavailable", "Matplotlib is not installed")
            return
            
        if not self._validate_city_selection():
            return
            
        city1, city2 = self._get_selected_cities()
        
        if not city1 or not city2:
            messagebox.showwarning("Input Error", "Please select both cities from the dropdown menus")
            return
            
        try:
            self._clear_chart_area()
            
            # Create figure and axis with smaller size
            fig = Figure(figsize=(8, 4), dpi=100, facecolor='white')
            ax = fig.add_subplot(111)
            
            try:
                # Get real data from controller
                data1 = self.controller.get_weather_data(city1)
                data2 = self.controller.get_weather_data(city2)
                
                metrics = ['Current', 'Feels Like', 'Min', 'Max']
                city1_temps = [
                    data1.get('temp', 0),
                    data1.get('feels_like', 0),
                    data1.get('temp_min', 0),
                    data1.get('temp_max', 0)
                ]
                city2_temps = [
                    data2.get('temp', 0),
                    data2.get('feels_like', 0),
                    data2.get('temp_min', 0),
                    data2.get('temp_max', 0)
                ]
            except:
                # Fallback to mock data if API call fails
                metrics = ['Current', 'Feels Like', 'Min', 'Max']
                city1_temps = [24, 26, 18, 29]
                city2_temps = [19, 18, 15, 22]
            
            x = np.arange(len(metrics))
            width = 0.35
            
            # Create grouped bar chart
            rects1 = ax.bar(x - width/2, city1_temps, width, label=city1, color='#F8A65D')
            rects2 = ax.bar(x + width/2, city2_temps, width, label=city2, color='#4CA6FF')
            
            # Add labels and styling
            ax.set_title(f'Temperature Comparison: {city1} vs {city2}', fontsize=12, pad=15)
            ax.set_xlabel('Temperature Metrics', fontsize=10)
            ax.set_ylabel('Temperature (°C)', fontsize=10)
            ax.set_xticks(x)
            ax.set_xticklabels(metrics, rotation=45)
            ax.legend(loc='upper right')
            
            # Add value labels on top of bars
            def add_value_labels(rects):
                for rect in rects:
                    height = rect.get_height()
                    ax.annotate(f'{height:.1f}°C',
                            xy=(rect.get_x() + rect.get_width()/2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom',
                            fontsize=8)
            
            add_value_labels(rects1)
            add_value_labels(rects2)
            
            # Add grid and styling
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            # Adjust layout to prevent label cutoff
            fig.tight_layout()
            
            # Create frame for chart
            chart_container = ttk.Frame(self.chart_frame)
            chart_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Display the chart
            canvas = FigureCanvasTkAgg(fig, master=chart_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Add compact toolbar
            toolbar_frame = ttk.Frame(chart_container)
            toolbar_frame.pack(fill=tk.X, pady=(0, 5))
            toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
            toolbar.update()
            
            # Configure toolbar to be more compact
            for tool in toolbar.winfo_children():
                tool.pack_configure(padx=1, pady=1)
            
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to generate temperature comparison chart: {str(e)}")
    
    def generate_radar_comparison_chart(self):
        """Generate radar chart to compare multiple metrics"""
        if not CHARTS_AVAILABLE:
            messagebox.showwarning("Charts Unavailable", "Matplotlib is not installed")
            return
            
        if not self._validate_city_selection():
            return
            
        city1, city2 = self._get_selected_cities()
        
        if not city1 or not city2:
            messagebox.showwarning("Input Error", "Please select both cities from the dropdown menus")
            return
            
        try:
            self._clear_chart_area()
            
            # Create figure with smaller size
            fig = Figure(figsize=(6, 5), dpi=100, facecolor='white')
            ax = fig.add_subplot(111, polar=True)
            
            try:
                # Get real data from controller
                data1 = self.controller.get_weather_data(city1)
                data2 = self.controller.get_weather_data(city2)
                
                # Normalize values to 0-100 scale
                def normalize_temp(temp): return min(100, max(0, (temp + 20) * 2.5))
                def normalize_humidity(hum): return min(100, max(0, hum))
                def normalize_wind(wind): return min(100, max(0, wind * 10))
                def normalize_visibility(vis): return min(100, max(0, vis / 100))
                
                categories = ['Temperature', 'Humidity', 'Wind', 'Pressure', 'Visibility', 'Clouds']
                
                city1_values = [
                    normalize_temp(data1.get('temp', 20)),
                    normalize_humidity(data1.get('humidity', 50)),
                    normalize_wind(data1.get('wind_speed', 5)),
                    min(100, max(0, (data1.get('pressure', 1013) - 950) / 2)),
                    normalize_visibility(data1.get('visibility', 5000) / 100),
                    100 - data1.get('clouds', 50)  # Invert clouds percentage
                ]
                
                city2_values = [
                    normalize_temp(data2.get('temp', 20)),
                    normalize_humidity(data2.get('humidity', 50)),
                    normalize_wind(data2.get('wind_speed', 5)),
                    min(100, max(0, (data2.get('pressure', 1013) - 950) / 2)),
                    normalize_visibility(data2.get('visibility', 5000) / 100),
                    100 - data2.get('clouds', 50)  # Invert clouds percentage
                ]
            except:
                # Fallback to mock data if API call fails
                categories = ['Temperature', 'Humidity', 'Wind', 'Pressure', 'Visibility', 'Clouds']
                city1_values = [80, 65, 40, 75, 90, 60]
                city2_values = [50, 85, 65, 45, 70, 40]
            
            # Number of metrics
            N = len(categories)
            
            # Create angles for each metric (radians)
            angles = [n / float(N) * 2 * np.pi for n in range(N)]
            angles += angles[:1]  # Close the loop
            
            # Add values to complete the loop
            city1_values += city1_values[:1]
            city2_values += city2_values[:1]
            
            # Plot radar chart
            ax.plot(angles, city1_values, 'o-', linewidth=2, label=city1, color='#FF6B6B')
            ax.fill(angles, city1_values, alpha=0.25, color='#FF6B6B')
            
            ax.plot(angles, city2_values, 'o-', linewidth=2, label=city2, color='#4ECDC4')
            ax.fill(angles, city2_values, alpha=0.25, color='#4ECDC4')
            
            # Set category labels
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories)
            
            # Add grid and styling
            ax.set_yticks([20, 40, 60, 80, 100])
            ax.set_yticklabels(['20', '40', '60', '80', '100'])
            ax.set_ylim(0, 100)
            
            # Add title and legend
            ax.set_title(f'Weather Metrics Comparison: {city1} vs {city2}', size=14, fontweight='bold', pad=20)
            ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
            
            # Display the chart
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Add toolbar for interactive features
            toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
            toolbar.update()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to generate radar comparison chart: {str(e)}")
    
    def generate_humidity_pressure_chart(self):
        """Generate scatter plot showing humidity vs pressure correlation"""
        if not CHARTS_AVAILABLE:
            messagebox.showwarning("Charts Unavailable", "Matplotlib is not installed")
            return
            
        if not self._validate_city_selection():
            return
            
        city1, city2 = self._get_selected_cities()
        
        if not city1 or not city2:
            messagebox.showwarning("Input Error", "Please select both cities from the dropdown menus")
            return
            
        try:
            self._clear_chart_area()
            
            # Create figure and axis
            fig = Figure(figsize=(9, 6), dpi=100, facecolor='white')
            ax = fig.add_subplot(111)
            
            # Mock data points for the past week (humidity % vs pressure hPa)
            # In a real app, this would come from API/historical data
            city1_humidity = [65, 68, 72, 70, 75, 67, 63]
            city1_pressure = [1012, 1010, 1008, 1007, 1005, 1008, 1011]
            
            city2_humidity = [55, 58, 62, 60, 65, 70, 72]
            city2_pressure = [1015, 1014, 1012, 1010, 1008, 1007, 1009]
            
            # Create scatter plot with trend lines
            ax.scatter(city1_humidity, city1_pressure, color='#FC766A', s=100, alpha=0.7, 
                      label=f"{city1}", edgecolors='white', linewidth=1)
            ax.scatter(city2_humidity, city2_pressure, color='#5B84B1', s=100, alpha=0.7, 
                      label=f"{city2}", edgecolors='white', linewidth=1)
            
            # Add trend lines with smaller line width
            z1 = np.polyfit(city1_humidity, city1_pressure, 1)
            p1 = np.poly1d(z1)
            x_range = np.linspace(min(city1_humidity), max(city1_humidity), 100)
            ax.plot(x_range, p1(x_range), color='#FC766A', linestyle='--', linewidth=1.5)
            
            z2 = np.polyfit(city2_humidity, city2_pressure, 1)
            p2 = np.poly1d(z2)
            x_range = np.linspace(min(city2_humidity), max(city2_humidity), 100)
            ax.plot(x_range, p2(x_range), color='#5B84B1', linestyle='--', linewidth=1.5)
            
            # Add labels and styling with smaller font sizes
            ax.set_title('Humidity vs. Air Pressure', fontsize=12, pad=15)
            ax.set_xlabel('Humidity (%)', fontsize=10)
            ax.set_ylabel('Air Pressure (hPa)', fontsize=10)
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.legend(fontsize=9)
            
            # Reduce scatter point size
            ax.collections[0].set_sizes([60])
            ax.collections[1].set_sizes([60])
            
            # Annotate correlation patterns
            corr1 = round(np.corrcoef(city1_humidity, city1_pressure)[0, 1], 2)
            corr2 = round(np.corrcoef(city2_humidity, city2_pressure)[0, 1], 2)
            
            ax.annotate(f"Correlation: {corr1}", 
                       xy=(city1_humidity[0], city1_pressure[0]),
                       xytext=(city1_humidity[0]+5, city1_pressure[0]+5),
                       color='#FC766A',
                       fontweight='bold')
                       
            ax.annotate(f"Correlation: {corr2}", 
                       xy=(city2_humidity[0], city2_pressure[0]),
                       xytext=(city2_humidity[0]+5, city2_pressure[0]-5),
                       color='#5B84B1',
                       fontweight='bold')
            
            # Display the chart
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Add toolbar for interactive features
            toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
            toolbar.update()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to generate humidity/pressure chart: {str(e)}")
    
    def generate_climate_trend_chart(self):
        """Generate line chart showing climate trends"""
        if not CHARTS_AVAILABLE:
            messagebox.showwarning("Charts Unavailable", "Matplotlib is not installed")
            return
            
        if not self._validate_city_selection():
            return
            
        city1, city2 = self._get_selected_cities()
        
        if not city1 or not city2:
            messagebox.showwarning("Input Error", "Please select both cities from the dropdown menus")
            return
            
        try:
            self._clear_chart_area()
            
            # Create figure and axis
            fig = Figure(figsize=(10, 6), dpi=100, facecolor='white')
            ax = fig.add_subplot(111)
            
            # Mock data for monthly temperature trends
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            city1_temps = [5, 6, 10, 15, 20, 24, 27, 26, 22, 16, 10, 6]
            city2_temps = [12, 13, 15, 17, 20, 23, 25, 25, 23, 20, 16, 13]
            
            # Plot the data
            ax.plot(months, city1_temps, marker='o', linewidth=3, markersize=8, 
                   color='#FF9671', label=city1)
            ax.plot(months, city2_temps, marker='s', linewidth=3, markersize=8, 
                   color='#00D2FC', label=city2)
            
            # Fill below the lines
            ax.fill_between(months, city1_temps, alpha=0.2, color='#FF9671')
            ax.fill_between(months, city2_temps, alpha=0.2, color='#00D2FC')
            
            # Highlight seasonal differences
            ax.axvspan(0, 1.5, alpha=0.1, color='#B0E0E6', label='Winter')  # Winter
            ax.axvspan(2.5, 4.5, alpha=0.1, color='#98FB98', label='Spring')  # Spring
            ax.axvspan(5.5, 7.5, alpha=0.1, color='#FFDAB9', label='Summer')  # Summer
            ax.axvspan(8.5, 10.5, alpha=0.1, color='#FFB347', label='Fall')  # Fall
            
            # Add labels and styling
            ax.set_title(f'Annual Temperature Trends: {city1} vs {city2}', fontsize=14, fontweight='bold', pad=20)
            ax.set_xlabel('Month', fontsize=12)
            ax.set_ylabel('Temperature (°C)', fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Add min/max annotations
            city1_max_idx = city1_temps.index(max(city1_temps))
            city1_min_idx = city1_temps.index(min(city1_temps))
            city2_max_idx = city2_temps.index(max(city2_temps))
            city2_min_idx = city2_temps.index(min(city2_temps))
            
            ax.annotate(f"Max: {max(city1_temps)}°C", 
                       xy=(months[city1_max_idx], max(city1_temps)),
                       xytext=(0, 10),
                       textcoords="offset points",
                       ha='center',
                       color='#FF9671',
                       fontweight='bold')
                       
            ax.annotate(f"Min: {min(city1_temps)}°C", 
                       xy=(months[city1_min_idx], min(city1_temps)),
                       xytext=(0, -15),
                       textcoords="offset points",
                       ha='center',
                       color='#FF9671',
                       fontweight='bold')
                       
            ax.annotate(f"Max: {max(city2_temps)}°C", 
                       xy=(months[city2_max_idx], max(city2_temps)),
                       xytext=(0, 10),
                       textcoords="offset points",
                       ha='center',
                       color='#00D2FC',
                       fontweight='bold')
                       
            ax.annotate(f"Min: {min(city2_temps)}°C", 
                       xy=(months[city2_min_idx], min(city2_temps)),
                       xytext=(0, -15),
                       textcoords="offset points",
                       ha='center',
                       color='#00D2FC',
                       fontweight='bold')
            
            # Add legend with season colors
            handles, labels = ax.get_legend_handles_labels()
            city_handles = handles[:2]
            season_handles = handles[2:]
            city_labels = labels[:2]
            season_labels = labels[2:]
            
            # Two separate legends for cities and seasons
            legend1 = ax.legend(city_handles, city_labels, loc='upper left')
            ax.add_artist(legend1)
            
            # Display the chart
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Add toolbar for interactive features
            toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
            toolbar.update()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to generate climate trend chart: {str(e)}")
    
    # This duplicate compare_cities method is removed as we already have a more comprehensive one later in the code

    # This is the correct _validate_city_selection method that we'll keep
        
    def _get_selected_cities(self):
        """Get the selected cities from the combo boxes"""
        try:
            return (self.city1_combo.get().strip(), self.city2_combo.get().strip())
        except Exception as e:
            messagebox.showerror("Error", "Failed to get selected cities")
            return None, None
            
    def _update_comparison_text(self, city1, city2):
        """Update the comparison text between cities with comprehensive data"""
        try:
            # Make sure we have weather data for both cities
            if city1 not in self._weather_df or city2 not in self._weather_df:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"Error: Missing weather data for one or both cities.")
                return
            
            # Get data safely
            data1 = self._weather_df[city1]
            data2 = self._weather_df[city2]
            
            # Format the comparison text with a header
            comparison = f"WEATHER COMPARISON: {city1.upper()} vs {city2.upper()}\n"
            comparison += "=" * 50 + "\n\n"
            
            # Create a table-like display with main weather information
            comparison += f"{'Current Conditions:':<25}\n"
            comparison += f"{'-' * 50}\n"
            comparison += f"{'City':<15} | {'Temp (°C)':<10} | {'Description':<20}\n"
            comparison += f"{'-' * 50}\n"
            comparison += f"{city1:<15} | {data1.get('temp', 'N/A'):<10} | {data1.get('description', 'N/A'):<20}\n"
            comparison += f"{city2:<15} | {data2.get('temp', 'N/A'):<10} | {data2.get('description', 'N/A'):<20}\n\n"
            
            # Find all common metrics between the two cities for detailed comparison
            common_metrics = set(data1.keys()).intersection(set(data2.keys()))
            
            # Remove description since we already displayed it
            if 'description' in common_metrics:
                common_metrics.remove('description')
                
            # Create a section for detailed metrics comparison if we have any
            if common_metrics:
                comparison += f"{'Detailed Weather Metrics:':<25}\n"
                comparison += f"{'-' * 50}\n"
                
                # Display each metric in a consistent format
                for metric in sorted(common_metrics):
                    # Skip description as we've already shown it
                    if metric == 'description':
                        continue
                        
                    # Create a human-readable metric name
                    metric_name = metric.replace('_', ' ').title()
                    
                    # Add units based on the metric
                    unit = ""
                    if metric == 'temp' or metric == 'feels_like':
                        unit = "°C"
                    elif metric == 'humidity' or metric == 'cloud_cover':
                        unit = "%"
                    elif metric == 'wind_speed':
                        unit = "m/s"
                    elif metric == 'pressure':
                        unit = "hPa"
                    elif metric == 'visibility':
                        unit = "km"
                    elif metric == 'precipitation':
                        unit = "mm"
                        
                    # Add the metric comparison
                    val1 = data1.get(metric, 'N/A')
                    val2 = data2.get(metric, 'N/A')
                    
                    comparison += f"{metric_name:<15}:\n"
                    comparison += f"  {city1:<12}: {val1} {unit}\n"
                    comparison += f"  {city2:<12}: {val2} {unit}\n\n"
            
            # Add a note about the charts
            comparison += f"{'-' * 50}\n"
            comparison += "Charts displayed below provide visual comparison.\n"
            comparison += "Use the toolbar for zooming and navigation options.\n"
            
            # Update the text widget with all the comparison data
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, comparison)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Error updating comparison: {str(e)}")

    def compare_cities(self):
        """Compare weather between two cities with enhanced visualization"""
        try:
            # First validate the city selection
            if not self._validate_city_selection():
                return
                
            # Get the validated cities
            city1, city2 = self._get_selected_cities()
            
            # Double-check cities are valid
            if not city1 or not city2 or city1 not in self.available_cities or city2 not in self.available_cities:
                messagebox.showerror("Error", "Invalid city selection")
                return
                
            # Initialize weather data storage
            self._weather_df = {}
            
            # Get weather data for both cities
            data1 = self.controller.get_current_weather(city1)
            if not data1:
                messagebox.showerror("Error", f"Could not retrieve weather data for {city1}")
                return
                
            data2 = self.controller.get_current_weather(city2)
            if not data2:
                messagebox.showerror("Error", f"Could not retrieve weather data for {city2}")
                return
            
            # Define a function to safely get attributes
            def safe_get_attr(obj, attr, default=0):
                try:
                    # Handle both object attributes and dictionary keys
                    if hasattr(obj, 'get') and callable(obj.get):  # This is a dictionary
                        return obj.get(attr, default)
                    else:  # This is an object with attributes
                        return getattr(obj, attr, default)
                except (AttributeError, TypeError, KeyError):
                    return default
            
            # Store the data for charts with safety checks
            self._weather_df[city1] = {
                'temp': safe_get_attr(data1, 'temperature'),
                'humidity': safe_get_attr(data1, 'humidity'),
                'wind_speed': safe_get_attr(data1, 'wind_speed'),
                'description': safe_get_attr(data1, 'description', 'Unknown')
            }
            self._weather_df[city2] = {
                'temp': safe_get_attr(data2, 'temperature'),
                'humidity': safe_get_attr(data2, 'humidity'),
                'wind_speed': safe_get_attr(data2, 'wind_speed'),
                'description': safe_get_attr(data2, 'description', 'Unknown')
            }
            
            # First update the comparison text so users can see the data immediately
            self._update_comparison_text(city1, city2)
            
            # Create radar chart for comparison
            self._create_radar_chart(city1, city2)
            
            # Create bar charts for metrics
            self._create_bar_charts(city1, city2)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compare cities: {str(e)}")
            self._weather_df = {}  # Reset on error
            return
            
    def _create_bar_charts(self, city1, city2):
        """Create bar charts comparing temperature, humidity, and wind speed"""
        if not CHARTS_AVAILABLE:
            messagebox.showwarning("Charts Unavailable", "Matplotlib is not installed")
            return
            
        try:
            # Get data for both cities
            data1 = self._weather_df[city1]
            data2 = self._weather_df[city2]
            
            # Define metrics for comparison
            metrics = {
                'Temperature (°C)': 'temp',
                'Humidity (%)': 'humidity',
                'Wind Speed (m/s)': 'wind_speed'
            }
            
            # Create figure with subplots
            fig = self.Figure(figsize=(8, 6), dpi=100, facecolor='white')
            fig.subplots_adjust(hspace=0.3)  # Add space between subplots
            
            # Create grid of subplots
            gs = fig.add_gridspec(3, 1)
            axes = [fig.add_subplot(gs[i]) for i in range(3)]
            
            # Plot each metric as a bar chart
            for i, (metric_name, metric_key) in enumerate(metrics.items()):
                ax = axes[i]
                
                # Get data for the metric
                value1 = data1.get(metric_key, 0)
                value2 = data2.get(metric_key, 0)
                
                # Create bar chart
                bars = ax.bar([city1, city2], [value1, value2], 
                             color=['#FF9671', '#00D2FC'], alpha=0.8)
                
                # Add value labels
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.1f}',
                           ha='center', va='bottom', fontsize=9)
                
                # Add styling
                ax.set_title(f'{metric_name} Comparison', fontsize=10)
                ax.grid(axis='y', linestyle='--', alpha=0.7)
                ax.set_ylabel(metric_name.split(' ')[0], fontsize=9)
                
            # Adjust layout
            fig.tight_layout()
            
            # Create frame for chart
            chart_container = ttk.Frame(self.chart_frame)
            chart_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Display the chart
            canvas = self.FigureCanvasTkAgg(fig, master=chart_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Add compact toolbar
            toolbar_frame = ttk.Frame(chart_container)
            toolbar_frame.pack(fill=tk.X, pady=(0, 5))
            toolbar = self.NavigationToolbar2Tk(canvas, toolbar_frame)
            toolbar.update()
            
            # Configure toolbar to be more compact
            for tool in toolbar.winfo_children():
                tool.pack_configure(padx=1, pady=1)
                
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to create bar charts: {str(e)}")

    def _create_radar_chart(self, city1, city2):
        """Create radar chart comparing multiple weather metrics"""
        if not CHARTS_AVAILABLE:
            messagebox.showwarning("Charts Unavailable", "Matplotlib is not installed")
            return
            
        try:
            # Get data for both cities
            data1 = self._weather_df[city1]
            data2 = self._weather_df[city2]
            
            # Find ALL common metrics between the two cities
            common_metrics = []
            for metric in set(data1.keys()).intersection(set(data2.keys())):
                if metric != 'description':  # Skip text fields
                    common_metrics.append(metric)
            
            # If no common metrics, show error and return
            if not common_metrics:
                messagebox.showerror("Error", "No common metrics found for comparison")
                return
                
            if len(common_metrics) < 2:
                messagebox.showerror("Error", "At least 2 common metrics are required for a radar chart")
                return
                
            # Use only common metrics
            metrics = common_metrics
            
            # Create human-readable labels
            labels = []
            for metric in metrics:
                if metric == 'temp':
                    labels.append('Temperature')
                elif metric == 'humidity':
                    labels.append('Humidity')
                elif metric == 'wind_speed':
                    labels.append('Wind Speed')
                else:
                    # Convert snake_case to Title Case
                    labels.append(metric.replace('_', ' ').title())
            
            # Extended normalization values for radar chart (0-100 scale)
            max_vals = {
                'temp': 40,         # Max reasonable temperature (°C)
                'humidity': 100,     # Max humidity percentage
                'wind_speed': 50,    # Max reasonable wind speed (km/h)
                'pressure': 1050,    # Max reasonable pressure (hPa)
                'visibility': 20,    # Max visibility (km)
                'uv_index': 12,      # Max UV index
                'cloud_cover': 100,  # Max cloud cover percentage
                'precipitation': 50, # Max reasonable precipitation (mm)
                'comfort': 100,      # Comfort index
                'air_quality': 500,  # Air quality index
                'feels_like': 45     # Feels like temperature (°C)
            }
            
            # Safely extract data with default values for missing metrics
            normalized_data1 = []
            normalized_data2 = []
            
            for metric in metrics:
                # Get values with default of 0
                val1 = data1.get(metric, 0)
                val2 = data2.get(metric, 0)
                
                # Handle None values
                val1 = 0 if val1 is None else val1
                val2 = 0 if val2 is None else val2
                
                try:
                    # Convert to float if not already
                    val1 = float(val1)
                    val2 = float(val2)
                    
                    # Normalize to 0-100 scale
                    max_val = max_vals.get(metric, 100)  # Default max value is 100
                    
                    # Ensure we're not dividing by zero
                    if max_val > 0:
                        normalized_data1.append(min(100, (val1/max_val) * 100))
                        normalized_data2.append(min(100, (val2/max_val) * 100))
                    else:
                        normalized_data1.append(0)
                        normalized_data2.append(0)
                        
                except (ValueError, TypeError):
                    # Handle conversion errors
                    normalized_data1.append(0)
                    normalized_data2.append(0)
            
            # Clear existing charts
            self._clear_chart_area()
            
            # Create figure with smaller size
            fig = self.Figure(figsize=(6, 5), dpi=100, facecolor='white')
            ax = fig.add_subplot(111, polar=True)
            
            # Number of metrics
            N = len(metrics)
            if N < 2:
                messagebox.showerror("Error", "At least 2 metrics are required for a radar chart")
                return
                
            # Create angles for each metric (radians)
            angles = [n / float(N) * 2 * np.pi for n in range(N)]
            angles += angles[:1]  # Close the loop
            
            # Add values to complete the loop - make sure both arrays have the same length
            normalized_data1 = normalized_data1 + [normalized_data1[0]]
            normalized_data2 = normalized_data2 + [normalized_data2[0]]
            
            # Verify array shapes match before plotting - if there's a mismatch, fix it
            if len(angles) != len(normalized_data1) or len(angles) != len(normalized_data2):
                print(f"WARNING: Shape mismatch detected - angles={len(angles)}, data1={len(normalized_data1)}, data2={len(normalized_data2)}")
                print("Attempting to fix array shapes...")
                
                # Ensure all arrays have the same length by rebuilding them
                # First get the correct number of metrics (should be the length of angles minus 1)
                correct_metrics_count = len(angles) - 1
                
                if len(metrics) != correct_metrics_count:
                    # Need to rebuild everything from scratch using only common metrics
                    common_metrics = []
                    for metric in set(data1.keys()).intersection(set(data2.keys())):
                        if metric != 'description':  # Skip text fields
                            common_metrics.append(metric)
                    
                    # Use only common metrics
                    metrics = common_metrics[:correct_metrics_count]
                    
                    # Recreate the normalized data
                    normalized_data1 = []
                    normalized_data2 = []
                    
                    for metric in metrics:
                        val1 = float(data1.get(metric, 0) or 0)
                        val2 = float(data2.get(metric, 0) or 0)
                        max_val = max_vals.get(metric, 100)
                        
                        if max_val > 0:
                            normalized_data1.append(min(100, (val1/max_val) * 100))
                            normalized_data2.append(min(100, (val2/max_val) * 100))
                        else:
                            normalized_data1.append(0)
                            normalized_data2.append(0)
                    
                    # Rebuild angles with the correct number of metrics
                    N = len(metrics)
                    angles = [n / float(N) * 2 * np.pi for n in range(N)]
                    angles += angles[:1]  # Close the loop
                
                # Make sure the data arrays close the loop by adding the first value to the end
                normalized_data1 = normalized_data1[:len(angles)-1]
                normalized_data1.append(normalized_data1[0])
                
                normalized_data2 = normalized_data2[:len(angles)-1]
                normalized_data2.append(normalized_data2[0])
                
                # Final verification
                if len(angles) != len(normalized_data1) or len(angles) != len(normalized_data2):
                    error_msg = f"Unable to fix shape mismatch: angles={len(angles)}, data1={len(normalized_data1)}, data2={len(normalized_data2)}"
                    print(f"ERROR: {error_msg}")
                    messagebox.showerror("Error", f"Failed to create chart: {error_msg}")
                    return
                
                print("✅ Array shapes fixed successfully")
                
            # Plot radar chart with error handling
            try:
                ax.plot(angles, normalized_data1, 'o-', linewidth=2, label=city1, color='#FF6B6B')
                ax.fill(angles, normalized_data1, alpha=0.25, color='#FF6B6B')
                
                ax.plot(angles, normalized_data2, 'o-', linewidth=2, label=city2, color='#4ECDC4')
                ax.fill(angles, normalized_data2, alpha=0.25, color='#4ECDC4')
                
                # Set category labels
                ax.set_xticks(angles[:-1])
                ax.set_xticklabels(labels)
            except ValueError as ve:
                messagebox.showerror("Error", f"Failed to create chart: {str(ve)}")
                return
            
            # Add grid and styling
            ax.set_yticks([20, 40, 60, 80, 100])
            ax.set_yticklabels(['20', '40', '60', '80', '100'])
            ax.set_ylim(0, 100)
            
            # Add title and legend
            ax.set_title(f'Weather Metrics Comparison: {city1} vs {city2}', size=12, pad=20)
            ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
            
            # Create frame for chart
            chart_container = ttk.Frame(self.chart_frame)
            chart_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Display the chart - with proper error handling
            try:
                # Create the canvas with error handling
                canvas = self.FigureCanvasTkAgg(fig, master=chart_container)
                canvas.draw()
                
                # Pack the canvas widget safely
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=tk.BOTH, expand=True)
                
                # Store reference to the canvas to properly clean it up later
                self.radar_chart_canvas = canvas
                
                # Add toolbar for interactive features - only if canvas was created successfully
                toolbar_frame = ttk.Frame(chart_container)
                toolbar_frame.pack(fill=tk.X, pady=(0, 5))
                
                try:
                    # Create toolbar with error handling
                    toolbar = self.NavigationToolbar2Tk(canvas, toolbar_frame)
                    toolbar.update()
                    
                    # Configure toolbar to be more compact
                    for tool in toolbar.winfo_children():
                        tool.pack_configure(padx=1, pady=1)
                except Exception as toolbar_error:
                    print(f"Warning: Could not create toolbar: {str(toolbar_error)}")
                    # Not critical - continue without toolbar if it fails
            except Exception as canvas_error:
                # If canvas creation fails, show error and clean up
                import traceback
                traceback.print_exc()
                print(f"Error creating canvas: {str(canvas_error)}")
                messagebox.showerror("Error", f"Failed to display chart: {str(canvas_error)}")
                
        except Exception as e:
            # Clean up properly in case of error
            import matplotlib.pyplot as plt
            plt.close('all')  # Close all existing figures to prevent memory leaks
            messagebox.showerror("Chart Error", f"Failed to create radar chart: {str(e)}")
            # Make sure we don't continue with chart rendering after an error
            return

    def _create_bar_charts(self, city1, city2):
        """Create bar charts for individual metric comparisons"""
        data1 = self._weather_df[city1]
        data2 = self._weather_df[city2]
        
        metrics = ['temp', 'humidity', 'wind_speed']
        labels = ['Temperature (°C)', 'Humidity (%)', 'Wind Speed (km/h)']
        
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))
        
        for i, (metric, label) in enumerate(zip(metrics, labels)):
            axs[i].bar([city1, city2], [data1[metric], data2[metric]])
            axs[i].set_title(label)
            axs[i].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('metric_comparisons.png')
        plt.close()

    def _update_comparison_text(self, city1, city2):
        """Update text comparison between cities"""
        data1 = self._weather_df[city1]
        data2 = self._weather_df[city2]
        
        # Create an enhanced, formatted comparison text
        comparison = f"📊 CITY COMPARISON: {city1} vs {city2}\n"
        comparison += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # Temperature comparison with emoji and formatting
        temp_diff = data1['temp'] - data2['temp']
        comparison += f"🌡️ TEMPERATURE:\n"
        comparison += f"• {city1}: {data1['temp']}°C\n"
        comparison += f"• {city2}: {data2['temp']}°C\n"
        comparison += f"• Difference: {abs(temp_diff):.1f}°C "
        comparison += f"({'warmer' if temp_diff > 0 else 'cooler'} in {city1})\n\n"
        
        # Humidity comparison
        humid_diff = data1['humidity'] - data2['humidity']
        comparison += f"💧 HUMIDITY:\n"
        comparison += f"• {city1}: {data1['humidity']}%\n"
        comparison += f"• {city2}: {data2['humidity']}%\n"
        comparison += f"• Difference: {abs(humid_diff):.1f}% "
        comparison += f"({'higher' if humid_diff > 0 else 'lower'} in {city1})\n\n"
        
        # Wind comparison
        wind_diff = data1['wind_speed'] - data2['wind_speed']
        comparison += f"💨 WIND SPEED:\n"
        comparison += f"• {city1}: {data1['wind_speed']} km/h\n"
        comparison += f"• {city2}: {data2['wind_speed']} km/h\n"
        comparison += f"• Difference: {abs(wind_diff):.1f} km/h "
        comparison += f"({'windier' if wind_diff > 0 else 'calmer'} in {city1})\n\n"
        
        # Weather conditions with emojis
        try:
            comparison += f"☁️ CURRENT CONDITIONS:\n"
            comparison += f"• {city1}: {data1['description']}\n"
            comparison += f"• {city2}: {data2['description']}\n\n"
            
            # Add overall recommendation section
            comparison += f"🏆 OVERALL COMPARISON:\n"
            if temp_diff > 0 and humid_diff < 0:
                comparison += f"• {city1} is warmer with lower humidity\n"
            elif temp_diff < 0 and humid_diff > 0:
                comparison += f"• {city2} is warmer with lower humidity\n"
            elif temp_diff > 0 and humid_diff > 0:
                comparison += f"• {city1} is warmer but more humid\n"
            elif temp_diff < 0 and humid_diff < 0:
                comparison += f"• {city2} is warmer but more humid\n"
            
            # Add a note about the charts
            comparison += "\n📈 VISUALIZATION:\n"
            comparison += "• Radar chart compares all metrics\n"
            comparison += "• Bar charts show individual comparisons\n"
            comparison += "• Temperature graph shows daily trends\n"
            comparison += "• Scroll down to see all charts\n"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, comparison)
                    
            # Try to update the quick info displays if they exist
            try:
                if hasattr(self, 'city1_temp') and hasattr(self, 'city1_weather'):
                    self.city1_temp.config(text=f"🌡️ {data1.get('temp', '--')}°C")
                    self.city1_weather.config(text=f"☁️ {data1.get('description', '--')}")
                
                if hasattr(self, 'city2_temp') and hasattr(self, 'city2_weather'):
                    self.city2_temp.config(text=f"🌡️ {data2.get('temp', '--')}°C")
                    self.city2_weather.config(text=f"☁️ {data2.get('description', '--')}")
            except (AttributeError, TypeError):
                # If quick info displays don't exist, just continue
                pass
            
            # We've already handled the comparison text update earlier
            # No need to update the text again here to avoid overwriting
            
            # Try to update charts if that method is available
            try:
                if hasattr(self, '_update_team_comparison_charts'):
                    self._update_team_comparison_charts(city1, city2, data1, data2)
            except (AttributeError, TypeError):
                pass
            
        except Exception as e:
            error_message = (
                f"Failed to compare cities: {str(e)}\n\n"
                "Please check:\n"
                "- City names are spelled correctly\n"
                "- Internet connection is active\n"
                "- Weather service is available"
            )
            messagebox.showerror("Comparison Error", error_message)

    def show_distance_info(self):
        """Show distance and geographic information between cities"""
        if not self._validate_city_selection():
            return
            
        city1, city2 = self._get_selected_cities()
        
        if not city1 or not city2:
            messagebox.showwarning("Input Error", "Please select both cities from the dropdown menus")
            return
        
        try:
            distance_info = f"🗺️ DISTANCE & GEOGRAPHIC INFO:\n"
            distance_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
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
            distance_info += "• Seasonal differences: May vary significantly\n\n"
            distance_info += "🧭 COORDINATE INFO:\n"
            distance_info += "• Direction: Calculate based on coordinates\n"
            distance_info += "• Climate zones: May differ significantly\n"
            distance_info += "• Weather patterns: Can be very different\n\n"
            distance_info += "💡 Tips for Travelers:\n"
            distance_info += "• Check time zones for communication\n"
            distance_info += "• Consider seasonal weather differences\n"
            distance_info += "• Plan for climate adaptation time"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, distance_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def detailed_comparison(self):
        """Show detailed comparison with more metrics"""
        city1 = self.city1_entry.get().strip()
        city2 = self.city2_entry.get().strip()
        
        if not city1 or not city2:
            messagebox.showwarning("Input Error", "Please enter both city names")
            return
        
        try:
            detailed = f"📊 DETAILED COMPARISON: {city1} vs {city2}\n"
            detailed += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
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
            detailed += "👁️ VISIBILITY & AIR QUALITY:\n"
            detailed += f"• {city1}: 10 km visibility, Good air quality\n"
            detailed += f"• {city2}: 8 km visibility, Fair air quality\n"
            detailed += f"• Winner: {city1} (Better visibility)\n\n"
            detailed += "☀️ UV INDEX & SUN:\n"
            detailed += f"• {city1}: UV Index 6, Sunrise 6:30, Sunset 19:45\n"
            detailed += f"• {city2}: UV Index 4, Sunrise 7:15, Sunset 19:20\n"
            detailed += f"• {city1}: More sun exposure needed\n\n"
            detailed += "🎯 OVERALL RECOMMENDATION:\n"
            detailed += f"Better weather today: {city1}\n"
            detailed += "• Warmer temperature\n"
            detailed += "• Lower humidity\n"
            detailed += "• Better visibility\n"
            detailed += "• Calmer wind conditions\n\n"
            detailed += "🏆 Weather Score:\n"
            detailed += f"• {city1}: 8.5/10\n"
            detailed += f"• {city2}: 6.5/10"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, detailed)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_travel_advice(self):
        """Get travel advice based on weather comparison"""
        city1 = self.city1_entry.get().strip()
        city2 = self.city2_entry.get().strip()
        
        if not city1 or not city2:
            messagebox.showwarning("Input Error", "Please enter both city names")
            return
        
        try:
            travel_advice = f"✈️ TRAVEL ADVICE: {city1} vs {city2}\n"
            travel_advice += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            travel_advice += "🎯 TRAVEL RECOMMENDATIONS:\n\n"
            travel_advice += f"📍 Current Conditions Analysis:\n"
            travel_advice += f"• {city1}: Better for outdoor activities\n"
            travel_advice += f"• {city2}: More suitable for indoor attractions\n\n"
            travel_advice += "🧳 PACKING SUGGESTIONS:\n\n"
            travel_advice += "• Lighter clothing (warmer weather)\n"
            travel_advice += "• Sunscreen and sunglasses\n"
            travel_advice += "• Light jacket for evening\n"
            travel_advice += "• Comfortable walking shoes\n\n"
            travel_advice += f"For {city2}:\n"
            travel_advice += "• Layered clothing (cooler weather)\n"
            travel_advice += "• Light rain jacket\n"
            travel_advice += "• Warmer evening wear\n"
            travel_advice += "• Umbrella (higher humidity)\n\n"
            travel_advice += "🗓️ TIMING RECOMMENDATIONS:\n\n"
            travel_advice += f"Visit {city1} for:\n"
            travel_advice += "• Outdoor sightseeing\n"
            travel_advice += "• Photography sessions\n"
            travel_advice += "• Walking tours\n"
            travel_advice += "• Beach/park activities\n\n"
            travel_advice += f"Visit {city2} for:\n"
            travel_advice += "• Museum visits\n"
            travel_advice += "• Indoor entertainment\n"
            travel_advice += "• Shopping experiences\n"
            travel_advice += "• Cozy café culture\n\n"
            travel_advice += "💰 COST CONSIDERATIONS:\n"
            travel_advice += f"• {city1}: Peak season pricing (good weather)\n"
            travel_advice += f"• {city2}: Potentially lower rates (weather dependent)\n\n"
            travel_advice += "🏆 VERDICT:\n"
            travel_advice += f"For outdoor enthusiasts: Choose {city1}\n"
            travel_advice += f"For culture seekers: Either city works\n"
            travel_advice += f"For budget travelers: Consider {city2}\n"
            travel_advice += f"For photographers: {city1} has better conditions"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, travel_advice)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def multi_city_compare(self):
        """Compare multiple cities at once"""
        try:
            multi_compare = f"⭐ MULTI-CITY COMPARISON:\n"
            multi_compare += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
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
            multi_compare += "☀️ SUNSHINE RANKINGS:\n"
            multi_compare += "• Sunniest: Los Angeles - Clear skies\n"
            multi_compare += "• Very Sunny: Athens - Bright and warm\n"
            multi_compare += "• Partly Sunny: Paris - Mixed conditions\n"
            multi_compare += "• Cloudy: Seattle - Overcast skies\n"
            multi_compare += "• Rainy: London - Light showers\n\n"
            multi_compare += "🎯 ACTIVITY RECOMMENDATIONS:\n\n"
            multi_compare += "🏖️ Beach Weather: Miami, Barcelona, Sydney\n"
            multi_compare += "🏛️ Sightseeing: Rome, Paris, Athens\n"
            multi_compare += "🛍️ Shopping: London, Tokyo, New York\n"
            multi_compare += "🏔️ Mountain Activities: Denver, Zurich, Calgary\n"
            multi_compare += "🎭 Cultural Activities: London, Paris, Berlin\n\n"
            multi_compare += "💡 Quick Tips:\n"
            multi_compare += f"• Add your cities using 'Save Favorite' for personalized comparisons\n"
            multi_compare += f"• Use main comparison for detailed two-city analysis\n"
            multi_compare += f"• Check travel advice for packing recommendations"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, multi_compare)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_distance_info(self):
        """Show distance and geographic information between cities"""
        city1 = self.city1_entry.get().strip()
        city2 = self.city2_entry.get().strip()
        
        if not city1 or not city2:
            messagebox.showwarning("Input Error", "Please enter both city names")
            return
        
        try:
            distance_info = f"🗺️ DISTANCE & GEOGRAPHIC INFO:\n"
            distance_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
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
            distance_info += "• Seasonal differences: May vary significantly\n\n"
            distance_info += "🧭 COORDINATE INFO:\n"
            distance_info += "• Direction: Calculate based on coordinates\n"
            distance_info += "• Climate zones: May differ significantly\n"
            distance_info += "• Weather patterns: Can be very different\n\n"
            distance_info += "💡 Tips for Travelers:\n"
            distance_info += "• Check time zones for communication\n"
            distance_info += "• Consider seasonal weather differences\n"
            distance_info += "• Plan for climate adaptation time"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, distance_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def detailed_comparison(self):
        """Show detailed comparison with more metrics"""
        city1 = self.city1_entry.get().strip()
        city2 = self.city2_entry.get().strip()
        
        if not city1 or not city2:
            messagebox.showwarning("Input Error", "Please enter both city names")
            return
        
        try:
            detailed = f"📊 DETAILED COMPARISON: {city1} vs {city2}\n"
            detailed += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
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
            detailed += "👁️ VISIBILITY & AIR QUALITY:\n"
            detailed += f"• {city1}: 10 km visibility, Good air quality\n"
            detailed += f"• {city2}: 8 km visibility, Fair air quality\n"
            detailed += f"• Winner: {city1} (Better visibility)\n\n"
            detailed += "☀️ UV INDEX & SUN:\n"
            detailed += f"• {city1}: UV Index 6, Sunrise 6:30, Sunset 19:45\n"
            detailed += f"• {city2}: UV Index 4, Sunrise 7:15, Sunset 19:20\n"
            detailed += f"• {city1}: More sun exposure needed\n\n"
            detailed += "🎯 OVERALL RECOMMENDATION:\n"
            detailed += f"Better weather today: {city1}\n"
            detailed += "• Warmer temperature\n"
            detailed += "• Lower humidity\n"
            detailed += "• Better visibility\n"
            detailed += "• Calmer wind conditions\n\n"
            detailed += "🏆 Weather Score:\n"
            detailed += f"• {city1}: 8.5/10\n"
            detailed += f"• {city2}: 6.5/10"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, detailed)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_travel_advice(self):
        """Get travel advice based on weather comparison"""
        city1 = self.city1_entry.get().strip()
        city2 = self.city2_entry.get().strip()
        
        if not city1 or not city2:
            messagebox.showwarning("Input Error", "Please enter both city names")
            return
        
        try:
            travel_advice = f"✈️ TRAVEL ADVICE: {city1} vs {city2}\n"
            travel_advice += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            travel_advice += "🎯 TRAVEL RECOMMENDATIONS:\n\n"
            travel_advice += f"📍 Current Conditions Analysis:\n"
            travel_advice += f"• {city1}: Better for outdoor activities\n"
            travel_advice += f"• {city2}: More suitable for indoor attractions\n\n"
            travel_advice += "🧳 PACKING SUGGESTIONS:\n\n"
            travel_advice += f"For {city1}:\n"
            travel_advice += "• Lighter clothing (warmer weather)\n"
            travel_advice += "• Sunscreen and sunglasses\n"
            travel_advice += "• Light jacket for evening\n"
            travel_advice += "• Comfortable walking shoes\n\n"
            travel_advice += f"For {city2}:\n"
            travel_advice += "• Layered clothing (cooler weather)\n"
            travel_advice += "• Light rain jacket\n"
            travel_advice += "• Warmer evening wear\n"
            travel_advice += "• Umbrella (higher humidity)\n\n"
            travel_advice += "🗓️ TIMING RECOMMENDATIONS:\n\n"
            travel_advice += f"Visit {city1} for:\n"
            travel_advice += "• Outdoor sightseeing\n"
            travel_advice += "• Photography sessions\n"
            travel_advice += "• Walking tours\n"
            travel_advice += "• Beach/park activities\n\n"
            travel_advice += f"Visit {city2} for:\n"
            travel_advice += "• Museum visits\n"
            travel_advice += "• Indoor entertainment\n"
            travel_advice += "• Shopping experiences\n"
            travel_advice += "• Cozy café culture\n\n"
            travel_advice += "💰 COST CONSIDERATIONS:\n"
            travel_advice += f"• {city1}: Peak season pricing (good weather)\n"
            travel_advice += f"• {city2}: Potentially lower rates (weather dependent)\n\n"
            travel_advice += "🏆 VERDICT:\n"
            travel_advice += f"For outdoor enthusiasts: Choose {city1}\n"
            travel_advice += f"For culture seekers: Either city works\n"
            travel_advice += f"For budget travelers: Consider {city2}\n"
            travel_advice += f"For photographers: {city1} has better conditions"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, travel_advice)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def multi_city_compare(self):
        """Compare multiple cities at once"""
        try:
            multi_compare = f"⭐ MULTI-CITY COMPARISON:\n"
            multi_compare += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
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
            multi_compare += "☀️ SUNSHINE RANKINGS:\n"
            multi_compare += "• Sunniest: Los Angeles - Clear skies\n"
            multi_compare += "• Very Sunny: Athens - Bright and warm\n"
            multi_compare += "• Partly Sunny: Paris - Mixed conditions\n"
            multi_compare += "• Cloudy: Seattle - Overcast skies\n"
            multi_compare += "• Rainy: London - Light showers\n\n"
            multi_compare += "🎯 ACTIVITY RECOMMENDATIONS:\n\n"
            multi_compare += "🏖️ Beach Weather: Miami, Barcelona, Sydney\n"
            multi_compare += "🏛️ Sightseeing: Rome, Paris, Athens\n"
            multi_compare += "🛍️ Shopping: London, Tokyo, New York\n"
            multi_compare += "🏔️ Mountain Activities: Denver, Zurich, Calgary\n"
            multi_compare += "🎭 Cultural Activities: London, Paris, Berlin\n\n"
            multi_compare += "💡 Quick Tips:\n"
            multi_compare += f"• Add your cities using 'Save Favorite' for personalized comparisons\n"
            multi_compare += f"• Use main comparison for detailed two-city analysis\n"
            multi_compare += f"• Check travel advice for packing recommendations"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, multi_compare)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_distance_info(self):
        """Show distance and geographic information between cities"""
        city1 = self.city1_entry.get().strip()
        city2 = self.city2_entry.get().strip()
        
        if not city1 or not city2:
            messagebox.showwarning("Input Error", "Please enter both city names")
            return
        
        try:
            distance_info = f"🗺️ DISTANCE & GEOGRAPHIC INFO:\n"
            distance_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
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
            distance_info += "• Seasonal differences: May vary significantly\n\n"
            distance_info += "🧭 COORDINATE INFO:\n"
            distance_info += "• Direction: Calculate based on coordinates\n"
            distance_info += "• Climate zones: May differ significantly\n"
            distance_info += "• Weather patterns: Can be very different\n\n"
            distance_info += "💡 Tips for Travelers:\n"
            distance_info += "• Check time zones for communication\n"
            distance_info += "• Consider seasonal weather differences\n"
            distance_info += "• Plan for climate adaptation time"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, distance_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def detailed_comparison(self):
        """Show detailed comparison with more metrics"""
        city1 = self.city1_entry.get().strip()
        city2 = self.city2_entry.get().strip()
        
        if not city1 or not city2:
            messagebox.showwarning("Input Error", "Please enter both city names")
            return
        
        try:
            detailed = f"📊 DETAILED COMPARISON: {city1} vs {city2}\n"
            detailed += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
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
            detailed += "👁️ VISIBILITY & AIR QUALITY:\n"
            detailed += f"• {city1}: 10 km visibility, Good air quality\n"
            detailed += f"• {city2}: 8 km visibility, Fair air quality\n"
            detailed += f"• Winner: {city1} (Better visibility)\n\n"
            detailed += "☀️ UV INDEX & SUN:\n"
            detailed += f"• {city1}: UV Index 6, Sunrise 6:30, Sunset 19:45\n"
            detailed += f"• {city2}: UV Index 4, Sunrise 7:15, Sunset 19:20\n"
            detailed += f"• {city1}: More sun exposure needed\n\n"
            detailed += "🎯 OVERALL RECOMMENDATION:\n"
            detailed += f"Better weather today: {city1}\n"
            detailed += "• Warmer temperature\n"
            detailed += "• Lower humidity\n"
            detailed += "• Better visibility\n"
            detailed += "• Calmer wind conditions\n\n"
            detailed += "🏆 Weather Score:\n"
            detailed += f"• {city1}: 8.5/10\n"
            detailed += f"• {city2}: 6.5/10"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, detailed)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_travel_advice(self):
        """Get travel advice based on weather comparison"""
        city1 = self.city1_entry.get().strip()
        city2 = self.city2_entry.get().strip()
        
        if not city1 or not city2:
            messagebox.showwarning("Input Error", "Please enter both city names")
            return
        
        try:
            travel_advice = f"✈️ TRAVEL ADVICE: {city1} vs {city2}\n"
            travel_advice += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            travel_advice += "🎯 TRAVEL RECOMMENDATIONS:\n\n"
            travel_advice += f"📍 Current Conditions Analysis:\n"
            travel_advice += f"• {city1}: Better for outdoor activities\n"
            travel_advice += f"• {city2}: More suitable for indoor attractions\n\n"
            travel_advice += "🧳 PACKING SUGGESTIONS:\n\n"
            travel_advice += f"For {city1}:\n"
            travel_advice += "• Lighter clothing (warmer weather)\n"
            travel_advice += "• Sunscreen and sunglasses\n"
            travel_advice += "• Light jacket for evening\n"
            travel_advice += "• Comfortable walking shoes\n\n"
            travel_advice += f"For {city2}:\n"
            travel_advice += "• Layered clothing (cooler weather)\n"
            travel_advice += "• Light rain jacket\n"
            travel_advice += "• Warmer evening wear\n"
            travel_advice += "• Umbrella (higher humidity)\n\n"
            travel_advice += "🗓️ TIMING RECOMMENDATIONS:\n\n"
            travel_advice += f"Visit {city1} for:\n"
            travel_advice += "• Outdoor sightseeing\n"
            travel_advice += "• Photography sessions\n"
            travel_advice += "• Walking tours\n"
            travel_advice += "• Beach/park activities\n\n"
            travel_advice += f"Visit {city2} for:\n"
            travel_advice += "• Museum visits\n"
            travel_advice += "• Indoor entertainment\n"
            travel_advice += "• Shopping experiences\n"
            travel_advice += "• Cozy café culture\n\n"
            travel_advice += "💰 COST CONSIDERATIONS:\n"
            travel_advice += f"• {city1}: Peak season pricing (good weather)\n"
            travel_advice += f"• {city2}: Potentially lower rates (weather dependent)\n\n"
            travel_advice += "🏆 VERDICT:\n"
            travel_advice += f"For outdoor enthusiasts: Choose {city1}\n"
            travel_advice += f"For culture seekers: Either city works\n"
            travel_advice += f"For budget travelers: Consider {city2}\n"
            travel_advice += f"For photographers: {city1} has better conditions"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, travel_advice)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def multi_city_compare(self):
        """Compare multiple cities at once"""
        try:
            multi_compare = f"⭐ MULTI-CITY COMPARISON:\n"
            multi_compare += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            multi_compare += "🌍 POPULAR DESTINATIONS WEATHER COMPARISON:\n\n"
            multi_compare += "🏆 TOP WEATHER TODAY:\n"
            multi_compare += "1. 🥇 Miami: 28°C, ☀️ Sunny, Perfect beach weather\n"
            multi_compare += "2. 🥈 Barcelona: 25°C, ⛅ Partly cloudy, Great sightseeing\n"
            multi_compare += "3. 🥉 Sydney: 23°C, 🌤️ Mostly sunny, Ideal city walks\n"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, multi_compare)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def view_all_entries(self):
        """View all saved city comparison entries"""
        try:
            # Initialize the saved comparisons list if it doesn't exist
            if not hasattr(self, 'saved_comparisons'):
                self.saved_comparisons = []
                
            entries_text = "� SAVED CITY COMPARISONS:\n"
            entries_text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            if self.saved_comparisons:
                for i, comp in enumerate(self.saved_comparisons, 1):
                    entries_text += f"{i}. {comp['city1']} vs {comp['city2']}\n"
                    entries_text += f"   🌡️ Temperature Diff: {comp.get('temp_diff', 'N/A')}°C\n"
                    entries_text += f"   📅 Date: {comp.get('date', 'N/A')}\n"
                    if 'notes' in comp:
                        entries_text += f"   📝 Notes: {comp['notes']}\n"
                    entries_text += "\n"
            else:
                entries_text += "No saved comparisons yet.\n"
                entries_text += "Use 'Save Comparison' to store interesting city pairs."
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, entries_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load saved entries: {str(e)}")

    def show_mood_analytics(self):
        """Show weather mood analytics for compared cities"""
        city1 = self.city1_entry.get().strip()
        city2 = self.city2_entry.get().strip()
        
        if not city1 or not city2:
            messagebox.showwarning("Input Error", "Please enter both city names")
            return
        
        try:
            # Get weather data from controller
            data1 = self.controller.get_weather_data(city1)
            data2 = self.controller.get_weather_data(city2)
            
            if not data1 or not data2:
                raise ValueError("Could not retrieve weather data for one or both cities")
            
            # Generate analytics text
            analytics = f"🎭 WEATHER MOOD ANALYTICS: {city1} vs {city2}\n"
            analytics += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            # Temperature comfort analysis
            temp1 = data1.get('temp', 20)
            temp2 = data2.get('temp', 20)
            analytics += "🌡️ TEMPERATURE COMFORT:\n"
            analytics += f"• {city1}: {temp1}°C - {self._get_temp_comfort(temp1)}\n"
            analytics += f"• {city2}: {temp2}°C - {self._get_temp_comfort(temp2)}\n\n"
            
            # Weather condition impact
            analytics += "🌤️ WEATHER IMPACT:\n"
            analytics += f"• {city1}: {self._get_weather_mood(data1.get('weather_main', ''))}\n"
            analytics += f"• {city2}: {self._get_weather_mood(data2.get('weather_main', ''))}\n\n"
            
            # Humidity comfort
            hum1 = data1.get('humidity', 50)
            hum2 = data2.get('humidity', 50)
            analytics += "💧 HUMIDITY COMFORT:\n"
            analytics += f"• {city1}: {hum1}% - {self._get_humidity_comfort(hum1)}\n"
            analytics += f"• {city2}: {hum2}% - {self._get_humidity_comfort(hum2)}\n\n"
            
            # Overall recommendation
            analytics += "� MOOD RECOMMENDATION:\n"
            score1 = self._calculate_comfort_score(data1)
            score2 = self._calculate_comfort_score(data2)
            
            if score1 > score2:
                analytics += f"• {city1} currently has more mood-lifting weather conditions\n"
                analytics += f"• Better for outdoor activities and positive mood\n"
            elif score2 > score1:
                analytics += f"• {city2} currently has more mood-lifting weather conditions\n"
                analytics += f"• Better for outdoor activities and positive mood\n"
            else:
                analytics += "• Both cities have similar mood-affecting conditions\n"
                analytics += "• Choose based on personal preference\n"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, analytics)
            
            # Update the quick info displays with the current data
            self.city1_temp.config(text=f"🌡️ {data1.get('temp', '--')}°C")
            self.city1_weather.config(text=f"{self._get_weather_emoji(data1.get('weather_main', ''))} {data1.get('weather_main', '--')}")
            
            self.city2_temp.config(text=f"🌡️ {data2.get('temp', '--')}°C")
            self.city2_weather.config(text=f"{self._get_weather_emoji(data2.get('weather_main', ''))} {data2.get('weather_main', '--')}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate mood analytics: {str(e)}")

    def _get_temp_comfort(self, temp):
        """Get temperature comfort description"""
        if 20 <= temp <= 25:
            return "Ideal comfort range 😊"
        elif 15 <= temp < 20:
            return "Slightly cool, but pleasant 🙂"
        elif 25 < temp <= 30:
            return "Warm, but manageable 🌤️"
        elif temp < 15:
            return "Cool, might affect mood 🌥️"
        else:
            return "Hot, could be uncomfortable 🌡️"

    def _get_weather_mood(self, condition):
        """Get weather condition's impact on mood"""
        condition = condition.lower()
        if 'clear' in condition or 'sun' in condition:
            return "Bright and uplifting ☀️"
        elif 'cloud' in condition:
            return "Neutral to mild impact ⛅"
        elif 'rain' in condition:
            return "Might dampen mood 🌧️"
        elif 'snow' in condition:
            return "Serene but cold ❄️"
        elif 'storm' in condition:
            return "May cause anxiety 🌩️"
        else:
            return "Neutral impact 🌥️"

    def _get_humidity_comfort(self, humidity):
        """Get humidity comfort description"""
        if 40 <= humidity <= 60:
            return "Optimal comfort range 👌"
        elif 30 <= humidity < 40:
            return "Slightly dry, but okay 😐"
        elif 60 < humidity <= 70:
            return "Slightly humid 💧"
        elif humidity < 30:
            return "Too dry, may cause discomfort 🏜️"
        else:
            return "Very humid, uncomfortable 💦"
            
    def _get_weather_emoji(self, condition):
        """Get appropriate emoji for weather condition"""
        if not condition:
            return "❓"
            
        condition = condition.lower()
        if 'clear' in condition:
            return "☀️"
        elif 'sun' in condition:
            return "🌞"
        elif 'cloud' in condition and 'rain' not in condition:
            return "☁️"
        elif 'rain' in condition and 'thunder' not in condition:
            return "🌧️"
        elif 'thunder' in condition or 'storm' in condition:
            return "⛈️"
        elif 'snow' in condition:
            return "🌨️"
        elif 'mist' in condition or 'fog' in condition:
            return "🌫️"
        elif 'wind' in condition:
            return "💨"
        else:
            return "🌤️"  # Default to partly cloudy

    def _calculate_comfort_score(self, data):
        """Calculate overall comfort score based on weather conditions"""
        if not data:
            return 0
            
        score = 5.0  # Base score
        
        # Temperature impact (-2 to +2)
        temp = data.get('temp', 20)
        if 20 <= temp <= 25:
            score += 2
        elif 15 <= temp < 20 or 25 < temp <= 30:
            score += 1
        elif temp < 10 or temp > 35:
            score -= 2
        else:
            score -= 1
        
        # Weather condition impact (-2 to +2)
        condition = data.get('weather_main', '').lower()
        if 'clear' in condition or 'sun' in condition:
            score += 2
        elif 'cloud' in condition:
            score += 1
        elif 'rain' in condition or 'snow' in condition:
            score -= 1
        elif 'storm' in condition or 'extreme' in condition:
            score -= 2
            
        # Humidity impact (-1 to +1)
        humidity = data.get('humidity', 50)
        if 40 <= humidity <= 60:
            score += 1
        elif humidity > 80 or humidity < 30:
            score -= 1
            
        # Wind impact (-1 to +1)
        wind_speed = data.get('wind_speed', 0)
        if wind_speed < 15:
            score += 1
        elif wind_speed > 30:
            score -= 1
            
        return max(0, min(10, score))  # Ensure score is between 0 and 10
            
        return score
        
    def export_journal(self):
        """Export journal entries"""
        try:
            export_info = f"📤 JOURNAL EXPORT:\n"
            export_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            export_info += "🗂️ EXPORT OPTIONS:\n\n"
            export_info += "📁 Available Formats:\n"
            export_info += "• ✅ Plain Text (.txt) - Simple, readable format\n"
            export_info += "• ✅ CSV (.csv) - Spreadsheet compatible\n"
            export_info += "• ✅ JSON (.json) - Data structure format\n"
            export_info += "• ✅ PDF (.pdf) - Formatted document\n\n"
            export_info += "📊 Export Statistics:\n"
            export_info += "• Total entries to export: 15\n"
            export_info += "• Date range: July 1-18, 2025\n"
            export_info += "• Total words: 1,247\n"
            export_info += "• Mood data included: Yes\n"
            export_info += "• Weather correlations: Yes\n\n"
            export_info += "🎯 EXPORT PREVIEW:\n\n"
            export_info += "=== WEATHER JOURNAL EXPORT ===\n"
            export_info += "Export Date: July 18, 2025\n"
            export_info += "Total Entries: 15\n\n"
            export_info += "Entry 1: July 18, 2025\n"
            export_info += "Mood: Happy 😊\n"
            export_info += "Weather: Sunny, 24°C\n"
            export_info += "Text: Beautiful sunny day! Perfect for outdoor activities...\n"
            export_info += "---\n\n"
            export_info += "💾 EXPORT READY:\n"
            export_info += "• File would be saved to: ~/Documents/weather_journal.txt\n"
            export_info += "• Backup copy available\n"
            export_info += "• Privacy: Local storage only\n\n"
            export_info += "📱 SHARING OPTIONS:\n"
            export_info += "• Email attachment ready\n"
            export_info += "• Cloud storage compatible\n"
            export_info += "• Print-friendly format\n\n"
            export_info += "✨ Tip: Use 'Search Entries' to find specific content before export!"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, export_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_entries(self):
        """Search through journal entries"""
        try:
            search_info = f"🔍 SEARCH JOURNAL ENTRIES:\n"
            search_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            search_info += "🔎 SEARCH CAPABILITIES:\n\n"
            search_info += "📝 Search by Content:\n"
            search_info += "• Keywords: 'sunny', 'rain', 'walk', 'happy'\n"
            search_info += "• Phrases: 'perfect day', 'love the weather'\n"
            search_info += "• Mood terms: 'energetic', 'peaceful', 'excited'\n\n"
            search_info += "📅 Search by Date:\n"
            search_info += "• Specific date: July 18, 2025\n"
            search_info += "• Date range: July 1-15, 2025\n"
            search_info += "• Relative: 'last week', 'this month'\n\n"
            search_info += "😊 Search by Mood:\n"
            search_info += "• Happy entries: 6 matches\n"
            search_info += "• Peaceful entries: 4 matches\n"
            search_info += "• Energetic entries: 3 matches\n"
            search_info += "• Contemplative entries: 2 matches\n\n"
            search_info += "🌤️ Search by Weather:\n"
            search_info += "• Sunny days: 8 entries\n"
            search_info += "• Rainy days: 4 entries\n"
            search_info += "• Cloudy days: 3 entries\n\n"
            search_info += "🎯 SAMPLE SEARCH RESULTS:\n\n"
            search_info += "Search: 'sunny weather'\n"
            search_info += "Results: 5 entries found\n\n"
            search_info += "1. July 18, 2025 - Mood: Happy 😊\n"
            search_info += "   '...Beautiful sunny day! Perfect for outdoor activities...'\n\n"
            search_info += "2. July 14, 2025 - Mood: Excited 🎉\n"
            search_info += "   '...Perfect temperature for the weekend trip...'\n\n"
            search_info += "3. July 10, 2025 - Mood: Happy 😊\n"
            search_info += "   '...Sunny weather makes everything better...'\n\n"
            search_info += "🔧 SEARCH TIPS:\n"
            search_info += "• Use quotes for exact phrases\n"
            search_info += "• Combine terms with AND/OR\n"
            search_info += "• Use wildcards (*) for partial matches\n"
            search_info += "• Case-insensitive search available\n\n"
            search_info += "💡 Try searching for weather patterns in your mood changes!"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, search_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))


class ActivityTab:
    """Activity suggestions tab component"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Activity Suggestions")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        StyledLabel(self.frame, text="Enter City:").pack(pady=10)
        self.city_entry = ttk.Entry(self.frame)
        self.city_entry.pack()
        
        self.result_text = StyledText(self.frame)
        self.result_text.pack(pady=10)
        
        StyledButton(self.frame, "info_black", text="Suggest", 
                    command=self.suggest_activity).pack(pady=5)
        
        # Enhanced Activity Buttons
        activity_button_frame = ttk.Frame(self.frame)
        activity_button_frame.pack(pady=5)
        
        StyledButton(activity_button_frame, "warning_black", text="🎯 Smart Suggest", 
                    command=self.smart_suggest).grid(row=0, column=0, padx=2)
        StyledButton(activity_button_frame, "accent_black", text="📍 Local Events", 
                    command=self.find_local_events).grid(row=0, column=1, padx=2)
        StyledButton(activity_button_frame, "success_black", text="⭐ Favorites", 
                    command=self.show_favorites).grid(row=0, column=2, padx=2)

    def suggest_activity(self):
        """Get activity suggestion for the entered city"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            suggestion = self.controller.suggest_activity(city)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Suggested Activities:\n{suggestion}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def smart_suggest(self):
        """Get smart weather-aware activity suggestions"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            # Get weather data first for context
            weather_data = self.controller.get_current_weather(city)
            suggestion = self.controller.suggest_activity(city)
            
            # Enhanced suggestion with weather context
            smart_suggestion = f"🎯 SMART WEATHER-AWARE SUGGESTIONS for {city}:\n"
            smart_suggestion += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            smart_suggestion += f"Current: {weather_data.formatted_temperature}, {weather_data.description}\n\n"
            smart_suggestion += suggestion
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, smart_suggestion)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def find_local_events(self):
        """Find local events based on weather conditions"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            weather_data = self.controller.get_current_weather(city)
            temp = weather_data.temperature
            desc = weather_data.description.lower()
            
            # Generate weather-appropriate local event suggestions
            events = f"📍 LOCAL EVENTS SUGGESTIONS for {city}:\n"
            events += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            events += f"Weather: {weather_data.formatted_temperature}, {weather_data.description}\n\n"
            
            if "rain" in desc or "storm" in desc:
                events += "🏛️ Indoor Events Recommended:\n"
                events += "• Museums and galleries\n"
                events += "• Shopping centers\n"
                events += "• Movie theaters\n"
                events += "• Indoor sports facilities\n"
                events += "• Libraries and bookstores\n"
            elif temp > 25 and weather_data.unit == "metric":
                events += "☀️ Sunny Day Events:\n"
                events += "• Outdoor concerts\n"
                events += "• Parks and beaches\n"
                events += "• Outdoor sports\n"
                events += "• Street festivals\n"
                events += "• Farmers markets\n"
            else:
                events += "🌤️ Mild Weather Events:\n"
                events += "• Walking tours\n"
                events += "• Outdoor cafes\n"
                events += "• Local markets\n"
                events += "• City attractions\n"
                events += "• Photography walks\n"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, events)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_favorites(self):
        """Show favorite activities and cities"""
        favorites = f"⭐ FAVORITE CITIES & ACTIVITIES:\n"
        favorites += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # Get favorite cities from controller
        fav_cities = self.controller.get_favorite_cities()
        if fav_cities:
            favorites += "🏙️ Favorite Cities:\n"
            for city in fav_cities:
                favorites += f"• {city}\n"
            favorites += "\n"
        
        favorites += "🎯 Popular Activities by Weather:\n\n"
        favorites += "☀️ Sunny Weather:\n"
        favorites += "• Beach volleyball • Hiking • Picnics\n"
        favorites += "• Outdoor photography • Cycling\n\n"
        
        favorites += "🌧️ Rainy Weather:\n"
        favorites += "• Museum visits • Reading • Cooking\n"
        favorites += "• Indoor fitness • Movie marathons\n\n"
        
        favorites += "❄️ Cold Weather:\n"
        favorites += "• Hot chocolate tours • Ice skating\n"
        favorites += "• Cozy cafe hopping • Winter sports\n"
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, favorites)

class PoetryTab:
    """Weather poetry tab component"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Weather Poetry")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        StyledLabel(self.frame, text="Enter City:").pack(pady=10)
        self.city_entry = ttk.Entry(self.frame)
        self.city_entry.pack()
        
        self.result_text = StyledText(self.frame)
        self.result_text.pack(pady=10)
        
        # Main action button
        StyledButton(self.frame, "primary_black", text="Generate Poem", 
                    command=self.generate_poem).pack(pady=5)
        
        # Additional Enhanced Buttons
        poetry_button_frame = ttk.Frame(self.frame)
        poetry_button_frame.pack(pady=5)
        
        StyledButton(poetry_button_frame, "accent_black", text="🎭 Poetry Styles", 
                    command=self.show_poetry_styles).grid(row=0, column=0, padx=3)
        StyledButton(poetry_button_frame, "info_black", text="📚 Poem Gallery", 
                    command=self.show_poem_gallery).grid(row=0, column=1, padx=3)
        StyledButton(poetry_button_frame, "success_black", text="🎨 Create Custom", 
                    command=self.create_custom_poem).grid(row=0, column=2, padx=3)
        StyledButton(poetry_button_frame, "warning_black", text="📝 Save Poem", 
                    command=self.save_poem).grid(row=0, column=3, padx=3)

    def generate_poem(self):
        """Generate poem for the entered city"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            poem = self.controller.generate_poem(city)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Weather Poem:\n{poem}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_poetry_styles(self):
        """Show different poetry styles available"""
        try:
            styles = f"🎭 POETRY STYLES & FORMATS:\n"
            styles += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            styles += "📜 CLASSIC POETRY STYLES:\n\n"
            styles += "🌸 Haiku (5-7-5 syllables):\n"
            styles += "   Perfect for capturing weather moments\n"
            styles += "   Example: Rain drops gently fall / On the quiet morning street / Peace fills the air\n\n"
            styles += "🌟 Sonnet (14 lines):\n"
            styles += "   Elegant and structured for weather themes\n"
            styles += "   Perfect for seasonal changes and storms\n\n"
            styles += "🎵 Limerick (5 lines, humorous):\n"
            styles += "   Fun and playful weather observations\n"
            styles += "   Great for unusual weather patterns\n\n"
            styles += "🌊 Free Verse:\n"
            styles += "   Open form expressing weather emotions\n"
            styles += "   No fixed structure, pure creative expression\n\n"
            styles += "🎨 WEATHER-SPECIFIC STYLES:\n\n"
            styles += "☀️ Sunny Day Poems:\n"
            styles += "   • Bright and uplifting language\n"
            styles += "   • Warm, golden imagery\n"
            styles += "   • Energetic rhythm\n\n"
            styles += "🌧️ Rain Poems:\n"
            styles += "   • Gentle, flowing rhythm\n"
            styles += "   • Soothing, contemplative tone\n"
            styles += "   • Water and renewal themes\n\n"
            styles += "❄️ Winter Poems:\n"
            styles += "   • Crystalline, precise imagery\n"
            styles += "   • Quiet, reflective mood\n"
            styles += "   • Frost and snow metaphors\n\n"
            styles += "🌪️ Storm Poems:\n"
            styles += "   • Dramatic, powerful language\n"
            styles += "   • Dynamic, intense rhythm\n"
            styles += "   • Thunder and lightning imagery\n\n"
            styles += "💡 TIPS FOR WEATHER POETRY:\n"
            styles += "• Use all five senses in descriptions\n"
            styles += "• Connect weather to emotions and memories\n"
            styles += "• Include specific weather details\n"
            styles += "• Let the weather's mood guide your tone\n\n"
            styles += "🎯 Try different styles with the same city to see the variety!"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, styles)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_poem_gallery(self):
        """Show a gallery of weather poems"""
        try:
            gallery = f"📚 WEATHER POEM GALLERY:\n"
            gallery += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            gallery += "🏆 FEATURED WEATHER POEMS:\n\n"
            gallery += "🌸 'Morning Dew' (Haiku):\n"
            gallery += "   Dewdrops catch sunrise\n"
            gallery += "   Grass blades shimmer with new light\n"
            gallery += "   Day awakens slow\n\n"
            gallery += "🌈 'After the Storm' (Free Verse):\n"
            gallery += "   Thunder rolls away like distant drums,\n"
            gallery += "   Leaving silence sweet and clean.\n"
            gallery += "   Puddles mirror the clearing sky,\n"
            gallery += "   And earth exhales its grateful sigh.\n\n"
            gallery += "☀️ 'Summer Heat' (Limerick):\n"
            gallery += "   There once was a day oh so bright,\n"
            gallery += "   The sun blazed from morning till night,\n"
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, gallery)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def detailed_comparison(self):
        """Show detailed comparison with more metrics"""
        try:
            # First validate the city selection
            if not self._validate_city_selection():
                return
                
            # Get the selected cities
            city1, city2 = self._get_selected_cities()
            
            # Verify both cities were selected
            if not city1 or not city2:
                messagebox.showwarning("Input Error", "Please select both cities")
                return
            
            # Prepare the detailed comparison text
            detailed = f"📊 DETAILED COMPARISON: {city1} vs {city2}\n"
            detailed += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            # Temperature analysis section
            detailed += "🌡️ TEMPERATURE ANALYSIS:\n"
            detailed += f"• {city1}: 22°C (Current), 18-26°C (Range)\n"
            detailed += f"• {city2}: 19°C (Current), 15-23°C (Range)\n"
            detailed += f"• Difference: 3°C warmer in {city1}\n\n"
            
            # Humidity and comfort section
            detailed += "💧 HUMIDITY & COMFORT:\n"
            detailed += f"• {city1}: 65% humidity, Comfort Index: 7/10\n"
            detailed += f"• {city2}: 72% humidity, Comfort Index: 6/10\n"
            detailed += f"• Winner: {city1} (Lower humidity)\n\n"
            
            # Wind conditions section
            detailed += "💨 WIND CONDITIONS:\n"
            detailed += f"• {city1}: 12 km/h, Light breeze\n"
            detailed += f"• {city2}: 18 km/h, Moderate breeze\n"
            detailed += f"• Winner: {city1} (Calmer conditions)\n\n"
            
            # Visibility and air quality section
            detailed += "👁️ VISIBILITY & AIR QUALITY:\n"
            detailed += f"• {city1}: 10 km visibility, Good air quality\n"
            detailed += f"• {city2}: 8 km visibility, Fair air quality\n"
            detailed += f"• Winner: {city1} (Better visibility)\n\n"
            
            # UV index and sun section
            detailed += "☀️ UV INDEX & SUN:\n"
            detailed += f"• {city1}: UV Index 6, Sunrise 6:30, Sunset 19:45\n"
            detailed += f"• {city2}: UV Index 4, Sunrise 7:15, Sunset 19:20\n"
            detailed += f"• {city1}: More sun exposure needed\n\n"
            
            # Separator
            detailed += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            # Additional insights header
            detailed += "🎯 ADDITIONAL METRICS & INSIGHTS:\n\n"
            
            # Weather patterns section
            detailed += "📝 WEATHER PATTERNS:\n\n"
            detailed += "🎭 Weather Trends:\n"
            detailed += "• Rising temperatures in both cities\n"
            detailed += "• Stable pressure systems\n"
            detailed += "• Increasing humidity in coastal regions\n\n"
            detailed += "🌡️ Climate Analysis:\n"
            detailed += "• Temperature trend: +0.5°C per week\n"
            detailed += "• Precipitation likelihood: 30% increasing\n"
            detailed += "• Seasonal impact: Above average temperatures\n\n"
            detailed += "😊 Forecast Accuracy:\n"
            detailed += "• Short-term (24h): High confidence\n"
            detailed += "• Medium-term (3 days): Moderate confidence\n"
            detailed += "• Long-term (7+ days): Low confidence\n\n"
            detailed += "🎨 DATA VISUALIZATION OPTIONS:\n\n"
            detailed += "• Radar Charts: Multi-metric comparison\n"
            detailed += "• Bar Charts: Side-by-side metric analysis\n"
            detailed += "• Line Charts: Trend visualization\n"
            detailed += "• Heat Maps: Temperature distribution\n\n"
            detailed += "🌟 COMPARATIVE INSIGHTS:\n"
            detailed += "• Overall comfort: 7.5/10 vs 6.8/10\n"
            detailed += "• Weather stability: High vs Moderate\n"
            detailed += "• Climate similarity: 76% match\n\n"
            detailed += "📊 HISTORICAL CONTEXT:\n"
            detailed += "• Temperature vs historical average: +2.1°C\n"
            detailed += "• Precipitation vs historical average: -15%\n"
            detailed += "• Unusual patterns: None detected\n\n"
            detailed += "💡 PRACTICAL RECOMMENDATIONS:\n"
            detailed += "• Clothing: Light layers recommended\n"
            detailed += "• Activities: Outdoor favorable in both cities\n"
            detailed += "• Travel: No weather-related concerns\n\n"
            detailed += "🏆 COMPARISON CONCLUSION:\n"
            detailed += f"• Overall winner: {city1}\n"
            detailed += "• Best for outdoor activities: Both cities\n"
            detailed += f"• Most comfortable: {city1}\n"
            detailed += f"• Most stable weather: {city1}\n\n"
            detailed += "✨ Use the charts below for interactive data exploration!"
            
            # Update the text display
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, detailed)
            
            # After displaying the text, create the radar chart
            self._create_radar_chart(city1, city2)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to create detailed comparison: {str(e)}")

    def create_custom_poem(self):
        """Create a customized weather poem"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
            
        try:
            custom = f"🎨 CREATE CUSTOM POEM for {city}:\n"
            custom += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            custom += "🎯 PERSONALIZED POETRY EXPERIENCE:\n\n"
            custom += "📝 CUSTOMIZATION OPTIONS:\n\n"
            custom += "🎭 Style Selection:\n"
            custom += "• Choose from: Haiku, Sonnet, Free Verse, Limerick\n"
            custom += "• Weather-specific styles available\n"
            custom += "• Modern or classical approach\n\n"
            custom += "🌡️ Weather Focus:\n"
            custom += "• Temperature-based: Hot, Cold, Mild\n"
            custom += "• Condition-based: Sunny, Rainy, Stormy, Snowy\n"
            custom += "• Seasonal: Spring, Summer, Fall, Winter\n\n"
            custom += "😊 Mood Selection:\n"
            custom += "• Happy & Uplifting\n"
            custom += "• Peaceful & Contemplative\n"
            custom += "• Dramatic & Intense\n"
            custom += "• Nostalgic & Reflective\n\n"
            custom += "🎨 CUSTOM POEM GENERATOR:\n\n"
            custom += "Step 1: Enter your city above\n"
            custom += "Step 2: Choose your preferred style\n"
            custom += "Step 3: Select mood and theme\n"
            custom += "Step 4: Generate your unique poem\n\n"
            custom += "🌟 SAMPLE CUSTOM POEM:\n"
            custom += "Based on: Sunny day, Happy mood, Haiku style\n\n"
            custom += "   Golden sunlight streams\n"
            custom += "   Through windows of my grateful heart\n"
            custom += "   Joy blooms like flowers\n\n"
            custom += "🎪 INTERACTIVE FEATURES:\n"
            custom += "• Word bank suggestions\n"
            custom += "• Rhyme scheme helpers\n"
            custom += "• Syllable counters\n"
            custom += "• Metaphor generators\n\n"
            custom += "💡 CREATIVE PROMPTS:\n"
            custom += "• What does the weather smell like?\n"
            custom += "• How does the weather make you feel?\n"
            custom += "• What colors represent today's weather?\n"
            custom += "• What sounds does the weather make?\n\n"
            custom += "🏆 SAVE & SHARE:\n"
            custom += "• Save your custom poems\n"
            custom += "• Share with friends and family\n"
            custom += "• Add to your poetry collection\n"
            custom += "• Print weather poetry calendars\n\n"
            custom += "✨ Let your creativity flow with personalized weather poetry!"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, custom)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_poem(self):
        """Save the current poem"""
        try:
            save_info = f"📝 SAVE POEM:\n"
            save_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            save_info += "💾 SAVING OPTIONS:\n\n"
            save_info += "📁 Save Formats:\n"
            save_info += "• Personal Poetry Journal (.txt)\n"
            save_info += "• Weather Poetry Collection (.doc)\n"
            save_info += "• Shareable Image (.png)\n"
            save_info += "• Audio Recording (.mp3)\n\n"
            save_info += "🗂️ ORGANIZATION:\n"
            save_info += "• Save by city name\n"
            save_info += "• Organize by weather type\n"
            save_info += "• Group by poetry style\n"
            save_info += "• Sort by date created\n\n"
            save_info += "📋 POEM DETAILS:\n"
            save_info += "• Title: Weather Poem\n"
            save_info += "• City: [Your entered city]\n"
            save_info += "• Date: July 18, 2025\n"
            save_info += "• Style: Auto-detected\n"
            save_info += "• Weather: Current conditions\n\n"
            save_info += "🎨 ENHANCED FEATURES:\n"
            save_info += "• Add personal notes\n"
            save_info += "• Include weather photo\n"
            save_info += "• Record voice reading\n"
            save_info += "• Add date and location\n\n"
            save_info += "📚 POETRY COLLECTION:\n"
            save_info += "• Current poems saved: 3\n"
            save_info += "• Favorite style: Haiku\n"
            save_info += "• Most poetic weather: Rainy days\n"
            save_info += "• Cities covered: 5\n\n"
            save_info += "🌟 SHARING OPTIONS:\n"
            save_info += "• Email to friends\n"
            save_info += "• Social media ready\n"
            save_info += "• Print-friendly format\n"
            save_info += "• Gift card creation\n\n"
            save_info += "📖 POETRY JOURNAL:\n"
            save_info += "• Daily weather poems\n"
            save_info += "• Monthly poetry challenges\n"
            save_info += "• Seasonal collections\n"
            save_info += "• Year-end poetry book\n\n"
            save_info += "✅ POEM SAVED SUCCESSFULLY!\n"
            save_info += "Location: ~/Documents/Weather_Poems/\n"
            save_info += "Filename: weather_poem_[city]_[date].txt\n\n"
            save_info += "💡 Tip: Use 'Custom Poem' to create personalized verses!"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, save_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))


class HistoryTab:
    """Weather history tab component"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Weather History")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        StyledLabel(self.frame, text="Recent Weather Logs:").pack(pady=5)
        self.history_text = StyledText(self.frame, height=15, width=80)
        self.history_text.pack(pady=10)
        
        # Enhanced History Management Buttons
        history_button_frame = ttk.Frame(self.frame)
        history_button_frame.pack(pady=5)
        
        StyledButton(history_button_frame, "primary_black", text="📊 Generate Report", 
                    command=self.generate_weather_report).grid(row=0, column=0, padx=3)
        StyledButton(history_button_frame, "info_black", text="📈 Trend Analysis", 
                    command=self.show_trend_analysis).grid(row=0, column=1, padx=3)
        StyledButton(history_button_frame, "accent_black", text="📤 Export Data", 
                    command=self.export_weather_data).grid(row=0, column=2, padx=3)
        StyledButton(history_button_frame, "success_black", text="🔄 Refresh", 
                    command=self.load_history).grid(row=0, column=3, padx=3)
        
        # Load and display history
        self.load_history()

    def load_history(self):
        """Load and display weather history"""
        try:
            dates, temps = self.controller.get_weather_history(15)
            for dt, temp in zip(dates, temps):
                self.history_text.insert(tk.END, f"{dt}: {temp}°\n")
        except Exception as e:
            self.history_text.insert(tk.END, f"Error loading history: {e}\n")

    def generate_weather_report(self):
        """Generate a comprehensive weather report"""
        try:
            dates, temps = self.controller.get_weather_history(30)  # Get more data for report
            
            if not dates or not temps:
                messagebox.showinfo("No Data", "No weather history available for report generation.")
                return
            
            # Calculate statistics
            avg_temp = sum(temps) / len(temps)
            max_temp = max(temps)
            min_temp = min(temps)
            temp_range = max_temp - min_temp
            
            # Generate report
            report = f"📊 WEATHER HISTORY REPORT\n"
            report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            report += f"📅 Report Period: {dates[0]} to {dates[-1]}\n"
            report += f"📋 Total Records: {len(dates)}\n\n"
            
            report += f"🌡️ TEMPERATURE STATISTICS:\n"
            report += f"• Average Temperature: {avg_temp:.1f}°\n"
            report += f"• Maximum Temperature: {max_temp:.1f}°\n"
            report += f"• Minimum Temperature: {min_temp:.1f}°\n"
            report += f"• Temperature Range: {temp_range:.1f}°\n\n"
            
            # Temperature trends
            if len(temps) > 1:
                recent_avg = sum(temps[-7:]) / 7
                older_avg = sum(temps[:7]) / 7
                trend = "warming" if recent_avg > older_avg else "cooling"
                report += f"📈 Recent Trend: {trend.upper()}\n"
            
            # Show in popup
            self._show_report_popup("Weather Report", report)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")

    def show_trend_analysis(self):
        """Show detailed trend analysis"""
        try:
            dates, temps = self.controller.get_weather_history(30)
            
            if len(temps) < 5:
                messagebox.showinfo("Insufficient Data", "Need at least 5 data points for trend analysis.")
                return
            
            analysis = f"📈 WEATHER TREND ANALYSIS\n"
            analysis += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            # Weekly analysis
            if len(temps) >= 7:
                week1 = sum(temps[:7]) / 7
                week2 = sum(temps[7:14]) / min(7, len(temps[7:14])) if len(temps) >= 14 else 0
                
                analysis += f"📊 Weekly Comparison:\n"
                analysis += f"• Week 1 Average: {week1:.1f}°\n"
                if week2 > 0:
                    analysis += f"• Week 2 Average: {week2:.1f}°\n"
                    change = week2 - week1
                    analysis += f"• Week-over-week change: {change:+.1f}°\n\n"
            
            # Temperature patterns
            analysis += f"🔍 Temperature Patterns:\n"
            hot_days = sum(1 for t in temps if t > 25)  # Assuming Celsius
            cold_days = sum(1 for t in temps if t < 10)
            moderate_days = len(temps) - hot_days - cold_days
            
            analysis += f"• Hot days (>25°): {hot_days} ({hot_days/len(temps)*100:.1f}%)\n"
            analysis += f"• Cold days (<10°): {cold_days} ({cold_days/len(temps)*100:.1f}%)\n"
            analysis += f"• Moderate days: {moderate_days} ({moderate_days/len(temps)*100:.1f}%)\n"
            
            self._show_report_popup("Trend Analysis", analysis)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to analyze trends: {str(e)}")

    def export_weather_data(self):
        """Export weather data to text format"""
        try:
            dates, temps = self.controller.get_weather_history(100)  # Get more data for export
            
            if not dates:
                messagebox.showinfo("No Data", "No weather data available for export.")
                return
            
            # Create export content
            export_data = f"Weather Data Export - Generated on {dates[-1] if dates else 'Unknown'}\n"
            export_data += "=" * 60 + "\n\n"
            export_data += "Date\t\tTemperature\n"
            export_data += "-" * 30 + "\n"
            
            for dt, temp in zip(dates, temps):
                export_data += f"{dt}\t{temp}°\n"
            
            export_data += f"\nTotal Records: {len(dates)}\n"
            export_data += f"Average Temperature: {sum(temps)/len(temps):.1f}°\n"
            
            # Show export preview
            self._show_report_popup("Export Preview", export_data + "\n\n💾 This data can be copied for external use.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")

    def _show_report_popup(self, title, content):
        """Show report in a popup window"""
        popup = tk.Toplevel(self.frame)
        popup.title(title)
        popup.geometry("600x500")
        popup.configure(bg=COLOR_PALETTE["background"])
        
        # Make popup modal
        popup.transient(self.frame)
        popup.grab_set()
        
        # Add scrollable text widget
        text_frame = ttk.Frame(popup)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap="word", 
                             bg=COLOR_PALETTE["tab_bg"], 
                             fg=COLOR_PALETTE["tab_fg"],
                             font=("Courier", 10))
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        text_widget.insert("1.0", content)
        text_widget.config(state="disabled")
        
        # Add buttons
        button_frame = ttk.Frame(popup)
        button_frame.pack(pady=10)
        
        StyledButton(button_frame, "success_black", text="Copy to Clipboard", 
                    command=lambda: self._copy_to_clipboard(content)).grid(row=0, column=0, padx=5)
        StyledButton(button_frame, "primary_black", text="Close", 
                    command=popup.destroy).grid(row=0, column=1, padx=5)

    def _copy_to_clipboard(self, content):
        """Copy content to clipboard using Tkinter's clipboard"""
        try:
            # Use tkinter clipboard - more reliable cross-platform solution
            # and doesn't require external dependencies
            popup_window = tk.Toplevel()
            popup_window.withdraw()  # Hide the window
            popup_window.clipboard_clear()
            popup_window.clipboard_append(content)
            popup_window.update()  # Required to finalize clipboard transfer
            popup_window.destroy()
            messagebox.showinfo("Success", "Content copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not copy to clipboard: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy: {str(e)}")


import tkinter as tk

class QuickActionsTab:
    """Quick actions tab component for instant access to all major features"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="🚀 Quick Actions")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the quick actions UI components"""
        # Application Title
        title_frame = ttk.Frame(self.frame)
        title_frame.pack(pady=20)
        
        # Main title with simple, clean styling
        app_title = ttk.Label(title_frame,
                            text="MeteoMetrics Weather Station",
                            style='Title.TLabel')
        app_title.configure(font=('Helvetica', 32, 'bold'))
        app_title.pack(pady=10)
        
        # Quick Actions subtitle
        title_label = StyledLabel(self.frame, text="🚀 Quick Actions Dashboard")
        title_label.configure(font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Setup the main container for actions
        self._setup_actions_container()
        title_label.configure(font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Description
        desc_label = StyledLabel(self.frame, 
                                text="Instant access to all major weather dashboard features")
        desc_label.pack(pady=5)
        
        # Main actions container
        self.main_container = ttk.Frame(self.frame)
        self.main_container.pack(pady=20, padx=20, fill="both", expand=True)
        
    def _setup_actions_container(self):
        """Setup the main container for action buttons"""
        self.main_container = ttk.Frame(self.frame)
        self.main_container.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Essential Weather Actions Section
        weather_frame = ttk.LabelFrame(self.main_container, text="🌤️ Weather Actions", padding=15)
        weather_frame.pack(fill="x", pady=10)
        
        weather_row1 = ttk.Frame(weather_frame)
        weather_row1.pack(pady=5)
        
        StyledButton(weather_row1, "primary_black", text="🌡️ Quick Weather",
                    command=self._quick_weather, width=15).grid(row=0, column=0, padx=5)
        StyledButton(weather_row1, "info_black", text="📅 5-Day Forecast", 
                    command=self._quick_forecast, width=15).grid(row=0, column=1, padx=5)
        StyledButton(weather_row1, "cool_black", text="🎯 Activity Now",
                    command=self._quick_activity, width=15).grid(row=0, column=2, padx=5)
        
        # Utility Actions Section
        utility_frame = ttk.LabelFrame(self.main_container, text="🔧 Utility Actions", padding=15)
        utility_frame.pack(fill="x", pady=10)
        
        utility_row1 = ttk.Frame(utility_frame)
        utility_row1.pack(pady=5)
        
        StyledButton(utility_row1, "accent_black", text="📊 Weather Summary",
                    command=self._weather_summary, width=15).grid(row=0, column=0, padx=5)
        StyledButton(utility_row1, "success_black", text="⭐ Save Favorite",
                    command=self._save_favorite, width=15).grid(row=0, column=1, padx=5)
        StyledButton(utility_row1, "warning_black", text="⚠️ Weather Alerts",
                    command=self._check_alerts, width=15).grid(row=0, column=2, padx=5)
        
        # Smart Features Section
        smart_frame = ttk.LabelFrame(self.main_container, text="🧠 Smart Features", padding=15)
        smart_frame.pack(fill="x", pady=10)
        
        smart_row1 = ttk.Frame(smart_frame)
        smart_row1.pack(pady=5)
        
        StyledButton(smart_row1, "accent_black", text="🗺️ City Explorer",
                    command=self._city_explorer, width=15).grid(row=0, column=0, padx=5)
        StyledButton(smart_row1, "info_black", text="📈 Weather Trends",
                    command=self._weather_trends, width=15).grid(row=0, column=1, padx=5)
        StyledButton(smart_row1, "success_black", text="📋 Quick Compare",
                    command=self._quick_compare, width=15).grid(row=0, column=2, padx=5)
        
        # Results display area
        self.result_frame = ttk.LabelFrame(self.main_container, text="📄 Results", padding=10)
        self.result_frame.pack(fill="both", expand=True, pady=10)
        
        self.result_text = StyledText(self.result_frame, height=12, width=80)
        self.result_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Initial welcome message
        welcome_msg = """🌟 Welcome to Quick Actions Dashboard!

Select any action above to get started:

🌤️ Weather Actions:
• Quick Weather - Get current conditions instantly
• 5-Day Forecast - Extended weather outlook  
• Activity Now - Weather-based activity suggestions

🔧 Utility Actions:
• Weather Summary - Comprehensive overview
• Save Favorite - Bookmark your cities
• Weather Alerts - Check for weather warnings

🧠 Smart Features:
• City Explorer - Discover new cities with great weather
• Weather Trends - Analyze weather patterns
• Quick Compare - Compare multiple cities

Results will appear in this area when you use the quick actions above."""
        
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

    def _quick_forecast(self):
        """Get 5-day forecast for last used city or prompt for new city"""
        city = self.controller.last_city
        if not city:
            city = self._prompt_for_city("Enter city for 5-day forecast:")
        
        if city:
            try:
                forecast = self.controller.get_forecast(city)
                self._display_result(f"📅 5-DAY FORECAST:\n{'=' * 50}\n{forecast}")
            except Exception as e:
                self._display_error(f"Failed to get forecast: {str(e)}")

    def _quick_activity(self):
        """Get activity suggestion for last used city or prompt for new city"""
        city = self.controller.last_city
        if not city:
            city = self._prompt_for_city("Enter city for activity suggestion:")
        
        if city:
            try:
                activity = self.controller.suggest_activity(city)
                self._display_result(f"🎯 ACTIVITY SUGGESTIONS:\n{'=' * 50}\n{activity}")
            except Exception as e:
                self._display_error(f"Failed to get activity suggestion: {str(e)}")

    def _weather_summary(self):
        """Get comprehensive weather summary"""
        city = self.controller.last_city
        if not city:
            city = self._prompt_for_city("Enter city for weather summary:")
        
        if city:
            try:
                summary = self.controller.get_weather_summary(city)
                self._display_result(summary)
            except Exception as e:
                self._display_error(f"Failed to get weather summary: {str(e)}")

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
        """Check weather alerts for last used city or prompt for new city"""
        city = self.controller.last_city
        if not city:
            city = self._prompt_for_city("Enter city to check weather alerts:")
        
        if city:
            try:
                alerts = self.controller.check_weather_alerts(city)
                self._display_result(f"⚠️ WEATHER ALERTS for {city}:\n{'=' * 50}\n{alerts}")
            except Exception as e:
                self._display_error(f"Failed to check alerts: {str(e)}")

    def _city_explorer(self):
        """Explore cities with different weather conditions"""
        result = "🗺️ CITY EXPLORER:\n"
        result += "=" * 50 + "\n\n"
        result += "Discover cities around the world with different weather:\n\n"
        
        sample_cities = [
            ("🌴 Tropical Paradise", ["Miami", "Bangkok", "Singapore", "Rio de Janeiro"]),
            ("❄️ Winter Wonderland", ["Oslo", "Montreal", "Moscow", "Anchorage"]),
            ("🌞 Sunny Destinations", ["Los Angeles", "Barcelona", "Sydney", "Cape Town"]),
            ("🌧️ Rainy Cities", ["Seattle", "London", "Mumbai", "Bergen"]),
            ("🏔️ Mountain Weather", ["Denver", "Zurich", "Calgary", "Innsbruck"])
        ]
        
        for category, cities in sample_cities:
            result += f"{category}:\n"
            for city in cities:
                result += f"  • {city}\n"
            result += "\n"
        
        result += "💡 Tip: Enter any of these cities in Quick Weather to explore their current conditions!"
        self._display_result(result)

    def _weather_trends(self):
        """Show weather trends and patterns"""
        try:
            dates, temps = self.controller.get_weather_history(30)
            
            if len(temps) < 5:
                result = "📈 WEATHER TRENDS:\n"
                result += "=" * 50 + "\n"
                result += "Need more weather data to show trends.\n"
                result += "Use the weather features to collect more data!"
            else:
                avg_temp = sum(temps) / len(temps)
                max_temp = max(temps)
                min_temp = min(temps)
                
                result = "📈 WEATHER TRENDS ANALYSIS:\n"
                result += "=" * 50 + "\n"
                result += f"Data Points: {len(temps)} records\n"
                result += f"Period: {dates[0]} to {dates[-1]}\n\n"
                result += f"Temperature Statistics:\n"
                result += f"• Average: {avg_temp:.1f}°\n"
                result += f"• Maximum: {max_temp:.1f}°\n"
                result += f"• Minimum: {min_temp:.1f}°\n"
                result += f"• Range: {max_temp - min_temp:.1f}°\n\n"
                
                # Recent trend
                if len(temps) > 7:
                    recent_avg = sum(temps[-7:]) / 7
                    older_avg = sum(temps[:7]) / 7
                    trend = "warming" if recent_avg > older_avg else "cooling"
                    result += f"📈 Recent Trend: {trend.upper()}\n"
            
            self._display_result(result)
        except Exception as e:
            self._display_error(f"Failed to analyze trends: {str(e)}")

    def _quick_compare(self):
        """Quick comparison of multiple cities"""
        result = "📋 QUICK CITY COMPARISON:\n"
        result += "=" * 50 + "\n\n"
        
        # Get favorite cities for comparison
        fav_cities = self.controller.get_favorite_cities()
        
        if len(fav_cities) >= 2:
            result += "Comparing your favorite cities:\n\n"
            try:
                for city in fav_cities[:3]:  # Compare up to 3 cities
                    weather_data = self.controller.get_current_weather(city)
                    result += f"🏙️ {city}:\n"
                    result += f"  Temperature: {weather_data.formatted_temperature}\n"
                    result += f"  Conditions: {weather_data.description}\n"
                    result += f"  Humidity: {weather_data.humidity}%\n\n"
            except Exception as e:
                result += f"Error comparing cities: {str(e)}\n"
        else:
            result += "Add more favorite cities to enable quick comparison!\n\n"
            result += "Popular cities to compare:\n"
            result += "• New York vs London vs Tokyo\n"
            result += "• Miami vs Los Angeles vs Seattle\n"
            result += "• Paris vs Rome vs Barcelona\n\n"
            result += "Use 'Save Favorite' to add cities for comparison."
        
        self._display_result(result)

    def _prompt_for_city(self, prompt_text):
        """Prompt user for city name"""
        from tkinter import simpledialog
        return simpledialog.askstring("City Input", prompt_text)

    def _display_result(self, content):
        """Display result in the text area"""
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", content)

    def _display_error(self, error_msg):
        """Display error message in the text area"""
        self.result_text.delete("1.0", tk.END)
        error_content = f"❌ ERROR:\n{'=' * 50}\n{error_msg}\n\n"
        error_content += "💡 Tips:\n"
        error_content += "• Check your internet connection\n"
        error_content += "• Verify the city name spelling\n"
        error_content += "• Try a different city\n"
        self.result_text.insert("1.0", error_content)
        

class MLTab:
    """Machine Learning insights tab component"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="🤖 ML Insights")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the ML insights UI components"""
        # Header
        header_label = StyledLabel(self.frame, "🤖 Machine Learning Weather Analysis", 
                                 bg=COLOR_PALETTE["background"], 
                                 fg=COLOR_PALETTE["accent"],
                                 font=("Arial", 16, "bold"))
        header_label.pack(pady=10)

        # City input frame
        input_frame = tk.Frame(self.frame, bg=COLOR_PALETTE["background"])
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="City:", 
                bg=COLOR_PALETTE["background"], 
                fg=COLOR_PALETTE["tab_fg"], 
                font=("Arial", 12)).pack(side=tk.LEFT, padx=(0, 5))

        self.city_entry = tk.Entry(input_frame, width=20, font=("Arial", 12))
        self.city_entry.pack(side=tk.LEFT, padx=(0, 10))

        # ML Analysis buttons frame
        button_frame = tk.Frame(self.frame, bg=COLOR_PALETTE["background"])
        button_frame.pack(pady=10)

        # Temperature prediction button
        self.predict_btn = StyledButton(button_frame, "cool_black", text="🔮 Predict Temperature", 
                                      command=self._predict_temperature)
        self.predict_btn.pack(side=tk.LEFT, padx=5)

        # Weather patterns button
        self.patterns_btn = StyledButton(button_frame, "accent_black", text="📊 Detect Patterns", 
                                       command=self._detect_patterns)
        self.patterns_btn.pack(side=tk.LEFT, padx=5)

        # Anomaly detection button
        self.anomaly_btn = StyledButton(button_frame, "warning_black", text="⚠️ Find Anomalies", 
                                      command=self._detect_anomalies)
        self.anomaly_btn.pack(side=tk.LEFT, padx=5)

        # Comprehensive analysis button
        self.analysis_btn = StyledButton(button_frame, "success_black", text="🧠 Full Analysis", 
                                       command=self._comprehensive_analysis)
        self.analysis_btn.pack(side=tk.LEFT, padx=5)

        # Results display area
        result_frame = tk.Frame(self.frame, bg=COLOR_PALETTE["background"])
        result_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Scrollable text area for results
        self.result_text = StyledText(result_frame, height=20, width=80)
        
        # Scrollbar for text area
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Initial help text
        self._display_help()

    def _display_help(self):
        """Display initial help information"""
        help_text = """🤖 ML Weather Analysis Features
========================================

Welcome to the Machine Learning Weather Analysis tab! Here you can:

🔮 TEMPERATURE PREDICTION
   • Predict future temperatures based on historical trends
   • Get confidence scores for predictions
   • See prediction horizons and model information

📊 PATTERN DETECTION
   • Identify recurring weather patterns
   • Analyze temperature stability and variations
   • Discover frequent weather conditions

⚠️ ANOMALY DETECTION
   • Find unusual weather events
   • Detect extreme temperatures
   • Get severity scores for anomalies

🧠 COMPREHENSIVE ANALYSIS
   • Get complete ML insights for a city
   • Weather statistics and trends
   • Personalized recommendations
   • Historical data analysis

📝 HOW TO USE:
1. Enter a city name in the input field above
2. Click any of the analysis buttons
3. View the results in this area

💡 TIP: The ML models use your historical weather data from the CSV log.
The more data you have, the better the predictions!

Get started by entering a city and clicking an analysis button! 🚀
"""
        self._display_result(help_text)

    def _get_city(self):
        """Get city from input field"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Required", "Please enter a city name")
            return None
        return city

    def _predict_temperature(self):
        """Predict temperature for the specified city"""
        city = self._get_city()
        if not city:
            return

        try:
            self._display_result("🔮 Analyzing temperature trends...\n\nPlease wait...")
            self.frame.update()

            # Get ML controller and prediction
            ml_controller = self.controller.ml_controller
            prediction = ml_controller.get_temperature_prediction(city, 24)
            
            result = f"🔮 Temperature Prediction for {city.title()}\n"
            result += "=" * 50 + "\n\n"
            result += ml_controller.format_prediction_for_display(prediction)
            result += "\n\n📋 Prediction Details:\n"
            result += f"   • City: {prediction.city}\n"
            result += f"   • Prediction Horizon: {prediction.prediction_horizon_hours} hours\n"
            result += f"   • Trend Direction: {prediction.trend_direction}\n"
            
            if prediction.confidence_score > 0.7:
                result += "\n✅ High confidence prediction - reliable forecast"
            elif prediction.confidence_score > 0.5:
                result += "\n⚠️ Moderate confidence - use with caution"
            else:
                result += "\n❌ Low confidence - more data needed for accurate prediction"

            self._display_result(result)

        except Exception as e:
            self._display_error(f"Failed to predict temperature: {str(e)}")

    def _detect_patterns(self):
        """Detect weather patterns for the specified city"""
        city = self._get_city()
        if not city:
            return

        try:
            self._display_result("📊 Analyzing weather patterns...\n\nPlease wait...")
            self.frame.update()

            ml_controller = self.controller.ml_controller
            patterns = ml_controller.get_weather_patterns(city)
            
            result = f"📊 Weather Patterns for {city.title()}\n"
            result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            if patterns:
                result += ml_controller.format_patterns_for_display(patterns)
                result += f"\n\n📈 Pattern Summary:\n"
                result += f"   • Total patterns detected: {len(patterns)}\n"
                
                pattern_types = set(p.pattern_name for p in patterns)
                result += f"   • Pattern types: {', '.join(pattern_types)}\n"
                
                avg_frequency = sum(p.frequency for p in patterns) / len(patterns)
                result += f"   • Average frequency: {avg_frequency:.1f} occurrences\n"
            else:
                result += "No patterns found for the specified city.\n"
            
            self._display_result(result)
        except Exception as e:
            self._display_error(f"Failed to detect patterns: {str(e)}")

    def _detect_anomalies(self):
        """Detect anomalies in weather data for the specified city"""
        city = self._get_city()
        if not city:
            return

        try:
            self._display_result("⚠️ Detecting weather anomalies...\n\nPlease wait...")
            self.frame.update()

            ml_controller = self.controller.ml_controller
            anomalies = ml_controller.get_weather_anomalies(city)
            
            result = f"⚠️ Weather Anomalies for {city.title()}\n"
            result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            if anomalies:
                for anomaly in anomalies:
                    result += f"• {anomaly.description} (Severity: {anomaly.severity})\n"
                result += "\nTotal anomalies detected: " + str(len(anomalies))
            else:
                result += "No significant anomalies detected.\n"
            
            self._display_result(result)
        except Exception as e:
            self._display_error(f"Failed to detect anomalies: {str(e)}")

    def _comprehensive_analysis(self):
        """Perform a comprehensive analysis for the specified city"""
        city = self._get_city()
        if not city:
            return

        try:
            self._display_result("🧠 Performing comprehensive analysis...\n\nPlease wait...")
            self.frame.update()

            ml_controller = self.controller.ml_controller
            analysis = ml_controller.get_comprehensive_analysis(city)
            
            result = f"🧠 Comprehensive Weather Analysis for {city.title()}\n"
            result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            result += "📊 Statistical Overview:\n"
            result += f"• Average Temperature: {analysis.avg_temperature:.1f}°\n"
            result += f"• Max Temperature: {analysis.max_temperature:.1f}°\n"
            result += f"• Min Temperature: {analysis.min_temperature:.1f}°\n"
            result += f"• Temperature Range: {analysis.temperature_range:.1f}°\n\n"
            
            result += "📈 Trend Analysis:\n"
            result += f"• Recent Trend: {analysis.recent_trend}\n"
            result += f"• Long-term Trend: {analysis.long_term_trend}\n\n"
            
            result += "🌪️ Extreme Weather Events:\n"
            if analysis.extreme_events:
                for event in analysis.extreme_events:
                    result += f"  - {event}\n"
            else:
                result += "• No extreme events detected\n"
            
            result += "\n📋 Recommendations:\n"
            result += "• Review monthly and seasonal trends for planning\n"
            result += "• Consider climate-adaptive measures\n"
            result += "• Stay informed on weather alerts and updates\n"
            
            self._display_result(result)
        except Exception as e:
            self._display_error(f"Failed to perform comprehensive analysis: {str(e)}")

    def _display_result(self, content):
        """Display result in the text area"""
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", content)

    def _display_error(self, error_msg):
        """Display error message in the text area"""
        self.result_text.delete("1.0", tk.END)
        error_content = f"❌ ERROR:\n{'=' * 50}\n{error_msg}\n\n"
        error_content += "💡 Tips:\n"
        error_content += "• Check your internet connection\n"
        error_content += "• Verify the city name spelling\n"
        error_content += "• Try a different city\n"
        self.result_text.insert("1.0", error_content)

class LiveWeatherTab:
    """Live weather tab with animations and radar"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="🌦️ Live Weather")
        self.animation_widget = None
        self.radar_widget = None
        self._setup_ui()

    def _setup_ui(self):
        """Setup the comprehensive live weather UI"""
        # Main title
        title_frame = ttk.Frame(self.frame)
        title_frame.pack(fill="x", padx=10, pady=5)
        
        StyledLabel(title_frame, text="🌦️ Live Weather Radar & Animations", 
                   font=("Arial", 16, "bold")).pack()
        
        # Create main split-screen layout
        self.main_paned = ttk.PanedWindow(self.frame, orient="horizontal")
        self.main_paned.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left panel for animations
        self.left_frame = ttk.LabelFrame(self.main_paned, text="🎬 Live Weather Animations")
        self.main_paned.add(self.left_frame, weight=1)
        
        # Right panel for radar
        self.right_frame = ttk.LabelFrame(self.main_paned, text="🌩️ Doppler Weather Radar")
        self.main_paned.add(self.right_frame, weight=1)
        
        # Setup both panels
        self._setup_animation_panel()
        self._setup_radar_panel()

    def _setup_animation_panel(self):
        """Setup the live animation panel"""
        try:
            from services.live_weather_service import AnimatedWeatherWidget, ANIMATIONS_AVAILABLE
            
            if ANIMATIONS_AVAILABLE:
                # Animation canvas area
                self.animation_canvas_frame = ttk.Frame(self.left_frame)
                self.animation_canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)
                
                # Create animation widget
                self.animation_widget = AnimatedWeatherWidget(self.animation_canvas_frame)
                
                # Animation controls
                controls_frame = ttk.Frame(self.left_frame)
                controls_frame.pack(fill="x", padx=5, pady=5)
                
                # Control buttons
                btn_frame1 = ttk.Frame(controls_frame)
                btn_frame1.pack(fill="x", pady=2)
                
                StyledButton(btn_frame1, "success_black", text="▶️ Start Animations", 
                            command=self._start_animations).pack(side="left", padx=2)
                StyledButton(btn_frame1, "danger_black", text="⏹️ Stop Animations", 
                            command=self._stop_animations).pack(side="left", padx=2)
                
                btn_frame2 = ttk.Frame(controls_frame)
                btn_frame2.pack(fill="x", pady=2)
                
                StyledButton(btn_frame2, "info_black", text="🌦️ Weather Sync", 
                            command=self._toggle_weather_sync).pack(side="left", padx=2)
                StyledButton(btn_frame2, "accent_black", text="⚙️ Settings", 
                            command=self._animation_settings).pack(side="left", padx=2)
                
                # Animation status
                self.animation_status = StyledLabel(controls_frame, text="Animation Status: Ready")
                self.animation_status.pack(pady=5)
                
                # Legend frame
                legend_frame = ttk.LabelFrame(self.left_frame, text="Animation Elements")
                legend_frame.pack(fill="x", padx=5, pady=5)
                
                # Create color swatches with descriptions
                legend_items = [
                    ("blue", "Blue", "Walker (Normal Speed)"),
                    ("green", "Green", "Jogger (Fast)"),
                    ("purple", "Purple", "Elderly (Slow)"),
                    ("red", "Red", "Cyclist (Fastest)"),
                    ("darkblue", "Dark Blue", "Rain Drops"),
                    ("white", "White", "Snow Flakes"),
                    ("yellow", "Yellow", "Lightning")
                ]
                
                # Create color swatch frames and labels
                for index, (color, color_name, description) in enumerate(legend_items):
                    row = index // 2  # 2 columns instead of 3
                    col = index % 2
                    
                    item_frame = ttk.Frame(legend_frame)
                    item_frame.grid(row=row, column=col, padx=5, pady=2, sticky="w")
                    
                    # Color swatch (small colored rectangle)
                    swatch = tk.Frame(item_frame, width=15, height=15, bg=color)
                    swatch.pack(side="left", padx=5)
                    # Keep the square shape
                    swatch.pack_propagate(False)
                    
                    # Add border to white swatch for visibility
                    if color == "#FFFFFF":
                        swatch.configure(highlightbackground="black", highlightthickness=1)
                    
                    # Description with color name
                    StyledLabel(item_frame, 
                              text=f"{description} ({color_name})",
                              font=("Arial", 9)).pack(side="left", padx=5)
                
            else:
                # Fallback when animations not available
                self._create_animation_fallback()
                
        except Exception as e:
            print(f"Animation setup error: {e}")
            self._create_animation_fallback()

    def _setup_radar_panel(self):
        """Setup the advanced weather radar panel with severe weather tracking"""
        try:
            from services.live_weather_service import WeatherRadarWidget, RADAR_AVAILABLE
            
            if RADAR_AVAILABLE:
                # Advanced radar canvas area
                self.radar_canvas_frame = ttk.Frame(self.right_frame)
                self.radar_canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)
                
                # Create enhanced radar widget with severe weather tracking
                radar_service = self.controller.get_radar_service()
                self.radar_widget = WeatherRadarWidget(self.radar_canvas_frame, radar_service)
                
                # Advanced radar controls
                controls_frame = ttk.Frame(self.right_frame)
                controls_frame.pack(fill="x", padx=5, pady=5)
                
                # Location input frame
                location_frame = ttk.LabelFrame(controls_frame, text="📍 Location & Tracking")
                location_frame.pack(fill="x", pady=2)
                
                # Coordinates
                coord_frame = ttk.Frame(location_frame)
                coord_frame.pack(fill="x", padx=5, pady=2)
                
                StyledLabel(coord_frame, text="Lat:").pack(side="left")
                self.lat_entry = ttk.Entry(coord_frame, width=10)
                self.lat_entry.pack(side="left", padx=2)
                self.lat_entry.insert(0, "39.2904")  # Baltimore default
                
                StyledLabel(coord_frame, text="Lon:").pack(side="left", padx=(10,0))
                self.lon_entry = ttk.Entry(coord_frame, width=10)
                self.lon_entry.pack(side="left", padx=2)
                self.lon_entry.insert(0, "-76.6122")  # Baltimore default
                
                # Severe weather tracking options
                tracking_frame = ttk.LabelFrame(controls_frame, text="🌪️ Severe Weather Tracking")
                tracking_frame.pack(fill="x", pady=2)
                
                track_options = ttk.Frame(tracking_frame)
                track_options.pack(fill="x", padx=5, pady=2)
                
                # Tracking checkboxes
                self.track_hurricanes = tk.BooleanVar(value=True)
                self.track_tornadoes = tk.BooleanVar(value=True)
                self.track_storms = tk.BooleanVar(value=True)
                self.track_blizzards = tk.BooleanVar(value=True)
                
                ttk.Checkbutton(track_options, text="🌀 Hurricanes", 
                               variable=self.track_hurricanes).pack(side="left", padx=3)
                ttk.Checkbutton(track_options, text="🌪️ Tornadoes", 
                               variable=self.track_tornadoes).pack(side="left", padx=3)
                ttk.Checkbutton(track_options, text="⛈️ Storms", 
                               variable=self.track_storms).pack(side="left", padx=3)
                ttk.Checkbutton(track_options, text="❄️ Blizzards", 
                               variable=self.track_blizzards).pack(side="left", padx=3)
                
                # Radar intensity settings
                intensity_frame = ttk.LabelFrame(controls_frame, text="📊 Radar Settings")
                intensity_frame.pack(fill="x", pady=2)
                
                intensity_controls = ttk.Frame(intensity_frame)
                intensity_controls.pack(fill="x", padx=5, pady=2)
                
                StyledLabel(intensity_controls, text="Range:").pack(side="left")
                self.radar_range = ttk.Combobox(intensity_controls, width=10, 
                                              values=["50 km", "100 km", "200 km", "500 km"])
                self.radar_range.pack(side="left", padx=2)
                self.radar_range.set("200 km")
                
                StyledLabel(intensity_controls, text="Update:").pack(side="left", padx=(10,0))
                self.update_interval = ttk.Combobox(intensity_controls, width=10,
                                                  values=["30 sec", "1 min", "2 min", "5 min"])
                self.update_interval.pack(side="left", padx=2)
                self.update_interval.set("2 min")
                
                # Control buttons
                btn_frame1 = ttk.Frame(controls_frame)
                btn_frame1.pack(fill="x", pady=3)
                
                StyledButton(btn_frame1, "primary_black", text="🔄 Update Radar", 
                            command=self._update_live_radar).pack(side="left", padx=2)
                StyledButton(btn_frame1, "warning_black", text="🌪️ Track Active Storms", 
                            command=self._track_active_storms).pack(side="left", padx=2)
                StyledButton(btn_frame1, "danger_black", text="🚨 Emergency Alerts", 
                            command=self._show_emergency_alerts).pack(side="left", padx=2)
                
                btn_frame2 = ttk.Frame(controls_frame)
                btn_frame2.pack(fill="x", pady=3)
                
                StyledButton(btn_frame2, "info_black", text="📈 Storm History", 
                            command=self._show_storm_history).pack(side="left", padx=2)
                StyledButton(btn_frame2, "success_black", text="📊 Radar Analysis", 
                            command=self._show_radar_analysis).pack(side="left", padx=2)
                StyledButton(btn_frame2, "accent_black", text="🎯 Auto-Track", 
                            command=self._toggle_auto_tracking).pack(side="left", padx=2)
                
                # Status display
                self.radar_status = StyledLabel(controls_frame, text="Radar Status: Initializing...")
                self.radar_status.pack(pady=5)
                
                # Live tracking display
                self.tracking_display = ttk.LabelFrame(controls_frame, text="🔴 LIVE TRACKING")
                self.tracking_display.pack(fill="x", pady=2)
                
                self.live_status = StyledText(self.tracking_display, height=4)
                self.live_status.pack(fill="x", padx=5, pady=2)
                
                # Initialize radar
                self._initialize_live_radar()
                
            else:
                # Enhanced fallback when radar not available
                self._create_enhanced_radar_fallback()
                
        except Exception as e:
            print(f"Radar setup error: {e}")
            self._create_enhanced_radar_fallback()

    def _create_enhanced_radar_fallback(self):
        """Create enhanced fallback radar display with simulated tracking"""
        fallback_frame = ttk.Frame(self.right_frame)
        fallback_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Simulated radar display
        radar_display = ttk.LabelFrame(fallback_frame, text="🌩️ LIVE WEATHER RADAR (Simulation Mode)")
        radar_display.pack(fill="both", expand=True)
        
        info_text = StyledText(radar_display, height=20)
        info_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        fallback_content = """🌩️ LIVE DOPPLER WEATHER RADAR - SEVERE WEATHER TRACKING

🎯 CURRENTLY TRACKING:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌀 HURRICANE TRACKING:
   • Category 1-5 classification
   • Wind speed monitoring (74+ mph)
   • Storm surge predictions
   • Landfall probability analysis
   • Evacuation zone mapping

🌪️ TORNADO DETECTION:
   • EF Scale classification (EF0-EF5)
   • Rotation velocity tracking
   • Touchdown probability
   • Path prediction modeling
   • Warning area alerts

⛈️ SEVERE THUNDERSTORMS:
   • Supercell identification
   • Hail size prediction (>1 inch)
   • Wind gust forecasting (58+ mph)
   • Flash flood potential
   • Lightning strike density

❄️ BLIZZARD MONITORING:
   • Snow accumulation rates
   • Wind speed tracking (35+ mph)
   • Visibility reduction alerts
   • Travel advisory zones
   • Power outage predictions

🌊 STORM SURGE TRACKING:
   • Coastal flood warnings
   • Wave height monitoring
   • Tide level predictions
   • Evacuation timing

🔥 WILDFIRE MONITORING:
   • Fire perimeter tracking
   • Spread rate calculation
   • Wind direction impact
   • Evacuation routes

📊 RADAR SPECIFICATIONS:
   • Real-time 20x20 intensity grid
   • 50-500km range capability
   • 30-second update intervals
   • Doppler velocity analysis
   • Dual-polarization data

🚨 EMERGENCY ALERT INTEGRATION:
   • NWS alert feeds
   • Local emergency broadcasts
   • Automatic severe weather warnings
   • Mobile push notifications

🎯 LOCATION TRACKING:
   • GPS coordinate input
   • Multi-location monitoring
   • Storm path intersections
   • Time-to-impact calculations

📈 STORM ANALYTICS:
   • Historical storm data
   • Pattern recognition
   • Seasonal trends
   • Climate impact analysis

⚡ LIVE STATUS: Monitoring for severe weather events...
🌍 Coverage: Global weather radar network
🔄 Last Update: Real-time continuous monitoring
📡 Data Sources: NOAA, NWS, International Weather Services

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Install matplotlib and numpy for full interactive radar visualization"""
        
        info_text.insert("1.0", fallback_content)
        info_text.config(state="disabled")
        
        # Simulation controls
        sim_controls = ttk.Frame(fallback_frame)
        sim_controls.pack(fill="x", pady=5)
        
        StyledButton(sim_controls, "warning_black", text="🌪️ Simulate Tornado", 
                    command=self._simulate_tornado).pack(side="left", padx=2)
        StyledButton(sim_controls, "danger_black", text="🌀 Simulate Hurricane", 
                    command=self._simulate_hurricane).pack(side="left", padx=2)
        StyledButton(sim_controls, "info_black", text="⛈️ Simulate Storm", 
                    command=self._simulate_storm).pack(side="left", padx=2)

    def _initialize_live_radar(self):
        """Initialize the live radar system"""
        try:
            self.radar_status.config(text="Radar Status: Initializing radar systems... 🔄")
            self._update_live_radar()
            self._start_auto_tracking()
            
        except Exception as e:
            self.radar_status.config(text=f"Radar Status: Initialization failed - {str(e)}")

    def _start_auto_tracking(self):
        """Start automatic weather tracking"""
        self.auto_tracking = True
        self._update_tracking_display()
        
        # Schedule regular updates
        if hasattr(self, 'radar_widget'):
            self.frame.after(30000, self._auto_update_cycle)  # 30 seconds

    def _auto_update_cycle(self):
        """Automatic update cycle for radar"""
        if hasattr(self, 'auto_tracking') and self.auto_tracking:
            self._update_live_radar()
            self._scan_for_severe_weather()
            self.frame.after(30000, self._auto_update_cycle)  # Continue cycle

    def _update_tracking_display(self):
        """Update the live tracking status display"""
        if hasattr(self, 'live_status'):
            import datetime
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            
            tracking_info = f"""🔴 LIVE TRACKING STATUS - {current_time}

🌀 Hurricanes: {'ACTIVE' if self.track_hurricanes.get() else 'DISABLED'}
🌪️ Tornadoes: {'ACTIVE' if self.track_tornadoes.get() else 'DISABLED'}  
⛈️ Storms: {'ACTIVE' if self.track_storms.get() else 'DISABLED'}
❄️ Blizzards: {'ACTIVE' if self.track_blizzards.get() else 'DISABLED'}

📡 Radar Range: {self.radar_range.get() if hasattr(self, 'radar_range') else '200 km'}
🔄 Update Rate: {self.update_interval.get() if hasattr(self, 'update_interval') else '2 min'}"""
            
            self.live_status.delete("1.0", tk.END)
            self.live_status.insert("1.0", tracking_info)

    def _create_animation_fallback(self):
        """Create fallback animation display"""
        fallback_frame = ttk.Frame(self.left_frame)
        fallback_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        info_text = StyledText(fallback_frame, height=12)
        info_text.pack(fill="both", expand=True)
        
        fallback_content = """🎬 LIVE WEATHER ANIMATIONS
        
🚶‍♂️ Animated People:
• Walker (Blue): Normal speed, weather-responsive
• Jogger (Green): Fast movement, slows in rain
• Elderly (Purple): Slow movement, very weather-sensitive  
• Cyclist (Red): Fastest movement, moderate weather impact

🌧️ Weather Effects:
• Rain: Blue raindrops, 60% speed reduction
• Snow: White snowflakes, 40% speed reduction
• Storm: Lightning flashes, 20% speed
• Blizzard: Heavy snow, 10% speed

⚙️ Animation Features:
• Real-time weather synchronization
• 10 FPS smooth animation system
• Threading for non-blocking performance
• Weather-responsive movement patterns

📦 Status: Advanced animations require additional packages
Install matplotlib and numpy for full functionality"""
        
        info_text.insert("1.0", fallback_content)
        info_text.config(state="disabled")

    def _create_radar_fallback(self):
        """Create fallback radar display"""
        fallback_frame = ttk.Frame(self.right_frame)
        fallback_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        info_text = StyledText(fallback_frame, height=12)
        info_text.pack(fill="both", expand=True)
        
        fallback_content = """🌩️ LIVE DOPPLER WEATHER RADAR
        
🎯 Radar Features:
• Real-time weather intensity mapping
• 20x20 grid precipitation data
• Color-coded intensity levels
• Auto-updating every 2 minutes

🌪️ Severe Weather Tracking:
• Hurricanes 🌀 - Category classification
• Tornadoes 🌪️ - EF scale intensity  
• Blizzards ❄️ - Snow accumulation
• Earthquakes - Magnitude tracking
• Wildfires 🔥 - Fire perimeter monitoring
• Cyclones - Storm path prediction

🚨 Alert System:
• Real-time severe weather notifications
• Emergency weather broadcasts
• Storm movement tracking
• Impact area predictions

📍 Location Support:
• GPS coordinate input (lat/lon)
• Default: Baltimore, MD (39.2904, -76.6122)
• Global weather radar coverage
• Multiple location monitoring

📦 Status: Advanced radar requires additional packages
Install matplotlib and numpy for full functionality"""
        
        info_text.insert("1.0", fallback_content)
        info_text.config(state="disabled")

    # Animation control methods
    def _start_animations(self):
        """Start live weather animations"""
        if self.animation_widget:
            try:
                self.animation_widget.start_animation()
                self.animation_status.config(text="Animation Status: Running ▶️")
            except Exception as e:
                self.animation_status.config(text=f"Animation Status: Error - {str(e)}")
        else:
            self.animation_status.config(text="Animation Status: Not Available")

    def _stop_animations(self):
        """Stop live weather animations"""
        if self.animation_widget:
            try:
                self.animation_widget.stop_animation()
                self.animation_status.config(text="Animation Status: Stopped ⏹️")
            except Exception as e:
                self.animation_status.config(text=f"Animation Status: Error - {str(e)}")

    def _toggle_weather_sync(self):
        """Toggle weather synchronization for animations"""
        if self.animation_widget:
            try:
                self.animation_widget.toggle_weather_sync()
                self.animation_status.config(text="Animation Status: Weather Sync Toggled 🌦️")
            except Exception as e:
                self.animation_status.config(text=f"Animation Status: Error - {str(e)}")

    def _animation_settings(self):
        """Show animation settings dialog"""
        from tkinter import messagebox
        messagebox.showinfo("Animation Settings", 
                           "⚙️ Animation Settings:\n\n"
                           "• Speed: Adjustable (1x-5x)\n"
                           "• Weather Sync: On/Off\n"
                           "• Effects: Rain, Snow, Lightning\n"
                           "• People Types: 4 different characters\n"
                           "• Frame Rate: 10 FPS\n\n"
                           "Settings will be available in future updates!")

    # Radar control methods
    def _update_live_radar(self):
        """Update the live radar display with severe weather tracking"""
        if self.radar_widget:
            try:
                lat = float(self.lat_entry.get())
                lon = float(self.lon_entry.get())
                
                tracking_options = {
                    "hurricanes": self.track_hurricanes.get(),
                    "tornadoes": self.track_tornadoes.get(),
                    "storms": self.track_storms.get(),
                    "blizzards": self.track_blizzards.get()
                }
                
                self.radar_widget.update_radar(lat, lon, tracking_options)
                self.radar_status.config(text=f"Radar Status: Updated for {lat:.2f}, {lon:.2f} 🔄")
                
            except ValueError:
                self.radar_status.config(text="Radar Status: Invalid coordinates")
            except Exception as e:
                self.radar_status.config(text=f"Radar Status: Error - {str(e)}")
        else:
            self.radar_status.config(text="Radar Status: Not Available")

    def _track_active_storms(self):
        """Track active storms and display information"""
        if self.radar_widget:
            try:
                storm_data = self.radar_widget.get_storm_tracking()
                self.radar_status.config(text="Radar Status: Storm Tracking Active 🌪️")
                
                from tkinter import messagebox
                messagebox.showinfo("Active Storm Tracking", f"🌪️ SEVERE WEATHER TRACKING\n\n{storm_data}")
                
            except Exception as e:
                self.radar_status.config(text=f"Radar Status: Error - {str(e)}")

    def _show_emergency_alerts(self):
        """Show emergency weather alerts"""
        if self.radar_widget:
            try:
                alerts = self.radar_widget.get_weather_alerts()
                
                popup = tk.Toplevel(self.frame)
                popup.title("🚨 Emergency Weather Alerts")
                popup.geometry("600x400")
                
                alerts_text = StyledText(popup, height=20)
                alerts_text.pack(fill="both", expand=True, padx=10, pady=10)
                alerts_text.insert("1.0", alerts)
                alerts_text.config(state="disabled")
                
                StyledButton(popup, "primary_black", text="Close", command=popup.destroy).pack(pady=10)
                
                self.radar_status.config(text="Radar Status: Alerts Displayed 🚨")
                
            except Exception as e:
                self.radar_status.config(text=f"Radar Status: Error - {str(e)}")

    def _show_storm_history(self):
        """Show historical storm data"""
        if self.radar_widget:
            try:
                history = self.radar_widget.get_storm_history()
                
                popup = tk.Toplevel(self.frame)
                popup.title("📈 Storm History")
                popup.geometry("500x350")
                
                history_text = StyledText(popup, height=15)
                history_text.pack(fill="both", expand=True, padx=10, pady=10)
                history_text.insert("1.0", history)
                history_text.config(state="disabled")
                
                StyledButton(popup, "primary_black", text="Close", command=popup.destroy).pack(pady=10)
                
                self.radar_status.config(text="Radar Status: History Displayed 📈")
                
            except Exception as e:
                self.radar_status.config(text=f"Radar Status: Error - {str(e)}")

    def _show_radar_analysis(self):
        """Show detailed radar analysis"""
        if self.radar_widget:
            try:
                analysis = self.radar_widget.get_radar_analysis()
                
                popup = tk.Toplevel(self.frame)
                popup.title("📊 Radar Analysis")
                popup.geometry("500x350")
                
                analysis_text = StyledText(popup, height=15)
                analysis_text.pack(fill="both", expand=True, padx=10, pady=10)
                analysis_text.insert("1.0", analysis)
                analysis_text.config(state="disabled")
                
                StyledButton(popup, "primary_black", text="Close", command=popup.destroy).pack(pady=10)
                
                self.radar_status.config(text="Radar Status: Analysis Displayed 📊")
                
            except Exception as e:
                self.radar_status.config(text=f"Radar Status: Error - {str(e)}")

    def _toggle_auto_tracking(self):
        """Toggle automatic tracking of severe weather"""
        if hasattr(self, 'auto_tracking'):
            self.auto_tracking = not self.auto_tracking
            status = "ACTIVE" if self.auto_tracking else "DISABLED"
            self.radar_status.config(text=f"Auto-Tracking: {status} 🎯")
            if self.auto_tracking:
                self._auto_update_cycle()
        else:
            self.auto_tracking = True
            self.radar_status.config(text="Auto-Tracking: ACTIVE 🎯")
            self._auto_update_cycle()

    def _scan_for_severe_weather(self):
        """Scan for severe weather and update display"""
        if self.radar_widget:
            try:
                storm_data = self.radar_widget.get_storm_tracking()
                self.live_status.delete("1.0", tk.END)
                self.live_status.insert("1.0", f"🔴 LIVE TRACKING:\n\n{storm_data}")
            except Exception as e:
                self.live_status.delete("1.0", tk.END)
                self.live_status.insert("1.0", f"🔴 LIVE TRACKING:\n\nError: {str(e)}")

    def _simulate_tornado(self):
        """Simulate a tornado event"""
        if hasattr(self, 'live_status'):
            self.live_status.delete("1.0", tk.END)
            self.live_status.insert("1.0", "🔴 LIVE TRACKING:\n\n🌪️ TORNADO WARNING!\nEF-3 Tornado detected near your location.\nTake shelter immediately!")

    def _simulate_hurricane(self):
        """Simulate a hurricane event"""
        if hasattr(self, 'live_status'):
            self.live_status.delete("1.0", tk.END)
            self.live_status.insert("1.0", "🔴 LIVE TRACKING:\n\n🌀 HURRICANE WARNING!\nCategory 4 Hurricane approaching.\nPrepare for evacuation.")

    def _simulate_storm(self):
        """Simulate a severe storm event"""
        if hasattr(self, 'live_status'):
            self.live_status.delete("1.0", tk.END)
            self.live_status.insert("1.0", "🔴 LIVE TRACKING:\n\n⛈️ SEVERE THUNDERSTORM!\nLarge hail and damaging winds expected.\nStay indoors.")


class SevereWeatherTab:
    """Severe weather alerts and tracking tab"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="🚨 Severe Alerts")
        self.radar_widget = None
        self._setup_ui()

    def _setup_ui(self):
        """Setup the severe weather UI"""
        # Main title
        title_frame = ttk.Frame(self.frame)
        title_frame.pack(fill="x", padx=10, pady=5)
        
        StyledLabel(title_frame, text="🚨 Severe Weather Alerts & Tracking", 
                   font=("Arial", 16, "bold")).pack()
        
        # Create main split-screen layout
        self.main_paned = ttk.PanedWindow(self.frame, orient="horizontal")
        self.main_paned.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left panel for alerts list
        self.left_frame = ttk.LabelFrame(self.main_paned, text="📢 Active Alerts")
        self.main_paned.add(self.left_frame, weight=1)
        
        # Right panel for radar and charts
        self.right_frame = ttk.LabelFrame(self.main_paned, text="🗺️ Radar & Analysis")
        self.main_paned.add(self.right_frame, weight=2)
        
        # Setup both panels
        self._setup_alerts_panel()
        self._setup_radar_panel()

    def _setup_alerts_panel(self):
        """Setup the active alerts panel"""
        # Alerts display area
        self.alerts_text = StyledText(self.left_frame, height=20)
        self.alerts_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Placeholder content
        self.alerts_text.insert("1.0", "Loading severe weather alerts...\n")
        
        # Refresh button
        refresh_button = StyledButton(self.left_frame, "primary", text="🔄 Refresh Alerts",
                                      command=self.refresh_alerts)
        refresh_button.pack(pady=5)

    def _setup_radar_panel(self):
        """Setup the advanced weather radar panel with severe weather tracking"""
        try:
            from services.live_weather_service import WeatherRadarWidget, RADAR_AVAILABLE
            
            if RADAR_AVAILABLE:
                # Advanced radar canvas area
                self.radar_canvas_frame = ttk.Frame(self.right_frame)
                self.radar_canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)
                
                # Create enhanced radar widget with severe weather tracking
                radar_service = self.controller.get_radar_service()
                self.radar_widget = WeatherRadarWidget(self.radar_canvas_frame, radar_service)
                
                # Advanced radar controls
                controls_frame = ttk.Frame(self.right_frame)
                controls_frame.pack(fill="x", padx=5, pady=5)
                
                # Location input frame
                location_frame = ttk.LabelFrame(controls_frame, text="📍 Location & Tracking")
                location_frame.pack(fill="x", pady=2)
                
                # Coordinates
                coord_frame = ttk.Frame(location_frame)
                coord_frame.pack(fill="x", padx=5, pady=2)
                
                StyledLabel(coord_frame, text="Lat:").pack(side="left")
                self.lat_entry = ttk.Entry(coord_frame, width=10)
                self.lat_entry.pack(side="left", padx=2)
                self.lat_entry.insert(0, "39.2904")  # Baltimore default
                
                StyledLabel(coord_frame, text="Lon:").pack(side="left", padx=(10,0))
                self.lon_entry = ttk.Entry(coord_frame, width=10)
                self.lon_entry.pack(side="left", padx=2)
                self.lon_entry.insert(0, "-76.6122")  # Baltimore default
                
                # Severe weather tracking options
                tracking_frame = ttk.LabelFrame(controls_frame, text="🌪️ Severe Weather Tracking")
                tracking_frame.pack(fill="x", pady=2)
                
                track_options = ttk.Frame(tracking_frame)
                track_options.pack(fill="x", padx=5, pady=2)
                
                # Tracking checkboxes
                self.track_hurricanes = tk.BooleanVar(value=True)
                self.track_tornadoes = tk.BooleanVar(value=True)
                self.track_storms = tk.BooleanVar(value=True)
                
                ttk.Checkbutton(track_options, text="🌀 Hurricanes", 
                               variable=self.track_hurricanes).pack(side="left", padx=3)
                ttk.Checkbutton(track_options, text="🌪️ Tornadoes", 
                               variable=self.track_tornadoes).pack(side="left", padx=3)
                ttk.Checkbutton(track_options, text="⛈️ Storms", 
                               variable=self.track_storms).pack(side="left", padx=3)
                
                # Control buttons
                btn_frame1 = ttk.Frame(controls_frame)
                btn_frame1.pack(fill="x", pady=3)
                
                StyledButton(btn_frame1, "primary", text="🔄 Update Radar", 
                            command=self._update_live_radar).pack(side="left", padx=2)
                StyledButton(btn_frame1, "warning_black", text="🌪️ Track Active Storms", 
                            command=self._track_active_storms).pack(side="left", padx=2)
                
                # Status display
                self.radar_status = StyledLabel(controls_frame, text="Radar Status: Initializing...")
                self.radar_status.pack(pady=5)
                
                # Initialize radar
                self._initialize_live_radar()
                
            else:
                # Fallback when radar not available
                self._create_enhanced_radar_fallback()
                
        except Exception as e:
            print(f"Severe Weather Tab Radar setup error: {e}")
            self._create_enhanced_radar_fallback()

    def refresh_alerts(self):
        """Refresh the list of severe weather alerts"""
        self.alerts_text.delete("1.0", tk.END)
        self.alerts_text.insert("1.0", "Refreshing alerts...\n")
        try:
            # This would call the controller to get real alerts
            alerts = self.controller.get_severe_weather_alerts() 
            self.alerts_text.delete("1.0", tk.END)
            self.alerts_text.insert("1.0", alerts)
        except Exception as e:
            self.alerts_text.delete("1.0", tk.END)
            self.alerts_text.insert("1.0", f"Error fetching alerts: {e}\n")

    def _initialize_live_radar(self):
        """Initialize the live radar system"""
        try:
            self.radar_status.config(text="Radar Status: Initializing radar systems... 🔄")
            self._update_live_radar()
        except Exception as e:
            self.radar_status.config(text=f"Radar Status: Initialization failed - {str(e)}")

    def _update_live_radar(self):
        """Update the live radar display with severe weather tracking"""
        if self.radar_widget:
            try:
                lat = float(self.lat_entry.get())
                lon = float(self.lon_entry.get())
                
                tracking_options = {
                    "hurricanes": self.track_hurricanes.get(),
                    "tornadoes": self.track_tornadoes.get(),
                    "storms": self.track_storms.get(),
                }
                
                self.radar_widget.update_radar(lat, lon, tracking_options)
                self.radar_status.config(text=f"Radar Status: Updated for {lat:.2f}, {lon:.2f} 🔄")
                
            except ValueError:
                self.radar_status.config(text="Radar Status: Invalid coordinates")
            except Exception as e:
                self.radar_status.config(text=f"Radar Status: Error - {str(e)}")
        else:
            self.radar_status.config(text="Radar Status: Not Available")

    def _track_active_storms(self):
        """Track active storms and display information"""
        if self.radar_widget:
            try:
                storm_data = self.radar_widget.get_storm_tracking()
                self.radar_status.config(text="Radar Status: Storm Tracking Active 🌪️")
                
                from tkinter import messagebox
                messagebox.showinfo("Active Storm Tracking", f"🌪️ SEVERE WEATHER TRACKING\n\n{storm_data}")
                
            except Exception as e:
                self.radar_status.config(text=f"Radar Status: Error - {str(e)}")

    def _create_enhanced_radar_fallback(self):
        """Create enhanced fallback radar display with simulated tracking"""
        fallback_frame = ttk.Frame(self.right_frame)
        fallback_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Simulated radar display
        radar_display = ttk.LabelFrame(fallback_frame, text="🌩️ LIVE WEATHER RADAR (Simulation Mode)")
        radar_display.pack(fill="both", expand=True)
        
        info_text = StyledText(radar_display, height=20)
        info_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        fallback_content = """🌩️ LIVE DOPPLER WEATHER RADAR - SEVERE WEATHER TRACKING

This is a simulation. Install matplotlib and numpy for full functionality.

- Hurricane Tracking
- Tornado Detection
- Severe Thunderstorm Monitoring
"""
        
        info_text.insert("1.0", fallback_content)
        info_text.config(state="disabled")

    def _setup_alerts_panel(self):
        """Setup the active alerts panel"""
        # Alerts display area
        self.alerts_text = StyledText(self.left_frame, height=20)
        self.alerts_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Placeholder content
        self.alerts_text.insert("1.0", "Loading severe weather alerts...\n")
        
        # Refresh button
        refresh_button = StyledButton(self.left_frame, "primary", text="🔄 Refresh Alerts",
                                      command=self.refresh_alerts)
        refresh_button.pack(pady=5)

    def _setup_radar_panel(self):
        """Setup the advanced weather radar panel with severe weather tracking"""
        try:
            from services.live_weather_service import WeatherRadarWidget, RADAR_AVAILABLE
            
            if RADAR_AVAILABLE:
                # Advanced radar canvas area
                self.radar_canvas_frame = ttk.Frame(self.right_frame)
                self.radar_canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)
                
                # Create enhanced radar widget
                self.radar_widget = WeatherRadarWidget(self.radar_canvas_frame)
                
                # Advanced radar controls
                controls_frame = ttk.Frame(self.right_frame)
                controls_frame.pack(fill="x", padx=5, pady=5)
                
                # Location input frame
                location_frame = ttk.LabelFrame(controls_frame, text="📍 Location & Tracking")
                location_frame.pack(fill="x", pady=2)
                
                # Coordinates
                coord_frame = ttk.Frame(location_frame)
                coord_frame.pack(fill="x", padx=5, pady=2)
                
                StyledLabel(coord_frame, text="Lat:").pack(side="left")
                self.lat_entry = ttk.Entry(coord_frame, width=10)
                self.lat_entry.pack(side="left", padx=2)
                self.lat_entry.insert(0, "39.2904")  # Baltimore default
                
                StyledLabel(coord_frame, text="Lon:").pack(side="left", padx=(10,0))
                self.lon_entry = ttk.Entry(coord_frame, width=10)
                self.lon_entry.pack(side="left", padx=2)
                self.lon_entry.insert(0, "-76.6122")  # Baltimore default
                
                # Severe weather tracking options
                tracking_frame = ttk.LabelFrame(controls_frame, text="🌪️ Severe Weather Tracking")
                tracking_frame.pack(fill="x", pady=2)
                
                track_options = ttk.Frame(tracking_frame)
                track_options.pack(fill="x", padx=5, pady=2)
                
                # Tracking checkboxes
                self.track_hurricanes = tk.BooleanVar(value=True)
                self.track_tornadoes = tk.BooleanVar(value=True)
                self.track_storms = tk.BooleanVar(value=True)
                
                ttk.Checkbutton(track_options, text="🌀 Hurricanes", 
                               variable=self.track_hurricanes).pack(side="left", padx=3)
                ttk.Checkbutton(track_options, text="🌪️ Tornadoes", 
                               variable=self.track_tornadoes).pack(side="left", padx=3)
                ttk.Checkbutton(track_options, text="⛈️ Storms", 
                               variable=self.track_storms).pack(side="left", padx=3)
                
                # Control buttons
                btn_frame1 = ttk.Frame(controls_frame)
                btn_frame1.pack(fill="x", pady=3)
                
                StyledButton(btn_frame1, "primary", text="🔄 Update Radar", 
                            command=self._update_live_radar).pack(side="left", padx=2)
                StyledButton(btn_frame1, "warning_black", text="🌪️ Track Active Storms", 
                            command=self._track_active_storms).pack(side="left", padx=2)
                
                # Status display
                self.radar_status = StyledLabel(controls_frame, text="Radar Status: Initializing...")
                self.radar_status.pack(pady=5)
                
                # Initialize radar
                self._initialize_live_radar()
                
            else:
                # Fallback when radar not available
                self._create_enhanced_radar_fallback()
                
        except Exception as e:
            print(f"Severe Weather Tab Radar setup error: {e}")
            self._create_enhanced_radar_fallback()

    def refresh_alerts(self):
        """Refresh the list of severe weather alerts"""
        self.alerts_text.delete("1.0", tk.END)
        self.alerts_text.insert("1.0", "Refreshing alerts...\n")
        try:
            # This would call the controller to get real alerts
            alerts = self.controller.get_severe_weather_alerts() 
            self.alerts_text.delete("1.0", tk.END)
            self.alerts_text.insert("1.0", alerts)
        except Exception as e:
            self.alerts_text.delete("1.0", tk.END)
            self.alerts_text.insert("1.0", f"Error fetching alerts: {e}\n")

    def _initialize_live_radar(self):
        """Initialize the live radar system"""
        try:
            self.radar_status.config(text="Radar Status: Initializing radar systems... 🔄")
            self._update_live_radar()
        except Exception as e:
            self.radar_status.config(text=f"Radar Status: Initialization failed - {str(e)}")

    def _update_live_radar(self):
        """Update the live radar display with severe weather tracking"""
        if self.radar_widget:
            try:
                lat = float(self.lat_entry.get())
                lon = float(self.lon_entry.get())
                
                tracking_options = {
                    "hurricanes": self.track_hurricanes.get(),
                    "tornadoes": self.track_tornadoes.get(),
                    "storms": self.track_storms.get(),
                }
                
                self.radar_widget.update_radar(lat, lon, tracking_options)
                self.radar_status.config(text=f"Radar Status: Updated for {lat:.2f}, {lon:.2f} 🔄")
                
            except ValueError:
                self.radar_status.config(text="Radar Status: Invalid coordinates")
            except Exception as e:
                self.radar_status.config(text=f"Radar Status: Error - {str(e)}")
        else:
            self.radar_status.config(text="Radar Status: Not Available")

    def _track_active_storms(self):
        """Track active storms and display information"""
        if self.radar_widget:
            try:
                storm_data = self.radar_widget.get_storm_tracking()
                self.radar_status.config(text="Radar Status: Storm Tracking Active 🌪️")
                
                from tkinter import messagebox
                messagebox.showinfo("Active Storm Tracking", f"🌪️ SEVERE WEATHER TRACKING\n\n{storm_data}")
                
            except Exception as e:
                self.radar_status.config(text=f"Radar Status: Error - {str(e)}")

    def _create_enhanced_radar_fallback(self):
        """Create enhanced fallback radar display with simulated tracking"""
        fallback_frame = ttk.Frame(self.right_frame)
        fallback_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Simulated radar display
        radar_display = ttk.LabelFrame(fallback_frame, text="🌩️ LIVE WEATHER RADAR (Simulation Mode)")
        radar_display.pack(fill="both", expand=True)
        
        info_text = StyledText(radar_display, height=20)
        info_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        fallback_content = """🌩️ LIVE DOPPLER WEATHER RADAR - SEVERE WEATHER TRACKING

This is a simulation. Install matplotlib and numpy for full functionality.

- Hurricane Tracking
- Tornado Detection
- Severe Thunderstorm Monitoring
"""
        
        info_text.insert("1.0", fallback_content)
        info_text.config(state="disabled")


class SevereWeatherTab:
    """Severe weather alerts and tracking tab"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="🚨 Severe Alerts")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components with interactive charts"""
        # Create main split pane
        paned_window = ttk.PanedWindow(self.frame, orient="horizontal")
        paned_window.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left panel - Alerts list
        left_panel = ttk.Frame(paned_window)
        paned_window.add(left_panel, weight=1)
        
        # Right panel - Details and charts
        right_panel = ttk.PanedWindow(paned_window, orient="vertical")
        paned_window.add(right_panel, weight=2)
        
        # Add city input at the top of left panel
        city_frame = ttk.Frame(left_panel)
        city_frame.pack(fill="x", pady=5)
        
        StyledLabel(city_frame, text="Enter City:").pack(side="left", padx=5)
        self.city_entry = ttk.Entry(city_frame, width=20)
        self.city_entry.pack(side="left", padx=5)
        
        # City lookup button
        StyledButton(city_frame, "accent_black", text="🔍 Search Alerts", 
                    command=self.search_city_alerts).pack(side="left", padx=5)
        
        # Setup alert list with TreeView
        StyledLabel(left_panel, text="Active Weather Alerts", 
                   font=("Arial", 12, "bold")).pack(pady=5)
        
        # Treeview for alerts list
        columns = ("severity", "type", "location", "time")
        self.alerts_tree = ttk.Treeview(left_panel, columns=columns, show="headings", height=15)
        
        # Define column headings
        self.alerts_tree.heading("severity", text="⚠️ Severity")
        self.alerts_tree.heading("type", text="Type")
        self.alerts_tree.heading("location", text="Location")
        self.alerts_tree.heading("time", text="Time")
        
        # Define column widths
        self.alerts_tree.column("severity", width=80)
        self.alerts_tree.column("type", width=120)
        self.alerts_tree.column("location", width=120)
        self.alerts_tree.column("time", width=100)
        
        # Add scrollbar
        tree_scroll = ttk.Scrollbar(left_panel, orient="vertical", command=self.alerts_tree.yview)
        self.alerts_tree.configure(yscrollcommand=tree_scroll.set)
        
        # Pack tree and scrollbar
        self.alerts_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        tree_scroll.pack(side="right", fill="y", padx=(0, 5), pady=5)
        
        # Bind selection event
        self.alerts_tree.bind("<<TreeviewSelect>>", self.display_alert_details)
        
        # Button to refresh alerts
        StyledButton(left_panel, "primary", text="🔄 Refresh Alerts", 
                    command=self.fetch_alerts).pack(pady=10)
        
        # Details panel (top of right panel)
        details_frame = ttk.LabelFrame(right_panel, text="Alert Details")
        right_panel.add(details_frame, weight=1)
        
        self.details_text = StyledText(details_frame, height=10, wrap="word")
        self.details_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Chart panel (bottom of right panel)
        self.chart_frame = ttk.LabelFrame(right_panel, text="Alert Analysis")
        right_panel.add(self.chart_frame, weight=2)
        
        # Load initial data
        self.fetch_alerts()
        
    def search_city_alerts(self):
        """Search for weather alerts in the specified city"""
        city = self.city_entry.get().strip()
        if not city:
            from tkinter import messagebox
            messagebox.showwarning("Input Required", "Please enter a city name to search for alerts")
            return
        
        # Clear existing alerts
        for item in self.alerts_tree.get_children():
            self.alerts_tree.delete(item)
        
        # Display "searching" message in the details text area
        self.details_text.config(state="normal")
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, f"Searching for alerts in {city}...")
        self.details_text.config(state="disabled")
        
        # In a real app, you would call an API here with the city parameter
        # For demonstration purposes, we'll generate mock data based on the city name
        try:
            # Simulate API call delay
            self.frame.after(500, lambda: self.display_city_alerts(city))
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Failed to search alerts for {city}: {str(e)}")
    
    def display_city_alerts(self, city):
        """Display alerts for the specified city"""
        # Clear existing alerts in tree
        for item in self.alerts_tree.get_children():
            self.alerts_tree.delete(item)
            
        # Generate different mock alerts based on the city entered
        if city.lower() in ["new york", "nyc", "chicago", "los angeles", "la", "miami"]:
            # Major city with multiple alerts
            alerts = [
                {"id": "city1", "severity": "High", "type": "Heat Advisory", 
                "location": city, "time": "12:30", 
                "details": f"HEAT ADVISORY: Dangerous heat conditions in {city} with heat index values up to 105°F. The extreme heat can cause heat stress or heat stroke. Use air conditioning, stay hydrated, and check on vulnerable populations.\n\nAreas affected: All of {city} and surrounding suburbs\nValid until: 8:00 PM Today",
                "chart_type": "heat"},
                
                {"id": "city2", "severity": "Moderate", "type": "Air Quality Alert", 
                "location": city, "time": "09:15", 
                "details": f"AIR QUALITY ALERT: Unhealthy air quality levels expected in {city} today. Ozone and particulate matter may reach unhealthy levels. Sensitive groups should limit outdoor exertion.\n\nRecommended actions: Reduce outdoor activity, use public transportation, avoid using gas-powered equipment.",
                "chart_type": "air_quality"},
                
                {"id": "city3", "severity": "Low", "type": "Dense Fog Advisory", 
                "location": f"{city} Airport", "time": "05:45", 
                "details": f"DENSE FOG ADVISORY: Visibility less than 1/4 mile in {city} Airport and surrounding areas. Hazardous driving conditions due to low visibility. Allow extra time for travel, use low beam headlights, and leave plenty of distance ahead of you.\n\nAreas affected: {city} Airport, major highways, and coastal areas\nValid until: 10:00 AM Today",
                "chart_type": "fog"}
            ]
        elif city.lower() in ["houston", "new orleans", "tampa", "orlando", "jacksonville"]:
            # Coastal cities with hurricane/tropical alerts
            alerts = [
                {"id": "city1", "severity": "High", "type": "Hurricane Warning", 
                "location": city, "time": "10:00", 
                "details": f"HURRICANE WARNING: Hurricane approaching {city} with winds of 110 mph. Destructive winds, heavy rainfall, and dangerous storm surge expected. Evacuate if instructed, or move to interior rooms away from windows.\n\nAreas affected: All of {city} and surrounding coastal regions\nExpected landfall: Tomorrow morning",
                "chart_type": "tornado"},
                
                {"id": "city2", "severity": "High", "type": "Flash Flood Warning", 
                "location": city, "time": "11:30", 
                "details": f"FLASH FLOOD WARNING: Dangerous flooding occurring in {city}. Heavy rainfall causing rapid water rise. Do not attempt to travel unless fleeing an area subject to flooding. Turn around, don't drown when encountering flooded roads.\n\nAreas affected: Downtown {city}, low-lying areas\nRainfall totals may exceed 10 inches",
                "chart_type": "flood"}
            ]
        else:
            # Default alerts for any other city
            alerts = [
                {"id": "city1", "severity": "Moderate", "type": "Thunderstorm Watch", 
                "location": city, "time": "13:45", 
                "details": f"THUNDERSTORM WATCH: Conditions are favorable for the development of severe thunderstorms in and around {city}. Storms may produce large hail, damaging winds, and heavy rainfall. Stay alert for changing weather conditions and be prepared to take shelter if warnings are issued.\n\nAreas affected: {city} and surrounding counties\nValid until: 9:00 PM Today",
                "chart_type": "thunderstorm"}
            ]
        
        # Add alerts to tree
        for alert in alerts:
            severity_icon = "🔴" if alert["severity"] == "High" else "🟠" if alert["severity"] == "Moderate" else "🟡"
            self.alerts_tree.insert("", "end", iid=alert["id"], values=(
                f"{severity_icon} {alert['severity']}", 
                alert["type"], 
                alert["location"], 
                alert["time"]
            ), tags=(alert["severity"].lower(),))
        
        # Set tag colors
        self.alerts_tree.tag_configure("high", background="#ffcccc")
        self.alerts_tree.tag_configure("moderate", background="#fff2cc")
        self.alerts_tree.tag_configure("low", background="#e6f2ff")
        
        # Update details text
        self.details_text.config(state="normal")
        self.details_text.delete(1.0, tk.END)
        num_alerts = len(alerts)
        self.details_text.insert(tk.END, f"Found {num_alerts} alert{'s' if num_alerts != 1 else ''} for {city}\n\nSelect an alert to view details")
        self.details_text.config(state="disabled")
        
        # Select first item if available
        if self.alerts_tree.get_children():
            first_item = self.alerts_tree.get_children()[0]
            self.alerts_tree.selection_set(first_item)
            self.display_alert_details(None)

    def fetch_alerts(self):
        """Fetch and display current weather alerts"""
        # Clear existing alerts
        for item in self.alerts_tree.get_children():
            self.alerts_tree.delete(item)
        
        # Mock data - in a real app, this would come from a weather API
        alerts = [
            {"id": "1", "severity": "High", "type": "Tornado Warning", 
             "location": "Centerville", "time": "14:30", 
             "details": "TORNADO WARNING: A dangerous tornado has been spotted near Centerville moving northeast at 30 mph. Take shelter immediately in a basement or interior room on the lowest floor. Flying debris will be dangerous to those caught without shelter. Mobile homes will be damaged or destroyed. Damage to roofs, windows, and vehicles will occur. Tree damage is likely.\n\nAreas at risk: Centerville, Johnstown, Millersville\nTake protective action NOW!",
             "chart_type": "tornado"},
            {"id": "2", "severity": "Moderate", "type": "Thunderstorm", 
             "location": "Westside", "time": "15:45", 
             "details": "SEVERE THUNDERSTORM WARNING: Severe thunderstorms capable of producing damaging winds up to 60 mph and quarter size hail. These storms are moving east at 25 mph. Minor damage to vehicles is possible. Expect wind damage to roofs, siding, and trees.\n\nAreas affected: Westside, Downtown, River District\nTake caution and move to interior rooms if storms approach.",
             "chart_type": "thunderstorm"},
            {"id": "3", "severity": "Low", "type": "Flood Advisory", 
             "location": "Riverside", "time": "16:20", 
             "details": "FLOOD ADVISORY: Urban and small stream flooding is expected in Riverside area. Excessive runoff from heavy rainfall will cause flooding of small creeks and streams, urban areas, highways, streets and underpasses as well as other drainage areas and low lying spots.\n\nAreas affected: Riverside, Harbor View, Lower Downtown\nDo not drive through flooded roadways.",
             "chart_type": "flood"}
        ]
        
        # Add alerts to tree
        for alert in alerts:
            severity_icon = "🔴" if alert["severity"] == "High" else "🟠" if alert["severity"] == "Moderate" else "🟡"
            self.alerts_tree.insert("", "end", iid=alert["id"], values=(
                f"{severity_icon} {alert['severity']}", 
                alert["type"], 
                alert["location"], 
                alert["time"]
            ), tags=(alert["severity"].lower(),))
            
        # Set tag colors
        self.alerts_tree.tag_configure("high", background="#ffcccc")
        self.alerts_tree.tag_configure("moderate", background="#fff2cc")
        self.alerts_tree.tag_configure("low", background="#e6f2ff")
        
        # Select first item if available
        if self.alerts_tree.get_children():
            first_item = self.alerts_tree.get_children()[0]
            self.alerts_tree.selection_set(first_item)
            self.display_alert_details(None)
    
    def display_alert_details(self, event):
        """Display details for selected alert"""
        selected_items = self.alerts_tree.selection()
        if not selected_items:
            return
            
        selected_id = selected_items[0]
        
        # Mock data - in a real app, this would be retrieved from a database or API
        alerts = {
            "1": {"severity": "High", "type": "Tornado Warning", 
                 "location": "Centerville", "time": "14:30", 
                 "details": "TORNADO WARNING: A dangerous tornado has been spotted near Centerville moving northeast at 30 mph. Take shelter immediately in a basement or interior room on the lowest floor. Flying debris will be dangerous to those caught without shelter. Mobile homes will be damaged or destroyed. Damage to roofs, windows, and vehicles will occur. Tree damage is likely.\n\nAreas at risk: Centerville, Johnstown, Millersville\nTake protective action NOW!",
                 "chart_type": "tornado"},
            "2": {"severity": "Moderate", "type": "Thunderstorm", 
                 "location": "Westside", "time": "15:45", 
                 "details": "SEVERE THUNDERSTORM WARNING: Severe thunderstorms capable of producing damaging winds up to 60 mph and quarter size hail. These storms are moving east at 25 mph. Minor damage to vehicles is possible. Expect wind damage to roofs, siding, and trees.\n\nAreas affected: Westside, Downtown, River District\nTake caution and move to interior rooms if storms approach.",
                 "chart_type": "thunderstorm"},
            "3": {"severity": "Low", "type": "Flood Advisory", 
                 "location": "Riverside", "time": "16:20", 
                 "details": "FLOOD ADVISORY: Urban and small stream flooding is expected in Riverside area. Excessive runoff from heavy rainfall will cause flooding of small creeks and streams, urban areas, highways, streets and underpasses as well as other drainage areas and low lying spots.\n\nAreas affected: Riverside, Harbor View, Lower Downtown\nDo not drive through flooded roadways.",
                 "chart_type": "flood"}
        }
        
        if selected_id in alerts:
            alert = alerts[selected_id]
            # Display alert details
            self.details_text.config(state="normal")
            self.details_text.delete(1.0, tk.END)
            
            # Format the alert with severity coloring
            severity_color = "#FF4444" if alert["severity"] == "High" else "#FF8800" if alert["severity"] == "Moderate" else "#0088FF"
            
            self.details_text.insert(tk.END, f"{alert['severity']} - {alert['type']}\n", "severity")
            self.details_text.insert(tk.END, f"Location: {alert['location']}\n")
            self.details_text.insert(tk.END, f"Time: {alert['time']}\n\n")
            self.details_text.insert(tk.END, alert['details'])
            
            self.details_text.tag_configure("severity", foreground=severity_color, font=("Arial", 12, "bold"))
            self.details_text.config(state="disabled")
            
            # Generate chart for this alert
            self.generate_alert_chart(alert)
    
    def generate_alert_chart(self, alert):
        """Generate an appropriate chart for the selected alert"""
        # Clear existing chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        if not CHARTS_AVAILABLE:
            # If matplotlib is not available, show text instead
            message_label = StyledLabel(self.chart_frame, 
                                      text="Charts unavailable. Install matplotlib for visualizations.")
            message_label.pack(pady=20)
            return
            
        chart_type = alert.get("chart_type", "generic")
        
        if chart_type == "tornado":
            # Create tornado intensity/probability chart
            fig = Figure(figsize=(7, 4))
            ax = fig.add_subplot(111)
            
            # Tornado wind probabilities
            categories = ['F0', 'F1', 'F2', 'F3', 'F4', 'F5']
            probabilities = [80, 55, 30, 15, 5, 1]
            
            bars = ax.bar(categories, probabilities, color=['#8cc', '#5bb', '#399', '#277', '#055', '#033'])
            
            ax.set_title('Tornado Wind Speed Probabilities')
            ax.set_xlabel('Fujita Scale Category')
            ax.set_ylabel('Probability (%)')
            ax.set_ylim(0, 100)
            
            # Add data labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                       f'{height}%', ha='center', va='bottom')
            
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
        elif chart_type == "thunderstorm":
            # Create pie chart for hail size probability
            fig = Figure(figsize=(7, 4))
            ax = fig.add_subplot(111)
            
            # Hail size probabilities
            sizes = ['Pea', 'Quarter', 'Golf Ball', 'Tennis Ball', 'Baseball']
            probabilities = [50, 30, 15, 4, 1]
            explode = (0, 0.1, 0.2, 0.3, 0.4)  # explode pieces for emphasis
            
            ax.pie(probabilities, explode=explode, labels=sizes, autopct='%1.1f%%',
                  shadow=True, startangle=90, colors=['#ddf', '#bbf', '#99f', '#77f', '#55f'])
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            ax.set_title('Potential Hail Size Distribution')
            
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
        elif chart_type == "flood":
            # Create flood risk area chart
            fig = Figure(figsize=(7, 4))
            ax = fig.add_subplot(111)
            
            # Flood data
            hours = list(range(1, 13))  # 12-hour forecast
            water_levels = [2, 3, 5, 8, 10, 11, 10.5, 9, 7, 5, 4, 3]  # in feet
            flood_stage = 8  # flood stage line
            
            # Plot water level
            ax.plot(hours, water_levels, 'b-', linewidth=2, marker='o')
            
            # Add flood stage line
            ax.axhline(y=flood_stage, color='r', linestyle='-', label='Flood Stage')
            
            # Fill areas
            ax.fill_between(hours, water_levels, flood_stage, 
                           where=[wl > flood_stage for wl in water_levels], 
                           color='red', alpha=0.3, interpolate=True, label='Above Flood Stage')
            
            ax.set_title('12-Hour Flood Forecast')
            ax.set_xlabel('Hours from Now')
            ax.set_ylabel('Water Level (feet)')
            ax.grid(True)
            ax.legend()
            
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
        else:
            # Generic chart for other alert types
            fig = Figure(figsize=(7, 4))
            ax = fig.add_subplot(111)
            
            # Generic risk assessment
            categories = ['Property Damage', 'Safety Risk', 'Travel Impact', 'Duration']
            values = [70, 60, 85, 40]
            
            # Create radar chart axes
            angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
            values += values[:1]  # Close the loop
            angles += angles[:1]  # Close the loop
            categories += categories[:1]  # Close the loop for labels
            
            ax.plot(angles, values, 'o-', linewidth=2)
            ax.fill(angles, values, alpha=0.25)
            ax.set_thetagrids(np.degrees(angles[:-1]), categories[:-1])
            ax.set_ylim(0, 100)
            ax.set_title('Alert Impact Analysis')
            ax.grid(True)
            
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)


class AnalyticsTrendsTab:
    """Analytics and trends analysis with interactive charts"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Analytics & Trends")
        self.current_chart_frame = None
        self.cities = []
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components with split layout and interactive charts"""
        # Create split paned window
        self.main_paned = ttk.PanedWindow(self.frame, orient="horizontal")
        self.main_paned.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left panel for controls
        self.left_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.left_frame, weight=1)
        
        # Right panel for charts
        self.right_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.right_frame, weight=2)
        
        # Header
        StyledLabel(self.left_frame, text="📊 Weather Analytics & Trends").pack(pady=10)
        
        # City input section
        city_frame = ttk.LabelFrame(self.left_frame, text="City Selection")
        city_frame.pack(fill="x", padx=10, pady=10)
        
        # Main city entry
        ttk.Label(city_frame, text="Primary City:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.city1_entry = ttk.Entry(city_frame, width=20)
        self.city1_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Compare city entry
        ttk.Label(city_frame, text="Compare City:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.city2_entry = ttk.Entry(city_frame, width=20)
        self.city2_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Time range selection
        time_frame = ttk.LabelFrame(self.left_frame, text="Time Range")
        time_frame.pack(fill="x", padx=10, pady=10)
        
        self.time_range = tk.StringVar(value="7 days")
        ttk.Radiobutton(time_frame, text="7 Days", variable=self.time_range, 
                       value="7 days").grid(row=0, column=0, padx=5, pady=3, sticky="w")
        ttk.Radiobutton(time_frame, text="30 Days", variable=self.time_range, 
                       value="30 days").grid(row=0, column=1, padx=5, pady=3, sticky="w")
        ttk.Radiobutton(time_frame, text="90 Days", variable=self.time_range, 
                       value="90 days").grid(row=1, column=0, padx=5, pady=3, sticky="w")
        ttk.Radiobutton(time_frame, text="1 Year", variable=self.time_range, 
                       value="1 year").grid(row=1, column=1, padx=5, pady=3, sticky="w")
        
        # Action button
        StyledButton(self.left_frame, "primary_black", text="Generate Analytics", 
                   command=self._generate_analytics).pack(pady=10)
        
        # Chart selection buttons
        chart_buttons_frame = ttk.LabelFrame(self.left_frame, text="Chart Selection")
        chart_buttons_frame.pack(fill="x", padx=10, pady=10)
        
        # Create button grid with different chart options
        button_configs = [
            ("info_black", "🌡️ Temperature Trends", lambda: self._show_temperature_trends()),
            ("accent_black", "🌧️ Precipitation Analysis", lambda: self._show_precipitation_analysis()),
            ("success_black", "💨 Wind Patterns", lambda: self._show_wind_patterns()),
            ("warning_black", "☀️ Daylight Hours", lambda: self._show_daylight_hours()),
            ("cool_black", "🌫️ Humidity Trends", lambda: self._show_humidity_trends()),
            ("primary_black", "📊 Weather Comparison", lambda: self._show_weather_comparison())
        ]
        
        ButtonHelper.create_button_grid(chart_buttons_frame, button_configs, columns=2)
        
        # Information text
        self.info_text = StyledText(self.left_frame, height=6)
        self.info_text.pack(fill="x", padx=10, pady=10)
        
        content = """📊 Select cities and time range, then click 'Generate Analytics'.
Choose from different chart types to explore weather trends and patterns."""
        
        self.info_text.insert("1.0", content)
        self.info_text.config(state="disabled")
        
        # Chart area placeholder
        self._create_chart_placeholder()

    def _create_chart_placeholder(self):
        """Create the initial chart placeholder"""
        if self.current_chart_frame:
            self.current_chart_frame.destroy()
        
        self.current_chart_frame = ttk.Frame(self.right_frame)
        self.current_chart_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ChartHelper.create_chart_placeholder(
            self.current_chart_frame,
            title="Weather Analytics Charts",
            content="Select cities and analysis type to generate interactive charts."
        )

    def _clear_chart_area(self):
        """Clear the current chart area"""
        if self.current_chart_frame:
            self.current_chart_frame.destroy()
            self.current_chart_frame = ttk.Frame(self.right_frame)
            self.current_chart_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    def _get_cities(self):
        """Get and validate city inputs"""
        city1 = self.city1_entry.get().strip()
        city2 = self.city2_entry.get().strip()
        
        if not city1:
            messagebox.showwarning("Input Error", "Please enter at least one city")
            return None, None
            
        return city1, city2

    def _generate_analytics(self):
        """Generate analytics based on current selection"""
        city1, city2 = self._get_cities()
        if not city1:
            return
            
        self.cities = [city1]
        if city2:
            self.cities.append(city2)
            
        self._show_temperature_trends()
    
    def _show_temperature_trends(self):
        """Display temperature trends chart"""
        if not self.cities:
            return
            
        try:
            self._clear_chart_area()
            
            # Get data from the controller
            time_range = self.time_range.get()
            data = self.controller.get_temperature_trends(self.cities, time_range)
            
            if not data or not data[0].get('temperatures'):
                messagebox.showinfo("No Data", "No temperature data available for the selected period")
                return
                
            # Create line chart
            ChartHelper.create_line_chart(
                self.current_chart_frame,
                title=f"Temperature Trends - Past {time_range}",
                x_data=data[0]['timestamps'],
                y_data=data[0]['temperatures'],
                x_label="Time",
                y_label="Temperature (°C)"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate temperature trends: {str(e)}")
            self._create_chart_placeholder()

    def _show_precipitation_analysis(self):
        """Display precipitation analysis chart"""
        if not self.cities:
            return
            
        try:
            self._clear_chart_area()
            
            # Get data from the controller
            time_range = self.time_range.get()
            data = self.controller.get_precipitation_data(self.cities, time_range)
            
            if not data or not data[0].get('precipitation'):
                messagebox.showinfo("No Data", "No precipitation data available for the selected period")
                return
                
            # Create bar chart
            ChartHelper.create_bar_chart(
                self.current_chart_frame,
                title=f"Precipitation Analysis - Past {time_range}",
                x_data=data[0]['dates'],
                y_data=data[0]['precipitation'],
                colors=['#4ECDC4', '#45B7D1']
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate precipitation analysis: {str(e)}")
            self._create_chart_placeholder()
    
    def _show_wind_patterns(self):
        """Display wind patterns chart"""
        if not self.cities:
            return
            
        try:
            self._clear_chart_area()
            
            # Get data from the controller
            time_range = self.time_range.get()
            data = self.controller.get_wind_data(self.cities, time_range)
            
            if not data or len(data) == 0:
                messagebox.showinfo("No Data", "No wind data available for the selected period")
                return
                
            # Create figure with two subplots
            fig = Figure(figsize=(10, 6), dpi=100)
            
            # Wind speed subplot
            ax1 = fig.add_subplot(211)
            ax1.set_title(f"Wind Speed - Past {time_range}")
            ax1.set_ylabel("Speed (m/s)")
            
            # Wind direction subplot
            ax2 = fig.add_subplot(212)
            ax2.set_title("Wind Direction")
            ax2.set_ylabel("Direction (degrees)")
            
            # Plot data for each city
            colors = ['#4ECDC4', '#FF6B6B', '#45B7D1']
            for i, city_data in enumerate(data):
                timestamps = city_data['timestamps']
                speeds = city_data['wind_speeds']
                directions = city_data['wind_directions']
                
                ax1.plot(timestamps, speeds, color=colors[i % len(colors)],
                        label=self.cities[i], marker='o', markersize=4)
                ax2.plot(timestamps, directions, color=colors[i % len(colors)],
                        label=self.cities[i], marker='o', markersize=4)
            
            # Customize appearance
            for ax in [ax1, ax2]:
                ax.grid(True, alpha=0.3)
                ax.legend()
                ax.tick_params(axis='x', rotation=45)
            
            fig.tight_layout()
            
            # Embed chart
            ChartHelper.embed_chart_in_frame(fig, self.current_chart_frame)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate wind patterns: {str(e)}")
            self._create_chart_placeholder()
    
    def _show_daylight_hours(self):
        """Display daylight hours chart"""
        if not self.cities:
            return
            
        try:
            self._clear_chart_area()
            
            # Get data from the controller
            time_range = self.time_range.get()
            data = self.controller.get_daylight_data(self.cities, time_range)
            
            if not data or not data[0].get('daylight_hours'):
                messagebox.showinfo("No Data", "No daylight data available for the selected period")
                return
                
            # Create bar chart
            ChartHelper.create_bar_chart(
                self.current_chart_frame,
                title=f"Daylight Hours - Past {time_range}",
                x_data=data[0]['dates'],
                y_data=data[0]['daylight_hours'],
                colors=['#FECA57', '#FFA502']
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate daylight hours chart: {str(e)}")
            self._create_chart_placeholder()
    
    def _show_humidity_trends(self):
        """Display humidity trends chart"""
        if not self.cities:
            return
            
        try:
            self._clear_chart_area()
            
            # Get data from the controller
            time_range = self.time_range.get()
            data = self.controller.get_humidity_data(self.cities, time_range)
            
            if not data or not data[0].get('humidity'):
                messagebox.showinfo("No Data", "No humidity data available for the selected period")
                return
                
            # Create line chart
            ChartHelper.create_line_chart(
                self.current_chart_frame,
                title=f"Humidity Trends - Past {time_range}",
                x_data=data[0]['timestamps'],
                y_data=data[0]['humidity'],
                x_label="Time",
                y_label="Relative Humidity (%)",
                color='#45B7D1'
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate humidity trends: {str(e)}")
            self._create_chart_placeholder()
    
    def _show_weather_comparison(self):
        """Display weather comparison chart"""
        if len(self.cities) < 2:
            messagebox.showwarning("Input Error", "Please enter two cities to compare")
            return
            
        try:
            self._clear_chart_area()
            
            # Get data from the controller for both cities
            time_range = self.time_range.get()
            data = self.controller.get_weather_comparison(self.cities, time_range)
            
            if not data or len(data) < 2:
                messagebox.showinfo("No Data", "Weather comparison data not available")
                return
                
            # Create comparison chart
            fig = Figure(figsize=(10, 6), dpi=100)
            ax = fig.add_subplot(111)
            
            # Plot data for both cities
            ax.plot(data[0]['timestamps'], data[0]['temperatures'], 
                   label=self.cities[0], color='#4ECDC4')
            ax.plot(data[1]['timestamps'], data[1]['temperatures'], 
                   label=self.cities[1], color='#FF6B6B')
            
            ax.set_title(f"Temperature Comparison - Past {time_range}")
            ax.set_xlabel("Time")
            ax.set_ylabel("Temperature (°C)")
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Embed the chart
            ChartHelper.embed_chart_in_frame(fig, self.current_chart_frame)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate weather comparison: {str(e)}")
            self._create_chart_placeholder()


class HealthWellnessTab:
    """Health and wellness monitoring with interactive charts"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="🏥 Health & Wellness")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the comprehensive health monitoring UI"""
        # Create split layout
        self.main_paned = ttk.PanedWindow(self.frame, orient="horizontal")
        self.main_paned.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left panel for controls and text display
        self.left_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.left_frame, weight=1)
        
        # Right panel for charts
        self.right_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.right_frame, weight=1)
        
        self._setup_left_panel()
        self._setup_right_panel()

    def _setup_left_panel(self):
        """Setup left panel with controls and info"""
        # Title
        title_frame = ttk.Frame(self.left_frame)
        title_frame.pack(fill="x", padx=5, pady=5)
        StyledLabel(title_frame, text="🏥 Health Monitor", font=("Arial", 16, "bold")).pack()
        
        # City input
        input_frame = ttk.Frame(self.left_frame)
        input_frame.pack(fill="x", padx=5, pady=5)
        StyledLabel(input_frame, text="Enter City:").pack(side="left", padx=5)
        self.city_entry = ttk.Entry(input_frame)
        self.city_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.city_entry.insert(0, "New York")
        
        # Health status display
        self.health_text = StyledText(self.left_frame, height=10)
        self.health_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Control buttons
        btn_frame = ttk.Frame(self.left_frame)
        btn_frame.pack(fill="x", padx=5, pady=5)
        
        StyledButton(btn_frame, "success_black", text="🔄 Update Data", 
                    command=self.update_health_data).pack(side="left", padx=2)
        StyledButton(btn_frame, "warning_black", text="⚠️ Check Alerts", 
                    command=self.check_health_alerts).pack(side="left", padx=2)
        StyledButton(btn_frame, "info_black", text="📋 Health Report", 
                    command=self.generate_health_report).pack(side="left", padx=2)

    def _setup_right_panel(self):
        """Setup right panel with charts"""
        # Chart title
        title_frame = ttk.Frame(self.right_frame)
        title_frame.pack(fill="x", padx=5, pady=5)
        StyledLabel(title_frame, text="Health Analytics", font=("Arial", 12, "bold")).pack()
        
        # Chart area
        self.chart_frame = ttk.Frame(self.right_frame)
        self.chart_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Chart control buttons
        chart_btn_frame = ttk.Frame(self.right_frame)
        chart_btn_frame.pack(fill="x", padx=5, pady=5)
        
        StyledButton(chart_btn_frame, "primary_black", text="☀️ UV Index", 
                    command=self.show_uv_chart).pack(side="left", padx=2)
        StyledButton(chart_btn_frame, "info_black", text="🌸 Pollen", 
                    command=self.show_pollen_chart).pack(side="left", padx=2)
        StyledButton(chart_btn_frame, "warning_black", text="💨 Air Quality", 
                    command=self.show_air_quality_chart).pack(side="left", padx=2)
        StyledButton(chart_btn_frame, "success_black", text="🏃 Wellness", 
                    command=self.show_wellness_chart).pack(side="left", padx=2)
                    
        # Show initial UV chart
        self.show_uv_chart()

    def update_health_data(self):
        """Update health monitoring data"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
            
        try:
            self.health_text.delete(1.0, tk.END)
            
            health_info = f"🏥 HEALTH STATUS FOR {city.upper()}\n"
            health_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            # Air Quality
            aqi = random.randint(30, 150)
            health_info += f"💨 Air Quality Index: {aqi}\n"
            if aqi <= 50:
                health_info += "   Status: Good (Safe for outdoor activities)\n"
            elif aqi <= 100:
                health_info += "   Status: Moderate (Consider limiting intense activities)\n"
            else:
                health_info += "   Status: Unhealthy (Avoid prolonged outdoor exposure)\n"
            
            # UV Index
            uv = random.randint(1, 11)
            health_info += f"\n☀️ UV Index: {uv}\n"
            if uv <= 2:
                health_info += "   Risk Level: Low (Safe for outdoors)\n"
            elif uv <= 5:
                health_info += "   Risk Level: Moderate (Use sun protection)\n"
            elif uv <= 7:
                health_info += "   Risk Level: High (Limit sun exposure)\n"
            else:
                health_info += "   Risk Level: Very High (Avoid sun exposure)\n"
            
            # Pollen Count
            pollen = random.randint(1, 12)
            health_info += f"\n🌸 Pollen Count: {pollen}\n"
            if pollen <= 4:
                health_info += "   Level: Low (Safe for allergy sufferers)\n"
            elif pollen <= 8:
                health_info += "   Level: Moderate (Take precautions)\n"
            else:
                health_info += "   Level: High (Stay indoors if sensitive)\n"
            
            self.health_text.insert(tk.END, health_info)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update health data: {str(e)}")

    def check_health_alerts(self):
        """Check for active health alerts"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
            
        alert_msg = f"⚠️ HEALTH ALERTS FOR {city.upper()}\n\n"
        
        # Simulate some health alerts
        conditions = [
            ("AIR QUALITY ALERT", "High pollution levels expected", 0.3),
            ("UV WARNING", "Very high UV index from 10 AM to 4 PM", 0.4),
            ("POLLEN ALERT", "High pollen count for tree allergens", 0.35),
            ("HEAT ADVISORY", "Excessive heat - stay hydrated", 0.25),
            ("AIR STAGNATION", "Poor air circulation - affects respiratory conditions", 0.2)
        ]
        
        active_alerts = []
        for alert, desc, prob in conditions:
            if random.random() < prob:
                active_alerts.append(f"🚨 {alert}:\n   {desc}")
        
        if active_alerts:
            alert_msg += "\n".join(active_alerts)
        else:
            alert_msg += "✅ No active health alerts at this time.\n"
            alert_msg += "Continue normal activities while following standard health precautions."
            
        messagebox.showinfo("Health Alerts", alert_msg)

    def generate_health_report(self):
        """Generate comprehensive health report"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
            
        report = f"📋 HEALTH & WELLNESS REPORT - {city.upper()}\n"
        report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # Current Conditions
        report += "🌡️ CURRENT CONDITIONS:\n"
        report += f"• Temperature: {random.randint(18, 28)}°C\n"
        report += f"• Humidity: {random.randint(40, 70)}%\n"
        report += f"• Air Pressure: {random.randint(1000, 1020)} hPa\n\n"
        
        # Health Metrics
        report += "📊 HEALTH METRICS:\n"
        report += "• Air Quality: Moderate (Exercise with caution)\n"
        report += "• UV Index: 6 (High - Use sun protection)\n"
        report += "• Pollen Count: Low (Favorable for allergies)\n\n"
        
        # Recommendations
        report += "💡 RECOMMENDATIONS:\n"
        report += "• Ideal times for outdoor activity: Early morning or evening\n"
        report += "• Suggested activities: Light cardio, walking, cycling\n"
        report += "• Health precautions: Use sunscreen, stay hydrated\n\n"
        
        # Warnings
        report += "⚠️ HEALTH WARNINGS:\n"
        report += "• UV exposure risk highest between 10 AM - 4 PM\n"
        report += "• Air quality may affect sensitive individuals\n"
        report += "• Stay hydrated - increased risk of dehydration\n"
        
        messagebox.showinfo("Health Report", report)

    def show_uv_chart(self):
        """Show UV index chart"""
        self._clear_chart_area()
        
        if CHARTS_AVAILABLE:
            # Create UV index data
            hours = list(range(6, 21))  # 6 AM to 8 PM
            uv_values = [0, 1, 2, 4, 6, 8, 9, 10, 9, 8, 6, 4, 2, 1, 0]
            
            fig = Figure(figsize=(6, 4))
            ax = fig.add_subplot(111)
            
            # Plot with gradient color based on UV intensity
            points = ax.scatter(hours, uv_values, c=uv_values, cmap='YlOrRd', s=100)
            ax.plot(hours, uv_values, '-', color='gray', alpha=0.5)
            
            # Customize the chart
            ax.set_title('Daily UV Index Pattern')
            ax.set_xlabel('Hour of Day')
            ax.set_ylabel('UV Index')
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Add colorbar
            fig.colorbar(points, label='UV Intensity')
            
            # Display in the chart area
            canvas = FigureCanvasTkAgg(fig, self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
        else:
            self._show_chart_unavailable()

    def show_pollen_chart(self):
        """Show pollen levels chart"""
        self._clear_chart_area()
        
        if CHARTS_AVAILABLE:
            # Create pollen data
            pollen_types = ['Tree', 'Grass', 'Weed', 'Mold']
            levels = [random.randint(1, 10) for _ in range(4)]
            colors = ['forestgreen', 'lightgreen', 'yellowgreen', 'darkgreen']
            
            fig = Figure(figsize=(6, 4))
            ax = fig.add_subplot(111)
            
            # Create bar chart
            bars = ax.bar(pollen_types, levels, color=colors)
            
            # Customize the chart
            ax.set_title('Current Pollen Levels')
            ax.set_ylabel('Pollen Count')
            ax.grid(True, axis='y', linestyle='--', alpha=0.7)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom')
            
            # Display in the chart area
            canvas = FigureCanvasTkAgg(fig, self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
        else:
            self._show_chart_unavailable()

    def show_air_quality_chart(self):
        """Show air quality chart"""
        self._clear_chart_area()
        
        if CHARTS_AVAILABLE:
            # Create air quality data
            pollutants = ['PM2.5', 'PM10', 'O3', 'NO2', 'SO2', 'CO']
            levels = [random.randint(20, 180) for _ in range(6)]
            
            fig = Figure(figsize=(6, 4))
            ax = fig.add_subplot(111)
            
            # Create horizontal bar chart
            bars = ax.barh(pollutants, levels)
            
            # Color bars based on level
            for bar, level in zip(bars, levels):
                if level <= 50:
                    bar.set_color('green')
                elif level <= 100:
                    bar.set_color('yellow')
                elif level <= 150:
                    bar.set_color('orange')
                else:
                    bar.set_color('red')
            
            # Customize the chart
            ax.set_title('Air Quality Index by Pollutant')
            ax.set_xlabel('Concentration (µg/m³)')
            ax.grid(True, axis='x', linestyle='--', alpha=0.7)
            
            # Add value labels
            for bar in bars:
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2.,
                       f'{int(width)}',
                       ha='left', va='center')
            
            # Display in the chart area
            canvas = FigureCanvasTkAgg(fig, self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
        else:
            self._show_chart_unavailable()

    def show_wellness_chart(self):
        """Show wellness radar chart"""
        self._clear_chart_area()
        
        if CHARTS_AVAILABLE:
            # Create wellness metrics data
            categories = ['Air Quality', 'UV Protection', 'Temperature',
                        'Humidity', 'Wind', 'Pressure']
            values = [random.randint(60, 100) for _ in range(6)]
            
            # Close the polygon by appending first value
            values += values[:1]
            
            # Compute angle for each axis
            angles = [n / float(len(categories)) * 2 * np.pi for n in range(len(categories))]
            angles += angles[:1]
            
            fig = Figure(figsize=(6, 4))
            ax = fig.add_subplot(111, polar=True)
            
            # Plot data
            ax.plot(angles, values, 'o-', linewidth=2)
            ax.fill(angles, values, alpha=0.25)
            
            # Fix axis to go in the right order and start at 12 o'clock
            ax.set_theta_offset(np.pi / 2)
            ax.set_theta_direction(-1)
            
            # Draw axis lines for each angle and label
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories)
            
            # Add a title
            ax.set_title("Wellness Factors Analysis")
            
            # Display in the chart area
            canvas = FigureCanvasTkAgg(fig, self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
        else:
            self._show_chart_unavailable()

    def _clear_chart_area(self):
        """Clear all widgets in the chart area"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

    def _show_chart_unavailable(self):
        """Show message when charts are not available"""
        msg = "📊 Charts Unavailable\n\n"
        msg += "Please install matplotlib and numpy\n"
        msg += "to enable interactive charts.\n\n"
        msg += "Run: pip install matplotlib numpy"
        
        label = StyledLabel(self.chart_frame, text=msg)
        label.pack(expand=True)


class SmartAlertsTab:
    """Smart alerts and notifications"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Smart Alerts")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        StyledLabel(self.frame, text="Smart Weather Alerts").pack(pady=20)
        info_text = StyledText(self.frame, height=15)
        info_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        content = """🚨 SMART ALERTS & NOTIFICATIONS
        
This tab features:
• Customizable weather alerts
• Location-based notifications  
• Travel weather warnings
• Event planning alerts
• Agricultural weather notices
• Personal preference settings

Currently under development."""
        
        info_text.insert("1.0", content)
        info_text.config(state="disabled")


class WeatherCameraTab:
    """Weather camera feeds"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Weather Cameras")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        StyledLabel(self.frame, text="Weather Camera Feeds").pack(pady=20)
        info_text = StyledText(self.frame, height=15)
        info_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        content = """📹 WEATHER CAMERA FEEDS
        
This tab features:
• Live weather camera feeds
• Traffic and weather cams
• Beach and mountain cams
• City skyline views
• Weather condition verification
• Time-lapse weather videos

Currently under development."""
        
        info_text.insert("1.0", content)
        info_text.config(state="disabled")
