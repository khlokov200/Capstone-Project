"""
Main Window - Clean UI assembly with proper separation of concerns
"""
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ui.constants import COLOR_PALETTE, UI_CONFIG
from ui.components import StyledButton
from ui.tabs import (WeatherTab, ForecastTab, FiveDayForecastTab, ComparisonTab, 
                     JournalTab, ActivityTab, PoetryTab, HistoryTab)


class MainWindow(tk.Tk):
    """Main application window with clean separation of concerns"""
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._setup_window()
        self._setup_styles()
        self._create_layout()
        self._setup_graph()

    def _setup_window(self):
        """Configure the main window"""
        self.title(UI_CONFIG["window_title"])
        self.geometry(UI_CONFIG["window_geometry"])
        self.configure(bg=COLOR_PALETTE["background"])

    def _setup_styles(self):
        """Setup TTK styles"""
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", 
                       background=COLOR_PALETTE["background"], 
                       borderwidth=0)
        style.configure("TNotebook.Tab", 
                       background=COLOR_PALETTE["tab_bg"], 
                       foreground=COLOR_PALETTE["tab_fg"], 
                       padding=10)
        style.map("TNotebook.Tab", 
                 background=[("selected", COLOR_PALETTE["accent"])])

    def _create_layout(self):
        """Create the main layout"""
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill="both", expand=True)
        
        # Temperature unit toggle button
        self._create_unit_toggle()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create all tabs
        self._create_tabs()

    def _create_unit_toggle(self):
        """Create the temperature unit toggle button"""
        self.toggle_btn = StyledButton(
            self.content_frame,
            style_type="cool",
            text="Switch to °F",
            command=self._toggle_unit
        )
        self.toggle_btn.pack(pady=10)

    def _create_tabs(self):
        """Create all dashboard tabs"""
        # Main weather tab with graph
        self.weather_tab = WeatherTab(self.notebook, self.controller)
        
        # Other tabs
        self.forecast_tab = ForecastTab(self.notebook, self.controller)
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
                                 bg=COLOR_PALETTE["button_warning"], 
                                 fg=COLOR_PALETTE["text_on_button"])
        else:
            self.toggle_btn.config(text="Switch to °F", 
                                 bg=COLOR_PALETTE["button_secondary"], 
                                 fg=COLOR_PALETTE["text_on_button"])
