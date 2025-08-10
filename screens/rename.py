#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

# Change to the screens directory
os.chdir('/Users/Tobi_Prod/Documents/JTC/Capstone-Project/screens')

# Get all PNG files in the directory
png_files = [f for f in os.listdir('.') if f.endswith('.png') and f.startswith('Screenshot')]

# Define the mappings
mappings = [
    ("Screenshot 2025-08-08 at 9.10.10 AM.png", "12_extra_feature.png"),
    ("Screenshot 2025-08-08 at 9.10.35 AM.png", "03_forecast.png"),
    ("Screenshot 2025-08-08 at 9.12.02 AM.png", "04_live_weather.png"),
    ("Screenshot 2025-08-08 at 9.12.51 AM.png", "05_analytics.png"),
    ("Screenshot 2025-08-08 at 9.13.20 AM.png", "06_city_comparison.png"),
    ("Screenshot 2025-08-08 at 9.13.50 AM.png", "07_health_wellness.png"),
    ("Screenshot 2025-08-08 at 9.15.31 AM.png", "08_activity_suggestions.png"),
    ("Screenshot 2025-08-08 at 9.16.07 AM.png", "09_poetry_generator.png"),
    ("Screenshot 2025-08-08 at 9.16.29 AM.png", "10_weather_history.png"),
    ("Screenshot 2025-08-08 at 9.16.35 AM.png", "11_settings.png")
]

# Print all files we found
print("Found PNG files:", png_files)

# For each file in the directory, try to match it with our mappings
for old_name, new_name in mappings:
    # Try exact match
    if old_name in png_files:
        print(f"Renaming: {old_name} to {new_name}")
        shutil.copy2(old_name, new_name)
        os.remove(old_name)
        continue
        
    # Try to match by timestamp in filename
    timestamp = old_name.split("at ")[1].split(" AM")[0]  # Extract "9.10.10" from filename
    matches = [f for f in png_files if timestamp in f]
    
    if matches:
        for match in matches:
            print(f"Matched by timestamp: {match} -> {new_name}")
            shutil.copy2(match, new_name)
            os.remove(match)
            png_files.remove(match)
            break

print("Renaming complete.")
