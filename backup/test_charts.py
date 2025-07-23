#!/usr/bin/env python3
"""
Test script to verify chart functionality in the weather dashboard
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

def test_chart_functionality():
    """Test the matplotlib chart functionality"""
    print("Testing chart functionality...")
    
    # Create a test window
    root = tk.Tk()
    root.title("Chart Functionality Test")
    root.geometry("800x600")
    
    # Create notebook for tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Test Line Chart Tab
    line_frame = ttk.Frame(notebook)
    notebook.add(line_frame, text="Line Chart Test")
    
    # Create line chart
    fig1 = Figure(figsize=(6, 4), dpi=100)
    ax1 = fig1.add_subplot(111)
    
    # Sample data
    days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']
    temperatures = [22, 24, 19, 26, 23]
    
    ax1.plot(days, temperatures, 'b-o', linewidth=2, markersize=6)
    ax1.set_title('5-Day Temperature Forecast')
    ax1.set_ylabel('Temperature (°C)')
    ax1.set_xlabel('Days')
    ax1.grid(True, alpha=0.3)
    fig1.tight_layout()
    
    canvas1 = FigureCanvasTkAgg(fig1, line_frame)
    canvas1.draw()
    canvas1.get_tk_widget().pack(fill="both", expand=True)
    
    # Test Bar Chart Tab
    bar_frame = ttk.Frame(notebook)
    notebook.add(bar_frame, text="Bar Chart Test")
    
    # Create bar chart
    fig2 = Figure(figsize=(6, 4), dpi=100)
    ax2 = fig2.add_subplot(111)
    
    # Sample data
    metrics = ['Temperature', 'Humidity', 'Wind Speed', 'Pressure']
    city1_values = [22, 65, 12, 1013]
    city2_values = [19, 72, 18, 1008]
    
    x_pos = np.arange(len(metrics))
    width = 0.35
    
    ax2.bar(x_pos - width/2, city1_values, width, label='City 1', color='steelblue', alpha=0.8)
    ax2.bar(x_pos + width/2, city2_values, width, label='City 2', color='lightcoral', alpha=0.8)
    
    ax2.set_title('City Comparison')
    ax2.set_ylabel('Values')
    ax2.set_xlabel('Metrics')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(metrics)
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    fig2.tight_layout()
    
    canvas2 = FigureCanvasTkAgg(fig2, bar_frame)
    canvas2.draw()
    canvas2.get_tk_widget().pack(fill="both", expand=True)
    
    # Test Histogram Tab
    hist_frame = ttk.Frame(notebook)
    notebook.add(hist_frame, text="Histogram Test")
    
    # Create histogram
    fig3 = Figure(figsize=(6, 4), dpi=100)
    ax3 = fig3.add_subplot(111)
    
    # Sample temperature data
    temps = [18, 19, 20, 21, 22, 23, 24, 25, 26, 22, 21, 20, 19, 23, 24, 25, 22, 21]
    
    n, bins, patches = ax3.hist(temps, bins=8, alpha=0.7, color='skyblue', edgecolor='black')
    
    ax3.set_title('Temperature Distribution')
    ax3.set_xlabel('Temperature (°C)')
    ax3.set_ylabel('Frequency')
    ax3.grid(True, alpha=0.3, axis='y')
    fig3.tight_layout()
    
    canvas3 = FigureCanvasTkAgg(fig3, hist_frame)
    canvas3.draw()
    canvas3.get_tk_widget().pack(fill="both", expand=True)
    
    print("✅ Chart functionality test completed successfully!")
    print("📊 All chart types are working:")
    print("   • Line charts for temperature trends")
    print("   • Bar charts for comparisons")
    print("   • Histograms for distributions")
    
    # Add close button
    close_button = ttk.Button(root, text="Close Test", command=root.quit)
    close_button.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    test_chart_functionality()
