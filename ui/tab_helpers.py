"""
Helper classes and methods to reduce duplication across tabs
"""
import tkinter as tk
from tkinter import ttk, messagebox
from .components import StyledButton, StyledText, StyledLabel
from .constants import COLOR_PALETTE

# Matplotlib imports with availability checking
CHARTS_AVAILABLE = False
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    from matplotlib.figure import Figure
    import numpy as np
    CHARTS_AVAILABLE = True
except ImportError:
    print("📊 Charts unavailable: matplotlib not installed")

class BaseTab:
    """Base class for all weather tabs to reduce duplication"""
    
    def __init__(self, notebook, controller, tab_name):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text=tab_name)

    def get_city_input(self):
        """Get and validate city input"""
        if not hasattr(self, 'city_entry'):
            return None
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return None
        return city

    def display_result(self, content):
        """Display result in the text widget"""
        if hasattr(self, 'result_text'):
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, content)

    def handle_error(self, error, action="operation"):
        """Standardized error handling"""
        error_msg = f"Error during {action}: {str(error)}"
        messagebox.showerror("Error", error_msg)
        if hasattr(self, 'result_text'):
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"❌ {error_msg}")

    def create_split_layout(self):
        """Create standardized split layout"""
        self.main_paned = ttk.PanedWindow(self.frame, orient="horizontal")
        self.main_paned.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left panel
        self.left_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.left_frame, weight=1)
        
        # Right panel  
        self.right_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.right_frame, weight=1)

    def setup_city_input(self, parent_frame):
        """Setup standardized city input"""
        StyledLabel(parent_frame, text="Enter City:").pack(pady=10)
        self.city_entry = ttk.Entry(parent_frame)
        self.city_entry.pack()

    def setup_result_text(self, parent_frame, height=12, width=60):
        """Setup standardized result text widget"""
        self.result_text = StyledText(parent_frame, height=height, width=width)
        self.result_text.pack(pady=10)

class ChartHelper:
    """Helper class for chart generation to reduce duplication"""
    
    @staticmethod
    def create_chart_frame(parent):
        """Create standardized chart frame"""
        chart_frame = ttk.Frame(parent)
        chart_frame.pack(fill="both", expand=True, padx=5, pady=5)
        return chart_frame

    @staticmethod
    def clear_chart_area(chart_frame):
        """Clear chart display area"""
        for widget in chart_frame.winfo_children():
            widget.destroy()

    @staticmethod
    def show_chart_unavailable(chart_frame):
        """Show chart unavailable message"""
        ChartHelper.clear_chart_area(chart_frame)
        unavailable_label = StyledLabel(chart_frame, 
                                      text="Charts unavailable\n(matplotlib not installed)", 
                                      foreground="red")
        unavailable_label.pack(expand=True)

    @staticmethod
    def create_chart_placeholder(chart_frame, title="Chart Display Area", content="Charts will appear here when generated."):
        """Create a placeholder for the chart area"""
        placeholder_frame = ttk.LabelFrame(chart_frame, text=title)
        placeholder_frame.pack(fill="both", expand=True)
        
        placeholder_text = tk.Text(placeholder_frame, height=10, wrap="word",
                                 bg=COLOR_PALETTE["tab_bg"], fg=COLOR_PALETTE["tab_fg"])
        placeholder_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        placeholder_text.insert("1.0", content)
        placeholder_text.config(state="disabled")

    @staticmethod
    def embed_chart_in_frame(fig, chart_frame):
        """Embed matplotlib chart in tkinter frame with toolbar"""
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        toolbar = NavigationToolbar2Tk(canvas, chart_frame)
        toolbar.update()

    @staticmethod
    def create_line_chart(chart_frame, title, x_data, y_data, x_label="X", y_label="Y", 
                         color='#2E86AB', marker_color='#A23B72'):
        """Create standardized line chart"""
        if not CHARTS_AVAILABLE:
            ChartHelper.show_chart_unavailable(chart_frame)
            return

        ChartHelper.clear_chart_area(chart_frame)
        
        fig = Figure(figsize=(8, 5), dpi=100, facecolor='white')
        ax = fig.add_subplot(111)
        
        ax.plot(x_data, y_data, marker='o', linewidth=2, markersize=8, 
               color=color, markerfacecolor=marker_color, markeredgecolor='white', markeredgewidth=2)
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel(x_label, fontsize=12)
        ax.set_ylabel(y_label, fontsize=12)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_facecolor('#f8f9fa')
        
        # Add value annotations
        for i, value in enumerate(y_data):
            ax.annotate(f'{value}°' if 'temp' in y_label.lower() else f'{value}', 
                       (i, value), textcoords="offset points", 
                       xytext=(0,10), ha='center', fontsize=10, fontweight='bold')
        
        fig.tight_layout()
        ChartHelper.embed_chart_in_frame(fig, chart_frame)

    @staticmethod
    def create_bar_chart(chart_frame, title, x_data, y_data, colors=None, rotate_labels=False):
        """Create standardized bar chart"""
        if not CHARTS_AVAILABLE:
            ChartHelper.show_chart_unavailable(chart_frame)
            return

        ChartHelper.clear_chart_area(chart_frame)
        
        fig = Figure(figsize=(8, 5), dpi=100, facecolor='white')
        ax = fig.add_subplot(111)
        
        if colors is None:
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']
        
        bars = ax.bar(x_data, y_data, color=colors[:len(x_data)], alpha=0.8, 
                     edgecolor='white', linewidth=1.5)
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_ylabel('Values', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax.set_facecolor('#f8f9fa')
        
        # Add value labels on bars
        for bar, value in zip(bars, y_data):
            height = bar.get_height()
            ax.annotate(f'{value}', xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                       fontsize=10, fontweight='bold')
        
        if rotate_labels:
            ax.tick_params(axis='x', rotation=45)
            
        fig.tight_layout()
        ChartHelper.embed_chart_in_frame(fig, chart_frame)

    @staticmethod
    def create_histogram(chart_frame, title, data, bins=15, color='#3498db'):
        """Create standardized histogram"""
        if not CHARTS_AVAILABLE:
            ChartHelper.show_chart_unavailable(chart_frame)
            return

        ChartHelper.clear_chart_area(chart_frame)
        
        fig = Figure(figsize=(8, 5), dpi=100, facecolor='white')
        ax = fig.add_subplot(111)
        
        n, bins, patches = ax.hist(data, bins=bins, alpha=0.7, color=color, 
                                 edgecolor='white', linewidth=1.2)
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Value', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax.set_facecolor('#f8f9fa')
        
        # Add statistical info
        if CHARTS_AVAILABLE:
            mean_val = np.mean(data)
            ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, 
                      label=f'Mean: {mean_val:.1f}')
            ax.legend()
        
        fig.tight_layout()
        ChartHelper.embed_chart_in_frame(fig, chart_frame)

class ButtonHelper:
    """Helper for creating standardized button layouts"""
    
    @staticmethod
    def create_button_grid(parent, buttons_config, columns=4):
        """Create grid of buttons with consistent spacing
        
        buttons_config: list of tuples (style, text, command)
        """
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=5)
        
        for i, (style, text, command) in enumerate(buttons_config):
            row = i // columns
            col = i % columns
            StyledButton(button_frame, style, text=text, 
                        command=command).grid(row=row, column=col, padx=2, pady=2)
        
        return button_frame

    @staticmethod
    def create_main_button(parent, style, text, command):
        """Create standardized main action button"""
        return StyledButton(parent, style, text=text, command=command).pack(pady=5)

class WeatherFormatter:
    """Helper for consistent weather data formatting"""
    
    @staticmethod
    def format_weather_display(weather_data):
        """Standard weather display format"""
        weather_text = f"Weather in {weather_data.city}:\n"
        weather_text += "━" * 62 + "\n"
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
        
        return weather_text

    @staticmethod
    def check_weather_alerts(weather_data):
        """Standard weather alert checking"""
        temp = weather_data.temperature
        desc = weather_data.description.lower()
        
        if (temp > 35 and weather_data.unit == "metric") or \
           (temp > 95 and weather_data.unit == "imperial") or \
           "storm" in desc:
            return "⚠️ Weather Alert: Stay safe!"
        return ""

class CommonActions:
    """Common action methods used across tabs"""
    
    @staticmethod
    def create_alert_popup(parent, title, content):
        """Create standardized alert popup"""
        popup = tk.Toplevel(parent)
        popup.title(title)
        popup.geometry("400x300")
        popup.configure(bg=COLOR_PALETTE["background"])
        
        text_widget = StyledText(popup, height=12, width=50)
        text_widget.pack(padx=10, pady=10, fill="both", expand=True)
        text_widget.insert("1.0", content)
        text_widget.config(state="disabled")
        
        StyledButton(popup, "primary", text="Close", 
                    command=popup.destroy).pack(pady=10)

    @staticmethod
    def show_info_message(title, message):
        """Show standardized info message"""
        messagebox.showinfo(title, message)

    @staticmethod
    def show_warning_message(title, message):
        """Show standardized warning message"""
        messagebox.showwarning(title, message)
