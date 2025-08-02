"""
Main Window - Clean UI assembly with proper separation of concerns
"""
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ui.constants import COLOR_PALETTE, UI_CONFIG
from ui.components import StyledButton
from ui.tabs import (WeatherTab, ForecastTab, FiveDayForecastTab, ComparisonTab, 
                     JournalTab, ActivityTab, PoetryTab, HistoryTab, QuickActionsTab, LiveWeatherTab,
                     SevereWeatherTab, AnalyticsTrendsTab, HealthWellnessTab, SmartAlertsTab, WeatherCameraTab)


class MainWindow(tk.Tk):
    """Main application window with clean separation of concerns"""
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.theme = "dark"
        self.palette = self._get_palette()
        self._setup_window()
        self._setup_styles()
        self._create_layout()
        self._setup_graph()

    def _get_palette(self):
        from ui.constants import get_palette
        return get_palette(self.theme)

    def _setup_window(self):
        """Configure the main window"""
        self.title(UI_CONFIG["window_title"])
        self.geometry(UI_CONFIG["window_geometry"])
        self.configure(bg=self.palette["background"])

    def _setup_styles(self):
        """Setup TTK styles"""
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", 
                       background=self.palette["background"], 
                       borderwidth=0)
        style.configure("TNotebook.Tab", 
                       background=self.palette["tab_bg"], 
                       foreground=self.palette["tab_fg"], 
                       padding=10)
        style.map("TNotebook.Tab", 
                 background=[("selected", self.palette["accent"])] )

    def _create_layout(self):
        """Create the main layout"""
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill="both", expand=True)
        # Theme toggle button
        self._create_theme_toggle()
        # Temperature unit toggle button
        self._create_unit_toggle()
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        # Create all tabs
        self._create_tabs()

    def _create_theme_toggle(self):
        """Create a theme toggle button"""
        btn = tk.Button(self.content_frame, text=self._get_theme_toggle_text(), command=self._toggle_theme)
        btn.pack(pady=5)
        self.theme_toggle_btn = btn

    def _get_theme_toggle_text(self):
        return "Switch to Light Theme" if self.theme == "dark" else "Switch to Dark Theme"

    def _toggle_theme(self):
        """Toggle between light and dark themes"""
        self.theme = "light" if self.theme == "dark" else "dark"
        self.palette = self._get_palette()
        self._apply_theme()
        # Update the button text to reflect the new theme
        self.theme_toggle_btn.config(text=self._get_theme_toggle_text())
        # Force redraw of the window and notebook to ensure background updates
        self.update_idletasks()
        if hasattr(self, 'notebook'):
            self.notebook.update_idletasks()

    def _apply_theme(self):
        """Apply the current theme to the window and widgets (background only)"""
        # Update the background colors of the main window and content frame
        self.configure(bg=self.palette["background"])
        self.content_frame.configure(bg=self.palette["background"])
        # Update notebook and tab backgrounds
        if hasattr(self, 'notebook'):
            style = ttk.Style(self)
            style.theme_use("clam")
            style.configure("TNotebook", background=self.palette["background"])
            style.configure("TNotebook.Tab", background=self.palette["tab_bg"], foreground=self.palette["tab_fg"])
            style.map("TNotebook.Tab", background=[("selected", self.palette["accent"])] )
            self.notebook.configure(bg=self.palette["background"])
            # Update all tab frames' backgrounds recursively
            for tab in self.notebook.winfo_children():
                self._set_frame_bg_recursive(tab, self.palette["background"])
            # Redraw tabs to force update
            self.notebook.update_idletasks()

    def _set_frame_bg_recursive(self, widget, color):
        # Recursively set background color for all frames and their children
        try:
            widget.configure(bg=color)
        except Exception:
            pass
        for child in getattr(widget, 'winfo_children', lambda: [])():
            self._set_frame_bg_recursive(child, color)

    def _update_tab_themes(self):
        """Update theme for all custom widgets in all tabs"""
        for tab in getattr(self, 'notebook', []).winfo_children():
            self._update_widget_theme(tab)

    def _update_widget_theme(self, widget):
        # Recursively update theme for custom widgets
        from ui.components import StyledButton, StyledLabel, StyledText
        if isinstance(widget, (StyledButton, StyledLabel, StyledText)):
            widget.update_theme(self.palette)
        for child in getattr(widget, 'winfo_children', lambda: [])():
            self._update_widget_theme(child)

    def _create_unit_toggle(self):
        """Create the temperature unit toggle button"""
        self.toggle_btn = StyledButton(
            self.content_frame,
            style_type="cool_black",
            text="Switch to °F",
            command=self._toggle_unit
        )
        self.toggle_btn.pack(pady=10)

    def _create_tabs(self):
        """Create all dashboard tabs"""
        # Quick Actions tab as the first tab
        self.quick_actions_tab = QuickActionsTab(self.notebook, self.controller)
        
        # Main weather tab with graph
        self.weather_tab = WeatherTab(self.notebook, self.controller)
        
        # Live Weather tab with animations and radar
        self.live_weather_tab = LiveWeatherTab(self.notebook, self.controller)
        
        # Forecast tabs
        self.forecast_tab = ForecastTab(self.notebook, self.controller)
        
        # New tabs positioned after forecast tab
        self.severe_weather_tab = SevereWeatherTab(self.notebook, self.controller)
        self.analytics_trends_tab = AnalyticsTrendsTab(self.notebook, self.controller)
        self.health_wellness_tab = HealthWellnessTab(self.notebook, self.controller)
        self.smart_alerts_tab = SmartAlertsTab(self.notebook, self.controller)
        self.weather_camera_tab = WeatherCameraTab(self.notebook, self.controller)
        
        # Remaining tabs
        self.five_day_tab = FiveDayForecastTab(self.notebook, self.controller)
        self.comparison_tab = ComparisonTab(self.notebook, self.controller)
        self.journal_tab = JournalTab(self.notebook, self.controller)
        self.activity_tab = ActivityTab(self.notebook, self.controller)
        self.poetry_tab = PoetryTab(self.notebook, self.controller)
        self.history_tab = HistoryTab(self.notebook, self.controller)

    def _setup_graph(self):
        """Setup the graph components in the weather tab"""
        # Create matplotlib figure and canvas
        self.fig, self.ax = plt.subplots(figsize=(5, 2))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.weather_tab.frame)
        self.canvas.get_tk_widget().pack()
        
        # Connect graph components to controller
        self.controller.set_graph_components(self.fig, self.ax, self.canvas)
        
        # Initial graph update
        self.controller.update_graph()

    def _toggle_unit(self):
        """Toggle temperature unit and update button text"""
        self.controller.toggle_unit()
        
        if self.controller.temp_unit_value == "imperial":
            self.toggle_btn.config(text="Switch to °C", 
                                 bg="#FFB347",  # Light orange background
                                 fg=COLOR_PALETTE["text_on_button_black"])
        else:
            self.toggle_btn.config(text="Switch to °F", 
                                 bg="#87CEEB",  # Sky blue background
                                 fg=COLOR_PALETTE["text_on_button_black"])

    # Quick Action Methods
    def _quick_weather(self):
        """Get weather for last used city or prompt for new city"""
        city = self.controller.last_city
        if not city:
            city = self._prompt_for_city("Enter city for quick weather:")
        
        if city:
            try:
                weather_data = self.controller.get_quick_weather(city)
                self._show_quick_result("Quick Weather", 
                    f"Weather in {weather_data.city}:\n"
                    f"🌡️ {weather_data.formatted_temperature}\n"
                    f"📋 {weather_data.description}\n"
                    f"💧 Humidity: {weather_data.humidity}%\n"
                    f"💨 Wind: {weather_data.formatted_wind}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to get weather: {str(e)}")

    def _quick_forecast(self):
        """Get 5-day forecast for last used city or prompt for new city"""
        city = self.controller.last_city
        if not city:
            city = self._prompt_for_city("Enter city for 5-day forecast:")
        
        if city:
            try:
                forecast = self.controller.get_five_day_forecast(city)
                self._show_quick_result("5-Day Forecast", forecast)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to get forecast: {str(e)}")

    def _quick_activity(self):
        """Get activity suggestion for last used city or prompt for new city"""
        city = self.controller.last_city
        if not city:
            city = self._prompt_for_city("Enter city for activity suggestion:")
        
        if city:
            try:
                activity = self.controller.suggest_activity(city)
                self._show_quick_result("Activity Suggestion", activity)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to get activity suggestion: {str(e)}")

    def _weather_summary(self):
        """Get comprehensive weather summary"""
        city = self.controller.last_city
        if not city:
            city = self._prompt_for_city("Enter city for weather summary:")
        
        if city:
            try:
                summary = self.controller.get_weather_summary(city)
                self._show_quick_result("Weather Summary", summary)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to get weather summary: {str(e)}")

    def _save_favorite(self):
        """Save current or entered city as favorite"""
        city = self.controller.last_city
        if not city:
            city = self._prompt_for_city("Enter city to save as favorite:")
        
        if city:
            result = self.controller.add_favorite_city(city)
            messagebox.showinfo("Favorite Saved", result)

    def _check_alerts(self):
        """Check weather alerts for last used city or prompt for new city"""
        city = self.controller.last_city
        if not city:
            city = self._prompt_for_city("Enter city to check weather alerts:")
        
        if city:
            try:
                alerts = self.controller.check_weather_alerts(city)
                self._show_quick_result("Weather Alerts", alerts)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to check alerts: {str(e)}")

    def _prompt_for_city(self, prompt_text):
        """Prompt user for city name"""
        from tkinter import simpledialog
        return simpledialog.askstring("City Input", prompt_text)

    def _show_quick_result(self, title, content):
        """Show quick result in a popup window"""
        popup = tk.Toplevel(self)
        popup.title(title)
        popup.geometry("500x400")
        popup.configure(bg=COLOR_PALETTE["background"])
        
        # Make popup modal
        popup.transient(self)
        popup.grab_set()
        
        # Add scrollable text widget
        text_frame = ttk.Frame(popup)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap="word", 
                             bg=COLOR_PALETTE["tab_bg"], 
                             fg=COLOR_PALETTE["tab_fg"],
                             font=("Arial", 10))
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        text_widget.insert("1.0", content)
        text_widget.config(state="disabled")
        
        # Add close button
        close_btn = StyledButton(popup, "primary", text="Close", 
                               command=popup.destroy)
        close_btn.pack(pady=10)
