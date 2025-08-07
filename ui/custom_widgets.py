"""
Custom widgets for the UI
"""
import tkinter as tk
from tkinter import ttk

# Import the color palette
from ui.config import COLOR_PALETTE

class StyledButton(ttk.Button):
    """A styled button widget"""
    def __init__(self, parent, style_prefix="primary", **kwargs):
        # Create the style for the button if it doesn't exist
        style_name = f"{style_prefix}.TButton"
        
        # Initialize the parent class
        super().__init__(parent, style=style_name, **kwargs)

class StyledLabel(ttk.Label):
    """A styled label widget"""
    def __init__(self, parent, **kwargs):
        # Initialize the parent class
        super().__init__(parent, **kwargs)

class StyledText(tk.Text):
    """A styled text widget"""
    def __init__(self, parent, height=10, width=60, **kwargs):
        # Initialize the parent class with custom styling
        super().__init__(parent, height=height, width=width,
                         bg=COLOR_PALETTE["tab_bg"],
                         fg=COLOR_PALETTE["tab_fg"],
                         wrap="word", **kwargs)
        
        # Add a scrollbar to the text widget
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=scrollbar.set)
        
        # Pack the text widget and scrollbar together
        self.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

def setup_style():
    """Set up the styles for the application"""
    style = ttk.Style()
    
    # Configure common styles
    style.configure("TFrame", background=COLOR_PALETTE["background"])
    style.configure("TLabel", background=COLOR_PALETTE["background"], foreground=COLOR_PALETTE["text"])
    style.configure("TButton", background=COLOR_PALETTE["primary"], foreground=COLOR_PALETTE["text"])
    
    # Configure special styles
    style.configure("primary.TButton", background=COLOR_PALETTE["primary"], foreground="white")
    style.configure("accent.TButton", background=COLOR_PALETTE["accent"], foreground="white")
    style.configure("primary_black.TButton", background=COLOR_PALETTE["primary"], foreground="black")
    style.configure("accent_black.TButton", background=COLOR_PALETTE["accent"], foreground="black")
    style.configure("info_black.TButton", background="#5bc0de", foreground="black")
    style.configure("success_black.TButton", background="#5cb85c", foreground="black")
    style.configure("warning_black.TButton", background="#f0ad4e", foreground="black")
    style.configure("cool_black.TButton", background="#5bc0de", foreground="black")
    
    # Title style
    style.configure("Title.TLabel", font=("Helvetica", 24, "bold"), 
                   background=COLOR_PALETTE["background"], foreground=COLOR_PALETTE["primary"])

def create_gradient_background(canvas, color1, color2, width, height):
    """Create a gradient background on a canvas"""
    # Create gradient
    for i in range(height):
        # Calculate color based on position
        r1, g1, b1 = [int(color1[j:j+2], 16) for j in range(1, 7, 2)]
        r2, g2, b2 = [int(color2[j:j+2], 16) for j in range(1, 7, 2)]
        
        # Linear interpolation between colors
        r = r1 + (r2 - r1) * i / height
        g = g1 + (g2 - g1) * i / height
        b = b1 + (b2 - b1) * i / height
        
        # Convert to hex
        color = f'#{int(r):02x}{int(g):02x}{int(b):02x}'
        
        # Draw line with calculated color
        canvas.create_line(0, i, width, i, fill=color)
    
    return canvas
