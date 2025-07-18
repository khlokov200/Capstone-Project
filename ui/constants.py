"""
UI Constants and Configuration
"""

# Color Palette
COLOR_PALETTE = {
    "background": "#23272e",
    "tab_bg": "#2c313c",
    "tab_fg": "#fff",
    "accent": "#ff9800",
    "cool": "#2196f3",
    "heat": "#f44336",
    "neutral": "#9e9e9e",
    # New button colors with better contrast
    "button_primary": "#4CAF50",      # Green - better contrast with white text
    "button_secondary": "#2196F3",    # Blue - good contrast
    "button_warning": "#FF5722",      # Orange-red - good contrast
    "button_info": "#00BCD4",         # Teal - good contrast
    "button_dark": "#212121",         # Dark gray - good contrast
    "text_on_button": "#FFFFFF"       # White text for buttons
}

# UI Configuration
UI_CONFIG = {
    "window_title": "Weather Dashboard Capstone",
    "window_geometry": "900x700",
    "text_widget_config": {
        "height": 10,
        "width": 60,
        "bg": COLOR_PALETTE["tab_bg"],
        "fg": COLOR_PALETTE["tab_fg"]
    },
    "entry_widget_config": {
        "width": 30
    }
}

# Temperature Units
TEMPERATURE_UNITS = {
    "metric": {
        "label": "°C",
        "name": "Celsius",
        "api_param": "metric"
    },
    "imperial": {
        "label": "°F", 
        "name": "Fahrenheit",
        "api_param": "imperial"
    }
}
