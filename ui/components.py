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
        self._style_type = style_type
        self._palette = kwargs.pop('palette', COLOR_PALETTE)
        self._apply_style(kwargs)
        super().__init__(master, *args, **kwargs)

    def _apply_style(self, kwargs):
        style_type = self._style_type
        palette = self._palette
        if style_type == "accent":
            kwargs.setdefault("bg", palette["accent"])
            kwargs.setdefault("fg", palette["text_on_button"])
            kwargs.setdefault("activebackground", "#FF8F00")
            kwargs.setdefault("activeforeground", palette["text_on_button"])
        elif style_type == "primary":
            kwargs.setdefault("bg", palette["button_primary"])
            kwargs.setdefault("fg", palette["text_on_button"])
            kwargs.setdefault("activebackground", "#45A049")
            kwargs.setdefault("activeforeground", palette["text_on_button"])
        elif style_type == "cool":
            kwargs.setdefault("bg", palette["button_secondary"])
            kwargs.setdefault("fg", palette["text_on_button"])
            kwargs.setdefault("activebackground", "#1976D2")
            kwargs.setdefault("activeforeground", palette["text_on_button"])
        elif style_type == "heat":
            kwargs.setdefault("bg", palette["button_warning"])
            kwargs.setdefault("fg", palette["text_on_button"])
            kwargs.setdefault("activebackground", "#D84315")
            kwargs.setdefault("activeforeground", palette["text_on_button"])
        elif style_type == "info":
            kwargs.setdefault("bg", palette["button_info"])
            kwargs.setdefault("fg", palette["text_on_button"])
            kwargs.setdefault("activebackground", "#0097A7")
            kwargs.setdefault("activeforeground", palette["text_on_button"])
        elif style_type == "primary_black":
            kwargs.setdefault("bg", "#90EE90")
            kwargs.setdefault("fg", palette["text_on_button_black"])
            kwargs.setdefault("activebackground", "#7FDD7F")
            kwargs.setdefault("activeforeground", palette["text_on_button_black"])
        elif style_type == "cool_black":
            kwargs.setdefault("bg", "#87CEEB")
            kwargs.setdefault("fg", palette["text_on_button_black"])
            kwargs.setdefault("activebackground", "#70C1E8")
            kwargs.setdefault("activeforeground", palette["text_on_button_black"])
        elif style_type == "info_black":
            kwargs.setdefault("bg", "#40E0D0")
            kwargs.setdefault("fg", palette["text_on_button_black"])
            kwargs.setdefault("activebackground", "#32C8BC")
            kwargs.setdefault("activeforeground", palette["text_on_button_black"])
        elif style_type == "accent_black":
            kwargs.setdefault("bg", palette["button_accent"])
            kwargs.setdefault("fg", palette["text_on_button_black"])
            kwargs.setdefault("activebackground", "#E6C200")
            kwargs.setdefault("activeforeground", palette["text_on_button_black"])
        elif style_type == "success_black":
            kwargs.setdefault("bg", palette["button_success"])
            kwargs.setdefault("fg", palette["text_on_button_black"])
            kwargs.setdefault("activebackground", "#8AE88A")
            kwargs.setdefault("activeforeground", palette["text_on_button_black"])
        elif style_type == "warning_black":
            kwargs.setdefault("bg", palette["button_warning_light"])
            kwargs.setdefault("fg", palette["text_on_button_black"])
            kwargs.setdefault("activebackground", "#F0D098")
            kwargs.setdefault("activeforeground", palette["text_on_button_black"])
        else:
            kwargs.setdefault("bg", palette["neutral"])
            kwargs.setdefault("fg", palette["text_on_button"])
            kwargs.setdefault("activebackground", "#757575")
            kwargs.setdefault("activeforeground", palette["text_on_button"])
        kwargs.setdefault("relief", "flat")
        kwargs.setdefault("borderwidth", 1)
        kwargs.setdefault("font", ("Arial", 10, "bold"))
        kwargs.setdefault("cursor", "hand2")

    def update_theme(self, palette):
        self._palette = palette
        # Remove all explicit color settings before reapplying
        for opt in ["bg", "fg", "activebackground", "activeforeground"]:
            self.config({opt: ''})
        self._apply_style(self.config())
        # Explicitly set all color options again
        self.config(bg=self.cget("bg"), fg=self.cget("fg"), activebackground=self.cget("activebackground"), activeforeground=self.cget("activeforeground"))


class StyledText(tk.Text):
    """Styled text widget with consistent theming"""
    
    def __init__(self, master, *args, **kwargs):
        self._palette = kwargs.pop('palette', COLOR_PALETTE)
        kwargs.setdefault("bg", self._palette["tab_bg"])
        kwargs.setdefault("fg", self._palette["tab_fg"])
        kwargs.setdefault("height", 10)
        kwargs.setdefault("width", 60)
        super().__init__(master, *args, **kwargs)

    def update_theme(self, palette):
        self._palette = palette
        self.config(bg=self._palette["tab_bg"], fg=self._palette["tab_fg"])


class StyledLabel(ttk.Label):
    """Styled label with consistent theming"""
    
    def __init__(self, master, *args, **kwargs):
        self._palette = kwargs.pop('palette', COLOR_PALETTE)
        kwargs.setdefault("background", self._palette["background"])
        kwargs.setdefault("foreground", self._palette["tab_fg"])
        super().__init__(master, *args, **kwargs)

    def update_theme(self, palette):
        self._palette = palette
        self.config(background=self._palette["background"], foreground=self._palette["tab_fg"])
