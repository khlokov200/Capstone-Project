#Enhanced Weather Dashboard

This is a fully interactive weather dashboard built with Python, Tkinter, and the OpenWeatherMap API. It was developed as part of a capstone project to demonstrate core software development and data integration skills.

🚀 Features

✅ Core Functionality
	•	Weather API Integration: Fetches real-time weather data from the OpenWeatherMap API.
	•	Tkinter GUI: Simple and intuitive user interface for city-based weather lookup.
	•	File-based Data Storage: Logs weather data to a CSV file for persistence.
	•	Error Handling: Gracefully handles invalid input, network issues, and API failures.

🌟 Capstone Additions

⭐ Data Feature: Weather History Tracker
	•	Saves daily temperature and description to CSV.
	•	Displays the last 7 days of weather history.
	•	Auto-generates a line chart of recent temperatures.

⭐⭐ Visual Feature: Temperature Graph
	•	Embedded Matplotlib chart within the Tkinter UI.
	•	Displays a trend line of the past 7 recorded temperature entries.

⭐⭐⭐ Smart Feature: Activity Suggester
	•	Recommends a fun, weather-appropriate activity (e.g., “Read a book” for rainy days, “Go for a hike” on clear days).

⭐⭐ Interactive Feature: Weather Alerts
	•	Triggers an on-screen alert when the temperature exceeds 35°C or storm conditions are detected.

⭐⭐ Visual Enhancement: Theme Switcher
	•	A Day/Night toggle button allows users to switch themes.
	•	Changes the background, text, and graph colors dynamically for improved readability and aesthetics.

🎨 Personal Touch: Weather Mascot
	•	Adds a friendly mascot (🐧) to the UI for a fun and engaging user experience.

⸻

📸 Screenshots / Demo
(Place Holder)

WeatherDashboard/
├── main.py               # Main GUI + API logic
├── weather_collector.py  # API call and response handler
├── weather_database.py   # CSV storage and read operations
├── data/
│   └── weather_log.csv   # Stores daily temperature data
├── docs/
│   └── demo_day.png      # Screenshots for demo
├── .env                  # API key (excluded via .gitignore)
├── .gitignore

🔍 Sample CSV Entry
date,city,temperature,description
2025-07-13,Toronto,28.5,Clear sky
2025-07-14,Toronto,30.1,Light rain

🧪 Requirements
	•	Python 3.x
	•	Tkinter (bundled with most Python installations)
	•	requests
	•	python-dotenv
	•	matplotlib

Install dependencies:
pip install requests python-dotenv matplotlib

🧰 Setup Instructions
	1.	Register on OpenWeatherMap and get your free API key.
	2.	Create a .env file at the project root:
   OPENWEATHER_API_KEY=your_api_key_here

	Run the app:
   python main.py

🔭 Future Enhancements
	•	Add a 5-day or hourly forecast view
	•	Location auto-detection using IP geolocation
	•	Export weather data to PDF reports
	•	Multi-city comparison mode

⸻

📄 License

MIT License (Add full LICENSE file if open-sourcing)   