"""
Test script to verify button styling and font legibility across all tabs
"""
import sys
import os
import tkinter as tk
from tkinter import ttk

# Add the project path to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = current_dir
sys.path.append(project_root)

# Import UI components
from ui.components import StyledButton
from ui.constants import COLOR_PALETTE

def test_button_styling():
    """
    Create a test window displaying all button styles to verify text legibility
    """
    root = tk.Tk()
    root.title("Button Style Test")
    root.geometry("800x600")
    root.configure(bg=COLOR_PALETTE["background"])
    
    title_label = tk.Label(root, text="Button Style Test - Verify Dark Text on All Buttons",
                         font=("Arial", 16, "bold"), 
                         bg=COLOR_PALETTE["background"],
                         fg="white")
    title_label.pack(pady=20)
    
    # Create a frame for regular styles
    regular_frame = ttk.LabelFrame(root, text="Regular Styles (Should all use dark text)")
    regular_frame.pack(pady=10, padx=10, fill="both")
    
    # Regular styles with dark text
    styles = ["primary_black", "info_black", "accent_black", "warning_black", 
              "success_black", "cool_black"]
    
    for i, style in enumerate(styles):
        button = StyledButton(regular_frame, style, text=f"{style} Button")
        button.grid(row=i//3, column=i%3, padx=10, pady=10)
    
    # Create a frame for helper function styles
    helper_frame = ttk.LabelFrame(root, text="Helper-Created Buttons (Should convert to dark text)")
    helper_frame.pack(pady=10, padx=10, fill="both")
    
    # Import helper after creating the above UI elements
    from ui.tab_helpers import ButtonHelper
    
    # Test buttons using ButtonHelper
    button_configs = [
        ("primary", "Primary Button", lambda: None),
        ("info", "Info Button", lambda: None),
        ("accent", "Accent Button", lambda: None),
        ("warning", "Warning Button", lambda: None)
    ]
    
    button_grid = ButtonHelper.create_button_grid(helper_frame, button_configs, columns=2)
    
    # Add a main action button
    ButtonHelper.create_main_button(helper_frame, "success", "Main Action Button", lambda: None)
    
    # Instructions
    instructions = tk.Text(root, height=4, width=60, 
                         bg=COLOR_PALETTE["tab_bg"], 
                         fg=COLOR_PALETTE["tab_fg"])
    instructions.pack(pady=10)
    instructions.insert("1.0", 
                      "All buttons should display with dark, legible text.\n"
                      "If any buttons have white or light text that is hard to read,\n"
                      "further updates may be needed.")
    instructions.config(state="disabled")
    
    # Add a quit button
    StyledButton(root, "primary_black", text="Close Test", 
               command=root.destroy).pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    test_button_styling()
