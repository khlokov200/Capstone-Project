#!/usr/bin/env python
"""
Command-line test script for radar chart fix implementation.
This script tests the radar chart with cities specified as command-line arguments.

Usage: python test_radar_fix_cli.py [city1] [city2] [city3]
Example: python test_radar_fix_cli.py "New York" "London" "Tokyo"
"""

import sys
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import logging
import json
from matplotlib.figure import Figure

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("radar_chart_cli_test.log")
    ]
)
logger = logging.getLogger(__name__)


class MockCity:
    """Mock city class for testing."""
    
    def __init__(self, name):
        """Initialize with name and generate metrics."""
        self.name = name
        self._metrics = self._generate_metrics()
    
    def _generate_metrics(self):
        """Generate random metrics for the city."""
        # Base metrics all cities will have
        metrics = {
            "temperature": np.random.uniform(0, 35),
            "humidity": np.random.uniform(30, 90)
        }
        
        # Additional metrics that may vary by city
        additional_metrics = {
            "wind_speed": np.random.uniform(0, 25),
            "pressure": np.random.uniform(990, 1030),
            "visibility": np.random.uniform(1, 10),
            "precipitation": np.random.uniform(0, 50),
            "cloud_cover": np.random.uniform(0, 100),
            "air_quality": np.random.uniform(0, 300),
            "uv_index": np.random.uniform(0, 11),
            "feels_like": np.random.uniform(0, 40),
            "dew_point": np.random.uniform(-5, 25)
        }
        
        # Each city gets a random subset of the additional metrics
        num_additional = np.random.randint(2, 6)
        metrics_to_add = np.random.choice(list(additional_metrics.keys()), 
                                         size=num_additional, 
                                         replace=False)
        
        for metric in metrics_to_add:
            metrics[metric] = additional_metrics[metric]
            
        return metrics
    
    def get_metrics(self):
        """Return the metrics dictionary."""
        return self._metrics


def create_radar_chart(cities, save_path=None):
    """
    Create a radar chart for the given cities.
    This is the implementation with the fix applied.
    """
    if len(cities) < 2:
        logger.error("Need at least 2 cities to compare")
        return False
        
    try:
        # Extract metrics sets from each city
        logger.info(f"Creating radar chart for cities: {', '.join(city.name for city in cities)}")
        
        for city in cities:
            metrics = city.get_metrics()
            logger.info(f"City: {city.name}, Metrics: {json.dumps(metrics, indent=2)}")
        
        metric_sets = []
        for city in cities:
            metric_sets.append(set(city.get_metrics().keys()))
        
        # Find common metrics among all selected cities
        common_metrics = set.intersection(*metric_sets)
        
        if not common_metrics:
            logger.error("No common metrics found between selected cities")
            return False
        
        # Sort common metrics for consistent ordering
        common_metrics = sorted(common_metrics)
        logger.info(f"Common metrics found: {', '.join(common_metrics)}")
        
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
            'uv_index': 11.0,      # UV Index
            'feels_like': 40.0,    # Celsius
            'dew_point': 30.0      # Celsius
        }
        
        # Create the figure and axis
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, polar=True)
        
        # Plot data for each city
        angles = np.linspace(0, 2*np.pi, len(common_metrics), endpoint=False)
        angles = np.append(angles, angles[0])  # Close the polygon
        
        for city in cities:
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
            ax.plot(angles, values, label=city.name, linewidth=2.0)
            ax.fill(angles, values, alpha=0.1)
        
        # Add city names as legend
        ax.legend(loc='upper right', fontsize='large')
        
        # Set chart labels
        ax.set_xticks(angles[:-1])  # Exclude the last duplicate angle
        ax.set_xticklabels(common_metrics)
        plt.title("City Comparison Radar Chart", size=16)
        
        # Save if requested
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Chart saved to {save_path}")
        
        # Show the chart
        plt.tight_layout()
        plt.show()
        
        return True
    except Exception as e:
        logger.error(f"Error creating radar chart: {e}")
        return False


def main():
    """Parse arguments and run the test."""
    parser = argparse.ArgumentParser(description="Test the radar chart fix implementation")
    parser.add_argument("cities", nargs='*', default=["New York", "London", "Tokyo"],
                       help="Cities to include in the radar chart")
    parser.add_argument("-s", "--save", help="Path to save the chart image")
    args = parser.parse_args()
    
    # Ensure we have at least 2 cities
    if len(args.cities) < 2:
        logger.error("Need at least 2 cities to compare")
        sys.exit(1)
    
    # Create mock cities
    cities = [MockCity(city_name) for city_name in args.cities]
    
    # Create and show the radar chart
    result = create_radar_chart(cities, args.save)
    
    if not result:
        logger.error("Failed to create radar chart")
        sys.exit(1)


if __name__ == "__main__":
    main()
