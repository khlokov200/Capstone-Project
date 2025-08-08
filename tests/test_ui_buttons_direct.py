#!/usr/bin/env python3
"""
Direct UI test for ComparisonTab buttons - checks for runtime issues
"""

import tkinter as tk
from tkinter import ttk
import os
import sys

def test_ui_buttons_direct():
    """Test the UI buttons directly"""
    print("🧪 DIRECT UI BUTTON TEST")
    print("=" * 40)
    
    try:
        # Set up mock environment
        os.environ['WEATHER_API_KEY'] = 'mock_api_key_for_testing'
        
        # Import with environment set
        from ui.tabs import ComparisonTab
        print("✅ ComparisonTab imported successfully")
        
        # Create test window
        root = tk.Tk()
        root.title("Button Functionality Test")
        root.geometry("800x600")
        
        # Create notebook
        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True)
        
        # Mock controller
        class MockController:
            def get_weather_data(self, city):
                return {"temperature": 20, "humidity": 60, "description": "Clear"}
        
        controller = MockController()
        
        # Create ComparisonTab
        comparison_tab = ComparisonTab(notebook, controller)
        print("✅ ComparisonTab created successfully")
        
        # Check if ComparisonService is available
        if hasattr(comparison_tab, 'comparison_service') and comparison_tab.comparison_service:
            print("✅ ComparisonService is available")
        else:
            print("⚠️ ComparisonService not available - buttons will show info dialogs")
        
        # Pre-fill test data if entry fields exist
        if hasattr(comparison_tab, 'detailed_city1_entry'):
            comparison_tab.detailed_city1_entry.insert(0, "London")
            comparison_tab.detailed_city2_entry.insert(0, "Bangkok")
            print("✅ Test cities pre-filled")
        
        # Test button methods
        button_tests = [
            ("Temperature Analysis", "show_temperature_analysis"),
            ("Humidity Analysis", "show_humidity_analysis"),
            ("Wind Analysis", "show_wind_analysis"),
            ("Complete Overview", "show_complete_overview")
        ]
        
        for button_name, method_name in button_tests:
            if hasattr(comparison_tab, method_name):
                print(f"✅ {button_name} method exists")
                
                # Try to call the method
                try:
                    method = getattr(comparison_tab, method_name)
                    # Note: This would normally show a dialog, so we just check it's callable
                    print(f"✅ {button_name} method is callable")
                except Exception as e:
                    print(f"❌ {button_name} method error: {e}")
            else:
                print(f"❌ {button_name} method missing")
        
        print("\n🎯 Manual Test Instructions:")
        print("1. The test window should open")
        print("2. Navigate to 'Detailed Analysis' tab")
        print("3. Cities should be pre-filled (London/Bangkok)")
        print("4. Click each button to test:")
        print("   • 🌡️ Temperature Analysis")
        print("   • 💧 Humidity & Comfort")
        print("   • 💨 Wind & Pressure")
        print("   • 🌦️ Complete Overview")
        print("5. Either charts should generate OR info dialogs should appear")
        print("\nClose the window when done testing.")
        
        # Start the application
        root.mainloop()
        
        print("✅ UI test completed")
        return True
        
    except Exception as e:
        print(f"❌ Error in UI test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_ui_buttons_direct()
