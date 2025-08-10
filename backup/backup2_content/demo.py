#!/usr/bin/env python3
"""
Demo script for Weather Dashboard Capstone Project
Showcases all core features and the advanced chart visualization system
"""

import os
import sys
import time
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demo_core_features():
    """Demonstrate core weather dashboard features"""
    print("🌟 Weather Dashboard Demo - Core Features")
    print("=" * 50)
    
    try:
        from controllers.weather_controller import WeatherController
        from ui.main_window import MainWindow
        
        print("✅ Successfully imported core modules")
        
        # Load environment variables
        load_dotenv()
        api_key = os.getenv("WEATHER_API_KEY")
        
        if not api_key:
            print("⚠️  No API key found. Using demo mode.")
            print("   Create .env file with WEATHER_API_KEY for live data")
        else:
            print("✅ API key loaded successfully")
        
        print("\n🚀 Starting Weather Dashboard Application...")
        print("\nFeatures to demonstrate:")
        print("1. 📍 Current Weather Lookup")
        print("2. 📅 5-Day Forecast")
        print("3. 📊 Advanced Chart Visualizations (12 chart types)")
        print("4. 🔄 City Comparison Tools")
        print("5. 🤖 ML Weather Predictions")
        print("6. 📈 Historical Data Analysis")
        print("7. 📝 Weather Journal")
        print("8. 🎯 Activity Suggestions")
        
        # Create controller and main window
        controller = WeatherController(api_key or "demo_key")
        app = MainWindow(controller)
        
        print("\n✨ Application launched successfully!")
        print("Navigate through the tabs to see all features.")
        print("Press Ctrl+C to exit when demo is complete.")
        
        # Start the application
        app.mainloop()
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo completed successfully!")
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        print("Please check the requirements and setup.")

def demo_chart_features():
    """Demonstrate chart functionality specifically"""
    print("\n📊 Chart Visualization Demo")
    print("=" * 50)
    
    try:
        import matplotlib.pyplot as plt
        print("✅ Matplotlib available - Charts will work")
        
        # Test basic chart functionality
        from backup.test_charts import test_line_chart, test_bar_chart, test_histogram
        print("✅ Running chart functionality tests...")
        
        # This will create and display sample charts
        print("   • Testing line charts...")
        test_line_chart()
        
        print("   • Testing bar charts...")
        test_bar_chart()
        
        print("   • Testing histograms...")
        test_histogram()
        
        print("✅ All chart types working correctly!")
        
    except ImportError:
        print("❌ Matplotlib not available - Charts will show fallback messages")
        print("   Install with: pip install matplotlib")
    except Exception as e:
        print(f"❌ Chart demo error: {e}")

def main():
    """Main demo function"""
    print("🎯 Weather Dashboard Capstone Milestone Demo")
    print("=" * 60)
    print("This demo showcases all core requirements and Feature 1:")
    print("• Real-time weather data")
    print("• Interactive GUI elements")
    print("• ML model predictions")
    print("• Advanced chart visualization system (Feature 1)")
    print("=" * 60)
    
    # Demo chart functionality first
    demo_chart_features()
    
    # Small delay for readability
    time.sleep(2)
    
    # Demo core application features
    demo_core_features()

if __name__ == "__main__":
    main()
