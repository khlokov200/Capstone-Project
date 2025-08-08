#!/usr/bin/env python
"""
Test script to verify ComparisonTab initialization and city loading
"""
import os
import sys
import tkinter as tk
from tkinter import ttk

# Add parent directory to path to import ui modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import required modules
try:
    from ui.tabs import ComparisonTab
except ImportError as e:
    print(f"Error importing: {e}")
    sys.exit(1)

class MockController:
    """Mock controller to pass to ComparisonTab"""
    def __init__(self):
        self.api_key = "demo_key"
        
    def toggle_graph_mode(self):
        print("Toggle graph mode called")
        
    def fetch_weather(self, city):
        print(f"Fetch weather called for {city}")
        return {"temp": 25, "description": "Sunny"}

def main():
    """Create a simple tkinter window and test the ComparisonTab"""
    # Create main window
    root = tk.Tk()
    root.title("ComparisonTab Test")
    root.geometry("800x600")
    
    # Create notebook to hold tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)
    
    # Create controller
    controller = MockController()
    
    print("Creating ComparisonTab...")
    # Create ComparisonTab
    comparison_tab = ComparisonTab(notebook, controller)
    
    print("Setup complete. Running main loop...")
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
