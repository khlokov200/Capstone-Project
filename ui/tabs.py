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
        
        # Results display
        self.result_text = StyledText(self.frame)
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
        StyledButton(self.frame, "primary", text="Get Weather", 
                    command=self.fetch_weather).pack(pady=5)
        
        StyledButton(self.frame, "info", text="Toggle Graph Type", 
                    command=self.controller.toggle_graph_mode).pack(pady=5)

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
        self.result_text.insert(tk.END, 
            f"Weather in {weather_data.city}:\n"
            f"{weather_data.formatted_temperature}\n"
            f"{weather_data.description}")

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
        
        StyledButton(self.frame, "primary", text="Get Forecast", 
                    command=self.fetch_forecast).pack(pady=5)

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
        
        StyledButton(self.frame, "primary", text="Get 5-Day Forecast", 
                    command=self.fetch_5day_forecast).pack(pady=5)

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
        
        StyledButton(self.frame, "info", text="Compare", 
                    command=self.compare_cities).pack(pady=5)

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
        
        StyledButton(self.frame, "primary", text="Save Entry", 
                    command=self.save_journal).pack(pady=5)

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
        
        StyledButton(self.frame, "dark", text="Generate Poem", 
                    command=self.generate_poem).pack(pady=5)

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
