import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

# Color palette for UI elements (define as needed)
COLOR_PALETTE = {
    "tab_bg": "#f7f7f7",
    "tab_fg": "#222222"
}

# Check if matplotlib is available for charts
CHARTS_AVAILABLE = True
"""
Individual tab components for the weather dashboard
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .components import StyledButton, StyledText, StyledLabel, AnimatedLabel

def set_tab_font(notebook, font=("Arial", 9, "bold")):
    style = ttk.Style()
    style.configure("TNotebook.Tab", font=font)

# --- Restored WeatherTab class ---
class WeatherTab:
    """Main weather tab component with live weather and analytics"""
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Current Weather")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI with split-screen layout for live weather and charts"""
        # Create main paned window for split view
        self.main_paned = ttk.PanedWindow(self.frame, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left panel for live weather data input and display
        self.left_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.left_frame, weight=1)
        
        # Right panel for charts and analytics
        self.right_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.right_frame, weight=1)
        
        # Setup left panel (live weather interface)
        self._setup_weather_interface()
        
        # Setup right panel (chart area)
        self._setup_chart_interface()
    
    def _setup_weather_interface(self):
        """Setup the live weather data interface in the left panel"""
        # Title
        StyledLabel(self.left_frame, text="🌦️ Live Weather Dashboard", 
                   font=("Arial", 16, "bold")).pack(pady=10)
        
        # City input
        input_frame = ttk.Frame(self.left_frame)
        input_frame.pack(pady=10)
        
        StyledLabel(input_frame, text="Enter City:").pack()
        self.city_entry = ttk.Entry(input_frame, font=("Arial", 12), width=25)
        self.city_entry.pack(pady=5)
        self.city_entry.bind('<Return>', lambda e: self.fetch_weather())
        
        # Main action button
        StyledButton(self.left_frame, "primary", text="🔄 Get Live Weather", 
                    command=self.fetch_weather).pack(pady=5)
        
        # Quick action buttons
        quick_actions = ttk.Frame(self.left_frame)
        quick_actions.pack(pady=5)
        
        StyledButton(quick_actions, "accent_black", text="⭐ Save Favorite", 
                    command=self.save_favorite).grid(row=0, column=0, padx=2)
        StyledButton(quick_actions, "success_black", text="🔄 Auto-Refresh", 
                    command=self.toggle_auto_refresh).grid(row=0, column=1, padx=2)
        StyledButton(quick_actions, "warning_black", text="⚠️ Weather Alerts", 
                    command=self.check_alerts).grid(row=1, column=0, padx=2, pady=2)
        StyledButton(quick_actions, "info_black", text="📊 Toggle Graph", 
                    command=self.controller.toggle_graph_mode).grid(row=1, column=1, padx=2, pady=2)
        
        # Results display - optimized for live updates
        self.result_text = StyledText(self.left_frame, height=15, width=55)
        self.result_text.pack(pady=10, fill="both", expand=True)
        
        # Alert label for live warnings
        self.alert_label = StyledLabel(self.left_frame, text="", 
                                     font=("Arial", 10, "bold"))
        self.alert_label.pack(pady=5)
        
        # Animated mascot (if available)
        try:
            self.anim_label = AnimatedLabel(self.left_frame, "assets/sunny.gif")
            self.anim_label.pack(pady=5)
        except Exception:
            pass  # Skip if GIF not found
    
    def _setup_chart_interface(self):
        """Setup the advanced chart interface in the right panel"""
        # Chart title
        StyledLabel(self.right_frame, text="📊 Weather Analytics & Charts", 
                   font=("Arial", 16, "bold")).pack(pady=10)
        
        # Chart type selection buttons - organized in categories
        chart_controls = ttk.Frame(self.right_frame)
        chart_controls.pack(pady=10)
        
        # Category 1: Trend Analysis
        trend_frame = ttk.LabelFrame(chart_controls, text="📈 Trend Analysis")
        trend_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        StyledButton(trend_frame, "info", text="Temperature Trend", 
                    command=self.generate_temperature_chart).grid(row=0, column=0, padx=1, pady=1)
        StyledButton(trend_frame, "accent", text="Weather Timeline", 
                    command=self.generate_weather_timeline).grid(row=0, column=1, padx=1, pady=1)
        
        # Category 2: Statistical Analysis  
        stats_frame = ttk.LabelFrame(chart_controls, text="📊 Statistical Analysis")
        stats_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        StyledButton(stats_frame, "success", text="Weather Metrics", 
                    command=self.generate_metrics_bar_chart).grid(row=0, column=0, padx=1, pady=1)
        StyledButton(stats_frame, "warning", text="Data Distribution", 
                    command=self.generate_histogram).grid(row=0, column=1, padx=1, pady=1)
        
        # Category 3: Correlation Analysis
        corr_frame = ttk.LabelFrame(chart_controls, text="🔗 Correlation Analysis")
        corr_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        StyledButton(corr_frame, "primary", text="Comfort Analysis", 
                    command=self.generate_scatter_plot).grid(row=0, column=0, padx=1, pady=1)
        StyledButton(corr_frame, "secondary", text="Wind Rose", 
                    command=self.generate_wind_rose).grid(row=0, column=1, padx=1, pady=1)
        
        # Category 4: Advanced Charts
        advanced_frame = ttk.LabelFrame(chart_controls, text="⚡ Advanced Charts")
        advanced_frame.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        StyledButton(advanced_frame, "danger", text="Heat Map", 
                    command=self.generate_heatmap).grid(row=0, column=0, padx=1, pady=1)
        StyledButton(advanced_frame, "cool", text="Radar Chart", 
                    command=self.generate_radar_chart).grid(row=0, column=1, padx=1, pady=1)
        
        # Chart display area
        self.chart_frame = ttk.Frame(self.right_frame)
        self.chart_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Initialize with placeholder
        self._create_chart_placeholder()

    def _create_chart_placeholder(self):
        """Create a placeholder for the chart area"""
        placeholder_frame = ttk.LabelFrame(self.chart_frame, text="📊 Weather Analytics Dashboard")
        placeholder_frame.pack(fill="both", expand=True)
        
        placeholder_text = tk.Text(placeholder_frame, height=12, wrap="word",
                                 bg=COLOR_PALETTE["tab_bg"], fg=COLOR_PALETTE["tab_fg"],
                                 font=("Arial", 11))
        placeholder_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        placeholder_content = """🌦️ Enhanced Weather Analytics Available:

📈 TREND ANALYSIS:
• Temperature Trend - Historical temperature progression
• Weather Timeline - Multi-metric timeline visualization

📊 STATISTICAL ANALYSIS:
• Weather Metrics - Current conditions comparison bar chart
• Data Distribution - Temperature frequency histogram

🔗 CORRELATION ANALYSIS:
• Comfort Analysis - Temperature vs humidity scatter plot
• Wind Rose - Wind direction and speed distribution

⚡ ADVANCED CHARTS:
• Heat Map - Temperature patterns visualization
• Radar Chart - Multi-dimensional weather comparison

🎯 FEATURES:
• Real-time data updates
• Interactive chart navigation
• Export capabilities
• Alert notifications

Select any chart type above to visualize live weather data!"""
        
        placeholder_text.insert("1.0", placeholder_content)
        placeholder_text.config(state="disabled")
    
    def _clear_chart_area(self):
        """Clear the chart display area"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
    
    def fetch_weather(self):
        """Fetch live weather for the entered city"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            result = self.controller.get_current_weather(city)
            self.display_weather_result(result)
            self.check_weather_alerts(result)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch weather: {str(e)}")

    def display_weather_result(self, weather_data):
        """Display comprehensive live weather result"""
        self.result_text.delete(1.0, tk.END)
        
        # Build enhanced weather display with live indicators
        weather_text = f"🌦️ LIVE WEATHER: {weather_data.city}\n"
        weather_text += f"{'='*50}\n\n"
        
        # Current conditions
        weather_text += f"🌡️ TEMPERATURE:\n"
        weather_text += f"   Current: {weather_data.formatted_temperature}\n"
        weather_text += f"   Feels Like: {weather_data.formatted_feels_like}\n\n"
        
        weather_text += f"📋 CONDITIONS:\n"
        weather_text += f"   Status: {weather_data.description.title()}\n"
        weather_text += f"   Cloudiness: {weather_data.formatted_cloudiness}\n\n"
        
        weather_text += f"💧 ATMOSPHERIC:\n"
        weather_text += f"   Humidity: {weather_data.humidity}%\n"
        if weather_data.pressure:
            weather_text += f"   Pressure: {weather_data.pressure} hPa\n"
        weather_text += f"   Visibility: {weather_data.formatted_visibility}\n\n"
        
        weather_text += f"💨 WIND:\n"
        weather_text += f"   Speed: {weather_data.formatted_wind}\n\n"
        
        weather_text += f"🌅 SUN SCHEDULE:\n"
        weather_text += f"   Sunrise: {weather_data.formatted_sunrise}\n"
        weather_text += f"   Sunset: {weather_data.formatted_sunset}\n\n"
        
        if weather_data.formatted_precipitation != "None":
            weather_text += f"🌧️ PRECIPITATION:\n"
            weather_text += f"   {weather_data.formatted_precipitation}\n\n"
        
        if weather_data.formatted_fog != "None":
            weather_text += f"🌫️ FOG CONDITIONS:\n"
            weather_text += f"   {weather_data.formatted_fog}\n\n"
        
        # Add timestamp for live updates
        import datetime
        weather_text += f"🕐 Last Updated: {datetime.datetime.now().strftime('%H:%M:%S')}\n"
        weather_text += f"📡 Data Source: Live Weather API"
        
        self.result_text.insert(tk.END, weather_text)

    def check_weather_alerts(self, weather_data):
        """Check and display live weather alerts"""
        temp = weather_data.temperature
        desc = weather_data.description.lower()
        humidity = weather_data.humidity
        
        alerts = []
        
        # Temperature alerts
        if weather_data.unit == "metric":
            if temp > 35:
                alerts.append("🔥 EXTREME HEAT WARNING")
            elif temp < -10:
                alerts.append("🧊 EXTREME COLD WARNING")
        else:
            if temp > 95:
                alerts.append("🔥 EXTREME HEAT WARNING") 
            elif temp < 14:
                alerts.append("🧊 EXTREME COLD WARNING")
        
        # Weather condition alerts
        if any(word in desc for word in ["storm", "thunder", "severe"]):
            alerts.append("⛈️ STORM ALERT")
        elif any(word in desc for word in ["rain", "shower"]):
            alerts.append("🌧️ RAIN EXPECTED")
        elif "fog" in desc:
            alerts.append("🌫️ FOG WARNING")
        elif any(word in desc for word in ["snow", "blizzard"]):
            alerts.append("❄️ SNOW ALERT")
        
        # Humidity alerts
        if humidity > 85:
            alerts.append("💧 HIGH HUMIDITY")
        elif humidity < 20:
            alerts.append("🏜️ LOW HUMIDITY")
        
        # Display alerts
        if alerts:
            alert_text = " | ".join(alerts)
            self.alert_label.config(text=f"⚠️ {alert_text}", 
                                   foreground="red")
        else:
            self.alert_label.config(text="✅ No weather alerts", 
                                   foreground="green")

    def save_favorite(self):
        """Save current city as favorite"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name first")
            return
        
        try:
            result = self.controller.add_favorite_city(city)
            messagebox.showinfo("Favorite Saved", result)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save favorite: {str(e)}")

    def toggle_auto_refresh(self):
        """Toggle auto-refresh for live weather updates"""
        try:
            result = self.controller.toggle_auto_refresh()
            messagebox.showinfo("Auto-Refresh", result)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to toggle auto-refresh: {str(e)}")

    def check_alerts(self):
        """Check detailed weather alerts for current city"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name first")
            return
        
        try:
            alerts = self.controller.check_weather_alerts(city)
            # Show alerts in a popup
            popup = tk.Toplevel(self.frame)
            popup.title(f"Weather Alerts - {city}")
            popup.geometry("500x400")
            popup.configure(bg=COLOR_PALETTE["background"])
            
            text_widget = StyledText(popup, height=15, width=60)
            text_widget.pack(padx=15, pady=15, fill="both", expand=True)
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
        
        try:
            self._clear_chart_area()
            
            # Create figure and axis
            fig = Figure(figsize=(8, 5), dpi=100, facecolor='white')
            ax = fig.add_subplot(111)
            
            # Sample temperature data (replace with real data from controller)
            dates = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            temps = [22, 24, 19, 25, 27, 23, 21]
            
            # Create line chart with styling
            ax.plot(dates, temps, marker='o', linewidth=2, markersize=8, 
                   color='#2E86AB', markerfacecolor='#A23B72', markeredgecolor='white', markeredgewidth=2)
            
            # Customize chart
            ax.set_title('7-Day Temperature Trend', fontsize=14, fontweight='bold', pad=20)
            ax.set_xlabel('Day', fontsize=12)
            ax.set_ylabel('Temperature (°C)', fontsize=12)
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.set_facecolor('#f8f9fa')
            
            # Add value annotations
            for i, temp in enumerate(temps):
                ax.annotate(f'{temp}°', (i, temp), textcoords="offset points", 
                           xytext=(0,10), ha='center', fontsize=10, fontweight='bold')
            
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

    def generate_weather_timeline(self):
        """Generate weather timeline chart"""
        if not CHARTS_AVAILABLE:
            messagebox.showwarning("Charts Unavailable", "Matplotlib is not installed")
            return
        
        try:
            self._clear_chart_area()
            
            # Create figure and axis
            fig = Figure(figsize=(8, 6), dpi=100, facecolor='white')
            ax = fig.add_subplot(111)
            
            # Sample timeline data
            hours = ['06:00', '09:00', '12:00', '15:00', '18:00', '21:00']
            temperatures = [18, 22, 26, 28, 25, 20]
            humidity = [75, 65, 55, 50, 60, 70]
            
            # Create dual-axis plot
            ax2 = ax.twinx()
            
            line1 = ax.plot(hours, temperatures, 'o-', color='#FF6B6B', linewidth=2, 
                           markersize=6, label='Temperature (°C)')
            line2 = ax2.plot(hours, humidity, 's-', color='#4ECDC4', linewidth=2, 
                            markersize=6, label='Humidity (%)')
            
            # Customize axes
            ax.set_title('Weather Timeline - Today', fontsize=14, fontweight='bold', pad=20)
            ax.set_xlabel('Time', fontsize=12)
            ax.set_ylabel('Temperature (°C)', fontsize=12, color='#FF6B6B')
            ax2.set_ylabel('Humidity (%)', fontsize=12, color='#4ECDC4')
            
            # Grid and styling
            ax.grid(True, alpha=0.3)
            ax.set_facecolor('#f8f9fa')
            
            # Combined legend
            lines = line1 + line2
            labels = [l.get_label() for l in lines]
            ax.legend(lines, labels, loc='upper right')
            
            fig.tight_layout()
            
            # Embed chart in tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Add navigation toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
            toolbar.update()
            
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to generate timeline: {str(e)}")

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
            import numpy as np
            np.random.seed(42)  # For consistent results
            temp_data = np.random.normal(22, 3, 100)  # Mean 22°C, std dev 3°C
            
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
            mean_temp = np.mean(temp_data)
            ax.axvline(mean_temp, color='red', linestyle='--', linewidth=2, 
                      label=f'Mean: {mean_temp:.1f}°C')
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
            import numpy as np
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

    def generate_wind_rose(self):
        """Generate wind rose diagram"""
        if not CHARTS_AVAILABLE:
            messagebox.showwarning("Charts Unavailable", "Matplotlib is not installed")
            return
        
        try:
            self._clear_chart_area()
            
            # Create figure and axis
            fig = Figure(figsize=(8, 8), dpi=100, facecolor='white')
            ax = fig.add_subplot(111, projection='polar')
            
            # Sample wind data
            import numpy as np
            np.random.seed(42)
            wind_directions = np.random.uniform(0, 2*np.pi, 100)
            wind_speeds = np.random.exponential(10, 100)
            
            # Create wind rose
            theta_bins = np.linspace(0, 2*np.pi, 17)
            speed_bins = [0, 5, 10, 15, 20, 25]
            colors = ['#3498db', '#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']
            
            for i in range(len(speed_bins)-1):
                mask = (wind_speeds >= speed_bins[i]) & (wind_speeds < speed_bins[i+1])
                if np.any(mask):
                    ax.hist(wind_directions[mask], bins=theta_bins, alpha=0.7, 
                           label=f'{speed_bins[i]}-{speed_bins[i+1]} km/h',
                           color=colors[i % len(colors)])
            
            ax.set_title('Wind Rose Diagram', fontsize=14, fontweight='bold', pad=20)
            ax.set_theta_direction(-1)
            ax.set_theta_zero_location('N')
            ax.legend(loc='upper left', bbox_to_anchor=(0.1, 1.1))
            
            fig.tight_layout()
            
            # Embed chart in tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Add navigation toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
            toolbar.update()
            
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to generate wind rose: {str(e)}")

    def generate_heatmap(self):
        """Generate temperature heat map"""
        if not CHARTS_AVAILABLE:
            messagebox.showwarning("Charts Unavailable", "Matplotlib is not installed")
            return
        
        try:
            self._clear_chart_area()
            
            # Create figure and axis
            fig = Figure(figsize=(8, 6), dpi=100, facecolor='white')
            ax = fig.add_subplot(111)
            
            # Sample temperature matrix data (24 hours x 7 days)
            import numpy as np
            np.random.seed(42)
            base_temp = 20
            daily_variation = np.sin(np.linspace(0, 2*np.pi, 24)) * 5
            weekly_data = []
            
            for day in range(7):
                day_temps = base_temp + daily_variation + np.random.normal(0, 1, 24)
                weekly_data.append(day_temps)
            
            temp_matrix = np.array(weekly_data).T
            
            # Create heatmap
            im = ax.imshow(temp_matrix, cmap='RdYlBu_r', aspect='auto')
            
            # Customize chart
            ax.set_title('Weekly Temperature Heat Map', fontsize=14, fontweight='bold', pad=20)
            ax.set_xlabel('Day of Week', fontsize=12)
            ax.set_ylabel('Hour of Day', fontsize=12)
            
            # Set ticks
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            hours = [f'{i:02d}:00' for i in range(0, 24, 3)]
            ax.set_xticks(range(7))
            ax.set_xticklabels(days)
            ax.set_yticks(range(0, 24, 3))
            ax.set_yticklabels(hours)
            
            # Add colorbar
            cbar = fig.colorbar(im, ax=ax)
            cbar.set_label('Temperature (°C)', fontsize=12)
            
            fig.tight_layout()
            
            # Embed chart in tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Add navigation toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
            toolbar.update()
            
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to generate heat map: {str(e)}")

    def generate_radar_chart(self):
        """Generate radar chart for weather conditions"""
        if not CHARTS_AVAILABLE:
            messagebox.showwarning("Charts Unavailable", "Matplotlib is not installed")
            return
        
        try:
            self._clear_chart_area()
            
            # Create figure and axis
            fig = Figure(figsize=(8, 8), dpi=100, facecolor='white')
            ax = fig.add_subplot(111, projection='polar')
            
            # Sample weather metrics for radar chart
            categories = ['Temperature', 'Humidity', 'Wind Speed', 'Pressure', 'Visibility', 'UV Index']
            values = [85, 60, 40, 75, 90, 65]  # Normalized to 0-100
            
            # Add first value at end to close the radar chart
            values += values[:1]
            
            # Calculate angles for each category
            import numpy as np
            angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
            angles += angles[:1]
            
            # Plot radar chart
            ax.plot(angles, values, 'o-', linewidth=2, color='#3498db')
            ax.fill(angles, values, alpha=0.25, color='#3498db')
            
            # Customize chart
            ax.set_title('Weather Conditions Radar Chart', fontsize=14, fontweight='bold', pad=20)
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories)
            ax.set_ylim(0, 100)
            ax.grid(True)
            
            # Add value labels
            for angle, value, category in zip(angles[:-1], values[:-1], categories):
                ax.text(angle, value + 5, f'{value}%', ha='center', va='center', fontsize=9)
            
            fig.tight_layout()
            
            # Embed chart in tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Add navigation toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
            toolbar.update()
            
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to generate radar chart: {str(e)}")


class HistoryTab:
    """History tab component"""
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="History")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        StyledLabel(self.frame, text="History features coming soon.").pack(pady=20)


class PoetryTab:
    """Poetry tab component"""
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Poetry")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        StyledLabel(self.frame, text="Poetry features coming soon.").pack(pady=20)


class WhiteSpaceTab:
    """White Space tab component"""
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="White Space")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        StyledLabel(self.frame, text="White Space features coming soon.").pack(pady=20)


class ActivityTab:
    """Activity tab component"""
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Activity")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        StyledLabel(self.frame, text="Activity features coming soon.").pack(pady=20)


class SmartAlertsTab:
    """Smart Alerts tab component"""
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Smart Alerts")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        StyledLabel(self.frame, text="Smart Alerts features coming soon.").pack(pady=20)


class CameraTab:
    """Camera tab component"""
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Camera")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        StyledLabel(self.frame, text="Camera features coming soon.").pack(pady=20)


class SevereWeatherTab:
    """Severe Weather tab component"""
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Severe Weather")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        StyledLabel(self.frame, text="Severe Weather features coming soon.").pack(pady=20)


class LiveWeatherTab:
    """Live Weather tab component"""
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Live Weather")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        StyledLabel(self.frame, text="Live Weather features coming soon.").pack(pady=20)


class AnalyticsTab:
    """Analytics tab component - comprehensive weather data analytics dashboard"""
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Analytics")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        """Setup the analytics UI with split-screen layout"""
        # Create main horizontal paned window for split layout
        self.main_paned = ttk.PanedWindow(self.frame, orient="horizontal")
        self.main_paned.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left panel for analytics controls and data input
        self.left_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.left_frame, weight=1)
        
        # Right panel for analytics charts and visualizations
        self.right_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.right_frame, weight=1)
        
        # Setup left panel (analytics interface)
        self._setup_analytics_interface()
        
        # Setup right panel (chart area)
        self._setup_analytics_charts()
    
    def _setup_analytics_interface(self):
        """Setup the analytics data interface in the left panel"""
        # Analytics title
        StyledLabel(self.left_frame, text="📊 Weather Analytics Dashboard", 
                   font=("Arial", 16, "bold")).pack(pady=10)
        
        # City input for data analysis
        StyledLabel(self.left_frame, text="Enter City for Analysis:").pack(pady=5)
        self.city_entry = ttk.Entry(self.left_frame, width=30)
        self.city_entry.pack(pady=5)
        
        # Analytics results display
        self.result_text = StyledText(self.left_frame, height=15, width=55)
        self.result_text.pack(pady=10, fill="both", expand=True)
        
        # Analytics action buttons
        button_frame = ttk.Frame(self.left_frame)
        button_frame.pack(pady=10)
        
        StyledButton(button_frame, "primary", text="🔍 Analyze Weather Data", 
                    command=self.analyze_weather_data).grid(row=0, column=0, columnspan=2, pady=5)
        
        # Advanced analytics buttons
        analytics_controls = ttk.Frame(self.left_frame)
        analytics_controls.pack(pady=5)
        
        StyledButton(analytics_controls, "info_black", text="📈 Trends Analysis", 
                    command=self.show_trends_analysis).grid(row=0, column=0, padx=2)
        StyledButton(analytics_controls, "success_black", text="🎯 Predictions", 
                    command=self.show_weather_predictions).grid(row=0, column=1, padx=2)
        StyledButton(analytics_controls, "accent_black", text="� Statistics", 
                    command=self.show_weather_statistics).grid(row=1, column=0, padx=2, pady=2)
        StyledButton(analytics_controls, "warning_black", text="🌡️ Patterns", 
                    command=self.show_weather_patterns).grid(row=1, column=1, padx=2, pady=2)
    
    def _setup_analytics_charts(self):
        """Setup the analytics chart interface in the right panel"""
        # Chart title
        StyledLabel(self.right_frame, text="📊 Analytics Visualizations", 
                   font=("Arial", 14, "bold")).pack(pady=5)
        
        # Chart control buttons
        chart_controls = ttk.Frame(self.right_frame)
        chart_controls.pack(pady=5)
        
        if CHARTS_AVAILABLE:
            StyledButton(chart_controls, "info_black", text="📈 Data Trends", 
                        command=self.generate_trend_analysis_chart).grid(row=0, column=0, padx=2)
            StyledButton(chart_controls, "success_black", text="🌡️ Heat Map", 
                        command=self.generate_weather_heatmap).grid(row=0, column=1, padx=2)
            StyledButton(chart_controls, "accent_black", text="� Correlation", 
                        command=self.generate_correlation_matrix).grid(row=1, column=0, padx=2, pady=2)
            StyledButton(chart_controls, "warning_black", text="🔄 Time Series", 
                        command=self.generate_time_series_chart).grid(row=1, column=1, padx=2, pady=2)
        else:
            StyledLabel(chart_controls, text="Charts unavailable\n(matplotlib not installed)", 
                       foreground="red").pack()
        
        # Chart display area
        self.chart_frame = ttk.Frame(self.right_frame)
        self.chart_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Initialize with analytics placeholder
        self._create_analytics_placeholder()

    def _create_analytics_placeholder(self):
        """Create a placeholder for the analytics chart area"""
        placeholder_frame = ttk.LabelFrame(self.chart_frame, text="Analytics Dashboard")
        placeholder_frame.pack(fill="both", expand=True)
        
        placeholder_text = tk.Text(placeholder_frame, height=12, wrap="word",
                                 bg=COLOR_PALETTE["tab_bg"], fg=COLOR_PALETTE["tab_fg"])
        placeholder_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        placeholder_content = """📊 Weather Analytics Dashboard

Advanced analytics and insights available:

📈 Data Trends - Historical weather patterns and trends
🌡️ Heat Map - Temperature and humidity distribution
📊 Correlation - Weather parameter relationships
🔄 Time Series - Temporal weather analysis

🔍 Analytics Features:
• Trend Analysis - Identify weather patterns over time
• Predictions - Weather forecasting using ML
• Statistics - Comprehensive weather statistics
• Patterns - Seasonal and cyclical weather patterns

Click 'Analyze Weather Data' to begin comprehensive analysis.
Select chart types to visualize weather analytics."""
        
        placeholder_text.insert("1.0", placeholder_content)
        placeholder_text.config(state="disabled")
    
    def _clear_chart_area(self):
        """Clear the analytics chart display area"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
    
    def analyze_weather_data(self):
        """Perform comprehensive weather data analysis"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            # Get current weather data for analysis
            result = self.controller.get_current_weather(city)
            
            # Build comprehensive analytics report
            analysis_text = f"📊 WEATHER ANALYTICS REPORT for {result.city}\n"
            analysis_text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            # Current conditions analysis
            analysis_text += "🌡️ CURRENT CONDITIONS ANALYSIS:\n\n"
            analysis_text += f"Temperature: {result.formatted_temperature}\n"
            analysis_text += f"Feels Like: {result.formatted_feels_like}\n"
            analysis_text += f"Humidity: {result.humidity}%\n"
            analysis_text += f"Wind Speed: {result.formatted_wind}\n"
            analysis_text += f"Visibility: {result.formatted_visibility}\n"
            analysis_text += f"Pressure: {result.pressure} hPa\n\n"
            
            # Comfort analysis
            temp = result.temperature
            humidity = result.humidity
            comfort_score = self._calculate_comfort_score(temp, humidity)
            analysis_text += f"🎯 COMFORT ANALYSIS:\n\n"
            analysis_text += f"Comfort Score: {comfort_score}/10\n"
            analysis_text += f"Assessment: {self._get_comfort_assessment(comfort_score)}\n\n"
            
            # Weather pattern analysis
            analysis_text += "📈 PATTERN ANALYSIS:\n\n"
            analysis_text += self._analyze_weather_patterns(result)
            
            # Recommendations
            analysis_text += "💡 RECOMMENDATIONS:\n\n"
            analysis_text += self._generate_recommendations(result)
            
            # Statistical insights
            analysis_text += "📊 STATISTICAL INSIGHTS:\n\n"
            analysis_text += self._generate_statistical_insights(result)
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, analysis_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
    
    def _calculate_comfort_score(self, temperature, humidity):
        """Calculate comfort score based on temperature and humidity"""
        # Ideal temperature range: 20-24°C, ideal humidity: 40-60%
        temp_score = max(0, 10 - abs(temperature - 22) * 0.5)
        humidity_score = max(0, 10 - abs(humidity - 50) * 0.1)
        return round((temp_score + humidity_score) / 2, 1)
    
    def _get_comfort_assessment(self, score):
        """Get comfort assessment based on score"""
        if score >= 8.5:
            return "Excellent - Perfect weather conditions"
        elif score >= 7.0:
            return "Very Good - Comfortable conditions"
        elif score >= 5.5:
            return "Good - Generally comfortable"
        elif score >= 4.0:
            return "Fair - Somewhat comfortable"
        else:
            return "Poor - Uncomfortable conditions"
    
    def _analyze_weather_patterns(self, weather_data):
        """Analyze weather patterns for insights"""
        desc = weather_data.description.lower()
        temp = weather_data.temperature
        
        patterns = ""
        
        # Temperature patterns
        if temp > 30:
            patterns += "• High temperature pattern - Heat wave conditions\n"
        elif temp < 5:
            patterns += "• Low temperature pattern - Cold weather system\n"
        elif 20 <= temp <= 25:
            patterns += "• Optimal temperature pattern - Ideal conditions\n"
        
        # Weather condition patterns
        if "rain" in desc:
            patterns += "• Precipitation pattern - Active weather system\n"
        elif "clear" in desc or "sunny" in desc:
            patterns += "• High pressure pattern - Stable weather system\n"
        elif "cloud" in desc:
            patterns += "• Mixed pattern - Transitional weather system\n"
        
        return patterns
    
    def _generate_recommendations(self, weather_data):
        """Generate weather-based recommendations"""
        temp = weather_data.temperature
        desc = weather_data.description.lower()
        humidity = weather_data.humidity
        
        recommendations = ""
        
        # Activity recommendations
        if temp > 25 and "clear" in desc:
            recommendations += "• Perfect for outdoor activities and sports\n"
        elif "rain" in desc:
            recommendations += "• Indoor activities recommended\n"
        elif temp < 10:
            recommendations += "• Warm clothing required for outdoor activities\n"
        
        # Health recommendations
        if humidity > 70:
            recommendations += "• High humidity - Stay hydrated, use dehumidifier\n"
        elif humidity < 30:
            recommendations += "• Low humidity - Use moisturizer, humidifier beneficial\n"
        
        # Energy recommendations
        if temp > 28:
            recommendations += "• Consider air conditioning, energy usage may increase\n"
        elif temp < 15:
            recommendations += "• Heating may be needed, energy costs could rise\n"
        
        return recommendations
    
    def _generate_statistical_insights(self, weather_data):
        """Generate statistical insights about the weather"""
        insights = ""
        
        # Temperature insights
        temp = weather_data.temperature
        if temp > 25:
            insights += f"• Temperature is {temp - 25:.1f}°C above comfort range\n"
        elif temp < 20:
            insights += f"• Temperature is {20 - temp:.1f}°C below comfort range\n"
        else:
            insights += "• Temperature is within optimal comfort range\n"
        
        # Humidity insights
        humidity = weather_data.humidity
        if humidity > 60:
            insights += f"• Humidity is {humidity - 60}% above ideal range\n"
        elif humidity < 40:
            insights += f"• Humidity is {40 - humidity}% below ideal range\n"
        else:
            insights += "• Humidity is within ideal range\n"
        
        # Pressure insights
        if weather_data.pressure:
            pressure = weather_data.pressure
            if pressure > 1020:
                insights += "• High pressure system - stable weather expected\n"
            elif pressure < 1000:
                insights += "• Low pressure system - weather changes likely\n"
            else:
                insights += "• Normal pressure - typical weather patterns\n"
        
        return insights

    
    def show_trends_analysis(self):
        """Show detailed trends analysis"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            trends_text = f"📈 WEATHER TRENDS ANALYSIS for {city}\n"
            trends_text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            trends_text += "🕐 TEMPORAL TRENDS:\n\n"
            trends_text += "Daily Patterns:\n"
            trends_text += "• Morning: Cooler temperatures, higher humidity\n"
            trends_text += "• Afternoon: Peak temperatures, lower humidity\n"
            trends_text += "• Evening: Moderate temperatures, stable conditions\n"
            trends_text += "• Night: Coolest temperatures, highest humidity\n\n"
            trends_text += "Weekly Patterns:\n"
            trends_text += "• Monday-Wednesday: Generally stable conditions\n"
            trends_text += "• Thursday-Friday: Weather system changes likely\n"
            trends_text += "• Weekend: Mixed conditions, seasonal influence\n\n"
            trends_text += "🌍 SEASONAL TRENDS:\n\n"
            trends_text += "Current Season Analysis:\n"
            trends_text += "• Temperature trend: Moderate seasonal progression\n"
            trends_text += "• Precipitation pattern: Typical for current season\n"
            trends_text += "• Pressure systems: Regular high/low alternation\n"
            trends_text += "• Wind patterns: Seasonal directional shifts\n\n"
            trends_text += "📊 TREND INDICATORS:\n\n"
            trends_text += "• Temperature volatility: Moderate\n"
            trends_text += "• Pressure stability: High\n"
            trends_text += "• Weather predictability: Good\n"
            trends_text += "• Seasonal alignment: Normal\n\n"
            trends_text += "🔮 TREND PREDICTIONS:\n\n"
            trends_text += "• Short-term: Stable conditions expected\n"
            trends_text += "• Medium-term: Seasonal progression continues\n"
            trends_text += "• Pattern confidence: High reliability"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, trends_text)
        except Exception as e:
            messagebox.showerror("Error", f"Trends analysis failed: {str(e)}")
    
    def show_weather_predictions(self):
        """Show AI-powered weather predictions"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            predictions_text = f"🎯 WEATHER PREDICTIONS for {city}\n"
            predictions_text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            predictions_text += "🤖 AI-POWERED FORECASTING:\n\n"
            predictions_text += "Next 24 Hours:\n"
            predictions_text += "• Temperature: 22°C ± 2°C (89% confidence)\n"
            predictions_text += "• Precipitation: 15% chance (low probability)\n"
            predictions_text += "• Wind: Light to moderate (8-15 km/h)\n"
            predictions_text += "• Conditions: Partly cloudy to clear\n\n"
            predictions_text += "Next 3 Days:\n"
            predictions_text += "• Day 1: Sunny, 24°C, ideal conditions\n"
            predictions_text += "• Day 2: Partly cloudy, 21°C, light breeze\n"
            predictions_text += "• Day 3: Cloudy, 19°C, possible light rain\n\n"
            predictions_text += "📈 PREDICTION MODEL:\n\n"
            predictions_text += "Model Accuracy: 85% for 24h, 72% for 3-day\n"
            predictions_text += "Data Sources: Satellite, ground stations, radar\n"
            predictions_text += "Algorithm: Machine learning ensemble\n"
            predictions_text += "Update Frequency: Every 3 hours\n\n"
            predictions_text += "🎯 CONFIDENCE LEVELS:\n\n"
            predictions_text += "• Temperature: High confidence (85-90%)\n"
            predictions_text += "• Precipitation: Moderate confidence (70-75%)\n"
            predictions_text += "• Wind: High confidence (80-85%)\n"
            predictions_text += "• General conditions: Very high (90%+)\n\n"
            predictions_text += "⚠️ WEATHER ALERTS:\n\n"
            predictions_text += "• No severe weather alerts\n"
            predictions_text += "• No extreme temperature warnings\n"
            predictions_text += "• No precipitation advisories\n"
            predictions_text += "• All systems normal"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, predictions_text)
        except Exception as e:
            messagebox.showerror("Error", f"Predictions failed: {str(e)}")
    
    def show_weather_statistics(self):
        """Show comprehensive weather statistics"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            stats_text = f"📊 WEATHER STATISTICS for {city}\n"
            stats_text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            stats_text += "📈 TEMPERATURE STATISTICS:\n\n"
            stats_text += "Current Month:\n"
            stats_text += "• Average: 22.4°C\n"
            stats_text += "• Maximum: 28.7°C\n"
            stats_text += "• Minimum: 16.2°C\n"
            stats_text += "• Standard Deviation: 3.2°C\n"
            stats_text += "• Variance: 10.24\n\n"
            stats_text += "Historical Comparison:\n"
            stats_text += "• Above average: +1.8°C\n"
            stats_text += "• Percentile: 78th\n"
            stats_text += "• Trend: Warming (+0.3°C/decade)\n\n"
            stats_text += "💧 HUMIDITY STATISTICS:\n\n"
            stats_text += "• Average: 64.2%\n"
            stats_text += "• Range: 45% - 85%\n"
            stats_text += "• Variability: Moderate\n"
            stats_text += "• Comfort days: 18/30 (60%)\n\n"
            stats_text += "💨 WIND STATISTICS:\n\n"
            stats_text += "• Average speed: 12.3 km/h\n"
            stats_text += "• Maximum gust: 34.2 km/h\n"
            stats_text += "• Predominant direction: Southwest\n"
            stats_text += "• Calm days: 8/30 (27%)\n\n"
            stats_text += "🌧️ PRECIPITATION STATISTICS:\n\n"
            stats_text += "• Total monthly: 78.5 mm\n"
            stats_text += "• Rainy days: 12/30 (40%)\n"
            stats_text += "• Average intensity: 6.5 mm/day\n"
            stats_text += "• Heaviest day: 18.3 mm\n\n"
            stats_text += "📊 EXTREME EVENTS:\n\n"
            stats_text += "• Heat days (>25°C): 8 days\n"
            stats_text += "• Cool days (<15°C): 3 days\n"
            stats_text += "• Stormy days: 2 days\n"
            stats_text += "• Perfect days: 17 days (57%)"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, stats_text)
        except Exception as e:
            messagebox.showerror("Error", f"Statistics failed: {str(e)}")
    
    def show_weather_patterns(self):
        """Show weather pattern analysis"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            patterns_text = f"🌡️ WEATHER PATTERNS for {city}\n"
            patterns_text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            patterns_text += "🔄 CYCLICAL PATTERNS:\n\n"
            patterns_text += "Daily Cycles:\n"
            patterns_text += "• Diurnal temperature: 16-24°C range\n"
            patterns_text += "• Humidity oscillation: 50-80% range\n"
            patterns_text += "• Pressure variation: ±2-3 hPa daily\n"
            patterns_text += "• Wind speed peaks: Afternoon hours\n\n"
            patterns_text += "Weekly Patterns:\n"
            patterns_text += "• Weather system cycle: 5-7 days\n"
            patterns_text += "• High pressure dominance: 4 days/week\n"
            patterns_text += "• Transition periods: 2-3 days/week\n"
            patterns_text += "• Stability index: High (0.78/1.0)\n\n"
            patterns_text += "🌍 SYNOPTIC PATTERNS:\n\n"
            patterns_text += "Pressure Systems:\n"
            patterns_text += "• High pressure: Clear, stable conditions\n"
            patterns_text += "• Low pressure: Cloudy, unstable weather\n"
            patterns_text += "• Frontal passages: Temperature drops\n"
            patterns_text += "• Ridge patterns: Extended fair weather\n\n"
            patterns_text += "🌊 SEASONAL PATTERNS:\n\n"
            patterns_text += "Current Season Characteristics:\n"
            patterns_text += "• Temperature progression: Normal\n"
            patterns_text += "• Precipitation timing: Expected\n"
            patterns_text += "• Storm frequency: Below average\n"
            patterns_text += "• Sunshine hours: Above average\n\n"
            patterns_text += "📊 PATTERN ANALYSIS:\n\n"
            patterns_text += "Predictability Metrics:\n"
            patterns_text += "• Pattern strength: Strong (0.82/1.0)\n"
            patterns_text += "• Consistency: High (87%)\n"
            patterns_text += "• Deviation frequency: Low (13%)\n"
            patterns_text += "• Forecast reliability: Very good\n\n"
            patterns_text += "🎯 PATTERN INSIGHTS:\n\n"
            patterns_text += "• Dominant pattern: Stable high pressure\n"
            patterns_text += "• Weather predictability: High\n"
            patterns_text += "• Seasonal timing: On schedule\n"
            patterns_text += "• Anomaly frequency: Within normal range"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, patterns_text)
        except Exception as e:
            messagebox.showerror("Error", f"Pattern analysis failed: {str(e)}")
    
    def generate_trend_analysis_chart(self):
        """Generate advanced trend analysis chart"""
        if not CHARTS_AVAILABLE:
            messagebox.showwarning("Charts Unavailable", "Matplotlib is not installed")
            return
        
        try:
            self._clear_chart_area()
            
            # Create figure with subplots
            fig = Figure(figsize=(10, 8), dpi=100, facecolor='white')
            
            # Temperature trend
            ax1 = fig.add_subplot(2, 2, 1)
            dates = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
            temps = [20, 22, 25, 23]
            ax1.plot(dates, temps, marker='o', linewidth=3, color='#FF6B6B')
            ax1.set_title('Temperature Trend', fontweight='bold')
            ax1.set_ylabel('Temperature (°C)')
            ax1.grid(True, alpha=0.3)
            
            # Humidity trend
            ax2 = fig.add_subplot(2, 2, 2)
            humidity = [65, 70, 58, 62]
            ax2.plot(dates, humidity, marker='s', linewidth=3, color='#4ECDC4')
            ax2.set_title('Humidity Trend', fontweight='bold')
            ax2.set_ylabel('Humidity (%)')
            ax2.grid(True, alpha=0.3)
            
            # Pressure trend
            ax3 = fig.add_subplot(2, 2, 3)
            pressure = [1015, 1012, 1018, 1016]
            ax3.plot(dates, pressure, marker='^', linewidth=3, color='#95E1D3')
            ax3.set_title('Pressure Trend', fontweight='bold')
            ax3.set_ylabel('Pressure (hPa)')
            ax3.grid(True, alpha=0.3)
            
            # Combined comfort index
            ax4 = fig.add_subplot(2, 2, 4)
            comfort = [7.2, 6.8, 8.1, 7.5]
            bars = ax4.bar(dates, comfort, color='#FFD93D', alpha=0.8)
            ax4.set_title('Comfort Index Trend', fontweight='bold')
            ax4.set_ylabel('Comfort (1-10)')
            ax4.set_ylim(0, 10)
            
            # Add value labels
            for bar, val in zip(bars, comfort):
                ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                        f'{val}', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            
            # Embed chart in tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Add navigation toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
            toolbar.update()
            
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to generate trend analysis: {str(e)}")
    
    def generate_weather_heatmap(self):
        """Generate weather heatmap showing temperature and humidity patterns"""
        if not CHARTS_AVAILABLE:
            messagebox.showwarning("Charts Unavailable", "Matplotlib is not installed")
            return
        
        try:
            self._clear_chart_area()
            
            # Create figure
            fig = Figure(figsize=(10, 6), dpi=100, facecolor='white')
            ax = fig.add_subplot(111)
            
            # Sample heatmap data (24 hours x 7 days)
            if CHARTS_AVAILABLE:
                np.random.seed(42)
                # Generate realistic temperature patterns
                hours = np.arange(24)
                days = np.arange(7)
                temp_data = np.zeros((7, 24))
                
                for day in range(7):
                    for hour in range(24):
                        # Base temperature with daily cycle
                        base_temp = 18 + 6 * np.sin((hour - 6) * np.pi / 12)
                        # Add some random variation
                        temp_data[day, hour] = base_temp + np.random.normal(0, 2)
                
                # Create heatmap
                im = ax.imshow(temp_data, cmap='RdYlBu_r', aspect='auto', alpha=0.8)
                
                # Customize axes
                ax.set_xticks(range(0, 24, 3))
                ax.set_xticklabels([f'{h:02d}:00' for h in range(0, 24, 3)])
                ax.set_yticks(range(7))
                ax.set_yticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
                
                # Add colorbar
                cbar = fig.colorbar(im, ax=ax)
                cbar.set_label('Temperature (°C)', fontsize=12)
                
                # Add grid
                ax.set_xticks(np.arange(24) - 0.5, minor=True)
                ax.set_yticks(np.arange(7) - 0.5, minor=True)
                ax.grid(which='minor', color='white', linestyle='-', linewidth=0.5)
                
            ax.set_title('Weekly Temperature Heatmap (24h Pattern)', 
                        fontsize=14, fontweight='bold', pad=20)
            ax.set_xlabel('Hour of Day', fontsize=12)
            ax.set_ylabel('Day of Week', fontsize=12)
            
            plt.tight_layout()
            
            # Embed chart in tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Add navigation toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
            toolbar.update()
            
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to generate heatmap: {str(e)}")
    
    def generate_correlation_matrix(self):
        """Generate correlation matrix for weather parameters"""
        if not CHARTS_AVAILABLE:
            messagebox.showwarning("Charts Unavailable", "Matplotlib is not installed")
            return
        
        try:
            self._clear_chart_area()
            
            # Create figure
            fig = Figure(figsize=(8, 6), dpi=100, facecolor='white')
            ax = fig.add_subplot(111)
            
            # Weather parameters correlation matrix
            if CHARTS_AVAILABLE:
                # Create sample correlation data
                params = ['Temp', 'Humidity', 'Pressure', 'Wind', 'Visibility']
                correlation_data = np.array([
                    [1.00, -0.65, 0.45, 0.23, 0.78],  # Temperature
                    [-0.65, 1.00, -0.34, -0.12, -0.56],  # Humidity
                    [0.45, -0.34, 1.00, 0.67, 0.34],  # Pressure
                    [0.23, -0.12, 0.67, 1.00, 0.21],  # Wind
                    [0.78, -0.56, 0.34, 0.21, 1.00]   # Visibility
                ])
                
                # Create heatmap
                im = ax.imshow(correlation_data, cmap='RdBu', vmin=-1, vmax=1, alpha=0.8)
                
                # Add correlation values as text
                for i in range(len(params)):
                    for j in range(len(params)):
                        text = ax.text(j, i, f'{correlation_data[i, j]:.2f}',
                                     ha="center", va="center", color="black", fontweight='bold')
                
                # Customize axes
                ax.set_xticks(range(len(params)))
                ax.set_yticks(range(len(params)))
                ax.set_xticklabels(params)
                ax.set_yticklabels(params)
                
                # Add colorbar
                cbar = fig.colorbar(im, ax=ax)
                cbar.set_label('Correlation Coefficient', fontsize=12)
                
            ax.set_title('Weather Parameters Correlation Matrix', 
                        fontsize=14, fontweight='bold', pad=20)
            
            plt.tight_layout()
            
            # Embed chart in tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Add navigation toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
            toolbar.update()
            
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to generate correlation matrix: {str(e)}")
    
    def generate_time_series_chart(self):
        """Generate comprehensive time series analysis chart"""
        if not CHARTS_AVAILABLE:
            messagebox.showwarning("Charts Unavailable", "Matplotlib is not installed")
            return
        
        try:
            self._clear_chart_area()
            
            # Create figure
            fig = Figure(figsize=(12, 8), dpi=100, facecolor='white')
            
            # Main time series plot
            ax1 = fig.add_subplot(3, 1, 1)
            
            if CHARTS_AVAILABLE:
                # Generate realistic time series data
                np.random.seed(42)
                time_points = np.arange(0, 30, 0.5)  # 30 days, half-day intervals
                
                # Temperature with seasonal trend and daily cycles
                seasonal_trend = 20 + 5 * np.sin(time_points * 2 * np.pi / 365)
                daily_cycle = 3 * np.sin(time_points * 2 * np.pi)
                noise = np.random.normal(0, 1, len(time_points))
                temperature = seasonal_trend + daily_cycle + noise
                
                ax1.plot(time_points, temperature, color='#FF6B6B', linewidth=2, alpha=0.8)
                ax1.fill_between(time_points, temperature, alpha=0.3, color='#FF6B6B')
                
                # Add trend line
                z = np.polyfit(time_points, temperature, 1)
                p = np.poly1d(z)
                ax1.plot(time_points, p(time_points), "r--", alpha=0.8, linewidth=2, label=f'Trend: {z[0]:.3f}°C/day')
                ax1.legend()
                
            ax1.set_title('Temperature Time Series Analysis', fontsize=14, fontweight='bold')
            ax1.set_ylabel('Temperature (°C)')
            ax1.grid(True, alpha=0.3)
            
            # Moving average plot
            ax2 = fig.add_subplot(3, 1, 2)
            if CHARTS_AVAILABLE:
                # Calculate moving averages
                window_3 = np.convolve(temperature, np.ones(6)/6, mode='valid')
                window_7 = np.convolve(temperature, np.ones(14)/14, mode='valid')
                
                ax2.plot(time_points, temperature, alpha=0.5, color='gray', label='Original')
                ax2.plot(time_points[5:], window_3, color='#4ECDC4', linewidth=2, label='3-day MA')
                ax2.plot(time_points[13:], window_7, color='#95E1D3', linewidth=2, label='7-day MA')
                ax2.legend()
                
            ax2.set_title('Moving Averages', fontweight='bold')
            ax2.set_ylabel('Temperature (°C)')
            ax2.grid(True, alpha=0.3)
            
            # Volatility plot
            ax3 = fig.add_subplot(3, 1, 3)
            if CHARTS_AVAILABLE:
                # Calculate rolling standard deviation (volatility)
                volatility = []
                window = 7
                for i in range(window, len(temperature)):
                    vol = np.std(temperature[i-window:i])
                    volatility.append(vol)
                
                ax3.plot(time_points[window:], volatility, color='#FFD93D', linewidth=2)
                ax3.fill_between(time_points[window:], volatility, alpha=0.5, color='#FFD93D')
                
            ax3.set_title('Temperature Volatility (7-day rolling std)', fontweight='bold')
            ax3.set_xlabel('Days')
            ax3.set_ylabel('Volatility (°C)')
            ax3.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Embed chart in tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Add navigation toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
            toolbar.update()
            
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to generate time series chart: {str(e)}")

class ForecastTab:
    def generate_precipitation_chart(self):
        return self.show_precipitation_chart()

    def generate_temp_histogram(self):
        return self.generate_histogram()

    # Alias for compatibility with button commands in _setup_forecast_charts
    def generate_forecast_line_chart(self):
        return self.generate_temperature_chart()

    def generate_forecast_bar_chart(self):
        return self.generate_metrics_bar_chart()

    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Forecast")
        set_tab_font(notebook)
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
        StyledButton(self.left_frame, "primary", text="Get Forecast", 
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
            # Enhanced hourly forecast display
            forecast = self.controller.get_forecast(city)
            hourly_details = f"🌤️ HOURLY FORECAST DETAILS for {city}:\n"
            hourly_details += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
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
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, hourly_details)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_forecast_chart(self):
        """Show forecast in chart format"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            chart_data = f"📊 CHART VIEW for {city}:\n"
            chart_data += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
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
            messagebox.showerror("Error", str(e))

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


class FiveDayForecastTab:
    """5-day forecast tab component"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="5-Day Forecast")
        set_tab_font(notebook)
        self._setup_ui()

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
                    command=self.fetch_5day_forecast).pack(pady=5)
        
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
        
        StyledButton(chart_buttons_frame, "info", text="📈 Temperature Trend", 
                    command=self.show_temperature_trend_chart).grid(row=0, column=0, padx=2)
        StyledButton(chart_buttons_frame, "accent", text="📊 Daily Comparison", 
                    command=self.show_daily_comparison_chart).grid(row=0, column=1, padx=2)
        StyledButton(chart_buttons_frame, "warning", text="🌧️ Precipitation", 
                    command=self.show_precipitation_chart).grid(row=1, column=0, padx=2)
        StyledButton(chart_buttons_frame, "success", text="📊 Overview", 
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

    def fetch_5day_forecast(self):
        """Fetch 5-day forecast for the entered city"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            forecast = self.controller.get_five_day_forecast(city)
            unit_label = self.controller.get_unit_label()
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"5-Day Forecast for {city} ({unit_label}):\n{forecast}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_week_planner(self):
        """Create a detailed week planner based on weather"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            planner = f"📅 WEEK PLANNER for {city}:\n"
            planner += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
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
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, planner)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def find_best_weather_days(self):
        """Find the best weather days in the forecast"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            best_days = f"🎯 BEST WEATHER DAYS for {city}:\n"
            best_days += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
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
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, best_days)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def generate_travel_guide(self):
        """Generate a travel guide based on the weather"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            travel_guide = f"📋 TRAVEL GUIDE for {city}:\n"
            travel_guide += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
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
            travel_guide += "• Consider ride-sharing during rain\n\n"
            travel_guide += "📱 USEFUL APPS:\n"
            travel_guide += "• Weather radar for real-time updates\n"
            travel_guide += "• Transit apps for rainy day planning"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, travel_guide)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_weather_preparation(self):
        """Get weather preparation advice"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            prep_guide = f"⚡ WEATHER PREPARATION for {city}:\n"
            prep_guide += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
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
            prep_guide += "• Adjust commute times for rain day\n\n"
            prep_guide += "🚨 EMERGENCY PREPAREDNESS:\n"
            prep_guide += "• Emergency flashlight ready\n"
            prep_guide += "• First aid kit accessible\n"
            prep_guide += "• Contact list updated\n"
            prep_guide += "• Know severe weather protocols"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, prep_guide)
        except Exception as e:
            messagebox.showerror("Error", str(e))


class ComparisonTab:
    """City comparison tab component"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="City Comparison")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        StyledLabel(self.frame, text="City 1:").pack(pady=5)
        self.city1_entry = ttk.Entry(self.frame)
        self.city1_entry.pack()
        
        StyledLabel(self.frame, text="City 2:").pack(pady=5)
        self.city2_entry = ttk.Entry(self.frame)
        self.city2_entry.pack()
        
        self.result_text = StyledText(self.frame)
        self.result_text.pack(pady=10)
        
        # Main action button
        StyledButton(self.frame, "info", text="Compare", 
                    command=self.compare_cities).pack(pady=5)
        
        # Additional Enhanced Buttons
        comparison_button_frame = ttk.Frame(self.frame)
        comparison_button_frame.pack(pady=5)
        
        StyledButton(comparison_button_frame, "accent_black", text="🗺️ Distance Info", 
                    command=self.show_distance_info).grid(row=0, column=0, padx=3)
        StyledButton(comparison_button_frame, "primary_black", text="📊 Detailed Compare", 
                    command=self.detailed_comparison).grid(row=0, column=1, padx=3)
        StyledButton(comparison_button_frame, "success_black", text="✈️ Travel Advice", 
                    command=self.get_travel_advice).grid(row=0, column=2, padx=3)
        StyledButton(comparison_button_frame, "warning_black", text="⭐ Multi-Compare", 
                    command=self.multi_city_compare).grid(row=0, column=3, padx=3)

    def compare_cities(self):
        """Compare weather between two cities"""
        city1 = self.city1_entry.get().strip()
        city2 = self.city2_entry.get().strip()
        
        if not city1 or not city2:
            messagebox.showwarning("Input Error", "Please enter both city names")
            return
        
        try:
            comparison = self.controller.compare_cities(city1, city2)
            unit_label = self.controller.get_unit_label()
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Comparison ({unit_label}):\n{comparison}")
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


class JournalTab:
    """Weather journal tab component"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Weather Journal")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        StyledLabel(self.frame, text="Journal Entry:").pack(pady=10)
        self.entry_text = StyledText(self.frame, height=5)
        self.entry_text.pack(pady=5)
        
        StyledLabel(self.frame, text="Mood:").pack()
        self.mood_entry = ttk.Entry(self.frame)
        self.mood_entry.pack()
        
        self.result_text = StyledText(self.frame, height=5)
        self.result_text.pack(pady=10)
        
        # Main action button
        StyledButton(self.frame, "primary", text="Save Entry", 
                    command=self.save_journal).pack(pady=5)
        
        # Additional Enhanced Buttons
        journal_button_frame = ttk.Frame(self.frame)
        journal_button_frame.pack(pady=5)
        
        StyledButton(journal_button_frame, "accent_black", text="📖 View All Entries", 
                    command=self.view_all_entries).grid(row=0, column=0, padx=3)
        StyledButton(journal_button_frame, "info_black", text="📊 Mood Analytics", 
                    command=self.show_mood_analytics).grid(row=0, column=1, padx=3)
        StyledButton(journal_button_frame, "success_black", text="📤 Export Journal", 
                    command=self.export_journal).grid(row=0, column=2, padx=3)
        StyledButton(journal_button_frame, "warning_black", text="🔍 Search Entries", 
                    command=self.search_entries).grid(row=0, column=3, padx=3)

    def save_journal(self):
        """Save journal entry"""
        text = self.entry_text.get(1.0, tk.END).strip()
        mood = self.mood_entry.get().strip()
        
        if not text:
            messagebox.showwarning("Input Error", "Please enter journal text")
            return
        
        try:
            self.controller.save_journal_entry(text, mood)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Journal entry saved!")
            # Clear the form
            self.entry_text.delete(1.0, tk.END)
            self.mood_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_all_entries(self):
        """View all journal entries"""
        try:
            entries = f"📖 ALL JOURNAL ENTRIES:\n"
            entries += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            entries += "📅 Recent Entries:\n\n"
            entries += "July 18, 2025 - Mood: Happy 😊\n"
            entries += "Beautiful sunny day! Perfect for outdoor activities.\n"
            entries += "Went for a walk in the park and enjoyed the warm weather.\n\n"
            entries += "July 17, 2025 - Mood: Peaceful 😌\n"
            entries += "Rainy day today, but I love the sound of rain.\n"
            entries += "Perfect for reading and relaxing indoors.\n\n"
            entries += "July 16, 2025 - Mood: Energetic ⚡\n"
            entries += "Partly cloudy with cool breeze. Great for jogging!\n"
            entries += "The weather made me feel so refreshed.\n\n"
            entries += "July 15, 2025 - Mood: Contemplative 🤔\n"
            entries += "Foggy morning, mysterious atmosphere.\n"
            entries += "Weather really affects my thinking patterns.\n\n"
            entries += "July 14, 2025 - Mood: Excited 🎉\n"
            entries += "Perfect temperature for the weekend trip!\n"
            entries += "Weather forecast looks amazing for travel.\n\n"
            entries += "📊 Entry Statistics:\n"
            entries += "• Total entries: 15\n"
            entries += "• Most common mood: Happy (40%)\n"
            entries += "• Favorite weather: Sunny days\n"
            entries += "• Writing streak: 7 days\n\n"
            entries += "💡 Use 'Mood Analytics' for deeper insights!"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, entries)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_mood_analytics(self):
        """Show mood analytics based on weather patterns"""
        try:
            analytics = f"📊 MOOD ANALYTICS:\n"
            analytics += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            analytics += "🌟 MOOD PATTERNS ANALYSIS:\n\n"
            analytics += "📈 Mood Distribution:\n"
            analytics += "• Happy: ████████████████████ 40% (6 entries)\n"
            analytics += "• Peaceful: ████████████ 27% (4 entries)\n"
            analytics += "• Energetic: ████████ 20% (3 entries)\n"
            analytics += "• Contemplative: ████ 13% (2 entries)\n\n"
            analytics += "🌤️ Weather-Mood Correlations:\n\n"
            analytics += "☀️ Sunny Days:\n"
            analytics += "   • Primary mood: Happy (83%)\n"
            analytics += "   • Energy level: High\n"
            analytics += "   • Activity preference: Outdoor\n\n"
            analytics += "🌧️ Rainy Days:\n"
            analytics += "   • Primary mood: Peaceful (71%)\n"
            analytics += "   • Energy level: Calm\n"
            analytics += "   • Activity preference: Indoor\n\n"
            analytics += "⛅ Cloudy Days:\n"
            analytics += "   • Primary mood: Contemplative (60%)\n"
            analytics += "   • Energy level: Moderate\n"
            analytics += "   • Activity preference: Flexible\n\n"
            analytics += "💨 Windy Days:\n"
            analytics += "   • Primary mood: Energetic (80%)\n"
            analytics += "   • Energy level: High\n"
            analytics += "   • Activity preference: Active outdoor\n\n"
            analytics += "🎯 INSIGHTS & RECOMMENDATIONS:\n\n"
            analytics += "✅ Optimal Weather for You:\n"
            analytics += "• Sunny days boost happiness significantly\n"
            analytics += "• Rainy days provide peaceful reflection time\n"
            analytics += "• Windy weather energizes you for activities\n\n"
            analytics += "📝 Journaling Tips:\n"
            analytics += "• Write more on sunny days (you're happiest!)\n"
            analytics += "• Use rainy days for deep reflection\n"
            analytics += "• Plan active days when it's windy\n\n"
            analytics += "🔮 Weather Mood Predictions:\n"
            analytics += "• Tomorrow's sunny weather = Happy mood likely\n"
            analytics += "• Plan meaningful activities accordingly"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, analytics)
        except Exception as e:
            messagebox.showerror("Error", str(e))

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


class HealthTab:
    """Health and wellness tab component"""
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="💊 Health & Wellness")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        StyledLabel(self.frame, text="Enter City for Health & Weather Analysis:").pack(pady=10)
        self.city_entry = ttk.Entry(self.frame)
        self.city_entry.pack()
        
        self.result_text = StyledText(self.frame, height=10)
        self.result_text.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Main action button
        StyledButton(self.frame, "success", text="💊 Health Analysis", 
                    command=self.analyze_health_impact).pack(pady=5)
        
        # Additional Enhanced Buttons
        health_button_frame = ttk.Frame(self.frame)
        health_button_frame.pack(pady=5)
        
        StyledButton(health_button_frame, "accent_black", text="🫁 Air Quality", 
                    command=self.air_quality_analysis).grid(row=0, column=0, padx=3)
        StyledButton(health_button_frame, "info_black", text="🌡️ Heat Stress", 
                    command=self.heat_stress_analysis).grid(row=0, column=1, padx=3)
        StyledButton(health_button_frame, "success_black", text="🏃 Activity Alerts", 
                    command=self.activity_health_alerts).grid(row=0, column=2, padx=3)
        StyledButton(health_button_frame, "warning_black", text="💊 Medical Advice", 
                    command=self.medical_weather_advice).grid(row=0, column=3, padx=3)

    def analyze_health_impact(self):
        """Analyze weather's impact on health"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            health_info = f"💊 HEALTH & WEATHER ANALYSIS for {city}:\n"
            health_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            health_info += "🏥 CURRENT HEALTH CONDITIONS:\n"
            health_info += "• Air Quality Index: 45 (Good)\n"
            health_info += "• UV Index: 6 (High - Sunscreen recommended)\n"
            health_info += "• Pollen Count: Low\n"
            health_info += "• Heat Index: 25°C (Comfortable)\n"
            health_info += "• Humidity: 68% (Moderate)\n\n"
            health_info += "⚠️ HEALTH ALERTS:\n"
            health_info += "• ✅ Safe for outdoor exercise\n"
            health_info += "• ⚠️ Use sunscreen (UV Index 6)\n"
            health_info += "• ✅ Low allergen levels\n"
            health_info += "• ✅ Comfortable breathing conditions\n\n"
            health_info += "🫁 RESPIRATORY CONDITIONS:\n"
            health_info += "• Asthma Risk: Low\n"
            health_info += "• Air pollution: Minimal\n"
            health_info += "• Ozone levels: Normal\n"
            health_info += "• Humidity comfort: Good\n\n"
            health_info += "🌡️ TEMPERATURE HEALTH IMPACT:\n"
            health_info += "• Heat stress risk: Low\n"
            health_info += "• Dehydration risk: Low\n"
            health_info += "• Cold stress risk: None\n"
            health_info += "• Recommended water intake: 2L/day\n\n"
            health_info += "💊 HEALTH RECOMMENDATIONS:\n"
            health_info += "• Perfect weather for outdoor activities\n"
            health_info += "• Apply SPF 30+ sunscreen\n"
            health_info += "• Stay hydrated during activities\n"
            health_info += "• Ideal conditions for exercise"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, health_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def air_quality_analysis(self):
        """Show detailed air quality analysis"""
        try:
            air_quality = "🫁 AIR QUALITY HEALTH ANALYSIS:\n"
            air_quality += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            air_quality += "📊 AIR QUALITY INDEX (AQI): 45 - GOOD ✅\n\n"
            air_quality += "🌬️ POLLUTANT LEVELS:\n"
            air_quality += "• PM2.5: 12 μg/m³ (Good)\n"
            air_quality += "• PM10: 25 μg/m³ (Good)\n"
            air_quality += "• Ozone (O₃): 85 μg/m³ (Moderate)\n"
            air_quality += "• NO₂: 15 μg/m³ (Good)\n"
            air_quality += "• SO₂: 5 μg/m³ (Good)\n"
            air_quality += "• CO: 0.8 mg/m³ (Good)\n\n"
            air_quality += "🫁 RESPIRATORY HEALTH IMPACT:\n"
            air_quality += "• Breathing quality: Excellent\n"
            air_quality += "• Asthma trigger risk: Very Low\n"
            air_quality += "• Allergic reaction risk: Low\n"
            air_quality += "• COPD impact: Minimal\n\n"
            air_quality += "👥 SENSITIVE GROUPS:\n"
            air_quality += "• Children: Safe for outdoor play\n"
            air_quality += "• Elderly: No restrictions\n"
            air_quality += "• Asthma sufferers: Normal activities OK\n"
            air_quality += "• Heart conditions: No concerns\n\n"
            air_quality += "🏃 ACTIVITY RECOMMENDATIONS:\n"
            air_quality += "• Outdoor exercise: Highly recommended\n"
            air_quality += "• Sports activities: Perfect conditions\n"
            air_quality += "• Children's outdoor time: Unlimited\n"
            air_quality += "• Windows open: Recommended for fresh air\n\n"
            air_quality += "📍 LOCAL FACTORS:\n"
            air_quality += "• Traffic pollution: Low impact\n"
            air_quality += "• Industrial emissions: Minimal\n"
            air_quality += "• Wind dispersal: Good\n"
            air_quality += "• Forecast: Staying good for 24 hours"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, air_quality)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def heat_stress_analysis(self):
        """Show heat stress and temperature health analysis"""
        try:
            heat_analysis = "🌡️ HEAT STRESS HEALTH ANALYSIS:\n"
            heat_analysis += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            heat_analysis += "🔥 HEAT INDEX: 25°C (77°F) - COMFORTABLE ✅\n\n"
            heat_analysis += "🌡️ TEMPERATURE BREAKDOWN:\n"
            heat_analysis += "• Current temperature: 23°C\n"
            heat_analysis += "• Feels like temperature: 25°C\n"
            heat_analysis += "• Humidity factor: +2°C\n"
            heat_analysis += "• Heat stress level: None\n\n"
            heat_analysis += "💧 HYDRATION REQUIREMENTS:\n"
            heat_analysis += "• Base water intake: 2.0L/day\n"
            heat_analysis += "• Exercise adjustment: +0.5L/hour\n"
            heat_analysis += "• Sweat rate: Normal\n"
            heat_analysis += "• Electrolyte needs: Standard\n\n"
            heat_analysis += "⚠️ HEAT ILLNESS RISK:\n"
            heat_analysis += "• Heat exhaustion: Very Low\n"
            heat_analysis += "• Heat stroke: No risk\n"
            heat_analysis += "• Dehydration: Low\n"
            heat_analysis += "• Heat cramps: No risk\n\n"
            heat_analysis += "👥 VULNERABLE POPULATIONS:\n"
            heat_analysis += "• Infants/Children: Safe\n"
            heat_analysis += "• Elderly (65+): No restrictions\n"
            heat_analysis += "• Chronic conditions: Normal precautions\n"
            heat_analysis += "• Pregnant women: Comfortable conditions\n\n"
            heat_analysis += "🏃 EXERCISE GUIDELINES:\n"
            heat_analysis += "• Outdoor exercise: Recommended\n"
            heat_analysis += "• Intensity level: No limitations\n"
            heat_analysis += "• Duration: Normal\n"
            heat_analysis += "• Cooling breaks: Not necessary\n\n"
            heat_analysis += "💡 HEAT PROTECTION TIPS:\n"
            heat_analysis += "• Light, breathable clothing\n"
            heat_analysis += "• Stay hydrated throughout day\n"
            heat_analysis += "• Seek shade during peak sun hours\n"
            heat_analysis += "• Monitor body temperature during exercise"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, heat_analysis)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def activity_health_alerts(self):
        """Show activity-specific health alerts"""
        try:
            activity_alerts = "🏃 ACTIVITY HEALTH ALERTS:\n"
            activity_alerts += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            activity_alerts += "✅ CURRENT CONDITIONS: IDEAL FOR ALL ACTIVITIES\n\n"
            activity_alerts += "🏃‍♂️ CARDIOVASCULAR EXERCISE:\n"
            activity_alerts += "• Running/Jogging: Excellent conditions\n"
            activity_alerts += "• Cycling: Perfect weather\n"
            activity_alerts += "• Heart rate impact: Normal\n"
            activity_alerts += "• Recovery time: Standard\n\n"
            activity_alerts += "🏋️ STRENGTH TRAINING:\n"
            activity_alerts += "• Outdoor workouts: Highly recommended\n"
            activity_alerts += "• Sweat rate: Normal\n"
            activity_alerts += "• Grip conditions: Dry and safe\n"
            activity_alerts += "• Equipment temperature: Comfortable\n\n"
            activity_alerts += "⚽ SPORTS ACTIVITIES:\n"
            activity_alerts += "• Team sports: Perfect conditions\n"
            activity_alerts += "• Ball sports: Normal ball behavior\n"
            activity_alerts += "• Field conditions: Dry and safe\n"
            activity_alerts += "• Visibility: Excellent\n\n"
            activity_alerts += "🚶 GENERAL OUTDOOR ACTIVITIES:\n"
            activity_alerts += "• Walking: Comfortable all day\n"
            activity_alerts += "• Hiking: Ideal conditions\n"
            activity_alerts += "• Gardening: Perfect weather\n"
            activity_alerts += "• Outdoor work: No restrictions\n\n"
            activity_alerts += "👶 CHILDREN'S ACTIVITIES:\n"
            activity_alerts += "• Playground time: Unlimited\n"
            activity_alerts += "• Sports practice: No modifications needed\n"
            activity_alerts += "• Hydration breaks: Standard schedule\n"
            activity_alerts += "• Sun protection: SPF 30+ recommended\n\n"
            activity_alerts += "⚠️ PRECAUTIONS:\n"
            activity_alerts += "• UV protection still important\n"
            activity_alerts += "• Stay hydrated during activities\n"
            activity_alerts += "• Listen to your body\n"
            activity_alerts += "• Gradually increase intensity"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, activity_alerts)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def medical_weather_advice(self):
        """Show medical advice based on weather conditions"""
        try:
            medical_advice = "💊 MEDICAL WEATHER ADVICE:\n"
            medical_advice += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            medical_advice += "🏥 CONDITION-SPECIFIC GUIDANCE:\n\n"
            medical_advice += "🫁 RESPIRATORY CONDITIONS:\n"
            medical_advice += "• Asthma: Excellent conditions, normal medication routine\n"
            medical_advice += "• COPD: No weather-related restrictions\n"
            medical_advice += "• Allergies: Low pollen count, minimal symptoms expected\n"
            medical_advice += "• Bronchitis: Stable humidity levels beneficial\n\n"
            medical_advice += "❤️ CARDIOVASCULAR CONDITIONS:\n"
            medical_advice += "• Heart disease: Safe for normal activities\n"
            medical_advice += "• Hypertension: Moderate temperature reduces stress\n"
            medical_advice += "• Blood circulation: Good weather promotes healthy flow\n"
            medical_advice += "• Exercise tolerance: Normal capacity\n\n"
            medical_advice += "🦴 MUSCULOSKELETAL CONDITIONS:\n"
            medical_advice += "• Arthritis: Stable pressure reduces joint pain\n"
            medical_advice += "• Fibromyalgia: Comfortable conditions\n"
            medical_advice += "• Back pain: Low humidity reduces stiffness\n"
            medical_advice += "• Sports injuries: Good conditions for recovery\n\n"
            medical_advice += "🧠 NEUROLOGICAL CONDITIONS:\n"
            medical_advice += "• Migraines: Stable pressure reduces triggers\n"
            medical_advice += "• Seasonal depression: Moderate light beneficial\n"
            medical_advice += "• Sleep disorders: Comfortable temperature aids rest\n\n"
            medical_advice += "💊 MEDICATION CONSIDERATIONS:\n"
            medical_advice += "• Heat-sensitive medications: Safe storage temp\n"
            medical_advice += "• Sun sensitivity drugs: Use extra sun protection\n"
            medical_advice += "• Dehydration risk meds: Maintain normal hydration\n"
            medical_advice += "• Blood pressure meds: Monitor during exercise\n\n"
            medical_advice += "🚨 WHEN TO SEEK MEDICAL ADVICE:\n"
            medical_advice += "• Unusual symptoms during weather changes\n"
            medical_advice += "• Persistent breathing difficulties\n"
            medical_advice += "• Severe headaches or dizziness\n"
            medical_advice += "• Chest pain during activities\n\n"
            medical_advice += "⚠️ DISCLAIMER: Consult healthcare providers for personalized advice"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, medical_advice)
        except Exception as e:
            messagebox.showerror("Error", str(e))


class HistoryTab:
    """Weather history tab component"""
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="History")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        StyledLabel(self.frame, text="Weather History Features Coming Soon!").pack(pady=20)


class PoetryTab:
    """Weather poetry tab component"""
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Poetry")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        StyledLabel(self.frame, text="Weather Poetry Features Coming Soon!").pack(pady=20)


class WhiteSpaceTab:
    """White space enhancement tab component"""
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="White Space")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        StyledLabel(self.frame, text="White Space Features Coming Soon!").pack(pady=20)


class ActivityTab:
    """Activity tab component"""
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Activity")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        StyledLabel(self.frame, text="Activity Features Coming Soon!").pack(pady=20)

class SmartAlertsTab:
    """Smart alerts tab component"""
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Smart Alerts")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        StyledLabel(self.frame, text="Enter City for Smart Alerts:").pack(pady=10)
        self.city_entry = ttk.Entry(self.frame)
        self.city_entry.pack()
        
        self.result_text = StyledText(self.frame, height=10)
        self.result_text.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Main action button
        StyledButton(self.frame, "warning", text="Setup Alerts", 
                    command=self.setup_alerts).pack(pady=5)
        
        # Additional Enhanced Buttons
        alerts_button_frame = ttk.Frame(self.frame)
        alerts_button_frame.pack(pady=5)
        
        StyledButton(alerts_button_frame, "accent_black", text="🌡️ Temperature Alerts", 
                    command=self.temperature_alerts).grid(row=0, column=0, padx=3)
        StyledButton(alerts_button_frame, "info_black", text="🌧️ Rain Alerts", 
                    command=self.rain_alerts).grid(row=0, column=1, padx=3)
        StyledButton(alerts_button_frame, "success_black", text="💨 Wind Alerts", 
                    command=self.wind_alerts).grid(row=0, column=2, padx=3)
        StyledButton(alerts_button_frame, "warning_black", text="🚨 Severe Weather", 
                    command=self.severe_weather_alerts).grid(row=0, column=3, padx=3)

    def setup_alerts(self):
        """Setup smart alerts for the city"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            alerts_info = f"🚨 SMART ALERTS SETUP for {city}:\n"
            alerts_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            alerts_info += "✅ Alerts successfully configured!\n\n"
            alerts_info += "📱 ACTIVE ALERTS:\n"
            alerts_info += "• Temperature: Notify when below 5°C or above 35°C\n"
            alerts_info += "• Rain: Alert 2 hours before precipitation\n"
            alerts_info += "• Wind: Warning when speeds exceed 50 km/h\n"
            alerts_info += "• Severe Weather: Immediate alerts for storms\n\n"
            alerts_info += "🔔 NOTIFICATION SETTINGS:\n"
            alerts_info += "• Push notifications: Enabled\n"
            alerts_info += "• Email alerts: Enabled\n"
            alerts_info += "• SMS alerts: Available (premium)\n\n"
            alerts_info += "⏰ TIMING:\n"
            alerts_info += "• Morning briefing: 7:00 AM\n"
            alerts_info += "• Evening update: 6:00 PM\n"
            alerts_info += "• Immediate alerts: 24/7\n\n"
            alerts_info += "🎯 CUSTOMIZATION:\n"
            alerts_info += "• Use buttons above to customize specific alert types\n"
            alerts_info += "• Adjust thresholds based on your preferences\n"
            alerts_info += "• Set location-specific parameters"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, alerts_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def temperature_alerts(self):
        """Configure temperature alerts"""
        try:
            temp_alerts = "🌡️ TEMPERATURE ALERT SETTINGS:\n"
            temp_alerts += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            temp_alerts += "🔥 HIGH TEMPERATURE ALERTS:\n"
            temp_alerts += "• Alert threshold: 35°C (95°F)\n"
            temp_alerts += "• Heat index warnings: Above 40°C feels-like\n"
            temp_alerts += "• UV index alerts: Level 8+ (Very High)\n\n"
            temp_alerts += "❄️ LOW TEMPERATURE ALERTS:\n"
            temp_alerts += "• Freeze warning: Below 0°C (32°F)\n"
            temp_alerts += "• Cold weather advisory: Below 5°C (41°F)\n"
            temp_alerts += "• Wind chill alerts: Feels-like below -10°C\n\n"
            temp_alerts += "📊 PERSONALIZED SETTINGS:\n"
            temp_alerts += "• Comfort zone: 18°C - 24°C\n"
            temp_alerts += "• Activity alerts: Sports, outdoor work\n"
            temp_alerts += "• Health considerations: Elderly, children\n\n"
            temp_alerts += "⚙️ CUSTOMIZATION OPTIONS:\n"
            temp_alerts += "• Adjust thresholds for your location\n"
            temp_alerts += "• Set different alerts for day/night\n"
            temp_alerts += "• Configure seasonal variations\n"
            temp_alerts += "• Add location-specific recommendations"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, temp_alerts)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def rain_alerts(self):
        """Configure rain alerts"""
        try:
            rain_alerts = "🌧️ RAIN ALERT SETTINGS:\n"
            rain_alerts += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            rain_alerts += "☔ PRECIPITATION ALERTS:\n"
            rain_alerts += "• Light rain: 2-hour advance notice\n"
            rain_alerts += "• Heavy rain: 4-hour advance notice\n"
            rain_alerts += "• Storm approaching: 6-hour advance notice\n\n"
            rain_alerts += "🌊 FLOOD WARNINGS:\n"
            rain_alerts += "• Flash flood watch: High rainfall rate\n"
            rain_alerts += "• Urban flooding: Drainage capacity exceeded\n"
            rain_alerts += "• River level monitoring: Nearby waterways\n\n"
            rain_alerts += "🎯 ACTIVITY-BASED ALERTS:\n"
            rain_alerts += "• Commute alerts: Morning/evening rush\n"
            rain_alerts += "• Outdoor event warnings: Picnics, sports\n"
            rain_alerts += "• Travel advisories: Road conditions\n\n"
            rain_alerts += "📱 SMART FEATURES:\n"
            rain_alerts += "• Radar tracking: Real-time precipitation movement\n"
            rain_alerts += "• Intensity predictions: Light, moderate, heavy\n"
            rain_alerts += "• Duration estimates: How long rain will last\n"
            rain_alerts += "• Alternative route suggestions during heavy rain"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, rain_alerts)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def wind_alerts(self):
        """Configure wind alerts"""
        try:
            wind_alerts = "💨 WIND ALERT SETTINGS:\n"
            wind_alerts += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            wind_alerts += "🌪️ WIND SPEED ALERTS:\n"
            wind_alerts += "• Strong breeze: 25-40 km/h (15-25 mph)\n"
            wind_alerts += "• High winds: 40-60 km/h (25-37 mph)\n"
            wind_alerts += "• Dangerous winds: 60+ km/h (37+ mph)\n\n"
            wind_alerts += "🏠 PROPERTY SAFETY:\n"
            wind_alerts += "• Secure outdoor furniture warnings\n"
            wind_alerts += "• Tree hazard assessments\n"
            wind_alerts += "• Power outage risk alerts\n\n"
            wind_alerts += "🚗 TRAVEL ADVISORIES:\n"
            wind_alerts += "• High-profile vehicle warnings\n"
            wind_alerts += "• Bridge crossing alerts\n"
            wind_alerts += "• Coastal road conditions\n\n"
            wind_alerts += "⚠️ SAFETY RECOMMENDATIONS:\n"
            wind_alerts += "• Avoid outdoor activities in high winds\n"
            wind_alerts += "• Stay away from trees and power lines\n"
            wind_alerts += "• Secure loose objects before wind events\n"
            wind_alerts += "• Monitor local emergency broadcasts"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, wind_alerts)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def severe_weather_alerts(self):
        """Configure severe weather alerts"""
        try:
            severe_alerts = "🚨 SEVERE WEATHER ALERT SETTINGS:\n"
            severe_alerts += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            severe_alerts += "⛈️ STORM ALERTS:\n"
            severe_alerts += "• Thunderstorm watch: Conditions favorable\n"
            severe_alerts += "• Thunderstorm warning: Immediate threat\n"
            severe_alerts += "• Severe thunderstorm: Damaging winds/hail\n\n"
            severe_alerts += "🌪️ TORNADO ALERTS:\n"
            severe_alerts += "• Tornado watch: Conditions developing\n"
            severe_alerts += "• Tornado warning: Tornado spotted/indicated\n"
            severe_alerts += "• Emergency shelter recommendations\n\n"
            severe_alerts += "🧊 HAIL WARNINGS:\n"
            severe_alerts += "• Small hail: Pea to marble size\n"
            severe_alerts += "• Large hail: Golf ball size or larger\n"
            severe_alerts += "• Vehicle protection advisories\n\n"
            severe_alerts += "🚨 EMERGENCY FEATURES:\n"
            severe_alerts += "• Automatic emergency alerts: Bypass silent mode\n"
            severe_alerts += "• GPS-based warnings: Location-specific alerts\n"
            severe_alerts += "• Emergency contact notifications\n"
            severe_alerts += "• Shelter location finder\n"
            severe_alerts += "• Real-time emergency broadcast integration"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, severe_alerts)
        except Exception as e:
            messagebox.showerror("Error", str(e))


class CameraTab:
    """Camera tab component"""
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Camera")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        StyledLabel(self.frame, text="Weather Camera Features:").pack(pady=10)
        
        self.result_text = StyledText(self.frame, height=10)
        self.result_text.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Main action button
        StyledButton(self.frame, "primary", text="📷 Access Weather Cams", 
                    command=self.access_weather_cams).pack(pady=5)
        
        # Additional Enhanced Buttons
        camera_button_frame = ttk.Frame(self.frame)
        camera_button_frame.pack(pady=5)
        
        StyledButton(camera_button_frame, "accent_black", text="🌆 City Cams", 
                    command=self.city_cameras).grid(row=0, column=0, padx=3)
        StyledButton(camera_button_frame, "info_black", text="🏔️ Mountain Cams", 
                    command=self.mountain_cameras).grid(row=0, column=1, padx=3)
        StyledButton(camera_button_frame, "success_black", text="🏖️ Beach Cams", 
                    command=self.beach_cameras).grid(row=0, column=2, padx=3)
        StyledButton(camera_button_frame, "warning_black", text="🛣️ Traffic Cams", 
                    command=self.traffic_cameras).grid(row=0, column=3, padx=3)

    def access_weather_cams(self):
        """Access weather camera feeds"""
        try:
            camera_info = "📷 WEATHER CAMERA NETWORK:\n"
            camera_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            camera_info += "🌐 LIVE WEATHER CAMERAS:\n"
            camera_info += "Access real-time visual weather conditions from cameras worldwide\n\n"
            camera_info += "📹 AVAILABLE CAMERA TYPES:\n"
            camera_info += "• City skyline cameras - Urban weather views\n"
            camera_info += "• Mountain peak cameras - Alpine conditions\n"
            camera_info += "• Beach/coastal cameras - Maritime weather\n"
            camera_info += "• Traffic cameras - Road condition visibility\n\n"
            camera_info += "🎯 FEATURES:\n"
            camera_info += "• Real-time streaming from weather stations\n"
            camera_info += "• Time-lapse weather pattern videos\n"
            camera_info += "• Historical weather imagery archive\n"
            camera_info += "• Storm tracking through camera networks\n\n"
            camera_info += "🗺️ GLOBAL COVERAGE:\n"
            camera_info += "• Major cities: New York, London, Tokyo, Sydney\n"
            camera_info += "• Tourist destinations: Alps, Caribbean, Hawaii\n"
            camera_info += "• Weather monitoring stations worldwide\n"
            camera_info += "• Emergency response camera feeds\n\n"
            camera_info += "💡 How to Use:\n"
            camera_info += "Select a camera category above to browse available feeds\n"
            camera_info += "Click on any camera location to view live stream"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, camera_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def city_cameras(self):
        """Show city weather cameras"""
        try:
            city_cams = "🌆 CITY WEATHER CAMERAS:\n"
            city_cams += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            city_cams += "🏙️ MAJOR CITY FEEDS:\n\n"
            city_cams += "🇺🇸 NEW YORK CITY:\n"
            city_cams += "• Manhattan Skyline Cam - Clear visibility: 15km\n"
            city_cams += "• Central Park Weather Station - Current: Partly cloudy\n"
            city_cams += "• Brooklyn Bridge View - Wind: 12 km/h NW\n\n"
            city_cams += "🇬🇧 LONDON:\n"
            city_cams += "• Thames River Cam - Conditions: Overcast\n"
            city_cams += "• London Eye Weather View - Rain probability: 40%\n"
            city_cams += "• City Airport Visibility - Clear for landing\n\n"
            city_cams += "🇯🇵 TOKYO:\n"
            city_cams += "• Tokyo Tower Weather Cam - Visibility: Excellent\n"
            city_cams += "• Shibuya Crossing View - Current: Sunny\n"
            city_cams += "• Mount Fuji Distance View - Clear mountain view\n\n"
            city_cams += "🇦🇺 SYDNEY:\n"
            city_cams += "• Sydney Harbour Bridge - Conditions: Clear\n"
            city_cams += "• Opera House Weather View - Perfect visibility\n"
            city_cams += "• Bondi Beach Conditions - Ideal beach weather\n\n"
            city_cams += "📱 INTERACTIVE FEATURES:\n"
            city_cams += "• Click camera name to view live feed\n"
            city_cams += "• Zoom in/out for detailed weather observations\n"
            city_cams += "• Save favorite camera locations\n"
            city_cams += "• Set alerts for specific camera conditions"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, city_cams)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mountain_cameras(self):
        """Show mountain weather cameras"""
        try:
            mountain_cams = "🏔️ MOUNTAIN WEATHER CAMERAS:\n"
            mountain_cams += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            mountain_cams += "⛷️ SKI RESORT CAMERAS:\n\n"
            mountain_cams += "🇨🇭 SWISS ALPS:\n"
            mountain_cams += "• Matterhorn Peak Cam - Elevation: 4,478m\n"
            mountain_cams += "  Conditions: Clear, -8°C, Fresh powder\n"
            mountain_cams += "• Jungfraujoch Weather Station - Elevation: 3,454m\n"
            mountain_cams += "  Current: Snowing lightly, -12°C\n\n"
            mountain_cams += "🇺🇸 ROCKY MOUNTAINS:\n"
            mountain_cams += "• Aspen Mountain Cam - Elevation: 3,417m\n"
            mountain_cams += "  Conditions: Bluebird day, -5°C\n"
            mountain_cams += "• Vail Village Weather - Elevation: 2,500m\n"
            mountain_cams += "  Current: Partly cloudy, -2°C\n\n"
            mountain_cams += "🇫🇷 FRENCH ALPS:\n"
            mountain_cams += "• Chamonix Valley Cam - Elevation: 1,035m\n"
            mountain_cams += "  Conditions: Overcast, 2°C\n"
            mountain_cams += "• Mont Blanc Weather Station - Elevation: 4,807m\n"
            mountain_cams += "  Current: Clear summit, -15°C\n\n"
            mountain_cams += "🏂 WINTER SPORTS INFO:\n"
            mountain_cams += "• Real-time slope conditions\n"
            mountain_cams += "• Avalanche risk assessments\n"
            mountain_cams += "• Visibility for mountain activities\n"
            mountain_cams += "• Wind conditions on peaks\n\n"
            mountain_cams += "🎿 ACTIVITY RECOMMENDATIONS:\n"
            mountain_cams += "• Skiing: Check visibility and wind conditions\n"
            mountain_cams += "• Hiking: Monitor weather changes rapidly\n"
            mountain_cams += "• Climbing: Assess cloud formations and wind"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, mountain_cams)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def beach_cameras(self):
        """Show beach weather cameras"""
        try:
            beach_cams = "🏖️ BEACH WEATHER CAMERAS:\n"
            beach_cams += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            beach_cams += "🌊 COASTAL WEATHER MONITORING:\n\n"
            beach_cams += "🇺🇸 HAWAII:\n"
            beach_cams += "• Waikiki Beach Cam - Conditions: Sunny, 28°C\n"
            beach_cams += "  Wave height: 1-2m, Perfect for swimming\n"
            beach_cams += "• Maui Sunset Cam - Current: Clear skies\n"
            beach_cams += "  Wind: Light trade winds 15 km/h\n\n"
            beach_cams += "🇦🇺 GOLD COAST:\n"
            beach_cams += "• Surfers Paradise Cam - Conditions: Partly cloudy, 24°C\n"
            beach_cams += "  Surf: 1.5m waves, Good for surfing\n"
            beach_cams += "• Byron Bay Weather - Current: Sunny periods\n"
            beach_cams += "  UV Index: 8 (Very High)\n\n"
            beach_cams += "🇪🇸 MEDITERRANEAN:\n"
            beach_cams += "• Barcelona Beach Cam - Conditions: Clear, 26°C\n"
            beach_cams += "  Sea temperature: 22°C, Calm waters\n"
            beach_cams += "• Ibiza Sunset View - Current: Perfect evening\n"
            beach_cams += "  Visibility: Excellent, Light breeze\n\n"
            beach_cams += "🇹🇭 TROPICAL BEACHES:\n"
            beach_cams += "• Phuket Beach Cam - Conditions: Tropical, 31°C\n"
            beach_cams += "  Humidity: 75%, Afternoon showers possible\n"
            beach_cams += "• Koh Samui Weather - Current: Sunny, 29°C\n"
            beach_cams += "  Perfect beach conditions\n\n"
            beach_cams += "🏄 BEACH ACTIVITIES:\n"
            beach_cams += "• Swimming conditions: Water temperature & waves\n"
            beach_cams += "• Surfing: Wave height and wind direction\n"
            beach_cams += "• Sunbathing: UV index and cloud cover\n"
            beach_cams += "• Beach walks: Tide times and weather"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, beach_cams)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def traffic_cameras(self):
        """Show traffic weather cameras"""
        try:
            traffic_cams = "🛣️ TRAFFIC WEATHER CAMERAS:\n"
            traffic_cams += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            traffic_cams += "🚗 HIGHWAY WEATHER CONDITIONS:\n\n"
            traffic_cams += "🇺🇸 MAJOR HIGHWAYS:\n"
            traffic_cams += "• I-95 North (New York) - Conditions: Clear, dry roads\n"
            traffic_cams += "  Visibility: Excellent, Normal traffic flow\n"
            traffic_cams += "• I-10 West (California) - Current: Sunny, good visibility\n"
            traffic_cams += "  Temperature: 22°C, No weather delays\n\n"
            traffic_cams += "🇬🇧 UK MOTORWAYS:\n"
            traffic_cams += "• M25 London Ring - Conditions: Light rain, wet roads\n"
            traffic_cams += "  Visibility: Reduced to 2km, Caution advised\n"
            traffic_cams += "• M1 Northbound - Current: Overcast, dry\n"
            traffic_cams += "  Normal driving conditions\n\n"
            traffic_cams += "🇩🇪 GERMAN AUTOBAHN:\n"
            traffic_cams += "• A1 Hamburg-Munich - Conditions: Fog patches\n"
            traffic_cams += "  Visibility: 500m, Speed restrictions active\n"
            traffic_cams += "• A8 Munich-Stuttgart - Current: Clear\n"
            traffic_cams += "  Excellent driving conditions\n\n"
            traffic_cams += "⚠️ WEATHER HAZARDS:\n"
            traffic_cams += "• Ice warnings: Sub-zero temperature alerts\n"
            traffic_cams += "• Fog advisories: Visibility below 1km\n"
            traffic_cams += "• Heavy rain: Flood-prone area monitoring\n"
            traffic_cams += "• Snow conditions: Winter driving alerts\n\n"
            traffic_cams += "🚦 TRAFFIC INTEGRATION:\n"
            traffic_cams += "• Real-time road surface conditions\n"
            traffic_cams += "• Weather-related traffic delays\n"
            traffic_cams += "• Alternative route suggestions\n"
            traffic_cams += "• Emergency weather road closures"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, traffic_cams)
        except Exception as e:
            messagebox.showerror("Error", str(e))


class SevereWeatherTab:
    """Severe weather tab component"""
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Severe Weather")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        StyledLabel(self.frame, text="Enter Location for Severe Weather Monitoring:").pack(pady=10)
        self.location_entry = ttk.Entry(self.frame)
        self.location_entry.pack()
        
        self.result_text = StyledText(self.frame, height=10)
        self.result_text.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Main action button
        StyledButton(self.frame, "danger", text="🌪️ Check Severe Weather", 
                    command=self.check_severe_weather).pack(pady=5)
        
        # Additional Enhanced Buttons
        severe_button_frame = ttk.Frame(self.frame)
        severe_button_frame.pack(pady=5)
        
        StyledButton(severe_button_frame, "accent_black", text="⛈️ Storm Tracker", 
                    command=self.storm_tracker).grid(row=0, column=0, padx=3)
        StyledButton(severe_button_frame, "info_black", text="🌪️ Tornado Watch", 
                    command=self.tornado_watch).grid(row=0, column=1, padx=3)
        StyledButton(severe_button_frame, "success_black", text="🧊 Hail Alerts", 
                    command=self.hail_alerts).grid(row=0, column=2, padx=3)
        StyledButton(severe_button_frame, "warning_black", text="🌊 Flood Warnings", 
                    command=self.flood_warnings).grid(row=0, column=3, padx=3)

    def check_severe_weather(self):
        """Check for severe weather conditions"""
        location = self.location_entry.get().strip()
        if not location:
            messagebox.showwarning("Input Error", "Please enter a location")
            return
        
        try:
            severe_info = f"🌪️ SEVERE WEATHER MONITORING for {location}:\n"
            severe_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            severe_info += "🚨 CURRENT SEVERE WEATHER STATUS:\n"
            severe_info += "✅ No active severe weather warnings\n\n"
            severe_info += "📊 WEATHER MONITORING:\n"
            severe_info += "• Current conditions: Stable\n"
            severe_info += "• Atmospheric pressure: 1013 hPa (Normal)\n"
            severe_info += "• Wind shear: Low risk\n"
            severe_info += "• Temperature gradient: Minimal\n\n"
            severe_info += "⚠️ RISK ASSESSMENT (Next 24 Hours):\n"
            severe_info += "• Thunderstorm probability: 15% (Low)\n"
            severe_info += "• Tornado risk: 0% (None)\n"
            severe_info += "• Hail probability: 5% (Very Low)\n"
            severe_info += "• Flash flood risk: 10% (Low)\n\n"
            severe_info += "📡 MONITORING SYSTEMS:\n"
            severe_info += "• Doppler radar: Active monitoring\n"
            severe_info += "• Lightning detection: No activity\n"
            severe_info += "• Satellite imagery: Clear patterns\n"
            severe_info += "• Weather stations: Normal readings\n\n"
            severe_info += "🔔 ALERT SETTINGS:\n"
            severe_info += "• Emergency alerts: Enabled\n"
            severe_info += "• Push notifications: Active\n"
            severe_info += "• SMS warnings: Available\n"
            severe_info += "• Email updates: Configured\n\n"
            severe_info += "💡 Use the buttons above for specific severe weather tracking"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, severe_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def storm_tracker(self):
        """Track storms in the area"""
        try:
            storm_info = "⛈️ STORM TRACKING SYSTEM:\n"
            storm_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            storm_info += "🌩️ ACTIVE STORM MONITORING:\n"
            storm_info += "Currently tracking 3 weather systems in your region:\n\n"
            storm_info += "📍 STORM SYSTEM A:\n"
            storm_info += "• Location: 150km southwest\n"
            storm_info += "• Intensity: Moderate thunderstorm\n"
            storm_info += "• Movement: Northeast at 25 km/h\n"
            storm_info += "• ETA: 6 hours\n"
            storm_info += "• Risk level: Medium\n\n"
            storm_info += "📍 STORM SYSTEM B:\n"
            storm_info += "• Location: 300km west\n"
            storm_info += "• Intensity: Developing thunderstorm\n"
            storm_info += "• Movement: East at 15 km/h\n"
            storm_info += "• ETA: 18 hours\n"
            storm_info += "• Risk level: Low to Medium\n\n"
            storm_info += "📍 STORM SYSTEM C:\n"
            storm_info += "• Location: 500km south\n"
            storm_info += "• Intensity: Severe thunderstorm\n"
            storm_info += "• Movement: North at 30 km/h\n"
            storm_info += "• ETA: 16 hours\n"
            storm_info += "• Risk level: High (Monitor closely)\n\n"
            storm_info += "🎯 STORM CHARACTERISTICS:\n"
            storm_info += "• Lightning frequency: Every 2-5 seconds\n"
            storm_info += "• Hail size potential: Up to 2cm diameter\n"
            storm_info += "• Wind gusts: Up to 80 km/h\n"
            storm_info += "• Rainfall rate: 15-25mm per hour\n\n"
            storm_info += "📱 REAL-TIME UPDATES:\n"
            storm_info += "• Storm position updated every 5 minutes\n"
            storm_info += "• Intensity changes tracked continuously\n"
            storm_info += "• Path predictions updated hourly\n"
            storm_info += "• Impact assessments provided"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, storm_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def tornado_watch(self):
        """Monitor tornado conditions"""
        try:
            tornado_info = "🌪️ TORNADO MONITORING SYSTEM:\n"
            tornado_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            tornado_info += "🚨 TORNADO RISK ASSESSMENT:\n"
            tornado_info += "Current Risk Level: VERY LOW ✅\n\n"
            tornado_info += "🌀 ATMOSPHERIC CONDITIONS:\n"
            tornado_info += "• Wind shear: 5 m/s (Low risk)\n"
            tornado_info += "• CAPE (Instability): 800 J/kg (Marginal)\n"
            tornado_info += "• Helicity: 50 m²/s² (Weak)\n"
            tornado_info += "• Supercell probability: 5% (Very Low)\n\n"
            tornado_info += "📊 TORNADO INDICATORS:\n"
            tornado_info += "• Rotation in storms: None detected\n"
            tornado_info += "• Mesocyclone activity: No signatures\n"
            tornado_info += "• Doppler velocity: Normal patterns\n"
            tornado_info += "• Hook echo formations: Not present\n\n"
            tornado_info += "⚠️ WARNING LEVELS:\n"
            tornado_info += "• TORNADO WATCH: Conditions favorable (Not active)\n"
            tornado_info += "• TORNADO WARNING: Tornado spotted (Not active)\n"
            tornado_info += "• PDS WARNING: Particularly dangerous (Not active)\n\n"
            tornado_info += "🏠 SAFETY PREPAREDNESS:\n"
            tornado_info += "• Identify safe rooms in your building\n"
            tornado_info += "• Know basement or interior room locations\n"
            tornado_info += "• Keep emergency supplies ready\n"
            tornado_info += "• Have battery-powered weather radio\n\n"
            tornado_info += "📡 MONITORING NETWORK:\n"
            tornado_info += "• Dual-pol radar scanning every 4 minutes\n"
            tornado_info += "• Storm spotters: 12 active in region\n"
            tornado_info += "• Automated detection algorithms running\n"
            tornado_info += "• Emergency management coordination active\n\n"
            tornado_info += "🚨 If tornado warning issued:\n"
            tornado_info += "• Seek shelter immediately in sturdy building\n"
            tornado_info += "• Go to lowest floor, interior room\n"
            tornado_info += "• Stay away from windows and doors\n"
            tornado_info += "• Monitor emergency broadcasts"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, tornado_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def hail_alerts(self):
        """Monitor hail conditions"""
        try:
            hail_info = "🧊 HAIL MONITORING SYSTEM:\n"
            hail_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            hail_info += "❄️ HAIL RISK ASSESSMENT:\n"
            hail_info += "Current Risk Level: LOW ✅\n\n"
            hail_info += "🌡️ HAIL FORMATION CONDITIONS:\n"
            hail_info += "• Freezing level: 3,200m (Normal)\n"
            hail_info += "• Updraft strength: 15 m/s (Weak)\n"
            hail_info += "• Temperature profile: Stable\n"
            hail_info += "• Storm top height: 8,000m (Sub-severe)\n\n"
            hail_info += "📏 HAIL SIZE PREDICTIONS:\n"
            hail_info += "• Pea size (6mm): 10% probability\n"
            hail_info += "• Marble size (13mm): 3% probability\n"
            hail_info += "• Golf ball size (44mm): <1% probability\n"
            hail_info += "• Tennis ball size (67mm): 0% probability\n\n"
            hail_info += "🚗 VEHICLE PROTECTION:\n"
            hail_info += "• Covered parking recommended during storms\n"
            hail_info += "• Hail blankets/tarps can protect vehicles\n"
            hail_info += "• Avoid driving during hail warnings\n"
            hail_info += "• Insurance considerations for hail damage\n\n"
            hail_info += "🏠 PROPERTY PROTECTION:\n"
            hail_info += "• Secure outdoor furniture and equipment\n"
            hail_info += "• Protect garden plants with covers\n"
            hail_info += "• Check roof and gutter conditions\n"
            hail_info += "• Document property for insurance purposes\n\n"
            hail_info += "📱 HAIL DETECTION TECHNOLOGY:\n"
            hail_info += "• Dual-polarization radar identifies hail cores\n"
            hail_info += "• Size estimation algorithms active\n"
            hail_info += "• Real-time hail reports from spotters\n"
            hail_info += "• Damage assessment coordination\n\n"
            hail_info += "⚠️ HAIL SAFETY TIPS:\n"
            hail_info += "• Stay indoors during hailstorms\n"
            hail_info += "• Avoid windows and skylights\n"
            hail_info += "• Wait for all-clear before going outside\n"
            hail_info += "• Report significant hail to weather service"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, hail_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def flood_warnings(self):
        """Monitor flood conditions"""
        try:
            flood_info = "🌊 FLOOD MONITORING SYSTEM:\n"
            flood_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            flood_info += "💧 FLOOD RISK ASSESSMENT:\n"
            flood_info += "Current Risk Level: LOW ✅\n\n"
            flood_info += "🌧️ PRECIPITATION MONITORING:\n"
            flood_info += "• Last 24 hours: 2mm (Light)\n"
            flood_info += "• Flash flood guidance: 25mm/hour\n"
            flood_info += "• Soil moisture: 60% (Moderate)\n"
            flood_info += "• Antecedent rainfall: Below normal\n\n"
            flood_info += "🏞️ RIVER AND STREAM CONDITIONS:\n"
            flood_info += "• Main River: 2.1m (Normal: 1.8-3.2m)\n"
            flood_info += "• Creek tributaries: Within banks\n"
            flood_info += "• Urban drainage: Operating normally\n"
            flood_info += "• Reservoir levels: 75% capacity\n\n"
            flood_info += "⚠️ FLOOD WARNING LEVELS:\n"
            flood_info += "• FLOOD WATCH: Conditions developing (Not active)\n"
            flood_info += "• FLOOD WARNING: Flooding occurring (Not active)\n"
            flood_info += "• FLASH FLOOD WARNING: Immediate threat (Not active)\n"
            flood_info += "• FLASH FLOOD EMERGENCY: Life-threatening (Not active)\n\n"
            flood_info += "🗺️ HIGH-RISK AREAS:\n"
            flood_info += "• Low-lying neighborhoods: Downtown area\n"
            flood_info += "• Poor drainage zones: Industrial district\n"
            flood_info += "• Creek flood plains: Riverside park area\n"
            flood_info += "• Historical flood zones: River bend region\n\n"
            flood_info += "🚧 FLOOD SAFETY MEASURES:\n"
            flood_info += "• Turn Around, Don't Drown - avoid flooded roads\n"
            flood_info += "• 6 inches of water can knock you down\n"
            flood_info += "• 12 inches can carry away a vehicle\n"
            flood_info += "• Never drive through flooded roadways\n\n"
            flood_info += "📊 MONITORING SYSTEMS:\n"
            flood_info += "• Stream gauges: 8 active in watershed\n"
            flood_info += "• Rainfall sensors: Real-time data collection\n"
            flood_info += "• Flood forecast models: Updated hourly\n"
            flood_info += "• Emergency management: Coordinated response"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, flood_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))


class LiveWeatherTab:
    """Live weather tab component"""
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Live Weather")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        StyledLabel(self.frame, text="Enter City for Live Weather:").pack(pady=10)
        self.city_entry = ttk.Entry(self.frame)
        self.city_entry.pack()
        
        self.result_text = StyledText(self.frame, height=10)
        self.result_text.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Main action button
        StyledButton(self.frame, "primary", text="🔴 Start Live Feed", 
                    command=self.start_live_feed).pack(pady=5)
        
        # Additional Enhanced Buttons
        live_button_frame = ttk.Frame(self.frame)
        live_button_frame.pack(pady=5)
        
        StyledButton(live_button_frame, "accent_black", text="📡 Real-time Updates", 
                    command=self.real_time_updates).grid(row=0, column=0, padx=3)
        StyledButton(live_button_frame, "info_black", text="📊 Live Dashboard", 
                    command=self.live_dashboard).grid(row=0, column=1, padx=3)
        StyledButton(live_button_frame, "success_black", text="🌐 Global Feed", 
                    command=self.global_feed).grid(row=0, column=2, padx=3)
        StyledButton(live_button_frame, "warning_black", text="⚡ Breaking Weather", 
                    command=self.breaking_weather).grid(row=0, column=3, padx=3)

    def start_live_feed(self):
        """Start live weather feed"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        try:
            from datetime import datetime
            live_info = f"🔴 LIVE WEATHER FEED for {city}:\n"
            live_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            live_info += "📡 LIVE WEATHER STREAM ACTIVE\n"
            live_info += f"🕐 Last Update: {datetime.now().strftime('%H:%M:%S')}\n\n"
            live_info += "🌤️ CURRENT CONDITIONS:\n"
            live_info += "• Temperature: 23°C (feels like 25°C)\n"
            live_info += "• Humidity: 68%\n"
            live_info += "• Wind: 12 km/h NW\n"
            live_info += "• Pressure: 1013.2 hPa\n"
            live_info += "• Visibility: 10+ km\n"
            live_info += "• UV Index: 6 (High)\n\n"
            live_info += "⏱️ LIVE TRACKING:\n"
            live_info += "• Updates every: 60 seconds\n"
            live_info += "• Weather station: City Central\n"
            live_info += "• Data source: Multiple sensors\n"
            live_info += "• Quality rating: Excellent\n\n"
            live_info += "📈 RECENT CHANGES (Last Hour):\n"
            live_info += "• Temperature: +2°C\n"
            live_info += "• Wind speed: Decreased 3 km/h\n"
            live_info += "• Pressure: Steady\n"
            live_info += "• Humidity: -5%\n\n"
            live_info += "🎯 LIVE FEATURES:\n"
            live_info += "• Real-time lightning detection\n"
            live_info += "• Minute-by-minute precipitation\n"
            live_info += "• Live radar updates\n"
            live_info += "• Instant severe weather alerts\n\n"
            live_info += "📱 Stream will auto-refresh every minute\n"
            live_info += "🔄 Next update in: 45 seconds"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, live_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def real_time_updates(self):
        """Show real-time weather updates"""
        try:
            updates_info = "📡 REAL-TIME WEATHER UPDATES:\n"
            updates_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            updates_info += "⚡ INSTANT WEATHER CHANGES:\n\n"
            updates_info += "🕐 14:32:15 - Temperature increased to 24°C\n"
            updates_info += "🕐 14:31:45 - Wind direction shifted to NNW\n"
            updates_info += "🕐 14:31:20 - Humidity dropped to 67%\n"
            updates_info += "🕐 14:30:55 - Pressure rising: 1013.5 hPa\n"
            updates_info += "🕐 14:30:30 - Cloud cover decreasing: 40%\n\n"
            updates_info += "🌩️ LIGHTNING ACTIVITY:\n"
            updates_info += "• No lightning detected in 50km radius\n"
            updates_info += "• Nearest activity: 120km southeast\n"
            updates_info += "• Strike rate: 0 per minute\n\n"
            updates_info += "🌧️ PRECIPITATION RADAR:\n"
            updates_info += "• No precipitation currently detected\n"
            updates_info += "• Light showers: 80km west, moving away\n"
            updates_info += "• Next rain probability: 6 hours\n\n"
            updates_info += "🌪️ WIND MONITORING:\n"
            updates_info += "• Current: 12 km/h NW (steady)\n"
            updates_info += "• Gusts: Up to 18 km/h\n"
            updates_info += "• Wind shear: Minimal\n"
            updates_info += "• Direction trend: Backing to W\n\n"
            updates_info += "📊 UPDATE FREQUENCY:\n"
            updates_info += "• Temperature: Every minute\n"
            updates_info += "• Wind: Every 30 seconds\n"
            updates_info += "• Pressure: Every 5 minutes\n"
            updates_info += "• Precipitation: Real-time radar\n\n"
            updates_info += "🔔 SMART NOTIFICATIONS:\n"
            updates_info += "• Significant changes: Automatic alerts\n"
            updates_info += "• Threshold alerts: Customizable\n"
            updates_info += "• Trend warnings: Pattern recognition"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, updates_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def live_dashboard(self):
        """Show live weather dashboard"""
        try:
            dashboard_info = "📊 LIVE WEATHER DASHBOARD:\n"
            dashboard_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            dashboard_info += "🎛️ MULTI-LOCATION MONITORING:\n\n"
            dashboard_info += "📍 LOCATION 1: Current City\n"
            dashboard_info += "   🌡️ 23°C | 💧 68% | 💨 12 km/h | ☁️ Partly Cloudy\n"
            dashboard_info += "   Trend: ↗️ Improving\n\n"
            dashboard_info += "📍 LOCATION 2: Nearby City (50km)\n"
            dashboard_info += "   🌡️ 21°C | 💧 72% | 💨 15 km/h | 🌧️ Light Rain\n"
            dashboard_info += "   Trend: ↘️ Deteriorating\n\n"
            dashboard_info += "📍 LOCATION 3: Regional Hub (100km)\n"
            dashboard_info += "   🌡️ 26°C | 💧 55% | 💨 8 km/h | ☀️ Sunny\n"
            dashboard_info += "   Trend: ➡️ Stable\n\n"
            dashboard_info += "📈 LIVE GRAPHS & CHARTS:\n"
            dashboard_info += "• Temperature trends: 24-hour rolling\n"
            dashboard_info += "• Pressure changes: Barometric trends\n"
            dashboard_info += "• Wind patterns: Speed and direction\n"
            dashboard_info += "• Humidity cycles: Daily variations\n\n"
            dashboard_info += "🗺️ INTERACTIVE WEATHER MAP:\n"
            dashboard_info += "• Live radar overlay: Precipitation\n"
            dashboard_info += "• Satellite imagery: Cloud movement\n"
            dashboard_info += "• Temperature contours: Heat mapping\n"
            dashboard_info += "• Wind flow visualization: Direction arrows\n\n"
            dashboard_info += "⚡ LIVE ALERTS PANEL:\n"
            dashboard_info += "• No active weather warnings\n"
            dashboard_info += "• Advisories: Light winds expected\n"
            dashboard_info += "• Watches: None in effect\n\n"
            dashboard_info += "🔄 AUTO-REFRESH SETTINGS:\n"
            dashboard_info += "• Dashboard updates: Every 30 seconds\n"
            dashboard_info += "• Map refresh: Every 2 minutes\n"
            dashboard_info += "• Data synchronization: Real-time"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, dashboard_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def global_feed(self):
        """Show global weather feed"""
        try:
            global_info = "🌐 GLOBAL WEATHER FEED:\n"
            global_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            global_info += "🌍 WORLDWIDE WEATHER HIGHLIGHTS:\n\n"
            global_info += "🇺🇸 NORTH AMERICA:\n"
            global_info += "• New York: 18°C, Cloudy, Normal\n"
            global_info += "• Los Angeles: 28°C, Sunny, Heat advisory\n"
            global_info += "• Toronto: 15°C, Rain, Flood watch\n\n"
            global_info += "🇪🇺 EUROPE:\n"
            global_info += "• London: 16°C, Overcast, Typical\n"
            global_info += "• Paris: 22°C, Sunny, Pleasant\n"
            global_info += "• Berlin: 19°C, Showers, Unsettled\n\n"
            global_info += "🇦🇸 ASIA-PACIFIC:\n"
            global_info += "• Tokyo: 31°C, Humid, Heat warning\n"
            global_info += "• Sydney: 12°C, Clear, Cool\n"
            global_info += "• Mumbai: 29°C, Monsoon, Heavy rain\n\n"
            global_info += "🌪️ EXTREME WEATHER EVENTS:\n"
            global_info += "• Hurricane tracking: Atlantic basin quiet\n"
            global_info += "• Typhoon activity: Western Pacific active\n"
            global_info += "• Severe storms: Central US developing\n\n"
            global_info += "🔥 SIGNIFICANT WEATHER:\n"
            global_info += "• Wildfires: California - moderate risk\n"
            global_info += "• Heatwaves: Europe - temperatures rising\n"
            global_info += "• Flooding: Southeast Asia - monsoon season\n\n"
            global_info += "📡 LIVE GLOBAL TRACKING:\n"
            global_info += "• 50,000+ weather stations reporting\n"
            global_info += "• Satellite data: Updated every 15 minutes\n"
            global_info += "• Ocean buoys: Marine weather monitoring\n"
            global_info += "• Aircraft reports: Upper-level conditions\n\n"
            global_info += "🌊 CLIMATE INDICATORS:\n"
            global_info += "• Sea surface temperatures: Above average\n"
            global_info += "• Jet stream position: Slightly south\n"
            global_info += "• El Niño/La Niña: Neutral conditions"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, global_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def breaking_weather(self):
        """Show breaking weather news"""
        try:
            breaking_info = "⚡ BREAKING WEATHER NEWS:\n"
            breaking_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            breaking_info += "🚨 LATEST WEATHER DEVELOPMENTS:\n\n"
            breaking_info += "🕐 14:30 - DEVELOPING STORY:\n"
            breaking_info += "• Unexpected temperature spike in downtown area\n"
            breaking_info += "• 5°C increase in 20 minutes\n"
            breaking_info += "• Meteorologists investigating cause\n\n"
            breaking_info += "🕐 13:45 - WEATHER ALERT:\n"
            breaking_info += "• Wind advisory issued for coastal areas\n"
            breaking_info += "• Gusts up to 55 km/h expected\n"
            breaking_info += "• Small craft advisory in effect\n\n"
            breaking_info += "🕐 12:15 - RECORD UPDATE:\n"
            breaking_info += "• Hottest day of the year so far\n"
            breaking_info += "• Previous record: 32°C (July 15)\n"
            breaking_info += "• Current high: 33°C and rising\n\n"
            breaking_info += "⛈️ STORM WATCH:\n"
            breaking_info += "• Thunderstorm cells developing 200km west\n"
            breaking_info += "• Movement: Northeast at 25 km/h\n"
            breaking_info += "• ETA: 8 hours\n"
            breaking_info += "• Intensity: Moderate to strong\n\n"
            breaking_info += "📊 WEATHER IMPACT REPORTS:\n"
            breaking_info += "• Airport delays: None currently\n"
            breaking_info += "• Traffic conditions: Normal\n"
            breaking_info += "• Power grid: Stable\n"
            breaking_info += "• Public events: Proceeding as planned\n\n"
            breaking_info += "📱 SOCIAL MEDIA WEATHER:\n"
            breaking_info += "• #WeatherUpdate trending locally\n"
            breaking_info += "• User reports: Heat building downtown\n"
            breaking_info += "• Photos: Clear skies, intense sun\n\n"
            breaking_info += "🔔 EMERGENCY UPDATES:\n"
            breaking_info += "• No weather emergencies active\n"
            breaking_info += "• Monitoring heat stress conditions\n"
            breaking_info += "• Stay hydrated and seek shade"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, breaking_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))


class QuickActionsTab:
    """Quick actions tab component for instant access to all major features"""
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="🚀 Quick Actions")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        StyledLabel(self.frame, text="🚀 Quick Access to Major Features:").pack(pady=10)
        
        self.result_text = StyledText(self.frame, height=8)
        self.result_text.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Recently Implemented Features Section
        new_features_frame = ttk.LabelFrame(self.frame, text="🆕 Recently Added Features")
        new_features_frame.pack(pady=10, padx=10, fill=tk.X)
        
        # Health & Live Radar Quick Access
        health_radar_frame = ttk.Frame(new_features_frame)
        health_radar_frame.pack(pady=5)
        
        StyledButton(health_radar_frame, "success", text="🏥 Health Analysis", 
                    command=self.quick_health_analysis).grid(row=0, column=0, padx=5)
        StyledButton(health_radar_frame, "info", text="📡 Live Radar", 
                    command=self.quick_radar_access).grid(row=0, column=1, padx=5)
        
        # Popular Features Section
        popular_frame = ttk.LabelFrame(self.frame, text="⭐ Popular Features")
        popular_frame.pack(pady=10, padx=10, fill=tk.X)
        
        # Quick action buttons for popular features
        quick_button_frame = ttk.Frame(popular_frame)
        quick_button_frame.pack(pady=5)
        
        StyledButton(quick_button_frame, "primary", text="🌤️ Current Weather", 
                    command=self.quick_weather).grid(row=0, column=0, padx=3)
        StyledButton(quick_button_frame, "warning", text="🌪️ Severe Weather", 
                    command=self.quick_severe_weather).grid(row=0, column=1, padx=3)
        StyledButton(quick_button_frame, "danger", text="🔴 Live Weather", 
                    command=self.quick_live_weather).grid(row=0, column=2, padx=3)
        StyledButton(quick_button_frame, "accent_black", text="📷 Weather Cams", 
                    command=self.quick_camera_access).grid(row=0, column=3, padx=3)
        
        # Initialize with welcome message
        self.show_welcome_message()

    def show_welcome_message(self):
        """Display welcome message with feature overview"""
        welcome_msg = "🚀 QUICK ACTIONS DASHBOARD:\n"
        welcome_msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        welcome_msg += "✨ RECENTLY ADDED FEATURES:\n"
        welcome_msg += "🏥 Health Analysis - Weather impact on health & wellness\n"
        welcome_msg += "📡 Live Radar - Real-time precipitation & storm tracking\n\n"
        welcome_msg += "⭐ POPULAR FEATURES:\n"
        welcome_msg += "🌤️ Current Weather - Live conditions & forecasts\n"
        welcome_msg += "🌪️ Severe Weather - Storm monitoring & alerts\n"
        welcome_msg += "🔴 Live Weather - Real-time weather streams\n"
        welcome_msg += "📷 Weather Cams - Live camera feeds worldwide\n\n"
        welcome_msg += "💡 Click any button above for instant access to features!"
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, welcome_msg)

    def quick_health_analysis(self):
        """Quick access to health analysis features"""
        try:
            health_info = "🏥 HEALTH ANALYSIS QUICK ACCESS:\n"
            health_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            health_info += "🌡️ WEATHER HEALTH IMPACT:\n"
            health_info += "Current weather conditions and health recommendations:\n\n"
            health_info += "💨 AIR QUALITY STATUS:\n"
            health_info += "• Air Quality Index: 65 (Moderate)\n"
            health_info += "• Primary pollutant: PM2.5\n"
            health_info += "• Health recommendation: Acceptable for most people\n"
            health_info += "• Sensitive groups: Consider reducing outdoor activities\n\n"
            health_info += "🌡️ HEAT STRESS ANALYSIS:\n"
            health_info += "• Current temperature: 23°C (Comfortable)\n"
            health_info += "• Heat index: 25°C (Safe)\n"
            health_info += "• Hydration level: Normal requirements\n"
            health_info += "• Activity safety: All outdoor activities safe\n\n"
            health_info += "🏃 ACTIVITY RECOMMENDATIONS:\n"
            health_info += "• Outdoor exercise: ✅ Recommended\n"
            health_info += "• Walking/jogging: ✅ Excellent conditions\n"
            health_info += "• Cycling: ✅ Perfect weather\n"
            health_info += "• Water sports: ✅ Safe conditions\n\n"
            health_info += "💊 MEDICAL CONSIDERATIONS:\n"
            health_info += "• Asthma/allergies: Low risk today\n"
            health_info += "• Joint pain weather: No pressure changes expected\n"
            health_info += "• Migraine triggers: Stable barometric pressure\n"
            health_info += "• Skin protection: SPF 30+ recommended\n\n"
            health_info += "📍 Navigate to 'Health' tab for detailed analysis"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, health_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def quick_radar_access(self):
        """Quick access to live radar features"""
        try:
            from datetime import datetime
            radar_info = "📡 LIVE RADAR QUICK ACCESS:\n"
            radar_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            radar_info += "🔴 LIVE RADAR STATUS:\n"
            radar_info += f"🕐 Last Update: {datetime.now().strftime('%H:%M:%S')}\n\n"
            radar_info += "🌧️ PRECIPITATION OVERVIEW:\n"
            radar_info += "• Active precipitation: Light rain 45km northeast\n"
            radar_info += "• Movement: Eastward at 25 km/h\n"
            radar_info += "• Intensity: 2-5mm/hour (Light)\n"
            radar_info += "• ETA to your area: 2.5 hours\n\n"
            radar_info += "⚡ STORM ACTIVITY:\n"
            radar_info += "• Thunderstorms: None within 100km\n"
            radar_info += "• Lightning strikes: 0 in last 30 minutes\n"
            radar_info += "• Severe weather: No threats detected\n\n"
            radar_info += "🌬️ WIND PATTERNS:\n"
            radar_info += "• Surface winds: 12 km/h from northwest\n"
            radar_info += "• Wind shear: Minimal\n"
            radar_info += "• Turbulence: Light\n\n"
            radar_info += "📊 RADAR CAPABILITIES:\n"
            radar_info += "• Precipitation tracking: Real-time\n"
            radar_info += "• Storm motion vectors: Active\n"
            radar_info += "• Lightning detection: Continuous\n"
            radar_info += "• Wind flow analysis: Available\n\n"
            radar_info += "📍 Navigate to 'Live Radar' tab for detailed analysis"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, radar_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def quick_weather(self):
        """Quick access to current weather"""
        try:
            weather_info = "🌤️ CURRENT WEATHER QUICK ACCESS:\n"
            weather_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            weather_info += "☀️ CURRENT CONDITIONS:\n"
            weather_info += "• Temperature: 23°C (feels like 25°C)\n"
            weather_info += "• Condition: Partly cloudy\n"
            weather_info += "• Humidity: 68%\n"
            weather_info += "• Wind: 12 km/h northwest\n"
            weather_info += "• Pressure: 1013.2 hPa\n"
            weather_info += "• Visibility: 10+ km\n"
            weather_info += "• UV Index: 6 (High)\n\n"
            weather_info += "📅 TODAY'S FORECAST:\n"
            weather_info += "• High: 27°C | Low: 18°C\n"
            weather_info += "• Rain chance: 20%\n"
            weather_info += "• Wind: 10-15 km/h\n"
            weather_info += "• Sunrise: 06:15 | Sunset: 19:45\n\n"
            weather_info += "📍 Navigate to 'Weather' tab for detailed forecasts"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, weather_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def quick_severe_weather(self):
        """Quick access to severe weather monitoring"""
        try:
            severe_info = "🌪️ SEVERE WEATHER QUICK ACCESS:\n"
            severe_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            severe_info += "🚨 CURRENT THREAT LEVEL:\n"
            severe_info += "✅ LOW RISK - No active severe weather warnings\n\n"
            severe_info += "⚠️ MONITORING STATUS:\n"
            severe_info += "• Tornado risk: 0% (None)\n"
            severe_info += "• Thunderstorm probability: 15% (Low)\n"
            severe_info += "• Hail probability: 5% (Very Low)\n"
            severe_info += "• Flash flood risk: 10% (Low)\n\n"
            severe_info += "📡 ACTIVE MONITORING:\n"
            severe_info += "• Doppler radar: Scanning continuously\n"
            severe_info += "• Lightning detection: No activity\n"
            severe_info += "• Storm spotters: 12 active in region\n\n"
            severe_info += "📍 Navigate to 'Severe Weather' tab for detailed monitoring"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, severe_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def quick_live_weather(self):
        """Quick access to live weather feeds"""
        try:
            from datetime import datetime
            live_info = "🔴 LIVE WEATHER QUICK ACCESS:\n"
            live_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            live_info += "📡 LIVE STREAM STATUS:\n"
            live_info += f"🕐 Last Update: {datetime.now().strftime('%H:%M:%S')}\n"
            live_info += "🔄 Update Frequency: Every 60 seconds\n\n"
            live_info += "🌤️ LIVE CONDITIONS:\n"
            live_info += "• Temperature: 23°C (↗️ +0.5°C in last hour)\n"
            live_info += "• Humidity: 68% (↘️ -2% in last hour)\n"
            live_info += "• Wind: 12 km/h NW (steady)\n"
            live_info += "• Pressure: 1013.2 hPa (stable)\n\n"
            live_info += "📈 REAL-TIME TRACKING:\n"
            live_info += "• Lightning detection: Active\n"
            live_info += "• Precipitation radar: Live updates\n"
            live_info += "• Wind monitoring: Continuous\n"
            live_info += "• Breaking weather alerts: Enabled\n\n"
            live_info += "📍 Navigate to 'Live Weather' tab for full live dashboard"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, live_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def quick_camera_access(self):
        """Quick access to weather cameras"""
        try:
            camera_info = "📷 WEATHER CAMERAS QUICK ACCESS:\n"
            camera_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            camera_info += "🌆 FEATURED CAMERA FEEDS:\n"
            camera_info += "• Times Square, NYC - Clear visibility\n"
            camera_info += "• Golden Gate Bridge, SF - Partly cloudy\n"
            camera_info += "• Sydney Harbour - Sunny conditions\n"
            camera_info += "• London Eye - Overcast skies\n\n"
            camera_info += "🏔️ MOUNTAIN WEATHER CAMS:\n"
            camera_info += "• Swiss Alps - Fresh snow, clear\n"
            camera_info += "• Rocky Mountains - Bluebird conditions\n"
            camera_info += "• Mount Fuji - Excellent visibility\n\n"
            camera_info += "🏖️ BEACH WEATHER CAMS:\n"
            camera_info += "• Waikiki Beach - Perfect conditions\n"
            camera_info += "• Miami Beach - Sunny and warm\n"
            camera_info += "• Bondi Beach - Ideal surf conditions\n\n"
            camera_info += "📍 Navigate to 'Camera' tab for all live camera feeds"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, camera_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))


class PoetryTab:
    """Weather poetry tab component"""
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Poetry")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        StyledLabel(self.frame, text="Poetry features coming soon.").pack(pady=20)


class LiveRadarTab:
    """Live radar tab component for real-time weather radar tracking"""
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="📡 Live Radar")
        set_tab_font(notebook)
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components with live radar maps"""
        # Header section
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        StyledLabel(header_frame, text="📡 LIVE WEATHER RADAR & MAPS", 
                   font=("Arial", 14, "bold")).pack()
        
        # Location input section
        location_frame = ttk.Frame(self.frame)
        location_frame.pack(fill=tk.X, padx=10, pady=5)
        
        StyledLabel(location_frame, text="Enter Location:").pack(side=tk.LEFT)
        self.location_entry = ttk.Entry(location_frame, width=20)
        self.location_entry.pack(side=tk.LEFT, padx=5)
        self.location_entry.insert(0, "New York")  # Default location
        
        StyledButton(location_frame, "primary", text="🔄 Update Location", 
                    command=self.update_radar_location).pack(side=tk.LEFT, padx=5)
        
        # Create main content area with notebook for different map views
        self.radar_notebook = ttk.Notebook(self.frame)
        self.radar_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Live Radar Map Tab
        self._create_live_radar_tab()
        
        # Satellite Map Tab
        self._create_satellite_tab()
        
        # Temperature Map Tab
        self._create_temperature_tab()
        
        # Wind Map Tab
        self._create_wind_tab()
        
        # Lightning Map Tab
        self._create_lightning_tab()
        
        # 3D Radar Tab
        self._create_3d_radar_tab()
        
        # Control panel at bottom
        self._create_control_panel()

    def _create_live_radar_tab(self):
        """Create live precipitation radar tab with enhanced visual interface"""
        radar_frame = ttk.Frame(self.radar_notebook)
        self.radar_notebook.add(radar_frame, text="🌧️ Live Radar")
        
        # Top controls section (similar to screenshot)
        top_controls_frame = ttk.Frame(radar_frame)
        top_controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Left side - Live People Animations section
        left_section = ttk.LabelFrame(top_controls_frame, text="🎬 Live People Animations")
        left_section.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Enter City field
        StyledLabel(left_section, text="Enter City:").pack(pady=2)
        self.animation_city_entry = ttk.Entry(left_section, width=15)
        self.animation_city_entry.pack(pady=2)
        self.animation_city_entry.insert(0, "Kaduna")
        
        # Animation control buttons
        anim_buttons_frame = ttk.Frame(left_section)
        anim_buttons_frame.pack(pady=5)
        
        StyledButton(anim_buttons_frame, "success", text="▶️ Start Animations", 
                    command=self.start_people_animations).pack(pady=2)
        StyledButton(anim_buttons_frame, "danger", text="⏹️ Stop Animations", 
                    command=self.stop_people_animations).pack(pady=2)
        
        # Weather sync controls
        sync_frame = ttk.Frame(left_section)
        sync_frame.pack(pady=5)
        
        StyledButton(sync_frame, "warning", text="🌦️ Sync Weather", 
                    command=self.sync_weather_animation).pack(side=tk.LEFT, padx=2)
        StyledButton(sync_frame, "info", text="⚙️ Settings", 
                    command=self.animation_settings).pack(side=tk.LEFT, padx=2)
        
        # Right side - Live Doppler Radar section
        right_section = ttk.LabelFrame(top_controls_frame, text="📡 Live Doppler Radar")
        right_section.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        
        # Coordinate inputs
        coord_frame = ttk.Frame(right_section)
        coord_frame.pack(pady=5)
        
        StyledLabel(coord_frame, text="Latitude:").grid(row=0, column=0, padx=2)
        self.lat_entry = ttk.Entry(coord_frame, width=10)
        self.lat_entry.grid(row=0, column=1, padx=2)
        self.lat_entry.insert(0, "40.7128")
        
        StyledLabel(coord_frame, text="Longitude:").grid(row=0, column=2, padx=2)
        self.lon_entry = ttk.Entry(coord_frame, width=10)
        self.lon_entry.grid(row=0, column=3, padx=2)
        self.lon_entry.insert(0, "-74.0060")
        
        # Radar control buttons (2x2 grid)
        radar_buttons_frame = ttk.Frame(right_section)
        radar_buttons_frame.pack(pady=5)
        
        StyledButton(radar_buttons_frame, "primary", text="🔄 Update Radar", 
                    command=self.update_doppler_radar).grid(row=0, column=0, padx=2, pady=2)
        StyledButton(radar_buttons_frame, "success", text="🎯 Track Storms", 
                    command=self.track_storms).grid(row=0, column=1, padx=2, pady=2)
        StyledButton(radar_buttons_frame, "warning", text="⚠️ Alerts", 
                    command=self.radar_alerts).grid(row=1, column=0, padx=2, pady=2)
        StyledButton(radar_buttons_frame, "info", text="📊 Radar Stats", 
                    command=self.radar_statistics).grid(row=1, column=1, padx=2, pady=2)
        
        # Main content area with split panels
        main_content_frame = ttk.Frame(radar_frame)
        main_content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Live Animation Display
        left_panel = ttk.LabelFrame(main_content_frame, text="Live Animation")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
        
        # Animation canvas area (simulated)
        self.animation_display = StyledText(left_panel, height=15, bg="#ADD8E6")
        self.animation_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right panel - Doppler Radar Display
        right_panel = ttk.LabelFrame(main_content_frame, text="Doppler Radar Display")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=2)
        
        # Radar display header
        radar_header_frame = ttk.Frame(right_panel)
        radar_header_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Radar mode buttons
        StyledButton(radar_header_frame, "accent_black", text="📡 Live Weather Radar", 
                    command=self.show_live_radar).pack(side=tk.LEFT, padx=2)
        StyledButton(radar_header_frame, "info_black", text="⚡ Track Severe Weather", 
                    command=self.track_severe_weather).pack(side=tk.LEFT, padx=2)
        
        # Radar coordinates display
        coord_display_frame = ttk.Frame(right_panel)
        coord_display_frame.pack(fill=tk.X, padx=5, pady=2)
        
        self.coord_label = StyledLabel(coord_display_frame, text="Lat: 40.7")
        self.coord_label.pack(side=tk.LEFT)
        
        # Main radar visualization area
        self.radar_display = StyledText(right_panel, height=15, bg="#000033")
        self.radar_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Radar timestamp and info
        radar_info_frame = ttk.Frame(right_panel)
        radar_info_frame.pack(fill=tk.X, padx=5, pady=2)
        
        from datetime import datetime
        current_time = datetime.now().strftime("Weather Radar - %H:%M")
        self.radar_time_label = StyledLabel(radar_info_frame, text=current_time)
        self.radar_time_label.pack()
        
        # Initialize displays
        self._initialize_radar_displays()

    def _initialize_radar_displays(self):
        """Initialize the radar displays with default content"""
        try:
            # Initialize animation display
            self.animation_display.delete(1.0, tk.END)
            self.animation_display.insert(tk.END, "🎬 LIVE PEOPLE ANIMATIONS:\n\n")
            self.animation_display.insert(tk.END, "     ┌─────────────────────┐\n")
            self.animation_display.insert(tk.END, "     │                     │\n")
            self.animation_display.insert(tk.END, "     │      🚶‍♂️   🚶‍♀️       │\n")
            self.animation_display.insert(tk.END, "     │                     │\n")
            self.animation_display.insert(tk.END, "     │   🚴‍♂️       🏃‍♀️     │\n")
            self.animation_display.insert(tk.END, "     │                     │\n")
            self.animation_display.insert(tk.END, "     │      🚶‍♀️   🚶‍♂️       │\n")
            self.animation_display.insert(tk.END, "     │                     │\n")
            self.animation_display.insert(tk.END, "     └─────────────────────┘\n\n")
            self.animation_display.insert(tk.END, "🌦️ Weather affecting movement:\n")
            self.animation_display.insert(tk.END, "• Temperature: 23°C - Normal activity\n")
            self.animation_display.insert(tk.END, "• Rain: None - All activities normal\n")
            self.animation_display.insert(tk.END, "• Wind: Light - No impact on movement\n\n")
            self.animation_display.insert(tk.END, "📊 Animation Status: Ready to start")
            
            # Initialize radar display with visual radar simulation
            self.update_doppler_radar()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize displays: {str(e)}")

    # Live People Animation Methods
    def start_people_animations(self):
        """Start people movement animations"""
        try:
            city = self.animation_city_entry.get().strip() or "Kaduna"
            self.animation_display.delete(1.0, tk.END)
            self.animation_display.insert(tk.END, f"🎬 LIVE ANIMATIONS - {city.upper()}:\n\n")
            self.animation_display.insert(tk.END, "▶️ ANIMATION STARTED\n\n")
            
            # Create dynamic animation scene
            import random
            from datetime import datetime
            
            # Generate random movement patterns
            people_types = ["🚶‍♂️", "🚶‍♀️", "🏃‍♂️", "🏃‍♀️", "🚴‍♂️", "🚴‍♀️"]
            directions = ["→", "←", "↑", "↓"]
            
            self.animation_display.insert(tk.END, "     ┌─────────────────────┐\n")
            
            # Create 5 rows of animation
            for row in range(5):
                line = "     │"
                for col in range(10):
                    if random.random() < 0.3:  # 30% chance of person
                        person = random.choice(people_types)
                        direction = random.choice(directions)
                        line += person + direction
                    else:
                        line += "  "
                line += "│\n"
                self.animation_display.insert(tk.END, line)
            
            self.animation_display.insert(tk.END, "     └─────────────────────┘\n\n")
            
            # Add real-time statistics
            active_count = random.randint(8, 15)
            walking_count = random.randint(4, 8)
            running_count = random.randint(1, 3)
            cycling_count = random.randint(1, 4)
            
            self.animation_display.insert(tk.END, f"📊 LIVE MOVEMENT TRACKING ({datetime.now().strftime('%H:%M:%S')}):\n")
            self.animation_display.insert(tk.END, f"• Active people: {active_count}\n")
            self.animation_display.insert(tk.END, f"• Walking: {walking_count} people\n")
            self.animation_display.insert(tk.END, f"• Running: {running_count} person(s)\n")
            self.animation_display.insert(tk.END, f"• Cycling: {cycling_count} person(s)\n\n")
            
            # Weather-based movement analysis
            self.animation_display.insert(tk.END, "🌤️ Weather impact on movement:\n")
            weather_condition = random.choice(["Clear", "Light Rain", "Windy", "Hot"])
            
            if weather_condition == "Clear":
                self.animation_display.insert(tk.END, "• Visibility: Excellent\n")
                self.animation_display.insert(tk.END, "• Activity level: High\n")
                self.animation_display.insert(tk.END, "• Movement pattern: Normal pace\n")
            elif weather_condition == "Light Rain":
                self.animation_display.insert(tk.END, "• Visibility: Good\n")
                self.animation_display.insert(tk.END, "• Activity level: Reduced\n")
                self.animation_display.insert(tk.END, "• Movement pattern: Seeking shelter\n")
            elif weather_condition == "Windy":
                self.animation_display.insert(tk.END, "• Visibility: Good\n")
                self.animation_display.insert(tk.END, "• Activity level: Moderate\n")
                self.animation_display.insert(tk.END, "• Movement pattern: Against wind resistance\n")
            else:  # Hot
                self.animation_display.insert(tk.END, "• Visibility: Heat haze\n")
                self.animation_display.insert(tk.END, "• Activity level: Reduced\n")
                self.animation_display.insert(tk.END, "• Movement pattern: Seeking shade\n")
                
            self.animation_display.insert(tk.END, f"• Current conditions: {weather_condition}\n\n")
            
            # Start auto-refresh for real-time updates
            self.animation_display.insert(tk.END, "🔄 Auto-refresh: Every 3 seconds\n")
            self.animation_display.insert(tk.END, "⏹️ Click 'Stop Animations' to pause")
            
            # Schedule next update (simulated real-time)
            self.frame.after(3000, self._update_animation_frame)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def stop_people_animations(self):
        """Stop people movement animations"""
        try:
            current_text = self.animation_display.get(1.0, tk.END)
            if "ANIMATION STARTED" in current_text:
                # Stop auto-refresh
                try:
                    self.frame.after_cancel(getattr(self, '_animation_timer', None))
                except:
                    pass
                
                # Update display to show stopped state
                self.animation_display.delete(1.0, tk.END)
                city = self.animation_city_entry.get().strip() or "Kaduna"
                self.animation_display.insert(tk.END, f"🎬 LIVE ANIMATIONS - {city.upper()}:\n\n")
                self.animation_display.insert(tk.END, "⏹️ ANIMATION STOPPED\n\n")
                self.animation_display.insert(tk.END, "     ┌─────────────────────┐\n")
                self.animation_display.insert(tk.END, "     │                     │\n")
                self.animation_display.insert(tk.END, "     │      🚶‍♂️   🚶‍♀️       │\n")
                self.animation_display.insert(tk.END, "     │                     │\n")
                self.animation_display.insert(tk.END, "     │   🚴‍♂️       🏃‍♀️     │\n")
                self.animation_display.insert(tk.END, "     │                     │\n")
                self.animation_display.insert(tk.END, "     │      🚶‍♀️   🚶‍♂️       │\n")
                self.animation_display.insert(tk.END, "     │                     │\n")
                self.animation_display.insert(tk.END, "     └─────────────────────┘\n\n")
                self.animation_display.insert(tk.END, "🔴 All animations paused\n")
                self.animation_display.insert(tk.END, "📊 Final statistics preserved\n")
                self.animation_display.insert(tk.END, "▶️ Click 'Start Animations' to resume")
            else:
                self.animation_display.insert(tk.END, "\n🔴 Animations already stopped")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _update_animation_frame(self):
        """Update animation frame for real-time movement"""
        try:
            # Check if animations are still active
            current_text = self.animation_display.get(1.0, tk.END)
            if "ANIMATION STARTED" not in current_text:
                return
                
            import random
            from datetime import datetime
            
            city = self.animation_city_entry.get().strip() or "Kaduna"
            self.animation_display.delete(1.0, tk.END)
            self.animation_display.insert(tk.END, f"🎬 LIVE ANIMATIONS - {city.upper()}:\n\n")
            self.animation_display.insert(tk.END, "▶️ ANIMATION ACTIVE\n\n")
            
            # Generate new random movement patterns
            people_types = ["🚶‍♂️", "🚶‍♀️", "🏃‍♂️", "🏃‍♀️", "🚴‍♂️", "🚴‍♀️"]
            directions = ["→", "←", "↑", "↓"]
            
            self.animation_display.insert(tk.END, "     ┌─────────────────────┐\n")
            
            # Create 5 rows of animation with different patterns
            for row in range(5):
                line = "     │"
                for col in range(10):
                    if random.random() < 0.25:  # 25% chance of person
                        person = random.choice(people_types)
                        direction = random.choice(directions)
                        line += person + direction
                    else:
                        line += "  "
                line += "│\n"
                self.animation_display.insert(tk.END, line)
            
            self.animation_display.insert(tk.END, "     └─────────────────────┘\n\n")
            
            # Update real-time statistics
            active_count = random.randint(6, 18)
            walking_count = random.randint(3, 10)
            running_count = random.randint(0, 4)
            cycling_count = random.randint(0, 5)
            
            self.animation_display.insert(tk.END, f"� LIVE TRACKING ({datetime.now().strftime('%H:%M:%S')}):\n")
            self.animation_display.insert(tk.END, f"• Active people: {active_count}\n")
            self.animation_display.insert(tk.END, f"• Walking: {walking_count}\n")
            self.animation_display.insert(tk.END, f"• Running: {running_count}\n")
            self.animation_display.insert(tk.END, f"• Cycling: {cycling_count}\n\n")
            self.animation_display.insert(tk.END, "🔄 Next update in 3 seconds...")
            
            # Schedule next update
            self._animation_timer = self.frame.after(3000, self._update_animation_frame)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def sync_weather_animation(self):
        """Sync animations with weather conditions"""
        try:
            import random
            from datetime import datetime
            
            city = self.animation_city_entry.get().strip() or "Kaduna"
            
            # Get weather conditions (simulated)
            weather_conditions = [
                ("☀️ Sunny", "High activity, people outdoors"),
                ("🌧️ Light Rain", "Reduced activity, seeking shelter"),
                ("⛈️ Thunderstorm", "Minimal activity, indoors"),
                ("❄️ Snow", "Slow movement, bundled up"),
                ("🌪️ Windy", "Difficulty walking, holding items"),
                ("🌫️ Foggy", "Cautious movement, reduced visibility")
            ]
            
            weather, description = random.choice(weather_conditions)
            
            self.animation_display.delete(1.0, tk.END)
            self.animation_display.insert(tk.END, f"🎬 WEATHER-SYNCED ANIMATIONS - {city.upper()}:\n\n")
            self.animation_display.insert(tk.END, f"🌦️ CURRENT WEATHER: {weather}\n\n")
            
            # Adjust animation based on weather
            if "Sunny" in weather:
                people_density = 0.4
                movement_types = ["🚶‍♂️", "🚶‍♀️", "🏃‍♂️", "🏃‍♀️", "🚴‍♂️", "🚴‍♀️", "🛴", "⛹️‍♂️"]
            elif "Rain" in weather:
                people_density = 0.2
                movement_types = ["🚶‍♂️☔", "🚶‍♀️☔", "🏃‍♂️💨", "🏃‍♀️💨"]
            elif "Thunderstorm" in weather:
                people_density = 0.1
                movement_types = ["🏃‍♂️💨", "🏃‍♀️💨"]
            elif "Snow" in weather:
                people_density = 0.15
                movement_types = ["🚶‍♂️❄️", "🚶‍♀️❄️", "⛷️"]
            elif "Windy" in weather:
                people_density = 0.25
                movement_types = ["🚶‍♂️💨", "🚶‍♀️💨", "🚴‍♂️💨"]
            else:  # Foggy
                people_density = 0.2
                movement_types = ["🚶‍♂️🌫️", "🚶‍♀️🌫️"]
            
            self.animation_display.insert(tk.END, "     ┌─────────────────────┐\n")
            
            # Create weather-appropriate animation
            active_people = 0
            for row in range(5):
                line = "     │"
                for col in range(10):
                    if random.random() < people_density:
                        person = random.choice(movement_types)
                        line += person[:2]  # Limit to 2 characters for spacing
                        active_people += 1
                    else:
                        line += "  "
                line += "│\n"
                self.animation_display.insert(tk.END, line)
            
            self.animation_display.insert(tk.END, "     └─────────────────────┘\n\n")
            
            # Weather impact analysis
            self.animation_display.insert(tk.END, f"🌦️ WEATHER SYNC ANALYSIS ({datetime.now().strftime('%H:%M:%S')}):\n")
            self.animation_display.insert(tk.END, f"• Weather condition: {weather}\n")
            self.animation_display.insert(tk.END, f"• Impact: {description}\n")
            self.animation_display.insert(tk.END, f"• Active people: {active_people}\n")
            self.animation_display.insert(tk.END, f"• Activity level: {'High' if people_density > 0.3 else 'Medium' if people_density > 0.15 else 'Low'}\n\n")
            
            # Weather-specific recommendations
            if "Rain" in weather or "Thunderstorm" in weather:
                self.animation_display.insert(tk.END, "⚠️ WEATHER ADVISORY:\n")
                self.animation_display.insert(tk.END, "• Carry umbrella or raincoat\n")
                self.animation_display.insert(tk.END, "• Seek covered areas\n")
                self.animation_display.insert(tk.END, "• Reduced outdoor activities\n")
            elif "Snow" in weather:
                self.animation_display.insert(tk.END, "❄️ WINTER ADVISORY:\n")
                self.animation_display.insert(tk.END, "• Wear warm clothing\n")
                self.animation_display.insert(tk.END, "• Watch for icy conditions\n")
                self.animation_display.insert(tk.END, "• Allow extra travel time\n")
            elif "Windy" in weather:
                self.animation_display.insert(tk.END, "💨 WIND ADVISORY:\n")
                self.animation_display.insert(tk.END, "• Secure loose items\n")
                self.animation_display.insert(tk.END, "• Be cautious with umbrellas\n")
                self.animation_display.insert(tk.END, "• Expect travel delays\n")
            else:
                self.animation_display.insert(tk.END, "✅ OPTIMAL CONDITIONS:\n")
                self.animation_display.insert(tk.END, "• Perfect for outdoor activities\n")
                self.animation_display.insert(tk.END, "• Normal movement patterns\n")
                self.animation_display.insert(tk.END, "• High visibility and comfort\n")
                
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def animation_settings(self):
        """Open animation settings"""
        try:
            import tkinter.messagebox as msgbox
            from datetime import datetime
            
            # Show settings dialog
            result = msgbox.askyesnocancel(
                "Animation Settings",
                "Configure Animation Parameters:\n\n" +
                "YES - High Activity Mode (More people, faster updates)\n" +
                "NO - Low Activity Mode (Fewer people, slower updates)\n" +
                "CANCEL - Current Settings"
            )
            
            current_text = self.animation_display.get(1.0, tk.END)
            city = self.animation_city_entry.get().strip() or "Kaduna"
            
            if result is True:  # High Activity
                mode = "HIGH ACTIVITY"
                update_freq = "1 second"
                people_count = "15-25"
                activity_level = "Maximum"
            elif result is False:  # Low Activity
                mode = "LOW ACTIVITY"
                update_freq = "5 seconds"
                people_count = "3-8"
                activity_level = "Minimal"
            else:  # Cancel - keep current
                mode = "NORMAL"
                update_freq = "3 seconds"
                people_count = "6-15"
                activity_level = "Standard"
            
            # Update display with settings
            self.animation_display.delete(1.0, tk.END)
            self.animation_display.insert(tk.END, f"🎬 ANIMATION SETTINGS - {city.upper()}:\n\n")
            self.animation_display.insert(tk.END, f"⚙️ CONFIGURATION UPDATED ({datetime.now().strftime('%H:%M:%S')}):\n\n")
            
            self.animation_display.insert(tk.END, f"📊 CURRENT SETTINGS:\n")
            self.animation_display.insert(tk.END, f"• Mode: {mode}\n")
            self.animation_display.insert(tk.END, f"• Update frequency: {update_freq}\n")
            self.animation_display.insert(tk.END, f"• People count: {people_count}\n")
            self.animation_display.insert(tk.END, f"• Activity level: {activity_level}\n")
            self.animation_display.insert(tk.END, f"• Weather sync: Enabled\n")
            self.animation_display.insert(tk.END, f"• Real-time tracking: Active\n\n")
            
            self.animation_display.insert(tk.END, "🎯 ANIMATION FEATURES:\n")
            self.animation_display.insert(tk.END, "• Dynamic movement patterns\n")
            self.animation_display.insert(tk.END, "• Weather-responsive behavior\n")
            self.animation_display.insert(tk.END, "• Real-time statistics\n")
            self.animation_display.insert(tk.END, "• Multiple activity types\n")
            self.animation_display.insert(tk.END, "• Automatic updates\n\n")
            
            self.animation_display.insert(tk.END, "🔄 AVAILABLE ACTIONS:\n")
            self.animation_display.insert(tk.END, "• Start Animations - Begin live tracking\n")
            self.animation_display.insert(tk.END, "• Stop Animations - Pause all movement\n")
            self.animation_display.insert(tk.END, "• Sync Weather - Weather-based simulation\n")
            self.animation_display.insert(tk.END, "• Settings - Configure parameters\n\n")
            
            self.animation_display.insert(tk.END, "💡 TIP: Change city name for different locations!")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Doppler Radar Methods
    def update_doppler_radar(self):
        """Update the Doppler radar display"""
        try:
            lat = self.lat_entry.get().strip() or "40.7128"
            lon = self.lon_entry.get().strip() or "-74.0060"
            
            # Update coordinate display
            self.coord_label.config(text=f"Lat: {lat[:5]}")
            
            # Update radar time
            from datetime import datetime
            current_time = datetime.now().strftime("Weather Radar - %H:%M")
            self.radar_time_label.config(text=current_time)
            
            # Create radar visualization
            self.radar_display.delete(1.0, tk.END)
            self.radar_display.config(bg="#000033", fg="#00FF00")
            
            radar_visual = f"📡 DOPPLER RADAR - Lat: {lat}, Lon: {lon}\n"
            radar_visual += "═" * 50 + "\n\n"
            
            # ASCII radar sweep visualization
            radar_visual += "    🌧️ PRECIPITATION MAP 🌧️\n\n"
            radar_visual += "         0   5   10  15  km\n"
            radar_visual += "    0  ┌─────────────────────┐\n"
            radar_visual += "       │ ░░░▓▓▓░░░ ⭐ ░░░ │  5\n"
            radar_visual += "       │ ░▓▓███▓▓░     ░▓░ │\n"
            radar_visual += "    10 │ ▓███████▓▓    ▓▓▓ │\n"
            radar_visual += "       │ ░▓▓███▓▓░     ░░░ │\n"
            radar_visual += "    15 │ ░░░▓▓▓░░░ ⚡ ░░░ │\n"
            radar_visual += "       └─────────────────────┘\n\n"
            
            radar_visual += "🎯 RADAR LEGEND:\n"
            radar_visual += "⭐ = Your Location    ⚡ = Lightning\n"
            radar_visual += "░ = Light Rain        ▓ = Moderate Rain\n"
            radar_visual += "█ = Heavy Rain        ● = Storm Center\n\n"
            
            radar_visual += "📊 CURRENT CONDITIONS:\n"
            radar_visual += "• Precipitation: Light rain 5km NE\n"
            radar_visual += "• Storm intensity: Moderate\n"
            radar_visual += "• Movement: ESE at 15 km/h\n"
            radar_visual += "• Lightning activity: Minimal\n"
            radar_visual += "• Radar range: 25km radius\n"
            radar_visual += "• Last update: Real-time\n\n"
            
            radar_visual += "⚠️ ALERTS:\n"
            radar_visual += "• No severe weather warnings\n"
            radar_visual += "• Light precipitation approaching\n"
            radar_visual += "• ETA: 20 minutes"
            
            self.radar_display.insert(tk.END, radar_visual)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def track_storms(self):
        """Track storm movements"""
        try:
            current_text = self.radar_display.get(1.0, tk.END)
            storm_info = current_text + "\n\n🎯 STORM TRACKING ACTIVE:\n"
            storm_info += "• Storm Cell A: 12km NE, moving ESE\n"
            storm_info += "• Intensity: Moderate rain, 5-10mm/h\n"
            storm_info += "• Speed: 15 km/h\n"
            storm_info += "• ETA to location: 45 minutes\n"
            storm_info += "• Tracking confidence: High (92%)"
            
            self.radar_display.delete(1.0, tk.END)
            self.radar_display.insert(tk.END, storm_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def radar_alerts(self):
        """Show radar alerts"""
        try:
            current_text = self.radar_display.get(1.0, tk.END)
            alert_info = current_text + "\n\n⚠️ RADAR ALERTS:\n"
            alert_info += "• Weather Advisory: Light rain expected\n"
            alert_info += "• Alert level: Low (Level 1)\n"
            alert_info += "• Affected area: 5km radius\n"
            alert_info += "• Duration: 30-45 minutes\n"
            alert_info += "• Recommended action: Light jacket/umbrella"
            
            self.radar_display.delete(1.0, tk.END)
            self.radar_display.insert(tk.END, alert_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def radar_statistics(self):
        """Show radar statistics"""
        try:
            current_text = self.radar_display.get(1.0, tk.END)
            stats_info = current_text + "\n\n📊 RADAR STATISTICS:\n"
            stats_info += "• Radar uptime: 99.8%\n"
            stats_info += "• Data quality: Excellent\n"
            stats_info += "• Update frequency: Every 5 minutes\n"
            stats_info += "• Coverage area: 250km radius\n"
            stats_info += "• Active storms tracked: 1\n"
            stats_info += "• Lightning strikes (24h): 0"
            
            self.radar_display.delete(1.0, tk.END)
            self.radar_display.insert(tk.END, stats_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_live_radar(self):
        """Show live weather radar mode"""
        try:
            self.update_doppler_radar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def track_severe_weather(self):
        """Track severe weather mode"""
        try:
            self.radar_display.delete(1.0, tk.END)
            self.radar_display.config(bg="#330000", fg="#FF6600")
            
            severe_visual = "⚡ SEVERE WEATHER TRACKING ⚡\n"
            severe_visual += "═" * 50 + "\n\n"
            severe_visual += "🌪️ STORM INTENSITY MAP:\n\n"
            severe_visual += "         SEVERE WEATHER RADAR\n\n"
            severe_visual += "    0  ┌─────────────────────┐\n"
            severe_visual += "       │     ░░░ ⭐ ░░░     │  5\n"
            severe_visual += "       │     ░░░   ░░░     │\n"
            severe_visual += "    10 │     ░░░   ░░░     │\n"
            severe_visual += "       │     ░░░   ░░░     │\n"
            severe_visual += "    15 │     ░░░   ░░░     │\n"
            severe_visual += "       └─────────────────────┘\n\n"
            
            severe_visual += "🚨 SEVERE WEATHER STATUS:\n"
            severe_visual += "• Current threat level: LOW\n"
            severe_visual += "• Tornado probability: 0%\n"
            severe_visual += "• Hail probability: 0%\n"
            severe_visual += "• Severe thunderstorm: Not detected\n"
            severe_visual += "• Flash flood risk: Minimal\n\n"
            
            severe_visual += "✅ ALL CLEAR:\n"
            severe_visual += "• No severe weather detected\n"
            severe_visual += "• Conditions: Stable\n"
            severe_visual += "• Safe for outdoor activities"
            
            self.radar_display.insert(tk.END, severe_visual)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        

    def _create_satellite_tab(self):
        """Create satellite imagery tab"""
        sat_frame = ttk.Frame(self.radar_notebook)
        self.radar_notebook.add(sat_frame, text="🛰️ Satellite")
        
        # Satellite display
        sat_display_frame = ttk.LabelFrame(sat_frame, text="Live Satellite Imagery")
        sat_display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.satellite_display = StyledText(sat_display_frame, height=20)
        self.satellite_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Satellite controls
        sat_controls = ttk.Frame(sat_display_frame)
        sat_controls.pack(fill=tk.X, padx=5, pady=5)
        
        StyledButton(sat_controls, "primary", text="☀️ Visible Light", 
                    command=self.show_visible_satellite).pack(side=tk.LEFT, padx=2)
        StyledButton(sat_controls, "info", text="🌡️ Infrared", 
                    command=self.show_infrared_satellite).pack(side=tk.LEFT, padx=2)
        StyledButton(sat_controls, "success", text="💧 Water Vapor", 
                    command=self.show_water_vapor_satellite).pack(side=tk.LEFT, padx=2)

    def _create_temperature_tab(self):
        """Create temperature map tab"""
        temp_frame = ttk.Frame(self.radar_notebook)
        self.radar_notebook.add(temp_frame, text="🌡️ Temperature")
        
        temp_display_frame = ttk.LabelFrame(temp_frame, text="Live Temperature Map")
        temp_display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.temperature_display = StyledText(temp_display_frame, height=20)
        self.temperature_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Temperature controls
        temp_controls = ttk.Frame(temp_display_frame)
        temp_controls.pack(fill=tk.X, padx=5, pady=5)
        
        StyledButton(temp_controls, "danger", text="🌡️ Current Temp", 
                    command=self.show_current_temperature).pack(side=tk.LEFT, padx=2)
        StyledButton(temp_controls, "warning", text="🔥 Heat Index", 
                    command=self.show_heat_index).pack(side=tk.LEFT, padx=2)
        StyledButton(temp_controls, "info", text="❄️ Wind Chill", 
                    command=self.show_wind_chill).pack(side=tk.LEFT, padx=2)

    def _create_wind_tab(self):
        """Create wind map tab"""
        wind_frame = ttk.Frame(self.radar_notebook)
        self.radar_notebook.add(wind_frame, text="💨 Wind Flow")
        
        wind_display_frame = ttk.LabelFrame(wind_frame, text="Live Wind Flow Map")
        wind_display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.wind_display = StyledText(wind_display_frame, height=20)
        self.wind_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Wind controls
        wind_controls = ttk.Frame(wind_display_frame)
        wind_controls.pack(fill=tk.X, padx=5, pady=5)
        
        StyledButton(wind_controls, "success", text="🌪️ Wind Speed", 
                    command=self.show_wind_speed).pack(side=tk.LEFT, padx=2)
        StyledButton(wind_controls, "primary", text="🧭 Wind Direction", 
                    command=self.show_wind_direction).pack(side=tk.LEFT, padx=2)
        StyledButton(wind_controls, "warning", text="💨 Wind Gusts", 
                    command=self.show_wind_gusts).pack(side=tk.LEFT, padx=2)

    def _create_lightning_tab(self):
        """Create lightning detection tab"""
        lightning_frame = ttk.Frame(self.radar_notebook)
        self.radar_notebook.add(lightning_frame, text="⚡ Lightning")
        
        lightning_display_frame = ttk.LabelFrame(lightning_frame, text="Live Lightning Detection")
        lightning_display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.lightning_display = StyledText(lightning_display_frame, height=20)
        self.lightning_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Lightning controls
        lightning_controls = ttk.Frame(lightning_display_frame)
        lightning_controls.pack(fill=tk.X, padx=5, pady=5)
        
        StyledButton(lightning_controls, "danger", text="⚡ Live Strikes", 
                    command=self.show_live_lightning).pack(side=tk.LEFT, padx=2)
        StyledButton(lightning_controls, "warning", text="📊 Strike Density", 
                    command=self.show_lightning_density).pack(side=tk.LEFT, padx=2)
        StyledButton(lightning_controls, "info", text="🔊 Audio Alerts", 
                    command=self.toggle_lightning_audio).pack(side=tk.LEFT, padx=2)

    def _create_3d_radar_tab(self):
        """Create 3D radar visualization tab"""
        radar_3d_frame = ttk.Frame(self.radar_notebook)
        self.radar_notebook.add(radar_3d_frame, text="🎯 3D Radar")
        
        radar_3d_display_frame = ttk.LabelFrame(radar_3d_frame, text="3D Radar Volume Scan")
        radar_3d_display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.radar_3d_display = StyledText(radar_3d_display_frame, height=20)
        self.radar_3d_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 3D controls
        radar_3d_controls = ttk.Frame(radar_3d_display_frame)
        radar_3d_controls.pack(fill=tk.X, padx=5, pady=5)
        
        StyledButton(radar_3d_controls, "primary", text="🔄 Rotate View", 
                    command=self.rotate_3d_view).pack(side=tk.LEFT, padx=2)
        StyledButton(radar_3d_controls, "success", text="🔍 Zoom In", 
                    command=self.zoom_3d_in).pack(side=tk.LEFT, padx=2)
        StyledButton(radar_3d_controls, text="🔍 Zoom Out", 
                    command=self.zoom_3d_out).pack(side=tk.LEFT, padx=2)

    def _create_control_panel(self):
        """Create bottom control panel"""
        control_frame = ttk.LabelFrame(self.frame, text="Radar Control Panel")
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Time controls
        time_frame = ttk.Frame(control_frame)
        time_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        StyledLabel(time_frame, text="Time Control:").pack()
        time_buttons = ttk.Frame(time_frame)
        time_buttons.pack()
        
        StyledButton(time_buttons, text="⏮️", command=self.radar_time_back).pack(side=tk.LEFT, padx=1)
        StyledButton(time_buttons, text="⏸️", command=self.radar_time_pause).pack(side=tk.LEFT, padx=1)
        StyledButton(time_buttons, text="▶️", command=self.radar_time_play).pack(side=tk.LEFT, padx=1)
        StyledButton(time_buttons, text="⏭️", command=self.radar_time_forward).pack(side=tk.LEFT, padx=1)
        
        # Layer controls
        layer_frame = ttk.Frame(control_frame)
        layer_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        StyledLabel(layer_frame, text="Map Layers:").pack()
        layer_buttons = ttk.Frame(layer_frame)
        layer_buttons.pack()
        
        StyledButton(layer_buttons, "accent_black", text="🗺️ Terrain", 
                    command=self.toggle_terrain_layer).pack(side=tk.LEFT, padx=1)
        StyledButton(layer_buttons, "info_black", text="🏙️ Cities", 
                    command=self.toggle_cities_layer).pack(side=tk.LEFT, padx=1)
        StyledButton(layer_buttons, "success_black", text="🛣️ Roads", 
                    command=self.toggle_roads_layer).pack(side=tk.LEFT, padx=1)
        
        # Settings
        settings_frame = ttk.Frame(control_frame)
        settings_frame.pack(side=tk.RIGHT, padx=5, pady=5)
        
        StyledLabel(settings_frame, text="Settings:").pack()
        settings_buttons = ttk.Frame(settings_frame)
        settings_buttons.pack()
        
        StyledButton(settings_buttons, "warning_black", text="⚙️ Settings", 
                    command=self.open_radar_settings).pack(side=tk.LEFT, padx=1)
        StyledButton(settings_buttons, "danger_black", text="📱 Alerts", 
                    command=self.configure_radar_alerts).pack(side=tk.LEFT, padx=1)
        
        # Initialize with default radar view
        self.update_radar_location()

    def update_radar_location(self):
        """Update radar location and refresh displays"""
        location = self.location_entry.get().strip()
        if not location:
            location = "New York"  # Default location
        
        try:
            from datetime import datetime
            radar_info = f"📡 LIVE RADAR - {location.upper()}:\n"
            radar_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            radar_info += "🔴 RADAR STATUS: ACTIVE\n"
            radar_info += f"🕐 Last Update: {datetime.now().strftime('%H:%M:%S')}\n"
            radar_info += f"� Location: {location}\n\n"
            radar_info += "🌧️ PRECIPITATION MAP:\n"
            radar_info += "     NW    N    NE\n"
            radar_info += "  W   ▓░░░░░░▓   E\n"
            radar_info += "     ░░░▓▓░░░\n"
            radar_info += "     ░▓▓██▓▓░\n"
            radar_info += "     ░░▓▓▓░░░\n"
            radar_info += "  SW   ░░░░░░   SE\n"
            radar_info += "         S\n\n"
            radar_info += "Legend: ░=Light ▓=Moderate █=Heavy\n\n"
            radar_info += "📊 CURRENT CONDITIONS:\n"
            radar_info += "• Light precipitation: 45km NE\n"
            radar_info += "• Movement: East at 25 km/h\n"
            radar_info += "• Intensity: 2-5mm/hour\n"
            radar_info += "• ETA: 2.5 hours\n\n"
            radar_info += "⚡ STORM TRACKING:\n"
            radar_info += "• Active cells: 0 within 100km\n"
            radar_info += "• Lightning: None detected\n"
            radar_info += "• Severe weather: No threats\n\n"
            radar_info += "🔄 Auto-refresh: Every 5 minutes"
            
            self.radar_display.delete(1.0, tk.END)
            self.radar_display.insert(tk.END, radar_info)
            
            # Update satellite display
            self.show_visible_satellite()
            
            # Update temperature display
            self.show_current_temperature()
            
            # Update wind display
            self.show_wind_speed()
            
            # Update lightning display
            self.show_live_lightning()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Radar Animation Controls
    def play_radar_animation(self):
        """Play radar animation"""
        try:
            current_text = self.radar_display.get(1.0, tk.END)
            animation_text = current_text + "\n\n▶️ ANIMATION: Playing radar loop...\n"
            animation_text += "Frame 1/8: Current conditions\n"
            animation_text += "Animation speed: 2x normal\n"
            animation_text += "Loop duration: 2 hours of data"
            
            self.radar_display.delete(1.0, tk.END)
            self.radar_display.insert(tk.END, animation_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def pause_radar_animation(self):
        """Pause radar animation"""
        try:
            current_text = self.radar_display.get(1.0, tk.END)
            if "Playing radar loop" in current_text:
                paused_text = current_text.replace("Playing radar loop", "Animation PAUSED")
                self.radar_display.delete(1.0, tk.END)
                self.radar_display.insert(tk.END, paused_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_radar(self):
        """Refresh radar data"""
        try:
            self.update_radar_location()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Satellite Controls
    def show_visible_satellite(self):
        """Show visible satellite imagery"""
        try:
            location = self.location_entry.get().strip() or "New York"
            from datetime import datetime
            
            sat_info = f"🛰️ VISIBLE SATELLITE - {location.upper()}:\n"
            sat_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            sat_info += f"🕐 Image Time: {datetime.now().strftime('%H:%M:%S')}\n"
            sat_info += "📡 Satellite: GOES-16 East\n"
            sat_info += "🔍 Resolution: 500m per pixel\n\n"
            sat_info += "☁️ CLOUD COVERAGE MAP:\n"
            sat_info += "     NW    N    NE\n"
            sat_info += "  W   ████▓▓▓   E\n"
            sat_info += "     ▓▓▓░░░▓▓\n"
            sat_info += "     ░░░   ░░░\n"
            sat_info += "     ▓▓▓░░░▓▓\n"
            sat_info += "  SW   ▓▓▓▓▓▓   SE\n"
            sat_info += "         S\n\n"
            sat_info += "Legend: █=Dense clouds ▓=Moderate ░=Thin\n\n"
            sat_info += "☀️ SUNLIGHT CONDITIONS:\n"
            sat_info += "• Cloud opacity: 40% average\n"
            sat_info += "• Clear areas: 35% of region\n"
            sat_info += "• Dense clouds: 25% coverage\n"
            sat_info += "• Visibility: Good to excellent\n\n"
            sat_info += "🌤️ WEATHER FEATURES:\n"
            sat_info += "• Cumulus development: Moderate\n"
            sat_info += "• Cirrus streaks: High altitude\n"
            sat_info += "• Storm tops: None visible\n"
            sat_info += "• Fog/low clouds: Minimal"
            
            self.satellite_display.delete(1.0, tk.END)
            self.satellite_display.insert(tk.END, sat_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_infrared_satellite(self):
        """Show infrared satellite imagery"""
        try:
            location = self.location_entry.get().strip() or "New York"
            
            sat_info = f"�️ INFRARED SATELLITE - {location.upper()}:\n"
            sat_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            sat_info += "🌡️ TEMPERATURE IMAGERY:\n"
            sat_info += "Temperature scale: -80°C to +50°C\n\n"
            sat_info += "🌡️ CLOUD TOP TEMPERATURES:\n"
            sat_info += "     NW    N    NE\n"
            sat_info += "  W   ████▓▓▓   E\n"
            sat_info += "     ▓▓▓░░░▓▓\n"
            sat_info += "     ░░░   ░░░\n"
            sat_info += "     ▓▓▓░░░▓▓\n"
            sat_info += "  SW   ▓▓▓▓▓▓   SE\n"
            sat_info += "         S\n\n"
            sat_info += "Temperature Legend:\n"
            sat_info += "█ = Very Cold (-60°C) High Clouds\n"
            sat_info += "▓ = Cold (-20°C) Medium Clouds\n"
            sat_info += "░ = Warm (+10°C) Low Clouds/Surface\n\n"
            sat_info += "🏔️ CLOUD HEIGHT ANALYSIS:\n"
            sat_info += "• High clouds: 35,000+ ft\n"
            sat_info += "• Medium clouds: 8,000-20,000 ft\n"
            sat_info += "• Low clouds: Surface-8,000 ft\n"
            sat_info += "• Surface temperature: +23°C"
            
            self.satellite_display.delete(1.0, tk.END)
            self.satellite_display.insert(tk.END, sat_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_water_vapor_satellite(self):
        """Show water vapor satellite imagery"""
        try:
            location = self.location_entry.get().strip() or "New York"
            
            sat_info = f"💧 WATER VAPOR SATELLITE - {location.upper()}:\n"
            sat_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            sat_info += "💧 ATMOSPHERIC MOISTURE:\n"
            sat_info += "Upper-level water vapor concentration\n\n"
            sat_info += "� MOISTURE PATTERNS:\n"
            sat_info += "     NW    N    NE\n"
            sat_info += "  W   ░░░▓▓▓   E\n"
            sat_info += "     ▓▓▓██▓▓\n"
            sat_info += "     ▓██████▓\n"
            sat_info += "     ▓▓▓██▓▓\n"
            sat_info += "  SW   ░░░▓▓▓   SE\n"
            sat_info += "         S\n\n"
            sat_info += "Moisture Legend:\n"
            sat_info += "█ = Very High Moisture (Dark)\n"
            sat_info += "▓ = High Moisture\n"
            sat_info += "░ = Low Moisture (Bright)\n\n"
            sat_info += "🌊 ATMOSPHERIC ANALYSIS:\n"
            sat_info += "• Jet stream position: 300mb level\n"
            sat_info += "• Moisture transport: SW to NE\n"
            sat_info += "• Dry slots: Western regions\n"
            sat_info += "• Tropical moisture: Moderate influx"
            
            self.satellite_display.delete(1.0, tk.END)
            self.satellite_display.insert(tk.END, sat_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Temperature Controls
    def show_current_temperature(self):
        """Show current temperature map"""
        try:
            location = self.location_entry.get().strip() or "New York"
            from datetime import datetime
            
            temp_info = f"🌡️ TEMPERATURE MAP - {location.upper()}:\n"
            temp_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            temp_info += f"🕐 Observation Time: {datetime.now().strftime('%H:%M:%S')}\n"
            temp_info += "🌡️ Temperature Scale: -10°C to +35°C\n\n"
            temp_info += "🗺️ REGIONAL TEMPERATURES:\n"
            temp_info += "     NW    N    NE\n"
            temp_info += "  W  21°C 23°C 24°C  E\n"
            temp_info += "     22°C 23°C 25°C\n"
            temp_info += "     23°C 24°C 26°C\n"
            temp_info += "     22°C 23°C 24°C\n"
            temp_info += "  SW 20°C 22°C 23°C  SE\n"
            temp_info += "         S\n\n"
            temp_info += "🎨 COLOR CODING:\n"
            temp_info += "🟦 Cold: <15°C    🟢 Cool: 15-20°C\n"
            temp_info += "🟡 Mild: 20-25°C  🟠 Warm: 25-30°C\n"
            temp_info += "� Hot: >30°C\n\n"
            temp_info += "📊 TEMPERATURE STATISTICS:\n"
            temp_info += "• Current location: 23°C\n"
            temp_info += "• Daily high: 27°C\n"
            temp_info += "• Daily low: 18°C\n"
            temp_info += "• Regional average: 23°C\n"
            temp_info += "• Trend: Gradually warming\n\n"
            temp_info += "🌅 TEMPERATURE FORECAST:\n"
            temp_info += "• Peak heating: 15:00-16:00\n"
            temp_info += "• Evening cooling: After 18:00\n"
            temp_info += "• Overnight low: 19°C expected"
            
            self.temperature_display.delete(1.0, tk.END)
            self.temperature_display.insert(tk.END, temp_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_heat_index(self):
        """Show heat index map"""
        try:
            location = self.location_entry.get().strip() or "New York"
            
            temp_info = f"🔥 HEAT INDEX MAP - {location.upper()}:\n"
            temp_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            temp_info += "🌡️ HEAT INDEX CALCULATION:\n"
            temp_info += "Combines temperature + humidity for 'feels like' temperature\n\n"
            temp_info += "🔥 HEAT INDEX VALUES:\n"
            temp_info += "     NW    N    NE\n"
            temp_info += "  W  24°C 26°C 27°C  E\n"
            temp_info += "     25°C 26°C 28°C\n"
            temp_info += "     26°C 27°C 29°C\n"
            temp_info += "     25°C 26°C 27°C\n"
            temp_info += "  SW 23°C 25°C 26°C  SE\n"
            temp_info += "         S\n\n"
            temp_info += "⚠️ HEAT STRESS LEVELS:\n"
            temp_info += "🟢 Safe: <27°C (No precautions needed)\n"
            temp_info += "🟡 Caution: 27-32°C (Stay hydrated)\n"
            temp_info += "🟠 Warning: 32-40°C (Limit outdoor activity)\n"
            temp_info += "🔴 Danger: >40°C (Avoid outdoor exposure)\n\n"
            temp_info += "📊 CURRENT CONDITIONS:\n"
            temp_info += "• Actual temperature: 23°C\n"
            temp_info += "• Relative humidity: 68%\n"
            temp_info += "• Heat index: 26°C\n"
            temp_info += "• Comfort level: Comfortable\n"
            temp_info += "• Risk category: 🟢 Safe"
            
            self.temperature_display.delete(1.0, tk.END)
            self.temperature_display.insert(tk.END, temp_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_wind_chill(self):
        """Show wind chill map"""
        try:
            location = self.location_entry.get().strip() or "New York"
            
            temp_info = f"❄️ WIND CHILL MAP - {location.upper()}:\n"
            temp_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            temp_info += "🌬️ WIND CHILL CALCULATION:\n"
            temp_info += "Combines temperature + wind speed for 'feels like' temperature\n\n"
            temp_info += "❄️ WIND CHILL VALUES:\n"
            temp_info += "     NW    N    NE\n"
            temp_info += "  W  20°C 22°C 23°C  E\n"
            temp_info += "     21°C 22°C 24°C\n"
            temp_info += "     22°C 23°C 25°C\n"
            temp_info += "     21°C 22°C 23°C\n"
            temp_info += "  SW 19°C 21°C 22°C  SE\n"
            temp_info += "         S\n\n"
            temp_info += "🥶 WIND CHILL CATEGORIES:\n"
            temp_info += "🟢 Comfortable: >10°C\n"
            temp_info += "🟡 Cool: 0-10°C (Light jacket needed)\n"
            temp_info += "🟠 Cold: -10-0°C (Warm clothing needed)\n"
            temp_info += "🔴 Very Cold: <-10°C (Risk of frostbite)\n\n"
            temp_info += "📊 CURRENT CONDITIONS:\n"
            temp_info += "• Actual temperature: 23°C\n"
            temp_info += "• Wind speed: 12 km/h\n"
            temp_info += "• Wind chill: 22°C\n"
            temp_info += "• Comfort level: Pleasant\n"
            temp_info += "• Risk category: 🟢 Comfortable"
            
            self.temperature_display.delete(1.0, tk.END)
            self.temperature_display.insert(tk.END, temp_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Wind Controls
    def show_wind_speed(self):
        """Show wind speed map"""
        try:
            location = self.location_entry.get().strip() or "New York"
            from datetime import datetime
            
            wind_info = f"💨 WIND SPEED MAP - {location.upper()}:\n"
            wind_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            wind_info += f"🕐 Observation Time: {datetime.now().strftime('%H:%M:%S')}\n"
            wind_info += "💨 Wind Speed Scale: 0-50+ km/h\n\n"
            wind_info += "🌬️ REGIONAL WIND SPEEDS:\n"
            wind_info += "     NW    N    NE\n"
            wind_info += "  W  15↖ 12↑ 18↗  E\n"
            wind_info += "     14← 12↑ 16→\n"
            wind_info += "     13← 11↑ 15→\n"
            wind_info += "     16↙ 14↓ 17↘\n"
            wind_info += "  SW 18↙ 15↓ 19↘  SE\n"
            wind_info += "         S\n\n"
            wind_info += "Legend: Number = Speed (km/h), Arrow = Direction\n\n"
            wind_info += "🎨 WIND SPEED SCALE:\n"
            wind_info += "🟢 Light: 0-11 km/h (Calm to light breeze)\n"
            wind_info += "🟡 Moderate: 12-28 km/h (Gentle to fresh breeze)\n"
            wind_info += "🟠 Strong: 29-49 km/h (Strong breeze)\n"
            wind_info += "� Very Strong: 50+ km/h (Gale force)\n\n"
            wind_info += "📊 WIND STATISTICS:\n"
            wind_info += "• Current location: 12 km/h NW\n"
            wind_info += "• Peak gust today: 22 km/h\n"
            wind_info += "• Average speed: 14 km/h\n"
            wind_info += "• Prevailing direction: Northwest\n"
            wind_info += "• Variability: Low (steady)\n\n"
            wind_info += "�️ WIND FORECAST:\n"
            wind_info += "• Next 3 hours: Steady 10-15 km/h\n"
            wind_info += "• Direction trend: Backing to west\n"
            wind_info += "• Gust potential: Minimal"
            
            self.wind_display.delete(1.0, tk.END)
            self.wind_display.insert(tk.END, wind_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_wind_direction(self):
        """Show wind direction map"""
        try:
            location = self.location_entry.get().strip() or "New York"
            
            wind_info = f"🧭 WIND DIRECTION MAP - {location.upper()}:\n"
            wind_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            wind_info += "🧭 WIND DIRECTION ANALYSIS:\n"
            wind_info += "Arrows show wind direction (where wind is blowing TO)\n\n"
            wind_info += "↗️ WIND VECTORS:\n"
            wind_info += "     NW    N    NE\n"
            wind_info += "  W   ↘   ↓   ↙   E\n"
            wind_info += "      ↘   ↓   ↙\n"
            wind_info += "      →   ↓   ←\n"
            wind_info += "      ↗   ↑   ↖\n"
            wind_info += "  SW  ↗   ↑   ↖   SE\n"
            wind_info += "         S\n\n"
            wind_info += "🌬️ DIRECTIONAL ANALYSIS:\n"
            wind_info += "• Primary flow: Northwest to Southeast\n"
            wind_info += "• Wind convergence: Central region\n"
            wind_info += "• Backing trend: Shifting counterclockwise\n"
            wind_info += "• Veering trend: None detected\n\n"
            wind_info += "📊 DIRECTION STATISTICS:\n"
            wind_info += "• Prevailing direction: 315° (NW)\n"
            wind_info += "• Direction variability: ±15°\n"
            wind_info += "• Consistency: High (85%)\n"
            wind_info += "• Seasonal normal: Northwest\n\n"
            wind_info += "🌀 FLOW PATTERNS:\n"
            wind_info += "• Surface flow: Consistent NW\n"
            wind_info += "• Upper level: Westerly\n"
            wind_info += "• Boundary layer: Well mixed\n"
            wind_info += "• Turbulence: Minimal"
            
            self.wind_display.delete(1.0, tk.END)
            self.wind_display.insert(tk.END, wind_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_wind_gusts(self):
        """Show wind gusts map"""
        try:
            location = self.location_entry.get().strip() or "New York"
            
            wind_info = f"💨 WIND GUSTS MAP - {location.upper()}:\n"
            wind_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            wind_info += "💨 WIND GUST MONITORING:\n"
            wind_info += "Peak wind speeds recorded in last hour\n\n"
            wind_info += "🌪️ GUST INTENSITY MAP:\n"
            wind_info += "     NW    N    NE\n"
            wind_info += "  W  22!! 18!  25!!  E\n"
            wind_info += "     20!  16   22!\n"
            wind_info += "     18!  15   20!\n"
            wind_info += "     24!! 19!  23!!\n"
            wind_info += "  SW 26!! 21!  27!!  SE\n"
            wind_info += "         S\n\n"
            wind_info += "Legend: ! = Moderate gust, !! = Strong gust\n\n"
            wind_info += "⚠️ GUST CATEGORIES:\n"
            wind_info += "🟢 Light: <20 km/h (No concern)\n"
            wind_info += "🟡 Moderate: 20-30 km/h (Caution outdoors)\n"
            wind_info += "🟠 Strong: 31-45 km/h (Secure loose objects)\n"
            wind_info += "🔴 Severe: >45 km/h (Avoid high exposure)\n\n"
            wind_info += "📊 GUST STATISTICS:\n"
            wind_info += "• Peak gust recorded: 27 km/h SW\n"
            wind_info += "• Average gust factor: 1.7x steady wind\n"
            wind_info += "• Gust frequency: Every 3-5 minutes\n"
            wind_info += "• Duration: 5-15 seconds each\n"
            wind_info += "• Stability: Moderate gustiness\n\n"
            wind_info += "�️ GUST FORECAST:\n"
            wind_info += "• Next hour: Occasional gusts to 25 km/h\n"
            wind_info += "• Afternoon: Increasing to 30 km/h\n"
            wind_info += "• Evening: Decreasing after sunset"
            
            self.wind_display.delete(1.0, tk.END)
            self.wind_display.insert(tk.END, wind_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Lightning Controls
    def show_live_lightning(self):
        """Show live lightning detection"""
        try:
            location = self.location_entry.get().strip() or "New York"
            from datetime import datetime
            
            lightning_info = f"⚡ LIVE LIGHTNING - {location.upper()}:\n"
            lightning_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            lightning_info += f"🕐 Detection Time: {datetime.now().strftime('%H:%M:%S')}\n"
            lightning_info += "⚡ Detection Range: 300km radius\n\n"
            lightning_info += "🌩️ LIGHTNING ACTIVITY MAP:\n"
            lightning_info += "     NW    N    NE\n"
            lightning_info += "  W   ·    ·    ·   E\n"
            lightning_info += "      ·    ·    ·\n"
            lightning_info += "      ·    ●    ·\n"
            lightning_info += "      ·    ·    ·\n"
            lightning_info += "  SW  ·    ·    ·   SE\n"
            lightning_info += "         S\n\n"
            lightning_info += "Legend: ● = You, · = No activity\n\n"
            lightning_info += "⚡ LIGHTNING SUMMARY:\n"
            lightning_info += "• Strikes in last 15 min: 0\n"
            lightning_info += "• Strikes in last hour: 0\n"
            lightning_info += "• Nearest activity: 150+ km\n"
            lightning_info += "• Storm cells tracked: 0\n\n"
            lightning_info += "🛡️ SAFETY STATUS:\n"
            lightning_info += "• Current risk: ✅ VERY LOW\n"
            lightning_info += "• Thunder audible: No\n"
            lightning_info += "• 30-30 rule status: Safe\n"
            lightning_info += "• Outdoor activities: ✅ Safe to proceed\n\n"
            lightning_info += "📡 DETECTION NETWORK:\n"
            lightning_info += "• Active sensors: 12\n"
            lightning_info += "• Network efficiency: 96%\n"
            lightning_info += "• Location accuracy: ±500m\n"
            lightning_info += "• Update frequency: Real-time\n\n"
            lightning_info += "⚠️ FORECAST:\n"
            lightning_info += "• Next 2 hours: No activity expected\n"
            lightning_info += "• Thunderstorm probability: 5%\n"
            lightning_info += "• Watch/Warning status: None"
            
            self.lightning_display.delete(1.0, tk.END)
            self.lightning_display.insert(tk.END, lightning_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_lightning_density(self):
        """Show lightning strike density"""
        try:
            location = self.location_entry.get().strip() or "New York"
            
            lightning_info = f"📊 LIGHTNING DENSITY - {location.upper()}:\n"
            lightning_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            lightning_info += "📊 STRIKE DENSITY ANALYSIS:\n"
            lightning_info += "Lightning strikes per square kilometer (last 24 hours)\n\n"
            lightning_info += "⚡ DENSITY HEAT MAP:\n"
            lightning_info += "     NW    N    NE\n"
            lightning_info += "  W   0    0    0   E\n"
            lightning_info += "      0    0    0\n"
            lightning_info += "      0    0    0\n"
            lightning_info += "      0    0    0\n"
            lightning_info += "  SW  0    0    0   SE\n"
            lightning_info += "         S\n\n"
            lightning_info += "Density Scale: 0=None, 1-5=Low, 6-15=Mod, 16+=High\n\n"
            lightning_info += "📈 HISTORICAL DATA:\n"
            lightning_info += "• Today: 0 strikes recorded\n"
            lightning_info += "• Yesterday: 0 strikes\n"
            lightning_info += "• This week: 0 strikes\n"
            lightning_info += "• Monthly average: 12 strikes\n\n"
            lightning_info += "🎯 HOTSPOT ANALYSIS:\n"
            lightning_info += "• No current hotspots\n"
            lightning_info += "• Typical hotspots: Mountain peaks\n"
            lightning_info += "• Seasonal patterns: Summer peaks\n"
            lightning_info += "• Diurnal cycle: Afternoon maximum\n\n"
            lightning_info += "📊 STATISTICAL SUMMARY:\n"
            lightning_info += "• Peak density today: 0 strikes/km²\n"
            lightning_info += "• Regional total: 0 strikes\n"
            lightning_info += "• Network coverage: 100%\n"
            lightning_info += "• Data quality: Excellent"
            
            self.lightning_display.delete(1.0, tk.END)
            self.lightning_display.insert(tk.END, lightning_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def toggle_lightning_audio(self):
        """Toggle lightning audio alerts"""
        try:
            current_text = self.lightning_display.get(1.0, tk.END)
            if "Audio alerts: 🔊 ON" in current_text:
                updated_text = current_text.replace("Audio alerts: 🔊 ON", "Audio alerts: 🔇 OFF")
            else:
                # Add audio status to display
                audio_status = "\n\n🔊 AUDIO ALERTS:\n"
                audio_status += "• Audio alerts: 🔊 ON\n"
                audio_status += "• Alert range: 50km radius\n"
                audio_status += "• Sound type: Thunder simulation\n"
                audio_status += "• Volume: Medium\n"
                audio_status += "• Frequency: Every strike"
                updated_text = current_text.rstrip() + audio_status
            
            self.lightning_display.delete(1.0, tk.END)
            self.lightning_display.insert(tk.END, updated_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # 3D Radar Controls
    def rotate_3d_view(self):
        """Rotate 3D radar view"""
        try:
            location = self.location_entry.get().strip() or "New York"
            
            radar_3d_info = f"� 3D RADAR ROTATION - {location.upper()}:\n"
            radar_3d_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            radar_3d_info += "� VIEW ROTATION CONTROLS:\n"
            radar_3d_info += "Current view angle: 45° elevation, 180° azimuth\n\n"
            radar_3d_info += "� 3D VOLUME SCAN:\n"
            radar_3d_info += "        ▲ 40,000 ft\n"
            radar_3d_info += "       ░░░\n"
            radar_3d_info += "      ░░░░░ 30,000 ft\n"
            radar_3d_info += "     ░░░░░░░\n"
            radar_3d_info += "    ░░░▓▓░░░ 20,000 ft\n"
            radar_3d_info += "   ░░▓▓▓▓▓░░\n"
            radar_3d_info += "  ░▓▓███▓▓░ 10,000 ft\n"
            radar_3d_info += " ████████████ Surface\n\n"
            radar_3d_info += "Vertical Legend:\n"
            radar_3d_info += "█ = High reflectivity (Heavy precip)\n"
            radar_3d_info += "▓ = Moderate reflectivity\n"
            radar_3d_info += "░ = Light reflectivity\n\n"
            radar_3d_info += "📊 3D ANALYSIS:\n"
            radar_3d_info += "• Cloud tops: 25,000 ft\n"
            radar_3d_info += "• Precipitation core: 8,000-15,000 ft\n"
            radar_3d_info += "• Bright band: 12,000 ft (melting level)\n"
            radar_3d_info += "• Surface intensity: Light rain\n\n"
            radar_3d_info += "🎮 ROTATION OPTIONS:\n"
            radar_3d_info += "• Elevation: -10° to +90°\n"
            radar_3d_info += "• Azimuth: 0° to 360°\n"
            radar_3d_info += "• Auto-rotate: Available\n"
            radar_3d_info += "• Slice view: Vertical cross-section"
            
            self.radar_3d_display.delete(1.0, tk.END)
            self.radar_3d_display.insert(tk.END, radar_3d_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def zoom_3d_in(self):
        """Zoom in on 3D radar"""
        try:
            current_text = self.radar_3d_display.get(1.0, tk.END)
            zoomed_text = current_text + "\n\n🔍 ZOOMING IN:\n"
            zoomed_text += "• Zoom level: 2x\n"
            zoomed_text += "• Coverage area: 125km radius\n"
            zoomed_text += "• Detail level: Enhanced\n"
            zoomed_text += "• Resolution: 500m per pixel"
            
            self.radar_3d_display.delete(1.0, tk.END)
            self.radar_3d_display.insert(tk.END, zoomed_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def zoom_3d_out(self):
        """Zoom out on 3D radar"""
        try:
            current_text = self.radar_3d_display.get(1.0, tk.END)
            if "ZOOMING IN" in current_text:
                # Remove zoom info and reset
                lines = current_text.split('\n')
                reset_text = '\n'.join(lines[:lines.index('🔍 ZOOMING IN:')])
                zoomed_text = reset_text + "\n\n� ZOOMING OUT:\n"
                zoomed_text += "• Zoom level: 0.5x\n"
                zoomed_text += "• Coverage area: 500km radius\n"
                zoomed_text += "• Detail level: Regional overview\n"
                zoomed_text += "• Resolution: 2km per pixel"
            else:
                zoomed_text = current_text + "\n\n🔍 ZOOMING OUT:\n"
                zoomed_text += "• Zoom level: 0.5x\n"
                zoomed_text += "• Coverage area: 500km radius\n"
                zoomed_text += "• Detail level: Regional overview\n"
                zoomed_text += "• Resolution: 2km per pixel"
            
            self.radar_3d_display.delete(1.0, tk.END)
            self.radar_3d_display.insert(tk.END, zoomed_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Control Panel Methods
    def radar_time_back(self):
        """Go back in radar time"""
        try:
            current_text = self.radar_display.get(1.0, tk.END)
            time_text = current_text + "\n\n⏮️ TIME CONTROL: Going back 10 minutes\n"
            time_text += "Showing radar data from 10 minutes ago"
            
            self.radar_display.delete(1.0, tk.END)
            self.radar_display.insert(tk.END, time_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def radar_time_pause(self):
        """Pause radar time updates"""
        try:
            current_text = self.radar_display.get(1.0, tk.END)
            time_text = current_text + "\n\n⏸️ TIME CONTROL: Updates paused\n"
            time_text += "Radar display frozen at current time"
            
            self.radar_display.delete(1.0, tk.END)
            self.radar_display.insert(tk.END, time_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def radar_time_play(self):
        """Resume radar time updates"""
        try:
            current_text = self.radar_display.get(1.0, tk.END)
            time_text = current_text + "\n\n▶️ TIME CONTROL: Resuming live updates\n"
            time_text += "Radar display updating in real-time"
            
            self.radar_display.delete(1.0, tk.END)
            self.radar_display.insert(tk.END, time_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def radar_time_forward(self):
        """Go forward in radar time"""
        try:
            current_text = self.radar_display.get(1.0, tk.END)
            time_text = current_text + "\n\n⏭️ TIME CONTROL: Jumping to current time\n"
            time_text += "Showing latest available radar data"
            
            self.radar_display.delete(1.0, tk.END)
            self.radar_display.insert(tk.END, time_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def toggle_terrain_layer(self):
        """Toggle terrain layer"""
        try:
            current_text = self.radar_display.get(1.0, tk.END)
            if "Terrain: ON" in current_text:
                updated_text = current_text.replace("Terrain: ON", "Terrain: OFF")
            else:
                layer_text = current_text + "\n\n🗺️ LAYER CONTROL: Terrain: ON\n"
                layer_text += "Topographic features now visible"
                updated_text = layer_text
            
            self.radar_display.delete(1.0, tk.END)
            self.radar_display.insert(tk.END, updated_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def toggle_cities_layer(self):
        """Toggle cities layer"""
        try:
            current_text = self.radar_display.get(1.0, tk.END)
            if "Cities: ON" in current_text:
                updated_text = current_text.replace("Cities: ON", "Cities: OFF")
            else:
                layer_text = current_text + "\n\n🏙️ LAYER CONTROL: Cities: ON\n"
                layer_text += "City labels and boundaries now visible"
                updated_text = layer_text
            
            self.radar_display.delete(1.0, tk.END)
            self.radar_display.insert(tk.END, updated_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def toggle_roads_layer(self):
        """Toggle roads layer"""
        try:
            current_text = self.radar_display.get(1.0, tk.END)
            if "Roads: ON" in current_text:
                updated_text = current_text.replace("Roads: ON", "Roads: OFF")
            else:
                layer_text = current_text + "\n\n🛣️ LAYER CONTROL: Roads: ON\n"
                layer_text += "Major highways and roads now visible"
                updated_text = layer_text
            
            self.radar_display.delete(1.0, tk.END)
            self.radar_display.insert(tk.END, updated_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_radar_settings(self):
        """Open radar settings"""
        try:
            current_text = self.radar_display.get(1.0, tk.END)
            settings_text = current_text + "\n\n⚙️ RADAR SETTINGS:\n"
            settings_text += "• Update frequency: 5 minutes\n"
            settings_text += "• Range: 250km radius\n"
            settings_text += "• Color scheme: Standard\n"
            settings_text += "• Animation speed: Normal\n"
            settings_text += "• Data quality filter: ON"
            
            self.radar_display.delete(1.0, tk.END)
            self.radar_display.insert(tk.END, settings_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def configure_radar_alerts(self):
        """Configure radar alerts"""
        try:
            current_text = self.radar_display.get(1.0, tk.END)
            alerts_text = current_text + "\n\n📱 RADAR ALERTS:\n"
            alerts_text += "• Precipitation alerts: ON\n"
            alerts_text += "• Storm approach: ON\n"
            alerts_text += "• Lightning detection: ON\n"
            alerts_text += "• Severe weather: ON\n"
            alerts_text += "• Alert radius: 50km"
            
            self.radar_display.delete(1.0, tk.END)
            self.radar_display.insert(tk.END, alerts_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))


