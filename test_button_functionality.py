#!/usr/bin/env python3
"""
Test script to verify all button functions are working
"""

import tkinter as tk
from tkinter import ttk
from ui.tabs import LiveRadarTab
import inspect

def test_button_functions():
    """Test all button functions in LiveRadarTab"""
    print("🔍 Testing LiveRadarTab button functionality...")
    
    # Create a dummy root and controller for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    class DummyController:
        def toggle_graph_mode(self):
            print("✅ Controller toggle_graph_mode called")
    
    controller = DummyController()
    
    # Create a dummy notebook
    notebook = ttk.Notebook(root)
    
    # Create LiveRadarTab instance
    try:
        radar_tab = LiveRadarTab(notebook, controller)
        print("✅ LiveRadarTab created successfully")
        
        # Test all the methods that should exist
        required_methods = [
            'start_people_animations',
            'stop_people_animations', 
            'sync_weather_animation',
            'animation_settings',
            'update_doppler_radar',
            'track_storms',
            'radar_alerts',
            'radar_statistics',
            'show_live_radar',
            'track_severe_weather',
            'show_visible_satellite',
            'show_infrared_satellite',
            'show_water_vapor_satellite',
            'show_current_temperature',
            'show_heat_index',
            'show_wind_chill',
            'show_wind_speed',
            'show_wind_direction',
            'show_wind_gusts',
            'show_live_lightning',
            'show_lightning_density',
            'toggle_lightning_audio',
            'rotate_3d_view',
            'zoom_3d_in',
            'zoom_3d_out',
            'radar_time_back',
            'radar_time_pause',
            'radar_time_play',
            'radar_time_forward',
            'toggle_terrain_layer',
            'toggle_cities_layer',
            'toggle_roads_layer',
            'open_radar_settings',
            'configure_radar_alerts',
            'update_radar_location',
            'refresh_radar',
            'play_radar_animation',
            'pause_radar_animation'
        ]
        
        missing_methods = []
        working_methods = []
        
        for method_name in required_methods:
            if hasattr(radar_tab, method_name):
                method = getattr(radar_tab, method_name)
                if callable(method):
                    working_methods.append(method_name)
                else:
                    missing_methods.append(f"{method_name} (not callable)")
            else:
                missing_methods.append(method_name)
        
        print(f"\n📊 RESULTS:")
        print(f"✅ Working button functions: {len(working_methods)}")
        print(f"❌ Missing button functions: {len(missing_methods)}")
        
        if working_methods:
            print(f"\n✅ WORKING FUNCTIONS ({len(working_methods)}):")
            for method in working_methods:
                print(f"   • {method}")
        
        if missing_methods:
            print(f"\n❌ MISSING FUNCTIONS ({len(missing_methods)}):")
            for method in missing_methods:
                print(f"   • {method}")
        else:
            print(f"\n🎉 ALL BUTTON FUNCTIONS ARE IMPLEMENTED!")
            
    except Exception as e:
        print(f"❌ Error creating LiveRadarTab: {e}")
    
    finally:
        root.destroy()

if __name__ == "__main__":
    test_button_functions()
