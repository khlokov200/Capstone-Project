#!/usr/bin/env python3
"""
Comprehensive test script to verify all button functions work correctly
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.tabs import *

def test_all_button_functions():
    """Test all button functions by creating instances and calling methods"""
    
    print("🧪 Testing all button functions...")
    
    # Create a temporary root window for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    try:
        # Create a notebook for tabs
        notebook = ttk.Notebook(root)
        
        # Mock controller
        class MockController:
            def toggle_graph_mode(self):
                print("✅ toggle_graph_mode")
        
        controller = MockController()
        
        # Test all tab classes and their button functions
        tab_classes = [
            ("WeatherTab", WeatherTab),
            ("LiveRadarTab", LiveRadarTab),
            ("ForecastTab", ForecastTab),
            ("FiveDayForecastTab", FiveDayForecastTab),
            ("ComparisonTab", ComparisonTab),
            ("JournalTab", JournalTab),
            ("HealthTab", HealthTab),
        ]
        
        test_results = {}
        
        for tab_name, tab_class in tab_classes:
            print(f"\n🔍 Testing {tab_name}...")
            
            try:
                # Create tab instance
                tab_instance = tab_class(notebook, controller)
                
                # Get all callable methods (button functions)
                methods = [method for method in dir(tab_instance) 
                          if callable(getattr(tab_instance, method)) 
                          and not method.startswith('_')
                          and method != 'controller']
                
                tab_results = {}
                
                for method_name in methods:
                    try:
                        method = getattr(tab_instance, method_name)
                        
                        # Try to call the method (many expect no arguments)
                        if method_name in ['__init__']:
                            continue  # Skip constructor
                            
                        method()
                        tab_results[method_name] = "✅ PASS"
                        print(f"  ✅ {method_name}")
                        
                    except Exception as e:
                        tab_results[method_name] = f"❌ FAIL: {str(e)}"
                        print(f"  ❌ {method_name}: {str(e)}")
                
                test_results[tab_name] = tab_results
                print(f"✅ {tab_name} completed")
                
            except Exception as e:
                test_results[tab_name] = {"ERROR": f"Failed to create tab: {str(e)}"}
                print(f"❌ {tab_name} failed to create: {str(e)}")
        
        # Print summary
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        
        total_tests = 0
        total_passed = 0
        
        for tab_name, results in test_results.items():
            if isinstance(results, dict) and "ERROR" not in results:
                passed = sum(1 for result in results.values() if result.startswith("✅"))
                total = len(results)
                total_tests += total
                total_passed += passed
                
                print(f"\n{tab_name}: {passed}/{total} functions working")
                
                # Show failed functions
                failed = [name for name, result in results.items() if result.startswith("❌")]
                if failed:
                    print(f"  Failed: {', '.join(failed)}")
            else:
                print(f"\n{tab_name}: FAILED TO CREATE")
        
        print(f"\n🎯 OVERALL: {total_passed}/{total_tests} button functions working")
        print(f"Success rate: {(total_passed/total_tests*100):.1f}%")
        
        if total_passed == total_tests:
            print("🎉 All button functions are working correctly!")
        else:
            print("⚠️ Some button functions need attention")
        
    finally:
        root.destroy()

if __name__ == "__main__":
    test_all_button_functions()
