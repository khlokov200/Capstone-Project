# import os
# import tkinter as tk
# from tkinter import ttk, messagebox
# from datetime import datetime
# import requests
# from core.api import WeatherAPI  # <-- Use your API client
# import csv
# import random
# from dotenv import load_dotenv
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# # --- Weather Service ---
# class OpenWeatherService:
#     def __init__(self, api_key, log_file="data/weather_log.csv"):
#         self.api_key = api_key
#         self.api = WeatherAPI(api_key)  # <-- Use WeatherAPI for current weather
#         self.log_file = log_file
#         os.makedirs(os.path.dirname(log_file), exist_ok=True)
#         self.activity_map = {
#             "clear": ["Go for a walk", "Have a picnic", "Go for a bike ride"],
#             "clouds": ["Visit a museum", "Go to a coffee shop", "Watch a movie"],
#             "rain": ["Read a book", "Do indoor yoga", "Bake something warm"],
#             "snow": ["Build a snowman", "Go sledding", "Drink hot chocolate"],
#             "default": ["Relax at home", "Do some journaling", "Organize your room"]
#         }

#     def get_current_weather(self, city):
#         data = self.api.fetch_weather(city)
#         if not data:
#             raise Exception("Failed to fetch weather")
#         desc = data["weather"][0]["description"].capitalize()
#         temp = data["main"]["temp"]
#         self.save_weather(city, temp, desc)
#         return temp, desc

#     def get_forecast(self, city):
#         url = f"https://api.openweathermap.org/data/2.5/forecast"
#         params = {"q": city, "appid": self.api_key, "units": "metric"}
#         resp = requests.get(url, params=params)
#         data = resp.json()
#         if resp.status_code != 200:
#             raise Exception(data.get("message", "Failed to fetch forecast"))
#         forecasts = []
#         for item in data["list"][:5]:
#             dt_txt = item["dt_txt"]
#             desc = item["weather"][0]["description"].capitalize()
#             temp = item["main"]["temp"]
#             forecasts.append(f"{dt_txt}: {desc}, {temp}°C")
#         return "\n".join(forecasts)

#     def compare_cities(self, c1, c2):
#         t1, d1 = self.get_current_weather(c1)
#         t2, d2 = self.get_current_weather(c2)
#         return f"{c1}: {t1}°C, {d1}\n{c2}: {t2}°C, {d2}"

#     def save_weather(self, city, temp, desc):
#         file_exists = os.path.isfile(self.log_file)
#         with open(self.log_file, "a", newline="") as file:
#             writer = csv.writer(file)
#             if not file_exists:
#                 writer.writerow(["DateTime", "City", "Temperature", "Description"])
#             writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), city, temp, desc])

#     def load_weather_history(self, limit=7):
#         if not os.path.exists(self.log_file):
#             return [], []
#         with open(self.log_file, "r") as file:
#             reader = list(csv.DictReader(file))
#             recent = reader[-limit:]
#             return [row["DateTime"] for row in recent], [float(row["Temperature"]) for row in recent]

#     def suggest(self, city):
#         temp, desc = self.get_current_weather(city)
#         key = next((k for k in self.activity_map if k in desc.lower()), "default")
#         return random.choice(self.activity_map[key])

#     def generate_poem(self, city):
#         temp, desc = self.get_current_weather(city)
#         return f"{city} weather inspires:\n{desc}, {temp}°C\nNature sings in every degree."

#     def save_entry(self, text, mood):
#         # Implement saving to file or database if needed
#         pass

# # --- Main GUI ---
# class MainWindow(tk.Tk):
#     def __init__(
#         self,
#         weather_service,
#         comparison_service,
#         journal_service,
#         activity_service,
#         poetry_service
#     ):
#         super().__init__()
#         self.title("Weather Dashboard Capstone")
#         self.geometry("900x700")
#         self.configure(bg="#23272e")

#         style = ttk.Style(self)
#         style.theme_use("clam")
#         style.configure("TNotebook", background="#23272e", borderwidth=0)
#         style.configure("TNotebook.Tab", background="#2c313c", foreground="#fff", padding=10)
#         style.map("TNotebook.Tab", background=[("selected", "#3a3f4b")])

#         notebook = ttk.Notebook(self)
#         notebook.pack(fill="both", expand=True, padx=10, pady=10)

#         self.current_weather_tab(notebook, weather_service)
#         self.forecast_tab(notebook, weather_service)
#         self.comparison_tab(notebook, comparison_service)
#         self.journal_tab(notebook, journal_service)
#         self.activity_tab(notebook, activity_service)
#         self.poetry_tab(notebook, poetry_service)
#         self.history_tab(notebook, weather_service)

#     def current_weather_tab(self, notebook, weather_service):
#         frame = ttk.Frame(notebook)
#         notebook.add(frame, text="Current Weather")
#         label = ttk.Label(frame, text="Enter City:", background="#23272e", foreground="#fff")
#         label.pack(pady=10)
#         city_entry = ttk.Entry(frame)
#         city_entry.pack()
#         result = tk.Text(frame, height=10, width=60, bg="#2c313c", fg="#fff")
#         result.pack(pady=10)
#         mascot_label = ttk.Label(frame, text="🐧", font=("Helvetica", 28), background="#23272e", foreground="#fff")
#         mascot_label.pack(pady=10)
#         alert_label = ttk.Label(frame, text="", background="#23272e", foreground="#fff")
#         alert_label.pack(pady=5)

#         def fetch_weather():
#             city = city_entry.get()
#             try:
#                 temp, desc = weather_service.get_current_weather(city)
#                 result.delete(1.0, tk.END)
#                 result.insert(tk.END, f"Weather in {city}:\n{temp}°C\n{desc}")
#                 if temp > 35 or "storm" in desc.lower():
#                     alert_label.config(text="⚠️ Weather Alert: Stay safe!", foreground="red")
#                 else:
#                     alert_label.config(text="", foreground="#fff")
#                 self.draw_graph(weather_service)
#             except Exception as e:
#                 messagebox.showerror("Error", str(e))

#         btn = ttk.Button(frame, text="Get Weather", command=fetch_weather)
#         btn.pack(pady=5)

#         # Matplotlib graph
#         self.fig, self.ax = plt.subplots(figsize=(5, 2))
#         self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
#         self.canvas.get_tk_widget().pack()
#         self.draw_graph(weather_service)

#     def draw_graph(self, weather_service):
#         dates, temps = weather_service.load_weather_history()
#         self.ax.clear()
#         self.ax.plot(dates, temps, marker='o', color='orange')
#         self.ax.set_title("Temperature History")
#         self.ax.set_ylabel("°C")
#         self.ax.tick_params(axis='x', labelrotation=45)
#         self.fig.tight_layout()
#         self.canvas.draw()

#     def forecast_tab(self, notebook, weather_service):
#         frame = ttk.Frame(notebook)
#         notebook.add(frame, text="Forecast")
#         label = ttk.Label(frame, text="Enter City:", background="#23272e", foreground="#fff")
#         label.pack(pady=10)
#         city_entry = ttk.Entry(frame)
#         city_entry.pack()
#         result = tk.Text(frame, height=10, width=60, bg="#2c313c", fg="#fff")
#         result.pack(pady=10)

#         def fetch_forecast():
#             city = city_entry.get()
#             try:
#                 forecast = weather_service.get_forecast(city)
#                 result.delete(1.0, tk.END)
#                 result.insert(tk.END, f"Forecast for {city}:\n{forecast}")
#             except Exception as e:
#                 messagebox.showerror("Error", str(e))

#         btn = ttk.Button(frame, text="Get Forecast", command=fetch_forecast)
#         btn.pack(pady=5)

#     def comparison_tab(self, notebook, comparison_service):
#         frame = ttk.Frame(notebook)
#         notebook.add(frame, text="City Comparison")
#         label1 = ttk.Label(frame, text="City 1:", background="#23272e", foreground="#fff")
#         label1.pack(pady=5)
#         city1_entry = ttk.Entry(frame)
#         city1_entry.pack()
#         label2 = ttk.Label(frame, text="City 2:", background="#23272e", foreground="#fff")
#         label2.pack(pady=5)
#         city2_entry = ttk.Entry(frame)
#         city2_entry.pack()
#         result = tk.Text(frame, height=10, width=60, bg="#2c313c", fg="#fff")
#         result.pack(pady=10)

#         def compare():
#             city1 = city1_entry.get()
#             city2 = city2_entry.get()
#             try:
#                 comparison = comparison_service.compare_cities(city1, city2)
#                 result.delete(1.0, tk.END)
#                 result.insert(tk.END, f"Comparison:\n{comparison}")
#             except Exception as e:
#                 messagebox.showerror("Error", str(e))

#         btn = ttk.Button(frame, text="Compare", command=compare)
#         btn.pack(pady=5)

#     def journal_tab(self, notebook, journal_service):
#         frame = ttk.Frame(notebook)
#         notebook.add(frame, text="Weather Journal")
#         label = ttk.Label(frame, text="Journal Entry:", background="#23272e", foreground="#fff")
#         label.pack(pady=10)
#         entry = tk.Text(frame, height=5, width=60, bg="#2c313c", fg="#fff")
#         entry.pack(pady=5)
#         mood_label = ttk.Label(frame, text="Mood:", background="#23272e", foreground="#fff")
#         mood_label.pack()
#         mood_entry = ttk.Entry(frame)
#         mood_entry.pack()
#         result = tk.Text(frame, height=5, width=60, bg="#2c313c", fg="#fff")
#         result.pack(pady=10)

#         def save_journal():
#             text = entry.get(1.0, tk.END).strip()
#             mood = mood_entry.get()
#             try:
#                 journal_service.save_entry(text, mood)
#                 result.delete(1.0, tk.END)
#                 result.insert(tk.END, "Journal entry saved!")
#             except Exception as e:
#                 messagebox.showerror("Error", str(e))

#         btn = ttk.Button(frame, text="Save Entry", command=save_journal)
#         btn.pack(pady=5)

#     def activity_tab(self, notebook, activity_service):
#         frame = ttk.Frame(notebook)
#         notebook.add(frame, text="Activity Suggestions")
#         label = ttk.Label(frame, text="Enter City:", background="#23272e", foreground="#fff")
#         label.pack(pady=10)
#         city_entry = ttk.Entry(frame)
#         city_entry.pack()
#         result = tk.Text(frame, height=10, width=60, bg="#2c313c", fg="#fff")
#         result.pack(pady=10)

#         def suggest():
#             city = city_entry.get()
#             try:
#                 suggestion = activity_service.suggest(city)
#                 result.delete(1.0, tk.END)
#                 result.insert(tk.END, f"Suggested Activities:\n{suggestion}")
#             except Exception as e:
#                 messagebox.showerror("Error", str(e))

#         btn = ttk.Button(frame, text="Suggest", command=suggest)
#         btn.pack(pady=5)

#     def poetry_tab(self, notebook, poetry_service):
#         frame = ttk.Frame(notebook)
#         notebook.add(frame, text="Weather Poetry")
#         label = ttk.Label(frame, text="Enter City:", background="#23272e", foreground="#fff")
#         label.pack(pady=10)
#         city_entry = ttk.Entry(frame)
#         city_entry.pack()
#         result = tk.Text(frame, height=10, width=60, bg="#2c313c", fg="#fff")
#         result.pack(pady=10)

#         def generate_poem():
#             city = city_entry.get()
#             try:
#                 poem = poetry_service.generate_poem(city)
#                 result.delete(1.0, tk.END)
#                 result.insert(tk.END, f"Weather Poem:\n{poem}")
#             except Exception as e:
#                 messagebox.showerror("Error", str(e))

#         btn = ttk.Button(frame, text="Generate Poem", command=generate_poem)
#         btn.pack(pady=5)

#     def history_tab(self, notebook, weather_service):
#         frame = ttk.Frame(notebook)
#         notebook.add(frame, text="Weather History")
#         label = ttk.Label(frame, text="Recent Weather Logs:", background="#23272e", foreground="#fff")
#         label.pack(pady=5)
#         history_box = tk.Text(frame, height=15, width=80, bg="#2c313c", fg="#fff")
#         history_box.pack(pady=10)
#         dates, temps = weather_service.load_weather_history(15)
#         for dt, temp in zip(dates, temps):
#             history_box.insert(tk.END, f"{dt}: {temp}°C\n")

# if __name__ == "__main__":
#     load_dotenv()
#     API_KEY = os.getenv("OPENWEATHER_API_KEY")
#     live_service = OpenWeatherService(API_KEY)
#     app = MainWindow(
#         live_service, live_service, live_service, live_service, live_service
#     )
#     app.mainloop()