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
    "text_on_button": "#FFFFFF",      # White text for buttons
    "text_on_button_black": "#000000", # Black text for buttons
    # New enhanced button colors for better UX
    "button_accent": "#FFD700",       # Gold - for accent actions
    "button_success": "#98FB98",      # Pale green - for positive actions
    "button_warning_light": "#FFE4B5" # Moccasin - for warning actions
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
