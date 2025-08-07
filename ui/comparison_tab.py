import tkinter as tk
from tkinter import ttk, messagebox

class ComparisonTab:
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Compare Cities")
        self._weather_df = {}
        self._setup_ui()
        
    def _setup_ui(self):
        selection_frame = ttk.Frame(self.frame)
        selection_frame.pack(pady=10)
        
        # First city
        ttk.Label(selection_frame, text="City 1:").grid(row=0, column=0, padx=5)
        self.city1_combo = ttk.Combobox(selection_frame)
        self.city1_combo.grid(row=0, column=1, padx=5)
        
        # Second city
        ttk.Label(selection_frame, text="City 2:").grid(row=0, column=2, padx=5)
        self.city2_combo = ttk.Combobox(selection_frame)
        self.city2_combo.grid(row=0, column=3, padx=5)
        
        # Compare button
        ttk.Button(selection_frame, text="Compare", 
                  command=self.compare_cities).grid(row=0, column=4, padx=10)
        
        # Result text area
        self.result_text = tk.Text(self.frame, height=15, width=50)
        self.result_text.pack(pady=10)
        
    def compare_cities(self):
        try:
            city1 = self.city1_combo.get().strip()
            city2 = self.city2_combo.get().strip()
            
            if not city1 or not city2:
                messagebox.showerror("Error", "Please select both cities")
                return
                
            if city1 == city2:
                messagebox.showerror("Error", "Please select different cities")
                return
            
            self._weather_df = {}  # Reset data
            
            # Get weather data
            data1 = self.controller.get_current_weather(city1)
            data2 = self.controller.get_current_weather(city2)
            
            if not data1 or not data2:
                messagebox.showerror("Error", "Could not retrieve weather data")
                return
            
            # Store data
            self._weather_df[city1] = {
                'temp': data1.temperature,
                'humidity': data1.humidity,
                'wind_speed': data1.wind_speed,
                'description': data1.description
            }
            
            self._weather_df[city2] = {
                'temp': data2.temperature,
                'humidity': data2.humidity,
                'wind_speed': data2.wind_speed,
                'description': data2.description
            }
            
            # Show comparison
            self._show_comparison(city1, city2)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compare cities: {str(e)}")
            self._weather_df = {}
            
    def _show_comparison(self, city1, city2):
        try:
            data1 = self._weather_df[city1]
            data2 = self._weather_df[city2]
            
            comparison = f"Weather Comparison: {city1} vs {city2}\n"
            comparison += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            # Temperature
            temp_diff = data1['temp'] - data2['temp']
            comparison += f"Temperature:\n"
            comparison += f"{city1}: {data1['temp']}°C\n"
            comparison += f"{city2}: {data2['temp']}°C\n"
            comparison += f"Difference: {abs(temp_diff)}°C "
            comparison += f"({'warmer' if temp_diff > 0 else 'cooler'} in {city1})\n\n"
            
            # Humidity
            humid_diff = data1['humidity'] - data2['humidity']
            comparison += f"Humidity:\n"
            comparison += f"{city1}: {data1['humidity']}%\n"
            comparison += f"{city2}: {data2['humidity']}%\n"
            comparison += f"Difference: {abs(humid_diff)}% "
            comparison += f"({'higher' if humid_diff > 0 else 'lower'} in {city1})\n\n"
            
            # Wind
            wind_diff = data1['wind_speed'] - data2['wind_speed']
            comparison += f"Wind Speed:\n"
            comparison += f"{city1}: {data1['wind_speed']} km/h\n"
            comparison += f"{city2}: {data2['wind_speed']} km/h\n"
            comparison += f"Difference: {abs(wind_diff)} km/h "
            comparison += f"({'windier' if wind_diff > 0 else 'calmer'} in {city1})\n\n"
            
            # Conditions
            comparison += f"Current Conditions:\n"
            comparison += f"{city1}: {data1['description']}\n"
            comparison += f"{city2}: {data2['description']}"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, comparison)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to show comparison: {str(e)}")
