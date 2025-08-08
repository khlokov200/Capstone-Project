# Radar Chart Fix Testing Guide

This guide explains how to test the radar chart fix implementation that addresses array shape mismatch issues when comparing cities with different available metrics.

## Available Test Scripts

### 1. Visual Test with UI
The `test_radar_fix_visual.py` script provides an interactive UI to test the radar chart fix:

```bash
python test_radar_fix_visual.py
```

This opens a window where you can:
- Select different cities using checkboxes
- Create a standard chart (original implementation that may fail)
- Create a fixed chart (new implementation that handles different metrics)
- Clear the chart
- View logs of the chart creation process

### 2. Command-line Test
The `test_radar_fix_cli.py` script allows testing from the command line:

```bash
python test_radar_fix_cli.py [city1] [city2] [city3] ...
```

Examples:
```bash
# Test with default cities (New York, London, Tokyo)
python test_radar_fix_cli.py

# Test with custom cities
python test_radar_fix_cli.py "New York" "London" "Paris" "Tokyo"

# Save the generated chart to a file
python test_radar_fix_cli.py -s radar_chart_output.png
```

This script:
- Creates mock cities with randomly generated metrics
- Finds common metrics between cities
- Creates a radar chart using only the common metrics
- Displays a visual representation of the chart

### 3. Comprehensive Unit Tests
The `test_radar_fix_comprehensive.py` script contains unit tests for the radar chart fix:

```bash
python -m unittest test_radar_fix_comprehensive.py
```

This runs tests that verify:
- The `_create_radar_chart` method handles cities with different metrics
- The `fix_radar_comparison` method works correctly
- Common metrics are correctly identified
- The fix works with realistic city data

## Expected Results

When the fix is working correctly:

1. No array shape mismatch errors should occur when comparing cities
2. The radar chart should display using only metrics common to all selected cities
3. The log should show which common metrics were found and used
4. The chart should correctly normalize values for different metric types

## Troubleshooting

If you encounter issues:

1. Check the log output for details about what went wrong
2. Ensure you've selected at least two cities for comparison
3. Verify that the selected cities have at least one common metric
4. Check that the normalization values are appropriate for each metric type

## How It Works

The fix works by:

1. Extracting the set of metrics available for each city
2. Finding the intersection of these sets to identify common metrics
3. Using only these common metrics for plotting
4. Applying appropriate normalization for each metric type
5. Ensuring array shapes are compatible before plotting

This prevents the "Failed to compare cities: x and y must have same first dimension" error that occurred when cities had different available metrics.
