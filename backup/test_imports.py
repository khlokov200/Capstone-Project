#!/usr/bin/env python3
"""
Test import isolation for charts functionality
"""

print("Testing imports step by step...")

# Test basic imports
print("1. Testing basic imports...")
try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    print("✅ Basic tkinter imports successful")
except Exception as e:
    print(f"❌ Basic imports failed: {e}")

# Test matplotlib imports
print("2. Testing matplotlib imports...")
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    import numpy as np
    CHARTS_AVAILABLE = True
    print("✅ Matplotlib imports successful")
    print(f"CHARTS_AVAILABLE = {CHARTS_AVAILABLE}")
except ImportError as e:
    CHARTS_AVAILABLE = False
    print(f"❌ Matplotlib imports failed: {e}")
    print(f"CHARTS_AVAILABLE = {CHARTS_AVAILABLE}")

# Test ui component imports
print("3. Testing ui component imports...")
try:
    from ui.components import StyledButton, StyledText, StyledLabel, AnimatedLabel
    from ui.constants import COLOR_PALETTE
    print("✅ UI component imports successful")
except Exception as e:
    print(f"❌ UI component imports failed: {e}")

# Test importing the tabs module section by section
print("4. Testing tabs module import...")
try:
    # Let's try a minimal version
    import sys
    import importlib.util
    
    # Load the module directly
    spec = importlib.util.spec_from_file_location("tabs", "ui/tabs.py")
    tabs_module = importlib.util.module_from_spec(spec)
    
    print("Module spec created successfully")
    
    # Execute the module
    spec.loader.exec_module(tabs_module)
    
    print("Module executed successfully")
    
    if hasattr(tabs_module, 'CHARTS_AVAILABLE'):
        print(f"✅ CHARTS_AVAILABLE found: {tabs_module.CHARTS_AVAILABLE}")
    else:
        print("❌ CHARTS_AVAILABLE not found")
        
except Exception as e:
    print(f"❌ Tabs module import failed: {e}")
    import traceback
    traceback.print_exc()

print("\nTest complete!")
