#!/usr/bin/env python
"""
Test script to verify city loading from team_cities.json
"""
import os
import json
import sys

def debug_load_team_cities():
    """Attempt to load team cities JSON and output detailed information"""
    try:
        # Get current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Current directory: {current_dir}")
        
        # Get path to data directory
        json_path = os.path.join(current_dir, 'data', 'team_cities.json')
        print(f"Looking for file at: {json_path}")
        print(f"File exists: {os.path.exists(json_path)}")
        
        # List all files in the data directory
        data_dir = os.path.join(current_dir, 'data')
        if os.path.exists(data_dir):
            print(f"Files in data directory: {os.listdir(data_dir)}")
        else:
            print("Data directory not found!")
        
        # Try to open and read the file
        if not os.path.exists(json_path):
            print("ERROR: JSON file does not exist at the specified path")
            sys.exit(1)
            
        with open(json_path, 'r') as f:
            print("File opened successfully, attempting to parse JSON...")
            team_data = json.load(f)
            print("JSON parsed successfully!")
            
        # Inspect the structure
        print(f"\nJSON structure:")
        print(f"Top-level keys: {list(team_data.keys())}")
        
        if 'cities_analysis' in team_data:
            cities_analysis = team_data['cities_analysis']
            print(f"cities_analysis keys: {list(cities_analysis.keys())}")
            
            if 'city_data' in cities_analysis:
                city_data = cities_analysis['city_data']
                cities = list(city_data.keys())
                print(f"Found {len(cities)} cities in city_data")
                print(f"Cities: {cities}")
                
                # Sample the first city to see its structure
                if cities:
                    first_city = cities[0]
                    print(f"\nSample data for {first_city}:")
                    print(json.dumps(city_data[first_city], indent=2)[:500] + '...')  # Show truncated data
                
                # Extract and sort cities
                available_cities = sorted([str(city).strip() for city in cities if city and str(city).strip()])
                print(f"\nSorted city list ({len(available_cities)} cities):")
                print(available_cities)
                
                return available_cities
            else:
                print("ERROR: No 'city_data' key found in cities_analysis")
        else:
            print("ERROR: No 'cities_analysis' key found in team_data")
            
        return []
    
    except Exception as e:
        print(f"ERROR loading cities: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    print("=== Team Cities JSON Loader Debugging ===")
    cities = debug_load_team_cities()
    print("\n=== Summary ===")
    print(f"Successfully loaded {len(cities)} cities")
    if cities:
        print("The cities JSON file appears to be valid and contains city data.")
    else:
        print("No cities were loaded. Please check the error messages above.")
