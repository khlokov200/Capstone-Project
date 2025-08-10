#!/bin/bash

# Change to the screens directory
cd /Users/Tobi_Prod/Documents/JTC/Capstone-Project/screens || exit

# Create a mapping of filenames
declare -A file_mappings
file_mappings["Screenshot 2025-08-08 at 9.10.10 AM.png"]="12_extra_feature.png"
file_mappings["Screenshot 2025-08-08 at 9.10.35 AM.png"]="03_forecast.png"
file_mappings["Screenshot 2025-08-08 at 9.12.02 AM.png"]="04_live_weather.png"
file_mappings["Screenshot 2025-08-08 at 9.12.51 AM.png"]="05_analytics.png"
file_mappings["Screenshot 2025-08-08 at 9.13.20 AM.png"]="06_city_comparison.png"
file_mappings["Screenshot 2025-08-08 at 9.13.50 AM.png"]="07_health_wellness.png"
file_mappings["Screenshot 2025-08-08 at 9.15.31 AM.png"]="08_activity_suggestions.png"
file_mappings["Screenshot 2025-08-08 at 9.16.07 AM.png"]="09_poetry_generator.png"
file_mappings["Screenshot 2025-08-08 at 9.16.29 AM.png"]="10_weather_history.png"
file_mappings["Screenshot 2025-08-08 at 9.16.35 AM.png"]="11_settings.png"

# Find all PNG files and rename them based on our mapping
find . -maxdepth 1 -name "Screenshot*.png" | while read -r file; do
    base_file=$(basename "$file")
    if [[ -n "${file_mappings[$base_file]}" ]]; then
        echo "Renaming: $base_file to ${file_mappings[$base_file]}"
        cp "$base_file" "${file_mappings[$base_file]}" && rm "$base_file"
    else
        echo "No mapping for: $base_file"
    fi
done

echo "Renaming complete."
