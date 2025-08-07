import tkinter as tk
from tkinter import ttk, messagebox

class ComparisonTab:
    """Weather comparison tab component"""
    
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Compare Cities")
        self._weather_df = {}
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the UI components"""
        # City selection frame
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
        """Compare weather between two cities with enhanced visualization"""
        try:
            # First validate the city selection
            if not self._validate_city_selection():
                return
                
            # Get the validated cities
            city1, city2 = self._get_selected_cities()
            
            if not city1 or not city2:
                messagebox.showerror("Error", "Please select both cities")
                return
            
            # Initialize weather data storage
            self._weather_df = {}
            
            # Get weather data for both cities
            data1 = self.controller.get_current_weather(city1)
            if not data1:
                messagebox.showerror("Error", f"Could not retrieve weather data for {city1}")
                return
                
            data2 = self.controller.get_current_weather(city2)
            if not data2:
                messagebox.showerror("Error", f"Could not retrieve weather data for {city2}")
                return
            
            # Store the data for comparison
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
            
            # Update display
            self._update_comparison_text(city1, city2)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compare cities: {str(e)}")
            self._weather_df = {}

    def _validate_city_selection(self):
        """Validate that both cities are selected"""
        city1, city2 = self._get_selected_cities()
        
        if not city1 or not city2:
            messagebox.showerror("Error", "Please select both cities")
            return False
            
        if city1 == city2:
            messagebox.showerror("Error", "Please select different cities")
            return False
            
        return True
        
    def _get_selected_cities(self):
        """Get the selected cities from the combo boxes"""
        try:
            return (self.city1_combo.get().strip(), self.city2_combo.get().strip())
        except Exception as e:
            messagebox.showerror("Error", "Failed to get selected cities")
            return None, None
            
    def _update_comparison_text(self, city1, city2):
        """Update the comparison text between cities"""
        try:
            data1 = self._weather_df[city1]
            data2 = self._weather_df[city2]
            
            comparison = f"Weather Comparison: {city1} vs {city2}\n"
            comparison += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            comparison += "🌡️ Temperature:\n"
            temp_diff = data1['temp'] - data2['temp']
            comparison += f"• {city1}: {data1['temp']}°C\n"
            comparison += f"• {city2}: {data2['temp']}°C\n"
            comparison += f"• Difference: {abs(temp_diff)}°C "
            comparison += f"({'warmer' if temp_diff > 0 else 'cooler'} in {city1})\n\n"
            
            comparison += "💧 Humidity:\n"
            humid_diff = data1['humidity'] - data2['humidity']
            comparison += f"• {city1}: {data1['humidity']}%\n"
            comparison += f"• {city2}: {data2['humidity']}%\n"
            comparison += f"• Difference: {abs(humid_diff)}% "
            comparison += f"({'higher' if humid_diff > 0 else 'lower'} in {city1})\n\n"
            
            comparison += "💨 Wind Speed:\n"
            wind_diff = data1['wind_speed'] - data2['wind_speed']
            comparison += f"• {city1}: {data1['wind_speed']} km/h\n"
            comparison += f"• {city2}: {data2['wind_speed']} km/h\n"
            comparison += f"• Difference: {abs(wind_diff)} km/h "
            comparison += f"({'windier' if wind_diff > 0 else 'calmer'} in {city1})\n\n"
            
            comparison += "🌤️ Conditions:\n"
            comparison += f"• {city1}: {data1['description']}\n"
            comparison += f"• {city2}: {data2['description']}"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, comparison)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update comparison: {str(e)}")
