import unittest
from unittest.mock import MagicMock
from tkinter import ttk
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np

class TestComparisonFunctionality(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.notebook = ttk.Notebook(self.root)
        self.controller = MagicMock()
        
        # Mock weather data
        self.mock_weather1 = MagicMock(
            temperature=25,
            humidity=65,
            wind_speed=12,
            description="Sunny"
        )
        self.mock_weather2 = MagicMock(
            temperature=20,
            humidity=75,
            wind_speed=15,
            description="Cloudy"
        )
        
        self.controller.get_current_weather.side_effect = [
            self.mock_weather1,
            self.mock_weather2
        ]
        
    def test_comparison_charts(self):
        """Test that comparison charts are created correctly"""
        from ui.tabs import ComparisonTab
        tab = ComparisonTab(self.notebook, self.controller)
        
        # Test radar chart creation
        tab._create_radar_chart("City1", "City2")
        self.assertTrue(plt.fignum_exists(1))
        
        # Test bar charts creation
        tab._create_bar_charts("City1", "City2")
        self.assertTrue(plt.fignum_exists(2))
        
    def test_comparison_text(self):
        """Test that comparison text is generated correctly"""
        from ui.tabs import ComparisonTab
        tab = ComparisonTab(self.notebook, self.controller)
        
        # Setup test data
        tab._weather_df = {
            "City1": {
                'temp': 25,
                'humidity': 65,
                'wind_speed': 12,
                'description': "Sunny"
            },
            "City2": {
                'temp': 20,
                'humidity': 75,
                'wind_speed': 15,
                'description': "Cloudy"
            }
        }
        
        # Test text update
        tab._update_comparison_text("City1", "City2")
        text = tab.result_text.get("1.0", tk.END)
        
        # Verify text content
        self.assertIn("City1", text)
        self.assertIn("City2", text)
        self.assertIn("25°C", text)
        self.assertIn("20°C", text)
        self.assertIn("warmer", text)
        
    def test_full_comparison(self):
        """Test the full comparison flow"""
        from ui.tabs import ComparisonTab
        tab = ComparisonTab(self.notebook, self.controller)
        
        # Setup cities
        tab.city1_combo.set("City1")
        tab.city2_combo.set("City2")
        
        # Trigger comparison
        tab.compare_cities()
        
        # Verify all components were updated
        self.assertTrue(tab._weather_df)
        self.assertTrue(plt.fignum_exists(1))  # Radar chart
        self.assertTrue(plt.fignum_exists(2))  # Bar charts
        
        # Verify text was updated
        text = tab.result_text.get("1.0", tk.END)
        self.assertIn("City1", text)
        self.assertIn("City2", text)

if __name__ == '__main__':
    unittest.main()
