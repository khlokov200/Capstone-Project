#!/bin/bash
# Weather Dashboard Launcher Script

echo "🌦️ Weather Dashboard Launcher"
echo "==============================="

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found"
    echo "Please run this script from the Capstone-Project directory"
    exit 1
fi

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 not found"
    echo "Please install Python 3"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Set environment variable if not set
if [ -z "$WEATHER_API_KEY" ]; then
    export WEATHER_API_KEY="demo_key_for_testing_12345"
    echo "⚠️  Using demo API key for testing"
fi

echo "🚀 Starting Weather Dashboard..."
echo ""
echo "🌦️ Features available:"
echo "   🎬 Live Weather Animations"
echo "   🌩️ Doppler Weather Radar" 
echo "   🌪️ Severe Weather Tracking"
echo "   📊 City Comparison Charts"
echo "   📈 Forecast Visualizations"
echo "   🤖 ML Weather Predictions"
echo ""

# Run the application
python3 main.py
