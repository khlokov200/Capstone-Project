#!/usr/bin/env python3
"""
Quick test script for City Comparison Chart functionality
"""
import os
import sys
import tkinter as tk
from tkinter import ttk

print("🧪 Testing City Comparison Charts")
print("=" * 40)

try:
    # Import required modules
    print("1. Testing imports...")
    from ui.main_window import MainWindow
    from controllers.weather_controller import WeatherController
    print("   ✅ All imports successful")
    
    print("\n2. Creating test window...")
    # Create root window
    root = tk.Tk()
    root.title("City Comparison Charts Test")
    root.geometry("1200x800")
    
    # Set test API key
    os.environ['WEATHER_API_KEY'] = 'test_key_for_validation'
    
    # Create controller
    controller = WeatherController(os.environ['WEATHER_API_KEY'])
    
    # Create notebook for tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # Import ComparisonTab class
    from ui.tabs import ComparisonTab
    
    # Create comparison tab
    print("3. Creating ComparisonTab...")
    comparison_tab = ComparisonTab(notebook, controller)
    print("   ✅ ComparisonTab created successfully")
    
    # Pre-fill cities for testing
    comparison_tab.city1_entry.insert(0, "New York")
    comparison_tab.city2_entry.insert(0, "London")
    
    print("\n✅ Test setup successful!")
    print("\n🚀 Running test window - you should see the city comparison tab with chart buttons")
    print("   Click on any chart button to test the visualization features")
    
    root.mainloop()
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
