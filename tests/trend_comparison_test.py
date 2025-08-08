#!/usr/bin/env python3
"""
Test script to validate the climate trend chart
"""
import os
import sys
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

print("🧪 Testing Climate Trend Comparison Chart")
print("=" * 40)

try:
    # Create root window
    root = tk.Tk()
    root.title("Climate Trend Comparison Chart Test")
    root.geometry("800x600")
    
    # Create a frame to hold the chart
    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Create figure and axis
    fig = Figure(figsize=(10, 6), dpi=100, facecolor='white')
    ax = fig.add_subplot(111)
    
    # Mock data
    city1 = "New York"
    city2 = "London"
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    city1_temps = [5, 6, 10, 15, 20, 24, 27, 26, 22, 16, 10, 6]
    city2_temps = [12, 13, 15, 17, 20, 23, 25, 25, 23, 20, 16, 13]
    
    # Plot the data
    ax.plot(months, city1_temps, marker='o', linewidth=3, markersize=8, 
           color='#FF9671', label=city1)
    ax.plot(months, city2_temps, marker='s', linewidth=3, markersize=8, 
           color='#00D2FC', label=city2)
    
    # Fill below the lines
    ax.fill_between(months, city1_temps, alpha=0.2, color='#FF9671')
    ax.fill_between(months, city2_temps, alpha=0.2, color='#00D2FC')
    
    # Highlight seasonal differences
    ax.axvspan(0, 1.5, alpha=0.1, color='#B0E0E6', label='Winter')  # Winter
    ax.axvspan(2.5, 4.5, alpha=0.1, color='#98FB98', label='Spring')  # Spring
    ax.axvspan(5.5, 7.5, alpha=0.1, color='#FFDAB9', label='Summer')  # Summer
    ax.axvspan(8.5, 10.5, alpha=0.1, color='#FFB347', label='Fall')  # Fall
    
    # Add labels and styling
    ax.set_title(f'Annual Temperature Trends: {city1} vs {city2}', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Temperature (°C)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Add min/max annotations
    city1_max_idx = city1_temps.index(max(city1_temps))
    city1_min_idx = city1_temps.index(min(city1_temps))
    city2_max_idx = city2_temps.index(max(city2_temps))
    city2_min_idx = city2_temps.index(min(city2_temps))
    
    ax.annotate(f"Max: {max(city1_temps)}°C", 
               xy=(months[city1_max_idx], max(city1_temps)),
               xytext=(0, 10),
               textcoords="offset points",
               ha='center',
               color='#FF9671',
               fontweight='bold')
               
    ax.annotate(f"Min: {min(city1_temps)}°C", 
               xy=(months[city1_min_idx], min(city1_temps)),
               xytext=(0, -15),
               textcoords="offset points",
               ha='center',
               color='#FF9671',
               fontweight='bold')
               
    ax.annotate(f"Max: {max(city2_temps)}°C", 
               xy=(months[city2_max_idx], max(city2_temps)),
               xytext=(0, 10),
               textcoords="offset points",
               ha='center',
               color='#00D2FC',
               fontweight='bold')
               
    ax.annotate(f"Min: {min(city2_temps)}°C", 
               xy=(months[city2_min_idx], min(city2_temps)),
               xytext=(0, -15),
               textcoords="offset points",
               ha='center',
               color='#00D2FC',
               fontweight='bold')
    
    # Add legend
    ax.legend(loc='upper left')
    
    # Display the chart
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # Add toolbar for interactive features
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    
    print("\n✅ Chart generated successfully!")
    print("   This window shows a sample climate trend comparison chart")
    
    # Save the chart as an image
    fig.savefig('trend_comparison_test.png', dpi=120, bbox_inches='tight')
    print("   Chart saved to 'trend_comparison_test.png'")
    
    root.mainloop()
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
