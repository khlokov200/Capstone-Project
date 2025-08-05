#!/usr/bin/env python3
"""
Simple launcher for the Weather Dashboard
This bypasses terminal issues and starts the app directly
"""
import os
import sys

def launch_app():
    """Launch the weather dashboard application"""
    
    print("🌦️ Weather Dashboard - Direct Launcher")
    print("=" * 45)
    
    # Set demo API key if not provided
    if not os.getenv("WEATHER_API_KEY"):
        os.environ["WEATHER_API_KEY"] = "demo_key_for_testing_12345"
        print("⚠️  Using demo API key - all features available with simulated data")
    
    try:
        # Import and run
        from main import main
        
        print("🚀 Launching Weather Dashboard...")
        print("📱 Close this terminal window to exit the app")
        print()
        
        # Start the application
        main()
        
    except KeyboardInterrupt:
        print("\n👋 Application closed by user")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you're in the correct directory")
        print("2. Check if all Python packages are installed")
        print("3. Try: pip install matplotlib tkinter python-dotenv requests pillow")
        
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    launch_app()
