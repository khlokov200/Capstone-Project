"""
Reusable UI Components
"""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
from .constants import COLOR_PALETTE


class AnimatedLabel(tk.Label):
    """Label widget that displays animated GIFs"""
    
    def __init__(self, master, gif_path, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        try:
            self.gif = Image.open(gif_path)
            self.frames = [ImageTk.PhotoImage(frame.copy().convert('RGBA')) 
                          for frame in ImageSequence.Iterator(self.gif)]
            self.idx = 0
            self.after(0, self.animate)
        except Exception:
            # Fallback if GIF loading fails
            self.frames = []

    def animate(self):
        """Animate the GIF frames"""
        if self.frames:
            self.config(image=self.frames[self.idx])
            self.idx = (self.idx + 1) % len(self.frames)
            self.after(100, self.animate)


class StyledButton(tk.Button):
    """Styled button with consistent theming"""
    
    def __init__(self, master, style_type="default", *args, **kwargs):
        # Apply default styling based on type - ALL BUTTONS NOW USE DARK TEXT
        if style_type == "accent":
            kwargs.setdefault("bg", COLOR_PALETTE["accent"])
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button_black"])  # Dark text
            kwargs.setdefault("activebackground", "#FF8F00")  # Darker orange when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button_black"])
        elif style_type == "primary":
            kwargs.setdefault("bg", COLOR_PALETTE["button_primary"])
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button_black"])  # Dark text
            kwargs.setdefault("activebackground", "#45A049")  # Darker green when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button_black"])
        elif style_type == "secondary":
            kwargs.setdefault("bg", COLOR_PALETTE["button_secondary"])
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button_black"])  # Dark text
            kwargs.setdefault("activebackground", "#1976D2")  # Darker blue when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button_black"])
        elif style_type == "success":
            kwargs.setdefault("bg", "#90EE90")  # Light green background for better contrast
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button_black"])  # Dark text
            kwargs.setdefault("activebackground", "#7FDD7F")  # Slightly darker when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button_black"])
        elif style_type == "danger":
            kwargs.setdefault("bg", "#FFB6C1")  # Light pink background for better contrast
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button_black"])  # Dark text
            kwargs.setdefault("activebackground", "#FFA0B4")  # Slightly darker when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button_black"])
        elif style_type == "warning":
            kwargs.setdefault("bg", "#FFE4B5")  # Light orange background for better contrast
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button_black"])  # Dark text
            kwargs.setdefault("activebackground", "#FFDB9A")  # Slightly darker when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button_black"])
        elif style_type == "info":
            kwargs.setdefault("bg", "#87CEEB")  # Light blue background for better contrast
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button_black"])  # Dark text
            kwargs.setdefault("activebackground", "#70C1E8")  # Slightly darker when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button_black"])
        elif style_type == "cool":
            kwargs.setdefault("bg", COLOR_PALETTE["button_secondary"])
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button_black"])  # Dark text
            kwargs.setdefault("activebackground", "#1976D2")  # Darker blue when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button_black"])
        elif style_type == "heat":
            kwargs.setdefault("bg", "#FFB6C1")  # Light pink background for better contrast
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button_black"])  # Dark text
            kwargs.setdefault("activebackground", "#FFA0B4")  # Slightly darker when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button_black"])
        elif style_type == "primary_black":
            kwargs.setdefault("bg", "#90EE90")  # Light green background
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button_black"])
            kwargs.setdefault("activebackground", "#7FDD7F")  # Slightly darker when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button_black"])
        elif style_type == "cool_black":
            kwargs.setdefault("bg", "#87CEEB")  # Sky blue background
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button_black"])
            kwargs.setdefault("activebackground", "#70C1E8")  # Slightly darker when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button_black"])
        elif style_type == "info_black":
            kwargs.setdefault("bg", "#40E0D0")  # Turquoise background
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button_black"])
            kwargs.setdefault("activebackground", "#32C8BC")  # Slightly darker when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button_black"])
        elif style_type == "accent_black":
            kwargs.setdefault("bg", COLOR_PALETTE["button_accent"])  # Gold background
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button_black"])
            kwargs.setdefault("activebackground", "#E6C200")  # Slightly darker when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button_black"])
        elif style_type == "success_black":
            kwargs.setdefault("bg", COLOR_PALETTE["button_success"])  # Pale green background
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button_black"])
            kwargs.setdefault("activebackground", "#8AE88A")  # Slightly darker when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button_black"])
        elif style_type == "warning_black":
            kwargs.setdefault("bg", COLOR_PALETTE["button_warning_light"])  # Moccasin background
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button_black"])
            kwargs.setdefault("activebackground", "#F0D098")  # Slightly darker when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button_black"])
        elif style_type == "danger_black":
            kwargs.setdefault("bg", "#FFB6C1")  # Light pink background
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button_black"])
            kwargs.setdefault("activebackground", "#FFA0B4")  # Slightly darker when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button_black"])
        else:
            kwargs.setdefault("bg", "#F0F0F0")  # Light gray for better contrast with dark text
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button_black"])  # Dark text
            kwargs.setdefault("activebackground", "#E0E0E0")  # Slightly darker when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button_black"])
        
        # Add common button styling for better appearance
        kwargs.setdefault("relief", "flat")
        kwargs.setdefault("borderwidth", 1)
        kwargs.setdefault("font", ("Arial", 9, "bold"))
        kwargs.setdefault("width", 26)  # Further increased width for full wording
        kwargs.setdefault("cursor", "hand2")
        super().__init__(master, *args, **kwargs)


class StyledText(tk.Text):
    """Styled text widget with consistent theming"""
    
    def __init__(self, master, *args, **kwargs):
        kwargs.setdefault("bg", COLOR_PALETTE["tab_bg"])
        kwargs.setdefault("fg", COLOR_PALETTE["tab_fg"])
        kwargs.setdefault("height", 10)
        kwargs.setdefault("width", 60)
        super().__init__(master, *args, **kwargs)


class StyledLabel(ttk.Label):
    """Styled label with consistent theming"""
    
    def __init__(self, master, *args, **kwargs):
        kwargs.setdefault("background", COLOR_PALETTE["background"])
        kwargs.setdefault("foreground", COLOR_PALETTE["tab_fg"])
        super().__init__(master, *args, **kwargs)
