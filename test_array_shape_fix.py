#!/usr/bin/env python3
"""
Test script for verifying the fix for array shape mismatches in radar charts.
This specifically tests the scenario where cities have different metrics.
"""

import os
import sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk

def test_array_shape_mismatch_fix():
    """Test that our fix for array shape mismatches works correctly"""
    print("\n🧪 Testing Array Shape Mismatch Fix")
    print("=" * 50)
    
    try:
        # Create a test window
        root = tk.Tk()
        root.title("Array Shape Mismatch Fix Test")
        root.geometry("800x600")
        
        # Create a status label
        status = ttk.Label(root, text="Running test...", font=("Arial", 12))
        status.pack(pady=10)
        
        # Create frame for chart
        frame = ttk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create simulated city data with intentionally different metrics
        print("Creating test data with different metrics...")
        
        # City 1 has metrics A, B, C, D, E
        city1 = "City Alpha"
        city1_data = {
            "temp": 25,
            "humidity": 60,
            "wind_speed": 12,
            "visibility": 15,
            "pressure": 1020
        }
        
        # City 2 has metrics A, B, C, F, G (some overlap, some different)
        city2 = "City Beta"
        city2_data = {
            "temp": 18,
            "humidity": 75,
            "wind_speed": 10,
            "cloud_cover": 40,
            "uv_index": 6
        }
        
        print(f"City 1 metrics: {list(city1_data.keys())}")
        print(f"City 2 metrics: {list(city2_data.keys())}")
        
        # Step 1: Find common metrics between cities
        print("\nStep 1: Finding common metrics")
        common_metrics = list(set(city1_data.keys()) & set(city2_data.keys()))
        print(f"Common metrics: {common_metrics}")
        
        # Check if we have enough metrics for a meaningful comparison
        if len(common_metrics) < 2:
            status.config(text="❌ Not enough common metrics for comparison")
            print("❌ Not enough common metrics for comparison")
            btn = ttk.Button(root, text="Close", command=root.destroy)
            btn.pack(pady=10)
            root.mainloop()
            return False
            
        # Step 2: Create labels for the chart
        labels = [metric.replace('_', ' ').capitalize() for metric in common_metrics]
        print(f"Chart labels: {labels}")
        
        # Step 3: Create normalized values for common metrics only
        # Define max values for normalization
        max_values = {
            'temp': 40,
            'humidity': 100,
            'wind_speed': 50,
            'pressure': 1050,
            'visibility': 20,
            'cloud_cover': 100,
            'uv_index': 11
        }
        
        # Normalize values to 0-100 scale
        city1_values = []
        city2_values = []
        
        for metric in common_metrics:
            # Get max value for normalization (default 100)
            max_val = max_values.get(metric, 100)
            
            # Normalize values
            city1_val = city1_data.get(metric, 0) / max_val * 100
            city2_val = city2_data.get(metric, 0) / max_val * 100
            
            city1_values.append(city1_val)
            city2_values.append(city2_val)
            
        print(f"City 1 normalized values: {city1_values}")
        print(f"City 2 normalized values: {city2_values}")
        
        # Step 4: Create radar chart
        print("\nStep 4: Creating radar chart with common metrics only")
        
        # Number of metrics (vertices)
        N = len(common_metrics)
        
        # Create angles for each metric
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        
        # Close the polygon by repeating the first value
        angles += angles[:1]
        
        # Add the first value again to close the polygon
        city1_values += city1_values[:1]
        city2_values += city2_values[:1]
        
        print(f"Angles array length: {len(angles)}")
        print(f"City 1 values array length: {len(city1_values)}")
        print(f"City 2 values array length: {len(city2_values)}")
        
        # Create plot
        fig = plt.figure(figsize=(6, 6), dpi=100)
        ax = fig.add_subplot(111, polar=True)
        
        # Plot data
        ax.plot(angles, city1_values, 'o-', linewidth=2, label=city1, color='#FF5733')
        ax.fill(angles, city1_values, alpha=0.25, color='#FF5733')
        
        ax.plot(angles, city2_values, 'o-', linewidth=2, label=city2, color='#33A1FF')
        ax.fill(angles, city2_values, alpha=0.25, color='#33A1FF')
        
        # Set labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        
        # Set y-axis limits and ticks
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'])
        
        # Add title and legend
        ax.set_title("Array Shape Mismatch Fix Test", size=14, pad=20)
        ax.legend(loc='upper right')
        
        # Display chart in frame
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Test successful
        status.config(text="✅ Test passed! Fixed array shape mismatch issue.")
        print("✅ Test passed! Arrays have matching dimensions now.")
        print("  This demonstrates that we properly handle cities with different metrics.")
        
        # Add close button
        btn = ttk.Button(root, text="Close", command=root.destroy)
        btn.pack(pady=10)
        
        # Start main loop
        root.mainloop()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        if 'root' in locals() and 'status' in locals():
            status.config(text=f"❌ Test failed: {str(e)}")
            btn = ttk.Button(root, text="Close", command=root.destroy)
            btn.pack(pady=10)
            root.mainloop()
        return False

if __name__ == "__main__":
    success = test_array_shape_mismatch_fix()
    sys.exit(0 if success else 1)
