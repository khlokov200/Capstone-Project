import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import requests
import csv
import random
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load API key
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
LOG_FILE = "data/weather_log.csv"
os.makedirs("data", exist_ok=True)

# Activity suggestions
ACTIVITY_MAP = {
    "clear": ["Go for a walk", "Have a picnic", "Go for a bike ride"],
    "clouds": ["Visit a museum", "Go to a coffee shop", "Watch a movie"],
    "rain": ["Read a book", "Do indoor yoga", "Bake something warm"],
    "snow": ["Build a snowman", "Go sledding", "Drink hot chocolate"],
    "default": ["Relax at home", "Do some journaling", "Organize your room"]
}

# Themes
THEMES = {
    "Day": {"bg": "#ffffff", "fg": "#000000"},
    "Night": {"bg": "#2c3e50", "fg": "#ecf0f1"}
}

# Save weather to CSV
def save_weather(city, temp, desc):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["DateTime", "City", "Temperature", "Description"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), city, temp, desc])

# Load weather history
def load_weather_history(limit=7):
    if not os.path.exists(LOG_FILE):
        return [], []
    with open(LOG_FILE, "r") as file:
        reader = list(csv.DictReader(file))
        recent = reader[-limit:]
        return [row["DateTime"] for row in recent], [float(row["Temperature"]) for row in recent]

# Suggest activity
def suggest_activity(desc):
    key = next((k for k in ACTIVITY_MAP if k in desc.lower()), "default")
    return random.choice(ACTIVITY_MAP[key])

# Fetch weather
def fetch_weather(city):
    try:
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data["main"]["temp"], data["weather"][0]["description"]
    except requests.RequestException as e:
        messagebox.showerror("API Error", str(e))
        return None, None

# Update weather UI
def update_weather():
    global city_entry
    city = city_entry.get()
    if not city.strip():
        messagebox.showwarning("Input Error", "Enter a city name.")
        return
    temp, desc = fetch_weather(city)
    if temp is not None:
        weather_label.config(text=f"{city}\n{temp}°C\n{desc}")
        activity = suggest_activity(desc)
        activity_label.config(text=f"Suggested Activity: {activity}")
        if temp > 35 or "storm" in desc.lower():
            alert_label.config(text="⚠️ Weather Alert: Stay safe!", fg="red")
        else:
            alert_label.config(text="", fg=theme["fg"])
        save_weather(city, temp, desc)
        draw_graph()

# Draw temperature graph
def draw_graph():
    dates, temps = load_weather_history()
    ax.clear()
    ax.plot(dates, temps, marker='o', color='orange')
    ax.set_title("Temperature History")
    ax.set_ylabel("°C")
    ax.tick_params(axis='x', labelrotation=45)
    fig.tight_layout()
    canvas.draw()

# Toggle theme
def toggle_theme():
    global theme
    theme = THEMES["Night"] if theme_switch.get() else THEMES["Day"]
    root.config(bg=theme["bg"])
    for widget in widgets:
        widget.config(bg=theme["bg"], fg=theme["fg"])
    mascot_label.config(bg=theme["bg"])
    draw_graph()

# GUI setup
root = tk.Tk()
root.title("Enhanced Weather Dashboard")
root.geometry("600x600")
theme = THEMES["Day"]
root.config(bg=theme["bg"])

city_entry = tk.Entry(root)
get_weather_btn = tk.Button(root, text="Get Weather", command=update_weather)
weather_label = tk.Label(root, text="", font=("Helvetica", 14))
activity_label = tk.Label(root, text="", font=("Helvetica", 12))
alert_label = tk.Label(root, text="", font=("Helvetica", 12))
mascot_label = tk.Label(root, text="🐧", font=("Helvetica", 28))
theme_switch = tk.IntVar()
theme_checkbox = tk.Checkbutton(root, text="Night Mode", variable=theme_switch, command=toggle_theme)

widgets = [city_entry, get_weather_btn, weather_label, activity_label, alert_label, theme_checkbox]
for widget in widgets:
    widget.config(bg=theme["bg"], fg=theme["fg"])

# Layout

tk.Label(root, text="Enter City:", bg=theme["bg"], fg=theme["fg"]).pack(pady=5)
city_entry.pack()
get_weather_btn.pack(pady=5)
weather_label.pack(pady=10)
activity_label.pack(pady=5)
alert_label.pack(pady=5)
theme_checkbox.pack()
mascot_label.pack(pady=10)

fig, ax = plt.subplots(figsize=(5, 2))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()
draw_graph()

# ✅ Starts the GUI event loop
root.mainloop()

# Weather Dashboard

# Tkinter GUI with theming, history tracking, activity suggestion, and alerting.
# Requires `.env` with `OPENWEATHER_API_KEY`
# Temperature chart rendered in window using Matplotlib.