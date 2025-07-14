# Enhanced Weather Dashboard

This is a fully interactive weather dashboard built with Python, Tkinter, and the OpenWeatherMap API. It was developed as part of a capstone project to demonstrate core software development and data integration skills.

## 🚀 Features

### ✅ Core Functionality
- **Weather API Integration**: Fetches real-time weather data from the OpenWeatherMap API.
- **Tkinter GUI**: Simple and intuitive user interface for city-based weather lookup.
- **File-based Data Storage**: Weather data is logged to a CSV file.
- **Error Handling**: Graceful handling of API errors and invalid input.

### 🌟 Capstone Additions

#### ⭐ Data Feature: Weather History Tracker
- Saves daily temperature and description to CSV.
- Displays the last 7 days of weather history.
- Auto-generates a line chart of recent temperatures.

#### ⭐⭐ Visual Feature: Temperature Graph
- Integrated Matplotlib graph embedded within the Tkinter UI.
- Displays trend over the last 7 recorded entries.

#### ⭐⭐⭐ Smart Feature: Activity Suggester
- Suggests a random activity based on the weather description (e.g., rain, clear, snow).

#### ⭐⭐ Interactive Feature: Weather Alerts
- Displays a weather warning message when temperatures exceed 35°C or include storm conditions.

#### ⭐⭐ Visual Enhancement: Theme Switcher
- Toggle between **Day** and **Night** modes.
- Changes background and text color dynamically.

#### 🎨 Personal Enhancement: Weather Mascot
- Adds a fun mascot (🐧) to personalize the application.

## 🛠️ Project Structure
```
WeatherDashboard/
├── main.py               # Main dashboard logic and GUI
├── .env                  # API key file (excluded from Git)
├── data/
│   └── weather_log.csv   # Automatically populated CSV log
├── .gitignore            # Ignores sensitive and cache files
```

## 🔧 Requirements
- Python 3.x
- Tkinter (comes with most Python installations)
- Requests
- Dotenv
- Matplotlib

Install dependencies:
```bash
pip install requests python-dotenv matplotlib
```

## 🔐 Setup Instructions
1. Register on [OpenWeatherMap](https://openweathermap.org/api) to get your API key.
2. Create a `.env` file in the root project folder with this content:
   ```env
   OPENWEATHER_API_KEY=your_api_key_here
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## 📈 Future Ideas
- Add support for 5-day forecast
- Integrate with geolocation
- Export reports as PDF

## 📄 License
MIT License (add if open-sourcing)

---
<<<<<<< ours
=======
Enjoy your enhanced, interactive, and personalized weather dashboard! ☀️🌧️🌙
>>>>>>> theirs
