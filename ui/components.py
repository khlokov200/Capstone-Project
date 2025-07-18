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
        # Apply default styling based on type
        if style_type == "accent":
            kwargs.setdefault("bg", COLOR_PALETTE["accent"])
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button"])
            kwargs.setdefault("activebackground", "#FF8F00")  # Darker orange when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button"])
        elif style_type == "primary":
            kwargs.setdefault("bg", COLOR_PALETTE["button_primary"])
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button"])
            kwargs.setdefault("activebackground", "#45A049")  # Darker green when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button"])
        elif style_type == "cool":
            kwargs.setdefault("bg", COLOR_PALETTE["button_secondary"])
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button"])
            kwargs.setdefault("activebackground", "#1976D2")  # Darker blue when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button"])
        elif style_type == "heat":
            kwargs.setdefault("bg", COLOR_PALETTE["button_warning"])
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button"])
            kwargs.setdefault("activebackground", "#D84315")  # Darker red when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button"])
        elif style_type == "info":
            kwargs.setdefault("bg", COLOR_PALETTE["button_info"])
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button"])
            kwargs.setdefault("activebackground", "#0097A7")  # Darker teal when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button"])
        elif style_type == "dark":
            kwargs.setdefault("bg", COLOR_PALETTE["button_dark"])
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button"])
            kwargs.setdefault("activebackground", "#424242")  # Lighter gray when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button"])
        else:
            kwargs.setdefault("bg", COLOR_PALETTE["neutral"])
            kwargs.setdefault("fg", COLOR_PALETTE["text_on_button"])
            kwargs.setdefault("activebackground", "#757575")  # Darker gray when pressed
            kwargs.setdefault("activeforeground", COLOR_PALETTE["text_on_button"])
        
        # Add common button styling for better appearance
        kwargs.setdefault("relief", "flat")
        kwargs.setdefault("borderwidth", 1)
        kwargs.setdefault("font", ("Arial", 10, "bold"))
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
