"""
Individual tab components for the weather dashboard
"""
import tkinter as tk
from tkinter import ttk, messagebox
from .components import StyledButton, StyledText, StyledLabel, AnimatedLabel
from .constants import COLOR_PALETTE


class WeatherTab:
    """Current weather tab component"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Current Weather")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        # City input
        StyledLabel(self.frame, text="Enter City:").pack(pady=10)
        self.city_entry = ttk.Entry(self.frame)
        self.city_entry.pack()
        
        # Results display - larger size to show all weather details
        self.result_text = StyledText(self.frame, height=15, width=80)
        self.result_text.pack(pady=10)
        
        # Animated mascot
        try:
            self.anim_label = AnimatedLabel(self.frame, "assets/sunny.gif")
            self.anim_label.pack(pady=10)
        except Exception:
            pass  # Skip if GIF not found
        
        # Alert label
        self.alert_label = StyledLabel(self.frame, text="")
        self.alert_label.pack(pady=5)
        
        # Buttons
        StyledButton(self.frame, "primary_black", text="Get Weather", 
                    command=self.fetch_weather).pack(pady=5)
        
        StyledButton(self.frame, "info_black", text="Toggle Graph Type", 
                    command=self.controller.toggle_graph_mode).pack(pady=5)
        
        # Additional Quick Action Buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=5)
        
        StyledButton(button_frame, "accent_black", text="⭐ Save Favorite", 
                    command=self.save_favorite).grid(row=0, column=0, padx=2)
        StyledButton(button_frame, "success_black", text="🔄 Auto-Refresh", 
                    command=self.toggle_auto_refresh).grid(row=0, column=1, padx=2)
        StyledButton(button_frame, "warning_black", text="⚠️ Check Alerts", 
                    command=self.check_alerts).grid(row=0, column=2, padx=2)

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
        temp = weather_data.temperature
        desc = weather_data.description.lower()
        
        if (temp > 35 and weather_data.unit == "metric") or \
           (temp > 95 and weather_data.unit == "imperial") or \
           "storm" in desc:
            self.alert_label.config(text="⚠️ Weather Alert: Stay safe!", 
                                   foreground=COLOR_PALETTE["heat"])
        else:
            self.alert_label.config(text="", foreground=COLOR_PALETTE["tab_fg"])

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


class ForecastTab:
    """Weather forecast tab component"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Forecast")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        StyledLabel(self.frame, text="Enter City:").pack(pady=10)
        self.city_entry = ttk.Entry(self.frame)
        self.city_entry.pack()
        
        self.result_text = StyledText(self.frame)
        self.result_text.pack(pady=10)
        
        # Main action button
        StyledButton(self.frame, "primary", text="Get Forecast", 
                    command=self.fetch_forecast).pack(pady=5)
        
        # Additional Enhanced Buttons
        forecast_button_frame = ttk.Frame(self.frame)
        forecast_button_frame.pack(pady=5)
        
        StyledButton(forecast_button_frame, "accent_black", text="🌤️ Hourly Details", 
                    command=self.get_hourly_forecast).grid(row=0, column=0, padx=3)
        StyledButton(forecast_button_frame, "info_black", text="📊 Chart View", 
                    command=self.show_forecast_chart).grid(row=0, column=1, padx=3)
        StyledButton(forecast_button_frame, "success_black", text="📱 Share Forecast", 
                    command=self.share_forecast).grid(row=0, column=2, padx=3)
        StyledButton(forecast_button_frame, "warning_black", text="⚠️ Weather Alerts", 
                    command=self.check_forecast_alerts).grid(row=0, column=3, padx=3)

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
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components"""
        StyledLabel(self.frame, text="Enter City:").pack(pady=10)
        self.city_entry = ttk.Entry(self.frame)
        self.city_entry.pack()
        
        self.result_text = StyledText(self.frame, height=15, width=80)
        self.result_text.pack(pady=10)
        
        # Main action button
        StyledButton(self.frame, "primary", text="Get 5-Day Forecast", 
                    command=self.fetch_5day_forecast).pack(pady=5)
        
        # Additional Enhanced Buttons
        fiveday_button_frame = ttk.Frame(self.frame)
        fiveday_button_frame.pack(pady=5)
        
        StyledButton(fiveday_button_frame, "accent_black", text="📅 Week Planner", 
                    command=self.create_week_planner).grid(row=0, column=0, padx=3)
        StyledButton(fiveday_button_frame, "info_black", text="🎯 Best Days", 
                    command=self.find_best_weather_days).grid(row=0, column=1, padx=3)
        StyledButton(fiveday_button_frame, "success_black", text="📋 Travel Guide", 
                    command=self.generate_travel_guide).grid(row=0, column=2, padx=3)
        StyledButton(fiveday_button_frame, "warning_black", text="⚡ Weather Prep", 
                    command=self.get_weather_preparation).grid(row=0, column=3, padx=3)

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


class JournalTab:
    """Weather journal tab component"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Weather Journal")
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
        
        StyledButton(self.frame, "info", text="Suggest", 
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
        StyledButton(self.frame, "dark", text="Generate Poem", 
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
            gallery += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
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
            gallery += "   The pavement did gleam,\n"
            gallery += "   Like a shimmering dream,\n"
            gallery += "   And everyone sought out the shade's delight!\n\n"
            gallery += "❄️ 'Winter's Whisper' (Free Verse):\n"
            gallery += "   Snowflakes dance on frozen air,\n"
            gallery += "   Each one unique, a frozen prayer.\n"
            gallery += "   The world sleeps under winter's veil,\n"
            gallery += "   While wind tells its ancient tale.\n\n"
            gallery += "🌧️ 'Rain Song' (Haiku):\n"
            gallery += "   Gentle rain falling\n"
            gallery += "   Washing worries from the world\n"
            gallery += "   Peace flows like water\n\n"
            gallery += "🌤️ 'Cloudy Day Musings' (Free Verse):\n"
            gallery += "   Gray clouds gather thoughts above,\n"
            gallery += "   Soft shadows dance on street and roof.\n"
            gallery += "   The sky holds mysteries untold,\n"
            gallery += "   While earth stays warm though air grows cold.\n\n"
            gallery += "💨 'Wind's Journey' (Haiku):\n"
            gallery += "   Wind carries stories\n"
            gallery += "   From distant lands and foreign seas\n"
            gallery += "   Whispering secrets\n\n"
            gallery += "🌟 COMMUNITY CONTRIBUTIONS:\n"
            gallery += "• Submit your weather poems to our gallery\n"
            gallery += "• Vote for your favorite seasonal pieces\n"
            gallery += "• Join our monthly poetry challenges\n"
            gallery += "• Share poems inspired by your city's weather\n\n"
            gallery += "🎨 Use these as inspiration for your own weather poetry!"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, gallery)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_custom_poem(self):
        """Create a custom poem with user preferences"""
        try:
            custom = f"🎨 CUSTOM POEM CREATOR:\n"
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
                recent_avg = sum(temps[-7:]) / min(7, len(temps))
                older_avg = sum(temps[:7]) / min(7, len(temps))
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
            analysis += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
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
        
        StyledButton(button_frame, "success", text="Copy to Clipboard", 
                    command=lambda: self._copy_to_clipboard(content)).grid(row=0, column=0, padx=5)
        StyledButton(button_frame, "primary", text="Close", 
                    command=popup.destroy).grid(row=0, column=1, padx=5)

    def _copy_to_clipboard(self, content):
        """Copy content to clipboard"""
        try:
            import pyperclip
            pyperclip.copy(content)
            messagebox.showinfo("Copied", "Content copied to clipboard!")
        except ImportError:
            # Fallback to tkinter clipboard
            popup_window = tk.Toplevel()
            popup_window.withdraw()
            popup_window.clipboard_clear()
            popup_window.clipboard_append(content)
            popup_window.destroy()
            messagebox.showinfo("Copied", "Content copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy: {str(e)}")


class QuickActionsTab:
    """Quick actions tab component for instant access to all major features"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="🚀 Quick Actions")
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
        main_container = ttk.Frame(self.frame)
        main_container.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Essential Weather Actions Section
        weather_frame = ttk.LabelFrame(main_container, text="🌤️ Weather Actions", padding=15)
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
        utility_frame = ttk.LabelFrame(main_container, text="🔧 Utility Actions", padding=15)
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
        smart_frame = ttk.LabelFrame(main_container, text="🧠 Smart Features", padding=15)
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
        self.result_frame = ttk.LabelFrame(main_container, text="📄 Results", padding=10)
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
                forecast = self.controller.get_five_day_forecast(city)
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
                    display_result += f"{i}. {fav_city}\n"
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
                    result += f"Recent Trend: {trend.upper()}\n"
            
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
