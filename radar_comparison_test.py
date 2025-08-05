#!/usr/bin/env python3
"""
Test script to validate the radar comparison chart
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

print("🧪 Testing Radar Comparison Chart")
print("=" * 40)

try:
    # Create root window
    root = tk.Tk()
    root.title("Radar Comparison Chart Test")
    root.geometry("800x600")
    
    # Create a frame to hold the chart
    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Create figure
    fig = Figure(figsize=(8, 7), dpi=100, facecolor='white')
    ax = fig.add_subplot(111, polar=True)
    
    # Mock data
    city1 = "New York"
    city2 = "London"
    categories = ['Temperature', 'Humidity', 'Wind', 'Comfort', 'Visibility', 'UV Index']
    
    # Values from 0-100 for each metric
    city1_values = [80, 65, 40, 75, 90, 60]
    city2_values = [50, 85, 65, 45, 70, 40]
    
    # Number of metrics
    N = len(categories)
    
    # Create angles for each metric (radians)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Add values to complete the loop
    city1_values += city1_values[:1]
    city2_values += city2_values[:1]
    
    # Plot radar chart
    ax.plot(angles, city1_values, 'o-', linewidth=2, label=city1, color='#FF6B6B')
    ax.fill(angles, city1_values, alpha=0.25, color='#FF6B6B')
    
    ax.plot(angles, city2_values, 'o-', linewidth=2, label=city2, color='#4ECDC4')
    ax.fill(angles, city2_values, alpha=0.25, color='#4ECDC4')
    
    # Set category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    
    # Add grid and styling
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'])
    ax.set_ylim(0, 100)
    
    # Add title and legend
    ax.set_title(f'Weather Metrics Comparison: {city1} vs {city2}', size=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    # Display the chart
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # Add toolbar for interactive features
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    
    print("\n✅ Chart generated successfully!")
    print("   This window shows a sample radar comparison chart")
    
    # Save the chart as an image
    fig.savefig('radar_comparison_test.png', dpi=120, bbox_inches='tight')
    print("   Chart saved to 'radar_comparison_test.png'")
    
    root.mainloop()
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
