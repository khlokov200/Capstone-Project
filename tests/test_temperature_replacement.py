#!/usr/bin/env python3
"""
Test script to validate the temperature comparison chart
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

print("🧪 Testing Temperature Comparison Chart")
print("=" * 40)

try:
    # Create root window
    root = tk.Tk()
    root.title("Temperature Comparison Chart Test")
    root.geometry("800x600")
    
    # Create a frame to hold the chart
    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Create figure and axis
    fig = Figure(figsize=(8, 5), dpi=100, facecolor='white')
    ax = fig.add_subplot(111)
    
    # Mock data
    city1 = "New York"
    city2 = "London"
    metrics = ['Current', 'Feels Like', 'Min', 'Max', 'Morning', 'Evening']
    city1_temps = [24, 26, 18, 29, 20, 23]
    city2_temps = [19, 18, 15, 22, 16, 20]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    # Create grouped bar chart
    rects1 = ax.bar(x - width/2, city1_temps, width, label=city1, color='#F8A65D')
    rects2 = ax.bar(x + width/2, city2_temps, width, label=city2, color='#4CA6FF')
    
    # Add labels and styling
    ax.set_title(f'Temperature Comparison: {city1} vs {city2}', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Temperature Metrics', fontsize=12)
    ax.set_ylabel('Temperature (°C)', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend()
    
    # Add value labels on top of bars
    for rect in rects1:
        height = rect.get_height()
        ax.annotate(f'{height}°C',
                    xy=(rect.get_x() + rect.get_width()/2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontweight='bold')
                    
    for rect in rects2:
        height = rect.get_height()
        ax.annotate(f'{height}°C',
                    xy=(rect.get_x() + rect.get_width()/2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontweight='bold')
    
    # Add grid and styling
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Display the chart
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # Add toolbar for interactive features
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    
    print("\n✅ Chart generated successfully!")
    print("   This window shows a sample temperature comparison chart")
    
    # Save the chart as an image
    fig.savefig('temp_comparison_test.png', dpi=120, bbox_inches='tight')
    print("   Chart saved to 'temp_comparison_test.png'")
    
    root.mainloop()
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
