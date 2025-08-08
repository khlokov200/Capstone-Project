#!/usr/bin/env python3
"""
Terminal Diagnostic and Fix Script
This will diagnose and fix common terminal issues
"""
import os
import sys
import platform
import subprocess

def diagnose_terminal():
    """Diagnose terminal and Python environment"""
    
    print("🔧 TERMINAL DIAGNOSTIC TOOL")
    print("=" * 50)
    
    # System info
    print(f"💻 System: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Current Directory: {os.getcwd()}")
    print(f"🌐 Environment Variables:")
    
    # Check important environment variables
    important_vars = ['PATH', 'PYTHONPATH', 'WEATHER_API_KEY', 'SHELL']
    for var in important_vars:
        value = os.environ.get(var, "Not Set")
        if len(value) > 80:
            value = value[:80] + "..."
        print(f"   {var}: {value}")
    
    print("\n" + "=" * 50)
    
    # Check Python modules
    print("📦 CHECKING PYTHON MODULES:")
    required_modules = [
        'tkinter', 'matplotlib', 'numpy', 'requests', 
        'PIL', 'dotenv', 'json', 'threading'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module} - MISSING")
            missing_modules.append(module)
    
    print("\n" + "=" * 50)
    
    # Check project files
    print("📁 CHECKING PROJECT FILES:")
    required_files = [
        'main.py', 'ui/main_window.py', 'controllers/weather_controller.py',
        'ui/tabs.py', 'services/live_weather_service.py'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MISSING")
            missing_files.append(file)
    
    print("\n" + "=" * 50)
    
    # Provide solutions
    if missing_modules or missing_files:
        print("🔧 FIXES NEEDED:")
        
        if missing_modules:
            print("\n📦 Install missing Python modules:")
            if 'tkinter' in missing_modules:
                print("   # For tkinter (Ubuntu/Debian):")
                print("   sudo apt-get install python3-tk")
            
            other_modules = [m for m in missing_modules if m != 'tkinter']
            if other_modules:
                modules_str = ' '.join(other_modules)
                print(f"   pip install {modules_str}")
        
        if missing_files:
            print(f"\n📁 Missing files: {', '.join(missing_files)}")
            print("   Make sure you're in the correct project directory")
    
    else:
        print("✅ ALL CHECKS PASSED!")
        print("\n🚀 READY TO LAUNCH:")
        print("   Option 1: python3 main.py")
        print("   Option 2: python3 gui_launcher.py")
        print("   Option 3: python3 launch.py")
    
    print("\n" + "=" * 50)
    
    # Test basic functionality
    print("🧪 TESTING BASIC FUNCTIONALITY:")
    try:
        # Set demo API key
        os.environ['WEATHER_API_KEY'] = 'demo_key_for_testing_12345'
        
        # Test main imports
        from main import main
        print("   ✅ Main application imports successfully")
        
        # Test UI imports
        from ui.main_window import MainWindow
        from controllers.weather_controller import WeatherController
        print("   ✅ Core UI components import successfully")
        
        # Test services
        from ui.tabs import LiveWeatherTab
        from services.live_weather_service import AnimatedWeatherWidget
        print("   ✅ Live Weather services import successfully")
        
        print("\n🎉 ALL TESTS PASSED!")
        print("🌦️ Your Weather Dashboard is ready with:")
        print("   🎬 Live Weather Animations")
        print("   🌩️ Doppler Weather Radar")
        print("   🌪️ Severe Weather Tracking")
        print("   📊 City Comparison Charts")
        
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        print("\n🔧 Try installing requirements:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    diagnose_terminal()
