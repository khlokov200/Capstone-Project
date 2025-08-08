#!/usr/bin/env python3
"""
Test script to verify that the ComparisonTab can load data from team_cities.json
"""

import os
import json
import sys

def main():
    # Path to team_cities.json
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'team_cities.json')
    
    # Check if file exists
    if not os.path.exists(json_path):
        print(f"Error: team_cities.json not found at {json_path}")
        return False
    
    try:
        # Load JSON data
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        # Check structure
        if 'cities_analysis' not in data or 'city_data' not in data['cities_analysis']:
            print("Error: Unexpected structure in team_cities.json")
            return False
        
        # Get cities
        cities = list(data['cities_analysis']['city_data'].keys())
        print(f"Found {len(cities)} cities in team_cities.json:")
        for city in cities:
            print(f"  - {city}")
        
        # Check sample data for first city
        if cities:
            first_city = cities[0]
            city_data = data['cities_analysis']['city_data'][first_city]
            print(f"\nSample data for {first_city}:")
            
            # Temperature
            if 'temperature' in city_data:
                temp_avg = city_data['temperature'].get('avg', 'N/A')
                print(f"  Temperature average: {temp_avg}")
            
            # Humidity
            if 'humidity' in city_data:
                humidity_avg = city_data['humidity'].get('avg', 'N/A')
                print(f"  Humidity average: {humidity_avg}")
            
            # Wind
            if 'wind' in city_data:
                wind_avg = city_data['wind'].get('avg', 'N/A')
                print(f"  Wind speed average: {wind_avg}")
            
            # Weather conditions
            if 'weather_conditions' in city_data:
                conditions = city_data['weather_conditions']
                print(f"  Weather conditions: {', '.join(conditions[:3])}{'...' if len(conditions) > 3 else ''}")
        
        return True
    
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in team_cities.json")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
