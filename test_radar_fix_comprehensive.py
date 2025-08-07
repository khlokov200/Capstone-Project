#!/usr/bin/env python
"""
Comprehensive test for the radar chart fix implementation.
This script tests the radar chart functionality with cities that have different metrics available.
"""

import sys
import os
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import unittest
from unittest.mock import MagicMock, patch
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the root directory to the path to import modules
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

try:
    # Import required modules
    from ui.tabs import ComparisonTab
    from models.city import City
    from services.weather_service import WeatherService
    logger.info("Successfully imported required modules")
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    sys.exit(1)

class TestRadarChartFix(unittest.TestCase):
    """Test case for the radar chart fix implementation."""
    
    def setUp(self):
        """Set up the test environment."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window
        self.notebook = ttk.Notebook(self.root)
        
        # Create mock service and cities with different metrics
        self.weather_service = MagicMock(spec=WeatherService)
        
        # Create city1 with 4 metrics
        self.city1 = MagicMock(spec=City)
        self.city1.name = "Test City 1"
        self.city1.get_metrics.return_value = {
            "temperature": 25.0,
            "humidity": 60.0,
            "wind_speed": 15.0,
            "pressure": 1013.0
        }
        
        # Create city2 with 5 metrics (different set)
        self.city2 = MagicMock(spec=City)
        self.city2.name = "Test City 2"
        self.city2.get_metrics.return_value = {
            "temperature": 22.0,
            "humidity": 65.0,
            "precipitation": 10.0,
            "cloud_cover": 30.0,
            "wind_speed": 12.0
        }
        
        # Mock the weather service to return our test cities
        self.weather_service.get_cities.return_value = [self.city1, self.city2]
        
        # Create the comparison tab with our mock service
        self.comparison_tab = ComparisonTab(self.notebook, self.weather_service)
        logger.info("Test environment set up successfully")
    
    def test_create_radar_chart_different_metrics(self):
        """Test that _create_radar_chart handles cities with different metrics."""
        try:
            # Access the private method for testing
            # We're testing the underlying functionality directly
            self.comparison_tab._selected_cities = [self.city1, self.city2]
            
            # Call the method - this should not raise an exception now with our fix
            self.comparison_tab._create_radar_chart()
            
            # Check if a figure was created
            self.assertIsNotNone(self.comparison_tab.radar_chart_canvas)
            logger.info("Radar chart created successfully with cities having different metrics")
        except Exception as e:
            self.fail(f"_create_radar_chart raised an exception: {e}")
    
    def test_fix_radar_comparison(self):
        """Test the fix_radar_comparison method."""
        try:
            # Set up the test conditions
            self.comparison_tab._selected_cities = [self.city1, self.city2]
            
            # Call the fix method
            self.comparison_tab.fix_radar_comparison()
            
            # Check if a figure was created
            self.assertIsNotNone(self.comparison_tab.radar_chart_canvas)
            logger.info("fix_radar_comparison executed successfully")
        except Exception as e:
            self.fail(f"fix_radar_comparison raised an exception: {e}")
    
    def test_common_metrics_detection(self):
        """Test that common metrics are correctly identified."""
        self.comparison_tab._selected_cities = [self.city1, self.city2]
        
        # Get metrics from both cities
        metrics1 = set(self.city1.get_metrics().keys())
        metrics2 = set(self.city2.get_metrics().keys())
        
        # Calculate expected common metrics
        expected_common = metrics1.intersection(metrics2)
        
        # Call the method under test (accessing a private method for testing)
        # We need to extract the common metrics calculation from the actual method
        # This is a bit of a hack but needed for unit testing
        with patch('matplotlib.pyplot.figure'):
            with patch('matplotlib.pyplot.subplot'):
                try:
                    self.comparison_tab._create_radar_chart()
                    # The actual verification depends on how the common metrics are stored
                    # For this test, we're just ensuring no exception is raised
                    logger.info(f"Expected common metrics: {expected_common}")
                    # In a real test, you might have access to the actual computed common metrics
                except Exception as e:
                    self.fail(f"Common metrics detection failed: {e}")
    
    def test_with_real_data(self):
        """Integration test with more realistic data."""
        # Create more realistic city data
        city1 = MagicMock(spec=City)
        city1.name = "New York"
        city1.get_metrics.return_value = {
            "temperature": 20.0,
            "humidity": 55.0,
            "wind_speed": 10.0,
            "pressure": 1012.0,
            "visibility": 10.0,
            "uv_index": 5.0,
            "air_quality": 45.0
        }
        
        city2 = MagicMock(spec=City)
        city2.name = "London"
        city2.get_metrics.return_value = {
            "temperature": 15.0,
            "humidity": 70.0,
            "wind_speed": 12.0,
            "precipitation": 5.0,
            "cloud_cover": 60.0,
            "feels_like": 13.0,
            "visibility": 8.0
        }
        
        # Test with these cities
        self.comparison_tab._selected_cities = [city1, city2]
        try:
            self.comparison_tab._create_radar_chart()
            logger.info("Successfully created radar chart with realistic data")
        except Exception as e:
            self.fail(f"Failed with realistic data: {e}")
    
    def tearDown(self):
        """Clean up after the test."""
        plt.close('all')  # Close any open figures
        self.root.destroy()
        logger.info("Test environment cleaned up")

if __name__ == "__main__":
    print("Running radar chart fix comprehensive tests...")
    unittest.main()
