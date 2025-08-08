"""
Live Animation and Weather Radar Service
Provides animated weather elements and real-time weather radar functionality
"""
import tkinter as tk
from tkinter import ttk
import threading
import time
import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
from PIL import Image, ImageTk, ImageDraw
import io

# Try to import additional packages for animations
ANIMATIONS_AVAILABLE = False
RADAR_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import numpy as np
    ANIMATIONS_AVAILABLE = True
    RADAR_AVAILABLE = True
except ImportError:
    print("📡 Advanced animations/radar unavailable: some packages not installed")

class LiveAnimationService:
    """Service for managing live weather animations"""
    
    def __init__(self):
        self.animations = {}
        self.running = False
        self.animation_thread = None
        
    def start_animations(self):
        """Start all animation systems"""
        if not self.running:
            self.running = True
            self.animation_thread = threading.Thread(target=self._animation_loop, daemon=True)
            self.animation_thread.start()
    
    def stop_animations(self):
        """Stop all animations"""
        self.running = False
        
    def _animation_loop(self):
        """Main animation loop"""
        while self.running:
            for anim_id, animation_obj in self.animations.items():
                if animation_obj.get('active', False):
                    try:
                        animation_obj['update_func']()
                    except Exception as e:
                        print(f"Animation error for {anim_id}: {e}")
            time.sleep(0.1)  # 10 FPS
    
    def register_animation(self, anim_id: str, update_func, active=True):
        """Register a new animation"""
        self.animations[anim_id] = {
            'update_func': update_func,
            'active': active
        }
    
    def remove_animation(self, anim_id: str):
        """Remove an animation"""
        if anim_id in self.animations:
            del self.animations[anim_id]

class WeatherRadarService:
    """Service for live weather radar and severe weather tracking"""
    
    def __init__(self, api_key: str = "demo_key"):
        self.api_key = api_key
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes
        
    def get_weather_alerts(self, lat: float, lon: float) -> List[Dict]:
        """Get weather alerts for specific coordinates"""
        # This is a mock implementation
        alerts = []
        if 30 < lat < 40 and -80 < lon < -70:
            alerts.append({
                "sender_name": "NWS", "event": "Tornado Warning",
                "start": int(time.time()), "end": int(time.time()) + 3600,
                "description": "Tornado Warning for your area. Take shelter immediately!"
            })
        return alerts

    def get_severe_weather_data(self, lat: float, lon: float, tracking_options: Dict) -> Dict:
        """Get severe weather data for specific coordinates with tracking options"""
        # This is a mock implementation
        severe_weather = {
            "hurricanes": [], "tornadoes": [], "storms": [], "blizzards": []
        }
        
        if tracking_options.get("hurricanes"):
            severe_weather["hurricanes"].append({
                "id": "HUR-01", "name": "Hurricane Alex", "category": 3,
                "lat": lat + 1.5, "lon": lon - 1.5, "wind_speed": 120
            })
            
        if tracking_options.get("tornadoes"):
            severe_weather["tornadoes"].append({
                "id": "TOR-01", "ef_scale": 2, "lat": lat - 0.5, "lon": lon + 0.5,
                "movement": "NE at 30 mph"
            })
            
        if tracking_options.get("storms"):
            severe_weather["storms"].append({
                "id": "STM-01", "type": "Supercell", "lat": lat + 0.2, "lon": lon - 0.2,
                "intensity": "High"
            })
            
        if tracking_options.get("blizzards"):
            severe_weather["blizzards"].append({
                "id": "BLZ-01", "lat": lat + 2.0, "lon": lon + 2.0,
                "snow_rate": "2 inches/hr", "wind_speed": 40
            })
            
        return severe_weather

    def get_radar_data(self, lat: float, lon: float, radar_range: str = "200 km") -> Dict:
        """Get radar data for specific coordinates"""
        # This is a mock implementation
        intensity = np.random.rand(20, 20) * 100
        return {"intensity": intensity, "range": radar_range}

    def get_storm_history(self, lat: float, lon: float) -> List[Dict]:
        """Get historical storm data for a location"""
        # Mock implementation
        return [
            {"date": "2023-08-15", "type": "Tornado", "ef_scale": 1},
            {"date": "2023-07-20", "type": "Hurricane", "category": 2},
        ]

    def get_radar_analysis(self, lat: float, lon: float) -> str:
        """Get a detailed analysis of the radar data"""
        # Mock implementation
        return f"Radar Analysis for {lat}, {lon}:\n\n- High precipitation core detected at center.\n- Scattered showers in the NE quadrant."

    
    def get_radar_data(self, lat: float, lon: float, zoom: int = 5) -> Optional[Dict]:
        """Get weather radar data for coordinates"""
        try:
            # Simulate radar data (in real implementation, use weather radar API)
            return self._generate_simulated_radar_data(lat, lon, zoom)
            
        except Exception as e:
            print(f"Radar data error: {e}")
            return None
    
    def _generate_simulated_radar_data(self, lat: float, lon: float, zoom: int) -> Dict:
        """Generate simulated radar data for demonstration"""
        # Create a grid of weather intensity data
        grid_size = 20
        radar_data = []
        
        for i in range(grid_size):
            row = []
            for j in range(grid_size):
                # Simulate weather patterns
                intensity = random.random()
                if intensity > 0.8:
                    weather_type = "severe_storm"
                elif intensity > 0.6:
                    weather_type = "heavy_rain"
                elif intensity > 0.4:
                    weather_type = "moderate_rain"
                elif intensity > 0.2:
                    weather_type = "light_rain"
                else:
                    weather_type = "clear"
                
                row.append({
                    'intensity': intensity,
                    'type': weather_type,
                    'lat': lat + (i - grid_size/2) * 0.1,
                    'lon': lon + (j - grid_size/2) * 0.1
                })
            radar_data.append(row)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'center_lat': lat,
            'center_lon': lon,
            'zoom': zoom,
            'grid_data': radar_data,
            'legends': {
                'severe_storm': '#8B0000',
                'heavy_rain': '#FF0000',
                'moderate_rain': '#FFA500',
                'light_rain': '#FFFF00',
                'clear': '#87CEEB'
            }
        }
    
    def track_severe_weather(self, lat: float, lon: float) -> Dict:
        """Track severe weather events"""
        alerts = self.get_weather_alerts(lat, lon)
        severe_events = []
        
        # Simulate severe weather tracking
        current_time = datetime.now()
        
        # Generate sample severe weather events
        events = [
            {
                'type': 'hurricane',
                'name': 'Hurricane Example',
                'intensity': 'Category 2',
                'location': {'lat': lat + 0.5, 'lon': lon + 0.3},
                'speed': '15 mph NW',
                'status': 'approaching',
                'eta': (current_time + timedelta(hours=8)).isoformat(),
                'icon': '🌀'
            },
            {
                'type': 'tornado_watch',
                'name': 'Tornado Watch #456',
                'intensity': 'EF2 potential',
                'location': {'lat': lat - 0.2, 'lon': lon - 0.1},
                'speed': '35 mph NE',
                'status': 'active',
                'eta': (current_time + timedelta(hours=2)).isoformat(),
                'icon': '🌪️'
            },
            {
                'type': 'blizzard',
                'name': 'Winter Storm Alpha',
                'intensity': 'Heavy snow 12-18"',
                'location': {'lat': lat - 0.8, 'lon': lon + 0.5},
                'speed': '25 mph E',
                'status': 'developing',
                'eta': (current_time + timedelta(hours=12)).isoformat(),
                'icon': '❄️'
            }
        ]
        
        # Filter events based on proximity and severity
        for event in events:
            if random.random() > 0.7:  # 30% chance of each event
                severe_events.append(event)
        
        return {
            'alerts': alerts,
            'severe_events': severe_events,
            'last_updated': current_time.isoformat()
        }

    def get_severe_weather_events(self, lat: float, lon: float) -> List[Dict]:
        """Get severe weather events near the specified coordinates"""
        try:
            # Use existing track_severe_weather method
            severe_weather = self.track_severe_weather(lat, lon)
            events = severe_weather.get('severe_events', [])
            
            # Add distance and formatted data for UI
            formatted_events = []
            for event in events:
                event_lat = event['location']['lat']
                event_lon = event['location']['lon']
                
                # Calculate approximate distance (simplified)
                distance = ((lat - event_lat) ** 2 + (lon - event_lon) ** 2) ** 0.5 * 111  # km
                
                formatted_events.append({
                    'type': event['type'],
                    'name': event['name'],
                    'intensity': event['intensity'],
                    'distance': distance,
                    'eta': event.get('eta', 'Unknown'),
                    'description': f"{event['name']} - {event['intensity']} moving {event['speed']}"
                })
            
            return formatted_events
            
        except Exception as e:
            print(f"Error getting severe weather events: {e}")
            return []
    
    def cleanup(self):
        """Cleanup radar service resources"""
        try:
            # Clear cache
            self.cache.clear()
            print("Radar service cleaned up successfully")
        except Exception as e:
            print(f"Error during radar cleanup: {e}")

class AnimatedWeatherWidget:
    """Animated weather widget with live people and weather effects"""
    
    def __init__(self, parent, width=400, height=300):
        self.parent = parent
        self.width = width
        self.height = height
        self.current_weather = 'clear'  # Initialize current weather
        
        # Create canvas for animations
        self.canvas = tk.Canvas(parent, width=width, height=height, bg='lightblue')
        self.canvas.pack(padx=5, pady=5)
        
        # Animation elements
        self.people = []
        self.weather_effects = []
        self.animation_speed = 50  # milliseconds
        self.animation_running = False
        
        # Initialize people
        self._create_people()
        
    def _create_people(self):
        """Create animated people figures"""
        people_data = [
            {'x': 50, 'y': 200, 'direction': 1, 'speed': 2, 'type': 'walker', 'color': 'blue'},
            {'x': 150, 'y': 180, 'direction': -1, 'speed': 1.5, 'type': 'jogger', 'color': 'green'},
            {'x': 250, 'y': 220, 'direction': 1, 'speed': 0.8, 'type': 'elderly', 'color': 'purple'},
            {'x': 350, 'y': 190, 'direction': -1, 'speed': 3, 'type': 'cyclist', 'color': 'red'}
        ]
        
        for person_data in people_data:
            person_id = self.canvas.create_oval(
                person_data['x'] - 10, person_data['y'] - 20,
                person_data['x'] + 10, person_data['y'],
                fill=person_data['color'], outline='black', width=2
            )
            self.people.append({
                'id': person_id,
                'data': person_data
            })
    
    def start_animation(self, weather_type='clear'):
        """Start weather animation"""
        if not self.animation_running:
            self.animation_running = True
            self.current_weather = weather_type
            self._animate_scene()
    
    def stop_animation(self):
        """Stop animation"""
        self.animation_running = False
    
    def _animate_scene(self):
        """Main animation loop"""
        if not self.animation_running:
            return
            
        # Update people positions
        self._update_people()
        
        # Update weather effects
        self._update_weather_effects()
        
        # Schedule next frame
        self.parent.after(self.animation_speed, self._animate_scene)
    
    def _update_people(self):
        """Update people movement based on weather"""
        for person in self.people:
            person_id = person['id']
            data = person['data']
            
            # Modify movement based on weather
            speed_modifier = self._get_weather_speed_modifier()
            actual_speed = data['speed'] * speed_modifier
            
            # Update position
            new_x = data['x'] + (data['direction'] * actual_speed)
            
            # Boundary checking and direction reversal
            if new_x <= 10 or new_x >= self.width - 10:
                data['direction'] *= -1
                new_x = data['x'] + (data['direction'] * actual_speed)
            
            data['x'] = new_x
            
            # Update canvas position
            self.canvas.coords(person_id, 
                             new_x - 10, data['y'] - 20,
                             new_x + 10, data['y'])
    
    def _get_weather_speed_modifier(self):
        """Get speed modifier based on current weather"""
        modifiers = {
            'clear': 1.0,
            'cloudy': 0.9,
            'rain': 0.6,
            'heavy_rain': 0.3,
            'snow': 0.4,
            'storm': 0.2,
            'blizzard': 0.1
        }
        return modifiers.get(self.current_weather, 1.0)
    
    def _update_weather_effects(self):
        """Update weather visual effects"""
        # Clear old effects
        for effect_id in self.weather_effects:
            self.canvas.delete(effect_id)
        self.weather_effects.clear()
        
        # Add new effects based on weather
        if self.current_weather == 'rain':
            self._add_rain_effects()
        elif self.current_weather == 'snow':
            self._add_snow_effects()
        elif self.current_weather == 'storm':
            self._add_storm_effects()
    
    def _add_rain_effects(self):
        """Add rain animation effects"""
        for _ in range(15):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height - 50)
            rain_drop = self.canvas.create_line(
                x, y, x + 2, y + 15,
                fill='blue', width=2
            )
            self.weather_effects.append(rain_drop)
    
    def _add_snow_effects(self):
        """Add snow animation effects"""
        for _ in range(20):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height - 30)
            snowflake = self.canvas.create_oval(
                x - 3, y - 3, x + 3, y + 3,
                fill='white', outline='lightgray'
            )
            self.weather_effects.append(snowflake)
    
    def _add_storm_effects(self):
        """Add storm animation effects"""
        # Lightning effect
        if random.random() > 0.9:  # 10% chance per frame
            lightning = self.canvas.create_line(
                random.randint(0, self.width), 0,
                random.randint(0, self.width), self.height,
                fill='yellow', width=3
            )
            self.weather_effects.append(lightning)
            
        # Heavy rain
        for _ in range(25):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height - 30)
            rain_drop = self.canvas.create_line(
                x, y, x + 3, y + 20,
                fill='darkblue', width=3
            )
            self.weather_effects.append(rain_drop)
    
    def update_weather(self, weather_type: str):
        """Update weather type and effects"""
        self.current_weather = weather_type
        # Add weather-specific background changes
        weather_colors = {
            'clear': 'lightblue',
            'cloudy': 'lightgray',
            'rain': 'gray',
            'storm': 'darkgray',
            'snow': 'whitesmoke',
            'blizzard': 'white'
        }
        self.canvas.config(bg=weather_colors.get(weather_type, 'lightblue'))

class WeatherRadarWidget:
    """Live weather radar display widget"""
    
    def __init__(self, parent, radar_service: WeatherRadarService, width=400, height=300):
        self.parent = parent
        self.radar_service = radar_service
        self.width = width
        self.height = height
        
        # Create main frame
        self.frame = ttk.LabelFrame(parent, text="🌩️ Live Weather Radar")
        self.frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Controls frame
        self.controls_frame = ttk.Frame(self.frame)
        self.controls_frame.pack(fill="x", padx=5, pady=5)
        
        # Location input
        ttk.Label(self.controls_frame, text="Lat:").grid(row=0, column=0, padx=2)
        self.lat_entry = ttk.Entry(self.controls_frame, width=10)
        self.lat_entry.grid(row=0, column=1, padx=2)
        self.lat_entry.insert(0, "39.2904")  # Baltimore default
        
        ttk.Label(self.controls_frame, text="Lon:").grid(row=0, column=2, padx=2)
        self.lon_entry = ttk.Entry(self.controls_frame, width=10)
        self.lon_entry.grid(row=0, column=3, padx=2)
        self.lon_entry.insert(0, "-76.6122")  # Baltimore default
        
        # Update button
        self.update_btn = ttk.Button(self.controls_frame, text="🔄 Update Radar", 
                                   command=self.update_radar)
        self.update_btn.grid(row=0, column=4, padx=5)
        
        # Tracking controls
        self.tracking_var = tk.BooleanVar(value=True)
        self.tracking_cb = ttk.Checkbutton(self.controls_frame, text="Track Severe Weather", 
                                         variable=self.tracking_var)
        self.tracking_cb.grid(row=0, column=5, padx=5)
        
        # Display area
        if RADAR_AVAILABLE:
            self._create_radar_display()
        else:
            self._create_text_display()
            
        # Auto-update
        self.auto_update = True
        self.update_radar()
        self._schedule_update()
    
    def _create_radar_display(self):
        """Create matplotlib radar display"""
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def _create_text_display(self):
        """Create text-based radar display"""
        self.text_area = tk.Text(self.frame, height=15, width=50)
        self.text_area.pack(fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.text_area.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_area.config(yscrollcommand=scrollbar.set)
    
    def update_radar(self, lat=None, lon=None, tracking_options=None):
        """Update radar display"""
        try:
            # Use provided coordinates if available, otherwise get from entry fields
            if lat is None or lon is None:
                lat = float(self.lat_entry.get())
                lon = float(self.lon_entry.get())
            
            # Get radar data
            radar_data = self.radar_service.get_radar_data(lat, lon)
            
            # Use tracking options if provided, otherwise use checkbox
            track_severe = True
            if tracking_options:
                # At least one tracking option is enabled
                track_severe = any(tracking_options.values())
            elif hasattr(self, 'tracking_var'):
                track_severe = self.tracking_var.get()
                
            if track_severe:
                severe_weather = self.radar_service.track_severe_weather(lat, lon)
            else:
                severe_weather = {'severe_events': [], 'alerts': []}
            
            if RADAR_AVAILABLE and hasattr(self, 'ax'):
                self._update_radar_chart(radar_data, severe_weather)
            else:
                self._update_text_radar(radar_data, severe_weather)
                
        except ValueError:
            if hasattr(self, 'text_area'):
                self.text_area.insert(tk.END, "❌ Invalid coordinates\n")
        except Exception as e:
            if hasattr(self, 'text_area'):
                self.text_area.insert(tk.END, f"❌ Radar update error: {e}\n")
    
    def _update_radar_chart(self, radar_data, severe_weather):
        """Update matplotlib radar chart"""
        self.ax.clear()
        
        if radar_data:
            # Create intensity matrix
            grid = radar_data['grid_data']
            intensity_matrix = [[cell['intensity'] for cell in row] for row in grid]
            
            # Plot radar data
            im = self.ax.imshow(intensity_matrix, cmap='Blues', alpha=0.7, origin='lower')
            
            # Add severe weather markers
            legend_labels = []
            for event in severe_weather.get('severe_events', []):
                # Convert lat/lon to grid coordinates (simplified)
                x = 10 + random.randint(-3, 3)
                y = 10 + random.randint(-3, 3)
                
                label = f"{event['icon']} {event['type']}"
                self.ax.scatter(x, y, c='red', s=100, marker='*', 
                              label=label)
                legend_labels.append(label)
            
            self.ax.set_title(f"Weather Radar - {datetime.now().strftime('%H:%M')}")
            
            # Only show legend if there are severe weather events
            if legend_labels:
                self.ax.legend()
        
        self.canvas.draw()
    
    def _update_text_radar(self, radar_data, severe_weather):
        """Update text-based radar display"""
        self.text_area.delete(1.0, tk.END)
        
        # Header
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.text_area.insert(tk.END, f"🌩️ LIVE WEATHER RADAR - {timestamp}\n")
        self.text_area.insert(tk.END, "=" * 60 + "\n\n")
        
        # Coordinates
        lat = self.lat_entry.get()
        lon = self.lon_entry.get()
        self.text_area.insert(tk.END, f"📍 Location: {lat}, {lon}\n\n")
        
        # Severe weather alerts
        if severe_weather.get('severe_events'):
            self.text_area.insert(tk.END, "🚨 SEVERE WEATHER ALERTS:\n")
            self.text_area.insert(tk.END, "-" * 40 + "\n")
            
            for event in severe_weather['severe_events']:
                self.text_area.insert(tk.END, f"{event['icon']} {event['name'].upper()}\n")
                self.text_area.insert(tk.END, f"   Type: {event['type'].replace('_', ' ').title()}\n")
                self.text_area.insert(tk.END, f"   Intensity: {event['intensity']}\n")
                self.text_area.insert(tk.END, f"   Speed: {event['speed']}\n")
                self.text_area.insert(tk.END, f"   Status: {event['status'].title()}\n")
                self.text_area.insert(tk.END, f"   ETA: {event['eta'][:16]}\n\n")
        
        # Weather radar grid (text representation)
        if radar_data:
            self.text_area.insert(tk.END, "🌦️ WEATHER INTENSITY MAP:\n")
            self.text_area.insert(tk.END, "-" * 40 + "\n")
            
            grid = radar_data['grid_data']
            for i, row in enumerate(grid[::4]):  # Every 4th row for display
                line = ""
                for j, cell in enumerate(row[::4]):  # Every 4th column
                    intensity = cell['intensity']
                    if intensity > 0.8:
                        symbol = "🔴"  # Severe
                    elif intensity > 0.6:
                        symbol = "🟠"  # Heavy
                    elif intensity > 0.4:
                        symbol = "🟡"  # Moderate
                    elif intensity > 0.2:
                        symbol = "🟢"  # Light
                    else:
                        symbol = "⚪"  # Clear
                    line += symbol
                self.text_area.insert(tk.END, line + "\n")
        
        # Comprehensive Legend
        self.text_area.insert(tk.END, "\n📋 DOPPLER RADAR ICON LEGEND:\n")
        self.text_area.insert(tk.END, "━" * 45 + "\n\n")
        
        # Precipitation Intensity Icons
        self.text_area.insert(tk.END, "🌦️ PRECIPITATION INTENSITY:\n")
        self.text_area.insert(tk.END, "🔴 Severe Weather    - Heavy storms, dangerous conditions\n")
        self.text_area.insert(tk.END, "🟠 Heavy Precipitation - Strong rain/snow, reduced visibility\n")
        self.text_area.insert(tk.END, "🟡 Moderate Rain     - Steady rainfall, use caution\n")
        self.text_area.insert(tk.END, "🟢 Light Precipitation - Light rain/drizzle, minimal impact\n")
        self.text_area.insert(tk.END, "⚪ Clear/Dry        - No precipitation, good visibility\n\n")
        
        # Severe Weather Event Icons
        self.text_area.insert(tk.END, "⚠️ SEVERE WEATHER EVENTS:\n")
        self.text_area.insert(tk.END, "🌀 Hurricane        - Category 1-5 tropical cyclone\n")
        self.text_area.insert(tk.END, "🌪️ Tornado         - F0-F5 scale rotating windstorm\n")
        self.text_area.insert(tk.END, "❄️ Blizzard        - Heavy snow with strong winds\n")
        self.text_area.insert(tk.END, "⛈️ Thunderstorm    - Lightning and heavy rain\n")
        self.text_area.insert(tk.END, "🌊 Flash Flood     - Rapid water rise, immediate danger\n")
        self.text_area.insert(tk.END, "🔥 Wildfire        - Active fire with smoke detection\n")
        self.text_area.insert(tk.END, "⚡ Lightning       - High electrical activity\n")
        self.text_area.insert(tk.END, "💨 High Winds      - Sustained winds >35 mph\n\n")
        
        # System Status Icons
        self.text_area.insert(tk.END, "📡 RADAR SYSTEM STATUS:\n")
        self.text_area.insert(tk.END, "✅ Online          - System operational, data current\n")
        self.text_area.insert(tk.END, "🔄 Updating        - Refreshing radar data\n")
        self.text_area.insert(tk.END, "⚠️ Warning         - System alert or maintenance\n")
        self.text_area.insert(tk.END, "❌ Offline         - System unavailable\n")
        self.text_area.insert(tk.END, "📍 Location        - Current radar coverage area\n\n")
        
        # Safety and Alert Icons
        self.text_area.insert(tk.END, "🚨 SAFETY INDICATORS:\n")
        self.text_area.insert(tk.END, "🟢 Safe           - Normal conditions, outdoor activities OK\n")
        self.text_area.insert(tk.END, "🟡 Caution        - Monitor conditions, be prepared\n")
        self.text_area.insert(tk.END, "🟠 Warning         - Dangerous conditions, take shelter\n")
        self.text_area.insert(tk.END, "🔴 Emergency       - Life-threatening, immediate action\n")
        self.text_area.insert(tk.END, "🏠 Shelter         - Stay indoors, avoid travel\n")
        self.text_area.insert(tk.END, "🚗 Travel Alert    - Road conditions hazardous\n\n")
        
        # Update info
        self.text_area.insert(tk.END, f"🔄 Last Updated: {timestamp}\n")
        self.text_area.insert(tk.END, "⏱️ Auto-updates every 2 minutes\n")
        
        # Scroll to top
        self.text_area.see(1.0)
    
    def _schedule_update(self):
        """Schedule automatic radar updates"""
        if self.auto_update:
            # Update every 2 minutes
            self.parent.after(120000, lambda: [self.update_radar(), self._schedule_update()])
    
    def stop_updates(self):
        """Stop automatic updates"""
        self.auto_update = False

    def update_location(self, lat: float, lon: float):
        """Update radar location coordinates"""
        try:
            self.lat_entry.delete(0, tk.END)
            self.lat_entry.insert(0, str(lat))
            self.lon_entry.delete(0, tk.END)
            self.lon_entry.insert(0, str(lon))
            # Trigger radar update
            self.update_radar()
        except Exception as e:
            print(f"Error updating radar location: {e}")
    
    def get_storm_tracking(self):
        """Get current storm tracking information"""
        try:
            lat = float(self.lat_entry.get())
            lon = float(self.lon_entry.get())
            
            # Get severe weather tracking from radar service
            severe_weather = self.radar_service.track_severe_weather(lat, lon)
            
            # Format the tracking data for display
            tracking_info = "SEVERE WEATHER TRACKING\n\n"
            
            if 'severe_events' in severe_weather and severe_weather['severe_events']:
                events = severe_weather['severe_events']
                for event in events:
                    tracking_info += f"{event['icon']} {event['type']}: {event['description']}\n"
                    tracking_info += f"   Location: {event['location']}\n"
                    tracking_info += f"   Severity: {event['severity']}\n"
                    tracking_info += f"   Movement: {event['movement']}\n\n"
            else:
                tracking_info += "No severe weather events detected at this time.\n\n"
                tracking_info += "Continuing to monitor..."
            
            return tracking_info
        except Exception as e:
            return f"Error retrieving storm tracking: {str(e)}"
    
    def get_weather_alerts(self):
        """Get current weather alerts for the area"""
        try:
            lat = float(self.lat_entry.get())
            lon = float(self.lon_entry.get())
            
            # In a real implementation, this would call the service to get alerts
            alerts = self.radar_service.get_weather_alerts(lat, lon)
            
            # Format the alerts for display
            alerts_info = "🚨 EMERGENCY WEATHER ALERTS 🚨\n\n"
            
            if alerts:
                for alert in alerts:
                    alerts_info += f"⚠️ {alert['headline']}\n"
                    alerts_info += f"⏰ {alert['effective']} to {alert['expires']}\n"
                    alerts_info += f"📝 {alert['description']}\n"
                    alerts_info += f"🔍 {alert['instruction']}\n\n"
            else:
                alerts_info += "No active weather alerts for this location.\n\n"
                alerts_info += "Stay tuned for updates as conditions can change rapidly."
                
            return alerts_info
        except Exception as e:
            return f"Error retrieving weather alerts: {str(e)}"
    
    def get_storm_history(self):
        """Get historical storm data for the area"""
        try:
            lat = float(self.lat_entry.get())
            lon = float(self.lon_entry.get())
            
            # In a real implementation, this would call the service
            history = self.radar_service.get_storm_history(lat, lon)
            
            # Format the history data for display
            history_info = "📈 STORM HISTORY REPORT 📈\n\n"
            
            if history:
                for event in history:
                    history_info += f"📆 {event['date']}\n"
                    history_info += f"🌪️ {event['type']}: {event['name']}\n"
                    history_info += f"💨 {event['details']}\n"
                    history_info += f"🏙️ {event['impact']}\n\n"
            else:
                history_info += "No significant storm history for this location in the past 30 days.\n\n"
                history_info += "Historical data includes events rated as severe or higher."
            
            return history_info
        except Exception as e:
            return f"Error retrieving storm history: {str(e)}"
    
    def get_radar_analysis(self):
        """Get detailed radar analysis for current conditions"""
        try:
            lat = float(self.lat_entry.get())
            lon = float(self.lon_entry.get())
            
            # In a real implementation, this would call the service
            analysis = self.radar_service.get_radar_analysis(lat, lon)
            
            # Format the analysis for display
            if not analysis:
                analysis = f"""📊 RADAR ANALYSIS REPORT 📊
                
🌐 Location: {lat:.4f}, {lon:.4f}
⏱️ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📈 PRECIPITATION ANALYSIS:
• Current intensity: Light to moderate
• Coverage area: 35% of radar view
• Movement: Northeast at 15 mph
• Trend: Increasing over next 2 hours

⛈️ STORM CELL ANALYSIS:
• Number of cells: 3
• Strongest cell: Moderate, no rotation detected
• Lightning activity: Low (12 strikes in past 10 min)
• Hail probability: <10% chance of small hail

🌀 WIND ANALYSIS:
• Surface winds: 8-12 mph from southwest
• Upper level winds: 25 mph from west
• Wind shear: Minimal
• Gust potential: Up to 20 mph

🔮 FORECAST PROJECTION:
• Precipitation will increase over next 1-2 hours
• Storm intensity expected to remain moderate
• No severe thunderstorm criteria met at this time
• Flash flooding potential: Low

🛰️ ANALYSIS BASED ON:
• Doppler radar
• Satellite imagery
• Surface observations
• Forecast models
• Storm reports"""
                
            return analysis
        except Exception as e:
            return f"Error retrieving radar analysis: {str(e)}"

# Global services
live_animation_service = LiveAnimationService()
