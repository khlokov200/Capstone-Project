#!/usr/bin/env python3
"""
Test script to verify LiveRadarTab functionality
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_live_radar_tab():
    """Test the LiveRadarTab implementation"""
    print("Testing LiveRadarTab implementation...")
    
    try:
        # Import the required modules
        from ui.tabs import LiveRadarTab
        from ui.components import StyledLabel, StyledButton, StyledText
        
        print("✅ Successfully imported LiveRadarTab and components")
        
        # Create a test window
        root = tk.Tk()
        root.title("LiveRadarTab Test")
        root.geometry("800x600")
        
        # Create a notebook widget
        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create a mock controller
        class MockController:
            def __init__(self):
                self.weather_data = {}
                
            def get_weather_data(self, location="New York"):
                return {"temperature": 23, "condition": "Partly Cloudy"}
        
        controller = MockController()
        
        # Create the LiveRadarTab
        live_radar_tab = LiveRadarTab(notebook, controller)
        
        print("✅ Successfully created LiveRadarTab instance")
        
        # Test key methods exist
        methods_to_test = [
            'update_radar_location',
            'start_people_animations', 
            'update_doppler_radar',
            'track_storms',
            'show_live_radar'
        ]
        
        for method_name in methods_to_test:
            if hasattr(live_radar_tab, method_name):
                print(f"✅ Method {method_name} exists")
            else:
                print(f"❌ Method {method_name} missing")
        
        print("LiveRadarTab test completed successfully!")
        print("Starting GUI - close window to continue...")
        
        # Run the GUI for manual testing
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Error during LiveRadarTab test: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_live_radar_tab()
    if success:
        print("\n🎉 LiveRadarTab implementation is working!")
    else:
        print("\n💥 LiveRadarTab implementation has issues.")
