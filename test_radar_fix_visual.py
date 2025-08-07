#!/usr/bin/env python
"""
Visual verification test for the radar chart fix implementation.
This script creates a simple window to visually test the radar chart with cities
that have different metrics available.
"""

import sys
import os
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("radar_chart_test.log")
    ]
)
logger = logging.getLogger(__name__)

class MockCity:
    """Mock city class for testing."""
    
    def __init__(self, name, metrics):
        """Initialize with name and metrics dictionary."""
        self.name = name
        self._metrics = metrics
    
    def get_metrics(self):
        """Return the metrics dictionary."""
        return self._metrics

class SimpleTester:
    """Simple tester for the radar chart fix."""
    
    def __init__(self, root):
        """Initialize the tester with a root window."""
        self.root = root
        self.root.title("Radar Chart Fix Test")
        self.root.geometry("800x600")
        
        # Create test cities with different metrics
        self.city1 = MockCity("New York", {
            "temperature": 22.0,
            "humidity": 55.0,
            "wind_speed": 10.0,
            "pressure": 1012.0
        })
        
        self.city2 = MockCity("London", {
            "temperature": 15.0,
            "humidity": 70.0,
            "precipitation": 5.0,
            "cloud_cover": 60.0,
            "wind_speed": 12.0
        })
        
        self.city3 = MockCity("Tokyo", {
            "temperature": 25.0,
            "humidity": 60.0,
            "wind_speed": 8.0,
            "visibility": 9.0,
            "air_quality": 45.0,
            "uv_index": 7.0
        })
        
        self.selected_cities = []
        
        # Create UI components
        self._create_ui()
        
    def _create_ui(self):
        """Create the user interface."""
        # Create frames
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        chart_frame = ttk.Frame(self.root)
        chart_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create city selection
        ttk.Label(control_frame, text="Select Cities:").grid(row=0, column=0, padx=5, pady=5)
        
        # City checkbuttons
        self.city1_var = tk.BooleanVar()
        ttk.Checkbutton(control_frame, text=self.city1.name, variable=self.city1_var).grid(row=0, column=1, padx=5, pady=5)
        
        self.city2_var = tk.BooleanVar()
        ttk.Checkbutton(control_frame, text=self.city2.name, variable=self.city2_var).grid(row=0, column=2, padx=5, pady=5)
        
        self.city3_var = tk.BooleanVar()
        ttk.Checkbutton(control_frame, text=self.city3.name, variable=self.city3_var).grid(row=0, column=3, padx=5, pady=5)
        
        # Create buttons
        ttk.Button(control_frame, text="Create Chart (Standard)", command=self.create_standard_chart).grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        ttk.Button(control_frame, text="Create Chart (Fixed)", command=self.create_fixed_chart).grid(row=1, column=2, columnspan=2, padx=5, pady=5)
        ttk.Button(control_frame, text="Clear", command=self.clear_chart).grid(row=1, column=4, padx=5, pady=5)
        
        # Create chart area
        self.chart_frame = chart_frame
        self.radar_chart_canvas = None
        
        # Create log display
        log_frame = ttk.LabelFrame(self.root, text="Log")
        log_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        self.log_text = tk.Text(log_frame, height=5, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
    def log_message(self, message):
        """Log a message to the log display."""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        logger.info(message)
    
    def _get_selected_cities(self):
        """Get the selected cities."""
        selected = []
        if self.city1_var.get():
            selected.append(self.city1)
        if self.city2_var.get():
            selected.append(self.city2)
        if self.city3_var.get():
            selected.append(self.city3)
        
        self.selected_cities = selected
        return selected
    
    def clear_chart(self):
        """Clear the chart."""
        if self.radar_chart_canvas:
            self.radar_chart_canvas.get_tk_widget().destroy()
            self.radar_chart_canvas = None
        self.log_message("Chart cleared")
    
    def create_standard_chart(self):
        """Create a standard radar chart (may fail with different metrics)."""
        selected = self._get_selected_cities()
        
        if len(selected) < 2:
            self.log_message("Please select at least 2 cities")
            return
        
        try:
            self.clear_chart()
            self.log_message(f"Creating standard chart for: {', '.join(city.name for city in selected)}")
            
            # This is similar to the original implementation that might fail
            # Create the figure and axis
            fig = Figure(figsize=(6, 4))
            ax = fig.add_subplot(111, polar=True)
            
            # Extract all metrics from all cities (this will cause the problem)
            all_metrics = []
            for city in selected:
                all_metrics.extend(city.get_metrics().keys())
            all_metrics = sorted(set(all_metrics))
            
            # Plot the data for each city
            for city in selected:
                metrics = city.get_metrics()
                values = []
                for metric in all_metrics:
                    # This will fail if a city doesn't have all metrics
                    if metric in metrics:
                        values.append(metrics[metric])
                    else:
                        values.append(0)  # This might cause the shape mismatch
                
                # Ensure we have at least 3 data points for a radar chart
                if len(values) < 3:
                    self.log_message(f"Not enough data points for {city.name}")
                    continue
                
                # Add the first value again to close the polygon
                values = np.append(values, values[0])
                
                # Plot
                angles = np.linspace(0, 2*np.pi, len(all_metrics), endpoint=False)
                angles = np.append(angles, angles[0])
                
                # This might fail with shape mismatch
                ax.plot(angles, values, label=city.name)
                ax.fill(angles, values, alpha=0.1)
            
            # Add city names as legend
            ax.legend(loc='upper right')
            
            # Set chart labels
            ax.set_xticks(np.linspace(0, 2*np.pi, len(all_metrics), endpoint=False))
            ax.set_xticklabels(all_metrics)
            
            # Create canvas
            self.radar_chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            self.radar_chart_canvas.draw()
            self.radar_chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.log_message("Standard chart created successfully")
        except Exception as e:
            self.log_message(f"Error creating standard chart: {e}")
    
    def create_fixed_chart(self):
        """Create a fixed radar chart that handles different metrics."""
        selected = self._get_selected_cities()
        
        if len(selected) < 2:
            self.log_message("Please select at least 2 cities")
            return
        
        try:
            self.clear_chart()
            self.log_message(f"Creating fixed chart for: {', '.join(city.name for city in selected)}")
            
            # Fixed implementation
            fig = Figure(figsize=(6, 4))
            ax = fig.add_subplot(111, polar=True)
            
            # Extract metrics sets from each city
            metric_sets = []
            for city in selected:
                metric_sets.append(set(city.get_metrics().keys()))
            
            # Find common metrics among all selected cities
            common_metrics = set.intersection(*metric_sets)
            
            if not common_metrics:
                self.log_message("No common metrics found between selected cities")
                return
            
            # Sort common metrics for consistent ordering
            common_metrics = sorted(common_metrics)
            self.log_message(f"Common metrics: {', '.join(common_metrics)}")
            
            # Define normalization values for known metrics
            normalization = {
                'temperature': 40.0,  # Celsius
                'humidity': 100.0,    # Percentage
                'pressure': 1030.0,   # hPa
                'wind_speed': 30.0,   # km/h
                'precipitation': 50.0,  # mm
                'cloud_cover': 100.0,  # Percentage
                'visibility': 10.0,    # km
                'air_quality': 300.0,  # AQI
                'uv_index': 11.0       # UV Index
            }
            
            # Plot data for each city
            angles = np.linspace(0, 2*np.pi, len(common_metrics), endpoint=False)
            angles = np.append(angles, angles[0])  # Close the polygon
            
            for city in selected:
                metrics = city.get_metrics()
                values = []
                
                for metric in common_metrics:
                    # Normalize the value if normalization is available
                    if metric in metrics:
                        if metric in normalization:
                            values.append(metrics[metric] / normalization[metric])
                        else:
                            # Default normalization if unknown metric
                            values.append(metrics[metric] / 100.0)
                
                # Add the first value again to close the polygon
                values = np.append(values, values[0])
                
                # Plot the data
                ax.plot(angles, values, label=city.name)
                ax.fill(angles, values, alpha=0.1)
            
            # Add city names as legend
            ax.legend(loc='upper right')
            
            # Set chart labels
            ax.set_xticks(angles[:-1])  # Exclude the last duplicate angle
            ax.set_xticklabels(common_metrics)
            
            # Create canvas
            self.radar_chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            self.radar_chart_canvas.draw()
            self.radar_chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.log_message("Fixed chart created successfully")
        except Exception as e:
            self.log_message(f"Error creating fixed chart: {e}")


def main():
    """Main function to run the tester."""
    root = tk.Tk()
    tester = SimpleTester(root)
    root.mainloop()


if __name__ == "__main__":
    main()
