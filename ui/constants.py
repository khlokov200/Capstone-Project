"""
UI Constants and Configuration
"""


# Light and Dark Color Palettes
LIGHT_PALETTE = {
    "background": "#f5f5f5",
    "tab_bg": "#e0e0e0",
    "tab_fg": "#23272e",
    "accent": "#2196f3",
    "cool": "#2196f3",
    "heat": "#f44336",
    "neutral": "#9e9e9e",
    "button_primary": "#1976D2",
    "button_secondary": "#4CAF50",
    "button_warning": "#FF9800",
    "button_info": "#00BCD4",
    "button_dark": "#212121",
    "text_on_button": "#23272e",
    "text_on_button_black": "#000000",
    "button_accent": "#FFD700",
    "button_success": "#388E3C",
    "button_warning_light": "#FFF8E1",
    "whitespace_bg": "#f0f4f8"
}

DARK_PALETTE = {
    "background": "#23272e",
    "tab_bg": "#2c313c",
    "tab_fg": "#fff",
    "accent": "#ff9800",
    "cool": "#2196f3",
    "heat": "#f44336",
    "neutral": "#9e9e9e",
    "button_primary": "#4CAF50",
    "button_secondary": "#2196F3",
    "button_warning": "#FF5722",
    "button_info": "#00BCD4",
    "button_dark": "#212121",
    "text_on_button": "#FFFFFF",
    "text_on_button_black": "#000000",
    "button_accent": "#FFD700",
    "button_success": "#98FB98",
    "button_warning_light": "#FFE4B5",
    "whitespace_bg": "#262a32"
}

def get_palette(theme: str = "dark"):
    if theme == "light":
        return LIGHT_PALETTE
    return DARK_PALETTE

COLOR_PALETTE = DARK_PALETTE

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
