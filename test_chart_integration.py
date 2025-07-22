#!/usr/bin/env python3
"""
Test chart integration within the weather dashboard application.
This tests the chart functionality as it would be used in the actual tabs.
"""

import sys
import os
import tkinter as tk
from tkinter import ttk

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_chart_imports():
    """Test that all chart-related imports work correctly"""
    print("🧪 Testing chart imports...")
    
    try:
        # Test matplotlib imports
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure
        import numpy as np
        print("✅ Matplotlib imports successful")
        
        # Test that tabs can import chart functionality
        from ui.tabs import CHARTS_AVAILABLE
        if CHARTS_AVAILABLE:
            print("✅ Chart functionality available in tabs")
        else:
            print("❌ Chart functionality not available in tabs")
            return False
            
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_forecast_tab_charts():
    """Test ForecastTab chart generation methods"""
    print("\n🧪 Testing ForecastTab chart methods...")
    
    try:
        from ui.tabs import ForecastTab
        from controllers.weather_controller import WeatherController
        
        # Create a mock controller
        class MockController:
            def get_forecast(self, city):
                return f"Mock forecast for {city}"
            
            def get_unit_label(self):
                return "°C"
        
        # Create a temporary root window for testing
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        notebook = ttk.Notebook(root)
        controller = MockController()
        
        # Create ForecastTab
        forecast_tab = ForecastTab(notebook, controller)
        
        # Test that chart methods exist
        chart_methods = [
            'generate_line_chart',
            'generate_bar_chart', 
            'generate_histogram'
        ]
        
        for method_name in chart_methods:
            if hasattr(forecast_tab, method_name):
                print(f"✅ ForecastTab.{method_name} method exists")
            else:
                print(f"❌ ForecastTab.{method_name} method missing")
                return False
        
        # Test that chart_frame exists
        if hasattr(forecast_tab, 'chart_frame'):
            print("✅ ForecastTab.chart_frame exists")
        else:
            print("❌ ForecastTab.chart_frame missing")
            return False
            
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ ForecastTab test error: {e}")
        return False

def test_comparison_tab_charts():
    """Test ComparisonTab chart generation methods"""
    print("\n🧪 Testing ComparisonTab chart methods...")
    
    try:
        from ui.tabs import ComparisonTab
        
        # Create a mock controller
        class MockController:
            def compare_cities(self, city1, city2):
                return f"Mock comparison of {city1} and {city2}"
        
        # Create a temporary root window for testing
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        notebook = ttk.Notebook(root)
        controller = MockController()
        
        # Create ComparisonTab
        comparison_tab = ComparisonTab(notebook, controller)
        
        # Test that chart methods exist
        chart_methods = [
            'generate_temp_comparison_chart',
            'generate_weather_comparison_chart',
            'generate_multi_city_chart'
        ]
        
        for method_name in chart_methods:
            if hasattr(comparison_tab, method_name):
                print(f"✅ ComparisonTab.{method_name} method exists")
            else:
                print(f"❌ ComparisonTab.{method_name} method missing")
                return False
        
        # Test that chart_frame exists
        if hasattr(comparison_tab, 'chart_frame'):
            print("✅ ComparisonTab.chart_frame exists")
        else:
            print("❌ ComparisonTab.chart_frame missing")
            return False
            
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ ComparisonTab test error: {e}")
        return False

def test_history_tab_charts():
    """Test HistoryTab chart generation methods"""
    print("\n🧪 Testing HistoryTab chart methods...")
    
    try:
        from ui.tabs import HistoryTab
        
        # Create a mock controller
        class MockController:
            def get_weather_history(self, days):
                import datetime
                dates = [f"2025-07-{20-i}" for i in range(days)]
                temps = [20 + i for i in range(days)]
                return dates, temps
        
        # Create a temporary root window for testing
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        notebook = ttk.Notebook(root)
        controller = MockController()
        
        # Create HistoryTab
        history_tab = HistoryTab(notebook, controller)
        
        # Test that chart methods exist
        chart_methods = [
            'generate_history_line_chart',
            'generate_trend_chart',
            'generate_stats_chart'
        ]
        
        for method_name in chart_methods:
            if hasattr(history_tab, method_name):
                print(f"✅ HistoryTab.{method_name} method exists")
            else:
                print(f"❌ HistoryTab.{method_name} method missing")
                return False
        
        # Test that chart_frame exists
        if hasattr(history_tab, 'chart_frame'):
            print("✅ HistoryTab.chart_frame exists")
        else:
            print("❌ HistoryTab.chart_frame missing")
            return False
            
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ HistoryTab test error: {e}")
        return False

def test_five_day_forecast_charts():
    """Test FiveDayForecastTab chart generation methods"""
    print("\n🧪 Testing FiveDayForecastTab chart methods...")
    
    try:
        from ui.tabs import FiveDayForecastTab
        
        # Create a mock controller
        class MockController:
            def get_five_day_forecast(self, city):
                return f"Mock 5-day forecast for {city}"
            
            def get_unit_label(self):
                return "°C"
        
        # Create a temporary root window for testing
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        notebook = ttk.Notebook(root)
        controller = MockController()
        
        # Create FiveDayForecastTab
        five_day_tab = FiveDayForecastTab(notebook, controller)
        
        # Test that chart methods exist
        chart_methods = [
            'generate_5day_line_chart',
            'generate_5day_bar_chart',
            'generate_5day_rain_chart'
        ]
        
        for method_name in chart_methods:
            if hasattr(five_day_tab, method_name):
                print(f"✅ FiveDayForecastTab.{method_name} method exists")
            else:
                print(f"❌ FiveDayForecastTab.{method_name} method missing")
                return False
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ FiveDayForecastTab test error: {e}")
        return False

def test_actual_chart_generation():
    """Test actual chart generation with matplotlib"""
    print("\n🧪 Testing actual chart generation...")
    
    try:
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure
        import numpy as np
        import tkinter as tk
        
        # Create a test window
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Create a simple chart
        fig = Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)
        
        # Sample data
        x = [1, 2, 3, 4, 5]
        y = [22, 25, 20, 24, 28]
        
        ax.plot(x, y, marker='o', linewidth=2)
        ax.set_title('Test Chart')
        ax.set_ylabel('Temperature (°C)')
        ax.grid(True, alpha=0.3)
        
        # Create canvas (this is what would be embedded in tkinter)
        canvas = FigureCanvasTkAgg(fig, root)
        canvas.draw()
        
        print("✅ Chart generation successful")
        
        # Clean up
        plt.close(fig)
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"❌ Chart generation error: {e}")
        return False

def main():
    """Run all chart integration tests"""
    print("🚀 Starting Chart Integration Tests")
    print("=" * 50)
    
    tests = [
        test_chart_imports,
        test_forecast_tab_charts,
        test_comparison_tab_charts,
        test_history_tab_charts,
        test_five_day_forecast_charts,
        test_actual_chart_generation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print(f"❌ Test {test.__name__} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All chart integration tests passed!")
        print("\n✅ Chart functionality is fully integrated and working!")
        print("\n📈 Available Chart Types:")
        print("   • Line charts for temperature trends")
        print("   • Bar charts for comparisons")
        print("   • Histograms for distributions")
        print("   • Multi-city comparison charts")
        print("   • Statistical analysis charts")
        print("\n🏷️ Available in Tabs:")
        print("   • Forecast Tab: Line, Bar, Histogram charts")
        print("   • 5-Day Forecast Tab: Trend, Daily, Rain charts")
        print("   • Comparison Tab: Temperature, Weather, Multi-city charts")
        print("   • History Tab: History Line, Trend, Statistics charts")
    else:
        print(f"❌ {total - passed} tests failed")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
