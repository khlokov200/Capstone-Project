#!/bin/bash
# Script to rename screenshot files

# Create an array of source files
declare -a SOURCE_FILES=(
  "Screenshot 2025-08-08 at 9.10.35 AM.png"
  "Screenshot 2025-08-08 at 9.12.02 AM.png"
  "Screenshot 2025-08-08 at 9.12.51 AM.png"
  "Screenshot 2025-08-08 at 9.13.20 AM.png"
  "Screenshot 2025-08-08 at 9.13.50 AM.png"
  "Screenshot 2025-08-08 at 9.15.31 AM.png"
  "Screenshot 2025-08-08 at 9.16.07 AM.png"
  "Screenshot 2025-08-08 at 9.16.29 AM.png"
  "Screenshot 2025-08-08 at 9.16.35 AM.png"
  "Screenshot 2025-08-08 at 9.10.10 AM.png"
)

# Create an array of target files
declare -a TARGET_FILES=(
  "03_forecast.png"
  "04_live_weather.png"
  "05_analytics.png"
  "06_city_comparison.png"
  "07_health_wellness.png"
  "08_activity_suggestions.png"
  "09_poetry_generator.png"
  "10_weather_history.png"
  "11_settings.png"
  "12_extra_feature.png"
)

# Loop through and rename files
for i in "${!SOURCE_FILES[@]}"; do
  if [ -f "${SOURCE_FILES[$i]}" ]; then
    echo "Renaming: ${SOURCE_FILES[$i]} -> ${TARGET_FILES[$i]}"
    mv -f "${SOURCE_FILES[$i]}" "${TARGET_FILES[$i]}"
  else
    echo "File not found: ${SOURCE_FILES[$i]}"
  fi
done

echo "Renaming complete."
