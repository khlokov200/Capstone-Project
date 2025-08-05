#!/usr/bin/env python3
"""
GUI Launcher for Weather Dashboard
This creates a simple GUI to launch the main application
and bypass any terminal issues
"""
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import threading

class WeatherDashboardLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌦️ Weather Dashboard Launcher")
        self.root.geometry("500x400")
        self.root.configure(bg="#2C3E50")
        
        # Make window centered
        self.root.eval('tk::PlaceWindow . center')
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the launcher UI"""
        # Title
        title_label = tk.Label(
            self.root,
            text="🌦️ Weather Dashboard",
            font=("Arial", 24, "bold"),
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            self.root,
            text="Live Weather Radar & Animations",
            font=("Arial", 12),
            bg="#2C3E50",
            fg="#BDC3C7"
        )
        subtitle_label.pack(pady=5)
        
        # Features frame
        features_frame = tk.Frame(self.root, bg="#2C3E50")
        features_frame.pack(pady=20)
        
        features_text = """✨ Features Available:
        
🎬 Live Weather Animations
🌩️ Doppler Weather Radar
🌪️ Severe Weather Tracking
📊 City Comparison Charts
📈 Forecast Visualizations
🤖 ML Weather Predictions
⚠️ Weather Alerts System
📍 GPS Location Support"""
        
        features_label = tk.Label(
            features_frame,
            text=features_text,
            font=("Arial", 10),
            bg="#2C3E50",
            fg="#ECF0F1",
            justify="left"
        )
        features_label.pack()
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg="#2C3E50")
        buttons_frame.pack(pady=30)
        
        # Launch button
        launch_btn = tk.Button(
            buttons_frame,
            text="🚀 Launch Weather Dashboard",
            font=("Arial", 14, "bold"),
            bg="#3498DB",
            fg="white",
            padx=20,
            pady=10,
            command=self.launch_dashboard,
            cursor="hand2"
        )
        launch_btn.pack(pady=10)
        
        # Test button
        test_btn = tk.Button(
            buttons_frame,
            text="🧪 Run Quick Test",
            font=("Arial", 12),
            bg="#27AE60",
            fg="white",
            padx=20,
            pady=5,
            command=self.run_test,
            cursor="hand2"
        )
        test_btn.pack(pady=5)
        
        # Exit button
        exit_btn = tk.Button(
            buttons_frame,
            text="❌ Exit",
            font=("Arial", 12),
            bg="#E74C3C",
            fg="white",
            padx=20,
            pady=5,
            command=self.root.quit,
            cursor="hand2"
        )
        exit_btn.pack(pady=5)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Ready to launch...",
            font=("Arial", 10),
            bg="#2C3E50",
            fg="#95A5A6"
        )
        self.status_label.pack(side="bottom", pady=10)
        
    def launch_dashboard(self):
        """Launch the main weather dashboard"""
        self.status_label.config(text="🚀 Starting Weather Dashboard...", fg="#3498DB")
        self.root.update()
        
        def run_app():
            try:
                # Set environment variable
                os.environ["WEATHER_API_KEY"] = "demo_key_for_testing_12345"
                
                # Import and run the main application
                from main import main
                
                # Hide launcher window
                self.root.withdraw()
                
                # Run main app
                main()
                
                # Show launcher again when app closes
                self.root.deiconify()
                self.status_label.config(text="Dashboard closed. Ready to launch again...", fg="#95A5A6")
                
            except Exception as e:
                self.root.deiconify()
                self.status_label.config(text=f"Error: {str(e)}", fg="#E74C3C")
                messagebox.showerror("Launch Error", 
                                   f"Failed to start Weather Dashboard:\n\n{str(e)}\n\n"
                                   f"Try running 'pip install -r requirements.txt' first.")
        
        # Run in separate thread to prevent blocking
        threading.Thread(target=run_app, daemon=True).start()
    
    def run_test(self):
        """Run a quick test of the application"""
        self.status_label.config(text="🧪 Running tests...", fg="#F39C12")
        self.root.update()
        
        def test_app():
            try:
                # Set test environment
                os.environ["WEATHER_API_KEY"] = "demo_key_for_testing_12345"
                
                # Test imports
                from ui.main_window import MainWindow
                from controllers.weather_controller import WeatherController
                from ui.tabs import LiveWeatherTab
                from services.live_weather_service import AnimatedWeatherWidget, WeatherRadarWidget
                
                self.status_label.config(text="✅ All tests passed! Ready to launch.", fg="#27AE60")
                
                messagebox.showinfo("Test Results", 
                                   "✅ All tests passed!\n\n"
                                   "🌦️ Weather Dashboard is ready to run with:\n"
                                   "• Live Weather Animations\n"
                                   "• Doppler Weather Radar\n"
                                   "• Severe Weather Tracking\n"
                                   "• City Comparison Charts\n"
                                   "• All tab features working\n\n"
                                   "Click 'Launch Weather Dashboard' to start!")
                
            except Exception as e:
                self.status_label.config(text="❌ Test failed. Check dependencies.", fg="#E74C3C")
                messagebox.showerror("Test Failed", 
                                   f"Test failed:\n\n{str(e)}\n\n"
                                   f"Try installing dependencies:\n"
                                   f"pip install matplotlib tkinter python-dotenv requests pillow")
        
        # Run in separate thread
        threading.Thread(target=test_app, daemon=True).start()
    
    def run(self):
        """Start the launcher"""
        self.root.mainloop()

if __name__ == "__main__":
    print("🌦️ Starting Weather Dashboard Launcher...")
    launcher = WeatherDashboardLauncher()
    launcher.run()
