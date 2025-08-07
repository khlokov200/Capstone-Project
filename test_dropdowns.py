#!/usr/bin/env python
"""
Test script to verify dropdown population with city data
"""
import os
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class DropdownTester(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("City Dropdown Test")
        self.geometry("400x300")
        
        # Load cities
        self.available_cities = self.load_team_cities()
        
        # Create UI
        self.create_ui()
    
    def load_team_cities(self):
        """Load team cities from JSON file"""
        try:
            # Get path to JSON file
            base_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(base_dir, 'data', 'team_cities.json')
            
            print(f"Loading cities from: {json_path}")
            print(f"File exists: {os.path.exists(json_path)}")
            
            # Read and parse JSON
            with open(json_path, 'r') as f:
                team_data = json.load(f)
            
            # Extract city names
            cities = list(team_data.get('cities_analysis', {}).get('city_data', {}).keys())
            
            # Clean and sort city names
            available_cities = sorted([str(city).strip() for city in cities if city and str(city).strip()])
            
            print(f"Loaded {len(available_cities)} cities: {available_cities}")
            return available_cities
            
        except Exception as e:
            print(f"Error loading cities: {str(e)}")
            messagebox.showerror("Error", f"Failed to load cities: {str(e)}")
            return []
    
    def create_ui(self):
        """Create the UI with dropdown components"""
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create label
        ttk.Label(frame, text="City Selection Test").pack(pady=10)
        
        # First dropdown
        ttk.Label(frame, text="City 1:").pack(pady=5)
        self.city1_var = tk.StringVar()
        self.city1_combo = ttk.Combobox(frame, 
                                       textvariable=self.city1_var,
                                       values=self.available_cities,
                                       state="readonly")
        self.city1_combo.pack(fill="x", pady=5)
        
        # Second dropdown
        ttk.Label(frame, text="City 2:").pack(pady=5)
        self.city2_var = tk.StringVar()
        self.city2_combo = ttk.Combobox(frame,
                                       textvariable=self.city2_var,
                                       values=self.available_cities,
                                       state="readonly")
        self.city2_combo.pack(fill="x", pady=5)
        
        # Set initial values if cities are available
        if self.available_cities and len(self.available_cities) > 1:
            self.city1_combo.set(self.available_cities[0])
            self.city2_combo.set(self.available_cities[1])
            print(f"Set initial values: {self.available_cities[0]} and {self.available_cities[1]}")
        else:
            print("No cities available to set initial values")
        
        # Button to check selection
        ttk.Button(frame, text="Check Selection", 
                  command=self.check_selection).pack(pady=10)
        
        # Status label
        self.status_label = ttk.Label(frame, text="")
        self.status_label.pack(pady=5)
    
    def check_selection(self):
        """Check the selected city values"""
        city1 = self.city1_var.get()
        city2 = self.city2_var.get()
        
        message = f"Selected: '{city1}' and '{city2}'"
        print(message)
        self.status_label.config(text=message)

if __name__ == "__main__":
    app = DropdownTester()
    app.mainloop()
