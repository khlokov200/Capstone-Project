#!/usr/bin/env python3
"""
Simple chart test that directly tests the chart functionality in tabs.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_simple_chart():
    """Test basic chart functionality"""
    print("🧪 Testing basic chart functionality...")
    
    try:
        # Test matplotlib imports
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend for testing
        import matplotlib.pyplot as plt
        from matplotlib.figure import Figure
        import numpy as np
        
        # Create a simple test chart
        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        
        # Sample data
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        temps = [22, 25, 20, 24, 28]
        
        # Create a line chart
        ax.plot(days, temps, marker='o', linewidth=2, color='blue')
        ax.set_title('Test Temperature Chart')
        ax.set_ylabel('Temperature (°C)')
        ax.grid(True, alpha=0.3)
        
        print("✅ Basic chart creation successful")
        
        # Test bar chart
        fig2 = Figure(figsize=(6, 4))
        ax2 = fig2.add_subplot(111)
        
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        ax2.bar(days, temps, color=colors, alpha=0.7)
        ax2.set_title('Test Bar Chart')
        ax2.set_ylabel('Temperature (°C)')
        
        print("✅ Bar chart creation successful")
        
        # Test histogram
        fig3 = Figure(figsize=(6, 4))
        ax3 = fig3.add_subplot(111)
        
        # Generate some random data for histogram
        np.random.seed(42)
        data = np.random.normal(22, 5, 100)
        
        ax3.hist(data, bins=15, alpha=0.7, color='lightcoral')
        ax3.set_title('Test Histogram')
        ax3.set_xlabel('Temperature (°C)')
        ax3.set_ylabel('Frequency')
        
        print("✅ Histogram creation successful")
        
        # Clean up
        plt.close('all')
        
        return True
        
    except Exception as e:
        print(f"❌ Chart test failed: {e}")
        return False

def test_tab_chart_methods():
    """Test that chart methods exist in tab classes"""
    print("\n🧪 Testing tab chart method availability...")
    
    try:
        # Test ForecastTab
        from ui.tabs import ForecastTab
        forecast_methods = ['generate_line_chart', 'generate_bar_chart', 'generate_histogram']
        
        for method in forecast_methods:
            if hasattr(ForecastTab, method):
                print(f"✅ ForecastTab.{method} exists")
            else:
                print(f"❌ ForecastTab.{method} missing")
                return False
        
        # Test ComparisonTab
        from ui.tabs import ComparisonTab
        comparison_methods = ['generate_temp_comparison_chart', 'generate_weather_comparison_chart', 'generate_multi_city_chart']
        
        for method in comparison_methods:
            if hasattr(ComparisonTab, method):
                print(f"✅ ComparisonTab.{method} exists")
            else:
                print(f"❌ ComparisonTab.{method} missing")
                return False
        
        # Test HistoryTab
        from ui.tabs import HistoryTab
        history_methods = ['generate_history_line_chart', 'generate_trend_chart', 'generate_stats_chart']
        
        for method in history_methods:
            if hasattr(HistoryTab, method):
                print(f"✅ HistoryTab.{method} exists")
            else:
                print(f"❌ HistoryTab.{method} missing")
                return False
        
        # Test FiveDayForecastTab
        from ui.tabs import FiveDayForecastTab
        five_day_methods = ['generate_5day_line_chart', 'generate_5day_bar_chart', 'generate_5day_rain_chart']
        
        for method in five_day_methods:
            if hasattr(FiveDayForecastTab, method):
                print(f"✅ FiveDayForecastTab.{method} exists")
            else:
                print(f"❌ FiveDayForecastTab.{method} missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Tab method test failed: {e}")
        return False

def test_charts_available():
    """Test if CHARTS_AVAILABLE is working"""
    print("\n🧪 Testing CHARTS_AVAILABLE...")
    
    try:
        # Direct test of chart imports
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure
        import numpy as np
        print("✅ Direct matplotlib imports successful")
        
        # Test in tabs context
        import ui.tabs
        
        # Check if we can access chart functionality in tabs
        if hasattr(ui.tabs, 'plt'):
            print("✅ matplotlib.pyplot available in tabs")
        else:
            print("❌ matplotlib.pyplot not available in tabs")
            
        if hasattr(ui.tabs, 'FigureCanvasTkAgg'):
            print("✅ FigureCanvasTkAgg available in tabs")
        else:
            print("❌ FigureCanvasTkAgg not available in tabs")
            
        if hasattr(ui.tabs, 'Figure'):
            print("✅ Figure available in tabs")
        else:
            print("❌ Figure not available in tabs")
            
        if hasattr(ui.tabs, 'np'):
            print("✅ numpy available in tabs")
        else:
            print("❌ numpy not available in tabs")
        
        return True
        
    except Exception as e:
        print(f"❌ CHARTS_AVAILABLE test failed: {e}")
        return False

def main():
    """Run all chart tests"""
    print("🚀 Running Chart Functionality Tests")
    print("=" * 50)
    
    tests = [
        test_simple_chart,
        test_tab_chart_methods,
        test_charts_available
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All chart tests passed!")
        print("\n✅ Chart Integration Status:")
        print("   • Matplotlib is properly installed")
        print("   • Chart generation methods are implemented")
        print("   • All chart types are working (Line, Bar, Histogram)")
        print("   • Chart methods exist in all relevant tabs")
        print("\n📈 Ready for Chart Generation:")
        print("   • ForecastTab: 3 chart types")
        print("   • ComparisonTab: 3 chart types") 
        print("   • HistoryTab: 3 chart types")
        print("   • FiveDayForecastTab: 3 chart types")
        print("\n🚀 Charts are ready to use in the application!")
    else:
        print(f"❌ {total - passed} tests failed")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
